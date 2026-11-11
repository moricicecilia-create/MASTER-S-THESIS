import sys
import unittest
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.splits import make_splits
from src.missingness import make_mask, apply_mask
from src.calibration import apply_temperature, fit_temperature
from src.metrics import calculate_metrics, reliability_bins
from src.preprocessing import ModelPreprocessor
from src.models import fit_mlp_with_validation_early_stopping


class PipelineTests(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(7)
        self.X = pd.DataFrame({
            "x1": rng.normal(size=120),
            "x2": rng.normal(size=120),
            "cat": np.where(np.arange(120) % 2 == 0, "A", "B"),
        })
        self.y = np.array([0, 1] * 60)

    def test_splits_disjoint_and_complete(self):
        splits = make_splits(self.y, 42, {
            "train_context": .60, "validation": .10,
            "calibration": .15, "test": .15
        })
        all_idx = np.concatenate(list(splits.values()))
        self.assertEqual(len(all_idx), len(self.y))
        self.assertEqual(len(np.unique(all_idx)), len(self.y))

    def test_feature_mask_masks_same_columns_for_all_rows(self):
        mask = make_mask(self.X.shape, "feature", .34, 42)
        self.assertTrue(np.all(mask == mask[0:1, :]))

    def test_cell_mask_is_reproducible(self):
        a = make_mask(self.X.shape, "cell", .3, 42)
        b = make_mask(self.X.shape, "cell", .3, 42)
        self.assertTrue(np.array_equal(a, b))

    def test_apply_mask_does_not_modify_original(self):
        mask = make_mask(self.X.shape, "cell", .2, 2)
        masked = apply_mask(self.X, mask)
        self.assertFalse(self.X.isna().any().any())
        self.assertTrue(masked.isna().to_numpy().any())

    def test_temperature_identity_at_one(self):
        p = np.array([.2, .7, .8])
        self.assertTrue(np.allclose(apply_temperature(p, 1.0), p))

    def test_temperature_fit_returns_positive_scalar(self):
        y = np.array([0, 1, 0, 1, 0, 1])
        p = np.array([.4, .6, .3, .7, .2, .8])
        t = fit_temperature(y, p)
        self.assertGreater(t, 0)

    def test_metrics_and_reliability_bins(self):
        y = np.array([0, 1, 0, 1, 0, 1])
        p = np.array([.1, .9, .2, .8, .4, .6])
        metrics = calculate_metrics(y, p, ece_bins=5)
        self.assertIn("AUROC", metrics)
        self.assertGreaterEqual(metrics["ECE"], 0)
        self.assertEqual(len(reliability_bins(y, p, 5)), 5)

    def test_preprocessing_fit_on_train_and_transform(self):
        train = self.X.iloc[:80].copy()
        test = self.X.iloc[80:].copy()
        prep = ModelPreprocessor("MLP", ["x1", "x2"], ["cat"])
        a = prep.fit_transform(train)
        b = prep.transform(test)
        self.assertEqual(a.shape[1], b.shape[1])
        self.assertFalse(np.isnan(a).any())

    def test_mlp_explicit_validation_early_stopping(self):
        prep = ModelPreprocessor("MLP", ["x1", "x2"], ["cat"])
        Xtr = prep.fit_transform(self.X.iloc[:80])
        Xva = prep.transform(self.X.iloc[80:])
        model = fit_mlp_with_validation_early_stopping(
            Xtr, self.y[:80], Xva, self.y[80:],
            {"hidden_layer_sizes": [8], "alpha": .001,
             "learning_rate_init": .01, "max_epochs": 8, "patience": 3}, 42
        )
        self.assertGreaterEqual(model.best_epoch_, 1)
        self.assertEqual(model.predict_proba(Xva).shape[1], 2)


if __name__ == "__main__":
    unittest.main()
