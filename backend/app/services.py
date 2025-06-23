from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import Depends

from models import Base, News

import requests
import os

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



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
def read_news(db: Session = Depends(get_db)):
    news_items = db.query(News).all()
    return {
        "news": [item.__dict__ for item in news_items]
    }

Base.metadata.create_all(bind=engine)