
import os

from dotenv import load_dotenv

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

# LOAD ENV
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

# ENGINE
engine = create_engine(
    DATABASE_URL
)

# SESSION
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# NEW SQLALCHEMY SESSION
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# TEMP COMPATIBILITY FIX
def get_connection():

    return engine.raw_connection()
