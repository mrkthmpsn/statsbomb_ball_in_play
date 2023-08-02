"""
Utils or helpful constants for calculation
"""
from pydantic import BaseModel

MID_BREAK_EVENT_TYPE_LIST = [
    "Camera On*",
    "Substitution",
    "Bad Behaviour",
    "Starting XI",
    "Tactical Shift",
]

# Johan Cruyff article (features IDs): https://statsbomb.com/articles/soccer/statsbomb-icons-johan-cruyff/
# Diego Maradona article (features IDs): https://statsbomb.com/articles/soccer/statsbomb-icons-diego-maradona/
STATSBOMB_ICONS_MATCH_IDS = [
    3888711,
    3750235,
    3888706,
    3888716,
    3888717,
    3888718,
    3888719,
    3888720,
    3888713,
    3888754,
    3889115,
    3889082,
    3888787,
    3750191,
    3889148,
    3889149,
    3793185,
    3888721,
    3887188,
    3889182,
]

# The below are actually incorrect-ish: Not all of these matches appear to be part of the StatsBomb Icons series
# At original time of coding I also didn't realise that the articles featured the relevant match IDs, which are now
# added above

# ---

# Creating a pydantic model is a bit of overkill but it ensures that competition and season IDs are present
class SbMatchesFunctionInput(BaseModel):
    competition_id: int
    season_id: int


OLD_ICONS_SEASON_INFO = [
    SbMatchesFunctionInput(competition_id=16, season_id=277),
    SbMatchesFunctionInput(competition_id=16, season_id=71),
    SbMatchesFunctionInput(competition_id=16, season_id=276),
    SbMatchesFunctionInput(competition_id=87, season_id=84),
    SbMatchesFunctionInput(competition_id=87, season_id=268),
    SbMatchesFunctionInput(competition_id=87, season_id=279),
    SbMatchesFunctionInput(competition_id=1470, season_id=274),
    SbMatchesFunctionInput(competition_id=43, season_id=55),
    SbMatchesFunctionInput(competition_id=43, season_id=51),
    SbMatchesFunctionInput(competition_id=43, season_id=272),
    SbMatchesFunctionInput(competition_id=43, season_id=270),
    SbMatchesFunctionInput(competition_id=43, season_id=269),
    SbMatchesFunctionInput(competition_id=11, season_id=278),
    SbMatchesFunctionInput(competition_id=81, season_id=275),
    SbMatchesFunctionInput(competition_id=116, season_id=68),
    SbMatchesFunctionInput(competition_id=12, season_id=86),
    SbMatchesFunctionInput(competition_id=35, season_id=75),
]
