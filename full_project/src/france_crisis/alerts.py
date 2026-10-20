"""Transparent threshold-based alerts."""
from __future__ import annotations

def evaluate_threshold(metric: str, value: float, warning: float, critical: float, higher_is_worse: bool = True) -> dict:
    if warning > critical:
        warning, critical = critical, warning
    v = float(value)
    if higher_is_worse:
        level = "critical" if v >= critical else "warning" if v >= warning else "normal"
    else:
        level = "critical" if v <= warning else "warning" if v <= critical else "normal"
    return {"metric": metric, "value": v, "level": level, "rule": "threshold-based",
            "note": "Alert thresholds are configurable signals, not proof of a crisis."}
