import random

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.get("/vote/")
def get_vote_store_id() -> dict:
    vote_store_id = str(random.randrange(100000, 999999))
    return {"VoteStoreID": vote_store_id}
