"""Food affordability indicators; price inflation is not a shortage measure."""
from __future__ import annotations
import pandas as pd

def affordability_pressure(food_inflation_pct: float, income_growth_pct: float) -> dict:
    """A simple descriptive gap, not a direct measure of food insecurity."""
    gap = float(food_inflation_pct) - float(income_growth_pct)
    return {"food_inflation_pct": float(food_inflation_pct),
            "income_growth_pct": float(income_growth_pct),
            "affordability_gap_pp": gap,
            "interpretation": "food prices rising faster than income" if gap > 0 else "income growth keeps pace with or exceeds food inflation",
            "limitation": "This gap alone cannot establish food shortages or household food insecurity."}

def summarize_food_prices(frame: pd.DataFrame, date_col: str = "date", value_col: str = "value") -> dict:
    if frame.empty:
        return {"latest": None, "latest_date": None, "change_pp": None}
    data = frame.copy()
    data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
    data[value_col] = pd.to_numeric(data[value_col], errors="coerce")
    data = data.dropna(subset=[date_col, value_col]).sort_values(date_col)
    if data.empty:
        return {"latest": None, "latest_date": None, "change_pp": None}
    return {"latest": float(data[value_col].iloc[-1]), "latest_date": data[date_col].iloc[-1].date().isoformat(),
            "change_pp": float(data[value_col].iloc[-1] - data[value_col].iloc[0])}
