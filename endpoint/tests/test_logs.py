from fastapi.testclient import TestClient
import pytest
from main import app
import os

client = TestClient(app)
id = os.environ.get("ID")
mac_address = os.environ.get("MAC_ADDRESS")


def sample_test():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to my FastAPI service"}


@pytest.mark.skip()
def test_create_log():
    response = client.post("/logs/", json={"user_id": id, "mac_address": mac_address})
    assert response.status_code == 200
    assert response.json() == {"message": "Log created"}


def test_get_all_ids():
    response = client.get("/logs/")
    assert response.status_code == 200
    resp = response.json()
    assert resp["ids"] is not None
    assert type(resp["ids"][0]) == str
    # print(resp)


def test_get_id_logs():
    response = client.get("/logs/" + id)
    assert response.status_code == 200
    resp = response.json()
    assert resp["id"] is not None
    assert resp["timestamps"] is not None
