from sqlalchemy import Column, Integer, String, DateTime, Float, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, nullable=False)  
    title = Column(String)
    description = Column(String)
    coin_ticker = Column(String, nullable=False)
    published_at = Column(DateTime)
    sentiment_score = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint('id', 'coin_ticker'),
    )