from enum import Enum
from typing import Optional, List

from pydantic import BaseModel
from core import model


class ModelType(str, Enum):
    linear_regressor = model.Linear.__name__
    random_forest = model.RandomForest.__name__


class ModelInput(BaseModel):
    model_name: ModelType
    target_col: str
    feature_cols: Optional[List[str]] = None
