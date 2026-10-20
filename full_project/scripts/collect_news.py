from __future__ import annotations
import json
from pathlib import Path
from france_crisis.news import collect_rss

if __name__ == "__main__":
    print(json.dumps(collect_rss(output_dir=Path("data")), indent=2))
