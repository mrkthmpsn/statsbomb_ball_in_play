"""
File to put together a summary dataframe of saved match-by-match in-play time statistics produced in `create_analysis.py`

- average percent ball in play time
- average minutes ball in play time
- matches below 48 minutes (current League Two average - see: https://www.skysports.com/football/news/11095/12931160/rule-changes-for-new-football-season-officials-to-crackdown-on-dissent-be-more-lenient-on-physical-challenges-and-add-on-wasted-time)
- matches below 50% (a round psychic threshold of despair)
- matches above 60 minutes (a round hour)
"""
import os

import pandas as pd
from pydantic import BaseModel, computed_field


class ResultsSummary(BaseModel):
    """
    Pydantic class for storing a set of summarised results of a sample of data
    """

    sample_name: str
    total_matches: int
    qualifying_matches: int
    match_time_min: float
    ball_in_play_pct: float
    ball_in_play_min: float
    matches_below_48_min: int
    matches_below_50_pct: int
    matches_above_60_min: int

    @computed_field
    @property
    def pct_below_48_min(self) -> float:
        return round(self.matches_below_48_min / self.qualifying_matches * 100, 2)

    @computed_field
    @property
    def pct_below_50_pct(self) -> float:
        return round(self.matches_below_50_pct / self.qualifying_matches * 100, 2)

    @computed_field
    @property
    def pct_above_60_min(self) -> float:
        return round(self.matches_above_60_min / self.qualifying_matches * 100, 2)


results_list = []
for data_file in os.listdir("./data/results/"):
    file_path = "./data/results/" + data_file
    df = pd.read_csv(file_path)
    qualifying_df = df[df["total_time_min"] >= 90]

    results_summary = ResultsSummary(
        sample_name=data_file.split("_")[-1][:-4],
        total_matches=len(df),
        qualifying_matches=len(qualifying_df),
        match_time_min=qualifying_df["total_time_min"].mean(),
        ball_in_play_pct=qualifying_df["pct_in_play"].mean(),
        ball_in_play_min=qualifying_df["in_play_time_min"].mean(),
        matches_below_48_min=len(qualifying_df[qualifying_df["in_play_time_min"] < 48]),
        matches_below_50_pct=len(qualifying_df[qualifying_df["pct_in_play"] < 50]),
        matches_above_60_min=len(qualifying_df[qualifying_df["in_play_time_min"] > 60]),
    )

    results_list.append(results_summary)

summary_df = pd.DataFrame([model.model_dump() for model in results_list])
