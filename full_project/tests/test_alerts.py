import pandas as pd
from france_crisis.alerts import robust_change_alerts,evaluate_threshold

def test_threshold_alert_levels():
 assert evaluate_threshold('x',10,5,9)['level']=='critical'

def test_anomaly_alert_short_series():
 assert robust_change_alerts(pd.DataFrame({'period':['a','b'],'value':[1,2]}))['status']=='insufficient_data'
