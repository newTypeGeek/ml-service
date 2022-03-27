from io import BytesIO
from typing import List, Optional

import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel

from core.ml_data import MLData
from core.model.linear_regressor import LinearRegressor
from logger import get_logger

logger = get_logger(__name__)
app = FastAPI()
ml_data = MLData()


class ModelInput(BaseModel):
    model_name: str
    target_col: str
    feature_cols: Optional[List[str]] = None


@app.post("/file/csv")
async def upload_file(file: UploadFile):
    content = await file.read()
    f = BytesIO(content)

    try:
        df: pd.DataFrame = pd.read_csv(f)
    except UnicodeDecodeError as e:
        message = f"Failed to read the csv file {file.filename=}, {file.content_type=}, Exception={e}"
        logger.error(message, exc_info=True)
        raise HTTPException(status_code=400, detail=message)

    if df.empty:
        message = "The uploaded csv file is an empty dataframe"
        logger.error(message)
        raise HTTPException(status_code=400, detail=message)

    error_msg = ml_data.update_train_data(df)
    if error_msg:
        raise HTTPException(status_code=400, detail=error_msg)

    return {
        "status": "Successfully uploaded the file"
    }


@app.post("/train")
def train_model(model_input: ModelInput):
    model_name = model_input.model_name
    target_col = model_input.target_col
    feature_cols = model_input.feature_cols

    error_msg = ml_data.update_target_feature_cols(target_col, feature_cols)
    if error_msg:
        raise HTTPException(status_code=400, detail=error_msg)

    model = LinearRegressor()
    model.fit(
        data=ml_data.train_data_,
        target_col=ml_data.target_col_,
        feature_cols=ml_data.feature_cols_
    )

    data_out = model.predict(
        data=ml_data.train_data_,
        feature_cols=ml_data.feature_cols_
    )

    print(data_out)

    return {}

