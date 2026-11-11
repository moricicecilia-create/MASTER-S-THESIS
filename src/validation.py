"""Fail before model loading when the experimental protocol is invalid."""
import math
import re

METHODS = ('No additional calibration', 'Reference calibration', 'Missingness-augmented calibration')
MODELS = ('TabPFN-v2', 'TabICLv2', 'TabDPT', 'CatBoost', 'MLP')


def safe_name(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', value):
        raise ValueError(f'Invalid dataset name: {value!r}')
    return value


def validate_experiment(c):
    seeds = c['seeds']
    if not seeds or len(seeds) != len(set(seeds)) or any(type(s) is not int or not 0 <= s < 2**32 for s in seeds):
        raise ValueError('Seeds must be distinct integers in [0, 2**32).')
    if type(c['threads']) is not int or c['threads'] < 1:
        raise ValueError('threads must be a positive integer.')
    ratios = [float(c['split'][k]) for k in ('train_context','validation','calibration','test')]
    if not all(math.isfinite(x) and x > 0 for x in ratios) or not math.isclose(sum(ratios), 1):
        raise ValueError('Four positive split ratios must sum to one.')
    for key in ('cell_rates','feature_rates','augmentation_cell_rates'):
        rates = c['missingness'][key]
        if len(rates) != len(set(rates)) or any(not math.isfinite(float(r)) or not 0 < float(r) <= 1 for r in rates):
            raise ValueError(f'{key}: rates must be distinct and in (0, 1].')
    cal = c['calibration']; methods = cal['methods']
    if not methods or len(set(methods)) != len(methods) or set(methods)-set(METHODS):
        raise ValueError('Invalid or duplicate calibration methods.')
    lo, hi = float(cal['temperature_min']), float(cal['temperature_max'])
    if not (math.isfinite(lo) and math.isfinite(hi) and 0 < lo < hi):
        raise ValueError('Require 0 < temperature_min < temperature_max.')
    for key in ('ece_bins','reliability_bins'):
        if type(cal[key]) is not int or cal[key] < 1: raise ValueError(f'{key} must be a positive integer.')
    for key in ('mask_seed_offset_calibration','mask_seed_offset_test'):
        if type(c['missingness'][key]) is not int or c['missingness'][key] < 0:
            raise ValueError(f'{key} must be a nonnegative integer.')
    if c['missingness']['mask_seed_offset_calibration'] == c['missingness']['mask_seed_offset_test']:
        raise ValueError('Calibration and test mask offsets must differ.')
    for key in ('max_epochs','patience'):
        if type(c['mlp'][key]) is not int or c['mlp'][key] < 1: raise ValueError(f'{key} must be positive.')
    if not c['mlp']['hidden_layer_sizes'] or any(type(x) is not int or x<1 for x in c['mlp']['hidden_layer_sizes']):
        raise ValueError('Invalid MLP hidden layer sizes.')
