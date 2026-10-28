
from pathlib import Path
import pandas as pd

# 1. Locate and load the original dataset
ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "raw" / "Online Retail.xlsx"

df = pd.read_excel(FILE)

print("=" * 60)
print("SALES DATA QUALITY ASSESSMENT")
print("=" * 60)

# 2. Investigate negative and zero quantities
negative_qty = df[df["Quantity"] < 0]
zero_qty = df[df["Quantity"] == 0]

print("\nNEGATIVE QUANTITIES:", len(negative_qty))
print("ZERO QUANTITIES:", len(zero_qty))

# 3. Investigate negative and zero prices
negative_prices = df[df["UnitPrice"] < 0]
zero_prices = df[df["UnitPrice"] == 0]

print("\nNEGATIVE PRICES:", len(negative_prices))
print("ZERO PRICES:", len(zero_prices))

# 4. Identify cancellation invoice numbers
cancelled = df[
    df["InvoiceNo"].astype(str).str.startswith("C")
]

print("\nCANCELLATION RECORDS:", len(cancelled))

# 5. Investigate incomplete customer information
print("\nMISSING CUSTOMER IDS:")
print(df["CustomerID"].isna().sum())

# 6. Investigate missing product descriptions
print("\nMISSING PRODUCT DESCRIPTIONS:")
print(df["Description"].isna().sum())

# 7. Count exactly repeated rows
print("\nEXACT DUPLICATE ROWS:")
print(df.duplicated().sum())

# 8. Check transaction date range
print("\nEARLIEST TRANSACTION:")
print(df["InvoiceDate"].min())

print("\nLATEST TRANSACTION:")
print(df["InvoiceDate"].max())

# 9. Display sample cancellation transactions
print("\nSAMPLE CANCELLATIONS:")
print(cancelled.head(10).to_string(index=False))

# 10. Display negative-price records
print("\nNEGATIVE PRICE RECORDS:")
print(negative_prices.head(10).to_string(index=False))