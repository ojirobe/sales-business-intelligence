from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "Online Retail.xlsx"
OUTPUT = ROOT / "data" / "processed"

df = pd.read_excel(RAW)

# Standardise identifiers and dates
df["InvoiceNo"] = df["InvoiceNo"].astype("string").str.strip()
df["StockCode"] = df["StockCode"].astype("string").str.strip()
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["CustomerID"] = pd.to_numeric(
    df["CustomerID"], errors="coerce"
).astype("Int64")

# Focus on known customers and valid prices
df = df.loc[
    df["CustomerID"].notna()
    & (df["UnitPrice"] > 0)
].copy()

# Single-line invoices only
invoice_sizes = df.groupby("InvoiceNo")["InvoiceNo"].transform("size")
single = df.loc[invoice_sizes == 1].copy()

purchases = single.loc[
    (single["Quantity"] > 0)
    & ~single["InvoiceNo"].str.startswith("C", na=False)
].copy()

returns = single.loc[
    (single["Quantity"] < 0)
    & single["InvoiceNo"].str.startswith("C", na=False)
].copy()

# Match by customer, product, price and quantity magnitude
purchases["QuantityMagnitude"] = purchases["Quantity"]
returns["QuantityMagnitude"] = returns["Quantity"].abs()

keys = [
    "CustomerID",
    "StockCode",
    "UnitPrice",
    "QuantityMagnitude"
]

matches = purchases.merge(
    returns,
    on=keys,
    suffixes=("_Purchase", "_Return")
)

# Cancellation must occur after the purchase
matches = matches.loc[
    matches["InvoiceDate_Return"]
    >= matches["InvoiceDate_Purchase"]
].copy()

# Report plausible matching pairs
print("\nPOTENTIAL FULL CANCELLATION MATCHES")
print("=" * 65)

print("Candidate pairs:", len(matches))

print(
    matches[
        [
            "CustomerID",
            "InvoiceNo_Purchase",
            "InvoiceNo_Return",
            "QuantityMagnitude"
        ]
    ].head(15).to_string(index=False)
)

# Save for review
OUTPUT.mkdir(parents=True, exist_ok=True)

matches.to_csv(
    OUTPUT / "potential_full_cancellations.csv",
    index=False
)

print("\nCandidate matches saved successfully!")
print("These are candidates, not yet unique verified matches.")