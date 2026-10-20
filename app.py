import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="France Crisis Intelligence",
    page_icon="🇫🇷",
    layout="wide"
)

st.title("🇫🇷 France Crisis Intelligence")
st.caption("Economic and social stress monitoring dashboard")

st.warning(
    "DEMO MODE: These charts use illustrative data, "
    "not current French statistics."
)

dates = pd.date_range("2023-01-01", periods=36, freq="MS")
rng = np.random.default_rng(42)

df = pd.DataFrame({
    "Month": dates,
    "Inflation (%)": 2 + np.sin(np.arange(36) / 4) + rng.normal(0, 0.2, 36),
    "Food price growth (%)": 3 + np.sin(np.arange(36) / 5) + rng.normal(0, 0.3, 36),
    "Unemployment (%)": 7.3 + np.sin(np.arange(36) / 6) * 0.2
})

c1, c2, c3 = st.columns(3)
c1.metric("Data status", "Demo only")
c2.metric("Official feeds", "Not connected")
c3.metric("Forecast status", "Illustrative")

metric = st.selectbox(
    "Choose an indicator",
    ["Inflation (%)", "Food price growth (%)", "Unemployment (%)"]
)

fig = px.line(df, x="Month", y=metric, markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Next steps")
st.write("1. Connect official French and European data sources.")
st.write("2. Validate indicators and their publication dates.")
st.write("3. Add tested forecasts and evidence-linked reports.")

st.info(
    "No conclusion about a French economic or food-supply crisis "
    "should be drawn from these demo charts."
)
