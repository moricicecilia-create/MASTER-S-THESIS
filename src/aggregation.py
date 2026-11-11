from __future__ import annotations
import pandas as pd

METRICS = ["AUROC", "balanced_acc", "logloss", "brier", "ECE",
           "runtime_seconds", "fit_seconds", "test_prediction_seconds", "peak_RAM_MB"]


def aggregate_results(results: pd.DataFrame):
    if results.empty:
        return pd.DataFrame()
    keys = ["dataset", "model", "missing_pattern", "missing_rate", "calibration"]
    agg = results.groupby(keys)[METRICS].agg(["mean", "std"]).reset_index()
    agg.columns = ["_".join(str(x) for x in col if x) if isinstance(col, tuple) else col for col in agg.columns]
    return agg


def paired_differences(results: pd.DataFrame):
    if results.empty:
        return pd.DataFrame()
    keys = ["dataset", "split_seed", "model"]
    ref = results[(results.missing_pattern == "reference") & (results.calibration == "No additional calibration")]
    ref = ref[keys + ["AUROC", "balanced_acc", "logloss", "brier", "ECE"]].rename(
        columns={m: f"{m}_reference_uncalibrated" for m in ["AUROC", "balanced_acc", "logloss", "brier", "ECE"]}
    )
    out = results.merge(ref, on=keys, how="left", validate="many_to_one")
    for m in ["AUROC", "balanced_acc", "logloss", "brier", "ECE"]:
        out[f"delta_{m}_vs_reference_uncalibrated"] = out[m] - out[f"{m}_reference_uncalibrated"]
    uncal = results[results.calibration == "No additional calibration"][
        keys + ["missing_pattern", "missing_rate", "AUROC", "balanced_acc", "logloss", "brier", "ECE"]
    ].rename(columns={m: f"{m}_uncalibrated_same_scenario" for m in ["AUROC", "balanced_acc", "logloss", "brier", "ECE"]})
    out = out.merge(uncal, on=keys + ["missing_pattern", "missing_rate"], how="left", validate="many_to_one")
    for m in ["AUROC", "balanced_acc", "logloss", "brier", "ECE"]:
        out[f"delta_{m}_vs_uncalibrated_same_scenario"] = out[m] - out[f"{m}_uncalibrated_same_scenario"]
    return out
