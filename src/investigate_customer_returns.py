from pathlib import Path
import pandas as pd

# STEP 1: Locate the original Excel dataset
ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "raw" / "Online Retail.xlsx"

# STEP 2: Load all transactions, including cancellations
df = pd.read_excel(FILE)

# STEP 3: Standardize customer identifiers
df["CustomerID"] = pd.to_numeric(
    df["CustomerID"], errors="coerce"
).astype("Int64")

# STEP 4: Calculate signed transaction values
df["LineValue"] = (
    df["Quantity"] * df["UnitPrice"]
)

# STEP 5: Investigate specific customers
customer_ids = [16446, 12346]

for customer_id in customer_ids:

    customer = df.loc[
        df["CustomerID"] == customer_id
    ].copy()

    print("\n" + "=" * 65)
    print(f"CUSTOMER {customer_id} TRANSACTION INVESTIGATION")
    print("=" * 65)

    print("\nTRANSACTIONS")
    print(
        customer[
            ["InvoiceNo", "StockCode", "Description",
             "Quantity", "UnitPrice", "LineValue"]
        ].to_string(index=False)
    )

    # Positive and negative transaction values
    positive = customer.loc[
        customer["LineValue"] > 0, "LineValue"
    ].sum()

    negative = customer.loc[
        customer["LineValue"] < 0, "LineValue"
    ].sum()

    net_value = customer["LineValue"].sum()

    print("\nCUSTOMER SUMMARY")
    print(f"Positive transactions: £{positive:,.2f}")
    print(f"Negative transactions: £{negative:,.2f}")
    print(f"Signed net value: £{net_value:,.2f}")

    print(
        "Unique invoices:",
        customer["InvoiceNo"].nunique()
    )

print("\nInvestigation completed successfully!")