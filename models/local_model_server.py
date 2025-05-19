from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama  # Make sure ollama Python client is installed and configured

app = FastAPI(title="Local LLM Server")

MODEL_NAME = "llama3.2:1b"

class GenerateRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate(request: GenerateRequest):
    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is empty")
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        generated_text = response["message"]["content"]
        return {"result": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
