# 🇫🇷 France Crisis Intelligence

An evidence-first data science project for monitoring France's economic and social indicators.

## Live dashboard

- **Streamlit app:** https://france-crisis-intelligence-k2frs8umaoyhbgvg2jheq.streamlit.app/
- **GitHub repository:** https://github.com/ShahulAnalytics/france-crisis-intelligence
- **Extended project workspace:** [full_project/](./full_project/)

## What it aims to investigate

- Inflation and food-price changes.
- Employment, income and purchasing power.
- Euro exchange rates and external price pressures.
- Historical trends, baseline forecasts and scenario analysis.
- Source-backed reporting and transparent limitations.

## Run the current dashboard locally

Install the root dashboard dependencies:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Evidence and limitations

The root dashboard currently uses illustrative demo data. It should not be interpreted as proof that France is experiencing a crisis. Live statistics, estimates, and forecasts must be clearly distinguished, with dates, source links, methodology, and uncertainty disclosed.

## Publication status

The existing root Streamlit app and its entry point (`app.py`) are preserved. An extended project workspace is being assembled under `full_project/`; it is **not yet validated as a complete, end-to-end deployable pipeline**. Use the live dashboard above for the currently deployed app, and do not treat placeholder/example datasets as current official statistics.

## Planned validation

1. Integrate and validate official INSEE, Eurostat and ECB data.
2. Preserve source URLs, retrieval dates, and raw-data provenance.
3. Evaluate forecasting baselines and quantify uncertainty.
4. Test report generation, API behavior, and data refresh.
5. Run automated tests before promoting the extended project to production.

## License

MIT
