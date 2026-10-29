
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# Locate the project and geographical dataset
ROOT = Path(__file__).resolve().parents[1]

GEO_FILE = (
    ROOT / "data" / "processed"
    / "geographical_sales.csv"
)

st.title("🌍 Geographical Sales Analytics")

st.caption(
    "Historical positive merchandise transaction "
    "values by country, before returns and cancellations."
)

if not GEO_FILE.exists():
    st.error("Geographical sales dataset not found.")
    st.stop()


# Load and validate geographical data
@st.cache_data
def load_geo_data():
    df = pd.read_csv(GEO_FILE)

    required = [
        "Country",
        "GrossMerchandiseValue",
        "TransactionLines",
        "InvoiceCount",
        "SalesSharePercent"
    ]

    missing = [
        col for col in required if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    return df


geo = load_geo_data()

# Calculate geographical KPIs
total_sales = geo["GrossMerchandiseValue"].sum()

uk_sales = geo.loc[
    geo["Country"] == "United Kingdom",
    "GrossMerchandiseValue"
].sum()

international_sales = total_sales - uk_sales

uk_share = (
    uk_sales / total_sales * 100
    if total_sales > 0 else 0
)

# Display KPIs
st.subheader("Geographical Sales Overview")

c1, c2, c3 = st.columns(3)

c1.metric(
    "UK Merchandise Sales",
    f"£{uk_sales / 1_000_000:.2f}M"
)

c2.metric(
    "International Sales",
    f"£{international_sales / 1_000_000:.2f}M"
)

c3.metric(
    "UK Sales Share",
    f"{uk_share:.2f}%"
)

# Interactive chart controls
st.subheader("Explore International Markets")

include_uk = st.checkbox(
    "Include United Kingdom in ranking",
    value=False
)

max_countries = len(geo)

top_n = st.slider(
    "Number of countries to display",
    min_value=1,
    max_value=max_countries,
    value=min(10, max_countries)
)

filtered_geo = geo.copy()

if not include_uk:
    filtered_geo = filtered_geo.loc[
        filtered_geo["Country"] != "United Kingdom"
    ]

top_countries = (
    filtered_geo
    .nlargest(top_n, "GrossMerchandiseValue")
    .sort_values("GrossMerchandiseValue")
)

# Plot geographical performance
fig = px.bar(
    top_countries,
    x="GrossMerchandiseValue",
    y="Country",
    orientation="h",
    color="GrossMerchandiseValue",
    color_continuous_scale="Blues",
    title="Leading Markets by Merchandise Sales",
    hover_data=[
        "InvoiceCount",
        "TransactionLines",
        "SalesSharePercent"
    ]
)

fig.update_layout(
    height=max(500, len(top_countries) * 35),
    xaxis_title="Positive Merchandise Sales (£)",
    yaxis_title="Country",
    xaxis_tickprefix="£",
    coloraxis_showscale=False
)

st.plotly_chart(fig)

# Detailed data
with st.expander("View Geographical Sales Data"):
    st.dataframe(
        geo.sort_values(
            "GrossMerchandiseValue",
            ascending=False
        ),
        hide_index=True
    )

# Download data
st.download_button(
    label="Download Geographical Sales Data",
    data=geo.to_csv(index=False).encode("utf-8"),
    file_name="geographical_sales.csv",
    mime="text/csv"
)

st.caption(
    "Sales shares are based on positive merchandise "
    "transactions only. Figures do not represent "
    "profit or net revenue after returns."
)