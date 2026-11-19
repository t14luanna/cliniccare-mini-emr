import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def anonymous_client(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "test.db"))
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def client(anonymous_client):
    response = anonymous_client.post(
        "/auth/login", json={"username": "doctor", "password": "doctor123"}
    )
    token = response.json()["access_token"]
    anonymous_client.headers["Authorization"] = f"Bearer {token}"
    return anonymous_client
