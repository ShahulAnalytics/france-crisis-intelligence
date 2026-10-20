import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(
page_title="France Crisis Intelligence",
page_icon="🇫🇷",
layout="wide"
)

st.title("🇫🇷 France Crisis Intelligence")
st.caption("Economic and social stress monitoring dashboard")

st.info(
"This dashboard uses official Eurostat inflation data when available. "
"Inflation alone cannot establish an economic or food-supply crisis."
)

@st.cache_data(ttl=3600)
def load_inflation_data():
url = (
"https://ec.europa.eu/eurostat/api/dissemination/"
"statistics/1.0/data/prc_hicp_manr"
)
params = {
"geo": "FR",
"coicop": "CP00",
"unit": "RCH_A",
"freq": "M",
"lang": "EN"
}

response = requests.get(url, params=params, timeout=25)
response.raise_for_status()
data = response.json()

dimensions = data["id"]
sizes = data["size"]
time_position = dimensions.index("time")
time_categories = data["dimension"]["time"]["category"]["index"]

if isinstance(time_categories, dict):
    time_codes = sorted(time_categories, key=time_categories.get)
else:
    time_codes = list(time_categories)

values = data.get("value", {})
if isinstance(values, list):
    value_items = enumerate(values)
else:
    value_items = (
        (int(index), value) for index, value in values.items()
    )

strides = []
for i in range(len(sizes)):
    strides.append(1)
for i in range(len(sizes) - 2, -1, -1):
    strides[i] = strides[i + 1] * sizes[i + 1]

rows = []
for flat_index, value in value_items:
    if value is None:
        continue

    coordinates = [
        (flat_index // strides[i]) % sizes[i]
        for i in range(len(sizes))
    ]
    time_index = coordinates[time_position]
    if time_index >= len(time_codes):
        continue

    period = time_codes[time_index]
    rows.append({
        "Month": pd.to_datetime(period, format="%Y-%m"),
        "Inflation (%)": float(value)
    })

result = pd.DataFrame(rows)
if result.empty:
    raise ValueError("Eurostat returned no usable inflation values.")

return result.sort_values("Month").drop_duplicates("Month")

try:
df = load_inflation_data()
latest = df.iloc[-1]

c1, c2, c3 = st.columns(3)
c1.metric("Latest annual inflation", f"{latest['Inflation (%)']:.1f}%")
c2.metric("Reference month", latest["Month"].strftime("%B %Y"))
c3.metric("Data status", "Eurostat connected")

st.subheader("France: annual inflation rate")
st.caption(
    "Source: Eurostat, HICP annual rate of change, all-items index. "
    "Values and reference periods are supplied by Eurostat."
)

fig = px.line(
    df,
    x="Month",
    y="Inflation (%)",
    markers=True,
    title="Monthly inflation rate"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Latest available observations")
st.dataframe(df.tail(12), use_container_width=True)

st.markdown(
    "[Open the Eurostat dataset](https://ec.europa.eu/eurostat/"
    "databrowser/view/prc_hicp_manr/default/table?lang=en)"
)

except Exception as error:
st.error(
"The live Eurostat data could not be loaded. "
"Check the connection and try again."
)
st.caption(f"Technical detail: {type(error).name}: {error}")
st.warning(
"No synthetic values are shown. The dashboard will not present "
"unverified numbers as official statistics."
)

st.divider()
st.subheader("Next development steps")
st.write("1. Add official food-price and unemployment indicators.")
st.write("2. Validate data dates, units, and missing observations.")
st.write("3. Add carefully evaluated forecasts and evidence-linked reports.")
