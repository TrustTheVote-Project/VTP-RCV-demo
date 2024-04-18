"""API endpoints for the VoteTrackerPlus backend"""

from backend import VtpBackend
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

# from starlette.responses import FileResponse

app = FastAPI()

########
# local variables
########
# A dict to store VoteStoreIDs
vote_store_ids = {}


# mount a static root for the static pages
app.mount("/static", StaticFiles(directory="static"), name="static")


# handle a root based index.html file
@app.get("/index.html")
async def read_index():
    """Redirect the default index.html page"""
    # return FileResponse("static/index.html")
    return RedirectResponse("static/index.html", status_code=status.HTTP_303_SEE_OTHER)


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
    return {"blank_ballot": blank_ballot}


# Testing Endpoint - reuse existin (backend) GUIDs
# pylint: disable=line-too-long
# % curl -i -X POST -H 'Content-Type: application/json' http://127.0.0.1:8000/web-api/restore-existing-guids
@app.post("/web-api/restore_existing_guids")
async def restore_existing_guids() -> dict:
    """Will restore the existing vote_store_id's"""
    guids = VtpBackend.get_all_guid_workspaces()
    for guid in guids:
        vote_store_ids[guid] = "restored"
    return {"restored": guids}


# Endpoint #3
#
# pylint: disable=line-too-long
# curl -i -X POST -H 'Content-Type: application/json' -d @docs/cast-ballot.json http://127.0.0.1:8000/web-api/cast_ballot
@app.post("/web-api/cast_ballot")
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
        return {"webapi_error": "VoteStoreID not found"}
    if vote_store_ids[vote_store_id] == "cast":
        return {"webapi_error": "This ballot has already been cast"}

    # Don't know why pylint is complaining about leftside=4 and
    # rightside=3 regarding the return tuple - it is 4 and 4
    # respectively.
    #
    # pylint: disable=unbalanced-tuple-unpacking
    ballot_check, vote_index, qr_svg, receipt_digest = VtpBackend.cast_ballot(
        vote_store_id,
        incoming_ballot_data,
    )
    vote_store_ids[vote_store_id] = "cast"
    return {
        "vote_store_id": vote_store_id,
        "ballot_check": ballot_check,
        "ballot_row": vote_index,
        "encoded_qr": qr_svg,
        "receipt_digest": receipt_digest,
    }


# Endpoint #4a
#
# pylint: disable=line-too-long
# curl -i -X GET -H 'Content-Type: application/json' -d @receipts/receipt.59.json http://127.0.0.1:8000/web-api/verify_ballot_receipt
@app.get("/web-api/verify_ballot_receipt/{vote_store_id}")
async def verify_ballot_receipt(
    vote_store_id: str,
    incoming_receipt_data: dict,
) -> dict:
    """
    Will verify the ballot-receipt and return STDOUT (that is rendered
    by the client side javascript).
    """
    if vote_store_id not in vote_store_ids:
        return {"webapi_error": "VoteStoreID not found"}
    # breakpoint()
    ballot_check_stdout = VtpBackend.verify_ballot_receipt(
        vote_store_id,
        incoming_receipt_data["ballot_check"],
        incoming_receipt_data["row_index"],
    )
    return {"verify_ballot_stdout": ballot_check_stdout}


# Endpoint #4b
#
# pylint: disable=line-too-long
# curl -i -X GET http://127.0.0.1:8000/web-api/verify_ballot_row/$UIDS/$DIGESTS
@app.get("/web-api/verify_ballot_row/{vote_store_id}/{uids}/{digests}")
async def verify_ballot_row(
    vote_store_id: str,
    uids: str,
    digests: str,
) -> dict:
    """
    Will verify the supllied list of digests.  Note - will not scale
    to large numbers of digests.
    """
    if vote_store_id not in vote_store_ids:
        return {"webapi_error": "VoteStoreID not found"}
    # breakpoint()
    return {
        "verify_ballot_stdout": VtpBackend.verify_ballot_row(
            vote_store_id,
            uids,
            digests,
        )
    }


# Endpoint #5
#
# To manually test #4 do something like:
# pylint: disable=line-too-long
# curl -i -X GET -H 'Content-Type: application/json' http://127.0.0.1:8000/web-api/tally_contests/d08a278a9a6b82040d505b9aae194efb72cceb0e/0001/8bef5f87658c40bbe7dcda814422a59e844b204d
@app.get("/web-api/tally_contests/{vote_store_id}/{contests}/{digests}/{verbosity}")
async def tally_contests(
    vote_store_id: str,
    contests: str,
    digests: str,
    verbosity: str,
) -> dict:
    """
    Will execute the tally, optionally limited to a list of contests,
    tracking an optional list of digests.

    The contests and digests fields are optional but must be a comma
    separated string with no spaces.  If not specified they should be
    the string "None".  Contest_uid can also be the string "all".

    Note that the backend returns STDOUT as an array of text lines.
    """
    if vote_store_id not in vote_store_ids:
        return {"webapi_error": "VoteStoreID not found"}
    tally_contests_stdout = VtpBackend.tally_contests(
        vote_store_id,
        contests,
        digests,
        verbosity,
    )
    return {"tally_election_stdout": tally_contests_stdout}


# Endpoint #6
@app.get("/web-api/show_contest/{vote_store_id}/{contest}")
async def show_contest(
    vote_store_id: str,
    contest: str,
) -> dict:
    """
    Will display the CVR contents, a.k.a. the git log of a specific
    commit digest.  The backend will convert the git log to json
    so that the client side can render that.
    """
    if vote_store_id not in vote_store_ids:
        return {"webapi_error": "VoteStoreID not found"}
    #    breakpoint()
    git_log = VtpBackend.show_contest(vote_store_id, contest)
    # import pdb; pdb.set_trace()
    return {"git_log": git_log}


# Endpoint #7
@app.get("/web-api/show_versioned_receipt/{vote_store_id}/{digest}")
async def show_versioned_receipt(
    vote_store_id: str,
    digest: str,
) -> dict:
    """
    Will return the contents of the versioned ballot receipt as an
    array of arrays (similar to cast_ballot above).
    """
    if vote_store_id not in vote_store_ids:
        return {"webapi_error": "VoteStoreID not found"}
    #    breakpoint()
    # import pdb; pdb.set_trace()
    return VtpBackend.show_versioned_receipt(vote_store_id, digest)
