
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "raw" / "Online Retail.xlsx"

df = pd.read_excel(FILE)

# Identify all rows belonging to duplicate groups
duplicate_groups = df[
    df.duplicated(keep=False)
].copy()

# Sort them for easier comparison
duplicate_groups = duplicate_groups.sort_values(
    by=["InvoiceNo", "StockCode"]
)

print("\nDUPLICATE INVESTIGATION")
print("-" * 50)

print("Original records:", len(df))

print(
    "Additional repeated rows:",
    df.duplicated().sum()
)

print(
    "Rows belonging to duplicate groups:",
    len(duplicate_groups)
)

print("\nSAMPLE DUPLICATE GROUPS")
print(duplicate_groups.head(20).to_string(index=False))

print("\nINVOICES WITH DUPLICATE RECORDS")
print(
    duplicate_groups["InvoiceNo"]
    .value_counts()
    .head(10)
)

# Export duplicate groups for manual inspection
output = ROOT / "data" / "processed" / "duplicate_review.csv"
output.parent.mkdir(parents=True, exist_ok=True)

duplicate_groups.to_csv(output, index=False)

print("\nDuplicate review file created.")