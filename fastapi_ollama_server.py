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
    model: str
    prompt: str
    # 'options' can hold advanced generation parameters like temperature, top_k, etc.
    # Provide an empty dict by default so it's always present but optional.
    options: dict = Field(default_factory=dict)


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
