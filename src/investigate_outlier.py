from pathlib import Path
import pandas as pd

# Locate the original dataset
ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "raw" / "Online Retail.xlsx"

df = pd.read_excel(FILE)

# Standardize identifiers
df["StockCode"] = df["StockCode"].astype("string").str.strip()
df["InvoiceNo"] = df["InvoiceNo"].astype("string").str.strip()

# Investigate the unusual product
product = df[df["StockCode"] == "23843"].copy()

product["LineValue"] = (
    product["Quantity"] * product["UnitPrice"]
)

print("\nUNUSUAL PRODUCT TRANSACTION INVESTIGATION")
print("=" * 65)

print("\nALL TRANSACTIONS FOR STOCK CODE 23843")
print(
    product[
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice", "LineValue",
         "InvoiceDate", "CustomerID"]
    ].to_string(index=False)
)

print("\nSUMMARY")
print("Number of records:", len(product))
print("Positive quantity:", product.loc[
    product["Quantity"] > 0, "Quantity"
].sum())

print("Negative quantity:", product.loc[
    product["Quantity"] < 0, "Quantity"
].sum())

print("Net quantity:", product["Quantity"].sum())

print(
    "Signed transaction value:",
    f"£{product['LineValue'].sum():,.2f}"
)

# Investigate other unusually large quantities
large = df.loc[
    df["Quantity"].abs() >= 10000
].copy()

print("\nOTHER EXTREME QUANTITY TRANSACTIONS")
print(
    large[
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice"]
    ].to_string(index=False)
)