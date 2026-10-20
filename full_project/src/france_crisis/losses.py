"""Loss-accounting guardrails to avoid invalid sums and double-counting."""
from __future__ import annotations
from typing import Any
import pandas as pd
REQUIRED={"estimate_id","category","value_eur","period_start","period_end","geography","status","source_url","method","overlap_group"}
VALID_STATUSES={"observed","reported","estimated","modelled","forecast","potential_exposure"}
def validate_loss_records(frame:pd.DataFrame)->list[str]:
 issues=[]; missing=REQUIRED.difference(frame.columns)
 if missing:return [f"missing_columns:{','.join(sorted(missing))}"]
 if frame["estimate_id"].duplicated().any():issues.append("duplicate_estimate_id")
 if (~frame["status"].isin(VALID_STATUSES)).any():issues.append("invalid_status")
 values=pd.to_numeric(frame["value_eur"],errors="coerce")
 if values.isna().any() or (values<0).any():issues.append("invalid_value_eur")
 if frame["source_url"].fillna("").str.strip().eq("").any():issues.append("missing_source_url")
 if frame["method"].fillna("").str.strip().eq("").any():issues.append("missing_method")
 if frame["overlap_group"].fillna("").astype(str).str.strip().eq("").any():issues.append("missing_overlap_group")
 return issues
def aggregate_non_overlapping_losses(frame:pd.DataFrame)->dict[str,Any]:
 issues=validate_loss_records(frame)
 if issues:raise ValueError("Loss records failed validation: "+", ".join(issues))
 sizes=frame["overlap_group"].astype(str).value_counts(); overlapping=frame[frame["overlap_group"].astype(str).map(lambda x:sizes.get(x,0)>1)].copy(); included=frame.drop(index=overlapping.index).copy()
 keys=[c for c in ["category","period_start","period_end","geography","status","gross_or_net"] if c in included.columns]; totals=[]
 if not included.empty:
  for values,subset in included.groupby(keys,dropna=False,sort=True):
   values=values if isinstance(values,tuple) else (values,); totals.append({**dict(zip(keys,values)),"sum_eur":float(pd.to_numeric(subset["value_eur"]).sum()),"count":int(len(subset)),"estimate_ids":subset["estimate_id"].astype(str).tolist()})
 return {"compatible_strata":totals,"single_stratum_sum_eur":totals[0]["sum_eur"] if len(totals)==1 else None,"included_count":int(len(included)),"excluded_overlap_count":int(len(overlapping)),"excluded_estimate_ids":overlapping["estimate_id"].astype(str).tolist(),"caveat":"Totals are only within compatible strata; analyst must still assess conceptual overlap."}
