"""One fresh subprocess per dataset/model/seed; immutable completed job folders."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import random
import subprocess
import sys
import time
import uuid


def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()


def environment():
    packages={}
    for name in ('numpy','pandas','scipy','scikit-learn','torch','tabpfn','tabicl','tabdpt','autogluon.tabular','catboost','psutil','matplotlib','threadpoolctl'):
        try: packages[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError: packages[name]=None
    return {'python':platform.python_version(),'platform':platform.platform(),'packages':packages}


def atomic_json(path, value):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    temp.write_text(json.dumps(value,indent=2,allow_nan=False),encoding='utf-8');os.replace(temp,path)


def fingerprint(root, dataset_cfg, exp_cfg, model, seed, threads, env):
    path=Path(dataset_cfg['path'])
    if not path.is_absolute(): path=Path(root)/path
    source={str(p.relative_to(root)):sha256(p) for p in sorted((Path(root)/'src').glob('*.py'))}
    source['run.py']=sha256(Path(root)/'run.py')
    payload={'dataset':dataset_cfg,'data_sha256':sha256(path),'experiment':exp_cfg,'model':model,
             'seed':seed,'threads':threads,'source':source,'environment':env,
             'models_config':json.loads((Path(root)/'configs/models.json').read_text())}
    return hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()


def completed(job, expected):
    job=Path(job); marker=job/'complete.json'
    if not marker.exists(): return False
    record=json.loads(marker.read_text())
    if record['fingerprint'] != expected: raise ValueError(f'Configuration, code, data or environment changed for {job}. Use a NEW --output folder.')
    for name,digest in record['files'].items():
        if not (job/name).is_file() or sha256(job/name)!=digest:
            raise ValueError(f'Incomplete or modified result: {job/name}. Use a new output folder.')
    return True


def worker(spec_path):
    # Invoked in a new interpreter, never in the orchestrator process.
    spec=json.loads(Path(spec_path).read_text()); stage=Path(spec['stage'])
    seed=spec['seed'];random.seed(seed)
    if spec['experiment'].get('allow_large_tabpfn_cpu',False):
        os.environ['TABPFN_ALLOW_CPU_LARGE_DATASET']='1'
    import numpy as np
    import pandas as pd
    np.random.seed(seed)
    if spec['model'] in ('TabPFN-v2','TabICLv2','TabDPT'):
        import torch
        torch.manual_seed(seed);torch.set_num_threads(spec['threads'])
    from threadpoolctl import threadpool_limits
    from .data import load_dataset
    from .splits import make_splits
    from .experiment import run_one_model_seed
    from .missingness import scenario_specs
    X,y,metadata=load_dataset(spec['dataset'],Path(spec['root']))
    splits=make_splits(y,seed,spec['experiment']['split'])
    t0=time.perf_counter()
    with threadpool_limits(limits=spec['threads']):
        rows,probs,status=run_one_model_seed(spec['dataset']['name'],spec['model'],seed,X,y,metadata,splits,
                                           spec['experiment'],stage,spec['threads'])
    status['worker_execution_seconds']=time.perf_counter()-t0
    atomic_json(stage/'dataset_metadata.json',metadata)
    pd.DataFrame([status]).to_csv(stage/'model_status.csv',index=False)
    if status['status']!='success': raise RuntimeError(status['error'])
    expected=len(scenario_specs(spec['experiment']))*len(spec['experiment']['calibration']['methods'])
    frame=pd.DataFrame(rows)
    if len(frame)!=expected or frame.duplicated(['missing_pattern','missing_rate','calibration']).any():
        raise RuntimeError('Incomplete or duplicate experimental grid.')
    if not np.isfinite(frame[['AUROC','balanced_acc','logloss','brier','ECE']]).all().all():
        raise RuntimeError('Nonfinite metrics.')
    frame.to_csv(stage/'all_results_long.csv',index=False)
    pd.DataFrame(probs).to_csv(stage/'probabilities_long.csv',index=False)
    names=('all_results_long.csv','probabilities_long.csv','model_status.csv','split_indices.csv','dataset_metadata.json')
    atomic_json(stage/'complete.json',{'fingerprint':spec['fingerprint'],'files':{n:sha256(stage/n) for n in names}})


def run_job(root,output,dataset,exp,model,seed,threads,resume,env):
    job=Path(output)/'jobs'/dataset['name']/model/f'seed_{seed}'
    digest=fingerprint(root,dataset,exp,model,seed,threads,env)
    if job.exists():
        if resume and completed(job,digest):
            print(f'RESUME: {dataset["name"]} | {model} | {seed}',flush=True);return
        raise ValueError(f'Job already exists: {job}. Use --resume or a new output folder.')
    stage=Path(output)/'_attempts'/f'{dataset["name"]}_{model}_{seed}_{uuid.uuid4().hex}'
    stage.mkdir(parents=True)
    spec={'root':str(root),'stage':str(stage),'dataset':dataset,'experiment':exp,'model':model,
          'seed':seed,'threads':threads,'fingerprint':digest}
    atomic_json(stage/'job_spec.json',spec)
    child_env=os.environ.copy()
    for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        child_env[key]=str(threads)
    child_env['PYTHONHASHSEED']=str(seed)
    print(f'RUN: {dataset["name"]} | {model} | {seed}',flush=True)
    with (stage/'execution.log').open('w',encoding='utf-8') as log:
        result=subprocess.run([sys.executable,str(Path(root)/'run.py'),'--worker',str(stage/'job_spec.json')],
                              cwd=root,env=child_env,stdout=log,stderr=subprocess.STDOUT)
    if result.returncode or not completed(stage,digest):
        raise RuntimeError(f'Execution failed; diagnostics retained in {stage}/execution.log')
    job.parent.mkdir(parents=True,exist_ok=True); stage.rename(job)


def export_tables(output):
    import pandas as pd
    from .aggregation import aggregate_results,paired_differences
    root=Path(output);jobs=sorted((root/'jobs').glob('*/*/seed_*'))
    tables={n:[] for n in ('all_results_long','probabilities_long','model_status','split_indices')}
    for job in jobs:
        marker=json.loads((job/'complete.json').read_text());completed(job,marker['fingerprint'])
        for n in tables: tables[n].append(pd.read_csv(job/(n+'.csv')))
    if not jobs:return
    merged={n:pd.concat(v,ignore_index=True) for n,v in tables.items()}
    merged['split_indices']=merged['split_indices'].drop_duplicates()
    def save(frame,path):
        temp=path.with_suffix('.tmp');frame.to_csv(temp,index=False);os.replace(temp,path)
    for n,frame in merged.items(): save(frame,root/(n+'.csv'))
    for dataset in merged['all_results_long'].dataset.unique():
        folder=root/dataset;folder.mkdir(exist_ok=True)
        for n,frame in merged.items():save(frame[frame.dataset==dataset],folder/(n+'.csv'))
        frame=merged['all_results_long'].query('dataset == @dataset')
        save(aggregate_results(frame),folder/'aggregate_results.csv')
        if 'No additional calibration' in set(frame.calibration):save(paired_differences(frame),folder/'paired_differences.csv')
    frame=merged['all_results_long']
    save(aggregate_results(frame),root/'aggregate_results_all_datasets.csv')
    if 'No additional calibration' in set(frame.calibration):save(paired_differences(frame),root/'paired_differences_all_datasets.csv')
