import pandas as pd
from typing import List, Optional


class MLData:
    def __init__(self):
        self._train_data: pd.DataFrame = pd.DataFrame()
        self._target_col: str = ""
        self._feature_cols: List[str] = []

    @property
    def train_data_(self):
        return self._train_data

    @property
    def target_col_(self):
        return self._target_col

    @property
    def feature_cols_(self):
        return self._feature_cols

    def update_train_data(self, data: pd.DataFrame):
        self._train_data = data

    def update_target_feature_cols(self, target_col: str, feature_cols: Optional[List[str]] = None):
        data_cols = self._train_data.columns

        if target_col not in data_cols:
            raise ValueError

        if feature_cols is not None:
            for feature_col in feature_cols:
                if feature_col not in data_cols:
                    raise ValueError
            feature_cols_ = feature_cols
        else:
            # remaining columns in the dataframe (in order) is regarded as feature_cols
            feature_cols_ = [col for col in data_cols if col != target_col]

        self._target_col = target_col
        self._feature_cols = feature_cols_
