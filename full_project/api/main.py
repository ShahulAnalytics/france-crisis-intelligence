"""Small API exposing project status and transparent analytical helpers."""
from fastapi import FastAPI
from pydantic import BaseModel, Field
from france_crisis.food_security import affordability_pressure
from france_crisis.alerts import evaluate_threshold

app = FastAPI(title="France Crisis Intelligence API", version="1.0.0", description="Evidence-first indicator analysis; not an official crisis declaration.")

class AffordabilityRequest(BaseModel):
    food_inflation_pct: float = Field(ge=-100, le=1000)
    income_growth_pct: float = Field(ge=-100, le=1000)

class AlertRequest(BaseModel):
    metric: str
    value: float
    warning: float
    critical: float
    higher_is_worse: bool = True

@app.get("/health")
def health():
    return {"status": "ok", "service": "france-crisis-intelligence", "data_verified": False,
            "message": "API is healthy; data freshness and source validity must be checked separately."}

@app.post("/analysis/food-affordability")
def food_affordability(request: AffordabilityRequest):
    return affordability_pressure(request.food_inflation_pct, request.income_growth_pct)

@app.post("/alerts/evaluate")
def alerts(request: AlertRequest):
    return evaluate_threshold(request.metric, request.value, request.warning, request.critical, request.higher_is_worse)
