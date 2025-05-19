# app/core/model_router.py

import os
import requests
from typing import Literal

LLM_BACKEND: Literal["local", "openai"] = os.getenv("LLM_BACKEND", "local")

LOCAL_MODEL_URL = os.getenv("LOCAL_MODEL_URL", "http://localhost:8000/generate")  # updated default for local dev

def generate_answer(prompt: str) -> str:
    if LLM_BACKEND == "local":
        response = requests.post(
            LOCAL_MODEL_URL,
            json={"prompt": prompt},
            timeout=30  # Optional: fail fast on local models
        )
        if response.status_code != 200:
            raise RuntimeError(f"Local model failed: {response.text}")
        return response.json()["result"]

    elif LLM_BACKEND == "openai":
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        chat_response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful business analyst."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return chat_response.choices[0].message["content"].strip()

    else:
        raise ValueError("Invalid LLM_BACKEND. Choose 'local' or 'openai'.")
