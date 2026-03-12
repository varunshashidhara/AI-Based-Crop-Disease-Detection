import requests

url = "http://localhost:8000/predict"
file_path = "myleaf.jpg"
try:
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
    print(response.json())
except Exception as e:
    print(f"Error: {e}")
