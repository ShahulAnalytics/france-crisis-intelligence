.PHONY: install refresh news report warehouse dashboard api test lint
install:
	pip install -e .
refresh:
	python -m france_crisis.cli refresh --output data
news:
	python -m france_crisis.cli news --output data
report:
	python -m france_crisis.cli report --data data --output reports/france_crisis_report.md
warehouse:
	python -m france_crisis.cli warehouse --data data --db data/france_crisis.duckdb
dashboard:
	streamlit run src/france_crisis/dashboard.py
api:
	uvicorn api.main:app --reload --port 8000
test:
	pytest
lint:
	ruff check src tests api
