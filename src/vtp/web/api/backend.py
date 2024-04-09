"""
Backend support for the web-api.  One important aspect of this file is
to support web-api testing in the absense of a live ElectionData
deployment.  An ElectionData deployment is when a
setup-vtp-demo-operation operation has been run, nominally creating a
/opt/VoteTrackerPlus/demo.01 ElectionData folder and the required
subfolders.

With an ElectionData deployment the VTP git commands can be executed
and VoteTracker+ can function as designed.

Without an ElectionData deployment VTP git commands cannot be
executed.  Currently this state is configured by the _MOCK_MODE
variable below.  When set, and when this repo is part of the
VTP-dev-env parent repo (or when the VoteTrackerPlus and
VTP-mock-election.US.xx repos are simply sibling repos of this one),
the commands here do not call into the VoteTrackerPlus repo and
instead stub out the effective IO operations with static, non-varying
mock data.  That mock data is currently nominally stored in (checked
into) the VTP-mock-election.US.xx repo as the mock data is a direct
function of the live ElectionData election configuration and CVR data
found in that repo.  And that is due to two things: 1) the
VTP-mock-election.US.xx holds the configuration of an election such as
the blank ballot definition and 2) it also holds several hundred
pre-cast random ballots so to fill the ballot cache so that
ballot-checks can be immediately produced upon casting a ballot.

Regardless, for the time being the VTP-mock-election.US.xx also holds
checkedin mock values for the data that the web-api and above layers
need when running in mock mode.
"""

import json

from vtp.core.webapi import WebAPI
from vtp.ops.accept_ballot_operation import AcceptBallotOperation
from vtp.ops.cast_ballot_operation import CastBallotOperation
from vtp.ops.setup_vtp_demo_operation import SetupVtpDemoOperation
from vtp.ops.show_contests_operation import ShowContestsOperation
from vtp.ops.tally_contests_operation import TallyContestsOperation
from vtp.ops.verify_ballot_receipt_operation import VerifyBallotReceiptOperation


class VtpBackend:
    """
    Class to keep the namespace separate and allow the creation of a
    shim layer in the VTP-web-api repo so that this repo can easily
    talk with the VoteTrackerPlus backend repo.
    """

    ########
    # backend demo constants
    ########
    # set mock mode
    _MOCK_MODE = False
    # where the blank ballot is stored for the spring demo
    _MOCK_BLANK_BALLOT = "mock-data/blank-ballot.json"
    # where the cast-ballot.json file is stored for the spring demo
    _MOCK_CAST_BALLOT = "mock-data/cast-ballot.json"
    # where the ballot-check is stored for the spring demo
    _MOCK_BALLOT_CHECK = "mock-data/receipt.26.csv"
    _MOCK_VOTER_INDEX = 26
    # a mock contest content
    _MOCK_CONTEST_CONTENT = "mock-data/mock_contest.json"
    # default guid - making one up
    _MOCK_GUID = "01d963fd74100ee3f36428740a8efd8afd781839"
    # default mock receipt log
    _MOCK_VERIFY_BALLOT_LOG = "mock-data/verify-ballot-doc.json"
    # default mock tally log
    _MOCK_TALLY_CONTESTS_LOG = "mock-data/tally-election-doc.json"
    # default mock show contest log
    _MOCK_SHOW_CONTEST_LOG = "mock-data/show-contest-doc.json"
    # backend default address
    _ADDRESS = "123, Main Street, Concord, Massachusetts"

    @staticmethod
    def get_vote_store_id() -> str:
        """
        Endpoint #1: will return a vote_store_id, a.k.a. a guid
        """
        if VtpBackend._MOCK_MODE:
            # in mock mode there is no guid - make one up
            return VtpBackend._MOCK_GUID
        operation = SetupVtpDemoOperation(
            election_data_dir=WebAPI.get_generic_ro_edf_dir(),
        )
        return operation.run(guid_client_store=True)

    @staticmethod
    def get_blank_ballot(voter_address: str = "") -> dict:
        """
        Endpoint #2: will return a blank ballot.  If an address is
        supplied, will be address specific.  If not, will return the
        first blank ballot (alphanumerically sorted).
        """
        if VtpBackend._MOCK_MODE:
            # in mock mode there is no guid - make one up
            with open(VtpBackend._MOCK_BLANK_BALLOT, "r", encoding="utf8") as infile:
                json_doc = json.load(infile)
            #            import pdb; pdb.set_trace()
            return json_doc
        # Get a/the blank ballot from the backend
        operation = CastBallotOperation(
            election_data_dir=WebAPI.get_generic_ro_edf_dir(),
        )
        # If there is no address, for now use the mock default
        if voter_address == "":
            voter_address = VtpBackend._ADDRESS
        return operation.run(
            an_address=voter_address,
            return_blank_ballot=True,
        )

    @staticmethod
    def get_all_guid_workspaces() -> list:
        """
        Will return a list of all the existing guid workspaces
        """
        return SetupVtpDemoOperation.get_all_guid_workspaces()

    @staticmethod
    def mock_get_cast_ballot() -> dict:
        """Mock only - return a static cast ballot"""
        with open(VtpBackend._MOCK_CAST_BALLOT, "r", encoding="utf8") as infile:
            json_doc = json.load(infile)
        return json_doc

    @staticmethod
    def mock_get_ballot_check() -> tuple[list, int, str]:
        """Mock only - return a static cast ballot"""
        with open(VtpBackend._MOCK_BALLOT_CHECK, "r", encoding="utf8") as infile:
            json_doc = json.load(infile)
        return json_doc["ballot_check"], json_doc["ballot_row"], json_doc["qr_svg"]

    @staticmethod
    def cast_ballot(vote_store_id: str, cast_ballot: dict) -> dict:
        """
        Endpoint #3: will cast (upload) a cast ballot and return the
        ballot-check and voter-index
        """
        if VtpBackend._MOCK_MODE:
            # Just return a mock ballot-check and voter-index
            return VtpBackend.mock_get_ballot_check()
        # handle the incoming ballot and return the ballot-check and voter-index
        operation = AcceptBallotOperation(
            election_data_dir=WebAPI.get_guid_based_edf_dir(vote_store_id),
        )
        # Returns a 2D (ballot check) array, index, and qr_svg tuple
        return operation.run(
            cast_ballot_json=cast_ballot,
            merge_contests=True,
        )

    @staticmethod
    def verify_ballot_receipt(
        ballot_check: list,
        vote_index: int,
        cvr: bool = False,
    ) -> str:
        """
        Endpoint #4: will verify a ballot-check and vote-inded, returning an
        undefined string at this time.
        """
        if VtpBackend._MOCK_MODE:
            # Just return a mock verify ballot string
            with open(
                VtpBackend._MOCK_VERIFY_BALLOT_LOG, "r", encoding="utf8"
            ) as infile:
                json_doc = json.load(infile)
            return json_doc
        # handle the incoming ballot and return the ballot-check and voter-index
        operation = VerifyBallotReceiptOperation(
            election_data_dir=WebAPI.get_generic_ro_edf_dir(),
            stdout_printing=False,
        )
        return operation.run(
            receipt_data=ballot_check,
            row=str(vote_index),
            cvr=cvr,
        )

    @staticmethod
    def tally_election_check(
        contests: str,
        digests: str,
    ) -> str:
        """
        Endpoint #5: will tally an election and print stuff
        """
        if VtpBackend._MOCK_MODE:
            # Just return a mock tally string
            with open(
                VtpBackend._MOCK_TALLY_CONTESTS_LOG, "r", encoding="utf8"
            ) as infile:
                json_doc = json.load(infile)
            return json_doc
        # handle the incoming ballot and return the ballot-check and voter-index
        operation = TallyContestsOperation(
            election_data_dir=WebAPI.get_generic_ro_edf_dir(),
            stdout_printing=False,
        )
        if digests == "None":
            digests = ""
        if contests == "None":
            contests = ""
        return operation.run(
            contest_uid=contests,
            track_contests=digests,
        )

    @staticmethod
    def show_contest(
        contests: str,
    ) -> dict:
        """
        Endpoint #6: display the contents of one or more contests
        """
        if VtpBackend._MOCK_MODE:
            # Just return a mock contest
            with open(
                VtpBackend._MOCK_SHOW_CONTEST_LOG, "r", encoding="utf8"
            ) as infile:
                json_doc = json.load(infile)
            return json_doc
        # handle the show_contest
        operation = ShowContestsOperation(
            election_data_dir=WebAPI.get_generic_ro_edf_dir(),
            stdout_printing=False,
        )
        # Note that ShowContestsOperation.run will return a dictionary
        return operation.run(contest_check=contests)
