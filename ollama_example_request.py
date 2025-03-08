import requests
import os


API_KEY = os.environ.get("API_KEY_OLLAMA_HTTP_SERVER") 
url = "http://localhost:8000/generate"
headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}
data = {
    "model": "llama3.2"
}

data["prompt"] = input("prompt:")

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print("Response:", response.json()["response"])
else:
    print("Error:", response.status_code, response.text)
