"""Read-only availability, version and TabDPT API checks. Does not download weights."""
import argparse,importlib,json,sys
from pathlib import Path
from src.execution import environment
ROOT=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--strict-versions',action='store_true');args=parser.parse_args()
    actual=environment();print(json.dumps(actual,indent=2))
    cfg=json.loads((ROOT/'configs/models.json').read_text());errors=[];mismatches=[]
    for name,module in [('TabPFN','tabpfn'),('TabICL','tabicl'),('TabDPT','tabdpt'),('AutoGluon','autogluon.tabular'),('CatBoost','catboost')]:
        try:importlib.import_module(module);print(f'IMPORT OK: {name}')
        except Exception as exc:errors.append(f'{name}: {type(exc).__name__}: {exc}')
    for name,record in cfg.get('versions',{}).items():
        package=record.get('package');expected=record.get('version')
        if package and expected and actual['packages'].get(package)!=expected:mismatches.append(f'{package}: expected {expected}; actual {actual["packages"].get(package)}')
        for package,expected in record.items():
            if package in {'package','version'}:continue
            if actual['packages'].get(package)!=expected:mismatches.append(f'{package}: expected {expected}; actual {actual["packages"].get(package)}')
    try:
        from autogluon.tabular.models.tabdpt.tabdpt_model import TabDPTModel
        import inspect
        print('TabDPT wrapper source:',inspect.getfile(TabDPTModel))
        seed_name=getattr(TabDPTModel,'seed_name',None);print('TabDPT seed parameter:',seed_name)
        if seed_name!='seed':errors.append('Installed TabDPT wrapper seed API needs verification.')
    except Exception as exc:errors.append(f'TabDPT API: {exc}')
    for text in mismatches:print('VERSION NOTICE:',text)
    for text in errors:print('ERROR:',text)
    print('Checkpoint hashes in models.json are historical declarations, NOT proof of weights loaded. Actual inference still requires a smoke run.')
    return 1 if errors or (args.strict_versions and mismatches) else 0

if __name__=='__main__':sys.exit(main())
