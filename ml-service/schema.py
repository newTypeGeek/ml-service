from typing import Optional, List
from enum import Enum
from pydantic import BaseModel


class ModelFrameWork(str, Enum):
    sklearn = "sklearn"


class ModelInput(BaseModel):
    framework: ModelFrameWork = ModelFrameWork.sklearn
    model_name: str
    params: dict = {}
    target_col: str
    feature_cols: Optional[List[str]] = None

