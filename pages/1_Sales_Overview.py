from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# Locate the project root
ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    ROOT / "data" / "processed"
    / "classified_sales.parquet"
)

st.title("📈 Sales Overview")

st.caption(
    "Historical retail merchandise sales "
    "from December 2010 to December 2011."
)

# Load the compressed dataset
@st.cache_data
def load_sales():
    df = pd.read_parquet(DATA_FILE)

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    )

    df["Revenue"] = pd.to_numeric(
        df["Revenue"], errors="coerce"
    )

    return df.loc[
        (df["TransactionCategory"] == "Merchandise")
        & df["InvoiceDate"].notna()
        & df["Revenue"].notna()
    ].copy()


sales = load_sales()

# Country filter
countries = ["All Countries"] + sorted(
    sales["Country"].dropna().unique().tolist()
)

country = st.selectbox(
    "Select Country",
    countries
)

filtered = sales.copy()

if country != "All Countries":
    filtered = filtered.loc[
        filtered["Country"] == country
    ].copy()

# Calculate business KPIs
total_sales = filtered["Revenue"].sum()
invoices = filtered["InvoiceNo"].nunique()
lines = len(filtered)

average_invoice = (
    total_sales / invoices if invoices else 0
)

# Display KPI cards
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Positive Merchandise Sales",
    f"£{total_sales / 1_000_000:.2f}M"
)

c2.metric("Unique Invoices", f"{invoices:,}")
c3.metric("Transaction Lines", f"{lines:,}")

c4.metric(
    "Average Invoice Value",
    f"£{average_invoice:,.2f}"
)

# Monthly sales calculation
monthly = (
    filtered.assign(
        Month=filtered["InvoiceDate"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )
    .groupby("Month", as_index=False)
    .agg(Sales=("Revenue", "sum"))
    .sort_values("Month")
)

# Exclude incomplete December 2011 from trend
complete_months = monthly.loc[
    monthly["Month"] < pd.Timestamp("2011-12-01")
].copy()

fig = px.line(
    complete_months,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Positive Merchandise Sales"
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Merchandise Sales (£)",
    yaxis_tickprefix="£"
)

st.plotly_chart(fig)

st.caption(
    "December 2011 is incomplete. Figures represent "
    "positive merchandise sales before returns."
)

with st.expander("View Monthly Data"):
    st.dataframe(monthly, hide_index=True)