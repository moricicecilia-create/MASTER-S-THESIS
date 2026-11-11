# Raisin | Experimental results

This README presents **one complete summary table** covering all **105 combinations** of five models, seven test conditions and three post-hoc calibration strategies. All numerical values are **mean ± sample standard deviation over split seeds 42, 43 and 44**; they are descriptive summaries, not statistical significance tests.

## Experimental settings

- **Models:** TabPFN-v2, TabICLv2, TabDPT, CatBoost and MLP.
- **Missing-data shift:** reference (no artificial missingness), cell-wise masking (10%, 30%, 50%) and complete-feature masking (10%, 30%, 50%). Missingness is applied to prediction inputs.
- **Calibration:** None (no additional calibration), Reference TS (temperature scaling fitted on reference calibration data), and Augmented TS (temperature scaling fitted on reference plus 10% and 30% cell-wise-masked calibration data).
- **Metrics:** AUROC and balanced accuracy (higher is better); log loss, Brier score and expected calibration error, ECE (lower is better). Runtime and peak RAM indicate computational costs.

## Unified results table

| Model | Missing pattern | Rate | Calibration | AUROC | Balanced acc. | Log loss | Brier | ECE | Runtime (s) | Peak RAM (MiB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TabPFN-v2 | Reference | 0% | None | 0.953 ± 0.007 | 0.894 ± 0.026 | 0.265 ± 0.019 | 0.080 ± 0.009 | 0.042 ± 0.011 | 28.13 ± 4.03 | 516.7 ± 2.8 |
| TabPFN-v2 | Reference | 0% | Reference TS | 0.953 ± 0.007 | 0.894 ± 0.026 | 0.265 ± 0.026 | 0.080 ± 0.010 | 0.039 ± 0.011 | 56.78 ± 10.03 | 516.7 ± 2.8 |
| TabPFN-v2 | Reference | 0% | Augmented TS | 0.953 ± 0.007 | 0.894 ± 0.026 | 0.267 ± 0.027 | 0.080 ± 0.010 | 0.041 ± 0.011 | 113.36 ± 20.40 | 516.7 ± 2.8 |
| TabPFN-v2 | Cell | 10% | None | 0.921 ± 0.020 | 0.842 ± 0.022 | 0.349 ± 0.034 | 0.111 ± 0.013 | 0.056 ± 0.017 | 29.01 ± 5.27 | 516.7 ± 2.8 |
| TabPFN-v2 | Cell | 10% | Reference TS | 0.921 ± 0.020 | 0.842 ± 0.022 | 0.350 ± 0.035 | 0.111 ± 0.013 | 0.056 ± 0.010 | 57.66 ± 11.27 | 516.7 ± 2.8 |
| TabPFN-v2 | Cell | 10% | Augmented TS | 0.921 ± 0.020 | 0.842 ± 0.022 | 0.351 ± 0.036 | 0.111 ± 0.014 | 0.056 ± 0.011 | 114.24 ± 21.62 | 516.7 ± 2.8 |
| TabPFN-v2 | Cell | 30% | None | 0.846 ± 0.016 | 0.726 ± 0.015 | 0.474 ± 0.028 | 0.160 ± 0.010 | 0.052 ± 0.025 | 28.57 ± 5.02 | 516.7 ± 2.8 |
| TabPFN-v2 | Cell | 30% | Reference TS | 0.846 ± 0.016 | 0.726 ± 0.015 | 0.476 ± 0.028 | 0.161 ± 0.009 | 0.068 ± 0.025 | 57.22 ± 11.00 | 516.7 ± 2.8 |
| TabPFN-v2 | Cell | 30% | Augmented TS | 0.846 ± 0.016 | 0.726 ± 0.015 | 0.476 ± 0.029 | 0.161 ± 0.009 | 0.058 ± 0.026 | 113.80 ± 21.34 | 516.7 ± 2.8 |
| TabPFN-v2 | Cell | 50% | None | 0.730 ± 0.088 | 0.635 ± 0.094 | 0.583 ± 0.081 | 0.207 ± 0.033 | 0.106 ± 0.025 | 28.70 ± 5.11 | 516.7 ± 2.8 |
| TabPFN-v2 | Cell | 50% | Reference TS | 0.730 ± 0.088 | 0.635 ± 0.094 | 0.579 ± 0.073 | 0.206 ± 0.029 | 0.098 ± 0.021 | 57.35 ± 11.09 | 516.7 ± 2.8 |
| TabPFN-v2 | Cell | 50% | Augmented TS | 0.730 ± 0.088 | 0.635 ± 0.094 | 0.578 ± 0.072 | 0.205 ± 0.029 | 0.105 ± 0.020 | 113.93 ± 21.45 | 516.7 ± 2.8 |
| TabPFN-v2 | Feature | 10% | None | 0.947 ± 0.016 | 0.894 ± 0.022 | 0.315 ± 0.059 | 0.091 ± 0.018 | 0.092 ± 0.034 | 32.16 ± 5.44 | 516.7 ± 2.8 |
| TabPFN-v2 | Feature | 10% | Reference TS | 0.947 ± 0.016 | 0.894 ± 0.022 | 0.321 ± 0.074 | 0.093 ± 0.023 | 0.105 ± 0.037 | 60.81 ± 8.27 | 516.7 ± 2.8 |
| TabPFN-v2 | Feature | 10% | Augmented TS | 0.947 ± 0.016 | 0.894 ± 0.022 | 0.324 ± 0.076 | 0.094 ± 0.023 | 0.105 ± 0.045 | 117.39 ± 17.26 | 516.7 ± 2.8 |
| TabPFN-v2 | Feature | 30% | None | 0.710 ± 0.408 | 0.686 ± 0.351 | 0.540 ± 0.339 | 0.185 ± 0.149 | 0.190 ± 0.151 | 30.08 ± 3.62 | 516.7 ± 2.8 |
| TabPFN-v2 | Feature | 30% | Reference TS | 0.710 ± 0.408 | 0.686 ± 0.351 | 0.569 ± 0.365 | 0.195 ± 0.159 | 0.211 ± 0.158 | 58.73 ± 7.52 | 516.7 ± 2.8 |
| TabPFN-v2 | Feature | 30% | Augmented TS | 0.710 ± 0.408 | 0.686 ± 0.351 | 0.568 ± 0.355 | 0.194 ± 0.155 | 0.210 ± 0.148 | 115.31 ± 17.23 | 516.7 ± 2.8 |
| TabPFN-v2 | Feature | 50% | None | 0.503 ± 0.383 | 0.550 ± 0.312 | 0.639 ± 0.292 | 0.230 ± 0.129 | 0.201 ± 0.116 | 29.22 ± 2.80 | 516.7 ± 2.8 |
| TabPFN-v2 | Feature | 50% | Reference TS | 0.503 ± 0.383 | 0.550 ± 0.312 | 0.622 ± 0.295 | 0.224 ± 0.128 | 0.176 ± 0.119 | 57.87 ± 7.91 | 516.7 ± 2.8 |
| TabPFN-v2 | Feature | 50% | Augmented TS | 0.503 ± 0.383 | 0.550 ± 0.312 | 0.621 ± 0.291 | 0.223 ± 0.126 | 0.166 ± 0.105 | 114.45 ± 18.00 | 516.7 ± 2.8 |
| TabICLv2 | Reference | 0% | None | 0.954 ± 0.002 | 0.886 ± 0.022 | 0.261 ± 0.013 | 0.079 ± 0.007 | 0.036 ± 0.003 | 15.20 ± 1.75 | 672.2 ± 5.6 |
| TabICLv2 | Reference | 0% | Reference TS | 0.954 ± 0.002 | 0.886 ± 0.022 | 0.268 ± 0.022 | 0.080 ± 0.007 | 0.047 ± 0.014 | 29.75 ± 3.88 | 672.2 ± 5.6 |
| TabICLv2 | Reference | 0% | Augmented TS | 0.954 ± 0.002 | 0.886 ± 0.022 | 0.262 ± 0.020 | 0.079 ± 0.008 | 0.039 ± 0.005 | 56.69 ± 7.17 | 672.2 ± 5.6 |
| TabICLv2 | Cell | 10% | None | 0.923 ± 0.023 | 0.866 ± 0.025 | 0.370 ± 0.041 | 0.116 ± 0.018 | 0.084 ± 0.025 | 15.27 ± 2.27 | 672.2 ± 5.6 |
| TabICLv2 | Cell | 10% | Reference TS | 0.923 ± 0.023 | 0.866 ± 0.025 | 0.376 ± 0.044 | 0.117 ± 0.019 | 0.102 ± 0.022 | 29.82 ± 4.40 | 672.2 ± 5.6 |
| TabICLv2 | Cell | 10% | Augmented TS | 0.923 ± 0.023 | 0.866 ± 0.025 | 0.366 ± 0.049 | 0.114 ± 0.021 | 0.087 ± 0.011 | 56.76 ± 7.69 | 672.2 ± 5.6 |
| TabICLv2 | Cell | 30% | None | 0.870 ± 0.018 | 0.790 ± 0.042 | 0.486 ± 0.036 | 0.160 ± 0.016 | 0.121 ± 0.051 | 15.85 ± 3.29 | 672.2 ± 5.6 |
| TabICLv2 | Cell | 30% | Reference TS | 0.870 ± 0.018 | 0.790 ± 0.042 | 0.491 ± 0.049 | 0.162 ± 0.021 | 0.114 ± 0.028 | 30.40 ± 5.42 | 672.2 ± 5.6 |
| TabICLv2 | Cell | 30% | Augmented TS | 0.870 ± 0.018 | 0.790 ± 0.042 | 0.480 ± 0.055 | 0.158 ± 0.023 | 0.102 ± 0.035 | 57.34 ± 8.68 | 672.2 ± 5.6 |
| TabICLv2 | Cell | 50% | None | 0.794 ± 0.078 | 0.704 ± 0.072 | 0.562 ± 0.060 | 0.191 ± 0.026 | 0.094 ± 0.044 | 15.41 ± 2.57 | 672.2 ± 5.6 |
| TabICLv2 | Cell | 50% | Reference TS | 0.794 ± 0.078 | 0.704 ± 0.072 | 0.564 ± 0.064 | 0.191 ± 0.028 | 0.083 ± 0.051 | 29.96 ± 4.70 | 672.2 ± 5.6 |
| TabICLv2 | Cell | 50% | Augmented TS | 0.794 ± 0.078 | 0.704 ± 0.072 | 0.554 ± 0.070 | 0.188 ± 0.031 | 0.089 ± 0.037 | 56.90 ± 7.99 | 672.2 ± 5.6 |
| TabICLv2 | Feature | 10% | None | 0.926 ± 0.050 | 0.884 ± 0.028 | 0.433 ± 0.138 | 0.133 ± 0.055 | 0.154 ± 0.031 | 15.30 ± 2.15 | 672.2 ± 5.6 |
| TabICLv2 | Feature | 10% | Reference TS | 0.926 ± 0.050 | 0.884 ± 0.028 | 0.444 ± 0.156 | 0.139 ± 0.061 | 0.119 ± 0.089 | 29.85 ± 4.28 | 672.2 ± 5.6 |
| TabICLv2 | Feature | 10% | Augmented TS | 0.926 ± 0.050 | 0.884 ± 0.028 | 0.424 ± 0.164 | 0.132 ± 0.063 | 0.096 ± 0.080 | 56.79 ± 7.55 | 672.2 ± 5.6 |
| TabICLv2 | Feature | 30% | None | 0.839 ± 0.034 | 0.805 ± 0.042 | 0.593 ± 0.035 | 0.201 ± 0.017 | 0.123 ± 0.080 | 15.40 ± 2.53 | 672.2 ± 5.6 |
| TabICLv2 | Feature | 30% | Reference TS | 0.839 ± 0.034 | 0.805 ± 0.042 | 0.603 ± 0.021 | 0.205 ± 0.010 | 0.058 ± 0.043 | 29.95 ± 4.66 | 672.2 ± 5.6 |
| TabICLv2 | Feature | 30% | Augmented TS | 0.839 ± 0.034 | 0.805 ± 0.042 | 0.592 ± 0.025 | 0.200 ± 0.011 | 0.090 ± 0.053 | 56.89 ± 7.94 | 672.2 ± 5.6 |
| TabICLv2 | Feature | 50% | None | 0.892 ± 0.057 | 0.769 ± 0.220 | 0.572 ± 0.086 | 0.191 ± 0.042 | 0.246 ± 0.031 | 15.17 ± 2.12 | 672.2 ± 5.6 |
| TabICLv2 | Feature | 50% | Reference TS | 0.892 ± 0.057 | 0.769 ± 0.220 | 0.571 ± 0.101 | 0.191 ± 0.048 | 0.205 ± 0.041 | 29.72 ± 4.24 | 672.2 ± 5.6 |
| TabICLv2 | Feature | 50% | Augmented TS | 0.892 ± 0.057 | 0.769 ± 0.220 | 0.555 ± 0.115 | 0.184 ± 0.054 | 0.236 ± 0.043 | 56.67 ± 7.54 | 672.2 ± 5.6 |
| TabDPT | Reference | 0% | None | 0.954 ± 0.005 | 0.884 ± 0.026 | 0.269 ± 0.016 | 0.082 ± 0.009 | 0.054 ± 0.002 | 57.18 ± 6.76 | 931.8 ± 1.2 |
| TabDPT | Reference | 0% | Reference TS | 0.954 ± 0.005 | 0.884 ± 0.026 | 0.268 ± 0.028 | 0.081 ± 0.010 | 0.052 ± 0.019 | 82.49 ± 9.88 | 931.8 ± 1.2 |
| TabDPT | Reference | 0% | Augmented TS | 0.954 ± 0.005 | 0.884 ± 0.026 | 0.262 ± 0.026 | 0.080 ± 0.010 | 0.033 ± 0.012 | 131.87 ± 15.33 | 931.8 ± 1.2 |
| TabDPT | Cell | 10% | None | 0.930 ± 0.019 | 0.867 ± 0.034 | 0.361 ± 0.037 | 0.112 ± 0.017 | 0.110 ± 0.031 | 56.59 ± 6.62 | 931.8 ± 1.2 |
| TabDPT | Cell | 10% | Reference TS | 0.930 ± 0.019 | 0.867 ± 0.034 | 0.359 ± 0.042 | 0.111 ± 0.018 | 0.102 ± 0.014 | 81.90 ± 9.72 | 931.8 ± 1.2 |
| TabDPT | Cell | 10% | Augmented TS | 0.930 ± 0.019 | 0.867 ± 0.034 | 0.349 ± 0.047 | 0.107 ± 0.021 | 0.084 ± 0.021 | 131.28 ± 15.17 | 931.8 ± 1.2 |
| TabDPT | Cell | 30% | None | 0.885 ± 0.009 | 0.774 ± 0.031 | 0.480 ± 0.014 | 0.158 ± 0.008 | 0.119 ± 0.031 | 56.87 ± 6.62 | 931.8 ± 1.2 |
| TabDPT | Cell | 30% | Reference TS | 0.885 ± 0.009 | 0.774 ± 0.031 | 0.480 ± 0.022 | 0.158 ± 0.009 | 0.121 ± 0.021 | 82.18 ± 9.70 | 931.8 ± 1.2 |
| TabDPT | Cell | 30% | Augmented TS | 0.885 ± 0.009 | 0.774 ± 0.031 | 0.471 ± 0.024 | 0.155 ± 0.011 | 0.105 ± 0.028 | 131.56 ± 15.14 | 931.8 ± 1.2 |
| TabDPT | Cell | 50% | None | 0.824 ± 0.058 | 0.691 ± 0.059 | 0.569 ± 0.058 | 0.195 ± 0.026 | 0.127 ± 0.017 | 56.66 ± 6.64 | 931.8 ± 1.2 |
| TabDPT | Cell | 50% | Reference TS | 0.824 ± 0.058 | 0.691 ± 0.059 | 0.567 ± 0.057 | 0.195 ± 0.025 | 0.132 ± 0.039 | 81.97 ± 9.79 | 931.8 ± 1.2 |
| TabDPT | Cell | 50% | Augmented TS | 0.824 ± 0.058 | 0.691 ± 0.059 | 0.560 ± 0.066 | 0.193 ± 0.029 | 0.133 ± 0.038 | 131.35 ± 15.25 | 931.8 ± 1.2 |
| TabDPT | Feature | 10% | None | 0.944 ± 0.019 | 0.901 ± 0.008 | 0.389 ± 0.056 | 0.116 ± 0.021 | 0.145 ± 0.009 | 56.56 ± 6.25 | 931.8 ± 1.2 |
| TabDPT | Feature | 10% | Reference TS | 0.944 ± 0.019 | 0.901 ± 0.008 | 0.387 ± 0.090 | 0.116 ± 0.032 | 0.141 ± 0.039 | 81.87 ± 9.39 | 931.8 ± 1.2 |
| TabDPT | Feature | 10% | Augmented TS | 0.944 ± 0.019 | 0.901 ± 0.008 | 0.366 ± 0.085 | 0.109 ± 0.029 | 0.127 ± 0.035 | 131.25 ± 14.84 | 931.8 ± 1.2 |
| TabDPT | Feature | 30% | None | 0.898 ± 0.058 | 0.764 ± 0.204 | 0.526 ± 0.116 | 0.173 ± 0.054 | 0.182 ± 0.042 | 56.47 ± 6.55 | 931.8 ± 1.2 |
| TabDPT | Feature | 30% | Reference TS | 0.898 ± 0.058 | 0.764 ± 0.204 | 0.540 ± 0.111 | 0.180 ± 0.054 | 0.218 ± 0.036 | 81.78 ± 9.69 | 931.8 ± 1.2 |
| TabDPT | Feature | 30% | Augmented TS | 0.898 ± 0.058 | 0.764 ± 0.204 | 0.525 ± 0.129 | 0.174 ± 0.061 | 0.206 ± 0.047 | 131.16 ± 15.14 | 931.8 ± 1.2 |
| TabDPT | Feature | 50% | None | 0.902 ± 0.051 | 0.703 ± 0.182 | 0.574 ± 0.085 | 0.195 ± 0.040 | 0.244 ± 0.062 | 56.85 ± 6.44 | 931.8 ± 1.2 |
| TabDPT | Feature | 50% | Reference TS | 0.902 ± 0.051 | 0.703 ± 0.182 | 0.562 ± 0.101 | 0.191 ± 0.044 | 0.218 ± 0.067 | 82.15 ± 9.58 | 931.8 ± 1.2 |
| TabDPT | Feature | 50% | Augmented TS | 0.902 ± 0.051 | 0.703 ± 0.182 | 0.553 ± 0.104 | 0.187 ± 0.046 | 0.228 ± 0.073 | 131.53 ± 15.03 | 931.8 ± 1.2 |
| CatBoost | Reference | 0% | None | 0.945 ± 0.018 | 0.886 ± 0.022 | 0.477 ± 0.215 | 0.158 ± 0.082 | 0.088 ± 0.104 | 2.16 ± 0.63 | 214.4 ± 1.7 |
| CatBoost | Reference | 0% | Reference TS | 0.945 ± 0.018 | 0.886 ± 0.022 | 0.292 ± 0.051 | 0.086 ± 0.018 | 0.049 ± 0.005 | 2.17 ± 0.62 | 214.4 ± 1.7 |
| CatBoost | Reference | 0% | Augmented TS | 0.945 ± 0.018 | 0.886 ± 0.022 | 0.292 ± 0.050 | 0.086 ± 0.018 | 0.048 ± 0.006 | 2.17 ± 0.62 | 214.4 ± 1.7 |
| CatBoost | Cell | 10% | None | 0.933 ± 0.028 | 0.861 ± 0.026 | 0.506 ± 0.192 | 0.169 ± 0.075 | 0.062 ± 0.062 | 2.16 ± 0.63 | 214.4 ± 1.7 |
| CatBoost | Cell | 10% | Reference TS | 0.933 ± 0.028 | 0.861 ± 0.026 | 0.349 ± 0.056 | 0.107 ± 0.021 | 0.068 ± 0.019 | 2.17 ± 0.62 | 214.4 ± 1.7 |
| CatBoost | Cell | 10% | Augmented TS | 0.933 ± 0.028 | 0.861 ± 0.026 | 0.348 ± 0.056 | 0.107 ± 0.021 | 0.067 ± 0.019 | 2.17 ± 0.62 | 214.4 ± 1.7 |
| CatBoost | Cell | 30% | None | 0.890 ± 0.058 | 0.799 ± 0.038 | 0.561 ± 0.129 | 0.191 ± 0.053 | 0.077 ± 0.062 | 2.16 ± 0.63 | 214.4 ± 1.7 |
| CatBoost | Cell | 30% | Reference TS | 0.890 ± 0.058 | 0.799 ± 0.038 | 0.462 ± 0.083 | 0.151 ± 0.031 | 0.123 ± 0.008 | 2.17 ± 0.62 | 214.4 ± 1.7 |
| CatBoost | Cell | 30% | Augmented TS | 0.890 ± 0.058 | 0.799 ± 0.038 | 0.462 ± 0.085 | 0.151 ± 0.031 | 0.124 ± 0.008 | 2.17 ± 0.62 | 214.4 ± 1.7 |
| CatBoost | Cell | 50% | None | 0.877 ± 0.034 | 0.712 ± 0.016 | 0.632 ± 0.039 | 0.217 ± 0.023 | 0.132 ± 0.108 | 2.16 ± 0.63 | 214.4 ± 1.7 |
| CatBoost | Cell | 50% | Reference TS | 0.877 ± 0.034 | 0.712 ± 0.016 | 0.597 ± 0.022 | 0.202 ± 0.010 | 0.209 ± 0.015 | 2.17 ± 0.62 | 214.4 ± 1.7 |
| CatBoost | Cell | 50% | Augmented TS | 0.877 ± 0.034 | 0.712 ± 0.016 | 0.598 ± 0.024 | 0.203 ± 0.011 | 0.210 ± 0.014 | 2.17 ± 0.62 | 214.4 ± 1.7 |
| CatBoost | Feature | 10% | None | 0.936 ± 0.020 | 0.846 ± 0.053 | 0.525 ± 0.207 | 0.178 ± 0.083 | 0.052 ± 0.055 | 2.16 ± 0.63 | 214.4 ± 1.7 |
| CatBoost | Feature | 10% | Reference TS | 0.936 ± 0.020 | 0.846 ± 0.053 | 0.383 ± 0.095 | 0.119 ± 0.038 | 0.115 ± 0.091 | 2.17 ± 0.62 | 214.4 ± 1.7 |
| CatBoost | Feature | 10% | Augmented TS | 0.936 ± 0.020 | 0.846 ± 0.053 | 0.383 ± 0.095 | 0.119 ± 0.038 | 0.114 ± 0.091 | 2.17 ± 0.62 | 214.4 ± 1.7 |
| CatBoost | Feature | 30% | None | 0.932 ± 0.018 | 0.635 ± 0.190 | 0.698 ± 0.083 | 0.251 ± 0.038 | 0.169 ± 0.170 | 2.16 ± 0.63 | 214.4 ± 1.7 |
| CatBoost | Feature | 30% | Reference TS | 0.932 ± 0.018 | 0.635 ± 0.190 | 0.589 ± 0.197 | 0.208 ± 0.088 | 0.223 ± 0.133 | 2.17 ± 0.62 | 214.4 ± 1.7 |
| CatBoost | Feature | 30% | Augmented TS | 0.932 ± 0.018 | 0.635 ± 0.190 | 0.587 ± 0.195 | 0.208 ± 0.087 | 0.221 ± 0.134 | 2.17 ± 0.62 | 214.4 ± 1.7 |
| CatBoost | Feature | 50% | None | 0.902 ± 0.029 | 0.747 ± 0.214 | 0.609 ± 0.107 | 0.211 ± 0.048 | 0.110 ± 0.091 | 2.16 ± 0.63 | 214.4 ± 1.7 |
| CatBoost | Feature | 50% | Reference TS | 0.902 ± 0.029 | 0.747 ± 0.214 | 0.616 ± 0.203 | 0.215 ± 0.090 | 0.223 ± 0.096 | 2.17 ± 0.62 | 214.4 ± 1.7 |
| CatBoost | Feature | 50% | Augmented TS | 0.902 ± 0.029 | 0.747 ± 0.214 | 0.618 ± 0.207 | 0.216 ± 0.092 | 0.225 ± 0.097 | 2.17 ± 0.62 | 214.4 ± 1.7 |
| MLP | Reference | 0% | None | 0.954 ± 0.012 | 0.901 ± 0.030 | 0.280 ± 0.061 | 0.082 ± 0.019 | 0.079 ± 0.039 | 1.11 ± 0.77 | 181.5 ± 0.0 |
| MLP | Reference | 0% | Reference TS | 0.954 ± 0.012 | 0.901 ± 0.030 | 0.274 ± 0.051 | 0.081 ± 0.017 | 0.075 ± 0.021 | 1.12 ± 0.77 | 181.5 ± 0.0 |
| MLP | Reference | 0% | Augmented TS | 0.954 ± 0.012 | 0.901 ± 0.030 | 0.276 ± 0.038 | 0.081 ± 0.014 | 0.085 ± 0.005 | 1.13 ± 0.77 | 181.5 ± 0.0 |
| MLP | Cell | 10% | None | 0.931 ± 0.024 | 0.867 ± 0.022 | 0.347 ± 0.035 | 0.105 ± 0.013 | 0.081 ± 0.028 | 1.11 ± 0.77 | 181.5 ± 0.0 |
| MLP | Cell | 10% | Reference TS | 0.931 ± 0.024 | 0.867 ± 0.022 | 0.338 ± 0.038 | 0.103 ± 0.015 | 0.073 ± 0.028 | 1.12 ± 0.77 | 181.5 ± 0.0 |
| MLP | Cell | 10% | Augmented TS | 0.931 ± 0.024 | 0.867 ± 0.022 | 0.332 ± 0.038 | 0.102 ± 0.015 | 0.070 ± 0.024 | 1.13 ± 0.77 | 181.5 ± 0.0 |
| MLP | Cell | 30% | None | 0.902 ± 0.046 | 0.829 ± 0.066 | 0.424 ± 0.082 | 0.133 ± 0.032 | 0.112 ± 0.028 | 1.11 ± 0.77 | 181.5 ± 0.0 |
| MLP | Cell | 30% | Reference TS | 0.902 ± 0.046 | 0.829 ± 0.066 | 0.411 ± 0.082 | 0.130 ± 0.033 | 0.096 ± 0.021 | 1.12 ± 0.77 | 181.5 ± 0.0 |
| MLP | Cell | 30% | Augmented TS | 0.902 ± 0.046 | 0.829 ± 0.066 | 0.398 ± 0.074 | 0.127 ± 0.031 | 0.080 ± 0.017 | 1.13 ± 0.77 | 181.5 ± 0.0 |
| MLP | Cell | 50% | None | 0.859 ± 0.102 | 0.785 ± 0.091 | 0.516 ± 0.155 | 0.164 ± 0.053 | 0.144 ± 0.025 | 1.12 ± 0.77 | 181.5 ± 0.0 |
| MLP | Cell | 50% | Reference TS | 0.859 ± 0.102 | 0.785 ± 0.091 | 0.500 ± 0.150 | 0.160 ± 0.054 | 0.143 ± 0.018 | 1.12 ± 0.77 | 181.5 ± 0.0 |
| MLP | Cell | 50% | Augmented TS | 0.859 ± 0.102 | 0.785 ± 0.091 | 0.479 ± 0.131 | 0.156 ± 0.051 | 0.129 ± 0.015 | 1.13 ± 0.77 | 181.5 ± 0.0 |
| MLP | Feature | 10% | None | 0.947 ± 0.006 | 0.886 ± 0.018 | 0.319 ± 0.039 | 0.095 ± 0.011 | 0.090 ± 0.055 | 1.11 ± 0.77 | 181.5 ± 0.0 |
| MLP | Feature | 10% | Reference TS | 0.947 ± 0.006 | 0.886 ± 0.018 | 0.312 ± 0.029 | 0.093 ± 0.008 | 0.088 ± 0.031 | 1.12 ± 0.77 | 181.5 ± 0.0 |
| MLP | Feature | 10% | Augmented TS | 0.947 ± 0.006 | 0.886 ± 0.018 | 0.310 ± 0.018 | 0.092 ± 0.005 | 0.082 ± 0.018 | 1.13 ± 0.77 | 181.5 ± 0.0 |
| MLP | Feature | 30% | None | 0.831 ± 0.191 | 0.768 ± 0.190 | 0.501 ± 0.266 | 0.164 ± 0.103 | 0.142 ± 0.058 | 1.11 ± 0.77 | 181.5 ± 0.0 |
| MLP | Feature | 30% | Reference TS | 0.831 ± 0.191 | 0.768 ± 0.190 | 0.486 ± 0.261 | 0.160 ± 0.103 | 0.131 ± 0.066 | 1.12 ± 0.77 | 181.5 ± 0.0 |
| MLP | Feature | 30% | Augmented TS | 0.831 ± 0.191 | 0.768 ± 0.190 | 0.466 ± 0.241 | 0.154 ± 0.097 | 0.110 ± 0.058 | 1.13 ± 0.77 | 181.5 ± 0.0 |
| MLP | Feature | 50% | None | 0.928 ± 0.028 | 0.854 ± 0.049 | 0.398 ± 0.127 | 0.124 ± 0.045 | 0.132 ± 0.082 | 1.11 ± 0.77 | 181.5 ± 0.0 |
| MLP | Feature | 50% | Reference TS | 0.928 ± 0.028 | 0.854 ± 0.049 | 0.388 ± 0.121 | 0.121 ± 0.042 | 0.119 ± 0.074 | 1.12 ± 0.77 | 181.5 ± 0.0 |
| MLP | Feature | 50% | Augmented TS | 0.928 ± 0.028 | 0.854 ± 0.049 | 0.380 ± 0.116 | 0.118 ± 0.040 | 0.111 ± 0.079 | 1.13 ± 0.77 | 181.5 ± 0.0 |

## Data and interpretation notes

- The table combines predictive metrics, probability-quality metrics and computational measurements in **one row per model × missingness scenario × calibration method**.
- `Reference` with rate `0%` means no artificially introduced missing values; it does **not** necessarily mean the original data had no missing values.
- AUROC and balanced accuracy need not change after positive temperature scaling, because it preserves ranking and the usual binary 0.5 decision boundary.
- Runtime is the pipeline-reported time per condition, **not** the elapsed time for the entire experiment. Fitting work reused across conditions must not be added as if it were repeated.
- Peak RAM includes the measured process and its child processes; values refer to reported MiB even though the underlying column is named `peak_RAM_MB`.
- The original aggregated file provides mean and standard deviation, **not seed-level observations**. Accordingly `split_seed` cannot be reconstructed from these data and no seed-level rows have been invented.
- The complete unrounded values and detailed computational fields (fit time and test prediction time, including standard deviations) are retained in [`aggregate_results.csv`](aggregate_results.csv).

**Reproducibility:** Exact package versions, model checkpoints, machine specifications and per-seed raw outputs must be documented separately. They cannot be recovered from these aggregate files alone.
