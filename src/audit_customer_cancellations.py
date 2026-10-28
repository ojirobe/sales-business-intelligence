from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "raw" / "Online Retail.xlsx"
OUTPUT = ROOT / "data" / "processed"

# Load original data, including negative transactions
df = pd.read_excel(FILE)

# Standardize customer and product identifiers
df["CustomerID"] = pd.to_numeric(
    df["CustomerID"], errors="coerce"
).astype("Int64")

df["StockCode"] = (
    df["StockCode"].astype("string").str.strip().str.upper()
)

df["InvoiceNo"] = (
    df["InvoiceNo"].astype("string").str.strip()
)

# Focus on identifiable customers and positive prices
df = df.loc[
    df["CustomerID"].notna()
    & (df["UnitPrice"] > 0)
].copy()

df["LineValue"] = df["Quantity"] * df["UnitPrice"]

# Calculate signed quantities and monetary values
# for each customer, product and unit price
audit = (
    df.groupby(
        ["CustomerID", "StockCode", "UnitPrice"],
        as_index=False,
        dropna=False
    )
    .agg(
        NetQuantity=("Quantity", "sum"),
        NetValue=("LineValue", "sum"),
        TransactionLines=("InvoiceNo", "size")
    )
)

# Identify groups whose signed quantity is zero
audit["FullyOffsetQuantity"] = (
    audit["NetQuantity"] == 0
)

print("\nCUSTOMER CANCELLATION AUDIT")
print("=" * 70)

print("Customer-product-price groups:", len(audit))

print(
    "Groups with zero net quantity:",
    audit["FullyOffsetQuantity"].sum()
)

print("\nCUSTOMER 12346")
print(
    audit.loc[
        audit["CustomerID"] == 12346
    ].to_string(index=False)
)

print("\nCUSTOMER 16446")
print(
    audit.loc[
        audit["CustomerID"] == 16446
    ].to_string(index=False)
)

# Save results for inspection
OUTPUT.mkdir(parents=True, exist_ok=True)

audit.to_csv(
    OUTPUT / "customer_cancellation_audit.csv",
    index=False
)

print("\nCustomer cancellation audit saved successfully!")