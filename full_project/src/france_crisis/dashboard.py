"""Streamlit dashboard for evidence-first France indicator analysis."""
from __future__ import annotations
import streamlit as st
import pandas as pd
import plotly.express as px
from france_crisis.analytics import clean_observations, summarize_series
from france_crisis.forecasting import naive_forecast
from france_crisis.food_security import affordability_pressure

st.set_page_config(page_title="France Crisis Intelligence", page_icon="🇫🇷", layout="wide")
st.title("🇫🇷 France Crisis Intelligence")
st.caption("Evidence-first monitoring of economic and social pressure. Indicators alone do not prove a national crisis.")
st.warning("Data quality notice: enter or load verified observations before interpreting this dashboard. Demonstration values are not live official statistics.")

with st.sidebar:
    st.header("Explore an indicator")
    metric = st.selectbox("Indicator", ["Annual inflation (%)", "Food inflation (%)", "Income growth (%)", "Unemployment (%)"])
    st.caption("Use the CSV uploader to analyse a source-verified dataset.")

uploaded = st.file_uploader("Upload observations CSV (columns: date,value; optional source_url)", type=["csv"])
if uploaded:
    try:
        frame = clean_observations(pd.read_csv(uploaded))
        if not {"date", "value"}.issubset(frame.columns):
            st.error("CSV must contain date and value columns.")
        elif frame.empty:
            st.warning("No valid observations were found.")
        else:
            stats = summarize_series(frame)
            a,b,c,d = st.columns(4)
            a.metric("Latest value", f"{stats['latest']:.2f}")
            b.metric("Observations", stats["count"])
            c.metric("Mean", f"{stats['mean']:.2f}")
            d.metric("Range", f"{stats['min']:.2f} – {stats['max']:.2f}")
            st.plotly_chart(px.line(frame, x="date", y="value", title=metric, markers=True), use_container_width=True)
            with st.expander("Forecast baseline (naive, not an official prediction)"):
                horizon = st.slider("Months/periods ahead", 1, 24, 6)
                forecast = naive_forecast(frame, horizon=horizon)
                st.dataframe(forecast, use_container_width=True)
                st.caption("This baseline repeats the latest value. It is for comparison only and should be evaluated against held-out observations.")
            if "source_url" in frame.columns:
                st.subheader("Source register from uploaded data")
                st.dataframe(frame[["date","value","source_url"]].tail(20), use_container_width=True)
    except Exception as exc:
        st.error(f"Could not read this CSV: {exc}")
else:
    st.info("Upload a CSV of verified observations to populate the analysis. Example: date,value,source_url.")
    st.code("date,value,source_url\n2024-01-01,3.1,https://example.org/source\n2024-02-01,2.9,https://example.org/source", language="csv")

st.subheader("Food affordability pressure")
col1, col2 = st.columns(2)
food = col1.number_input("Food inflation (%)", min_value=-100.0, max_value=1000.0, value=4.0, step=0.1)
income = col2.number_input("Income growth (%)", min_value=-100.0, max_value=1000.0, value=2.0, step=0.1)
result = affordability_pressure(food, income)
st.metric("Food inflation minus income growth", f"{result['affordability_gap_pp']:.1f} percentage points")
st.caption(result["interpretation"].capitalize() + ". " + result["limitation"])

st.subheader("Interpretation checklist")
st.markdown("- Verify the source, reference period, unit, and revision status.\n- Compare multiple indicators and credible reporting.\n- Separate observed facts, estimates, disputed claims, and future scenarios.\n- Do not infer shortages from price inflation alone.")
