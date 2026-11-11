"""Common CLI for binary datasets, with isolated workers and guarded resume."""
import argparse,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name,default in [('datasets','sonar'),('models','all'),('seeds','all'),('output','results_v2')]:parser.add_argument('--'+name,default=default)
    parser.add_argument('--threads',type=int)
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--validate-only',action='store_true')
    parser.add_argument('--worker',help=argparse.SUPPRESS)
    args=parser.parse_args()
    from src.execution import worker,run_job,export_tables,environment,atomic_json,sha256
    if args.worker:worker(args.worker);return
    from src.validation import validate_experiment,safe_name,MODELS
    from src.data import load_dataset
    from src.splits import make_splits
    exp=json.loads((ROOT/'configs/experiment.json').read_text())
    mc=json.loads((ROOT/'configs/models.json').read_text())
    seeds=exp['seeds'] if args.seeds=='all' else [int(x.strip()) for x in args.seeds.split(',')]
    threads=args.threads if args.threads is not None else exp['threads'];exp['threads']=threads
    validate_experiment(dict(exp,seeds=seeds))
    models=mc['models'] if args.models=='all' else [x.strip() for x in args.models.split(',')]
    if not models or len(models)!=len(set(models)) or set(models)-set(MODELS):raise ValueError('Invalid/duplicate models.')
    paths=sorted(p for p in (ROOT/'configs/datasets').glob('*.json') if p.stem!='template') if args.datasets=='all' else [ROOT/'configs/datasets'/f'{safe_name(n.strip())}.json' for n in args.datasets.split(',')]
    if not paths:raise ValueError('No datasets selected.')
    datasets=[json.loads(p.read_text()) for p in paths];names=[safe_name(d['name']) for d in datasets]
    if len(names)!=len(set(names)):raise ValueError('Duplicate datasets.')
    identities={}
    for cfg in datasets:
        X,y,meta=load_dataset(cfg,ROOT)
        for seed in seeds:make_splits(y,seed,exp['split'])
        identities[cfg['name']]={'config':cfg,'sha256':meta['source_sha256']}
        print(f'VALID: {cfg["name"]}: {len(X)} rows, {X.shape[1]} features; {meta["n_categorical"]} categorical; {meta["original_missing_cells"]} missing cells',flush=True)
    if args.validate_only:print('Data/config/splits passed; models have not been executed.');return
    env=environment()
    req={'TabPFN-v2':['tabpfn','torch'],'TabICLv2':['tabicl','torch'],'TabDPT':['autogluon.tabular','tabdpt','torch'],'CatBoost':['catboost'],'MLP':['scikit-learn']}
    missing=sorted({p for m in models for p in req[m] if env['packages'].get(p) is None})
    if missing:raise RuntimeError(f'Missing selected model dependencies: {missing}')
    for m in models:
        d=mc.get('versions',{}).get(m,{});package=d.get('package');version=d.get('version')
        if package and version and env['packages'].get(package)!=version:print(f'NOTICE: {package}: installed {env["packages"].get(package)}, declared {version}; recording actual environment.',flush=True)
    output=(ROOT/args.output).resolve()
    if output.exists() and any(output.iterdir()) and not args.resume:raise ValueError('Output not empty. Use --resume for the same protocol or a NEW --output folder.')
    output.mkdir(parents=True,exist_ok=True);lock=output/'.run.lock'
    try:fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    except FileExistsError:raise RuntimeError('Output locked. If interrupted, verify no run is active before removing .run.lock.')
    os.write(fd,str(os.getpid()).encode());os.close(fd)
    try:
        protocol={'experiment':exp,'models_config':mc,'environment':env,'source':{str(p.relative_to(ROOT)):sha256(p) for p in sorted((ROOT/'src').glob('*.py'))},'run_py':sha256(ROOT/'run.py')}
        manifest=output/'run_manifest.json'
        if manifest.exists():
            old=json.loads(manifest.read_text())
            if old['protocol']!=protocol:raise ValueError('Protocol/code/environment changed. Use a NEW --output folder.')
            for name,identity in identities.items():
                if name in old['datasets'] and old['datasets'][name]!=identity:raise ValueError(f'Dataset {name} changed. Use a NEW output folder.')
            identities={**old['datasets'],**identities}
        elif any(p.name!='.run.lock' for p in output.iterdir()):raise ValueError('Cannot resume legacy output without v2 manifest. Use a NEW folder.')
        atomic_json(manifest,{'protocol':protocol,'datasets':identities});failures=[]
        for cfg in datasets:
            for seed in seeds:
                for model in models:
                    try:run_job(ROOT,output,cfg,exp,model,seed,threads,args.resume,env)
                    except Exception as exc:
                        failures.append({'dataset':cfg['name'],'seed':seed,'model':model,'error':str(exc)});print(f'FAILED: {exc}',flush=True)
                    export_tables(output)
        atomic_json(output/'last_invocation.json',{'datasets':names,'models':models,'seeds':seeds,'failures':failures})
        if failures:raise RuntimeError(f'{len(failures)} failed jobs; see last_invocation.json and _attempts. Completed jobs retained.')
        print(f'Completed selected grid. Output: {output}')
    finally:lock.unlink(missing_ok=True)

if __name__=='__main__':
    try:main()
    except Exception as exc:print(f'{type(exc).__name__}: {exc}',file=sys.stderr);sys.exit(1)
