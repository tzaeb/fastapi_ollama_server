import requests
import os

API_KEY = os.environ.get("API_KEY_OLLAMA_HTTP_SERVER")

url = "http://localhost:8000/generate"
headers = {"Content-Type": "application/json", "X-API-Key": API_KEY}


# Uncomment and modify the following lines if you want to include specific parameters in the request
data = {
    # "model": "gemma3:12b",
    # "options": {
    #     "temperature": 0.7,  # Controls randomness (0.0 to 2.0)
    #     "top_p": 0.9,  # Nucleus sampling parameter (0.0 to 1.0)
    #     "stop": ["\n\n"],  # Stop sequences
    # },
    # "format": "json",  # Optional format parameter
}

data["prompt"] = input("prompt: ")

try:
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Response:", response.json()["response"])
    else:
        print("Error:", response.status_code, response.text)

except requests.exceptions.ConnectionError:
    print("ERROR: Could not connect to the server at", url)
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
