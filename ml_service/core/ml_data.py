from typing import List, Optional

import pandas as pd

from logger import get_logger

logger = get_logger(__name__)


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

    def update_train_data(self, data: pd.DataFrame) -> Optional[str]:
        if data.empty:
            message = "Empty training dataframe"
            logger.error(message)
            return message

        self._train_data = data
        return None

    def update_target_feature_cols(self, target_col: str, feature_cols: Optional[List[str]] = None) -> Optional[str]:
        data_cols = self._train_data.columns

        if target_col not in data_cols:
            message = f"{target_col=} does not exist in the dataframe columns. Available columns are {data_cols}"
            logger.error(message)
            return message

        if feature_cols:
            missing_cols = []
            for feature_col in feature_cols:
                if feature_col not in data_cols:
                    missing_cols.append(feature_col)

            if missing_cols:
                message = f"These requested feature columns {missing_cols} do not exist in the dataframe columns. " \
                          f"Available columns are {data_cols}"
                logger.error(message)
                return message
            feature_cols_ = feature_cols
        else:
            logger.info(f"By default, use the non-target columns as the feature columns in that order")
            # remaining columns in the dataframe (in order) is regarded as feature_cols
            feature_cols_ = [col for col in data_cols if col != target_col]

        self._target_col = target_col
        self._feature_cols = feature_cols_
        return None
