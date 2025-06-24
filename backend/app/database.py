from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLITE_URL = "sqlite:///./news.db"
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./patterns.db")

engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)