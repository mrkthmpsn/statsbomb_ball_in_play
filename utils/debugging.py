"""
File for debugging various things
"""
import numpy as np
import pandas as pd
from statsbombpy import sb

from utils.constants import MID_BREAK_EVENT_TYPE_LIST


def create_debug_dataframe(statsbomb_match_id: int) -> pd.DataFrame:
    """
    Function to create a simple dataframe from a Statsbomb match ID, along with flags for 'restart' events and time
    since previous event. This dataframe should be able to help check whether the ball in play calculations were
    correct and reasonable.

    :param statsbomb_match_id: A StatsBomb match ID
    :return: A dataframe containing the following fields, ordered by match period and total seconds:
        `type`,
        `pass_type`,
        `team`,
        `period`,
        `timestamp`,
        `restart_event`,
        `total_seconds`,
        `previous_total_seconds`,
        `restart_time`
    """

    statsbomb_events_df = sb.events(statsbomb_match_id)

    df = statsbomb_events_df[
        ~(statsbomb_events_df["type"].isin(MID_BREAK_EVENT_TYPE_LIST))
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

    debug_df = (
        df[
            [
                "type",
                "pass_type",
                "team",
                "period",
                "timestamp",
                "restart_event",
                "total_seconds",
                "previous_total_seconds",
                "restart_time",
            ]
        ]
        .sort_values(["period", "total_seconds"], ascending=True)
        .reset_index()
    )

    return debug_df
