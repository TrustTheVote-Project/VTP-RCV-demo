"""API endpoints for the VoteTrackerPlus backend"""
import json
import random

from fastapi import FastAPI

app = FastAPI()

# create a list to store VoteStoreIDs
vote_store_ids = []
# read empty ballot from JSON file
empty_ballot = json.load(open("alameda_ca.json"))


@app.get("/")
async def root() -> dict:
    """Demonstrate that API is working"""
    return {"version": "0.1.0"}


@app.get("/vote/")
async def get_vote_store_id() -> dict:
    """Create and store a unique Vote Store ID for each client"""
    vote_store_id = str(random.randrange(100000, 999999))
    # add VoteStoreID to list
    vote_store_ids.append(vote_store_id)
    return {"VoteStoreID": vote_store_id}


@app.get("/vote/{vote_store_id}")
async def get_empty_ballot(vote_store_id: str) -> dict:
    """Return an empty ballot for a given Vote Store ID"""
    if vote_store_id in vote_store_ids:
        return {"ballot": f"{empty_ballot}"}
    else:
        return {"error": "VoteStoreID not found"}
