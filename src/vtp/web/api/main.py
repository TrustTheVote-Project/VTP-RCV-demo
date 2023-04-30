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
@app.post("/vote")
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


# for testing - reuse a guid
@app.get("/reuse/{vote_store_id}")
async def reuse_guid(vote_store_id: str) -> dict:
    """Reuse a pre-existing guid workspace"""

    vote_store_ids[vote_store_id] = "uncast"
    return {"VoteStoreID": vote_store_id}

# for testing - show a mock cast ballot
@app.get("/show-mock-ballot")
async def show_mock_cast_ballot() -> dict:
    """Print a mock cast ballot"""

    a_cast_ballot = VtpBackend.mock_get_cast_ballot()
    return {"cast-ballot": a_cast_ballot}

@app.get("/restore-existing-guids")
async def restore_existing_guids() -> dict:
    """Will restore the existing vote_store_id's"""
    guids = VtpBackend.get_all_guid_workspaces()
    for guid in guids:
        vote_store_ids[guid] = "restored"
    return { "restored": guids }

# To manually test endpoint #3
# pylint: disable=line-too-long
#  curl -i -X POST -H 'Content-Type: application/json' -d '{"active_ggos":[".","GGOs/states/Massachusetts","GGOs/states/Massachusetts/GGOs/counties/Middlesex","GGOs/states/Massachusetts/GGOs/towns/Concord"],"ballot_filename":"000,001,002,003,ballot.json","ballot_node":"GGOs/states/Massachusetts/GGOs/towns/Concord","ballot_subdir":"GGOs/states/Massachusetts/GGOs/towns/Concord","contests":{"GGOs/states/Massachusetts":[{"US president":{"choices":[{"name":"Circle Party Ticket","ticket_names":["Rey Skywalker","Obi-Wan Kenobi"]},{"name":"Square Party Ticket","ticket_names":["Atticus Finch","Hermione  Granger"]},{"name":"Triangle Party Ticket","ticket_names":["Evelyn Quan Wang","Waymond Wang"]}],"contest_type":"ticket","selection":["2: Triangle Party Ticket","1: Square Party Ticket"],"tally":"rcv","ticket_offices":["President","Vice President"],"uid":"0000"}},{"US senate":{"choices":[{"name":"Anthony Alpha","party":"Circle Party"},{"name":"Betty Beta","party":"Pentagon Party"},{"name":"Gloria Gamma","party":"Square Party"},{"name":"David Delta","party":"Triangle Party"},{"name":"Emily Echo","party":"Ellipse Party"},{"name":"Francis Foxtrot","party":"Octagon Party"}],"selection":["5: Francis Foxtrot","3: David Delta","1: Betty Beta"],"tally":"rcv","uid":"0001"}},{"governor":{"choices":[{"name":"Spencer Cogswell","party":"Circle Party"},{"name":"Cosmo Spacely","party":"Triangle Party"}],"max":1,"selection":["1: Cosmo Spacely"],"tally":"plurality","uid":"0002"}}],"GGOs/states/Massachusetts/GGOs/counties/Middlesex":[{"County Clerk":{"choices":["Jean-Luc Picard","Katniss Everdeen","James T. Kirk"],"max":1,"selection":["0: Jean-Luc Picard"],"tally":"plurality","uid":"0003"}}],"GGOs/states/Massachusetts/GGOs/towns/Concord":[{"Question 1 - should the starting time of the annual town meeting be moved to 6:30PM?":{"choices":["yes","no"],"description":"Should the Town of Concord start the annual Town Meeting at 6:30PM instead of 7:00PM?\n","max":1,"selection":["0: yes"],"tally":"plurality","uid":"0004"}}]}}' http://127.0.0.1:8000/cast-ballot/01d963fd74100ee3f36428740a8efd8afd781839

# Endpoint #3
@app.post("/cast-ballot/{vote_store_id}")
async def cast_ballot(
    vote_store_id: str,
    incoming_json: dict,
) -> dict:
    """
    Uploads the ballot; the backend accepts it, merges it, and returns
    the ballot check and voter index
    """

    # import pdb; pdb.set_trace()
    if vote_store_id in vote_store_ids:
        if vote_store_ids[vote_store_id] != "cast":
            ballot_check, vote_index = VtpBackend.cast_ballot(
                vote_store_id,
                incoming_json,
            )
            vote_store_ids[vote_store_id] = "cast"
            return {"ballot-check": ballot_check, "vote-index": vote_index}
        return {"error": "This ballot has already been cast"}
    return {"error": "VoteStoreID not found"}


# Endpoint #4
@app.post("/verify-ballot-check/{vote_store_id}")
async def verify_ballot_check(
    vote_store_id: str,
    incoming_json: dict,
) -> dict:
    """
    Will verify the ballot-check and voter-id.  Return values are TBD
    pending further discussions
    """

    #    import pdb; pdb.set_trace()
    ballot_check = incoming_json["ballot-check"]
    vote_index = incoming_json["vote-index"]
    if vote_store_id in vote_store_ids:
        ballot_check_doc = VtpBackend.verify_ballot_check(
            vote_store_id,
            ballot_check,
            vote_index,
        )
        return {"ballot-check-doc": ballot_check_doc}
    return {"error": "VoteStoreID not found"}


# Endpoint #5
@app.get("/tally-election/{vote_store_id}/{contests}/{digests}")
async def tally_election(
    vote_store_id: str,
    contests: str,
    digests: str,
) -> dict:
    """
    Will execute the tally, optionally limited to a list of contests,
    tracking an optional list of digests, with an optional verbosity
    level.

    The contests and digests fields are optional but must be a comma
    separated string (no spaces).  If not specified they should be the
    string "None".
    """

    #    import pdb; pdb.set_trace()
    if vote_store_id in vote_store_ids:
        tally_election_doc = VtpBackend.tally_election_check(
            vote_store_id,
            contests,
            digests,
        )
        return {"tally-election-doc": tally_election_doc}
    return {"error": "VoteStoreID not found"}

# Endpoint #6
@app.get("/show-contest/{vote_store_id}/{contests}")
async def show_contest(
    vote_store_id: str,
    contests: str,
) -> dict:
    """
    Will display the CVR contents of one or more contests
    """

    #    import pdb; pdb.set_trace()
    if vote_store_id in vote_store_ids:
        return VtpBackend.show_contest(
            vote_store_id,
            contests,
        )
    return {"error": "VoteStoreID not found"}
