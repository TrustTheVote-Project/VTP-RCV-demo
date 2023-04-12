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
@app.post("/vote/{vote_store_id}/cast-ballot")
async def cast_ballot(
        vote_store_id: str,
        incoming_cast_ballot: dict = None,
    ) -> dict:
    """
    Uploads the ballot; the backend accepts it, merges it, and returns
    the ballot check and voter index
    """

    if vote_store_id in vote_store_ids:
        if vote_store_ids[vote_store_id] == "uncast":
            ballot_check, voter_index = VtpBackend.cast_ballot(vote_store_id, incoming_cast_ballot)
            vote_store_ids[vote_store_id] = "cast"
            return {"ballot_check": ballot_check, "voter_index": voter_index}
        return {"error": "This ballot has already been cast"}
    return {"error": "VoteStoreID not found"}


# Endpoint #4
@app.post("/vote/{vote_store_id}/verify-ballot-check")
async def verify_ballot_check(
        vote_store_id: str,
        ballot_check: list = None,
        vote_index: int = 0,
    ) -> dict:
    """
    Will verify the ballot-check and voter-id.  Return values are TBD
    pending further discussions
    """

    if vote_store_id in vote_store_ids:
        if vote_store_ids[vote_store_id] == "cast":
            ballot_check_doc = VtpBackend.verify_ballot_check(
                vote_store_id,
                ballot_check,
                vote_index,
            )
            return {"ballot_check_doc": ballot_check_doc}
        return {"error": "The supplied rest endpoint (URL) is not a valid URL"}
    return {"error": "VoteStoreID not found"}


# Endpoint #5
