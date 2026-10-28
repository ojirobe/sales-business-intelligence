
from pathlib import Path
import pandas as pd

# 1. Set project file locations
ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "Online Retail.xlsx"
OUTPUT_DIR = ROOT / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 2. Read the original data
df = pd.read_excel(RAW_FILE)

print("Original rows:", len(df))

# 3. Standardize selected column types
df["InvoiceNo"] = df["InvoiceNo"].astype("string").str.strip()
df["StockCode"] = df["StockCode"].astype("string").str.strip()
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# 4. Create data-quality flags
df["IsCancellation"] = df["InvoiceNo"].str.startswith(
    "C", na=False
)

df["IsNegativeQuantity"] = df["Quantity"] < 0
df["IsNonPositivePrice"] = df["UnitPrice"] <= 0
df["MissingCustomerID"] = df["CustomerID"].isna()
df["IsExactDuplicate"] = df.duplicated(
    subset=[
        "InvoiceNo", "StockCode", "Description",
        "Quantity", "InvoiceDate", "UnitPrice",
        "CustomerID", "Country"
    ],
    keep="first"
)

# 5. Define qualifying merchandise sales
sales_mask = (
    (df["Quantity"] > 0)
    & (df["UnitPrice"] > 0)
    & (~df["IsCancellation"])
)

sales = df.loc[sales_mask].copy()

# 6. Calculate line-level sales value
sales["Revenue"] = (
    sales["Quantity"] * sales["UnitPrice"]
)

# 7. Create the customer analysis subset
customer_sales = sales.loc[
    sales["CustomerID"].notna()
].copy()

# 8. Keep excluded records for review
excluded = df.loc[~sales_mask].copy()

# 9. Save the datasets as CSV
sales.to_csv(
    OUTPUT_DIR / "valid_sales.csv", index=False
)

customer_sales.to_csv(
    OUTPUT_DIR / "customer_sales.csv", index=False
)

excluded.to_csv(
    OUTPUT_DIR / "excluded_records.csv", index=False
)

# 10. Print validation summary
print("\nCLEANING SUMMARY")
print("-" * 45)
print("Valid sales rows:", len(sales))
print("Customer sales rows:", len(customer_sales))
print("Excluded rows:", len(excluded))
print("Duplicate flags:", df["IsExactDuplicate"].sum())

print("\nGROSS MERCHANDISE SALES")
print(f"£{sales['Revenue'].sum():,.2f}")

print("\nVALIDATION")
assert len(sales) + len(excluded) == len(df)
assert (sales["Quantity"] > 0).all()
assert (sales["UnitPrice"] > 0).all()

print("All basic validation checks passed.")