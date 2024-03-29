from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, pool_size=50, max_overflow=100)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
