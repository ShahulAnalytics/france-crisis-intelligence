# France Crisis Intelligence — Extended Project

Evidence-first research and data-science tooling for monitoring selected French economic and social indicators. This project is a monitoring framework, not a claim that France is experiencing a crisis.

## Repository links

- Live dashboard: https://france-crisis-intelligence-k2frs8umaoyhbgvg2jheq.streamlit.app/
- Repository root dashboard: [../app.py](../app.py)
- Research methodology: [docs/research_methodology.md](docs/research_methodology.md)
- Source register: [docs/source_register.md](docs/source_register.md)
- Limitations: [docs/limitations.md](docs/limitations.md)

## Install and run

Requires Python 3.11 or newer.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest -q
```

Refresh public indicators (requires network access):

```bash
python -m france_crisis.cli refresh --output data
python -m france_crisis.cli news --output data
python -m france_crisis.cli alerts --data data --output reports/alerts.json
python -m france_crisis.cli report --data data --output reports/france_crisis_report.md --pdf reports/france_crisis_report.pdf
```

Optional DuckDB warehouse:

```bash
python -m france_crisis.cli warehouse --data data --db data/france_crisis.duckdb
```

Run the API from this directory:

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000
```

## Data and evidence rules

- Primary-source indicators should carry their source URL, retrieval time, period, units and series definition.
- News/RSS records are discovery leads, not fact-checks.
- Food inflation does not establish physical shortages or household food insecurity.
- ECB reference rates are not transaction quotes; state quotation direction.
- Anomaly scores are not proof of a crisis.
- Forecasts are baselines/scenarios, not certainties; evaluate with time-ordered backtests.
- Loss estimates need a counterfactual and overlap checks; do not sum incompatible estimates.
- Missing data are not zero and do not prove that no event occurred.

## Automated workflows

GitHub Actions includes tests on changes under `full_project/` and a weekday scheduled/manual public-data refresh. Inspect workflow logs and each feed's status before trusting generated outputs. Network APIs can change or fail, so the refresh job records per-feed errors instead of treating failed retrieval as a zero value.

## Current limitations

The root Streamlit dashboard currently uses illustrative demo data. The extended ingestion code retrieves a limited set of Eurostat HICP series and one ECB currency series; it does not yet cover every risk area in the project brief. The research ledgers are scaffolding and must not be presented as a comprehensive investigation. Human review is required before external publication.

## License

MIT — see [LICENSE](LICENSE).
