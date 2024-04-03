"""API endpoints for the VoteTrackerPlus backend"""

from backend import VtpBackend
from fastapi import FastAPI

app = FastAPI()

########
# local variables
########
# A dict to store VoteStoreIDs
vote_store_ids = {}


@app.get("/web-api")
async def root() -> dict:
    """Demonstrate that API is working"""
    return {"version": "0.1.0"}


# Endpoint #2
#
# pylint: disable=line-too-long
# % curl -i -X GET -H 'Content-Type: application/json' http://127.0.0.1:8000/web-api/get_blank_ballot
@app.get("/web-api/get_blank_ballot")
async def get_blank_ballot(voter_address: str = "") -> dict:
    """Return an blank ballot for a given VoteStoreID"""

    blank_ballot = VtpBackend.get_blank_ballot(voter_address)
    return {"blank-ballot": blank_ballot}


# Testing Endpoint - reuse existin (backend) GUIDs
# pylint: disable=line-too-long
# % curl -i -X POST -H 'Content-Type: application/json' http://127.0.0.1:8000/web-api/restore-existing-guids
@app.post("/web-api/restore-existing-guids")
async def restore_existing_guids() -> dict:
    """Will restore the existing vote_store_id's"""
    guids = VtpBackend.get_all_guid_workspaces()
    for guid in guids:
        vote_store_ids[guid] = "restored"
    return {"restored": guids}


# Endpoint #3
#
# pylint: disable=line-too-long
# curl -i -X POST -H 'Content-Type: application/json' -d @docs/cast-ballot.json http://127.0.0.1:8000/web-api/cast-ballot
@app.post("/web-api/cast-ballot")
async def cast_ballot(
    incoming_ballot_data: dict,
) -> dict:
    """
    Uploads a castballot.  Will first create a guid workspace and use
    that to run the backend code.

    Returns the GUID, ballot_receipt, row_index, and qr_svg image
    """
    # breakpoint()

    # create a new VoteStoreID
    vote_store_id = VtpBackend.get_vote_store_id()
    vote_store_ids[vote_store_id] = "uncast"
    # leftover checks from previous implementation
    if vote_store_id not in vote_store_ids:
        return {"error": "VoteStoreID not found"}
    if vote_store_ids[vote_store_id] == "cast":
        return {"error": "This ballot has already been cast"}

    ballot_check, vote_index, qr_svg = VtpBackend.cast_ballot(
        vote_store_id,
        incoming_ballot_data,
    )
    vote_store_ids[vote_store_id] = "cast"
    return {
        "vote_store_id": vote_store_id,
        "ballot_check": ballot_check,
        "vote_index": vote_index,
        "qr_svg": qr_svg,
    }


# Endpoint #4
#
# pylint: disable=line-too-long
# curl -i -X GET -H 'Content-Type: application/json' -d @receipts/receipt.59.json http://127.0.0.1:8000/web-api/verify-ballot-check/d08a278a9a6b82040d505b9aae194efb72cceb0e
@app.get("/web-api/verify-ballot-check/{vote_store_id}")
async def verify_ballot_receipt(
    vote_store_id: str,
    incoming_receipt_data: dict,
) -> dict:
    """
    Will verify the ballot-receipt and return STDOUT (that is rendered
    by the client side javascript).
    """
    # breakpoint()
    ballot_check = incoming_receipt_data["ballot_check"]
    vote_index = incoming_receipt_data["row_index"]
    if vote_store_id not in vote_store_ids:
        return {"error": "VoteStoreID not found"}

    ballot_check_stdout = VtpBackend.verify_ballot_receipt(
        vote_store_id,
        ballot_check,
        vote_index,
    )
    return {"ballot-check-stdout": ballot_check_stdout}


# Endpoint #5


# To manually test #4 do something like:
# pylint: disable=line-too-long
# curl -i -X GET -H 'Content-Type: application/json' http://127.0.0.1:8000/web-api/tally-election/d08a278a9a6b82040d505b9aae194efb72cceb0e/0001/8bef5f87658c40bbe7dcda814422a59e844b204d
@app.get("/web-api/tally-contests/{vote_store_id}/{contests}/{digests}")
async def tally_contests(
    vote_store_id: str,
    contests: str,
    digests: str,
) -> dict:
    """
    Will execute the tally, optionally limited to a list of contests,
    tracking an optional list of digests.

    The contests and digests fields are optional but must be a comma
    separated string with no spaces.  If not specified they should be
    the string "None".  Contest_uid can also be the string "all".
    """

    #    breakpoint()
    if vote_store_id not in vote_store_ids:
        return {"error": "VoteStoreID not found"}

    tally_election_stdout = VtpBackend.tally_election_check(
        vote_store_id,
        contests,
        digests,
    )
    return {"tally-election-stdout": tally_election_stdout}


# Endpoint #6
@app.get("/web-api/contests/{vote_store_id}/{contest}")
async def show_contest(
    vote_store_id: str,
    contest: str,
) -> dict:
    """
    Will display the CVR contents, a.k.a. the git log of a specific
    commit digest.
    """
    #    breakpoint()
    if vote_store_id not in vote_store_ids:
        return {"error": "VoteStoreID not found"}

    git_log = VtpBackend.show_contest(
        vote_store_id,
        contest,
    )
    return {"git_log": git_log}
