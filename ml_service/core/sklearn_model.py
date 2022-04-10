from typing import Any, List

import numpy as np
import pandas as pd
import sklearn.ensemble
import sklearn.linear_model
import sklearn.neural_network
import sklearn.svm

from logger import get_logger

logger = get_logger(__name__)


class SklearnModel:
    _sklearn_linear_models = dir(sklearn.linear_model)
    _sklearn_svm_models = dir(sklearn.svm)
    _sklearn_ensemble_models = dir(sklearn.ensemble)
    _sklearn_neural_models = dir(sklearn.neural_network)

    def __init__(self):
        self._model = None

    @property
    def model_(self):
        return self._model

    @classmethod
    def get_model_class(cls, model_name: str) -> Any:
        if model_name in cls._sklearn_linear_models:
            model_class = getattr(sklearn.linear_model, model_name)
        elif model_name in cls._sklearn_svm_models:
            model_class = getattr(sklearn.svm, model_name)
        elif model_name in cls._sklearn_ensemble_models:
            model_class = getattr(sklearn.ensemble, model_name)
        elif model_name in cls._sklearn_neural_models:
            model_class = getattr(sklearn.neural_network, model_name)
        else:
            logger.error(f"Failed to get sklearn model with {model_name=}")
            raise ValueError

        logger.info(f"Get model class {model_class}")
        return model_class

    def create_model(self, model, **kwargs):
        self._model = None
        logger.debug(f"Init {model} instance with {kwargs=}")
        self._model = model(**kwargs)

    def fit(self, data: pd.DataFrame, target_col: str, feature_cols: List[str]):
        features = data[feature_cols]
        target = data[target_col]
        self._model.fit(features, target)

    def predict(self, data: pd.DataFrame, feature_cols: List[str]) -> np.array:
        data_ = data.copy()
        features = data_[feature_cols]
        return self._model.predict(features)
