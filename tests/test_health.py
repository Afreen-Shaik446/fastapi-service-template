from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz_returns_ok():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readyz_returns_ready():
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_openapi_schema_is_served():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "/healthz" in schema["paths"]
    assert "/readyz" in schema["paths"]


def test_request_id_header_is_propagated():
    response = client.get("/healthz", headers={"X-Request-ID": "test-123"})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-123"
