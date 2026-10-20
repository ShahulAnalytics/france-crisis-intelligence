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

@st.cache_data(ttl=3600)
def load_inflation_data():
    url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_manr"
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
            (int(index), value)
            for index, value in values.items()
        )

    strides = [1] * len(sizes)
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


st.info(
    "Inflation is one indicator. It cannot by itself prove an economic "
    "or food-supply crisis."
)

try:
    df = load_inflation_data()
    latest = df.iloc[-1]

    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Latest annual inflation",
        f"{latest['Inflation (%)']:.1f}%"
    )
    col2.metric(
        "Reference month",
        latest["Month"].strftime("%B %Y")
    )
    col3.metric("Data status", "Eurostat connected")

    st.subheader("France: annual inflation rate")
    st.caption(
        "Source: Eurostat HICP annual rate of change, all items. "
        "The figures and dates come from the official dataset."
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
        "[Open the official Eurostat dataset]"
        "(https://ec.europa.eu/eurostat/databrowser/view/"
        "prc_hicp_manr/default/table?lang=en)"
    )

except Exception as error:
    st.error("Live Eurostat data could not be loaded.")
    st.caption(f"Technical detail: {type(error).__name__}: {error}")
    st.warning(
        "No synthetic values are displayed. Check the error before "
        "drawing conclusions from this dashboard."
    )

st.divider()
st.subheader("Next development steps")
st.write("1. Add official food-price and unemployment indicators.")
st.write("2. Validate dates, units, missing values, and source quality.")
st.write("3. Evaluate forecasts before using them in crisis reports.")

st.divider()
st.subheader("France food-price inflation")

@st.cache_data(ttl=3600)
def load_food_inflation():
    url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_minr"
    params = {
    "geo": "FR",
    "coicop18": "FOOD",
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
    categories = data["dimension"]["time"]["category"]["index"]

    if isinstance(categories, dict):
        periods = sorted(categories, key=categories.get)
    else:
        periods = list(categories)

    values = data.get("value", {})
    if isinstance(values, list):
        items = enumerate(values)
    else:
        items = ((int(i), v) for i, v in values.items())

    strides = [1] * len(sizes)
    for i in range(len(sizes) - 2, -1, -1):
        strides[i] = strides[i + 1] * sizes[i + 1]

    rows = []
    for index, value in items:
        if value is None:
            continue
        coords = [
            (index // strides[i]) % sizes[i]
            for i in range(len(sizes))
        ]
        period_index = coords[time_position]
        if period_index < len(periods):
            rows.append({
                "Month": pd.to_datetime(
                    periods[period_index], format="%Y-%m"
                ),
                "Food inflation (%)": float(value)
            })

    result = pd.DataFrame(rows)
    if result.empty:
        raise ValueError("No food inflation observations returned.")
    return result.sort_values("Month").drop_duplicates("Month")


try:
    food_df = load_food_inflation()
    latest_food = food_df.iloc[-1]

    c1, c2 = st.columns(2)
    c1.metric(
        "Latest annual food inflation",
        f"{latest_food['Food inflation (%)']:.1f}%"
    )
    c2.metric(
        "Food data reference month",
        latest_food["Month"].strftime("%B %Y")
    )

    food_fig = px.line(
        food_df,
        x="Month",
        y="Food inflation (%)",
        markers=True,
        title="France: annual food-price inflation"
    )
    st.plotly_chart(food_fig, use_container_width=True)
    st.caption(
        "Source: Eurostat HICP monthly rate dataset, France, food category. "
        "Food inflation measures price changes; it does not by itself "
        "measure food shortages or food insecurity."
    )
    st.markdown(
        "[View the official Eurostat dataset]"
        "(https://ec.europa.eu/eurostat/databrowser/view/"
        "prc_hicp_minr/default/table?lang=en)"
    )

except Exception as error:
    st.error("Food-price data could not be loaded from Eurostat.")
    st.caption(f"Technical detail: {type(error).__name__}: {error}")

