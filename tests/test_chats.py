"""
API tests: chats (create, list, get, delete) – require auth.
"""
import pytest
from fastapi.testclient import TestClient


def test_create_chat_without_auth_returns_401(client: TestClient):
    r = client.post("/chats", json={"title": "My chat"})
    assert r.status_code == 401


def test_create_chat_with_auth(client: TestClient, auth_headers: dict):
    r = client.post("/chats", json={"title": "First"}, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "First"
    assert "id" in data
    assert data["message_count"] == 0


def test_list_chats_empty(client: TestClient, auth_headers: dict):
    r = client.get("/chats", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["chats"] == []
    assert r.json()["total"] == 0


def test_list_chats_after_create(client: TestClient, auth_headers: dict):
    client.post("/chats", json={"title": "A"}, headers=auth_headers)
    client.post("/chats", json={"title": "B"}, headers=auth_headers)
    r = client.get("/chats", headers=auth_headers)
    assert r.status_code == 200
    chats = r.json()["chats"]
    assert len(chats) == 2
    titles = {c["title"] for c in chats}
    assert titles == {"A", "B"}


def test_get_chat(client: TestClient, auth_headers: dict):
    create = client.post("/chats", json={"title": "Get me"}, headers=auth_headers)
    assert create.status_code == 201
    chat_id = create.json()["id"]
    r = client.get(f"/chats/{chat_id}", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["title"] == "Get me"
    assert r.json()["id"] == chat_id


def test_get_chat_404(client: TestClient, auth_headers: dict):
    r = client.get("/chats/00000000-0000-0000-0000-000000000000", headers=auth_headers)
    assert r.status_code == 404


def test_delete_chat(client: TestClient, auth_headers: dict):
    create = client.post("/chats", json={"title": "To delete"}, headers=auth_headers)
    chat_id = create.json()["id"]
    r = client.delete(f"/chats/{chat_id}", headers=auth_headers)
    assert r.status_code == 204
    get_r = client.get(f"/chats/{chat_id}", headers=auth_headers)
    assert get_r.status_code == 404
