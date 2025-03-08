from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

API_KEY = os.environ.get("API_KEY_OLLAMA_HTTP_SERVER")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

class PromptRequest(BaseModel):
    model: str
    prompt: str

@app.post("/generate")
def generate_text(request: PromptRequest, api_key: str = Depends(verify_api_key)):
    try:
        # Check if the model is valid by running `ollama list` and parsing the output
        available_models = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            encoding="utf-8"  # Explicitly set UTF-8 encoding
        )
        if available_models.returncode != 0:
            raise HTTPException(status_code=500, detail="Failed to retrieve available models")

        model_list = [line.split()[0].replace(":latest", "") for line in available_models.stdout.splitlines() if line]
        if request.model not in model_list:
            raise HTTPException(status_code=400, detail=f"Model '{request.model}' is not supported. Available models: {', '.join(model_list)}")

        result = subprocess.run(
            ["ollama", "run", request.model, request.prompt],
            capture_output=True,
            text=True,
            encoding="utf-8"  # Explicitly set UTF-8 encoding
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return {"response": result.stdout.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Example request with API Key
# Run the server and send a request using curl:
# curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -H "X-API-Key: your_secure_api_key" -d '{"model": "mistral", "prompt": "Tell me a joke"}'
