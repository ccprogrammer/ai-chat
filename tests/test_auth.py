"""
API tests: auth (register, login).
"""
import pytest
from fastapi.testclient import TestClient


def test_register_ok(client: TestClient):
    r = client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "password123"},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == "user@example.com"
    assert "id" in data
    assert "created_at" in data


def test_register_duplicate_email(client: TestClient):
    client.post(
        "/auth/register",
        json={"email": "dup@example.com", "password": "password123"},
    )
    r = client.post(
        "/auth/register",
        json={"email": "dup@example.com", "password": "otherpassword"},
    )
    assert r.status_code == 409


def test_login_ok(client: TestClient):
    client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "secret456"},
    )
    r = client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "secret456"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient):
    client.post(
        "/auth/register",
        json={"email": "wrong@example.com", "password": "right"},
    )
    r = client.post(
        "/auth/login",
        json={"email": "wrong@example.com", "password": "wrong"},
    )
    assert r.status_code == 401


def test_login_unknown_email(client: TestClient):
    r = client.post(
        "/auth/login",
        json={"email": "nobody@example.com", "password": "any"},
    )
    assert r.status_code == 401
