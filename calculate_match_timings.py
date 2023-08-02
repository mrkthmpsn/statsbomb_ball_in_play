"""
File to calculate the total time, in-play time, and out-of-play time for a match of StatsBomb data

For more details on the calculation reasoning, see `README.md`
"""
import numpy as np
import pandas as pd
from pydantic import BaseModel, computed_field

from utils.constants import MID_BREAK_EVENT_TYPE_LIST


class StatsbombMatchTimingsOutput(BaseModel):
    """
    Pydantic class to store ball-in-play information about a match. Contains computed fields to derive further
    information from the inputs.
    """

    match_id: int
    total_time_s: float
    in_play_time_s: float
    out_of_play_time_s: float

    @computed_field
    @property
    def pct_in_play(self) -> float:
        return round(self.in_play_time_s / self.total_time_s * 100, 2)

    @computed_field
    @property
    def total_time_min(self) -> float:
        return round(self.total_time_s / 60, 2)

    @computed_field
    @property
    def in_play_time_min(self) -> float:
        return round(self.in_play_time_s / 60, 2)


def calculate_statsbomb_match_timings(
    statsbomb_match_id: int,
    statsbomb_match_events_df: pd.DataFrame,
) -> StatsbombMatchTimingsOutput:
    """
    Function to calculate the match timings from a dataframe of Statsbomb match data.

    This Statsbomb events dataframe should have been obtained using the `sb.events([match_id])` function, with the
    `flatten_attrs` attribute set to `True` (as it is by default)

    :param statsbomb_match_id: a StatsBomb match ID, purely for purposes of storing directly in the
        `StatsbombMatchTimingsOutput`
    :param statsbomb_match_events_df: a dataframe of StatsBomb match events
    :return: `StatsbombMatchTimingsOutput` object, featuring ball-in-play metrics derived from this function and
        additional calculated metrics produced by the pydantic class
    """

    df = statsbomb_match_events_df[
        ~(statsbomb_match_events_df["type"].isin(MID_BREAK_EVENT_TYPE_LIST))
    ]

    df["restart_event"] = np.where(
        (df["type"] == "Referee Ball-Drop")
        | (
            (df["type"] == "Pass")
            & (
                df["pass_type"].isin(
                    ["Corner", "Free Kick", "Goal Kick", "Kick Off", "Throw-in"]
                )
            )
        )
        | (
            (df["type"] == "Shot")
            & (df["shot_type"].isin(["Corner", "Free Kick", "Penalty", "Kick Off"]))
        ),
        True,
        False,
    )

    df["total_seconds"] = df.apply(
        lambda row: (int(row["timestamp"].split(":")[1]) * 60)
        + float(row["timestamp"].split(":")[2]),
        axis=1,
    )
    df["previous_total_seconds"] = (
        df.sort_values(["period", "total_seconds"])
        .groupby("period")["total_seconds"]
        .shift(1)
    )
    df["restart_time"] = df.apply(
        lambda row: row["total_seconds"] - row["previous_total_seconds"]
        if row["restart_event"]
        else 0,
        axis=1,
    )

    match_time = (
        df[df["type"] == "Half End"]
        .groupby("period")["total_seconds"]
        .max()
        .reset_index()["total_seconds"]
        .sum()
    )
    out_of_play_time = df["restart_time"].sum()
    in_play_time = match_time - out_of_play_time

    return StatsbombMatchTimingsOutput(
        match_id=statsbomb_match_id,
        total_time_s=match_time,
        in_play_time_s=in_play_time,
        out_of_play_time_s=out_of_play_time,
    )
