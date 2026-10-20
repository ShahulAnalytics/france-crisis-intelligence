# France Crisis Intelligence — Full Project

An evidence-first Python project for tracking France's economic and social indicators. It combines official-statistics ingestion, source registers, news collection, claims/event ledgers, food-security indicators, loss estimates, forecasting, alerts, an API, a Streamlit dashboard, and research reports.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
streamlit run src/france_crisis/dashboard.py
```

API:
```bash
uvicorn api.main:app --reload
```

## Evidence standards

- Distinguish verified statistics, reported claims, estimates, and scenarios.
- Preserve source URLs, publication/reference dates, and collection timestamps.
- Never interpret inflation alone as proof of food shortages.
- Forecasts are exploratory, carry uncertainty, and are not presented as facts.
- Data refreshes can fail when external sources change or are unavailable.

## Project map

- `src/france_crisis/`: ingestion, analytics, forecasting, news, alerts, reporting
- `api/`: FastAPI service
- `config/`: source registry, news feeds, alert rules
- `data/research/`: claim/event ledgers and research tables
- `reports/`: executive summary and report
- `tests/`: unit and integration tests
- `.github/workflows/`: tests and scheduled refresh workflow

This full implementation is published alongside the existing root Streamlit dashboard; the existing `app.py` is intentionally preserved.