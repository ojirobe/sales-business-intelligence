
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Locate the customer dataset
ROOT = Path(__file__).resolve().parents[1]

RFM_FILE = (
    ROOT / "data" / "processed"
    / "rfm_segments_preliminary.csv"
)

st.title("👥 Customer Analytics")

st.caption(
    "Preliminary RFM segmentation of historical "
    "online retail customers. Cancellation "
    "matching is not yet fully resolved."
)

if not RFM_FILE.exists():
    st.error("Customer RFM dataset not found.")
    st.stop()


# 2. Load and validate customer data
@st.cache_data
def load_customers():
    df = pd.read_csv(
        RFM_FILE,
        dtype={"CustomerID": "string"}
    )

    required = [
        "CustomerID", "Recency", "Frequency",
        "Monetary", "Segment"
    ]

    missing = [
        c for c in required if c not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    for col in ["Recency", "Frequency", "Monetary"]:
        df[col] = pd.to_numeric(
            df[col], errors="coerce"
        )

    return df


rfm = load_customers()

# 3. Calculate overall KPIs
total = rfm["CustomerID"].nunique()

champions = (
    rfm["Segment"] == "Champions"
).sum()

at_risk = (
    rfm["Segment"] == "At Risk"
).sum()

hibernating = (
    rfm["Segment"] == "Hibernating"
).sum()

st.subheader("Customer Segmentation Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Customers Analysed", f"{total:,}")
c2.metric("Champions", f"{champions:,}")
c3.metric("At Risk", f"{at_risk:,}")
c4.metric("Hibernating", f"{hibernating:,}")

# 4. Interactive segment filter
st.subheader("Explore Customer Segments")

segments = sorted(
    rfm["Segment"].dropna().unique().tolist()
)

selected = st.multiselect(
    "Select customer segments",
    options=segments,
    default=segments
)

filtered = rfm[
    rfm["Segment"].isin(selected)
].copy()

if filtered.empty:
    st.info("Select a segment to display results.")
    st.stop()

# 5. Customer distribution
summary = (
    filtered.groupby("Segment", as_index=False)
    .agg(Customers=("CustomerID", "nunique"))
)

summary["Percentage"] = (
    summary["Customers"] / total * 100
).round(2)

summary = summary.sort_values("Customers")

fig = px.bar(
    summary,
    x="Customers",
    y="Segment",
    orientation="h",
    color="Segment",
    text="Customers",
    hover_data=["Percentage"],
    title="Customer Distribution by RFM Segment"
)

fig.update_layout(
    showlegend=False,
    height=450,
    xaxis_title="Number of Customers",
    yaxis_title="Customer Segment"
)

st.plotly_chart(fig)

# 6. Customer purchasing behaviour
st.subheader("Customer Purchasing Behaviour")

plot_data = filtered.dropna(
    subset=["Frequency", "Monetary"]
)

scatter = px.scatter(
    plot_data,
    x="Frequency",
    y="Monetary",
    color="Segment",
    hover_data=["CustomerID", "Recency"],
    opacity=0.6,
    title="Purchase Frequency vs Monetary Value",
    labels={
        "Frequency": "Purchase Frequency",
        "Monetary": "Signed Transaction Value (£)"
    }
)

scatter.update_layout(
    height=550,
    yaxis_tickprefix="£"
)

st.plotly_chart(scatter)

# 7. Customer details
st.subheader("Customer Data")

st.dataframe(
    filtered,
    hide_index=True
)

# 8. Download filtered data
st.download_button(
    "Download Customer Data",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="customer_rfm_data.csv",
    mime="text/csv"
)

# 9. Methodology
with st.expander("RFM Methodology"):
    st.write(
        "**Recency:** Days since the latest "
        "qualifying retained purchase."
    )

    st.write(
        "**Frequency:** Number of qualifying "
        "purchase invoices."
    )

    st.write(
        "**Monetary:** Signed merchandise "
        "transaction value."
    )

    st.warning(
        "These are provisional results. Partial "
        "and ambiguous cancellations have not "
        "been fully reconciled. Customers without "
        "retained purchases are excluded."
    )