"""Recompute metrics from probabilities and check the last requested grid."""
import argparse,json,sys
from pathlib import Path
import numpy as np
import pandas as pd
from src.metrics import calculate_metrics
from src.execution import completed
from src.missingness import scenario_specs,scenario_name

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='results_v2');args=parser.parse_args()
    root=(Path(__file__).resolve().parent/args.output).resolve()
    manifest=json.loads((root/'run_manifest.json').read_text());inv=json.loads((root/'last_invocation.json').read_text())
    if inv['failures']:raise ValueError('Last invocation has failed jobs; inspect last_invocation.json.')
    cfg=manifest['protocol']['experiment'];methods=cfg['calibration']['methods'];scenes=scenario_specs(cfg)
    checked=0
    for dataset in inv['datasets']:
        for model in inv['models']:
            for seed in inv['seeds']:
                job=root/'jobs'/dataset/model/f'seed_{seed}';marker=json.loads((job/'complete.json').read_text())
                if not completed(job,marker['fingerprint']):raise ValueError('Missing completed job.')
                r=pd.read_csv(job/'all_results_long.csv');p=pd.read_csv(job/'probabilities_long.csv')
                if len(r)!=len(scenes)*len(methods):raise ValueError('Incorrect row count.')
                if p.duplicated(['subset','scenario','observation_id','calibration']).any():raise ValueError('Duplicate probabilities.')
                for pattern,rate in scenes:
                    for method in methods:
                        a=r[(r.missing_pattern==pattern)&np.isclose(r.missing_rate,rate)&(r.calibration==method)]
                        if len(a)!=1:raise ValueError('Missing/duplicate experimental combination.')
                        a=a.iloc[0];q=p[(p.subset=='test')&(p.scenario==scenario_name(pattern,rate))&(p.calibration==method)]
                        if len(q)!=a.n_test:raise ValueError('Incorrect test prediction count.')
                        got=calculate_metrics(q.y_true,q.calibrated_probability,cfg['calibration']['ece_bins'])
                        for name,value in got.items():
                            if not np.isclose(value,a[name],rtol=1e-8,atol=1e-10):raise ValueError(f'Metric mismatch: {name}')
                        checked+=1
    print(f'PASS: {checked} conditions in the last requested grid; integrity, counts and five recomputed metrics.')

if __name__=='__main__':main()
