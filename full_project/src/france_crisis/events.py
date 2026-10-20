"""Event ledger validation and timeline helpers."""
import pandas as pd

def validate_event_records(frame: pd.DataFrame) -> list[str]:
 errors=[]
 for col in ('event_date','event','source_url'):
  if col not in frame.columns: errors.append('Missing required column: '+col)
 if 'source_url' in frame and frame['source_url'].fillna('').astype(str).str.strip().eq('').any(): errors.append('One or more events have no source URL')
 if 'event_date' in frame:
  invalid=pd.to_datetime(frame['event_date'],errors='coerce').isna() & frame['event_date'].notna()
  if invalid.any(): errors.append(f'{int(invalid.sum())} events have invalid dates')
 return errors

def event_timeline(frame: pd.DataFrame) -> pd.DataFrame:
 out=frame.copy()
 if 'event_date' in out: out['event_date']=pd.to_datetime(out['event_date'],errors='coerce'); out=out.sort_values('event_date',ascending=False,na_position='last')
 return out.reset_index(drop=True)
