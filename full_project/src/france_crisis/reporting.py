"""Generate a transparent Markdown report from local datasets."""
from datetime import datetime, timezone
from pathlib import Path
import json
import pandas as pd

def generate_report(data_dir: Path, output_path: Path) -> Path:
    data_dir=Path(data_dir); output_path=Path(output_path); output_path.parent.mkdir(parents=True,exist_ok=True)
    lines=['# France Crisis Intelligence — Indicator Report','',f'Generated (UTC): {datetime.now(timezone.utc).isoformat()}','','## Scope and caveats','','This automated summary describes datasets available locally. Missing data are not evidence of no event. Statistical signals are not proof of a crisis. Validate definitions, source links, revisions and context before drawing conclusions.','','## Available processed datasets','']
    folder=data_dir/'processed'; files=sorted(folder.glob('*.csv')) if folder.exists() else []
    if not files: lines.append('No processed CSV datasets are available. Run the refresh command to attempt public-source retrieval.')
    for path in files:
        try:
            frame=pd.read_csv(path); lines += [f'### {path.stem}','',f'- Rows: {len(frame)}',f'- Columns: {", ".join(frame.columns.astype(str))}']
            if 'period' in frame and 'value' in frame:
                clean=frame.dropna(subset=['value'])
                if not clean.empty: lines += [f'- Latest period: {clean.iloc[-1]["period"]}',f'- Latest value: {clean.iloc[-1]["value"]}']
            if 'source_url' in frame and not frame['source_url'].dropna().empty: lines.append(f'- Source: {frame.source_url.dropna().iloc[-1]}')
            lines.append('')
        except Exception as exc: lines += [f'### {path.stem}','','Could not read dataset: '+str(exc),'']
    manifest=folder/'refresh_manifest.json'
    if manifest.exists():
        try: lines += ['## Refresh manifest','','```json',json.dumps(json.loads(manifest.read_text(encoding='utf-8')),indent=2),'```','']
        except Exception: pass
    lines += ['## Interpretation guardrails','','- Inflation measures price changes, not the absolute price level or household food insecurity.','- Exchange-rate quotations must state direction and unit.','- Forecasts are conditional scenarios, not certainties.','- Loss estimates must not be summed across overlapping categories.','']
    output_path.write_text('\n'.join(lines),encoding='utf-8'); return output_path
