from abc import ABC, abstractmethod
from typing import List

import pandas as pd


class MLModel(ABC):
    def __init__(self):
        self._model = None

    @abstractmethod
    def fit(self, data: pd.DataFrame, target_col: str, feature_cols: List[str]):
        raise NotImplementedError

    @abstractmethod
    def predict(self, data: pd.DataFrame, feature_cols: List[str]) -> pd.DataFrame:
        raise NotImplementedError
