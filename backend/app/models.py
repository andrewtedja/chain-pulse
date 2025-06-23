from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    coin_ticker = Column(String, index=True)
    published_at = Column(DateTime)
    link = Column(String)
    sentiment_score = Column(Float)
