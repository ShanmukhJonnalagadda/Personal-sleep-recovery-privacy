"""Validation and feature engineering for synthetic WHOOP-style data.

This module deliberately contains no API credentials, authentication logic,
database identifiers, or personal health records.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "cycle_date",
    "recovery_score",
    "hrv_ms",
    "resting_hr_bpm",
    "sleep_performance_pct",
    "sleep_duration_min",
    "day_strain",
    "workout_strain",
}


def load_demo_data(path: str | Path) -> pd.DataFrame:
    """Load the synthetic dataset and return analysis-ready records."""
    frame = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    frame["cycle_date"] = pd.to_datetime(frame["cycle_date"], errors="coerce")
    frame = frame.dropna(subset=["cycle_date"]).copy()

    numeric_columns = REQUIRED_COLUMNS.difference({"cycle_date"})
    for column in numeric_columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    frame = (
        frame.drop_duplicates(subset=["cycle_date"], keep="last")
        .sort_values("cycle_date")
        .reset_index(drop=True)
    )

    frame["sleep_duration_hr"] = frame["sleep_duration_min"] / 60.0
    frame["next_cycle_recovery"] = frame["recovery_score"].shift(-1)
    frame["recovery_7d"] = frame["recovery_score"].rolling(7, min_periods=1).mean()
    frame["hrv_7d"] = frame["hrv_ms"].rolling(7, min_periods=1).mean()
    return frame


def filter_by_days(frame: pd.DataFrame, days: int | None) -> pd.DataFrame:
    """Return the most recent number of days, or the complete dataset."""
    if days is None or frame.empty:
        return frame.copy()
    cutoff = frame["cycle_date"].max() - pd.Timedelta(days=days - 1)
    return frame.loc[frame["cycle_date"] >= cutoff].copy()


def summary_metrics(frame: pd.DataFrame) -> dict[str, float]:
    """Calculate the primary dashboard summary values."""
    return {
        "Recovery": frame["recovery_score"].mean(),
        "HRV": frame["hrv_ms"].mean(),
        "Resting HR": frame["resting_hr_bpm"].mean(),
        "Sleep performance": frame["sleep_performance_pct"].mean(),
        "Day strain": frame["day_strain"].mean(),
    }

