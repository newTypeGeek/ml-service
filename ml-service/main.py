from io import BytesIO

import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException

from logger import get_logger

logger = get_logger(__name__)

app = FastAPI()


@app.post("/file/csv")
async def upload_file(file: UploadFile):
    content = await file.read()
    f = BytesIO(content)

    try:
        df = pd.read_csv(f)
    except UnicodeDecodeError as e:
        exception = f"Failed to read the csv file {file.filename=}, {file.content_type=}, Exception={e}"
        logger.error(exception, exc_info=True)
        raise HTTPException(status_code=400, detail=exception)

    print(df)

    return {
        "status": "Successfully uploaded the file"
    }