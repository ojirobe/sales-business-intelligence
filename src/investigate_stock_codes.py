
from pathlib import Path
import pandas as pd

# STEP 1: Locate our project and cleaned sales dataset
ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "processed" / "valid_sales.csv"

# STEP 2: Load the cleaned dataset
df = pd.read_csv(
    FILE,
    dtype={
        "InvoiceNo": "string",
        "StockCode": "string",
        "CustomerID": "string"
    },
    low_memory=False
)

print("=" * 60)
print("SPECIAL STOCK CODE INVESTIGATION")
print("=" * 60)

# STEP 3: Standardize stock codes
df["StockCode"] = df["StockCode"].str.strip().str.upper()

# STEP 4: Identify codes containing letters or special characters
special_mask = df["StockCode"].str.contains(
    r"[^0-9]",
    regex=True,
    na=False
)

special = df.loc[special_mask].copy()

print("\nTOTAL QUALIFYING SALES ROWS:", len(df))
print("ROWS WITH NON-NUMERIC STOCK CODES:", len(special))

# STEP 5: Summarize special stock codes
summary = (
    special.groupby("StockCode")
    .agg(
        Records=("StockCode", "size"),
        TotalValue=("Revenue", "sum"),
        UniqueDescriptions=("Description", "nunique")
    )
    .sort_values("TotalValue", ascending=False)
)

print("\nSPECIAL STOCK CODE SUMMARY")
print("-" * 60)
print(summary.to_string())

# STEP 6: Show descriptions for classification
examples = (
    special[
        ["StockCode", "Description", "Quantity",
         "UnitPrice", "Revenue"]
    ]
    .drop_duplicates()
)

print("\nEXAMPLE DESCRIPTIONS")
print("-" * 60)
print(examples.head(40).to_string(index=False))

# STEP 7: Export results for review
OUTPUT_DIR = ROOT / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

summary.to_csv(
    OUTPUT_DIR / "special_stock_code_summary.csv"
)

special.to_csv(
    OUTPUT_DIR / "special_stock_codes.csv",
    index=False
)

print("\nFiles successfully created:")
print("1. special_stock_code_summary.csv")
print("2. special_stock_codes.csv")

print("\nInvestigation completed successfully!")