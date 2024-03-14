"""API endpoints for the VoteTrackerPlus backend"""

from fastapi import FastAPI
from backend import VtpBackend

app = FastAPI()

########
# local variables
########
# A dict to store VoteStoreIDs
vote_store_ids = {}


@app.get("/")
async def root() -> dict:
    """Demonstrate that API is working"""
    return {"version": "0.1.0"}


# Endpoint #1
#
# % curl -i -X POST -H 'Content-Type: application/json' http://127.0.0.1:8000/vote
@app.post("/vote")
async def get_vote_store_id() -> dict:
    """Create and store a unique Vote Store ID for each client"""

    vote_store_id = VtpBackend.get_vote_store_id()
    vote_store_ids[vote_store_id] = "uncast"
    return {"VoteStoreID": vote_store_id}


# Endpoint #2
#
# % curl -i -X POST -H 'Content-Type: application/json' http://127.0.0.1:8000/restore-existing-guids
@app.get("/vote/{vote_store_id}")
async def get_empty_ballot(vote_store_id: str) -> dict:
    """Return an empty ballot for a given Vote Store ID"""

    if vote_store_id not in vote_store_ids:
        return {"error": "VoteStoreID not found"}

    empty_ballot = VtpBackend.get_empty_ballot(vote_store_id)
    return {"blank-ballot": empty_ballot}

# for testing - show a mock cast ballot
@app.get("/show-mock-ballot")
async def show_mock_cast_ballot() -> dict:
    """Print a mock cast ballot"""

    a_cast_ballot = VtpBackend.mock_get_cast_ballot()
    return {"cast-ballot": a_cast_ballot}

# for testing - reuse a guid
@app.post("/restore-existing-guids")
async def restore_existing_guids() -> dict:
    """Will restore the existing vote_store_id's"""
    guids = VtpBackend.get_all_guid_workspaces()
    for guid in guids:
        vote_store_ids[guid] = "restored"
    return { "restored": guids }

# Endpoint #3
#
# pylint: disable=line-too-long
# curl -i -X POST -H 'Content-Type: application/json' -d @docs/cast-ballot.json http://127.0.0.1:8000/cast-ballot/904ac6dc58021d7d9bf9e215bcd69c8e3a28b807

@app.post("/cast-ballot/{vote_store_id}")
async def cast_ballot(
    vote_store_id: str,
    incoming_ballot_data: dict,
) -> dict:
    """
    Uploads the ballot; the backend accepts it, merges it, and returns
    the ballot check and voter index
    """

    # breakpoint()
    if vote_store_id not in vote_store_ids:
        return {"error": "VoteStoreID not found"}
    if vote_store_ids[vote_store_id] == "cast":
        return {"error": "This ballot has already been cast"}

    ballot_check, vote_index, qr_svg = VtpBackend.cast_ballot(
        vote_store_id,
        incoming_ballot_data,
    )
    vote_store_ids[vote_store_id] = "cast"
    return {"ballot-check": ballot_check, "vote-index": row, "qr_svg": qr_svg}

# Endpoint #4
#
# pylint: disable=line-too-long
# curl -i -X POST -H 'Content-Type: application/json' -d @receipts/receipt.59.json http://127.0.0.1:8000/verify-ballot-check/d08a278a9a6b82040d505b9aae194efb72cceb0e

@app.post("/verify-ballot-check/{vote_store_id}")
async def verify_ballot_check(
    vote_store_id: str,
    incoming_ballot_data: dict,
) -> dict:
    """
    Will verify the ballot-check and voter-id.  Return values are TBD
    pending further discussions
    """

    #    breakpoint()
    ballot_check = incoming_ballot_data["ballot-check"]
    vote_index = incoming_ballot_data["vote-index"]
    if vote_store_id not in vote_store_ids:
        return {"error": "VoteStoreID not found"}

    ballot_check_doc = VtpBackend.verify_ballot_check(
        vote_store_id,
        ballot_check,
        vote_index,
    )
    return {"ballot-check-doc": ballot_check_doc}


# Endpoint #5

# To manually test #4 do something like:
# pylint: disable=line-too-long
# curl -i -X GET -H 'Content-Type: application/json' http://127.0.0.1:8000/tally-election/d08a278a9a6b82040d505b9aae194efb72cceb0e/0001/8bef5f87658c40bbe7dcda814422a59e844b204d

@app.get("/tally-election/{vote_store_id}/{contests}/{digests}")
async def tally_election(
    vote_store_id: str,
    contests: str,
    digests: str,
) -> dict:
    """
    Will execute the tally, optionally limited to a list of contests,
    tracking an optional list of digests.  At some later time with a
    better understanding of the client side UX a verbosity switch
    could be added.  Perhaps.

    The contests and digests fields are optional but must be a comma
    separated string (no spaces).  If not specified they should be the
    string "None".
    """

    #    breakpoint()
    if vote_store_id not in vote_store_ids:
        return {"error": "VoteStoreID not found"}

    tally_election_doc = VtpBackend.tally_election_check(
        vote_store_id,
        contests,
        digests,
    )
    return {"tally-election-doc": tally_election_doc}

# Endpoint #6
@app.get("/contests/{vote_store_id}/{contests}")
async def show_contest(
    vote_store_id: str,
    contests: str,
) -> dict:
    """
    Will display the CVR contents of one or more contests
    """

    #    breakpoint()
    if vote_store_id not in vote_store_ids:
        return {"error": "VoteStoreID not found"}

    return VtpBackend.show_contest(
            vote_store_id,
            contests,
    )
