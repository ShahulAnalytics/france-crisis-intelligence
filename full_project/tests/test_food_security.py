from france_crisis.food_security import affordability_pressure

def test_food_inflation_exceeds_income_growth():
    result = affordability_pressure(5, 2)
    assert result["affordability_gap_pp"] == 3
    assert "shortages" in result["limitation"]
