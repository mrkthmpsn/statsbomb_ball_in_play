"""
File to produce and save a list of match IDs from multiple competition-seasons for future use.
"""
from typing import List

import pandas as pd
from statsbombpy import sb

from utils.constants import SbMatchesFunctionInput

# You can use the below lines to check available competitions and match information
# statsbomb_competitions = sb.competitions()
# comp_matches = sb.matches(competition_id=1470, season_id=274)


def create_match_id_csv(
    match_finding_input_values: List[SbMatchesFunctionInput],
) -> None:
    """
    Takes a list of competition and season ID combinations (as codified by `SbMatchesFunctionInput`) and outputs a
    single-column csv of match IDs.

    You can create your own inputs for this by creating a list of `SbMatchesFunctionInput` objects, which ensure that
    you have a `competition_id` and `season_id`, which are arguments which StatsBomb's `sb.matches` function requires.

    :param match_finding_input_values: List of objects containing a competition and season ID, structure supported by
        `SbMatchesFunctionInput` pydantic class
    :return: Returns `None`, but saves a csv as part of the function.
    """

    match_ids_list = []

    for competition_season_item in match_finding_input_values:
        matches_df = sb.matches(
            competition_id=competition_season_item.competition_id,
            season_id=competition_season_item.season_id,
        )

        match_ids_list += list(matches_df["match_id"])

    match_ids_df = pd.DataFrame(match_ids_list, columns=["match_id"])

    match_ids_df.to_csv("./data/match_ids_list.csv", index=False)


# Example implementation
# from utils.constants import OLD_ICONS_SEASON_INFO
# create_match_id_csv(OLD_ICONS_SEASON_INFO)
