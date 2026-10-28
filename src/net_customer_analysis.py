from pathlib import Path
import pandas as pd

# 1. Locate the project and dataset
ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "Online Retail.xlsx"
OUTPUT = ROOT / "data" / "processed"

# 2. Read original transactions including cancellations
df = pd.read_excel(RAW_FILE)

# 3. Standardize identifiers
df["StockCode"] = (
    df["StockCode"].astype("string").str.strip().str.upper()
)

df["InvoiceNo"] = (
    df["InvoiceNo"].astype("string").str.strip()
)

df["CustomerID"] = pd.to_numeric(
    df["CustomerID"], errors="coerce"
).astype("Int64")

# 4. Apply reviewed non-merchandise exclusions
non_merchandise = {
    "DOT", "POST", "C2", "23444",
    "AMAZONFEE", "B", "BANK CHARGES",
    "M", "S"
}

sales = df.loc[
    df["CustomerID"].notna()
    & ~df["StockCode"].isin(non_merchandise)
    & (df["UnitPrice"] > 0)
    & df["Description"].notna()
].copy()

# 5. Calculate signed monetary values
sales["LineValue"] = (
    sales["Quantity"] * sales["UnitPrice"]
)

sales["PositiveValue"] = sales["LineValue"].clip(lower=0)
sales["NegativeValue"] = sales["LineValue"].clip(upper=0)

# 6. Summarize by customer
summary = (
    sales.groupby("CustomerID")
    .agg(
        GrossPurchases=("PositiveValue", "sum"),
        NegativeTransactions=("NegativeValue", "sum"),
        NetValue=("LineValue", "sum"),
        NetUnits=("Quantity", "sum")
    )
    .reset_index()
)

# 7. Sort customers by signed net value
summary = summary.sort_values(
    "NetValue", ascending=False
)

print("\nCUSTOMERS RANKED BY NET TRANSACTION VALUE")
print("=" * 85)

print(
    summary.head(10).to_string(
        index=False,
        formatters={
            "GrossPurchases": lambda x: f"£{x:,.2f}",
            "NegativeTransactions": lambda x: f"£{x:,.2f}",
            "NetValue": lambda x: f"£{x:,.2f}"
        }
    )
)

# 8. Verify important customers
print("\nPREVIOUSLY INVESTIGATED CUSTOMERS")
print(
    summary[
        summary["CustomerID"].isin([16446, 12346])
    ].to_string(index=False)
)

# 9. Validate arithmetic
assert (
    summary["GrossPurchases"]
    + summary["NegativeTransactions"]
    - summary["NetValue"]
).abs().max() < 0.01

# 10. Save results
OUTPUT.mkdir(parents=True, exist_ok=True)

summary.to_csv(
    OUTPUT / "net_customer_analysis.csv",
    index=False
)

print("\nCustomer net analysis completed successfully!")