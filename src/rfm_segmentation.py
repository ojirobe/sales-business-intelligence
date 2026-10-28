from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

SALES_FILE = PROCESSED / "classified_sales.csv"
NET_FILE = PROCESSED / "net_customer_analysis.csv"
MATCH_FILE = PROCESSED / "unique_cancellation_candidates.csv"

# Load datasets
sales = pd.read_csv(
    SALES_FILE,
    dtype={"InvoiceNo": "string"},
    low_memory=False
)

net = pd.read_csv(NET_FILE)

matches = pd.read_csv(
    MATCH_FILE,
    dtype={"InvoiceNo_Purchase": "string"}
)

# Standardise customer IDs
sales["CustomerID"] = pd.to_numeric(
    sales["CustomerID"], errors="coerce"
).astype("Int64")

net["CustomerID"] = pd.to_numeric(
    net["CustomerID"], errors="coerce"
).astype("Int64")

sales["InvoiceDate"] = pd.to_datetime(
    sales["InvoiceDate"]
)

# Remove purchase invoices identified as fully cancelled
cancelled_invoice_ids = set(
    matches["InvoiceNo_Purchase"].dropna()
)

purchases = sales.loc[
    (sales["TransactionCategory"] == "Merchandise")
    & sales["CustomerID"].notna()
    & ~sales["InvoiceNo"].isin(cancelled_invoice_ids)
].copy()

# Fixed snapshot date
snapshot = pd.Timestamp("2011-12-10")

# Calculate recency and frequency
rf = (
    purchases.groupby("CustomerID")
    .agg(
        LastPurchase=("InvoiceDate", "max"),
        Frequency=("InvoiceNo", "nunique")
    )
    .reset_index()
)

rf["Recency"] = (
    snapshot.normalize()
    - rf["LastPurchase"].dt.normalize()
).dt.days

# Add signed net monetary values
rfm = rf.merge(
    net[["CustomerID", "NetValue"]],
    on="CustomerID",
    how="left",
    validate="one_to_one"
)

rfm = rfm.rename(columns={"NetValue": "Monetary"})

# Flag uncertain monetary cases
rfm["NeedsReview"] = (
    rfm["Monetary"].isna()
    | (rfm["Monetary"] <= 0)
)

# Score eligible customers
eligible = rfm.loc[
    ~rfm["NeedsReview"]
].copy()

def percentile_score(series, higher_is_better=True):
    percentile = series.rank(
        method="average", pct=True
    )

    if not higher_is_better:
        percentile = 1 - percentile

    return np.clip(
        np.ceil(percentile * 5), 1, 5
    ).astype(int)

eligible["R_Score"] = percentile_score(
    eligible["Recency"], higher_is_better=False
)

eligible["F_Score"] = percentile_score(
    eligible["Frequency"], higher_is_better=True
)

eligible["M_Score"] = percentile_score(
    eligible["Monetary"], higher_is_better=True
)

# Assign business-friendly customer segments
conditions = [
    (eligible["R_Score"] >= 4)
    & (eligible["F_Score"] >= 4)
    & (eligible["M_Score"] >= 4),

    (eligible["R_Score"] >= 4)
    & (eligible["F_Score"] <= 2),

    (eligible["R_Score"] <= 2)
    & (eligible["F_Score"] >= 4),

    (eligible["R_Score"] <= 2)
    & (eligible["F_Score"] <= 2),
]

labels = [
    "Champions",
    "New / Occasional",
    "At Risk",
    "Hibernating"
]

eligible["Segment"] = np.select(
    conditions,
    labels,
    default="Regular Customers"
)

# Combine eligible and review cases
review = rfm.loc[rfm["NeedsReview"]].copy()
review["R_Score"] = pd.NA
review["F_Score"] = pd.NA
review["M_Score"] = pd.NA
review["Segment"] = "Needs Review"

result = pd.concat(
    [eligible, review],
    ignore_index=True
)

# Validate
assert result["CustomerID"].is_unique
assert (eligible["Recency"] >= 0).all()
assert (eligible["Frequency"] >= 1).all()

# Display segmentation results
print("\nCUSTOMER RFM SEGMENTATION")
print("=" * 65)

print("Customers with retained purchase activity:", len(result))

print("\nSEGMENT DISTRIBUTION")
print(result["Segment"].value_counts().to_string())

print("\nCUSTOMER 16446")
print(
    result.loc[
        result["CustomerID"] == 16446
    ].to_string(index=False)
)

print("\nCUSTOMER 12346")
print(
    result.loc[
        result["CustomerID"] == 12346
    ].to_string(index=False)
)

# Save output
result.to_csv(
    PROCESSED / "rfm_segments_preliminary.csv",
    index=False
)

print("\nPreliminary RFM segmentation saved!")