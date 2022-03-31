curl -X 'POST' \
  'http://127.0.0.1:8000/file/csv' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@data.csv;type=text/csv'

echo

curl -X 'POST' \
  'http://127.0.0.1:8000/train' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "framework": "sklearn",
  "model_name": "LinearRegression",
  "params": {},
  "target_col": "target"
}' \
  -o "sklearn_model.pickle"