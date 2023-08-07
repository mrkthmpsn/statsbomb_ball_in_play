"""
File to put together everything else that we've done
"""
from calculate_match_timings import calculate_statsbomb_match_timings
from statsbombpy import sb
import pandas as pd

from utils.constants import STATSBOMB_ICONS_MATCH_IDS
from utils.debugging import create_debug_dataframe


# StatsBomb Icons series
matches_list = STATSBOMB_ICONS_MATCH_IDS
# Invincibles season
# matches_df = sb.matches(competition_id=2, season_id=44)
# matches_list = matches_df['match_id']
# 2015/16 Premier League
# matches_df = sb.matches(competition_id=2, season_id=27)
# matches_list = matches_df['match_id']
# 2021/22 Indian Super League
# matches_df = sb.matches(competition_id=1238, season_id=108)
# matches_list = matches_df[matches_df['competition_stage'] == 'Regular Season']['match_id']
# 2020/21 WSL
# matches_df = sb.matches(competition_id=37, season_id=90)
# matches_list = matches_df['match_id']
# 2019 World Cup
# matches_df = sb.matches(competition_id=72, season_id=30)
# extra_time_matches = [68357, 69137, 69284]
# matches_list = matches_df[~(matches_df["match_id"].isin(extra_time_matches))][
#     "match_id"
# ]
# 2018 World Cup
# matches_df = sb.matches(competition_id=43, season_id=3)
# extra_time_matches = [7581, 7582, 7585, 8652, 8656]
# matches_list = matches_df[~(matches_df["match_id"].isin(extra_time_matches))][
#     "match_id"
# ]
# 2022 World Cup
# matches_df = sb.matches(competition_id=43, season_id=106)
# extra_time_matches = [3869219, 3869220, 3869321, 3869420, 3869685]
# matches_list = matches_df[~(matches_df["match_id"].isin(extra_time_matches))][
#     "match_id"
# ]
# 2011/12 Messi
# matches_df = sb.matches(competition_id=11, season_id=23)
# matches_list = matches_df["match_id"]
# 2015/16 La Liga
# matches_df = sb.matches(competition_id=11, season_id=27)
# matches_list = matches_df["match_id"]


output_list = []

for match_idx, match_id in enumerate(matches_list):
    print(f"Fetching events for match {match_idx+1} of {len(matches_list)}")
    match_events_df = sb.events(match_id=match_id)
    print(f"Calculating timings for match {match_idx+1} of {len(matches_list)}")
    match_output = calculate_statsbomb_match_timings(match_id, match_events_df)
    print(f"Appending output for match {match_idx+1} of {len(matches_list)}")
    output_list.append(match_output)

output_df = pd.DataFrame([model.model_dump() for model in output_list])
# To match the file format convention that `summary_analysis.py` makes use of, use the space after the final
# underscore to add a different label for each dataset
output_df.to_csv("./data/results/ball_in_play_time_statsbombicons.csv", index=False)

# Investigating a match where fewer than 90 minutes were played (according to the calculations)
too_little_time_df = create_debug_dataframe(3888713)
# In both halves, the HalfEnd events are earlier than 45 minutes on the timestamp - shrug.

# Investigating a match where there was 110 minutes of match time (according to the data)
too_much_time_df = create_debug_dataframe(3813264)
# There was a near-eleven-minute injury stoppage in the first half, that'll contribute.

# Huge amount of ball-in-play time in this match
too_much_in_play_time_df = create_debug_dataframe(8657)
# Couldn't reach conclusion as to why - seems it may just be an unusual match
