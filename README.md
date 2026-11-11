# Tabular Foundation Models: Robustness and Calibration

Reusable Python pipeline for a master's thesis on binary tabular classification under missing data. The benchmark compares predictive performance, probability calibration, runtime, and memory usage using shared code and dataset-specific JSON configurations.

## Models and experimental setup

**Models:** TabPFN-v2, TabICLv2, TabDPT, CatBoost, and MLP. TabDPT replaces Mitra in this study; the two models are not equivalent.

| Setting | Value |
| --- | --- |
| Seeds | 42, 43, 44 |
| Train / validation / calibration / test | 60% / 10% / 15% / 15% |
| Test scenarios | Reference; cell-wise and feature-wise missingness at 10%, 30%, 50% |
| Calibration | No additional calibration; reference Temperature Scaling; missingness-augmented Temperature Scaling |
| Calibration augmentation | Reference + cell-wise missingness at 10% and 30% |
| Metrics | AUROC, balanced accuracy, log loss, Brier score, ECE |
| ECE bins / temperature bounds | 5 uniform bins / 0.05–20 |

Each complete dataset run contains **15 model–seed jobs, 315 evaluated conditions, and 105 aggregate rows**. Splits are stratified and disjoint within each seed. Models share the same splits and missingness masks. External preprocessing is fitted on training data only; calibration and test data are not passed to model fitting.


## Repository layout

| Path | Purpose |
| --- | --- |
| `run.py` | Run or resume experiments |
| `src/` | Shared pipeline implementation |
| `configs/experiment.json` | Common experimental protocol |
| `configs/models.json` | Model configuration and checkpoint declarations |
| `configs/datasets/` | Dataset configurations and template |
| `data/<dataset>/` | Original dataset files |
| `tests/` | Unit and regression tests |
| `check_environment.py` | Dependency and TabDPT wrapper checks |
| `freeze_environment.py` | Record the current environment |
| `verify_results.py` | Check outputs and recompute metrics |
| `requirements-base.txt`, `requirements-lock.txt` | Dependencies and recorded environment snapshot |


## Usage

Run commands from the directory containing `run.py`:

```powershell
python -m unittest discover -s tests -v
python check_environment.py
python run.py --datasets wdbc --validate-only
```

Start a complete run in a new output folder:

```powershell
python run.py --datasets wdbc --models all --seeds all --output risultati_wdbc_v2
```

Resume an existing run and verify its results:

```powershell
python run.py --datasets wdbc --models all --seeds all --output risultati_wdbc_v2 --resume
python verify_results.py --output risultati_wdbc_v2
```

To add a dataset, place its original file in `data/<dataset>/` and add a JSON configuration in `configs/datasets/`, specifying its path, target, positive/negative classes, column types, and ID columns to exclude. CSV and supported dense ARFF files are accepted. Multiclass targets are not automatically binarized; duplicate predictor rows are rejected by default and require methodological review.

## Results

Each output folder contains:

- `all_results_long.csv`: individual metrics and computational costs.
- `probabilities_long.csv`: saved probabilities.
- `model_status.csv`: completed-job status and timing information.
- `<dataset>/aggregate_results.csv`: mean and sample standard deviation across available seeds.
- `<dataset>/paired_differences.csv`: differences from the uncalibrated reference and the uncalibrated matching scenario.
- `jobs/`: individual job outputs, metadata, splits, masks, and plots.
- `run_manifest.json` and `last_invocation.json`: environment/configuration records and the latest requested grid.

Files ending in `all_datasets.csv` cover only datasets within the same output folder. They do not automatically combine separate output folders. Failed attempts are retained in `_attempts/`; exported CSVs include completed jobs only. The verifier checks the **last requested grid**, file integrity, counts, and all five metrics recomputed from probabilities.


