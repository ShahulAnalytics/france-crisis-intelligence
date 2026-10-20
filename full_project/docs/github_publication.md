# GitHub publication and deployment

The full project is maintained in this directory while the repository-root Streamlit app remains preserved.

## Local setup

1. Use Python 3.11 or later.
2. Create and activate a virtual environment.
3. Run `pip install -e .`.
4. Run `pytest -q`.
5. Start the dashboard with `streamlit run src/france_crisis/dashboard.py`.
6. Start the API with `uvicorn api.main:app --reload`.

## Before production

- Verify the source registry and all dataset identifiers.
- Run tests and check API schemas.
- Review all research claims and dates.
- Never publish secrets, `.env` files, or private data.
- Configure deployment to use `full_project/src/france_crisis/dashboard.py` as the app entry point and `full_project/requirements.txt` as dependencies.
