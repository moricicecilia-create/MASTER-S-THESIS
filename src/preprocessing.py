from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class ModelPreprocessor:
    """Fit preprocessing on train/context only; transform all held-out subsets."""
    def __init__(self, model_name: str, numeric_columns: list[str], categorical_columns: list[str]):
        self.model_name = model_name
        self.numeric_columns = list(numeric_columns)
        self.categorical_columns = list(categorical_columns)
        self.transformer = None
        self.feature_names_out_ = None

    @staticmethod
    def _one_hot_encoder():
        try:
            return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        except TypeError:  # compatibility with older scikit-learn
            return OneHotEncoder(handle_unknown="ignore", sparse=False)

    def fit(self, X_train: pd.DataFrame):
        if self.model_name in {"CatBoost", "TabDPT"}:
            # These libraries can work with DataFrames and their native missing-value handling.
            self.transformer = "native_dataframe"
            return self

        transformers = []
        if self.numeric_columns:
            num_steps = [("imputer", SimpleImputer(strategy="median", keep_empty_features=True))]
            if self.model_name == "MLP":
                num_steps.append(("scaler", StandardScaler()))
            transformers.append(("numeric", Pipeline(num_steps), self.numeric_columns))
        if self.categorical_columns:
            cat_pipe = Pipeline([
                ("imputer", SimpleImputer(strategy="constant", fill_value="__MISSING__", keep_empty_features=True)),
                ("onehot", self._one_hot_encoder()),
            ])
            transformers.append(("categorical", cat_pipe, self.categorical_columns))
        self.transformer = ColumnTransformer(
            transformers=transformers, remainder="drop", sparse_threshold=0.0
        )
        self.transformer.fit(X_train)
        try:
            self.feature_names_out_ = self.transformer.get_feature_names_out().tolist()
        except Exception:
            self.feature_names_out_ = None
        return self

    def transform(self, X: pd.DataFrame):
        if isinstance(self.transformer, str) and self.transformer == "native_dataframe":
            out = X.copy()
            for col in self.categorical_columns:
                out[col] = out[col].astype("object").where(out[col].notna(), "__MISSING__").astype(str)
            return out
        arr = self.transformer.transform(X)
        return np.asarray(arr, dtype=np.float32)

    def fit_transform(self, X_train: pd.DataFrame):
        return self.fit(X_train).transform(X_train)
