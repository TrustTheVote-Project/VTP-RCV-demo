from fastapi.testclient import TestClient

from vtp.web.api.main import app

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_vote_store_id():
    response = client.get("/vote/")
    assert response.status_code == 200
    assert "VoteStoreID" in response.json()
