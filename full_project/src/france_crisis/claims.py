"""Claim ledger helpers to separate evidence strength from narrative."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Claim:
    claim_id: str
    claim: str
    status: str = "unverified"
    source_url: Optional[str] = None
    source_date: Optional[str] = None
    notes: str = ""
    def to_dict(self) -> dict:
        return asdict(self)

def validate_claim_status(status: str) -> str:
    allowed = {"verified", "partially_verified", "disputed", "unverified", "scenario"}
    if status not in allowed:
        raise ValueError(f"status must be one of {sorted(allowed)}")
    return status
