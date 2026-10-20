import pandas as pd
from france_crisis.analytics import clean_observations, summarize_series

def test_clean_observations_removes_bad_rows_and_sorts():
    frame = pd.DataFrame({"date":["2024-02-01","bad","2024-01-01"],"value":[2,"x",1]})
    out = clean_observations(frame)
    assert len(out) == 2
    assert list(out["value"]) == [1,2]

def test_summary_empty():
    assert summarize_series(pd.DataFrame())["count"] == 0
