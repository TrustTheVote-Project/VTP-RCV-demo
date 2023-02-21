import random

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict:
    """Test that API is working"""
    return {"message": "Hello World"}


@app.get("/vote/")
async def get_vote_store_id() -> dict:
    """Get a unique Vote Store ID for each client"""
    vote_store_id = str(random.randrange(100000, 999999))
    return {"VoteStoreID": vote_store_id}

