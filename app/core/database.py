"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from dotenv import load_dotenv

# Ensure environment variables from .env are loaded before reading settings
load_dotenv()

# Environment: "local" (default) or "production"
APP_ENV = os.getenv("APP_ENV", "local")

if APP_ENV == "production":
    # In production, fail loudly if DATABASE_URL is not configured (e.g. Neon on Render)
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("APP_ENV=production but DATABASE_URL is not set")
else:
    # In local/dev, prefer a dedicated local URL and fall back to SQLite file
    DATABASE_URL = os.getenv("DATABASE_URL_LOCAL", "sqlite:///./ai_chat.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database - create all tables
    """
    # Ensure models are imported before creating tables
    # (otherwise Base.metadata may be empty at startup)
    from app.models import database  # noqa: F401
    Base.metadata.create_all(bind=engine)
