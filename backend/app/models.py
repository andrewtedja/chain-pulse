from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    slug = Column(String)
    published_at = Column(DateTime)
    created_at = Column(DateTime)
    kind = Column(String)
    link = Column(String)
