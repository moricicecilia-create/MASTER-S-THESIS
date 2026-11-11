# WDBC | Experimental results

This README presents **one complete summary table** covering all **105 combinations** of five models, seven test conditions and three post-hoc calibration strategies. All numerical values are **mean ± sample standard deviation over split seeds 42, 43 and 44**; they are descriptive summaries, not statistical significance tests.

## Experimental settings

- **Models:** TabPFN-v2, TabICLv2, TabDPT, CatBoost and MLP.
- **Missing-data shift:** reference (no artificial missingness), cell-wise masking (10%, 30%, 50%) and complete-feature masking (10%, 30%, 50%). Missingness is applied to prediction inputs.
- **Calibration:** None (no additional calibration), Reference TS (temperature scaling fitted on reference calibration data), and Augmented TS (temperature scaling fitted on reference plus 10% and 30% cell-wise-masked calibration data).
- **Metrics:** AUROC and balanced accuracy (higher is better); log loss, Brier score and expected calibration error, ECE (lower is better). Runtime and peak RAM indicate computational costs.

## Unified results table

| Model | Missing pattern | Rate | Calibration | AUROC | Balanced acc. | Log loss | Brier | ECE | Runtime (s) | Peak RAM (MiB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TabPFN-v2 | Reference | 0% | None | 0.998 ± 0.003 | 0.983 ± 0.021 | 0.058 ± 0.024 | 0.015 ± 0.009 | 0.026 ± 0.005 | 73.41 ± 18.80 | 608.2 ± 0.1 |
| TabPFN-v2 | Reference | 0% | Reference TS | 0.998 ± 0.003 | 0.983 ± 0.021 | 0.082 ± 0.097 | 0.014 ± 0.011 | 0.018 ± 0.011 | 138.94 ± 36.83 | 608.2 ± 0.1 |
| TabPFN-v2 | Reference | 0% | Augmented TS | 0.998 ± 0.003 | 0.983 ± 0.021 | 0.067 ± 0.065 | 0.014 ± 0.010 | 0.018 ± 0.010 | 272.41 ± 77.82 | 608.2 ± 0.1 |
| TabPFN-v2 | Cell | 10% | None | 0.996 ± 0.004 | 0.952 ± 0.017 | 0.090 ± 0.021 | 0.025 ± 0.007 | 0.045 ± 0.012 | 59.97 ± 6.30 | 608.2 ± 0.1 |
| TabPFN-v2 | Cell | 10% | Reference TS | 0.996 ± 0.004 | 0.952 ± 0.017 | 0.133 ± 0.129 | 0.024 ± 0.012 | 0.028 ± 0.005 | 125.50 ± 14.17 | 608.2 ± 0.1 |
| TabPFN-v2 | Cell | 10% | Augmented TS | 0.996 ± 0.004 | 0.952 ± 0.017 | 0.108 ± 0.083 | 0.024 ± 0.011 | 0.029 ± 0.004 | 258.97 ± 54.74 | 608.2 ± 0.1 |
| TabPFN-v2 | Cell | 30% | None | 0.992 ± 0.006 | 0.932 ± 0.018 | 0.136 ± 0.020 | 0.039 ± 0.006 | 0.045 ± 0.011 | 59.64 ± 5.70 | 608.2 ± 0.1 |
| TabPFN-v2 | Cell | 30% | Reference TS | 0.992 ± 0.006 | 0.932 ± 0.018 | 0.226 ± 0.164 | 0.042 ± 0.011 | 0.041 ± 0.008 | 125.17 ± 13.00 | 608.2 ± 0.1 |
| TabPFN-v2 | Cell | 30% | Augmented TS | 0.992 ± 0.006 | 0.932 ± 0.018 | 0.178 ± 0.100 | 0.041 ± 0.010 | 0.042 ± 0.013 | 258.64 ± 54.02 | 608.2 ± 0.1 |
| TabPFN-v2 | Cell | 50% | None | 0.979 ± 0.014 | 0.869 ± 0.008 | 0.234 ± 0.018 | 0.071 ± 0.002 | 0.083 ± 0.022 | 59.04 ± 5.38 | 608.2 ± 0.1 |
| TabPFN-v2 | Cell | 50% | Reference TS | 0.979 ± 0.014 | 0.869 ± 0.008 | 0.390 ± 0.189 | 0.081 ± 0.008 | 0.094 ± 0.008 | 124.57 ± 13.37 | 608.2 ± 0.1 |
| TabPFN-v2 | Cell | 50% | Augmented TS | 0.979 ± 0.014 | 0.869 ± 0.008 | 0.308 ± 0.110 | 0.077 ± 0.005 | 0.092 ± 0.007 | 258.04 ± 54.38 | 608.2 ± 0.1 |
| TabPFN-v2 | Feature | 10% | None | 0.994 ± 0.007 | 0.957 ± 0.025 | 0.092 ± 0.046 | 0.024 ± 0.014 | 0.034 ± 0.007 | 59.70 ± 6.02 | 608.2 ± 0.1 |
| TabPFN-v2 | Feature | 10% | Reference TS | 0.994 ± 0.007 | 0.957 ± 0.025 | 0.141 ± 0.156 | 0.023 ± 0.016 | 0.028 ± 0.012 | 125.23 ± 12.76 | 608.2 ± 0.1 |
| TabPFN-v2 | Feature | 10% | Augmented TS | 0.994 ± 0.007 | 0.957 ± 0.025 | 0.111 ± 0.105 | 0.023 ± 0.016 | 0.022 ± 0.010 | 258.70 ± 53.75 | 608.2 ± 0.1 |
| TabPFN-v2 | Feature | 30% | None | 0.992 ± 0.011 | 0.934 ± 0.027 | 0.143 ± 0.070 | 0.039 ± 0.020 | 0.067 ± 0.023 | 60.51 ± 2.84 | 608.2 ± 0.1 |
| TabPFN-v2 | Feature | 30% | Reference TS | 0.992 ± 0.011 | 0.934 ± 0.027 | 0.211 ± 0.226 | 0.037 ± 0.021 | 0.044 ± 0.027 | 126.05 ± 15.71 | 608.2 ± 0.1 |
| TabPFN-v2 | Feature | 30% | Augmented TS | 0.992 ± 0.011 | 0.934 ± 0.027 | 0.170 ± 0.149 | 0.037 ± 0.020 | 0.047 ± 0.024 | 259.52 ± 56.80 | 608.2 ± 0.1 |
| TabPFN-v2 | Feature | 50% | None | 0.984 ± 0.005 | 0.888 ± 0.061 | 0.213 ± 0.065 | 0.064 ± 0.023 | 0.084 ± 0.041 | 62.72 ± 0.53 | 608.2 ± 0.1 |
| TabPFN-v2 | Feature | 50% | Reference TS | 0.984 ± 0.005 | 0.888 ± 0.061 | 0.298 ± 0.119 | 0.069 ± 0.027 | 0.083 ± 0.031 | 128.25 ± 18.97 | 608.2 ± 0.1 |
| TabPFN-v2 | Feature | 50% | Augmented TS | 0.984 ± 0.005 | 0.888 ± 0.061 | 0.250 ± 0.091 | 0.067 ± 0.027 | 0.082 ± 0.033 | 261.73 ± 60.09 | 608.2 ± 0.1 |
| TabICLv2 | Reference | 0% | None | 0.999 ± 0.001 | 0.989 ± 0.010 | 0.049 ± 0.021 | 0.013 ± 0.007 | 0.022 ± 0.015 | 19.62 ± 0.77 | 864.1 ± 2.4 |
| TabICLv2 | Reference | 0% | Reference TS | 0.999 ± 0.001 | 0.989 ± 0.010 | 0.042 ± 0.031 | 0.011 ± 0.009 | 0.017 ± 0.010 | 37.32 ± 0.61 | 864.1 ± 2.4 |
| TabICLv2 | Reference | 0% | Augmented TS | 0.999 ± 0.001 | 0.989 ± 0.010 | 0.039 ± 0.030 | 0.010 ± 0.009 | 0.013 ± 0.008 | 70.82 ± 1.56 | 864.1 ± 2.4 |
| TabICLv2 | Cell | 10% | None | 0.997 ± 0.003 | 0.965 ± 0.020 | 0.112 ± 0.021 | 0.028 ± 0.007 | 0.065 ± 0.019 | 19.79 ± 1.12 | 864.1 ± 2.4 |
| TabICLv2 | Cell | 10% | Reference TS | 0.997 ± 0.003 | 0.965 ± 0.020 | 0.085 ± 0.033 | 0.024 ± 0.010 | 0.035 ± 0.004 | 37.48 ± 0.96 | 864.1 ± 2.4 |
| TabICLv2 | Cell | 10% | Augmented TS | 0.997 ± 0.003 | 0.965 ± 0.020 | 0.078 ± 0.032 | 0.023 ± 0.010 | 0.031 ± 0.007 | 70.98 ± 1.91 | 864.1 ± 2.4 |
| TabICLv2 | Cell | 30% | None | 0.992 ± 0.008 | 0.916 ± 0.005 | 0.201 ± 0.016 | 0.052 ± 0.006 | 0.108 ± 0.028 | 19.82 ± 0.81 | 864.1 ± 2.4 |
| TabICLv2 | Cell | 30% | Reference TS | 0.992 ± 0.008 | 0.916 ± 0.005 | 0.151 ± 0.038 | 0.043 ± 0.008 | 0.057 ± 0.018 | 37.52 ± 0.65 | 864.1 ± 2.4 |
| TabICLv2 | Cell | 30% | Augmented TS | 0.992 ± 0.008 | 0.916 ± 0.005 | 0.146 ± 0.036 | 0.043 ± 0.007 | 0.051 ± 0.009 | 71.02 ± 1.60 | 864.1 ± 2.4 |
| TabICLv2 | Cell | 50% | None | 0.982 ± 0.015 | 0.846 ± 0.045 | 0.299 ± 0.018 | 0.087 ± 0.007 | 0.147 ± 0.034 | 19.96 ± 0.68 | 864.1 ± 2.4 |
| TabICLv2 | Cell | 50% | Reference TS | 0.982 ± 0.015 | 0.846 ± 0.045 | 0.266 ± 0.021 | 0.083 ± 0.009 | 0.100 ± 0.034 | 37.66 ± 0.61 | 864.1 ± 2.4 |
| TabICLv2 | Cell | 50% | Augmented TS | 0.982 ± 0.015 | 0.846 ± 0.045 | 0.272 ± 0.027 | 0.084 ± 0.010 | 0.105 ± 0.036 | 71.16 ± 1.54 | 864.1 ± 2.4 |
| TabICLv2 | Feature | 10% | None | 0.995 ± 0.006 | 0.957 ± 0.020 | 0.122 ± 0.037 | 0.029 ± 0.008 | 0.069 ± 0.019 | 19.75 ± 0.77 | 864.1 ± 2.4 |
| TabICLv2 | Feature | 10% | Reference TS | 0.995 ± 0.006 | 0.957 ± 0.020 | 0.092 ± 0.043 | 0.022 ± 0.006 | 0.030 ± 0.005 | 37.44 ± 0.56 | 864.1 ± 2.4 |
| TabICLv2 | Feature | 10% | Augmented TS | 0.995 ± 0.006 | 0.957 ± 0.020 | 0.085 ± 0.042 | 0.022 ± 0.006 | 0.034 ± 0.012 | 70.94 ± 1.49 | 864.1 ± 2.4 |
| TabICLv2 | Feature | 30% | None | 0.998 ± 0.002 | 0.953 ± 0.041 | 0.221 ± 0.044 | 0.054 ± 0.017 | 0.156 ± 0.025 | 19.72 ± 0.84 | 864.1 ± 2.4 |
| TabICLv2 | Feature | 30% | Reference TS | 0.998 ± 0.002 | 0.953 ± 0.041 | 0.131 ± 0.032 | 0.034 ± 0.014 | 0.080 ± 0.013 | 37.41 ± 0.78 | 864.1 ± 2.4 |
| TabICLv2 | Feature | 30% | Augmented TS | 0.998 ± 0.002 | 0.953 ± 0.041 | 0.117 ± 0.051 | 0.032 ± 0.018 | 0.068 ± 0.019 | 70.91 ± 1.71 | 864.1 ± 2.4 |
| TabICLv2 | Feature | 50% | None | 0.982 ± 0.011 | 0.849 ± 0.140 | 0.313 ± 0.083 | 0.091 ± 0.035 | 0.169 ± 0.069 | 19.64 ± 0.82 | 864.1 ± 2.4 |
| TabICLv2 | Feature | 50% | Reference TS | 0.982 ± 0.011 | 0.849 ± 0.140 | 0.282 ± 0.120 | 0.084 ± 0.055 | 0.118 ± 0.072 | 37.33 ± 0.63 | 864.1 ± 2.4 |
| TabICLv2 | Feature | 50% | Augmented TS | 0.982 ± 0.011 | 0.849 ± 0.140 | 0.281 ± 0.144 | 0.085 ± 0.060 | 0.114 ± 0.082 | 70.83 ± 1.57 | 864.1 ± 2.4 |
| TabDPT | Reference | 0% | None | 0.999 ± 0.001 | 0.980 ± 0.020 | 0.058 ± 0.025 | 0.016 ± 0.010 | 0.035 ± 0.012 | 43.98 ± 5.64 | 925.7 ± 9.1 |
| TabDPT | Reference | 0% | Reference TS | 0.999 ± 0.001 | 0.980 ± 0.020 | 0.179 ± 0.251 | 0.019 ± 0.017 | 0.024 ± 0.018 | 62.10 ± 8.50 | 925.7 ± 9.1 |
| TabDPT | Reference | 0% | Augmented TS | 0.999 ± 0.001 | 0.980 ± 0.020 | 0.051 ± 0.041 | 0.016 ± 0.014 | 0.021 ± 0.016 | 104.47 ± 14.66 | 925.7 ± 9.1 |
| TabDPT | Cell | 10% | None | 0.996 ± 0.003 | 0.958 ± 0.008 | 0.127 ± 0.039 | 0.032 ± 0.012 | 0.076 ± 0.015 | 53.43 ± 12.50 | 925.7 ± 9.1 |
| TabDPT | Cell | 10% | Reference TS | 0.996 ± 0.003 | 0.958 ± 0.008 | 0.254 ± 0.297 | 0.034 ± 0.018 | 0.039 ± 0.018 | 71.54 ± 12.92 | 925.7 ± 9.1 |
| TabDPT | Cell | 10% | Augmented TS | 0.996 ± 0.003 | 0.958 ± 0.008 | 0.092 ± 0.045 | 0.030 ± 0.015 | 0.034 ± 0.015 | 113.91 ± 21.08 | 925.7 ± 9.1 |
| TabDPT | Cell | 30% | None | 0.994 ± 0.003 | 0.953 ± 0.016 | 0.228 ± 0.042 | 0.057 ± 0.016 | 0.145 ± 0.019 | 49.45 ± 8.73 | 925.7 ± 9.1 |
| TabDPT | Cell | 30% | Reference TS | 0.994 ± 0.003 | 0.953 ± 0.016 | 0.220 ± 0.163 | 0.041 ± 0.018 | 0.061 ± 0.022 | 67.56 ± 10.01 | 925.7 ± 9.1 |
| TabDPT | Cell | 30% | Augmented TS | 0.994 ± 0.003 | 0.953 ± 0.016 | 0.127 ± 0.063 | 0.037 ± 0.018 | 0.057 ± 0.022 | 109.93 ± 18.44 | 925.7 ± 9.1 |
| TabDPT | Cell | 50% | None | 0.968 ± 0.025 | 0.884 ± 0.048 | 0.377 ± 0.034 | 0.112 ± 0.017 | 0.185 ± 0.010 | 54.96 ± 16.24 | 925.7 ± 9.1 |
| TabDPT | Cell | 50% | Reference TS | 0.968 ± 0.025 | 0.884 ± 0.048 | 0.857 ± 1.063 | 0.102 ± 0.052 | 0.123 ± 0.046 | 73.08 ± 16.59 | 925.7 ± 9.1 |
| TabDPT | Cell | 50% | Augmented TS | 0.968 ± 0.025 | 0.884 ± 0.048 | 0.320 ± 0.132 | 0.092 ± 0.034 | 0.110 ± 0.028 | 115.45 ± 24.63 | 925.7 ± 9.1 |
| TabDPT | Feature | 10% | None | 0.995 ± 0.007 | 0.966 ± 0.038 | 0.138 ± 0.065 | 0.034 ± 0.019 | 0.090 ± 0.031 | 44.23 ± 6.47 | 925.7 ± 9.1 |
| TabDPT | Feature | 10% | Reference TS | 0.995 ± 0.007 | 0.966 ± 0.038 | 0.292 ± 0.411 | 0.033 ± 0.032 | 0.042 ± 0.028 | 62.35 ± 9.27 | 925.7 ± 9.1 |
| TabDPT | Feature | 10% | Augmented TS | 0.995 ± 0.007 | 0.966 ± 0.038 | 0.089 ± 0.070 | 0.028 ± 0.023 | 0.040 ± 0.026 | 104.72 ± 14.75 | 925.7 ± 9.1 |
| TabDPT | Feature | 30% | None | 0.997 ± 0.004 | 0.958 ± 0.009 | 0.263 ± 0.043 | 0.065 ± 0.013 | 0.191 ± 0.028 | 43.20 ± 6.92 | 925.7 ± 9.1 |
| TabDPT | Feature | 30% | Reference TS | 0.997 ± 0.004 | 0.958 ± 0.009 | 0.211 ± 0.187 | 0.037 ± 0.012 | 0.062 ± 0.007 | 61.31 ± 9.70 | 925.7 ± 9.1 |
| TabDPT | Feature | 30% | Augmented TS | 0.997 ± 0.004 | 0.958 ± 0.009 | 0.118 ± 0.027 | 0.034 ± 0.007 | 0.060 ± 0.009 | 103.68 ± 14.95 | 925.7 ± 9.1 |
| TabDPT | Feature | 50% | None | 0.984 ± 0.007 | 0.934 ± 0.015 | 0.350 ± 0.054 | 0.097 ± 0.021 | 0.200 ± 0.028 | 44.98 ± 6.67 | 925.7 ± 9.1 |
| TabDPT | Feature | 50% | Reference TS | 0.984 ± 0.007 | 0.934 ± 0.015 | 0.390 ± 0.261 | 0.063 ± 0.012 | 0.090 ± 0.033 | 63.09 ± 9.52 | 925.7 ± 9.1 |
| TabDPT | Feature | 50% | Augmented TS | 0.984 ± 0.007 | 0.934 ± 0.015 | 0.219 ± 0.046 | 0.063 ± 0.015 | 0.082 ± 0.042 | 105.46 ± 15.46 | 925.7 ± 9.1 |
| CatBoost | Reference | 0% | None | 0.989 ± 0.010 | 0.951 ± 0.023 | 0.252 ± 0.028 | 0.059 ± 0.013 | 0.156 ± 0.016 | 2.47 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Reference | 0% | Reference TS | 0.989 ± 0.010 | 0.951 ± 0.023 | 0.127 ± 0.060 | 0.036 ± 0.021 | 0.029 ± 0.018 | 2.48 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Reference | 0% | Augmented TS | 0.989 ± 0.010 | 0.951 ± 0.023 | 0.128 ± 0.055 | 0.036 ± 0.020 | 0.037 ± 0.021 | 2.48 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Cell | 10% | None | 0.986 ± 0.012 | 0.915 ± 0.047 | 0.297 ± 0.023 | 0.077 ± 0.010 | 0.178 ± 0.013 | 2.47 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Cell | 10% | Reference TS | 0.986 ± 0.012 | 0.915 ± 0.047 | 0.173 ± 0.040 | 0.052 ± 0.015 | 0.053 ± 0.011 | 2.48 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Cell | 10% | Augmented TS | 0.986 ± 0.012 | 0.915 ± 0.047 | 0.174 ± 0.036 | 0.052 ± 0.015 | 0.057 ± 0.012 | 2.48 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Cell | 30% | None | 0.980 ± 0.019 | 0.794 ± 0.005 | 0.371 ± 0.016 | 0.109 ± 0.006 | 0.196 ± 0.023 | 2.47 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Cell | 30% | Reference TS | 0.980 ± 0.019 | 0.794 ± 0.005 | 0.307 ± 0.037 | 0.098 ± 0.008 | 0.126 ± 0.014 | 2.48 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Cell | 30% | Augmented TS | 0.980 ± 0.019 | 0.794 ± 0.005 | 0.302 ± 0.032 | 0.097 ± 0.008 | 0.124 ± 0.013 | 2.48 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Cell | 50% | None | 0.962 ± 0.028 | 0.620 ± 0.039 | 0.473 ± 0.009 | 0.156 ± 0.004 | 0.240 ± 0.053 | 2.47 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Cell | 50% | Reference TS | 0.962 ± 0.028 | 0.620 ± 0.039 | 0.594 ± 0.037 | 0.194 ± 0.013 | 0.242 ± 0.011 | 2.48 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Cell | 50% | Augmented TS | 0.962 ± 0.028 | 0.620 ± 0.039 | 0.571 ± 0.030 | 0.190 ± 0.010 | 0.236 ± 0.008 | 2.48 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Feature | 10% | None | 0.987 ± 0.011 | 0.920 ± 0.030 | 0.286 ± 0.028 | 0.072 ± 0.012 | 0.176 ± 0.031 | 2.47 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Feature | 10% | Reference TS | 0.987 ± 0.011 | 0.920 ± 0.030 | 0.168 ± 0.063 | 0.049 ± 0.022 | 0.053 ± 0.015 | 2.48 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Feature | 10% | Augmented TS | 0.987 ± 0.011 | 0.920 ± 0.030 | 0.167 ± 0.057 | 0.048 ± 0.021 | 0.054 ± 0.011 | 2.48 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Feature | 30% | None | 0.989 ± 0.009 | 0.672 ± 0.184 | 0.411 ± 0.059 | 0.128 ± 0.030 | 0.228 ± 0.055 | 2.47 ± 0.58 | 219.3 ± 0.3 |
| CatBoost | Feature | 30% | Reference TS | 0.989 ± 0.009 | 0.672 ± 0.184 | 0.398 ± 0.175 | 0.141 ± 0.071 | 0.187 ± 0.095 | 2.48 ± 0.58 | 219.3 ± 0.3 |
| CatBoost | Feature | 30% | Augmented TS | 0.989 ± 0.009 | 0.672 ± 0.184 | 0.389 ± 0.163 | 0.138 ± 0.067 | 0.183 ± 0.092 | 2.49 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Feature | 50% | None | 0.982 ± 0.015 | 0.589 ± 0.080 | 0.456 ± 0.040 | 0.149 ± 0.017 | 0.235 ± 0.035 | 2.47 ± 0.59 | 219.3 ± 0.3 |
| CatBoost | Feature | 50% | Reference TS | 0.982 ± 0.015 | 0.589 ± 0.080 | 0.515 ± 0.110 | 0.182 ± 0.041 | 0.239 ± 0.033 | 2.48 ± 0.60 | 219.3 ± 0.3 |
| CatBoost | Feature | 50% | Augmented TS | 0.982 ± 0.015 | 0.589 ± 0.080 | 0.503 ± 0.114 | 0.179 ± 0.042 | 0.234 ± 0.035 | 2.49 ± 0.60 | 219.3 ± 0.3 |
| MLP | Reference | 0% | None | 0.997 ± 0.001 | 0.973 ± 0.007 | 0.073 ± 0.014 | 0.021 ± 0.004 | 0.021 ± 0.009 | 1.02 ± 0.24 | 180.8 ± 0.0 |
| MLP | Reference | 0% | Reference TS | 0.997 ± 0.001 | 0.973 ± 0.007 | 0.115 ± 0.081 | 0.022 ± 0.003 | 0.022 ± 0.010 | 1.02 ± 0.24 | 180.8 ± 0.0 |
| MLP | Reference | 0% | Augmented TS | 0.997 ± 0.001 | 0.973 ± 0.007 | 0.071 ± 0.013 | 0.021 ± 0.003 | 0.022 ± 0.011 | 1.03 ± 0.24 | 180.8 ± 0.0 |
| MLP | Cell | 10% | None | 0.996 ± 0.001 | 0.959 ± 0.006 | 0.088 ± 0.006 | 0.026 ± 0.001 | 0.022 ± 0.003 | 1.02 ± 0.24 | 180.8 ± 0.0 |
| MLP | Cell | 10% | Reference TS | 0.996 ± 0.001 | 0.959 ± 0.006 | 0.153 ± 0.123 | 0.028 ± 0.005 | 0.029 ± 0.005 | 1.02 ± 0.24 | 180.8 ± 0.0 |
| MLP | Cell | 10% | Augmented TS | 0.996 ± 0.001 | 0.959 ± 0.006 | 0.088 ± 0.011 | 0.026 ± 0.002 | 0.025 ± 0.008 | 1.03 ± 0.24 | 180.8 ± 0.0 |
| MLP | Cell | 30% | None | 0.987 ± 0.006 | 0.926 ± 0.010 | 0.146 ± 0.009 | 0.043 ± 0.004 | 0.040 ± 0.012 | 1.02 ± 0.24 | 180.8 ± 0.0 |
| MLP | Cell | 30% | Reference TS | 0.987 ± 0.006 | 0.926 ± 0.010 | 0.261 ± 0.199 | 0.043 ± 0.006 | 0.044 ± 0.011 | 1.02 ± 0.24 | 180.8 ± 0.0 |
| MLP | Cell | 30% | Augmented TS | 0.987 ± 0.006 | 0.926 ± 0.010 | 0.155 ± 0.020 | 0.043 ± 0.006 | 0.044 ± 0.010 | 1.03 ± 0.24 | 180.8 ± 0.0 |
| MLP | Cell | 50% | None | 0.978 ± 0.015 | 0.858 ± 0.002 | 0.229 ± 0.041 | 0.073 ± 0.011 | 0.073 ± 0.008 | 1.02 ± 0.24 | 180.8 ± 0.0 |
| MLP | Cell | 50% | Reference TS | 0.978 ± 0.015 | 0.858 ± 0.002 | 0.483 ± 0.458 | 0.085 ± 0.026 | 0.094 ± 0.021 | 1.02 ± 0.24 | 180.8 ± 0.0 |
| MLP | Cell | 50% | Augmented TS | 0.978 ± 0.015 | 0.858 ± 0.002 | 0.255 ± 0.073 | 0.077 ± 0.015 | 0.086 ± 0.010 | 1.03 ± 0.24 | 180.8 ± 0.0 |
| MLP | Feature | 10% | None | 0.992 ± 0.005 | 0.965 ± 0.019 | 0.091 ± 0.025 | 0.025 ± 0.007 | 0.031 ± 0.012 | 1.02 ± 0.24 | 180.8 ± 0.0 |
| MLP | Feature | 10% | Reference TS | 0.992 ± 0.005 | 0.965 ± 0.019 | 0.180 ± 0.183 | 0.026 ± 0.010 | 0.030 ± 0.010 | 1.02 ± 0.24 | 180.8 ± 0.0 |
| MLP | Feature | 10% | Augmented TS | 0.992 ± 0.005 | 0.965 ± 0.019 | 0.095 ± 0.037 | 0.025 ± 0.008 | 0.027 ± 0.005 | 1.03 ± 0.24 | 180.8 ± 0.0 |
| MLP | Feature | 30% | None | 0.996 ± 0.003 | 0.943 ± 0.045 | 0.121 ± 0.042 | 0.035 ± 0.015 | 0.056 ± 0.011 | 1.02 ± 0.25 | 180.8 ± 0.0 |
| MLP | Feature | 30% | Reference TS | 0.996 ± 0.003 | 0.943 ± 0.045 | 0.201 ± 0.183 | 0.039 ± 0.025 | 0.053 ± 0.021 | 1.03 ± 0.25 | 180.8 ± 0.0 |
| MLP | Feature | 30% | Augmented TS | 0.996 ± 0.003 | 0.943 ± 0.045 | 0.119 ± 0.050 | 0.035 ± 0.017 | 0.055 ± 0.019 | 1.03 ± 0.25 | 180.8 ± 0.0 |
| MLP | Feature | 50% | None | 0.980 ± 0.011 | 0.861 ± 0.066 | 0.243 ± 0.112 | 0.077 ± 0.036 | 0.084 ± 0.064 | 1.02 ± 0.24 | 180.8 ± 0.0 |
| MLP | Feature | 50% | Reference TS | 0.980 ± 0.011 | 0.861 ± 0.066 | 0.553 ± 0.613 | 0.090 ± 0.055 | 0.100 ± 0.058 | 1.03 ± 0.24 | 180.8 ± 0.0 |
| MLP | Feature | 50% | Augmented TS | 0.980 ± 0.011 | 0.861 ± 0.066 | 0.273 ± 0.153 | 0.081 ± 0.042 | 0.093 ± 0.064 | 1.04 ± 0.24 | 180.8 ± 0.0 |

## Data and interpretation notes

- The table combines predictive metrics, probability-quality metrics and computational measurements in **one row per model × missingness scenario × calibration method**.
- `Reference` with rate `0%` means no artificially introduced missing values; it does **not** necessarily mean the original data had no missing values.
- AUROC and balanced accuracy need not change after positive temperature scaling, because it preserves ranking and the usual binary 0.5 decision boundary.
- Runtime is the pipeline-reported time per condition, **not** the elapsed time for the entire experiment. Fitting work reused across conditions must not be added as if it were repeated.
- Peak RAM includes the measured process and its child processes; values refer to reported MiB even though the underlying column is named `peak_RAM_MB`.
- The original aggregated file provides mean and standard deviation, **not seed-level observations**. Accordingly `split_seed` cannot be reconstructed from these data and no seed-level rows have been invented.
- The complete unrounded values and detailed computational fields (fit time and test prediction time, including standard deviations) are retained in [`aggregate_results.csv`](aggregate_results.csv).

**Reproducibility:** Exact package versions, model checkpoints, machine specifications and per-seed raw outputs must be documented separately. They cannot be recovered from these aggregate files alone.
