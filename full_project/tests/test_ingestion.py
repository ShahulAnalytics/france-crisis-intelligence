import pytest
from france_crisis.ingestion import eurostat_json_to_frame

def test_eurostat_json_stat_flattening():
 payload={'id':['geo','time'],'size':[1,2],'dimension':{'geo':{'category':{'index':{'FR':0}}},'time':{'category':{'index':{'2023':0,'2024':1}}}},'value':{'0':2.1,'1':1.8}}
 frame=eurostat_json_to_frame(payload,'demo')
 assert list(frame['time'])==['2023','2024']
 assert list(frame['value'])==[2.1,1.8]

def test_invalid_payload_rejected():
 with pytest.raises(ValueError): eurostat_json_to_frame({},'demo')
