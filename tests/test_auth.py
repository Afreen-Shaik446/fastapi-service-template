from fastapi.testclient import TestClient

from app.config import get_settings
from app.deps import create_access_token
from app.main import app

client = TestClient(app)


def _token() -> str:
    return create_access_token("pytest-user", get_settings())


def test_create_item_requires_token():
    response = client.post("/items", json={"name": "no-auth"})
    assert response.status_code == 401


def test_create_item_rejects_bad_token():
    response = client.post(
        "/items",
        json={"name": "bad"},
        headers={"Authorization": "Bearer not-a-real-token"},
    )
    assert response.status_code == 401


def test_create_and_list_items_with_token():
    create = client.post(
        "/items",
        json={"name": "widget", "description": "test item"},
        headers={"Authorization": f"Bearer {_token()}"},
    )
    assert create.status_code == 201
    body = create.json()
    assert body["name"] == "widget"
    assert body["created_by"] == "pytest-user"

    listed = client.get("/items")
    assert listed.status_code == 200
    assert any(item["id"] == body["id"] for item in listed.json())


def test_get_missing_item_returns_404():
    response = client.get("/items/999999")
    assert response.status_code == 404
