from typing import Optional, List

from pydantic import BaseModel


class ModelInput(BaseModel):
    model_name: str
    target_col: str
    feature_cols: Optional[List[str]] = None
