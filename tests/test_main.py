"""Tests for API endpoints for the VoteTrackerPlus backend"""

import pytest
from fastapi.testclient import TestClient

from vtp.web.api.main import app

client = TestClient(app)


def test_get_root():
    """Test the root test node"""
    response = client.get("/web-api")
    assert response.status_code == 200
    assert "version" in response.json()


# Endpoint #3
@pytest.fixture
def cast_ballot(incoming_ballot_data):
    """Cast of a filled-in ballot"""
    # breakpoint()
    response = client.post(
        "/web-api/cast-ballot",
        json=incoming_ballot_data.json(),
    )
    return response


def test_cast_ballot(incoming_ballot_data):
    """Test cast_ballot"""
    assert incoming_ballot_data.status_code == 200
    assert "vote_store_id" in incoming_ballot_data.json()
    assert "ballot_check" in incoming_ballot_data.json()
    assert "vote_index" in incoming_ballot_data.json()
    assert "qr_svr" in incoming_ballot_data.json()


# Endpoint #4
def test_verify_ballot_receipt(vote_store_id, ballot_receipt):
    """testing the verification of a ballot receipt"""
    # import pdb; pdb.set_trace()
    response = client.post(
        f"/web-api/verify-ballot-receipt/{vote_store_id}",
        json=ballot_receipt.json(),
    )
    assert response.status_code == 200
    assert "ballot-receipt-stdout" in response.json()


# Endpoint #5
def test_tally_election(vote_store_id):
    """testing the tally"""
    # import pdb; pdb.set_trace()
    response = client.post(
        f"/web-api/tally-election/{vote_store_id}",
        json={
            "contest-uids": None,
            "track-contests": "123",
            "verbosity": 3,
        },
    )
    assert response.status_code == 200
    assert "tally-contest-stdout" in response.json()
