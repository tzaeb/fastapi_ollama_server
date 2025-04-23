from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
import ollama
import os

app = FastAPI()

API_KEY = os.environ.get("API_KEY_OLLAMA_HTTP_SERVER")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")


class PromptRequest(BaseModel):
    prompt: str
    options: dict = Field(
        default_factory=lambda: {
            "temperature": 0.7,
            "top_p": 0.9,
            "stop": ["\n\n"],
        }
    )
    model: Optional[str] = "gemma3:1b"
    format: Optional[str] = None


@app.post("/generate")
def generate_text(request: PromptRequest, api_key: str = Depends(verify_api_key)):
    # Get list of available models first
    try:
        models = ollama.list()
        model_list = [model["model"] for model in models["models"]]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Failed to fetch available models", "details": str(e)},
        )

    # Validate model before attempting generation
    if request.model not in model_list:
        raise HTTPException(
            status_code=400,
            detail={
                "error": f"Model '{request.model}' is not supported.",
                "available_models": model_list,
            },
        )

    try:
        # Generate text using the specified model and prompt
        response = ollama.generate(
            model=request.model,
            prompt=request.prompt,
            options=request.options,
            format=request.format,
        )
        return {"response": response["response"]}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Generation failed", "details": str(e)},
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
