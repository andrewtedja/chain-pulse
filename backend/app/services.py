from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from contextlib import asynccontextmanager
from dotenv import load_dotenv

from sqlalchemy.orm import Session
from fastapi import Depends
from datetime import datetime
from dateutil import parser

from .database import SessionLocal, engine
from .sentiment_analysis import analyze_sentiment
from .coins import identify_coins_in_text, COIN_KEYWORDS


from .models import Base, News

import requests
import os

load_dotenv()

API_KEY = os.getenv("CRYPTO_PANIC_API_KEY")
BASE_URL = os.getenv("CRYPTO_PANIC_BASE_URL")
print("[KEY] API_KEY =", API_KEY)
print("[BASE_URL] BASE_URL =", BASE_URL)

# coin_list = ",".join(COIN_KEYWORDS.keys())
params = {
    "auth_token": API_KEY,
    # "public": True,
    # "currencies": "BTC,ETH,SOL",
    "region": "en",
    "filter": "latest",
    "kind": "news",
    # "size": 100
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    db = SessionLocal()
    try:
        news_items = fetch_crypto_news()
        insert_news_to_db(news_items, db)
    except Exception as e:
        print("[LIFESPAN] Failed to fetch/insert news:", e)
    finally:
        db.close()
    
    yield  # App runs here

    # Optional: teardown logic if needed



app = FastAPI(lifespan=lifespan)
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= DB =================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET
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
        return data.get("results", [])
    except Exception as e:
        print("[DEBUG] Error fetching news:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch news from CryptoPanic")

# ================= Insert fetched news to DB =================
def insert_news_to_db(news_list, db):
    # Limit 100 news (latest)
    news_list = news_list[:100] 

    for news in news_list:

        # ! Skip jika sudah ada fieldnya di db
        if db.query(News).filter(News.id == news.get("id")).first():
            continue

        # print("Inserting:", news)
        text = (news.get("title") or "") + " " + (news.get("description") or "")

        mentioned_coins = identify_coins_in_text(text)

        if not mentioned_coins:
            continue

        sentiment = analyze_sentiment(text)
        score = sentiment["score"]

        for coin in mentioned_coins:
            news_item = News(
                id=news.get("id"),
                title=news.get("title"),
                description=news.get("description"),
                coin_ticker = coin,
                published_at=parser.parse(news.get("published_at")) if news.get("published_at") else None,
                sentiment_score=score
            )
            db.add(news_item)
    try:
        db.commit()
    except Exception as e:
        print("[DEBUG] DB commit error:", e)
        raise HTTPException(status_code=500, detail="DB insert failed")
    
    return {"[RESULTS] inserted": len(news_list)}


# POST 
@router.post("/api/refresh-news")
def refresh_news(db: Session = Depends(get_db)):
    news_items = fetch_crypto_news()
    result = insert_news_to_db(news_items, db)
    return {"message": "News refreshed", **result}


# ================= Table Init =================
Base.metadata.create_all(bind=engine)
app.include_router(router)