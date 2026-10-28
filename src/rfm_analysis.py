from pathlib import Path
import pandas as pd

# 1. Locate our existing analytical datasets
ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

SALES_FILE = PROCESSED / "classified_sales.csv"
NET_FILE = PROCESSED / "net_customer_analysis.csv"

# 2. Load the datasets
sales = pd.read_csv(
    SALES_FILE,
    dtype={"InvoiceNo": "string"},
    low_memory=False
)

net = pd.read_csv(NET_FILE)

# 3. Standardize customer identifiers
sales["CustomerID"] = pd.to_numeric(
    sales["CustomerID"], errors="coerce"
).astype("Int64")

net["CustomerID"] = pd.to_numeric(
    net["CustomerID"], errors="coerce"
).astype("Int64")

sales["InvoiceDate"] = pd.to_datetime(
    sales["InvoiceDate"]
)

# 4. Select identifiable positive merchandise sales
purchases = sales.loc[
    (sales["TransactionCategory"] == "Merchandise")
    & sales["CustomerID"].notna()
].copy()

# 5. Define a reproducible analysis date
snapshot_date = pd.Timestamp("2011-12-10")

# 6. Calculate recency and frequency
rf = (
    purchases.groupby("CustomerID")
    .agg(
        LastPurchase=("InvoiceDate", "max"),
        Frequency=("InvoiceNo", "nunique")
    )
    .reset_index()
)

rf["Recency"] = (
    snapshot_date - rf["LastPurchase"]
).dt.days

# 7. Add preliminary net monetary values
rfm = rf.merge(
    net[["CustomerID", "NetValue"]],
    on="CustomerID",
    how="left",
    validate="one_to_one"
)

rfm = rfm.rename(
    columns={"NetValue": "Monetary"}
)

# 8. Flag customers requiring special review
rfm["NeedsReview"] = rfm["Monetary"] <= 0

# 9. Validate the results
assert rfm["CustomerID"].is_unique
assert (rfm["Recency"] >= 0).all()
assert (rfm["Frequency"] >= 1).all()
assert rfm["Monetary"].notna().all()

# 10. Display results
print("\nPRELIMINARY RFM CUSTOMER ANALYSIS")
print("=" * 75)

print("Customers analysed:", len(rfm))
print("Customers flagged:", rfm["NeedsReview"].sum())

print("\nRFM SUMMARY")
print(
    rfm[["Recency", "Frequency", "Monetary"]]
    .describe()
    .round(2)
)

print("\nPREVIOUSLY INVESTIGATED CUSTOMERS")
print(
    rfm[
        rfm["CustomerID"].isin([16446, 12346])
    ].to_string(index=False)
)

# 11. Export analysis
rfm.to_csv(
    PROCESSED / "rfm_metrics_preliminary.csv",
    index=False
)

print("\nPreliminary RFM metrics saved successfully!")