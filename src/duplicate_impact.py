
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "processed" / "valid_sales.csv"

# Load qualifying sales
df = pd.read_csv(
    FILE,
    dtype={
        "InvoiceNo": "string",
        "StockCode": "string"
    },
    low_memory=False
)

# Calculate revenue with all qualifying records
revenue_original = df["Revenue"].sum()

# Remove exact duplicates based on original business fields
business_columns = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
]

deduplicated = df.drop_duplicates(
    subset=business_columns, keep="first"
)

revenue_deduplicated = deduplicated["Revenue"].sum()

# Compare the scenarios
difference = revenue_original - revenue_deduplicated
percentage = difference / revenue_original * 100

print("\nDUPLICATE SENSITIVITY ANALYSIS")
print("-" * 50)

print(f"Original sales rows: {len(df):,}")
print(f"After deduplication: {len(deduplicated):,}")

print(f"\nRevenue with repeated rows: £{revenue_original:,.2f}")
print(f"Revenue without repeated rows: £{revenue_deduplicated:,.2f}")

print(f"\nDifference: £{difference:,.2f}")
print(f"Percentage difference: {percentage:.2f}%")