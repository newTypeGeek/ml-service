import pickle
from io import BytesIO

import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse

from core.ml_data import MLData
from core.sklearn_model import SklearnModel
from logger import get_logger
from schema import ModelInput, ModelFrameWork

logger = get_logger(__name__)
app = FastAPI()
ml_data = MLData()


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
    framework = model_input.framework
    model_name = model_input.model_name
    params = model_input.params
    target_col = model_input.target_col
    feature_cols = model_input.feature_cols

    error_msg = ml_data.update_target_feature_cols(target_col, feature_cols)
    if error_msg:
        raise HTTPException(status_code=400, detail=error_msg)

    # TODO: currently only support sklearn, will support other framework later
    if framework == ModelFrameWork.sklearn:
        model_class = SklearnModel.get_model_class(model_name)
        sklearn_model = SklearnModel()
        sklearn_model.create_model(model_class, **params)
        sklearn_model.fit(
            data=ml_data.train_data_,
            target_col=ml_data.target_col_,
            feature_cols=ml_data.feature_cols_
        )
        f = pickle.dumps(sklearn_model.model_)
        return StreamingResponse(BytesIO(f))
