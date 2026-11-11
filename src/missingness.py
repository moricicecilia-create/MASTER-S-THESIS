from __future__ import annotations
import numpy as np
import pandas as pd


def make_mask(shape, pattern: str, rate: float, seed: int):
    if pattern not in {"reference", "cell", "feature"} or not np.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("Invalid missingness pattern or rate.")
    n_rows, n_cols = shape
    if pattern == "reference" or rate == 0:
        return np.zeros(shape, dtype=bool)
    rng = np.random.default_rng(seed)
    if pattern == "cell":
        return rng.random(shape) < rate
    if pattern == "feature":
        n_masked = int(round(n_cols * rate))
        mask = np.zeros(shape, dtype=bool)
        if n_masked:
            cols = rng.choice(n_cols, size=n_masked, replace=False)
            mask[:, cols] = True
        return mask
    raise ValueError(f"Unknown missingness pattern: {pattern}")


def apply_mask(X: pd.DataFrame, mask: np.ndarray):
    if mask.shape != X.shape:
        raise ValueError(f"Mask shape {mask.shape} does not match X shape {X.shape}.")
    out = X.copy(deep=True)
    return out.mask(mask)


def scenario_specs(experiment_config: dict):
    miss = experiment_config["missingness"]
    scenarios = [("reference", 0.0)]
    scenarios += [("cell", float(r)) for r in miss["cell_rates"]]
    scenarios += [("feature", float(r)) for r in miss["feature_rates"]]
    return scenarios


def scenario_name(pattern, rate):
    return "reference" if pattern == "reference" else f"{pattern}_{format(float(rate)*100, '.12g')}"
