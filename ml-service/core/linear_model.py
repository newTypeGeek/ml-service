from typing import List
from .ml_model import MLModel
from sklearn.linear_model import LinearRegression

import pandas as pd


class LinearRegressor(MLModel):
    def __init__(self):
        super().__init__()
        self._model = LinearRegression()

    def fit(self, data: pd.DataFrame, target_col: str, feature_cols: List[str]):
        features = data[feature_cols]
        target = data[target_col]
        self._model.fit(features, target)

    def predict(self, data: pd.DataFrame, feature_cols: List[str]) -> pd.DataFrame:
        features = data[feature_cols]
        predictions = self._model.predict(features)
        data["prediction"] = predictions
        return data


