# API

The project includes a small FastAPI service for lightweight affordability and threshold calculations. Start it from the `full_project` directory after installing dependencies:

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Open `/docs` for the interactive API schema and `/health` for a health check. This API is exploratory, not an official statistical authority. Do not expose it publicly without rate limiting, access controls, request limits, monitoring and deployment hardening.