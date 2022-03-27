from io import BytesIO

import pandas as pd
from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.post("/file")
async def upload_file(file: UploadFile):
    content = await file.read()
    f = BytesIO(content)

    try:
        df = pd.read_csv(f)
    except UnicodeDecodeError as e:
        print(f"Exception = {e}")
        return {
            "status": "Failed to read file",
            "reason": str(e),
        }
    print(df)

    return {
        "status": "Successfully uploaded the file"
    }
