"""Load and validate a lightweight source register."""
from __future__ import annotations
from pathlib import Path
import yaml

def load_sources(path: str | Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    sources = payload.get("sources", []) if isinstance(payload, dict) else payload
    if not isinstance(sources, list):
        raise ValueError("source registry must contain a list named 'sources'")
    return [s for s in sources if isinstance(s, dict) and s.get("name") and s.get("url")]
