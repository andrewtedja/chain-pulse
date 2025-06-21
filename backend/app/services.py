from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv

import requests
import os

load_dotenv()
API_KEY = os.getenv("CRYPTO_PANIC_API_KEY")
BASE_URL = os.getenv("CRYPTO_PANIC_BASE_URL")

params = {
    "auth_token": API_KEY,
    # "public": True,
    # "currencies": "BTC,ETH,SOL",
    "region": "en",
    "filter": "rising",
    "kind": "news",
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/news")
def get_news():
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "news": data.get("results", []),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
