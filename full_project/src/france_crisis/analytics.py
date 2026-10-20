"""Analytics helpers for time-series economic indicators."""
from __future__ import annotations
import pandas as pd

def clean_observations(frame: pd.DataFrame, date_col: str = "date", value_col: str = "value") -> pd.DataFrame:
    """Normalize dates/values and remove invalid observations; preserve source metadata."""
    out = frame.copy()
    out[date_col] = pd.to_datetime(out[date_col], errors="coerce", utc=True)
    out[value_col] = pd.to_numeric(out[value_col], errors="coerce")
    out = out.dropna(subset=[date_col, value_col]).sort_values(date_col)
    return out.drop_duplicates(subset=[date_col], keep="last").reset_index(drop=True)

def percent_change(frame: pd.DataFrame, value_col: str = "value", periods: int = 12) -> pd.Series:
    """Calculate a percent change series, defaulting to year-over-year for monthly data."""
    return frame[value_col].pct_change(periods=periods) * 100

def summarize_series(frame: pd.DataFrame, value_col: str = "value") -> dict:
    if frame.empty or value_col not in frame:
        return {"count": 0, "latest": None, "mean": None, "min": None, "max": None}
    s = pd.to_numeric(frame[value_col], errors="coerce").dropna()
    return {"count": int(s.size), "latest": float(s.iloc[-1]) if len(s) else None,
            "mean": float(s.mean()) if len(s) else None,
            "min": float(s.min()) if len(s) else None,
            "max": float(s.max()) if len(s) else None}
