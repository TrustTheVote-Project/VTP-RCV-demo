"""
Pydantic Models for the blank and cast ballots, the ballot check, and
the voter's index.  It is probably the case that there is not enough
time to create models for endpoints 4 and 5 as that data is currently
in more or less system log sytax.
"""

from typing import Dict, List, Union

from pydantic import BaseModel

# This is a data model file
# pylint: disable=too-few-public-methods


class Choice(BaseModel):
    """A choice made by a voter in a contest"""

    name: str
    party: str = None
    ticket_names: List[str] = None


class BaseUncastContest(BaseModel):
    """The common fields across all VTP contests when uncast"""

    choices: List[Choice]
    max: int = None
    tally: str
    uid: str
    win_by: float = None


class BaseCastContest(BaseModel):
    """The common fields across all VTP contests when cast"""

    choices: List[Choice]
    contest_type: str = None
    max: int = None
    selection: List[str]
    tally: str
    uid: str
    win_by: float = None


class ContestantUncastContest(BaseUncastContest):
    """
    A contestant contest is the most basic.  The description field is
    optional while being mostly ignored.
    """

    contest_type: str = None
    description: str = None


class ContestantCastContest(BaseCastContest):
    """
    A contestant contest is the most basic.  The description field is
    optional while being mostly ignored.
    """

    contest_type: str = None
    description: str = None


class QuestionUncastContest(BaseUncastContest):
    """
    A ballot question data object - requires a description (well not
    really, but why not?)
    """

    description: str


class QuestionCastContest(BaseCastContest):
    """
    A ballot question data object - requires a description (well not
    really, but why not?)
    """

    description: str


class TicketUncastContest(BaseUncastContest):
    """A ticket contest requires a contest_type value of 'ticket'"""

    contest_type: str = "ticket"
    ticket_offices: List[str]


class TicketCastContest(BaseCastContest):
    """A ticket contest requires a contest_type value of 'ticket'"""

    contest_type: str = "ticket"
    ticket_offices: List[str]


class AnyUncastContest(BaseModel):
    """
    Only here because I don't know what I am doing and the CastBallot
    class needs to be able to contain any number of any of the threee
    """

    __root__: List[
        Dict[
            str,
            Union[ContestantUncastContest, QuestionUncastContest, TicketUncastContest],
        ]
    ]


class AnyCastContest(BaseModel):
    """
    Only here because I don't know what I am doing and the CastBallot
    class needs to be able to contain any number of any of the threee
    """

    __root__: List[
        Dict[
            str,
            Union[ContestantCastContest, QuestionCastContest, TicketCastContest],
        ]
    ]


class BlankBallot(BaseModel):
    """A blank ballot - cannot contain a selection node in any contest"""

    active_ggos: List[str]
    ballot_filename: str
    ballot_node: str
    ballot_subdir: str
    contests: Dict[str, AnyUncastContest]


class CastBallot(BaseModel):
    """A cast ballot - must contain a selection node in each contest"""

    active_ggos: List[str]
    ballot_filename: str
    ballot_node: str
    ballot_subdir: str
    contests: Dict[str, AnyCastContest]
