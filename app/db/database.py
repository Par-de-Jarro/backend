import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.settings import MAX_OVERFLOW, POOL_SIZE, SILENT_ENVIROMENTS, SQLALCHEMY_DATABASE_URL

ECHO_QUERIES = False if os.getenv("ENVIRONMENT") in SILENT_ENVIROMENTS else True
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=ECHO_QUERIES, pool_size=POOL_SIZE, max_overflow=MAX_OVERFLOW
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
