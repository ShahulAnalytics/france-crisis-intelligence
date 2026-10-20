"""Command-line interface for data refresh, news collection, warehouse and reports."""
from __future__ import annotations
import argparse, json, logging
from datetime import datetime, timezone
from pathlib import Path
from .ingestion import refresh_all
from .news import collect_rss
from .reporting import generate_report
from .warehouse import build_warehouse
from .alerts import robust_change_alerts
from .analytics import load_processed
from .pdf_reporting import markdown_to_pdf

def main() -> None:
    parser=argparse.ArgumentParser(prog="france-crisis"); sub=parser.add_subparsers(dest="command", required=True)
    refresh=sub.add_parser("refresh",help="Refresh official public data feeds"); refresh.add_argument("--output",type=Path,default=Path("data"))
    news=sub.add_parser("news",help="Collect metadata from configured public RSS feeds"); news.add_argument("--output",type=Path,default=Path("data"))
    report=sub.add_parser("report",help="Generate Markdown report from stored data"); report.add_argument("--data",type=Path,default=Path("data")); report.add_argument("--output",type=Path,default=Path("reports/france_crisis_report.md")); report.add_argument("--pdf",type=Path,default=None)
    warehouse=sub.add_parser("warehouse",help="Build optional DuckDB and Parquet outputs"); warehouse.add_argument("--data",type=Path,default=Path("data")); warehouse.add_argument("--db",type=Path,default=Path("data/france_crisis.duckdb"))
    alerts=sub.add_parser("alerts",help="Evaluate historical-anomaly checks"); alerts.add_argument("--data",type=Path,default=Path("data")); alerts.add_argument("--output",type=Path,default=Path("reports/alerts.json"))
    args=parser.parse_args(); logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s")
    if args.command=="refresh": print(json.dumps(refresh_all(args.output),indent=2))
    elif args.command=="news": print(json.dumps(collect_rss(output_dir=args.output),indent=2))
    elif args.command=="report":
        path=generate_report(args.data,args.output); print(path)
        if args.pdf: print(markdown_to_pdf(path,args.pdf))
    elif args.command=="warehouse": print(json.dumps(build_warehouse(args.data,args.db),indent=2))
    elif args.command=="alerts":
        results=[]
        for dataset_id,frame in load_processed(args.data).items():
            if {"period","value"}.issubset(frame.columns):
                result=robust_change_alerts(frame); result["dataset_id"]=dataset_id; results.append(result)
        payload={"run_at_utc":datetime.now(timezone.utc).isoformat(),"thresholds":{"watch":">=2","elevated":">=3","severe":">=4"},"results":results,"caveat":"Statistical anomalies require verification and are not proof of a crisis."}
        args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(payload,indent=2),encoding="utf-8"); print(json.dumps(payload,indent=2))

if __name__=="__main__": main()
