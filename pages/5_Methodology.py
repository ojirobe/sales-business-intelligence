
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"

st.title("📚 Methodology & Data Quality")

st.caption(
    "Technical documentation, business definitions, "
    "data validation and limitations."
)

st.header("1. Dataset Overview")

st.write(
    "This project analyses the UCI Online Retail dataset, "
    "which contains transactions recorded between "
    "1 December 2010 and 9 December 2011."
)

st.write(
    "The analysis uses Python, Pandas, DuckDB, SQL, "
    "Plotly and Streamlit."
)

st.markdown(
    "[Original UCI Online Retail Dataset]"
    "(https://archive.ics.uci.edu/dataset/352/online+retail)"
)

st.header("2. Data Quality Assessment")

quality = pd.DataFrame({
    "Quality Indicator": [
        "Original transaction rows",
        "Missing Customer IDs",
        "Missing product descriptions",
        "Additional exact duplicate rows",
        "Negative quantity records",
        "Cancellation invoice records",
        "Negative price records",
        "Positive transaction rows retained"
    ],
    "Observed Count": [
        541909,
        135080,
        1454,
        5268,
        10624,
        9288,
        2,
        530104
    ]
})

st.dataframe(quality, hide_index=True)

st.caption(
    "Counts were obtained from the original data "
    "exploration and cleaning scripts. Duplicate "
    "and cancellation counts represent different "
    "quality indicators and may overlap."
)

st.header("3. Data Preparation")

with st.expander("Cleaning and classification rules", expanded=True):
    st.write(
        "The pipeline identifies missing values, "
        "negative quantities, cancellations, unusual "
        "stock codes and repeated transaction records."
    )

    st.write(
        "Positive merchandise lines are separated from "
        "shipping, fees, accounting adjustments and "
        "other transaction categories."
    )

    st.write(
        "Exact duplicates were investigated separately. "
        "Their removal was assessed using a sensitivity "
        "analysis rather than assumed automatically."
    )

    st.warning(
        "Transaction classification and cancellation "
        "matching remain provisional. Some ambiguous "
        "records require further review."
    )

st.header("4. Business KPI Definitions")

st.subheader("Positive Merchandise Sales")

st.latex(
    r"GMS = \sum_{i \in \mathcal{M}^{+}} q_i p_i"
)

st.write(
    "Where q represents quantity, p represents unit "
    "price and M+ is the set of qualifying positive "
    "merchandise transaction lines."
)

st.subheader("Average Invoice Value")

st.latex(
    r"AIV = \frac{GMS}{N_{\mathrm{invoices}}}"
)

st.write(
    "The denominator is the number of distinct invoices "
    "containing qualifying positive merchandise lines."
)

st.subheader("Geographical Sales Share")

st.latex(
    r"S_c = \frac{GMS_c}{GMS_{\mathrm{all}}}\times 100"
)

st.write(
    "This measures the percentage of positive "
    "merchandise sales attributed to country c."
)

st.subheader("Net Product Transaction Value")

st.latex(
    r"NetValue_j = \sum_{i \in j} q_i p_i"
)

st.write(
    "Positive and negative qualifying merchandise "
    "transaction lines are combined for each product. "
    "This is not accounting profit."
)

st.header("5. Customer RFM Methodology")

rfm_definitions = pd.DataFrame({
    "Metric": ["Recency", "Frequency", "Monetary"],
    "Definition": [
        "Days since latest qualifying retained purchase",
        "Number of qualifying purchase invoices",
        "Signed transaction value per customer"
    ]
})

st.dataframe(rfm_definitions, hide_index=True)

st.info(
    "RFM results use a historical reference period. "
    "They are preliminary because some return and "
    "cancellation matches remain unresolved."
)

st.header("6. Automated Reconciliation Checks")

parquet_file = DATA / "classified_sales.parquet"
geo_file = DATA / "geographical_sales.csv"
rfm_file = DATA / "rfm_segments_preliminary.csv"

if all(
    file.exists()
    for file in [parquet_file, geo_file, rfm_file]
):

    @st.cache_data
    def load_validation_data():
        sales = pd.read_parquet(parquet_file)
        geo = pd.read_csv(geo_file)
        rfm = pd.read_csv(rfm_file)

        sales["Revenue"] = pd.to_numeric(
            sales["Revenue"], errors="coerce"
        )

        sales["InvoiceDate"] = pd.to_datetime(
            sales["InvoiceDate"], errors="coerce"
        )

        return sales, geo, rfm

    sales, geo, rfm = load_validation_data()

    merchandise = sales.loc[
        (sales["TransactionCategory"] == "Merchandise")
        & sales["InvoiceDate"].notna()
        & sales["Revenue"].notna()
    ]

    sales_total = merchandise["Revenue"].sum()
    geo_total = geo["GrossMerchandiseValue"].sum()

    checks = pd.DataFrame({
        "Validation": [
            "Classified transaction row count",
            "Merchandise line count",
            "Sales vs geographical total",
            "RFM customer record count"
        ],
        "Passed": [
            len(sales) == 530104,
            len(merchandise) == 527713,
            abs(sales_total - geo_total) < 0.01,
            len(rfm) == 4333
        ]
    })

    st.dataframe(checks, hide_index=True)

    if checks["Passed"].all():
        st.success("All four reconciliation checks passed.")
    else:
        st.error(
            "One or more checks failed. "
            "Review the source datasets."
        )

    st.caption(
        "These checks establish selected row counts and "
        "aggregate consistency. They do not constitute "
        "a complete audit of all transaction rules."
    )

else:
    st.warning(
        "One or more validation datasets are missing."
    )

st.header("7. Analytical Limitations")

st.markdown("""
- The dataset is historical and does not describe current retail performance.
- Positive merchandise sales exclude negative transactions and returns.
- The dataset does not provide sufficient cost information to calculate reliable profit margins.
- Exact duplicate records require contextual review.
- Some cancellations cannot yet be matched unambiguously.
- Customer segments are provisional, not fully validated retention classifications.
- December 2011 is an incomplete reporting month.
""")

st.header("8. Reproducibility")

st.write(
    "The GitHub repository will contain the analysis "
    "scripts, SQL queries, environment requirements, "
    "data documentation and Streamlit application."
)

st.code(
    "python -m pip install -r requirements.txt\n"
    "python -m streamlit run app.py",
    language="bash"
)

st.caption(
    "Sales & Business Intelligence Portfolio | "
    "Data Quality, Statistical Analysis and Reproducibility"
)