from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "raw" / "Online Retail.xlsx"

df = pd.read_excel(FILE)

df["CustomerID"] = pd.to_numeric(
    df["CustomerID"], errors="coerce"
).astype("Int64")

df["InvoiceNo"] = (
    df["InvoiceNo"].astype("string").str.strip()
)

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["LineValue"] = df["Quantity"] * df["UnitPrice"]

# Examine the two customers we already investigated
selected = df[
    df["CustomerID"].isin([12346, 16446])
].copy()

# Classify invoice type
selected["InvoiceType"] = "Purchase"

selected.loc[
    selected["InvoiceNo"].str.startswith("C", na=False),
    "InvoiceType"
] = "Cancellation"

# Summarise each individual invoice
invoices = (
    selected.groupby(
        ["CustomerID", "InvoiceNo", "InvoiceType"],
        as_index=False
    )
    .agg(
        InvoiceDate=("InvoiceDate", "min"),
        LineCount=("StockCode", "size"),
        InvoiceValue=("LineValue", "sum")
    )
    .sort_values(["CustomerID", "InvoiceDate"])
)

print("\nCUSTOMER INVOICE INVESTIGATION")
print("=" * 75)

print(
    invoices.to_string(
        index=False,
        formatters={
            "InvoiceValue": lambda x: f"£{x:,.2f}"
        }
    )
)

# Reconcile signed invoice totals by customer
summary = (
    invoices.groupby("CustomerID")
    .agg(
        InvoiceCount=("InvoiceNo", "nunique"),
        SignedValue=("InvoiceValue", "sum")
    )
)

print("\nCUSTOMER RECONCILIATION")
print(summary.to_string())

# Save results
output = (
    ROOT / "data" / "processed"
    / "customer_invoice_review.csv"
)

invoices.to_csv(output, index=False)

print("\nInvoice investigation saved successfully!")