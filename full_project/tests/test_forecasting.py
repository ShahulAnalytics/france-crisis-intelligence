import pandas as pd
from france_crisis.forecasting import naive_forecast

def test_naive_forecast_repeats_latest_value():
    frame = pd.DataFrame({"date":pd.date_range("2024-01-01", periods=4, freq="MS"),"value":[1,2,3,4]})
    out = naive_forecast(frame, horizon=3)
    assert len(out) == 3
    assert out["value"].tolist() == [4.0,4.0,4.0]

def test_empty_forecast():
    assert naive_forecast(pd.DataFrame(), horizon=2).empty
