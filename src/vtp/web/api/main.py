"""API endpoints for the VoteTrackerPlus backend"""

# import json
import os

from fastapi import FastAPI
from vtp.ops.accept_ballot_operation import AcceptBallotOperation
from vtp.ops.cast_ballot_operation import CastBallotOperation
from vtp.ops.setup_vtp_demo_operation import SetupVtpDemoOperation

app = FastAPI()

########
# backend demo constants
########
# where the ElectionData repo is
DEFAULT_ELECTION_DATA_DIR = (
    "/opt/VoteTrackerPlus/demo.01/mock-clients/scanner.00/VTP-mock-election.US.13"
)
# pylint: disable=line-too-long
DEFAULT_BLANK_BALLOT = "GGOs/states/Massachusetts/GGOs/towns/Concord/blank-ballots/json/000,001,002,003,ballot.json"
# for testing only
DEFAULT_CAST_BALLOT = os.path.join(
    DEFAULT_ELECTION_DATA_DIR,
    "receipts",
    "cast-ballot.json",
)
# backend verbosity
VERBOSITY = 3

########
# local variables
########
# A dict to store VoteStoreIDs
vote_store_ids = []


@app.get("/")
async def root() -> dict:
    """Demonstrate that API is working"""
    return {"version": "0.1.0"}


# Endpoint #1
@app.get("/vote/")
async def get_vote_store_id() -> dict:
    """Create and store a unique Vote Store ID for each client"""

    svdo = SetupVtpDemoOperation(
        election_data_dir=DEFAULT_ELECTION_DATA_DIR,
        verbosity=VERBOSITY,
    )
    guid = svdo.run(
        guid_client_store=True,
    )

    vote_store_id = guid
    # add VoteStoreID to list
    vote_store_ids.append(vote_store_id)
    return {"VoteStoreID": vote_store_id}


# Endpoint #2
@app.get("/vote/{vote_store_id}")
async def get_empty_ballot(vote_store_id: str) -> dict:
    """Return an empty ballot for a given Vote Store ID"""

    if vote_store_id in vote_store_ids:
        # Cet a (the) blank ballot from the backend
        cbo = CastBallotOperation(
            guid=vote_store_id,
            verbosity=VERBOSITY,
        )
        empty_ballot = cbo.run(
            blank_ballot=DEFAULT_BLANK_BALLOT,
            return_bb=True,
        )
        return {"blank-ballot": empty_ballot}
    return {"error": "VoteStoreID not found"}


# Endpoint #3
@app.get("/vote/cast-ballot/{vote_store_id}")
async def cast_ballot(vote_store_id: str, cast_ballot_json: dict = None) -> dict:
    """
    Uploads the ballot; the backend accepts it, merges it, and returns
    the ballot check and voter index
    """

    if vote_store_id in vote_store_ids:
        # Accept the incoming cast ballot json and return a ballot check and voter index
        abo = AcceptBallotOperation(
            guid=vote_store_id,
            verbosity=VERBOSITY,
        )
        # ZZZ stub out cast ballot
        ballot_check, voter_index = abo.run(
            cast_ballot=DEFAULT_CAST_BALLOT,
            cast_ballot_json=cast_ballot_json,
            merge_contests=True,
        )
        return {"ballot_check": ballot_check, "voter_index": voter_index}
    return {"error": "VoteStoreID not found"}
