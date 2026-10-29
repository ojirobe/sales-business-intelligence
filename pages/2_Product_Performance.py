
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]

PRODUCT_FILE = (
    ROOT / "data" / "processed"
    / "net_product_performance.csv"
)

st.title("🛍️ Product Performance Analytics")

st.caption(
    "Historical product sales and returns, "
    "using signed transaction values."
)

@st.cache_data
def load_products():
    return pd.read_csv(
        PRODUCT_FILE,
        dtype={"StockCode": "string"}
    )


if not PRODUCT_FILE.exists():
    st.error("Product performance dataset not found.")
    st.stop()

products = load_products()

# Product ranking controls
col1, col2 = st.columns(2)

with col1:
    top_n = st.slider(
        "Number of products",
        min_value=5,
        max_value=30,
        value=10,
        step=5
    )

with col2:
    metric = st.selectbox(
        "Rank products by",
        ["NetSales", "GrossSales", "NetUnits"]
    )

# Calculate rankings
top_products = (
    products.nlargest(top_n, metric)
    .sort_values(metric)
)

# Display interactive chart
fig = px.bar(
    top_products,
    x=metric,
    y="ProductName",
    orientation="h",
    hover_data=[
        "StockCode",
        "GrossSales",
        "Returns",
        "NetSales",
        "NetUnits"
    ],
    title=f"Top {top_n} Products by {metric}"
)

fig.update_layout(
    height=max(500, top_n * 35),
    xaxis_title=metric,
    yaxis_title="Product"
)

if metric != "NetUnits":
    fig.update_xaxes(tickprefix="£")

st.plotly_chart(fig)

st.caption(
    "GrossSales represents positive merchandise value. "
    "NetSales incorporates signed negative transactions. "
    "Results are provisional."
)

# Detailed results
with st.expander("View Product Performance Data"):
    st.dataframe(
        top_products.sort_values(
            metric, ascending=False
        ),
        hide_index=True
    )

# Download results
st.download_button(
    "Download Product Rankings",
    data=top_products.to_csv(index=False).encode("utf-8"),
    file_name="product_rankings.csv",
    mime="text/csv"
)