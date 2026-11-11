from __future__ import annotations
import numpy as np
from sklearn.model_selection import train_test_split


def make_splits(y, seed: int, ratios: dict):
    y = np.asarray(y)
    names = ("train_context", "validation", "calibration", "test")
    vals = [float(ratios[k]) for k in names]
    if not np.isclose(sum(vals), 1.0):
        raise ValueError(f"Split ratios must sum to 1.0; got {sum(vals)}")
    if min(vals) <= 0:
        raise ValueError("Every split ratio must be positive.")

    indices = np.arange(len(y))
    test_ratio = vals[3]
    remaining_idx, test_idx = train_test_split(
        indices, test_size=test_ratio, stratify=y, random_state=seed
    )
    remaining_fraction = 1.0 - test_ratio
    cal_relative = vals[2] / remaining_fraction
    train_val_idx, cal_idx = train_test_split(
        remaining_idx, test_size=cal_relative,
        stratify=y[remaining_idx], random_state=seed
    )
    train_val_fraction = vals[0] + vals[1]
    val_relative = vals[1] / train_val_fraction
    train_idx, val_idx = train_test_split(
        train_val_idx, test_size=val_relative,
        stratify=y[train_val_idx], random_state=seed
    )
    result = {
        "train_context": np.asarray(train_idx),
        "validation": np.asarray(val_idx),
        "calibration": np.asarray(cal_idx),
        "test": np.asarray(test_idx),
    }
    flattened = np.concatenate(list(result.values()))
    if len(flattened) != len(y) or len(np.unique(flattened)) != len(y):
        raise RuntimeError("Split indices are not a disjoint partition of the full dataset.")
    for name, idx in result.items():
        if len(np.unique(y[idx])) != 2:
            raise ValueError(f"Split '{name}' does not contain both target classes.")
    return result
