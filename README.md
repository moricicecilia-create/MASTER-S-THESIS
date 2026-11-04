# Robustness and Probability Calibration of Tabular Foundation Models under Missing-Data Shift

## 1. Project Overview

This repository contains the experimental framework developed for a Master's thesis investigating the robustness and probability calibration of pretrained Tabular Foundation Models under missing-data shift.

The study compares five classification models:

**Foundation Models**
- TabPFN-v2
- TabICLv2
- TabDPT

**Baseline Models**
- CatBoost
- Multilayer Perceptron (MLP)

TabDPT is used as a practical replacement for Mitra because of local compatibility and computational constraints encountered during the feasibility study. This methodological deviation is documented explicitly.

The foundation models are used with frozen pretrained weights, without downstream fine-tuning. CatBoost and MLP are trained from scratch on the downstream training split.

The main objectives are:
- Evaluate predictive robustness under different missing-data conditions.
- Assess probability calibration and its transferability under missing-data shift.
- Compare the computational costs of the selected models.

## 2. Repository Structure

The project follows a centralized and reusable architecture. Experimental code is shared across datasets, avoiding separate implementations for each dataset.

```text
tfm_reusable_pipeline/
│
├── src/
│   ├── data_loader.py
│   ├── data_split.py
│   ├── preprocessing.py
│   ├── models.py
│   ├── missingness.py
│   ├── calibration.py
│   ├── metrics.py
│   ├── experiment.py
│   └── aggregation.py
│
├── configs/
│   ├── experiment.json
│   ├── models.json
│   ├── environment-lock.json
│   └── datasets/
│       └── sonar.json
│
├── data/
│   └── sonar/
│
├── results/
│   └── sonar/
│
├── notebooks/
│
├── tests/
│
├── run.py
├── freeze_environment.py
├── check_environment.py
├── requirements-base.txt
├── requirements-lock.txt
├── README.md
└── .gitignore
```

### Main directories

| Directory | Description |
|---|---|
| `src/` | Shared experimental code, including preprocessing, model execution, missingness generation, calibration and evaluation. |
| `configs/` | Experimental settings, model configurations and dataset-specific metadata. |
| `data/` | Original datasets used in the experiments. |
| `results/` | Predictions, metrics, masks, model status and figures. |
| `notebooks/` | Exploratory analysis and visualization of experimental results. |
| `tests/` | Automated tests for the experimental pipeline. |

The same experimental functions are applied to different datasets through configuration files.

## 3. Models

| Model | Type | Training strategy |
|---|---|---|
| TabPFN-v2 | Tabular Foundation Model | Frozen pretrained weights |
| TabICLv2 | Tabular Foundation Model | Frozen pretrained weights |
| TabDPT | Tabular Foundation Model | Frozen pretrained weights |
| CatBoost | Gradient-boosted decision trees | Downstream training |
| MLP | Neural network | Downstream training with validation-based early stopping |

The foundation models use their pretrained knowledge to make predictions on new tabular datasets through their respective inference procedures.

CatBoost and MLP serve as conventional machine learning and deep learning baselines.

## 4. Computational Environment and Reproducibility

All experiments are associated with a recorded computational environment.

### 4.1. Software environment

| Component | Version |
|---|---|
| Python | 3.13.15 |
| Operating System | Windows 11, 64-bit |
| PyTorch | 2.13.0+cpu |
| NumPy | 2.5.2 |
| Pandas | 2.3.3 |
| SciPy | 1.18.0 |
| Scikit-learn | 1.8.0 |
| TabPFN | 9.1.0 |
| TabICL | 2.2.0 |
| TabDPT | 1.2.0 |
| AutoGluon Tabular | 1.6.3 |
| CatBoost | 1.2.10 |
| Matplotlib | 3.11.1 |
| psutil | 7.2.2 |

The complete list of installed package versions is available in:

- `requirements-lock.txt`
- `configs/environment-lock.json`

`requirements-lock.txt` records exact package versions using version pinning.

`environment-lock.json` records the Python version, operating system and principal package versions.

### 4.2. Pretrained checkpoint identification

The following pretrained checkpoints were identified in the local model cache.

| Model | Package | Checkpoint |
|---|---|---|
| TabPFN-v2 | tabpfn 9.1.0 | `tabpfn-v2-classifier-finetuned-zk73skhh.ckpt` |
| TabICLv2 | tabicl 2.2.0 | `tabicl-classifier-v2-20260212.ckpt` |
| TabDPT | tabdpt 1.2.0 | `tabdpt1_2.safetensors` |

**TabPFN-v2**

- Repository: `Prior-Labs/TabPFN-v2-clf`
- Checkpoint: `tabpfn-v2-classifier-finetuned-zk73skhh.ckpt`
- SHA-256:

```text
CF8C519C01EAF1613EE91239006D57B1C806FF5F23AC1AEB1315BA1015210E49
```

The checkpoint corresponds to the default v2 classifier checkpoint configured in the installed TabPFN package.

**TabICLv2**

- Repository: `jingang/TabICL`
- Checkpoint: `tabicl-classifier-v2-20260212.ckpt`
- Repository revision:

```text
4dcd344ece2c00be9e831fdd35bed57b5ad83e19
```

- SHA-256:

```text
BDC7DBD5E4FF21F8F0456FCF90C6B7CDF72DBEA960F2D05B19BEC19F9B3D4ED0
```

**TabDPT**

- Repository: `Layer6/TabDPT`
- Checkpoint: `tabdpt1_2.safetensors`
- Repository revision:

```text
a5ca6e01c0fa09ec68c73e958e5199d1932abb3a
```

- SHA-256:

```text
06680220FD66C4524051706B98C1C659A674D19D3A766CD0BB276505E99FACCD
```

AutoGluon uses the default weights supplied by the installed TabDPT package. The `model_weight_path` parameter is not explicitly specified in the current configuration.

The SHA-256 values identify the checkpoint files found in the local cache. They should be checked against the actual files used in each experimental run.

CatBoost and MLP do not use pretrained foundation-model checkpoints.

### 4.3. Environment verification

To record the installed environment:

```powershell
python freeze_environment.py
```

To check the availability of the required packages:

```powershell
python check_environment.py
```

The package availability check does not replace actual model inference testing.

## 5. Experimental Methodology

### 5.1. Dataset

The initial experimental pilot uses the Sonar dataset.

- 208 observations.
- 60 numerical features.
- Binary classification.
- Target classes: `M` and `R`.
- Positive class: `M`.

The dataset is divided into four disjoint subsets:

| Subset | Percentage | Purpose |
|---|---:|---|
| Training/context | 60% | Model training and labelled context |
| Validation | 10% | Model selection and early stopping |
| Calibration | 15% | Fitting post-hoc calibration |
| Test | 15% | Final evaluation |

Three random seeds are used:

```text
42, 43, 44
```

The same partitions are shared across models for each seed.

### 5.2. Preprocessing

Preprocessing is centralized but model-specific where necessary.

- **CatBoost and TabDPT:** DataFrame-based input and supported native handling of missing values and categorical features.
- **TabPFN-v2 and TabICLv2:** Numerical input, with median imputation and one-hot encoding when categorical features are present.
- **MLP:** Median imputation, numerical feature scaling and one-hot encoding.

All learned preprocessing transformations are fitted exclusively on the training/context set.

Missingness is introduced on the original features before model-specific preprocessing.

### 5.3. Missingness Scenarios

The experiments consider seven evaluation conditions:

| Scenario | Missingness level |
|---|---:|
| Reference | 0% |
| Cell-wise missingness | 10% |
| Cell-wise missingness | 30% |
| Cell-wise missingness | 50% |
| Feature-wise missingness | 10% |
| Feature-wise missingness | 30% |
| Feature-wise missingness | 50% |

Cell-wise missingness randomly masks individual feature values.

Feature-wise missingness makes selected original features completely unavailable across all test observations.

The training/context set remains unchanged.

The same missingness masks are shared across models to ensure paired comparisons.

### 5.4. Probability Calibration

Three calibration conditions are considered:

| Calibration strategy | Description |
|---|---|
| No additional calibration | Original model probabilities |
| Reference calibration | Temperature Scaling fitted on the reference calibration set |
| Missingness-augmented calibration | Temperature Scaling fitted using reference, cell-wise 10% and cell-wise 30% calibration predictions |

Temperature Scaling is used as the primary post-hoc calibration method.

The missingness-augmented calibrator is evaluated under more severe and structurally different missingness conditions, including cell-wise 50% and feature-wise missingness.

Each original calibration observation receives equal total weight across its masked copies.

Calibration and test masks are generated independently.

## 6. Evaluation Metrics

The evaluation considers predictive performance, probability quality and computational costs.

| Metric | Purpose |
|---|---|
| AUROC | Discriminative performance |
| Balanced Accuracy | Classification performance accounting for class imbalance |
| Log-loss | Probabilistic prediction quality |
| Brier Score | Mean squared probability error |
| Expected Calibration Error (ECE) | Difference between predicted probabilities and observed frequencies |

ECE is calculated using five uniform probability bins for the positive class, consistently with the reliability diagrams.

Reliability diagrams include the number of observations in each bin.

### Computational evaluation

The following quantities are recorded:

- Model preparation or training time.
- Calibration prediction time.
- Test prediction time.
- Calibration fitting time.
- Peak memory consumption.

Initial model loading and repeated inference are distinguished where available.

Memory measurements are based on sampled process and child-process RSS using `psutil`.

## 7. Running the Experiments

### 7.1. Dataset preparation

Place the original Sonar dataset in:

```text
data/sonar/sonar.all-data
```

### 7.2. Install dependencies

Activate the intended Python environment.

For a new compatible environment, use the pinned dependency file:

```powershell
python -m pip install -r requirements-lock.txt
```

The CPU-specific PyTorch distribution may require installation from the appropriate official PyTorch package index.

### 7.3. Run automated tests

```powershell
python -m unittest discover -s tests -v
```

### 7.4. Run a preliminary MLP experiment

```powershell
python run.py --datasets sonar --models MLP --seeds 42
```

### 7.5. Run all models with one seed

```powershell
python run.py --datasets sonar --models all --seeds 42
```

### 7.6. Run the complete Sonar experiment

```powershell
python run.py --datasets sonar --models all --seeds all
```

To limit computational threads:

```powershell
python run.py --datasets sonar --models all --seeds all --threads 4
```

The same pipeline can be extended to additional datasets by adding their corresponding configuration files under `configs/datasets/`.

## 8. Results and Output Files

Results are organized by dataset.

The main output files include:

| File | Description |
|---|---|
| `all_results_long.csv` | Detailed metrics for every experimental condition |
| `probabilities_long.csv` | Original and calibrated predicted probabilities |
| `split_indices.csv` | Dataset partition assignments |
| `model_status.csv` | Model execution status and computational information |
| `aggregate_results.csv` | Mean and standard deviation across seeds |
| `paired_differences.csv` | Paired performance differences |
| `masks/` | Generated missingness masks |
| `reliability_diagrams/` | Calibration plots |
| `model_artifacts/` | Local model artifacts |

Global aggregate tables are also generated under `results/`.

A run should only be considered complete when all expected model executions have been checked and the corresponding entries in `model_status.csv` indicate successful execution.

## 9. Reproducibility and Experimental Limitations

Several aspects are important when interpreting and reproducing the results:

1. The same experimental partitions and missingness masks are used across models.
2. Foundation-model weights remain frozen throughout the experiments.
3. Calibration and test labels are never included in the training/context set.
4. All learned preprocessing transformations are fitted exclusively on the training/context set.
5. Results from previous standalone scripts must not be mixed with results generated by the centralized pipeline.
6. Sonar is a relatively small dataset. Its calibration and test subsets contain few observations, which may increase the variability of calibration estimates and reliability diagrams.
7. The replacement of Mitra with TabDPT represents a documented deviation from the initial model selection.
8. Package availability, checkpoint identification and successful model inference are distinct verification steps. The actual execution environment and checkpoint files must be verified before claiming full reproducibility.

## 10. Future Work

The next stage of the project consists of extending the validated Sonar pipeline to the remaining selected binary classification datasets.

The centralized architecture allows additional datasets to be introduced through configuration files without duplicating the experimental code.

The final benchmark will include six datasets, with possible expansion to eight depending on computational feasibility.
