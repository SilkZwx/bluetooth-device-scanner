from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)


def sample_test():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to my FastAPI service"}


def test_create_log():
    response = client.post(
        "/logs/", json={"user_id": "c19009", "mac_address": "00:1A:2B:3C:4D:5E"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Log created"}
