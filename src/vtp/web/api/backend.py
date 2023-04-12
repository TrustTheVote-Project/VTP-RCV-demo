"""
Backend support for the web-api.  One important aspect of this file is
to support web-api testing in the absense of a live ElectionData
deployment.  An ElectionData deployment is when a setup-mock-election
operation has been run, nominally creating a
/opt/VoteTrackerPlus/demo.01 ElectionData folder and the required
subfolders.

With an ElectionData deployment the VTP git commands can be executed
and VoteTracker+ can function as designed.

Without an ElectionData deployment VTP git commands cannot be
executed.  Currently this state is configured by the _MOCK_MODE
variable below.  When set, and when this repo is part of the
VTP-dev-env parent repo (or when the VoteTrackerPlus and
VTP-mock-election.US.xx repos are simply sibling repos of this one),
the commands here do call into the VoteTrackerPlus repo and instead
stub out the IO with static, non-varying mock data.  That mock data is
currently nominally stored in (checked into) the
VTP-mock-election.US.xx repo as it is a function of the live
ElectionData election configuration and CVR data found in that repo.
This is specifically due to two things: the VTP-mock-election.US.xx
holds the configuration of an election such as the blank ballot
definition as well as several hundred pre-cast random ballots so to
fill the ballot cache so that ballot-checks can be immediately
produced upon casting a ballot.
"""

import csv
import json
import os

from vtp.ops.accept_ballot_operation import AcceptBallotOperation
from vtp.ops.cast_ballot_operation import CastBallotOperation
from vtp.ops.setup_vtp_demo_operation import SetupVtpDemoOperation
from vtp.ops.tally_contests_operation import TallyContestsOperation
from vtp.ops.verify_ballot_receipt_operation import VerifyBallotReceiptOperation


class VtpBackend:
    """Class to keep the namespace separate"""

    ########
    # backend demo constants
    ########
    # set mock mode
    _MOCK_MODE = True
    # where the ElectionData repo is
    _DEFAULT_ELECTIONDATA = "VTP-mock-election.US.13"
    # where the blank ballot is stored for the spring demo
    # pylint: disable=line-too-long
    _MOCK_BLANK_BALLOT = "GGOs/states/Massachusetts/GGOs/towns/Concord/blank-ballots/json/000,001,002,003,ballot.json"
    # where the cast-ballot.json file is stored for the spring demo
    _MOCK_CAST_BALLOT = "receipts/cast-ballot.json"
    # where the ballot-check is stored for the spring demo
    _MOCK_BALLOT_CHECK = "receipts/receipts.26.csv"
    _MOCK_VOTER_INDEX = 26
    # default guid - making one up
    _MOCK_GUID = "01d963fd74100ee3f36428740a8efd8afd781839"
    # backend verbosity
    _VERBOSITY = 3

    # Class variables
    _election_data_dir = None
    _mock_blank_ballot = None
    _mock_cast_ballot = None
    _mock_ballot_check = None

    @staticmethod
    def set_election_data():
        """Will set _election_data_dir or raise an error"""
        # Just return if already set
        if VtpBackend._election_data_dir:
            return
        # Start wherever here is
        cur_dir = os.getcwd()
        while True:
            file_list = os.listdir(cur_dir)
            parent_dir = os.path.dirname(cur_dir)
            if VtpBackend._DEFAULT_ELECTIONDATA in file_list:
                # bingo
                VtpBackend._election_data_dir = os.path.join(
                    cur_dir,
                    VtpBackend._DEFAULT_ELECTIONDATA,
                )
                VtpBackend._mock_blank_ballot = os.path.join(
                    VtpBackend._election_data_dir,
                    VtpBackend._MOCK_BLANK_BALLOT,
                )
                VtpBackend._mock_cast_ballot = os.path.join(
                    VtpBackend._election_data_dir,
                    VtpBackend._MOCK_CAST_BALLOT,
                )
                VtpBackend._mock_ballot_check = os.path.join(
                    VtpBackend._election_data_dir,
                    VtpBackend._MOCK_BALLOT_CHECK,
                )
                break
            # if dir is root dir, raise error
            if cur_dir == parent_dir:
                raise OSError(
                    f"The ElecationData directory ({VtpBackend._DEFAULT_ELECTIONDATA}) "
                    "was not found prior to reaching the root (/) of the filesystem"
                )
            # continue walking up
            cur_dir = parent_dir

    @staticmethod
    def get_vote_store_id() -> str:
        """
        Endpoint #1: will return a vote_store_id, a.k.a. a guid
        """
        VtpBackend.set_election_data()
        if VtpBackend._MOCK_MODE:
            # in mock mode there is no guid - make one up
            return VtpBackend._MOCK_GUID
        operation = SetupVtpDemoOperation(
            election_data_dir=VtpBackend._election_data_dir,
            verbosity=VtpBackend._VERBOSITY,
        )
        return operation.run(guid_client_store=True)

    @staticmethod
    def get_empty_ballot(vote_store_id: str) -> dict:
        """
        Endpoint #2: given an existing guid, will return the blank
        ballot
        """
        VtpBackend.set_election_data()
        if VtpBackend._MOCK_MODE:
            # in mock mode there is no guid - make one up
            with open(VtpBackend._mock_blank_ballot, "r", encoding="utf8") as infile:
                json_doc = json.load(infile)
            #            import pdb; pdb.set_trace()
            return json_doc
        # Cet a (the) blank ballot from the backend
        operation = CastBallotOperation(
            guid=vote_store_id,
            verbosity=VtpBackend._VERBOSITY,
        )
        return operation.run(
            blank_ballot=VtpBackend._MOCK_BLANK_BALLOT,
            return_bb=True,
        )

    @staticmethod
    def mock_get_cast_ballot() -> dict:
        """Mock only - return a static cast ballot"""
        VtpBackend.set_election_data()
        with open(VtpBackend._mock_cast_ballot, "r", encoding="utf8") as infile:
            json_doc = json.load(infile)
            return json_doc


    @staticmethod
    def mock_get_ballot_check() -> tuple[list, int]:
        """Mock only - return a static cast ballot"""
        VtpBackend.set_election_data()
        with open(VtpBackend._mock_ballot_check, "r", encoding="utf8") as infile:
            csv_doc = list(csv.reader(infile))
        return csv_doc, VtpBackend._MOCK_VOTER_INDEX


    @staticmethod
    def cast_ballot(vote_store_id: str, cast_ballot: dict) -> dict:
        """
        Endpoint #3: will cast (upload) a cast ballot and return the
        ballot-check and voter-index
        """
        VtpBackend.set_election_data()
        if VtpBackend._MOCK_MODE:
            # Just return a mock ballot-check and voter-index
            return VtpBackend.mock_get_ballot_check()
        # handle the incoming ballot and return the ballot-check and voter-index
        operation = AcceptBallotOperation(
            guid=vote_store_id,
            verbosity=VtpBackend._VERBOSITY,
        )
        return operation.run(
            cast_ballot_json=cast_ballot,
            merge_contests=True,
        )


    @staticmethod
    def mock_get_verify_ballot_string() -> str:
        """Return a mock tally string"""
        return "Hello World"

    @staticmethod
    def verify_ballot_check(
        vote_store_id: str,
        incoming_json: dict,
    ) -> str:
        """
        Endpoint $4: will verify a ballot-check and vote-inded, returning an
        undefined string at this time.
        """
        VtpBackend.set_election_data()
        if VtpBackend._MOCK_MODE:
            # Just return a mock verify ballot string
            return VtpBackend.mock_get_verify_ballot_string()
        # handle the incoming ballot and return the ballot-check and voter-index
        operation = VerifyBallotReceiptOperation(
            guid=vote_store_id,
            verbosity=VtpBackend._VERBOSITY,
        )
        return operation.run(
            receipt_csv=incoming_json["ballot-check"],
            row=incoming_json["vote-index"],
            cvr=True,
        )


    @staticmethod
    def mock_get_tally_string() -> str:
        """Return a mock tally string"""
        return "Good Morning"


    @staticmethod
    def tally_election_check(
        vote_store_id: str,
        incoming_json: dict,
    ) -> str:
        """
        Endpoint #5: will verify a ballot-check and vote-inded,
        returning an undefined string at this time.
        """
        VtpBackend.set_election_data()
        if VtpBackend._MOCK_MODE:
            # Just return a mock tally string
            return VtpBackend.mock_get_tally_string()
        # handle the incoming ballot and return the ballot-check and voter-index
        verbosity = 3 if not "verbosity" in incoming_json else incoming_json["verbosity"]
        operation = TallyContestsOperation(
            guid=vote_store_id,
            verbosity=verbosity,
        )
        return operation.run(
            contest_uid=incoming_json["contest-uids"],
            track_contests=incoming_json["track-contests"],
        )
