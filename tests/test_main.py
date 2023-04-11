import pytest
from fastapi.testclient import TestClient

from vtp.web.api.main import app

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "version" in response.json()


@pytest.fixture
def test_get_vote_store_id():
    response = client.get("/vote/")
    assert response.status_code == 200
    assert "VoteStoreID" in response.json()
    # retrieve VoteStoreID from response
    return response.json()["VoteStoreID"]


def test_get_empty_ballot(test_get_vote_store_id):
    # test with invalid VoteStoreID
    response = client.get("/vote/00000X")
    assert response.status_code == 200
    assert "error" in response.json()
    # test with valid VoteStoreID
    response = client.get(f"/vote/{test_get_vote_store_id}")
    assert response.status_code == 200
    assert "ballot" in response.json()
