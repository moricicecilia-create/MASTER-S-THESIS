# Sonar | Experimental results

This README presents **one complete summary table** covering all **105 combinations** of five models, seven test conditions and three post-hoc calibration strategies. All numerical values are **mean ± sample standard deviation over split seeds 42, 43 and 44**; they are descriptive summaries, not statistical significance tests.

## Experimental settings

- **Models:** TabPFN-v2, TabICLv2, TabDPT, CatBoost and MLP.
- **Missing-data shift:** reference (no artificial missingness), cell-wise masking (10%, 30%, 50%) and complete-feature masking (10%, 30%, 50%). Missingness is applied to prediction inputs.
- **Calibration:** None (no additional calibration), Reference TS (temperature scaling fitted on reference calibration data), and Augmented TS (temperature scaling fitted on reference plus 10% and 30% cell-wise-masked calibration data).
- **Metrics:** AUROC and balanced accuracy (higher is better); log loss, Brier score and expected calibration error, ECE (lower is better). Runtime and peak RAM indicate computational costs.

## Unified results table

| Model | Missing pattern | Rate | Calibration | AUROC | Balanced acc. | Log loss | Brier | ECE | Runtime (s) | Peak RAM (MiB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TabPFN-v2 | Reference | 0% | None | 0.925 ± 0.016 | 0.820 ± 0.069 | 0.334 ± 0.047 | 0.111 ± 0.018 | 0.056 ± 0.036 | 35.74 ± 12.99 | 548.5 ± 8.7 |
| TabPFN-v2 | Reference | 0% | Reference TS | 0.925 ± 0.016 | 0.820 ± 0.069 | 0.341 ± 0.053 | 0.113 ± 0.019 | 0.070 ± 0.032 | 69.29 ± 24.25 | 548.5 ± 8.7 |
| TabPFN-v2 | Reference | 0% | Augmented TS | 0.925 ± 0.016 | 0.820 ± 0.069 | 0.340 ± 0.050 | 0.112 ± 0.018 | 0.068 ± 0.026 | 137.37 ± 48.92 | 548.5 ± 8.7 |
| TabPFN-v2 | Cell | 10% | None | 0.920 ± 0.019 | 0.810 ± 0.029 | 0.339 ± 0.036 | 0.111 ± 0.013 | 0.065 ± 0.026 | 35.86 ± 13.15 | 548.5 ± 8.7 |
| TabPFN-v2 | Cell | 10% | Reference TS | 0.920 ± 0.019 | 0.810 ± 0.029 | 0.339 ± 0.038 | 0.113 ± 0.012 | 0.068 ± 0.020 | 69.41 ± 24.42 | 548.5 ± 8.7 |
| TabPFN-v2 | Cell | 10% | Augmented TS | 0.920 ± 0.019 | 0.810 ± 0.029 | 0.340 ± 0.037 | 0.113 ± 0.012 | 0.060 ± 0.015 | 137.50 ± 49.09 | 548.5 ± 8.7 |
| TabPFN-v2 | Cell | 30% | None | 0.892 ± 0.038 | 0.792 ± 0.034 | 0.402 ± 0.050 | 0.133 ± 0.019 | 0.074 ± 0.020 | 36.59 ± 12.53 | 548.5 ± 8.7 |
| TabPFN-v2 | Cell | 30% | Reference TS | 0.892 ± 0.038 | 0.792 ± 0.034 | 0.415 ± 0.050 | 0.137 ± 0.020 | 0.112 ± 0.015 | 70.14 ± 23.77 | 548.5 ± 8.7 |
| TabPFN-v2 | Cell | 30% | Augmented TS | 0.892 ± 0.038 | 0.792 ± 0.034 | 0.415 ± 0.045 | 0.137 ± 0.018 | 0.116 ± 0.020 | 138.23 ± 48.43 | 548.5 ± 8.7 |
| TabPFN-v2 | Cell | 50% | None | 0.841 ± 0.091 | 0.746 ± 0.115 | 0.499 ± 0.134 | 0.170 ± 0.057 | 0.132 ± 0.065 | 40.23 ± 13.49 | 548.5 ± 8.7 |
| TabPFN-v2 | Cell | 50% | Reference TS | 0.841 ± 0.091 | 0.746 ± 0.115 | 0.519 ± 0.167 | 0.176 ± 0.068 | 0.119 ± 0.071 | 73.79 ± 24.20 | 548.5 ± 8.7 |
| TabPFN-v2 | Cell | 50% | Augmented TS | 0.841 ± 0.091 | 0.746 ± 0.115 | 0.513 ± 0.156 | 0.174 ± 0.065 | 0.116 ± 0.065 | 141.87 ± 48.55 | 548.5 ± 8.7 |
| TabPFN-v2 | Feature | 10% | None | 0.919 ± 0.031 | 0.819 ± 0.048 | 0.346 ± 0.057 | 0.113 ± 0.021 | 0.063 ± 0.036 | 36.36 ± 13.82 | 548.5 ± 8.7 |
| TabPFN-v2 | Feature | 10% | Reference TS | 0.919 ± 0.031 | 0.819 ± 0.048 | 0.352 ± 0.066 | 0.115 ± 0.021 | 0.064 ± 0.025 | 69.91 ± 25.07 | 548.5 ± 8.7 |
| TabPFN-v2 | Feature | 10% | Augmented TS | 0.919 ± 0.031 | 0.819 ± 0.048 | 0.350 ± 0.065 | 0.115 ± 0.021 | 0.073 ± 0.036 | 138.00 ± 49.74 | 548.5 ± 8.7 |
| TabPFN-v2 | Feature | 30% | None | 0.888 ± 0.042 | 0.787 ± 0.047 | 0.403 ± 0.033 | 0.134 ± 0.017 | 0.093 ± 0.047 | 36.50 ± 13.94 | 548.5 ± 8.7 |
| TabPFN-v2 | Feature | 30% | Reference TS | 0.888 ± 0.042 | 0.787 ± 0.047 | 0.406 ± 0.057 | 0.135 ± 0.022 | 0.086 ± 0.021 | 70.05 ± 25.20 | 548.5 ± 8.7 |
| TabPFN-v2 | Feature | 30% | Augmented TS | 0.888 ± 0.042 | 0.787 ± 0.047 | 0.412 ± 0.058 | 0.136 ± 0.022 | 0.094 ± 0.040 | 138.14 ± 49.87 | 548.5 ± 8.7 |
| TabPFN-v2 | Feature | 50% | None | 0.820 ± 0.137 | 0.720 ± 0.124 | 0.500 ± 0.168 | 0.171 ± 0.068 | 0.144 ± 0.066 | 35.87 ± 13.77 | 548.5 ± 8.7 |
| TabPFN-v2 | Feature | 50% | Reference TS | 0.820 ± 0.137 | 0.720 ± 0.124 | 0.501 ± 0.177 | 0.170 ± 0.066 | 0.114 ± 0.046 | 69.43 ± 25.03 | 548.5 ± 8.7 |
| TabPFN-v2 | Feature | 50% | Augmented TS | 0.820 ± 0.137 | 0.720 ± 0.124 | 0.496 ± 0.176 | 0.169 ± 0.065 | 0.107 ± 0.039 | 137.51 ± 49.71 | 548.5 ± 8.7 |
| TabICLv2 | Reference | 0% | None | 0.967 ± 0.028 | 0.893 ± 0.035 | 0.231 ± 0.050 | 0.072 ± 0.018 | 0.070 ± 0.012 | 14.82 ± 5.28 | 794.2 ± 16.0 |
| TabICLv2 | Reference | 0% | Reference TS | 0.967 ± 0.028 | 0.893 ± 0.035 | 0.224 ± 0.060 | 0.074 ± 0.018 | 0.078 ± 0.004 | 26.27 ± 9.27 | 794.2 ± 16.0 |
| TabICLv2 | Reference | 0% | Augmented TS | 0.967 ± 0.028 | 0.893 ± 0.035 | 0.226 ± 0.057 | 0.075 ± 0.019 | 0.062 ± 0.032 | 50.40 ± 20.28 | 794.2 ± 16.0 |
| TabICLv2 | Cell | 10% | None | 0.963 ± 0.019 | 0.893 ± 0.023 | 0.255 ± 0.033 | 0.077 ± 0.012 | 0.083 ± 0.014 | 14.92 ± 5.69 | 794.2 ± 16.0 |
| TabICLv2 | Cell | 10% | Reference TS | 0.963 ± 0.019 | 0.893 ± 0.023 | 0.229 ± 0.053 | 0.074 ± 0.014 | 0.087 ± 0.019 | 26.37 ± 9.70 | 794.2 ± 16.0 |
| TabICLv2 | Cell | 10% | Augmented TS | 0.963 ± 0.019 | 0.893 ± 0.023 | 0.228 ± 0.049 | 0.074 ± 0.013 | 0.108 ± 0.029 | 50.49 ± 20.71 | 794.2 ± 16.0 |
| TabICLv2 | Cell | 30% | None | 0.929 ± 0.037 | 0.835 ± 0.045 | 0.357 ± 0.065 | 0.111 ± 0.027 | 0.105 ± 0.026 | 14.64 ± 5.33 | 794.2 ± 16.0 |
| TabICLv2 | Cell | 30% | Reference TS | 0.929 ± 0.037 | 0.835 ± 0.045 | 0.344 ± 0.095 | 0.112 ± 0.034 | 0.095 ± 0.022 | 26.10 ± 9.34 | 794.2 ± 16.0 |
| TabICLv2 | Cell | 30% | Augmented TS | 0.929 ± 0.037 | 0.835 ± 0.045 | 0.347 ± 0.097 | 0.113 ± 0.036 | 0.095 ± 0.035 | 50.22 ± 20.36 | 794.2 ± 16.0 |
| TabICLv2 | Cell | 50% | None | 0.855 ± 0.041 | 0.767 ± 0.070 | 0.465 ± 0.061 | 0.154 ± 0.027 | 0.108 ± 0.009 | 14.67 ± 5.31 | 794.2 ± 16.0 |
| TabICLv2 | Cell | 50% | Reference TS | 0.855 ± 0.041 | 0.767 ± 0.070 | 0.484 ± 0.084 | 0.163 ± 0.037 | 0.109 ± 0.038 | 26.12 ± 9.31 | 794.2 ± 16.0 |
| TabICLv2 | Cell | 50% | Augmented TS | 0.855 ± 0.041 | 0.767 ± 0.070 | 0.485 ± 0.103 | 0.163 ± 0.042 | 0.115 ± 0.065 | 50.25 ± 20.33 | 794.2 ± 16.0 |
| TabICLv2 | Feature | 10% | None | 0.965 ± 0.010 | 0.861 ± 0.017 | 0.264 ± 0.034 | 0.082 ± 0.011 | 0.098 ± 0.024 | 14.55 ± 5.05 | 794.2 ± 16.0 |
| TabICLv2 | Feature | 10% | Reference TS | 0.965 ± 0.010 | 0.861 ± 0.017 | 0.264 ± 0.046 | 0.086 ± 0.014 | 0.096 ± 0.023 | 26.00 ± 9.06 | 794.2 ± 16.0 |
| TabICLv2 | Feature | 10% | Augmented TS | 0.965 ± 0.010 | 0.861 ± 0.017 | 0.262 ± 0.045 | 0.085 ± 0.017 | 0.087 ± 0.023 | 50.13 ± 20.07 | 794.2 ± 16.0 |
| TabICLv2 | Feature | 30% | None | 0.924 ± 0.036 | 0.852 ± 0.047 | 0.355 ± 0.043 | 0.111 ± 0.020 | 0.088 ± 0.047 | 14.50 ± 5.12 | 794.2 ± 16.0 |
| TabICLv2 | Feature | 30% | Reference TS | 0.924 ± 0.036 | 0.852 ± 0.047 | 0.340 ± 0.086 | 0.110 ± 0.031 | 0.083 ± 0.042 | 25.95 ± 9.14 | 794.2 ± 16.0 |
| TabICLv2 | Feature | 30% | Augmented TS | 0.924 ± 0.036 | 0.852 ± 0.047 | 0.333 ± 0.084 | 0.109 ± 0.030 | 0.087 ± 0.048 | 50.08 ± 20.16 | 794.2 ± 16.0 |
| TabICLv2 | Feature | 50% | None | 0.863 ± 0.083 | 0.795 ± 0.066 | 0.480 ± 0.090 | 0.157 ± 0.037 | 0.099 ± 0.065 | 14.41 ± 5.16 | 794.2 ± 16.0 |
| TabICLv2 | Feature | 50% | Reference TS | 0.863 ± 0.083 | 0.795 ± 0.066 | 0.477 ± 0.120 | 0.155 ± 0.042 | 0.098 ± 0.070 | 25.87 ± 9.17 | 794.2 ± 16.0 |
| TabICLv2 | Feature | 50% | Augmented TS | 0.863 ± 0.083 | 0.795 ± 0.066 | 0.487 ± 0.120 | 0.156 ± 0.042 | 0.107 ± 0.057 | 49.99 ± 20.20 | 794.2 ± 16.0 |
| TabDPT | Reference | 0% | None | 0.953 ± 0.037 | 0.872 ± 0.053 | 0.280 ± 0.074 | 0.087 ± 0.027 | 0.088 ± 0.009 | 22.37 ± 4.68 | 933.4 ± 6.2 |
| TabDPT | Reference | 0% | Reference TS | 0.953 ± 0.037 | 0.872 ± 0.053 | 0.255 ± 0.085 | 0.085 ± 0.029 | 0.090 ± 0.036 | 31.01 ± 8.28 | 933.4 ± 6.2 |
| TabDPT | Reference | 0% | Augmented TS | 0.953 ± 0.037 | 0.872 ± 0.053 | 0.254 ± 0.085 | 0.085 ± 0.029 | 0.079 ± 0.028 | 65.25 ± 45.87 | 933.4 ± 6.2 |
| TabDPT | Cell | 10% | None | 0.945 ± 0.042 | 0.850 ± 0.047 | 0.313 ± 0.063 | 0.095 ± 0.025 | 0.114 ± 0.046 | 21.96 ± 3.91 | 933.4 ± 6.2 |
| TabDPT | Cell | 10% | Reference TS | 0.945 ± 0.042 | 0.850 ± 0.047 | 0.277 ± 0.082 | 0.089 ± 0.029 | 0.071 ± 0.030 | 30.60 ± 7.50 | 933.4 ± 6.2 |
| TabDPT | Cell | 10% | Augmented TS | 0.945 ± 0.042 | 0.850 ± 0.047 | 0.274 ± 0.082 | 0.089 ± 0.029 | 0.087 ± 0.023 | 64.85 ± 45.09 | 933.4 ± 6.2 |
| TabDPT | Cell | 30% | None | 0.911 ± 0.050 | 0.819 ± 0.047 | 0.405 ± 0.068 | 0.126 ± 0.029 | 0.118 ± 0.032 | 21.95 ± 3.87 | 933.4 ± 6.2 |
| TabDPT | Cell | 30% | Reference TS | 0.911 ± 0.050 | 0.819 ± 0.047 | 0.362 ± 0.099 | 0.116 ± 0.037 | 0.079 ± 0.022 | 30.60 ± 7.47 | 933.4 ± 6.2 |
| TabDPT | Cell | 30% | Augmented TS | 0.911 ± 0.050 | 0.819 ± 0.047 | 0.360 ± 0.094 | 0.116 ± 0.036 | 0.071 ± 0.010 | 64.84 ± 45.06 | 933.4 ± 6.2 |
| TabDPT | Cell | 50% | None | 0.833 ± 0.084 | 0.698 ± 0.067 | 0.514 ± 0.093 | 0.172 ± 0.039 | 0.120 ± 0.048 | 21.93 ± 3.87 | 933.4 ± 6.2 |
| TabDPT | Cell | 50% | Reference TS | 0.833 ± 0.084 | 0.698 ± 0.067 | 0.500 ± 0.118 | 0.171 ± 0.043 | 0.078 ± 0.031 | 30.57 ± 7.47 | 933.4 ± 6.2 |
| TabDPT | Cell | 50% | Augmented TS | 0.833 ± 0.084 | 0.698 ± 0.067 | 0.503 ± 0.120 | 0.172 ± 0.044 | 0.080 ± 0.026 | 64.81 ± 45.06 | 933.4 ± 6.2 |
| TabDPT | Feature | 10% | None | 0.940 ± 0.050 | 0.873 ± 0.061 | 0.320 ± 0.090 | 0.099 ± 0.033 | 0.122 ± 0.033 | 21.93 ± 3.82 | 933.4 ± 6.2 |
| TabDPT | Feature | 10% | Reference TS | 0.940 ± 0.050 | 0.873 ± 0.061 | 0.286 ± 0.100 | 0.093 ± 0.034 | 0.081 ± 0.016 | 30.57 ± 7.42 | 933.4 ± 6.2 |
| TabDPT | Feature | 10% | Augmented TS | 0.940 ± 0.050 | 0.873 ± 0.061 | 0.285 ± 0.098 | 0.094 ± 0.034 | 0.078 ± 0.037 | 64.81 ± 45.01 | 933.4 ± 6.2 |
| TabDPT | Feature | 30% | None | 0.916 ± 0.038 | 0.818 ± 0.020 | 0.403 ± 0.053 | 0.126 ± 0.019 | 0.093 ± 0.027 | 21.95 ± 3.82 | 933.4 ± 6.2 |
| TabDPT | Feature | 30% | Reference TS | 0.916 ± 0.038 | 0.818 ± 0.020 | 0.376 ± 0.059 | 0.120 ± 0.017 | 0.095 ± 0.030 | 30.59 ± 7.42 | 933.4 ± 6.2 |
| TabDPT | Feature | 30% | Augmented TS | 0.916 ± 0.038 | 0.818 ± 0.020 | 0.369 ± 0.060 | 0.119 ± 0.018 | 0.092 ± 0.034 | 64.84 ± 45.01 | 933.4 ± 6.2 |
| TabDPT | Feature | 50% | None | 0.877 ± 0.093 | 0.741 ± 0.127 | 0.485 ± 0.098 | 0.158 ± 0.044 | 0.115 ± 0.033 | 22.24 ± 3.78 | 933.4 ± 6.2 |
| TabDPT | Feature | 50% | Reference TS | 0.877 ± 0.093 | 0.741 ± 0.127 | 0.447 ± 0.138 | 0.148 ± 0.054 | 0.114 ± 0.030 | 30.88 ± 7.35 | 933.4 ± 6.2 |
| TabDPT | Feature | 50% | Augmented TS | 0.877 ± 0.093 | 0.741 ± 0.127 | 0.448 ± 0.135 | 0.149 ± 0.054 | 0.108 ± 0.011 | 65.12 ± 44.93 | 933.4 ± 6.2 |
| CatBoost | Reference | 0% | None | 0.901 ± 0.029 | 0.787 ± 0.022 | 0.519 ± 0.086 | 0.169 ± 0.036 | 0.146 ± 0.055 | 2.30 ± 0.81 | 222.1 ± 0.2 |
| CatBoost | Reference | 0% | Reference TS | 0.901 ± 0.029 | 0.787 ± 0.022 | 0.403 ± 0.061 | 0.133 ± 0.023 | 0.105 ± 0.040 | 2.31 ± 0.81 | 222.1 ± 0.2 |
| CatBoost | Reference | 0% | Augmented TS | 0.901 ± 0.029 | 0.787 ± 0.022 | 0.401 ± 0.053 | 0.131 ± 0.020 | 0.088 ± 0.004 | 2.33 ± 0.81 | 222.1 ± 0.2 |
| CatBoost | Cell | 10% | None | 0.872 ± 0.050 | 0.767 ± 0.062 | 0.541 ± 0.087 | 0.179 ± 0.038 | 0.144 ± 0.064 | 2.30 ± 0.81 | 222.1 ± 0.2 |
| CatBoost | Cell | 10% | Reference TS | 0.872 ± 0.050 | 0.767 ± 0.062 | 0.430 ± 0.075 | 0.145 ± 0.029 | 0.079 ± 0.033 | 2.31 ± 0.81 | 222.1 ± 0.2 |
| CatBoost | Cell | 10% | Augmented TS | 0.872 ± 0.050 | 0.767 ± 0.062 | 0.433 ± 0.076 | 0.144 ± 0.029 | 0.089 ± 0.043 | 2.33 ± 0.80 | 222.1 ± 0.2 |
| CatBoost | Cell | 30% | None | 0.820 ± 0.046 | 0.659 ± 0.072 | 0.604 ± 0.050 | 0.209 ± 0.022 | 0.141 ± 0.056 | 2.29 ± 0.81 | 222.1 ± 0.2 |
| CatBoost | Cell | 30% | Reference TS | 0.820 ± 0.046 | 0.659 ± 0.072 | 0.585 ± 0.068 | 0.207 ± 0.030 | 0.188 ± 0.061 | 2.31 ± 0.81 | 222.1 ± 0.2 |
| CatBoost | Cell | 30% | Augmented TS | 0.820 ± 0.046 | 0.659 ± 0.072 | 0.566 ± 0.058 | 0.199 ± 0.025 | 0.162 ± 0.062 | 2.33 ± 0.80 | 222.1 ± 0.2 |
| CatBoost | Cell | 50% | None | 0.724 ± 0.082 | 0.572 ± 0.051 | 0.675 ± 0.005 | 0.241 ± 0.003 | 0.147 ± 0.053 | 2.30 ± 0.81 | 222.1 ± 0.2 |
| CatBoost | Cell | 50% | Reference TS | 0.724 ± 0.082 | 0.572 ± 0.051 | 0.930 ± 0.169 | 0.309 ± 0.015 | 0.308 ± 0.047 | 2.32 ± 0.80 | 222.1 ± 0.2 |
| CatBoost | Cell | 50% | Augmented TS | 0.724 ± 0.082 | 0.572 ± 0.051 | 0.808 ± 0.082 | 0.285 ± 0.015 | 0.270 ± 0.051 | 2.33 ± 0.80 | 222.1 ± 0.2 |
| CatBoost | Feature | 10% | None | 0.876 ± 0.022 | 0.792 ± 0.011 | 0.557 ± 0.078 | 0.186 ± 0.034 | 0.150 ± 0.065 | 2.30 ± 0.81 | 222.1 ± 0.2 |
| CatBoost | Feature | 10% | Reference TS | 0.876 ± 0.022 | 0.792 ± 0.011 | 0.452 ± 0.057 | 0.152 ± 0.020 | 0.132 ± 0.067 | 2.31 ± 0.81 | 222.1 ± 0.2 |
| CatBoost | Feature | 10% | Augmented TS | 0.876 ± 0.022 | 0.792 ± 0.011 | 0.455 ± 0.065 | 0.151 ± 0.023 | 0.099 ± 0.037 | 2.33 ± 0.80 | 222.1 ± 0.2 |
| CatBoost | Feature | 30% | None | 0.831 ± 0.081 | 0.688 ± 0.175 | 0.593 ± 0.082 | 0.204 ± 0.038 | 0.186 ± 0.007 | 2.29 ± 0.81 | 222.1 ± 0.2 |
| CatBoost | Feature | 30% | Reference TS | 0.831 ± 0.081 | 0.688 ± 0.175 | 0.611 ± 0.272 | 0.216 ± 0.111 | 0.195 ± 0.131 | 2.31 ± 0.81 | 222.1 ± 0.2 |
| CatBoost | Feature | 30% | Augmented TS | 0.831 ± 0.081 | 0.688 ± 0.175 | 0.577 ± 0.206 | 0.204 ± 0.090 | 0.190 ± 0.089 | 2.33 ± 0.80 | 222.1 ± 0.2 |
| CatBoost | Feature | 50% | None | 0.752 ± 0.073 | 0.579 ± 0.078 | 0.662 ± 0.070 | 0.237 ± 0.032 | 0.137 ± 0.085 | 2.29 ± 0.81 | 222.1 ± 0.2 |
| CatBoost | Feature | 50% | Reference TS | 0.752 ± 0.073 | 0.579 ± 0.078 | 0.871 ± 0.329 | 0.300 ± 0.106 | 0.287 ± 0.152 | 2.31 ± 0.81 | 222.1 ± 0.2 |
| CatBoost | Feature | 50% | Augmented TS | 0.752 ± 0.073 | 0.579 ± 0.078 | 0.774 ± 0.256 | 0.277 ± 0.093 | 0.244 ± 0.137 | 2.33 ± 0.80 | 222.1 ± 0.2 |
| MLP | Reference | 0% | None | 0.933 ± 0.048 | 0.863 ± 0.043 | 0.329 ± 0.120 | 0.103 ± 0.044 | 0.079 ± 0.028 | 0.80 ± 0.37 | 182.7 ± 0.5 |
| MLP | Reference | 0% | Reference TS | 0.933 ± 0.048 | 0.863 ± 0.043 | 0.331 ± 0.120 | 0.104 ± 0.042 | 0.077 ± 0.039 | 0.81 ± 0.37 | 182.7 ± 0.5 |
| MLP | Reference | 0% | Augmented TS | 0.933 ± 0.048 | 0.863 ± 0.043 | 0.328 ± 0.117 | 0.104 ± 0.041 | 0.069 ± 0.028 | 0.82 ± 0.37 | 182.7 ± 0.5 |
| MLP | Cell | 10% | None | 0.897 ± 0.063 | 0.822 ± 0.060 | 0.393 ± 0.114 | 0.123 ± 0.047 | 0.088 ± 0.035 | 0.81 ± 0.36 | 182.7 ± 0.5 |
| MLP | Cell | 10% | Reference TS | 0.897 ± 0.063 | 0.822 ± 0.060 | 0.384 ± 0.111 | 0.123 ± 0.041 | 0.082 ± 0.015 | 0.81 ± 0.36 | 182.7 ± 0.5 |
| MLP | Cell | 10% | Augmented TS | 0.897 ± 0.063 | 0.822 ± 0.060 | 0.382 ± 0.110 | 0.123 ± 0.042 | 0.079 ± 0.037 | 0.82 ± 0.37 | 182.7 ± 0.5 |
| MLP | Cell | 30% | None | 0.942 ± 0.053 | 0.876 ± 0.052 | 0.330 ± 0.131 | 0.102 ± 0.040 | 0.082 ± 0.004 | 0.80 ± 0.37 | 182.7 ± 0.5 |
| MLP | Cell | 30% | Reference TS | 0.942 ± 0.053 | 0.876 ± 0.052 | 0.364 ± 0.140 | 0.113 ± 0.047 | 0.133 ± 0.026 | 0.81 ± 0.37 | 182.7 ± 0.5 |
| MLP | Cell | 30% | Augmented TS | 0.942 ± 0.053 | 0.876 ± 0.052 | 0.359 ± 0.131 | 0.111 ± 0.044 | 0.129 ± 0.017 | 0.82 ± 0.37 | 182.7 ± 0.5 |
| MLP | Cell | 50% | None | 0.818 ± 0.066 | 0.739 ± 0.085 | 0.546 ± 0.135 | 0.179 ± 0.051 | 0.125 ± 0.045 | 0.80 ± 0.37 | 182.7 ± 0.5 |
| MLP | Cell | 50% | Reference TS | 0.818 ± 0.066 | 0.739 ± 0.085 | 0.510 ± 0.104 | 0.171 ± 0.043 | 0.083 ± 0.022 | 0.81 ± 0.37 | 182.7 ± 0.5 |
| MLP | Cell | 50% | Augmented TS | 0.818 ± 0.066 | 0.739 ± 0.085 | 0.510 ± 0.104 | 0.171 ± 0.043 | 0.074 ± 0.026 | 0.82 ± 0.37 | 182.7 ± 0.5 |
| MLP | Feature | 10% | None | 0.915 ± 0.045 | 0.844 ± 0.057 | 0.366 ± 0.098 | 0.110 ± 0.040 | 0.077 ± 0.003 | 0.80 ± 0.37 | 182.7 ± 0.5 |
| MLP | Feature | 10% | Reference TS | 0.915 ± 0.045 | 0.844 ± 0.057 | 0.365 ± 0.102 | 0.113 ± 0.039 | 0.100 ± 0.023 | 0.81 ± 0.37 | 182.7 ± 0.5 |
| MLP | Feature | 10% | Augmented TS | 0.915 ± 0.045 | 0.844 ± 0.057 | 0.361 ± 0.100 | 0.112 ± 0.038 | 0.085 ± 0.029 | 0.82 ± 0.37 | 182.7 ± 0.5 |
| MLP | Feature | 30% | None | 0.899 ± 0.055 | 0.841 ± 0.055 | 0.406 ± 0.104 | 0.124 ± 0.032 | 0.094 ± 0.042 | 0.80 ± 0.37 | 182.7 ± 0.5 |
| MLP | Feature | 30% | Reference TS | 0.899 ± 0.055 | 0.841 ± 0.055 | 0.414 ± 0.086 | 0.129 ± 0.031 | 0.133 ± 0.025 | 0.81 ± 0.37 | 182.7 ± 0.5 |
| MLP | Feature | 30% | Augmented TS | 0.899 ± 0.055 | 0.841 ± 0.055 | 0.407 ± 0.088 | 0.127 ± 0.031 | 0.121 ± 0.014 | 0.82 ± 0.37 | 182.7 ± 0.5 |
| MLP | Feature | 50% | None | 0.854 ± 0.059 | 0.806 ± 0.057 | 0.496 ± 0.118 | 0.162 ± 0.044 | 0.129 ± 0.027 | 0.80 ± 0.37 | 182.7 ± 0.5 |
| MLP | Feature | 50% | Reference TS | 0.854 ± 0.059 | 0.806 ± 0.057 | 0.485 ± 0.118 | 0.161 ± 0.046 | 0.082 ± 0.019 | 0.81 ± 0.37 | 182.7 ± 0.5 |
| MLP | Feature | 50% | Augmented TS | 0.854 ± 0.059 | 0.806 ± 0.057 | 0.485 ± 0.113 | 0.161 ± 0.044 | 0.118 ± 0.058 | 0.82 ± 0.37 | 182.7 ± 0.5 |

## Data and interpretation notes

- The table combines predictive metrics, probability-quality metrics and computational measurements in **one row per model × missingness scenario × calibration method**.
- `Reference` with rate `0%` means no artificially introduced missing values; it does **not** necessarily mean the original data had no missing values.
- AUROC and balanced accuracy need not change after positive temperature scaling, because it preserves ranking and the usual binary 0.5 decision boundary.
- Runtime is the pipeline-reported time per condition, **not** the elapsed time for the entire experiment. Fitting work reused across conditions must not be added as if it were repeated.
- Peak RAM includes the measured process and its child processes; values refer to reported MiB even though the underlying column is named `peak_RAM_MB`.
- The original aggregated file provides mean and standard deviation, **not seed-level observations**. Accordingly `split_seed` cannot be reconstructed from these data and no seed-level rows have been invented.
- The complete unrounded values and detailed computational fields (fit time and test prediction time, including standard deviations) are retained in [`aggregate_results.csv`](aggregate_results.csv).

**Reproducibility:** Exact package versions, model checkpoints, machine specifications and per-seed raw outputs must be documented separately. They cannot be recovered from these aggregate files alone.
