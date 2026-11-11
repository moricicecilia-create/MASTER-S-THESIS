from __future__ import annotations
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import expit, logit


def apply_temperature(probabilities, temperature: float):
    if not np.isfinite(temperature) or temperature <= 0:
        raise ValueError("Temperature must be finite and positive.")
    probabilities = np.asarray(probabilities, dtype=float)
    if not np.isfinite(probabilities).all() or np.any((probabilities < 0) | (probabilities > 1)):
        raise ValueError("Probabilities must be finite and within [0,1].")
    p = np.clip(probabilities, 1e-7, 1 - 1e-7)
    return expit(logit(p) / float(temperature))


def fit_temperature(y_true, probabilities, lower=0.05, upper=20.0, sample_weight=None):
    if not 0 < lower < upper or not np.isfinite([lower,upper]).all():
        raise ValueError("Invalid temperature bounds.")
    raw = np.asarray(probabilities, dtype=float)
    if not np.isfinite(raw).all() or np.any((raw < 0) | (raw > 1)):
        raise ValueError("Invalid probabilities.")
    y = np.asarray(y_true, dtype=int)
    p = np.clip(np.asarray(probabilities, dtype=float), 1e-12, 1 - 1e-12)
    if len(y) != len(p) or len(y) == 0:
        raise ValueError("Calibration labels and probabilities must be non-empty and have equal length.")
    if set(np.unique(y)) != {0, 1}:
        raise ValueError("Temperature scaling requires both classes in the calibration subset.")
    weights = np.ones(len(y), dtype=float) if sample_weight is None else np.asarray(sample_weight, dtype=float)
    if len(weights) != len(y) or not np.isfinite(weights).all() or np.any(weights < 0) or weights.sum() <= 0:
        raise ValueError("Invalid calibration sample weights.")

    def objective(log_t):
        q = np.clip(apply_temperature(p, np.exp(log_t)), 1e-12, 1 - 1e-12)
        losses = -(y * np.log(q) + (1 - y) * np.log1p(-q))
        return float(np.average(losses, weights=weights))

    result = minimize_scalar(objective, bounds=(np.log(lower), np.log(upper)), method="bounded")
    if not result.success:
        raise RuntimeError(f"Temperature optimization failed: {result.message}")
    return float(np.exp(result.x))
