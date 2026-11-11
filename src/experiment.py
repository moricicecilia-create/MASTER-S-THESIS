from __future__ import annotations
import gc
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
from .missingness import make_mask, apply_mask, scenario_specs, scenario_name
from .preprocessing import ModelPreprocessor
from .models import make_model, fit_model, positive_probability
from .calibration import fit_temperature, apply_temperature
from .metrics import calculate_metrics
from .monitoring import PeakMemoryMonitor
from .plots import save_reliability_figure


def _prepare_inputs(preprocessor, X_train, X_val, X_cal, X_test_scenarios):
    t0 = time.perf_counter()
    preprocessor.fit(X_train)
    transformed = {"train": preprocessor.transform(X_train),
                   "validation": preprocessor.transform(X_val)}
    return transformed, time.perf_counter() - t0


def run_one_model_seed(dataset_name, model_name, seed, X, y, metadata, split_indices,
                       experiment_cfg, output_dir, threads):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    splits_file = output_dir / "split_indices.csv"
    split_rows = []
    for split_name, ids in split_indices.items():
        split_rows.extend({"dataset": dataset_name, "split_seed": seed,
                           "observation_id": int(i), "split": split_name} for i in ids)
    split_df = pd.DataFrame(split_rows)
    if splits_file.exists():
        old = pd.read_csv(splits_file)
        old = old.loc[~((old.dataset == dataset_name) & (old.split_seed == seed))]
        split_df = pd.concat([old, split_df], ignore_index=True)
    split_df.to_csv(splits_file, index=False)

    idx = split_indices
    X_train, y_train = X.iloc[idx["train_context"]].copy(), y[idx["train_context"]]
    X_val, y_val = X.iloc[idx["validation"]].copy(), y[idx["validation"]]
    X_cal, y_cal = X.iloc[idx["calibration"]].copy(), y[idx["calibration"]]
    X_test, y_test = X.iloc[idx["test"]].copy(), y[idx["test"]]

    miss_cfg = experiment_cfg["missingness"]
    cal_seed_base = seed * 100000 + int(miss_cfg.get("mask_seed_offset_calibration", 10000))
    test_seed_base = seed * 100000 + int(miss_cfg.get("mask_seed_offset_test", 20000))
    scenarios = scenario_specs(experiment_cfg)

    # Build and persist the exact masks once. The same test masks are reused by every model.
    test_scenarios = {}
    mask_records = []
    for j, (pattern, rate) in enumerate(scenarios):
        scenario = scenario_name(pattern, rate)
        mask = make_mask(X_test.shape, pattern, rate, test_seed_base + j)
        test_scenarios[scenario] = apply_mask(X_test, mask)
        mask_records.append({"scenario": scenario, "subset": "test", "mask": mask})
    methods = experiment_cfg["calibration"]["methods"]
    augmentation = []
    if any(m != "No additional calibration" for m in methods):
        augmentation = [("reference", 0.0)]
    if "Missingness-augmented calibration" in methods:
        augmentation += [("cell", float(r)) for r in miss_cfg["augmentation_cell_rates"]]
    cal_aug_scenarios = {}
    for j, (pattern, rate) in enumerate(augmentation):
        scenario = scenario_name(pattern, rate)
        mask = make_mask(X_cal.shape, pattern, rate, cal_seed_base + j)
        cal_aug_scenarios[scenario] = apply_mask(X_cal, mask)
        mask_records.append({"scenario": scenario, "subset": "calibration", "mask": mask})

    mask_dir = output_dir / "masks"
    mask_dir.mkdir(exist_ok=True)
    mask_path = mask_dir / f"{dataset_name}_seed_{seed}.npz"
    np.savez_compressed(mask_path, **{f"{r['subset']}__{r['scenario']}": r["mask"] for r in mask_records})

    preprocessor = ModelPreprocessor(model_name, metadata["numeric_columns"], metadata["categorical_columns"])
    status = {"dataset": dataset_name, "split_seed": seed, "model": model_name, "status": "running", "error": ""}
    result_rows, probability_rows = [], []
    scenario_plot_predictions, scenario_plot_y = {}, {}

    with PeakMemoryMonitor() as memory_monitor:
        try:
            transformed, preprocessing_seconds = _prepare_inputs(
                preprocessor, X_train, X_val, X_cal, test_scenarios
            )
            # TabDPT uses its own native dataframe interface; all other models use transformed arrays/dataframes.
            Xtr, Xva = transformed["train"], transformed["validation"]
            ytr, yva = y_train, y_val

            t0 = time.perf_counter()
            model = make_model(model_name, seed, threads, output_dir / "model_artifacts")
            initialization_seconds = time.perf_counter() - t0
            t0 = time.perf_counter()
            model = fit_model(model_name, model, Xtr, ytr, Xva, yva,
                              experiment_cfg["mlp"], seed)
            fit_seconds = time.perf_counter() - t0

            # Calibration predictions: reference + cell-wise 10% + cell-wise 30%.
            cal_probabilities = {}
            calibration_prediction_seconds = 0.0
            cal_costs = {}
            for scenario, Xcal_masked in cal_aug_scenarios.items():
                t0 = time.perf_counter()
                Xcal_t = preprocessor.transform(Xcal_masked)
                p = positive_probability(model, Xcal_t)
                elapsed = time.perf_counter() - t0
                calibration_prediction_seconds += elapsed
                cal_costs[scenario] = elapsed
                cal_probabilities[scenario] = p
                for obs_id, yy, pp in zip(idx["calibration"], y_cal, p):
                    probability_rows.append({
                        "dataset": dataset_name, "split_seed": seed, "model": model_name,
                        "scenario": scenario, "subset": "calibration",
                        "observation_id": int(obs_id), "y_true": int(yy),
                        "raw_probability": float(pp), "calibration": "raw"
                    })

            temperatures, cal_fit_costs, method_prediction_costs = {}, {}, {}
            temp_min = float(experiment_cfg["calibration"]["temperature_min"])
            temp_max = float(experiment_cfg["calibration"]["temperature_max"])
            for method in methods:
                if method == "No additional calibration":
                    temperatures[method] = 1.0
                    cal_fit_costs[method] = method_prediction_costs[method] = 0.0
                    continue
                keys = ["reference"] if method == "Reference calibration" else list(cal_probabilities)
                probs = np.concatenate([cal_probabilities[k] for k in keys])
                labels = np.tile(y_cal, len(keys))
                t0 = time.perf_counter()
                temperatures[method] = fit_temperature(labels, probs, lower=temp_min, upper=temp_max,
                                                      sample_weight=np.full(len(labels), 1.0/len(keys)))
                cal_fit_costs[method] = time.perf_counter() - t0
                method_prediction_costs[method] = sum(cal_costs[k] for k in keys)
            calibration_fit_seconds = sum(cal_fit_costs.values())
            def near_temperature_boundary(t):
                return bool((t <= temp_min * 1.01) or (t >= temp_max / 1.01))

            for scenario, Xtest_raw in test_scenarios.items():
                t0 = time.perf_counter()
                Xtest_t = preprocessor.transform(Xtest_raw)
                p_raw = positive_probability(model, Xtest_t)
                scenario_prediction_seconds = time.perf_counter() - t0
                scenario_plot_predictions[scenario] = {}
                scenario_plot_y[scenario] = y_test
                for method, temperature in temperatures.items():
                    t_apply = time.perf_counter()
                    p_calibrated = p_raw.copy() if method == "No additional calibration" else apply_temperature(p_raw, temperature)
                    calibration_apply_seconds = time.perf_counter() - t_apply
                    if not np.array_equal((p_raw >= 0.5), (p_calibrated >= 0.5)):
                        raise RuntimeError("Temperature scaling unexpectedly changed binary class predictions at threshold 0.5.")
                    metrics = calculate_metrics(y_test, p_calibrated,
                                                ece_bins=experiment_cfg["calibration"]["ece_bins"])
                    pattern, _, rate_text = scenario.partition("_")
                    rate = 0.0 if scenario == "reference" else float(rate_text) / 100.0
                    runtime = (initialization_seconds + preprocessing_seconds + fit_seconds +
                               method_prediction_costs[method] + cal_fit_costs[method] + scenario_prediction_seconds + calibration_apply_seconds)
                    row = {
                        "dataset": dataset_name, "split_seed": seed, "model": model_name,
                        "fit_phase": "baseline_training" if model_name in {"CatBoost", "MLP"} else "context_setup_frozen_foundation_model",
                        "missing_pattern": pattern, "missing_rate": rate,
                        "calibration": method, **metrics,
                        "initialization_seconds": initialization_seconds,
                        "preprocessing_seconds": preprocessing_seconds,
                        "fit_seconds": fit_seconds,
                        "calibration_prediction_seconds": method_prediction_costs[method],
                        "calibration_fit_seconds": cal_fit_costs[method],
                        "calibration_apply_seconds": calibration_apply_seconds,
                        "test_prediction_seconds": scenario_prediction_seconds,
                        "runtime_seconds": runtime,
                        "peak_RAM_MB": float(memory_monitor.peak_mb),
                        "n_train_context": len(y_train), "n_validation": len(y_val),
                        "n_calibration": len(y_cal), "n_test": len(y_test),
                        "temperature": float(temperature),
                        "temperature_boundary_warning": method != "No additional calibration" and near_temperature_boundary(float(temperature)),
                    }
                    result_rows.append(row)
                    scenario_plot_predictions[scenario][method] = p_calibrated
                    for obs_id, yy, rawp, pp in zip(idx["test"], y_test, p_raw, p_calibrated):
                        probability_rows.append({
                            "dataset": dataset_name, "split_seed": seed, "model": model_name,
                            "scenario": scenario, "subset": "test", "observation_id": int(obs_id),
                            "y_true": int(yy), "raw_probability": float(rawp),
                            "calibrated_probability": float(pp), "calibration": method
                        })

            if model_name == "MLP":
                status["best_epoch"] = int(getattr(model, "best_epoch_", -1))
                status["best_validation_logloss"] = float(getattr(model, "best_validation_logloss_", np.nan))
            status["status"] = "success"
            status["error"] = ""
            del model
            gc.collect()
        except Exception as exc:
            status["status"] = "failed"
            status["error"] = f"{type(exc).__name__}: {exc}"
            print(f"FAILED: {dataset_name} | {model_name} | seed={seed}: {status['error']}")

    # Plots and file export are excluded from the model-phase RSS monitor.
    if status["status"] == "success":
        try:
            save_reliability_figure(dataset_name, model_name, seed, scenario_plot_predictions,
                                    scenario_plot_y, output_dir / "reliability_diagrams",
                                    n_bins=experiment_cfg["calibration"]["reliability_bins"])
        except Exception as exc:
            status["plot_error"] = f"{type(exc).__name__}: {exc}"
    else:
        result_rows, probability_rows = [], []
    # Use the final monitor peak consistently in every row for this model/seed.
    for row in result_rows:
        row["peak_RAM_MB"] = float(memory_monitor.peak_mb)
    status["peak_RAM_MB"] = float(memory_monitor.peak_mb)
    status["memory_scope"] = "isolated worker process plus child RSS; model phases; includes imports"
    status["preprocessing_seconds"] = locals().get("preprocessing_seconds", np.nan)
    status["initialization_seconds"] = locals().get("initialization_seconds", np.nan)
    status["fit_seconds"] = locals().get("fit_seconds", np.nan)
    status["calibration_prediction_seconds"] = locals().get("calibration_prediction_seconds", np.nan)
    status["calibration_fit_seconds"] = locals().get("calibration_fit_seconds", np.nan)
    status["n_rows"] = metadata["n_rows"]
    status["n_features"] = metadata["n_features"]
    return result_rows, probability_rows, status
