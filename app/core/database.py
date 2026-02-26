"""
Database configuration and session management
"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from dotenv import load_dotenv

# Ensure environment variables from .env are loaded before reading DATABASE_URL
load_dotenv()

# Database URL – defaults to local SQLite if not overridden
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_chat.db")

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


def _migrate_token_version():
    """Add token_version column to users if it doesn't exist (for existing DBs)."""
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN token_version VARCHAR DEFAULT '0'"))
            conn.commit()
    except Exception:
        pass  # Column likely already exists


def init_db():
    """
    Initialize database - create all tables
    """
    # Ensure models are imported before creating tables
    # (otherwise Base.metadata may be empty at startup)
    from app.models import database  # noqa: F401
    Base.metadata.create_all(bind=engine)
    _migrate_token_version()
