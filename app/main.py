from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(
    title="Tally AI Infrastructure",
    description="API for chat-based financial Q&A using local and OpenAI LLMs",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api")

# Optional: root endpoint for quick health check
@app.get("/")
async def root():
    return {"message": "Welcome to Tally AI Infrastructure API!"}
