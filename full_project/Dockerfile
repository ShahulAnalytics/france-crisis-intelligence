FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml requirements.txt README.md ./
COPY src ./src
COPY api ./api
RUN pip install --no-cache-dir .
COPY config ./config
COPY docs ./docs
COPY reports ./reports
COPY data ./data
EXPOSE 8501 8000
CMD ["streamlit", "run", "src/france_crisis/dashboard.py", "--server.address=0.0.0.0", "--server.port=8501"]
