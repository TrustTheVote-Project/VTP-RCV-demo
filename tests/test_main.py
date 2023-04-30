"""Tests for API endpoints for the VoteTrackerPlus backend"""

import pytest
from fastapi.testclient import TestClient

from vtp.web.api.main import app

client = TestClient(app)


def test_get_root():
    """test the root test node"""
    response = client.get("/")
    assert response.status_code == 200
    assert "version" in response.json()


# Endpoint #1
@pytest.fixture
def vote_store_id():
    """Test retreiving and printing a voter store id guid"""
    response = client.post("/vote")
    return response
def test_get_vote_store_id(vote_store_id)
    assert vote_store_id.status_code == 200
    assert "VoteStoreID" in vote_store_id.json()
    # retrieve VoteStoreID from response
    return vote_store_id.json()["VoteStoreID"]


# Endpoint #2
@pytest.fixture
def test_get_empty_ballot(test_get_vote_store_id):
    """Test with invalid VoteStoreID"""
    response = client.get("/vote/00000X")
    assert response.status_code == 200
    assert "error" in response.json()
    # test with valid VoteStoreID
    response = client.get(f"/vote/{test_get_vote_store_id}")
    assert response.status_code == 200
    assert "blank-ballot" in response.json()
    return response.json()["blank-ballot"]


# Endpoint #3
@pytest.fixture
def cast_ballot(vote_store_id, empty_ballot):
    """Cast of a filled-in ballot"""
    # breakpoint()
    response = client.post(
        f"/vote/cast-ballot/{vote_store_id}",
        json=empty_ballot.json(),
     )
     return response
def test_cast_ballot(vote_store_id, empty_ballot)
    assert empty_ballot.status_code == 200
    assert "ballot-check" in empty_ballot.json()
    assert "vote-index" in empty_ballot.json()


# Endpoint #4
def test_verify_ballot_check(vote_store_id, cast_ballot):
    """testing the verification of a ballot check"""
    # import pdb; pdb.set_trace()
    response = client.post(
        f"/vote/verify-ballot-check/{vote_store_id}",
        json=cast_ballot.json(),
    )
    assert response.status_code == 200
    assert "ballot-check-doc" in response.json()


# Endpoint #5
def test_tally_election(vote_store_id):
    """testing the tally"""
    # import pdb; pdb.set_trace()
    response = client.post(
        f"/vote/tally-election/{test_get_vote_store_id}",
        json={
            "contest-uids": None,
            "track-contests": "123",
            "verbosity": 3,
        },
    )
    assert response.status_code == 200
    assert "tally-election-doc" in response.json()
