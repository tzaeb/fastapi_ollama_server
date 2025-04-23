# FastAPI Ollama Server

This project sets up a FastAPI server that interfaces with the Ollama Python package to generate text responses based on user prompts. The server supports API key authentication and allows users to interact with various machine learning models via HTTP requests.

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
   uvicorn fastapi_ollama_server:app --host 0.0.0.0 --port 8000
   ```

   The server will be available at `http://localhost:8000`.

## API Documentation

The server exposes a POST endpoint:

### `POST /generate`

Generates text based on the provided model, prompt, and optional generation parameters.

**Request Body:**
```json
{
  "model": "gemma3:1b",
  "prompt": "Tell me a joke",
  "options": {
    "temperature": 0.7,
    "num_predict": 100,
    "top_k": 40,
    "top_p": 0.9,
    "stop": ["\n\n"],
    "repeat_penalty": 1.1,
    "seed": 42
  }
}
```

**Parameters:**
- `prompt` (required): The input text prompt
- `model` (optional): Name of the Ollama model to use
- `options` (optional): Dictionary containing generation parameters:
  - `temperature` (optional, 0.0-2.0): Controls randomness in generation
  - `num_predict` (optional, >0): Maximum number of tokens to generate
  - `top_k` (optional, ≥0): Top K sampling parameter
  - `top_p` (optional, 0.0-1.0): Top P (nucleus) sampling parameter
  - `stop` (optional): List of sequences where generation should stop
  - `repeat_penalty` (optional, ≥0): Penalty for repeated tokens
  - `seed` (optional): Random number seed for reproducible generation

**Note on Options:**
The available options and their valid ranges may vary depending on the specific model being used. Not all models support all options. For more information on model-specific options, refer to the [Ollama documentation](https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values) or check the model's specific documentation.

**Headers:**
- `X-API-Key`: Your API key (required)

**Responses:**
- `200 OK`: Successfully generated text
- `400 Bad Request`: If the model is invalid or other input is incorrect
- `403 Forbidden`: If the API key is invalid
- `500 Internal Server Error`: If there is an issue with the Ollama package

## Example Usage

See `ollama_example_request.py` for a complete example of how to use the API with generation options.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
