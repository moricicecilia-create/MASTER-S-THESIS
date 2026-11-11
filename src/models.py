from __future__ import annotations
import copy
import shutil
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import log_loss


class TabDPTAdapter:
    """AutoGluon wrapper for frozen TabDPT inference; no downstream fine-tuning."""
    def __init__(self, seed: int, threads: int, artifact_path: Path):
        self.seed = seed
        self.threads = threads
        self.artifact_path = Path(artifact_path)
        self.predictor = None

    def fit(self, X_train, y_train, X_val, y_val):
        from autogluon.tabular import TabularPredictor
        if self.artifact_path.exists():
            shutil.rmtree(self.artifact_path)
        self.artifact_path.mkdir(parents=True, exist_ok=True)
        train = X_train.copy() if isinstance(X_train, pd.DataFrame) else pd.DataFrame(X_train)
        valid = X_val.copy() if isinstance(X_val, pd.DataFrame) else pd.DataFrame(X_val)
        train["__target__"] = np.asarray(y_train, dtype=int)
        valid["__target__"] = np.asarray(y_val, dtype=int)
        self.predictor = TabularPredictor(
            label="__target__", problem_type="binary", path=str(self.artifact_path), verbosity=0
        )
        from autogluon.tabular.models.tabdpt.tabdpt_model import TabDPTModel
        if getattr(TabDPTModel, "seed_name", None) != "seed":
            raise RuntimeError("This AutoGluon TabDPT adapter does not declare seed_name=seed; verify installed API before benchmarking.")
        self.predictor.fit(
            train_data=train,
            tuning_data=valid,
            hyperparameters={"TABDPT": [{"seed": self.seed}]},
            calibrate=False,
            calibrate_decision_threshold=False,
            num_gpus=0,
            num_cpus=self.threads,
            fit_weighted_ensemble=False,
            dynamic_stacking=False,
            raise_on_model_failure=True,
        )
        return self

    def predict_proba(self, X):
        frame = X.copy() if isinstance(X, pd.DataFrame) else pd.DataFrame(X)
        return self.predictor.predict_proba(frame)


def fit_mlp_with_validation_early_stopping(X_train, y_train, X_val, y_val, config, seed):
    """Use partial_fit epochs and explicit validation log-loss for early stopping."""
    model = MLPClassifier(
        hidden_layer_sizes=tuple(config.get("hidden_layer_sizes", [64, 32])),
        activation="relu",
        solver="adam",
        alpha=float(config.get("alpha", 1e-4)),
        learning_rate_init=float(config.get("learning_rate_init", 1e-3)),
        max_iter=1,
        random_state=seed,
        shuffle=True,
        early_stopping=False,
        warm_start=True,
    )
    classes = np.array([0, 1], dtype=int)
    best_loss = float("inf")
    best_coefs = None
    best_intercepts = None
    best_epoch = 0
    patience = int(config.get("patience", 30))
    max_epochs = int(config.get("max_epochs", 500))
    stale = 0
    for epoch in range(1, max_epochs + 1):
        if epoch == 1:
            model.partial_fit(X_train, y_train, classes=classes)
        else:
            model.partial_fit(X_train, y_train)
        val_p = model.predict_proba(X_val)[:, 1]
        current_loss = float(log_loss(y_val, val_p, labels=[0, 1]))
        if current_loss < best_loss - 1e-7:
            best_loss = current_loss
            best_coefs = [w.copy() for w in model.coefs_]
            best_intercepts = [b.copy() for b in model.intercepts_]
            best_epoch = epoch
            stale = 0
        else:
            stale += 1
        if stale >= patience:
            break
    if best_coefs is None:
        raise RuntimeError("MLP did not produce a valid checkpoint.")
    model.coefs_ = best_coefs
    model.intercepts_ = best_intercepts
    model.best_epoch_ = best_epoch
    model.best_validation_logloss_ = best_loss
    return model


def make_model(model_name: str, seed: int, threads: int, artifact_dir: Path):
    if model_name == "TabPFN-v2":
        from tabpfn import TabPFNClassifier
        from tabpfn.constants import ModelVersion
        return TabPFNClassifier.create_default_for_version(
            ModelVersion.V2, device="cpu", n_estimators=8,
            random_state=seed, n_preprocessing_jobs=1, show_progress_bar=False
        )
    if model_name == "TabICLv2":
        from tabicl import TabICLClassifier
        return TabICLClassifier(
            checkpoint_version="tabicl-classifier-v2-20260212.ckpt",
            device="cpu", n_estimators=8, n_jobs=threads,
            random_state=seed, verbose=False
        )
    if model_name == "TabDPT":
        return TabDPTAdapter(seed, threads, artifact_dir / f"tabdpt_seed_{seed}")
    if model_name == "CatBoost":
        from catboost import CatBoostClassifier
        return CatBoostClassifier(
            iterations=500, learning_rate=0.03, depth=6, l2_leaf_reg=3,
            loss_function="Logloss", eval_metric="AUC", random_seed=seed,
            thread_count=threads, verbose=False
        )
    if model_name == "MLP":
        return "MLP_EARLY_STOPPING"
    raise ValueError(f"Unknown model: {model_name}")


def fit_model(model_name, model, X_train, y_train, X_val, y_val, mlp_config, seed):
    if model_name == "MLP":
        return fit_mlp_with_validation_early_stopping(
            X_train, y_train, X_val, y_val, mlp_config, seed
        )
    if model_name == "CatBoost":
        cat_features = [c for c in X_train.columns if str(X_train[c].dtype) in {"object", "category", "string"}] if isinstance(X_train, pd.DataFrame) else None
        model.fit(
            X_train, y_train, eval_set=(X_val, y_val),
            use_best_model=True, early_stopping_rounds=50,
            cat_features=cat_features or None, verbose=False
        )
        return model
    if model_name == "TabDPT":
        return model.fit(X_train, y_train, X_val, y_val)
    return model.fit(X_train, y_train)


def positive_probability(model, X):
    probs = model.predict_proba(X)
    if isinstance(probs, pd.DataFrame):
        if 1 in probs.columns:
            values = probs[1].to_numpy(dtype=float)
            if not np.isfinite(values).all() or np.any((values < 0) | (values > 1)):
                raise ValueError("Invalid probabilities.")
            return values
        if "1" in probs.columns:
            values = probs["1"].to_numpy(dtype=float)
            if not np.isfinite(values).all() or np.any((values < 0) | (values > 1)):
                raise ValueError("Invalid probabilities.")
            return values
        raise ValueError(f"Cannot identify positive class in probability columns: {list(probs.columns)}")
    probs = np.asarray(probs)
    if probs.ndim != 2 or probs.shape[1] != 2 or not np.isfinite(probs).all() or np.any((probs < 0) | (probs > 1)):
        raise ValueError("Invalid binary probability output.")
    classes = np.asarray(getattr(model, "classes_", [0, 1]))
    matches = np.flatnonzero(classes == 1)
    if len(matches) != 1:
        raise ValueError(f"Cannot identify class 1 in model classes: {classes}")
    return probs[:, int(matches[0])].astype(float)
