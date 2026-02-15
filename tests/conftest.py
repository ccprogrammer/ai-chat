"""
Pytest fixtures: shared test client, DB override, and auth helper.
Run all tests with: pytest (or pytest -v, pytest tests/ -v)
"""
import os

# Use a real file for tests so all connections share one DB (file in project root)
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_db.sqlite")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.core.database import SessionLocal, get_db
from app.main import app


def _clean_db():
    """Delete all data from tables so each test sees a clean DB."""
    db = SessionLocal()
    try:
        db.execute(text("DELETE FROM messages"))
        db.execute(text("DELETE FROM chats"))
        db.execute(text("DELETE FROM users"))
        db.commit()
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    """
    Test client using the app's in-memory DB. DB is cleared before each test.
    """
    _clean_db()
    with TestClient(app) as c:
        yield c
    _clean_db()


@pytest.fixture
def auth_headers(client):
    """
    Register a user, login, return headers with Bearer token.
    Use: def test_something(client, auth_headers): ... client.get("/chats", headers=auth_headers)
    """
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    r = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert r.status_code == 200
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
