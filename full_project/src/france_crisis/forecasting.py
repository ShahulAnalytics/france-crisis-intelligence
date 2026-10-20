"""Baseline forecasting with explicit caveats; not a causal or official forecast."""
from __future__ import annotations
import pandas as pd

def naive_forecast(frame: pd.DataFrame, date_col: str = "date", value_col: str = "value", horizon: int = 6) -> pd.DataFrame:
    """Forecast using the latest observed value; returns a transparent baseline."""
    if horizon < 1:
        raise ValueError("horizon must be >= 1")
    data = frame.copy()
    data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
    data[value_col] = pd.to_numeric(data[value_col], errors="coerce")
    data = data.dropna(subset=[date_col, value_col]).sort_values(date_col)
    if data.empty:
        return pd.DataFrame(columns=[date_col, value_col, "forecast_type"])
    last_date, last_value = data[date_col].iloc[-1], float(data[value_col].iloc[-1])
    freq = pd.infer_freq(data[date_col]) if len(data) >= 3 else None
    if freq is None:
        freq = "MS"
    dates = pd.date_range(start=last_date, periods=horizon + 1, freq=freq)[1:]
    return pd.DataFrame({date_col: dates, value_col: [last_value] * horizon, "forecast_type": "naive baseline"})
