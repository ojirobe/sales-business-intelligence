from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "raw" / "Online Retail.xlsx"

df = pd.read_excel(FILE)

df["InvoiceNo"] = df["InvoiceNo"].astype("string").str.strip()
df["CustomerID"] = pd.to_numeric(
    df["CustomerID"], errors="coerce"
).astype("Int64")

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["LineValue"] = df["Quantity"] * df["UnitPrice"]

# Verified matching invoice pairs from our investigation
verified_pairs = {
    "541431": "C541433",
    "581483": "C581484"
}

# Validate that each pair has equal and opposite values
for purchase_no, cancellation_no in verified_pairs.items():
    purchase = df[df["InvoiceNo"] == purchase_no]
    cancellation = df[df["InvoiceNo"] == cancellation_no]

    assert not purchase.empty
    assert not cancellation.empty

    assert (
        purchase["CustomerID"].dropna().unique().tolist()
        == cancellation["CustomerID"].dropna().unique().tolist()
    )

    assert abs(
        purchase["LineValue"].sum()
        + cancellation["LineValue"].sum()
    ) < 0.01

# These purchases are verified as fully reversed
cancelled_purchases = set(verified_pairs.keys())

snapshot = pd.Timestamp("2011-12-10")

print("\nVALIDATED CUSTOMER RFM EXAMPLES")
print("=" * 65)

for customer_id in [12346, 16446]:
    customer = df[df["CustomerID"] == customer_id].copy()

    valid = customer[
        (customer["Quantity"] > 0)
        & (customer["UnitPrice"] > 0)
        & (~customer["InvoiceNo"].isin(cancelled_purchases))
        & (~customer["InvoiceNo"].str.startswith("C", na=False))
    ].copy()

    # Signed monetary activity from all known transactions
    net_value = customer["LineValue"].sum()

    print(f"\nCustomer: {customer_id}")
    print(f"Signed net value: £{net_value:,.2f}")

    if valid.empty:
        print("Retained purchase invoices: 0")
        print("Recency: Not applicable")
        print("Status: No verified retained purchase")
    else:
        last_purchase = valid["InvoiceDate"].max()
        frequency = valid["InvoiceNo"].nunique()
        recency = (snapshot - last_purchase).days

        print(f"Retained purchase invoices: {frequency}")
        print(f"Last retained purchase: {last_purchase}")
        print(f"Recency: {recency} days")

print("\nValidation completed successfully!")