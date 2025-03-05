
# FastAPI Ollama Server

This project sets up a FastAPI server that interfaces with the Ollama HTTP server to generate text responses based on user prompts. The server supports API key authentication and allows users to interact with various machine learning models via HTTP requests.


## Setup

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your environment variable for the API key:
   ```bash
   export API_KEY_OLLAMA_HTTP_SERVER=<your_api_key>
   ```

4. Start the server:
   ```bash
   uvicorn server:app --host 0.0.0.0 --port 8000
   ```

   The server will be available at `http://localhost:8000`.

## API Documentation

The server exposes a POST endpoint:

### `POST /generate`

Generates text based on the provided model and prompt.

**Request Body:**
```json
{
  "model": "mistral",
  "prompt": "Tell me a joke"
}
```

**Headers:**
- `X-API-Key`: Your API key (required)

**Responses:**
- `200 OK`: Successfully generated text.
- `400 Bad Request`: If the model is invalid or other input is incorrect.
- `403 Forbidden`: If the API key is invalid.
- `500 Internal Server Error`: If there is an issue with the Ollama server.

## Example Usage

### Sending a Request

Using Python's `requests` library:

```python
import requests
import os

API_KEY = os.environ.get("API_KEY_OLLAMA_HTTP_SERVER")
url = "http://localhost:8000/generate"
headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}
data = {
    "model": "mistral",
    "prompt": "Tell me a joke"
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print("Response:", response.json()["response"])
else:
    print("Error:", response.status_code, response.text)
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
