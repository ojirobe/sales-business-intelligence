from pathlib import Path

import pandas as pd
import streamlit as st

# ==========================================
# PAGE CONFIGURATION
# ==========================================


ROOT = Path(__file__).resolve().parent

DATA_FILE = (
    ROOT / "data" / "processed"
    / "classified_sales.parquet"
)

# ==========================================
# HOMEPAGE
# ==========================================

st.title("📊 Retail Sales Intelligence")

st.subheader(
    "An Interactive Business Intelligence "
    "and Customer Analytics Portfolio Project"
)

st.write(
    "Explore historical retail transactions through "
    "interactive dashboards covering sales performance, "
    "product rankings, customer segmentation and "
    "international markets."
)

st.caption(
    "Data period: December 2010 – December 2011 | "
    "Source: UCI Online Retail Dataset"
)

st.divider()

# ==========================================
# VERIFIED PROJECT INDICATORS
# ==========================================

st.header("Project at a Glance")


@st.cache_data
def get_project_metrics():
    data = pd.read_parquet(
        DATA_FILE,
        columns=[
            "InvoiceNo",
            "TransactionCategory",
            "Revenue"
        ]
    )

    merchandise = data.loc[
        data["TransactionCategory"] == "Merchandise"
    ].copy()

    merchandise["Revenue"] = pd.to_numeric(
        merchandise["Revenue"],
        errors="coerce"
    )

    merchandise = merchandise.dropna(
        subset=["Revenue"]
    )

    return {
        "sales": merchandise["Revenue"].sum(),
        "invoices": merchandise["InvoiceNo"].nunique(),
        "lines": len(merchandise)
    }


if DATA_FILE.exists():

    metrics = get_project_metrics()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Positive Merchandise Sales",
        f"£{metrics['sales'] / 1_000_000:.2f}M"
    )

    c2.metric(
        "Unique Sales Invoices",
        f"{metrics['invoices']:,}"
    )

    c3.metric(
        "Merchandise Transaction Lines",
        f"{metrics['lines']:,}"
    )

else:
    st.warning(
        "The classified retail dataset was not found."
    )

st.caption(
    "Positive merchandise sales are before returns "
    "and cancellations. These figures do not "
    "represent net profit."
)

st.divider()

# ==========================================
# DASHBOARD NAVIGATION
# ==========================================

st.header("Explore the Analytics")

st.write(
    "Select one of the analytical pages below "
    "to investigate the results."
)

col1, col2 = st.columns(2)

with col1:

    st.subheader("📈 Sales Overview")

    st.write(
        "Explore monthly merchandise sales, "
        "invoice values and country-level filters."
    )

    st.page_link(
        "pages/1_Sales_Overview.py",
        label="Open Sales Dashboard",
        icon="📈"
    )

    st.subheader("👥 Customer Analytics")

    st.write(
        "Investigate RFM customer segmentation, "
        "purchasing frequency and monetary value."
    )

    st.page_link(
        "pages/3_Customer_Analytics.py",
        label="Explore Customers",
        icon="👥"
    )

    st.subheader("📚 Methodology & Data Quality")

    st.write(
        "Review cleaning decisions, statistical "
        "definitions, limitations and validation."
    )

    st.page_link(
        "pages/5_Methodology.py",
        label="View Methodology",
        icon="📚"
    )

with col2:

    st.subheader("🛍️ Product Performance")

    st.write(
        "Compare gross and net product transaction "
        "values and investigate returns."
    )

    st.page_link(
        "pages/2_Product_Performance.py",
        label="Explore Products",
        icon="🛍️"
    )

    st.subheader("🌍 Geographical Analytics")

    st.write(
        "Examine international market performance, "
        "country rankings and market concentration."
    )

    st.page_link(
        "pages/4_Geographical_Analytics.py",
        label="Explore Markets",
        icon="🌍"
    )

st.divider()

# ==========================================
# TECHNOLOGIES
# ==========================================

st.header("Technology Stack")

st.write(
    "Python | Pandas | SQL | DuckDB | "
    "Parquet | Plotly | Streamlit | Git"
)

st.header("Project Limitations")

st.info(
    "This portfolio uses a historical dataset. "
    "Transaction classifications and some cancellation "
    "matches remain provisional. Detailed assumptions "
    "and reconciliation checks are documented "
    "on the Methodology page."
)

st.divider()

st.caption(
    "Retail Sales Intelligence | "
    "Data Analytics & Business Intelligence Portfolio"
)