from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import Depends

from datetime import datetime
from dateutil import parser


from .models import Base, News

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

print("[KEY] API_KEY =", API_KEY)
print("[BASE_URL] BASE_URL =", BASE_URL)

params = {
    "auth_token": API_KEY,
    # "public": True,
    # "currencies": "BTC,ETH,SOL",
    "region": "en",
    "filter": "latest",
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


# ================= DB =================
@app.get("/api/news")
def read_news(db: Session = Depends(get_db)):
    news_items = db.query(News).all()
    return {
        "news": [item.__dict__ for item in news_items]
    }

# ================= Fetch API =================
def fetch_crypto_news():
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        print("✅ API response sample:", data.get("results", [])[0] if data.get("results") else "No results")
        return data.get("results", [])
    except Exception as e:
        print("❌ Error fetching news:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch news from CryptoPanic")

# ================= Insert fetched news to DB =================
def insert_news_to_db(news_list, db):
    for news in news_list:
        print("📰 Inserting news:", news)
        try:
            news_item = News(
            id=news.get("id"),
            title=news.get("title"),
            description=news.get("description"),
            published_at=parser.parse(news.get("published_at")) if news.get("published_at") else None,
            link=news.get("url")
            )

            db.add(news_item)
        except Exception as e:
            print("❌ Error adding news:", e)
    try:
        db.commit()
    except Exception as e:
        print("❌ DB commit error:", e)
        raise HTTPException(status_code=500, detail="DB insert failed")
    
    return {"inserted": len(news_list)}


# ================= API Endpoint (POST) -> Fetch + Insert to DB =================
@app.post("/api/refresh-news")
def refresh_news(db: Session = Depends(get_db)):
    news = fetch_crypto_news()
    insert_news_to_db(news, db)
    return {"message": f"{len(news)} news saved to DB"}


# ================= Run Table Create =================
Base.metadata.create_all(bind=engine)