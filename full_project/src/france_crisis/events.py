"""Validation helpers for source-linked event timeline records."""
from __future__ import annotations
from urllib.parse import urlparse
import pandas as pd
REQUIRED_EVENT_FIELDS=("event_id","event_title","event_category","geography","start_date","source_url","verification_status")
VALID_EVENT_STATUSES={"verified_primary","corroborated_independent","plausible_unconfirmed","disputed","unsupported","preliminary"}
def validate_event_records(frame:pd.DataFrame)->list[str]:
 errors=[]; missing=[f for f in REQUIRED_EVENT_FIELDS if f not in frame.columns]
 if missing:return [f"Missing required columns: {', '.join(missing)}"]
 if frame["event_id"].astype(str).duplicated().any():errors.append("event_id must be unique")
 invalid=set(frame["verification_status"].dropna().astype(str))-VALID_EVENT_STATUSES
 if invalid:errors.append(f"Invalid verification_status values: {', '.join(sorted(invalid))}")
 bad=[]
 for idx,url in frame["source_url"].items():
  parsed=urlparse(str(url))
  if parsed.scheme not in {"https","http"} or not parsed.netloc:bad.append(str(idx))
 if bad:errors.append(f"Rows without valid http(s) source URLs: {', '.join(bad[:10])}")
 start=pd.to_datetime(frame["start_date"],errors="coerce")
 if start.isna().any():errors.append(f"Rows with invalid start_date: {', '.join(map(str,frame.index[start.isna()][:10]))}")
 if "end_date" in frame.columns:
  text=frame["end_date"].fillna("").astype(str).str.strip(); has=text.ne(""); end=pd.to_datetime(text.where(has),errors="coerce")
  if (has&end.isna()).any():errors.append("Rows with invalid end_date")
  if (has&end.notna()&start.notna()&(end<start)).any():errors.append("Rows where end_date precedes start_date")
 for field in ("direct_financial_cost_eur","indirect_cost_estimate_eur"):
  if field in frame.columns:
   vals=pd.to_numeric(frame[field],errors="coerce"); populated=frame[field].notna()&frame[field].astype(str).str.strip().ne("")
   if (populated&(vals.isna()|(vals<0))).any():errors.append(f"Invalid nonnegative numeric values in {field}")
 return errors
def event_timeline(frame:pd.DataFrame)->pd.DataFrame:
 if frame.empty or "start_date" not in frame.columns:return frame.copy()
 out=frame.copy(); out["start_date"]=pd.to_datetime(out["start_date"],errors="coerce"); return out.sort_values("start_date",ascending=False,na_position="last")
