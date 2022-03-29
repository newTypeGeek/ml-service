import unittest
from ml_service.main import app
from ml_service.core.ml_data import MLData
from fastapi.testclient import TestClient
import pandas as pd


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self._client = TestClient(app)
        self._data_filename = "test_data.csv"
        self._ml_data = MLData()

    def test_upload_csv(self):
        with open(self._data_filename, "r") as f:
            response = self._client.post("/file/csv", files={"file": ("filename", f)})
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
