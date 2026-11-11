from __future__ import annotations
import numpy as np
from sklearn.metrics import roc_auc_score, balanced_accuracy_score, log_loss, brier_score_loss


def positive_class_ece(y_true, probabilities, n_bins=5):
    """ECE for the positive-class probability; uses the same uniform bins as the reliability plot."""
    y = np.asarray(y_true, dtype=int)
    p = np.asarray(probabilities, dtype=float)
    if len(y) != len(p) or len(y) == 0:
        raise ValueError("y_true and probabilities must be non-empty and have equal length.")
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    total = 0.0
    for i in range(n_bins):
        if i == n_bins - 1:
            mask = (p >= edges[i]) & (p <= edges[i + 1])
        else:
            mask = (p >= edges[i]) & (p < edges[i + 1])
        if mask.any():
            total += mask.mean() * abs(float(y[mask].mean()) - float(p[mask].mean()))
    return float(total)


def calculate_metrics(y_true, probabilities, ece_bins=5):
    raw = np.asarray(probabilities, dtype=float)
    if not np.isfinite(raw).all() or np.any((raw < 0) | (raw > 1)):
        raise ValueError("Probabilities must be finite and in [0,1].")
    y = np.asarray(y_true, dtype=int)
    if set(np.unique(y)) != {0,1}:
        raise ValueError("Metrics require binary labels and both classes.")
    p = np.clip(np.asarray(probabilities, dtype=float), 1e-12, 1 - 1e-12)
    pred = (p >= 0.5).astype(int)
    return {
        "AUROC": float(roc_auc_score(y, p)),
        "balanced_acc": float(balanced_accuracy_score(y, pred)),
        "logloss": float(log_loss(y, p, labels=[0, 1])),
        "brier": float(brier_score_loss(y, p)),
        "ECE": positive_class_ece(y, p, n_bins=ece_bins),
    }


def reliability_bins(y_true, probabilities, n_bins=5):
    y = np.asarray(y_true, dtype=int)
    p = np.asarray(probabilities, dtype=float)
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    rows = []
    for i in range(n_bins):
        mask = (p >= edges[i]) & ((p <= edges[i + 1]) if i == n_bins - 1 else (p < edges[i + 1]))
        rows.append({
            "bin": i + 1,
            "lower": float(edges[i]),
            "upper": float(edges[i + 1]),
            "count": int(mask.sum()),
            "mean_probability": float(p[mask].mean()) if mask.any() else np.nan,
            "fraction_positive": float(y[mask].mean()) if mask.any() else np.nan,
        })
    return rows
