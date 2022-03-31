import unittest

from fastapi.testclient import TestClient

from ml_service.core.ml_data import MLData
from ml_service.main import app


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self._client = TestClient(app)
        self._data_filename = "test_data.csv"
        self._ml_data = MLData()

    def test_train_model(self):
        with open(self._data_filename, "r") as f:
            res_upload = self._client.post("/file/csv", files={"file": ("filename", f)})
            self.assertEqual(res_upload.status_code, 200)

        req_body = {
            "framework": "sklearn",
            "model_name": "LinearRegression",
            "target_col": "target"
        }
        res_train = self._client.post("/train", json=req_body)
        self.assertEqual(res_train.status_code, 200)
        self.assertEqual(type(res_train.content), bytes)


if __name__ == '__main__':
    unittest.main()
