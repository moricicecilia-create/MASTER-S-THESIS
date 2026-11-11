from pathlib import Path
import hashlib
import numpy as np
import pandas as pd


def load_dataset(config, root):
    """Load binary tabular data without learning transformations on held-out rows."""
    path = Path(config['path'])
    if not path.is_absolute(): path = Path(root) / path
    fmt = config.get('format', 'csv').lower()
    if fmt == 'csv':
        raw = pd.read_csv(path, header=config.get('header', 0), sep=config.get('separator', ','),
                          encoding=config.get('encoding','utf-8'), na_values=config.get('na_values'),
                          keep_default_na=config.get('keep_default_na', True))
        if config.get('header',0) is None:
            names = config.get('column_names')
            if names is None and config['name'].lower() == 'sonar' and raw.shape[1] == 61:
                names = [f"{config.get('feature_prefix','feature_')}{i}" for i in range(1,61)] + [config['target_column']]
            if not names or len(names) != raw.shape[1]:
                raise ValueError('Headerless CSV requires column_names matching its columns.')
            raw.columns = names
    elif fmt == 'arff':
        from scipy.io import arff
        with path.open(encoding=config.get('encoding','utf-8')) as stream:
            records, _ = arff.loadarff(stream)
        raw = pd.DataFrame(records)
        for col in raw.select_dtypes(include=['object']).columns:
            raw[col] = raw[col].map(lambda x: x.decode(config.get('encoding','utf-8')) if isinstance(x,bytes) else x)
        raw = raw.replace('?',np.nan)
    else:
        raise ValueError(f'Unsupported format {fmt!r}; supported: csv, arff.')
    raw.columns = raw.columns.map(str)
    if not raw.columns.is_unique: raise ValueError('Duplicate column names.')
    target = str(config['target_column'])
    if target not in raw: raise ValueError(f'Target {target!r} not found.')
    if raw[target].isna().any(): raise ValueError('Target contains missing values.')
    # Always honour the declared positive class, including numeric 0/1 targets.
    def label(x):
        if isinstance(x,(float,np.floating)) and np.isfinite(x) and x.is_integer(): return str(int(x))
        return str(x).strip()
    negative, positive = label(config['negative_class']), label(config['positive_class'])
    if negative == positive: raise ValueError('Positive and negative labels must differ.')
    labels = raw[target].map(label)
    if set(labels.unique()) != {negative,positive}:
        raise ValueError(f'Target must contain exactly declared classes {negative!r}, {positive!r}; found {sorted(labels.unique())}. No implicit binarization.')
    y = labels.map({negative:0,positive:1}).to_numpy(dtype=int)
    drop = list(config.get('drop_columns',[]))
    if set(drop)-set(raw.columns): raise ValueError('Unknown drop_columns.')
    X = raw.drop(columns=list(dict.fromkeys([target]+drop))).copy()
    if X.shape[1] == 0: raise ValueError('No predictor columns remain.')
    cats, nums = list(config.get('categorical_columns',[])), list(config.get('numeric_columns',[]))
    if set(cats)&set(nums): raise ValueError('Numeric and categorical overrides overlap.')
    if (set(cats)|set(nums))-set(X.columns): raise ValueError('Unknown feature overrides.')
    categorical = list(dict.fromkeys(cats+[c for c in X if c not in nums and not pd.api.types.is_numeric_dtype(X[c])]))
    numeric = [c for c in X if c not in categorical]
    for c in numeric:
        X[c] = pd.to_numeric(X[c],errors='raise').astype(float)
        if np.isinf(X[c]).any(): raise ValueError(f'Infinite values in {c}.')
    for c in categorical:
        X[c] = X[c].map(lambda v: str(v) if pd.notna(v) else np.nan).astype(object)
    metadata = {'n_rows':len(X),'n_features':X.shape[1], 'n_numeric':len(numeric),'n_categorical':len(categorical),
                'class_counts':{'0':int((y==0).sum()),'1':int((y==1).sum())},
                'target_mapping':{negative:0,positive:1}, 'duplicate_rows':int(raw.duplicated().sum()),
                'duplicate_predictors':int(X.duplicated().sum()),
                'original_missing_cells':int(X.isna().sum().sum()),'feature_columns':list(X.columns),
                'numeric_columns':numeric,'categorical_columns':categorical,'source_path':str(path),
                'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    if metadata['duplicate_predictors'] and config.get('duplicate_policy','error') != 'allow':
        raise ValueError('Duplicate predictor rows detected. Resolve duplicates/grouping or explicitly set duplicate_policy="allow" and document the limitation.')
    return X.reset_index(drop=True), y, metadata
