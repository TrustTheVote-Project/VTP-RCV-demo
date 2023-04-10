"""
Pydantic Models for the blank and cast ballots, the ballot check.  It
is probably the case that there is not enough time to create models
for endpoints 4 and 5 as that data is currently in more or less system
log sytax.
"""

from typing import List, Dict
from pydantic import BaseModel

class Choice(BaseModel):
    name: str
    party: str = None
    ticket_names: List[str] = None

class BaseContest(BaseModel):
    choices: List[Choice]
    contest_type: str = None
    max: int = None
    selection: List[str]
    tally: str
    uid: str
    win_by: float = 0.5

class ContestentContest(BaseContest):

class QuestionContest(BaseModel):
    description: str

class TicketContest(BaseModel):
    contest_type: str = "ticket"
    ticket_offices: List[str]

class ContestDict(BaseModel):
    __root__: List[Dict[str, Union[ContestentContest, QuestionContest, TicketContest]]]

class CastBallot(BaseModel):
    active_ggos: List[str]
    ballot_filename: str
    ballot_node: str
    ballot_subdir: str
    contests: Dict[str, ContestDict]

