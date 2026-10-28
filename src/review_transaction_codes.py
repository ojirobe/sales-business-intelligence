
from pathlib import Path
import pandas as pd

# Locate the project directory
ROOT = Path(__file__).resolve().parents[1]

# Load qualifying sales data
FILE = ROOT / "data" / "processed" / "valid_sales.csv"

df = pd.read_csv(
    FILE,
    dtype={
        "InvoiceNo": "string",
        "StockCode": "string",
        "CustomerID": "string"
    },
    low_memory=False
)

# List codes that require investigation
codes = [
    "DOT", "M", "POST", "AMAZONFEE",
    "B", "DCGSSBOY", "DCGSSGIRL",
    "S", "PADS"
]

# Standardize stock codes
df["StockCode"] = df["StockCode"].str.strip().str.upper()

# Select relevant transactions
review = df[df["StockCode"].isin(codes)].copy()

print("\nTRANSACTION CODE REVIEW")
print("=" * 65)

# Show descriptions for each code
for code in codes:
    subset = review[review["StockCode"] == code]

    print(f"\nSTOCK CODE: {code}")
    print("-" * 65)

    if subset.empty:
        print("No matching records.")
        continue

    print("Records:", len(subset))
    print("Total value:", f"£{subset['Revenue'].sum():,.2f}")

    print("\nDescriptions:")
    print(subset["Description"].value_counts(dropna=False).head(10))

    print("\nSample transactions:")
    print(
        subset[
            ["InvoiceNo", "Description", "Quantity",
             "UnitPrice", "Revenue"]
        ].head(5).to_string(index=False)
    )

# Export the records for future documentation
OUTPUT = ROOT / "data" / "processed" / "transaction_code_review.csv"

review.to_csv(OUTPUT, index=False)

print("\nReview file saved successfully.")