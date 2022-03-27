from typing import List

import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from .ml_model import MLModel


class RandomForest(MLModel):
    def __init__(self, **kwargs):
        super().__init__()
        if kwargs.get("random_state"):
            kwargs.update({"random_state": 1})

        self._model = RandomForestRegressor(**kwargs)

    def fit(self, data: pd.DataFrame, target_col: str, feature_cols: List[str]):
        features = data[feature_cols]
        target = data[target_col]
        self._model.fit(features, target)

    def predict(self, data: pd.DataFrame, feature_cols: List[str]) -> pd.DataFrame:
        features = data[feature_cols]
        predictions = self._model.predict(features)
        data["prediction"] = predictions
        return data


