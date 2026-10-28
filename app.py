from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Configure the application
st.set_page_config(
    page_title="Retail Sales Intelligence",
    page_icon="📊",
    layout="wide"
)

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "processed" / "classified_sales.csv"


# Cache the dataset so it is not reloaded on every interaction
@st.cache_data
def load_data():
    df = pd.read_csv(
        DATA_FILE,
        dtype={
            "InvoiceNo": "string",
            "StockCode": "string",
            "CustomerID": "string"
        },
        low_memory=False
    )

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


# Load data
if not DATA_FILE.exists():
    st.error("Classified sales data not found.")
    st.stop()

df = load_data()

# Header
st.title("📊 Retail Sales Intelligence Dashboard")



st.write(
    "Interactive business intelligence analysis "
    "of historical UK online retail transactions."
)

st.caption(
    "Dataset: December 2010–December 2011. "
    "Positive merchandise transactions before returns. "
    "Classification remains provisional."
)

# Sidebar filters
st.sidebar.header("Dashboard Filters")

countries = ["All Countries"] + sorted(
    df["Country"].dropna().unique().tolist()
)

selected_country = st.sidebar.selectbox(
    "Select Country",
    countries
)

filtered = df.copy()

if selected_country != "All Countries":
    filtered = filtered.loc[
        filtered["Country"] == selected_country
    ].copy()

# Calculate KPIs from the filtered data
gross_sales = filtered["Revenue"].sum()
invoice_count = filtered["InvoiceNo"].nunique()
transaction_lines = len(filtered)

average_order_value = (
    gross_sales / invoice_count
    if invoice_count > 0
    else 0
)

# KPI cards
st.subheader("Sales Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Positive Merchandise Sales",
    f"£{gross_sales / 1_000_000:,.2f}M",
    help=f"Exact value: £{gross_sales:,.2f}"
)

col2.metric(
    "Unique Invoices",
    f"{invoice_count:,}"
)

col3.metric(
    "Transaction Lines",
    f"{transaction_lines:,}"
)

col4.metric(
    "Average Invoice Value",
    f"£{average_order_value:,.2f}"
)

# Monthly analysis
monthly = (
    filtered.assign(
        SalesMonth=filtered["InvoiceDate"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )
    .groupby("SalesMonth", as_index=False)
    .agg(
        MerchandiseSales=("Revenue", "sum"),
        TransactionLines=("InvoiceNo", "size")
    )
    .sort_values("SalesMonth")
)

st.subheader("Monthly Merchandise Sales Trend")

complete_months = monthly.loc[
    monthly["SalesMonth"] < "2011-12-01"
].copy()

fig = px.line(
    complete_months,
    x="SalesMonth",
    y="MerchandiseSales",
    markers=True,
    title="Monthly Positive Merchandise Sales",
    labels={
        "SalesMonth": "Month",
        "MerchandiseSales": "Sales Value (£)"
    }
)

fig.update_layout(
    hovermode="x unified",
    yaxis_tickprefix="£",
    xaxis_title="Month",
    yaxis_title="Merchandise Sales (£)"
)

st.plotly_chart(fig)

st.caption(
    "Note: December 2011 includes transactions only up to "
    "9 December. Sales figures represent positive merchandise "
    "transactions before returns and cancellations."
)

# Detailed results
with st.expander("View Monthly Data"):
    st.dataframe(
    monthly,
    width="stretch",
    hide_index=True
)
st.divider()

st.caption(
    "Portfolio project | Python · Pandas · SQL · "
    "Streamlit · Plotly"
)




# ==========================================
# PRODUCT PERFORMANCE ANALYSIS
# ==========================================

st.divider()
st.header("Product Performance Analytics")

st.caption(
    "All-country product performance. "
    "Signed transaction values include negative quantities. "
    "Results remain preliminary."
)

PRODUCT_FILE = (
    ROOT / "data" / "processed"
    / "net_product_performance.csv"
)

if PRODUCT_FILE.exists():

    @st.cache_data
    def load_products():
        return pd.read_csv(
            PRODUCT_FILE,
            dtype={"StockCode": "string"}
        )

    products = load_products()

    # Product selection controls
    col_a, col_b = st.columns(2)

    with col_a:
        top_n = st.slider(
            "Number of products",
            min_value=5,
            max_value=30,
            value=10,
            step=5
        )

    with col_b:
        metric = st.selectbox(
            "Rank products by",
            ["NetSales", "GrossSales", "NetUnits"]
        )

    top_products = (
        products.sort_values(
            metric, ascending=False
        )
        .head(top_n)
        .sort_values(metric)
    )

    # Interactive bar chart
    fig_products = px.bar(
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

    fig_products.update_layout(
        height=max(500, top_n * 35),
        xaxis_title=metric,
        yaxis_title="Product"
    )

    if metric in ["NetSales", "GrossSales"]:
        fig_products.update_xaxes(
            tickprefix="£"
        )

    st.plotly_chart(fig_products)

    # Product performance table
    with st.expander("View Product Performance Data"):
        st.dataframe(
            products.head(100),
            width="stretch",
            hide_index=True
        )

else:
    st.warning(
        "Product performance dataset not found. "
        "Run net_product_performance.py first."
    )




# ==================================================
# CUSTOMER RFM SEGMENTATION DASHBOARD
# ==================================================

st.divider()
st.header("Customer Intelligence | RFM Segmentation")

st.caption(
    "Historical customer segmentation using Recency, "
    "Frequency and Monetary values. Results are preliminary "
    "because some cancellations remain unresolved."
)

RFM_FILE = (
    ROOT / "data" / "processed"
    / "rfm_segments_preliminary.csv"
)

if RFM_FILE.exists():

    @st.cache_data
    def load_rfm_data():
        data = pd.read_csv(
            RFM_FILE,
            dtype={"CustomerID": "string"},
            low_memory=False
        )

        data["Recency"] = pd.to_numeric(
            data["Recency"], errors="coerce"
        )

        data["Frequency"] = pd.to_numeric(
            data["Frequency"], errors="coerce"
        )

        data["Monetary"] = pd.to_numeric(
            data["Monetary"], errors="coerce"
        )

        return data

    rfm = load_rfm_data()

    # ------------------------------------------
    # 1. CUSTOMER KPIs
    # ------------------------------------------

    total_customers = len(rfm)

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

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Customers Analysed",
        f"{total_customers:,}"
    )

    k2.metric(
        "Champions",
        f"{champions:,}"
    )

    k3.metric(
        "At Risk",
        f"{at_risk:,}"
    )

    k4.metric(
        "Hibernating",
        f"{hibernating:,}"
    )

    # ------------------------------------------
    # 2. FILTER CUSTOMER SEGMENTS
    # ------------------------------------------

    st.subheader("Explore Customer Segments")

    available_segments = sorted(
        rfm["Segment"].dropna().unique().tolist()
    )

    selected_segments = st.multiselect(
    "Choose customer segments",
    options=available_segments,
    default=["Champions", "At Risk", "Hibernating"],
    key="rfm_segment_filter"
)

    filtered_rfm = rfm.loc[
        rfm["Segment"].isin(selected_segments)
    ].copy()

    if filtered_rfm.empty:
        st.warning(
            "No customers match the selected segments."
        )

    else:

        # ------------------------------------------
        # 3. SEGMENT DISTRIBUTION
        # ------------------------------------------

        segment_summary = (
            filtered_rfm.groupby(
                "Segment", as_index=False
            )
            .agg(
                Customers=("CustomerID", "nunique"),
                MedianRecency=("Recency", "median"),
                MedianFrequency=("Frequency", "median"),
                MedianMonetary=("Monetary", "median")
            )
        )

        segment_summary["Percentage"] = (
            segment_summary["Customers"]
            / total_customers * 100
        ).round(2)

        segment_summary = segment_summary.sort_values(
            "Customers", ascending=True
        )

        fig_segments = px.bar(
            segment_summary,
            x="Customers",
            y="Segment",
            orientation="h",
            text="Customers",
            color="Segment",
            title="Customer Distribution by RFM Segment",
            hover_data=[
                "Percentage",
                "MedianRecency",
                "MedianFrequency",
                "MedianMonetary"
            ]
        )

        fig_segments.update_traces(
            textposition="outside"
        )

        fig_segments.update_layout(
            height=480,
            showlegend=False,
            xaxis_title="Number of Customers",
            yaxis_title="Customer Segment"
        )

        st.plotly_chart(fig_segments)

        st.caption(
            "Segment percentages use the full preliminary "
            "RFM population as their denominator."
        )

        # ------------------------------------------
        # 4. CUSTOMER BEHAVIOUR SCATTER PLOT
        # ------------------------------------------

        st.subheader(
            "Purchase Frequency vs Customer Monetary Value"
        )

        scatter_data = filtered_rfm.loc[
            filtered_rfm["Frequency"].notna()
            & filtered_rfm["Monetary"].notna()
            & filtered_rfm["Recency"].notna()
        ].copy()

        fig_scatter = px.scatter(
            scatter_data,
            x="Frequency",
            y="Monetary",
            color="Segment",
            hover_data=[
                "CustomerID",
                "Recency",
                "Frequency",
                "Monetary"
            ],
            title="Customer Purchasing Behaviour",
            labels={
                "Frequency": "Purchase Frequency",
                "Monetary": "Net Transaction Value (£)"
            },
            opacity=0.65
        )

        fig_scatter.update_layout(
            height=550,
            yaxis_tickprefix="£"
        )

        st.plotly_chart(fig_scatter)

        st.caption(
            "A small number of very high-value customers "
            "may affect the chart scale. Values are based "
            "on preliminary signed transaction calculations."
        )

        # ------------------------------------------
        # 5. CUSTOMER DETAILS
        # ------------------------------------------

        st.subheader("Customer Segmentation Details")

        display_columns = [
            "CustomerID",
            "Recency",
            "Frequency",
            "Monetary",
            "R_Score",
            "F_Score",
            "M_Score",
            "Segment"
        ]

        customer_table = filtered_rfm[
            display_columns
        ].copy()

        st.dataframe(
            customer_table,
            hide_index=True
        )

        # ------------------------------------------
        # 6. DOWNLOAD CUSTOMER DATA
        # ------------------------------------------

        csv_data = customer_table.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Filtered RFM Data",
            data=csv_data,
            file_name="rfm_customer_segments.csv",
            mime="text/csv",
            key="rfm_download"
        )

    # ------------------------------------------
    # 7. METHODOLOGY
    # ------------------------------------------

    with st.expander("RFM Methodology and Limitations"):

        st.write(
            "**Recency:** Calendar days since the latest "
            "qualifying purchase, measured relative to "
            "10 December 2011."
        )

        st.write(
            "**Frequency:** Distinct qualifying purchase "
            "invoices after excluding selected full "
            "cancellation candidates."
        )

        st.write(
            "**Monetary:** Signed merchandise transaction "
            "value based on the provisional classification."
        )

        st.warning(
            "The RFM model is preliminary. Only a subset "
            "of full cancellations has been matched. "
            "Partial, ambiguous and multi-line cancellations "
            "require further validation. Customers with no "
            "retained purchase activity are not included "
            "in the current segmentation file."
        )

        st.caption(
            "This section describes all-country historical "
            "customer segments. The Sales Overview country "
            "filter does not apply here."
        )

else:

    st.error(
        "RFM segmentation data was not found. "
        "Run: python src/rfm_segmentation.py"
    )




# ==========================================
# GEOGRAPHICAL SALES ANALYTICS
# ==========================================

st.divider()
st.header("Geographical Sales Analytics")

st.caption(
    "Historical positive merchandise sales by country, "
    "before returns and cancellations."
)

GEO_FILE = (
    ROOT / "data" / "processed"
    / "geographical_sales.csv"
)

if GEO_FILE.exists():

    @st.cache_data
    def load_geo_data():
        return pd.read_csv(GEO_FILE)

    geo = load_geo_data()

    uk_sales = geo.loc[
        geo["Country"] == "United Kingdom",
        "GrossMerchandiseValue"
    ].sum()

    total_geo_sales = geo["GrossMerchandiseValue"].sum()
    international_sales = total_geo_sales - uk_sales

    uk_share = uk_sales / total_geo_sales * 100

    g1, g2, g3 = st.columns(3)

    g1.metric(
        "UK Merchandise Sales",
        f"£{uk_sales / 1_000_000:.2f}M"
    )

    g2.metric(
        "International Sales",
        f"£{international_sales / 1_000_000:.2f}M"
    )

    g3.metric(
        "UK Sales Share",
        f"{uk_share:.2f}%"
    )

    # Let the user include or exclude the UK
    include_uk = st.checkbox(
        "Include United Kingdom in ranking",
        value=False
    )

    top_n_geo = st.slider(
        "Number of countries to display",
        5, 20, 10,
        key="geo_top_n"
    )

    geo_filtered = geo.copy()

    if not include_uk:
        geo_filtered = geo_filtered.loc[
            geo_filtered["Country"] != "United Kingdom"
        ]

    top_countries = (
        geo_filtered.nlargest(
            top_n_geo, "GrossMerchandiseValue"
        )
        .sort_values("GrossMerchandiseValue")
    )

    fig_geo = px.bar(
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

    fig_geo.update_layout(
        height=550,
        xaxis_title="Positive Merchandise Sales (£)",
        yaxis_title="Country",
        xaxis_tickprefix="£",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig_geo)

    with st.expander("View Geographical Sales Data"):
        st.dataframe(geo, hide_index=True)

    st.download_button(
        "Download Geographical Sales Data",
        data=geo.to_csv(index=False).encode("utf-8"),
        file_name="geographical_sales.csv",
        mime="text/csv"
    )

else:
    st.warning("Geographical sales dataset not found.")
