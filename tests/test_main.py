from fastapi.testclient import TestClient

from vtp.web.api.main import app

client = TestClient(app)
_vote_store_id = ""


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "version" in response.json()


def test_get_vote_store_id():
    response = client.get("/vote/")
    assert response.status_code == 200
    assert "VoteStoreID" in response.json()
    # retrieve VoteStoreID from response
    _vote_store_id = response.json()["VoteStoreID"]
