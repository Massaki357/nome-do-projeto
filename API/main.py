import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageRequest(BaseModel):
    message: str


@app.post("/send_message")
def send_message(request: MessageRequest) -> dict:
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['API_KEY_OPENROUTER']}"},
        json={
            "model": os.environ["OPENROUTER_MODEL"],
            "messages": [{"role": "user", "content": request.message}],
        },
    )
    response.raise_for_status()
    return {"response": response.json()["choices"][0]["message"]["content"]}


def start() -> None:
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
