"""API endpoints for the VoteTrackerPlus backend"""

from backend import VtpBackend
from fastapi import FastAPI

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
@app.get("/vote/")
async def get_vote_store_id() -> dict:
    """Create and store a unique Vote Store ID for each client"""

    vote_store_id = VtpBackend.get_vote_store_id()
    vote_store_ids[vote_store_id] = "uncast"
    return {"VoteStoreID": vote_store_id}


# Endpoint #2
@app.get("/vote/{vote_store_id}")
async def get_empty_ballot(vote_store_id: str) -> dict:
    """Return an empty ballot for a given Vote Store ID"""

    if vote_store_id in vote_store_ids:
        empty_ballot = VtpBackend.get_empty_ballot(vote_store_id)
        return {"blank-ballot": empty_ballot}
    return {"error": "VoteStoreID not found"}


# Endpoint #3
@app.post("/vote/cast-ballot/{vote_store_id}")
async def cast_ballot(
    vote_store_id: str,
    incoming_json: dict = None,
) -> dict:
    """
    Uploads the ballot; the backend accepts it, merges it, and returns
    the ballot check and voter index
    """

    # import pdb; pdb.set_trace()
    if vote_store_id in vote_store_ids:
        if vote_store_ids[vote_store_id] == "uncast":
            ballot_check, vote_index = VtpBackend.cast_ballot(
                vote_store_id,
                incoming_json,
            )
            vote_store_ids[vote_store_id] = "cast"
            return {"ballot-check": ballot_check, "vote-index": vote_index}
        return {"error": "This ballot has already been cast"}
    return {"error": "VoteStoreID not found"}


# Endpoint #4
@app.post("/vote/verify-ballot-check/{vote_store_id}")
async def verify_ballot_check(
    vote_store_id: str,
    incoming_json: dict = None,
) -> dict:
    """
    Will verify the ballot-check and voter-id.  Return values are TBD
    pending further discussions
    """

    #    import pdb; pdb.set_trace()
    if vote_store_id in vote_store_ids:
        ballot_check_doc = VtpBackend.verify_ballot_check(
            vote_store_id,
            incoming_json,
        )
        return {"ballot-check-doc": ballot_check_doc}
    return {"error": "VoteStoreID not found"}


# Endpoint #5
@app.post("/vote/tally-election/{vote_store_id}")
async def tally_election(
    vote_store_id: str,
    incoming_json: dict = None,
) -> dict:
    """
    Will execute the tally, optionally limited to a list of contests,
    tracking an optional list of digests, with an optional verbosity
    level.
    """

    #    import pdb; pdb.set_trace()
    if vote_store_id in vote_store_ids:
        tally_election_doc = VtpBackend.tally_election_check(
            vote_store_id,
            incoming_json,
        )
        return {"tally-election-doc": tally_election_doc}
    return {"error": "VoteStoreID not found"}
