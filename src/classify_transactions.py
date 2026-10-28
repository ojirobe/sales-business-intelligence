from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "processed" / "valid_sales.csv"
OUTPUT = ROOT / "data" / "processed"

df = pd.read_csv(
    FILE,
    dtype={
        "InvoiceNo": "string",
        "StockCode": "string",
        "CustomerID": "string"
    },
    low_memory=False
)

# Standardize stock codes
df["StockCode"] = df["StockCode"].str.strip().str.upper()

# Create default category
df["TransactionCategory"] = "Merchandise"

# Explicit business classification rules
shipping_codes = ["DOT", "POST", "C2", "23444"]
marketplace_codes = ["AMAZONFEE"]
financial_charge_codes = ["BANK CHARGES"]
adjustment_codes = ["B"]
manual_codes = ["M"]
sample_codes = ["S"]

df.loc[
    df["StockCode"].isin(shipping_codes),
    "TransactionCategory"
] = "Shipping"

df.loc[
    df["StockCode"].isin(marketplace_codes),
    "TransactionCategory"
] = "Marketplace Charges"

df.loc[
    df["StockCode"].isin(adjustment_codes),
    "TransactionCategory"
] = "Accounting Adjustments"

df.loc[
    df["StockCode"].isin(manual_codes),
    "TransactionCategory"
] = "Unclassified Manual"

df.loc[
    df["StockCode"].isin(sample_codes),
    "TransactionCategory"
] = "Samples"

df.loc[
    df["StockCode"].isin(financial_charge_codes),
    "TransactionCategory"
] = "Financial Charges"

# Summarize by category
summary = (
    df.groupby("TransactionCategory")
    .agg(
        Records=("InvoiceNo", "size"),
        TotalValue=("Revenue", "sum")
    )
    .sort_values("TotalValue", ascending=False)
)

print("\nTRANSACTION CLASSIFICATION SUMMARY")
print("=" * 60)
print(
    summary.to_string(
        formatters={
            "TotalValue": lambda x: f"£{x:,.2f}"
        }
    )
)

print("\nTOTAL CLASSIFIED VALUE")
print(f"£{summary['TotalValue'].sum():,.2f}")

print("\nORIGINAL POSITIVE TRANSACTION VALUE")
print(f"£{df['Revenue'].sum():,.2f}")

# Verify classification preserves all records and value
assert summary["Records"].sum() == len(df)
assert abs(
    summary["TotalValue"].sum() - df["Revenue"].sum()
) < 0.01

# Export for future SQL and dashboards
df.to_csv(
    OUTPUT / "classified_sales.csv",
    index=False
)

summary.to_csv(
    OUTPUT / "transaction_category_summary.csv"
)

print("\nClassification files saved successfully!")
print("Validation checks passed.")