from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "Online Retail.xlsx"
OUTPUT = ROOT / "data" / "processed"

# Load all original transactions, including returns
df = pd.read_excel(RAW)

df["StockCode"] = (
    df["StockCode"].astype("string").str.strip().str.upper()
)
df["InvoiceNo"] = (
    df["InvoiceNo"].astype("string").str.strip()
)

# Codes identified during our earlier investigations
non_merchandise = {
    "DOT", "POST", "C2", "23444",
    "AMAZONFEE", "B", "BANK CHARGES",
    "M", "S"
}

# Restrict to merchandise candidates
df = df[
    ~df["StockCode"].isin(non_merchandise)
    & (df["UnitPrice"] > 0)
    & df["Description"].notna()
].copy()

# Calculate signed transaction value
df["LineValue"] = df["Quantity"] * df["UnitPrice"]

# Positive sales and negative transactions
df["PositiveSales"] = df["LineValue"].clip(lower=0)
df["ReturnsValue"] = df["LineValue"].clip(upper=0)

# Aggregate by product code
summary = (
    df.groupby("StockCode", as_index=False)
    .agg(
        ProductName=("Description", "first"),
        GrossSales=("PositiveSales", "sum"),
        Returns=("ReturnsValue", "sum"),
        NetSales=("LineValue", "sum"),
        NetUnits=("Quantity", "sum")
    )
)

summary = summary.sort_values(
    "NetSales", ascending=False
)

print("\nTOP 10 PRODUCTS BY NET TRANSACTION VALUE")
print("=" * 85)

print(
    summary.head(10).to_string(
        index=False,
        formatters={
            "GrossSales": lambda x: f"£{x:,.2f}",
            "Returns": lambda x: f"£{x:,.2f}",
            "NetSales": lambda x: f"£{x:,.2f}"
        }
    )
)

print("\nCHECKING UNUSUAL PRODUCTS")
print(
    summary[
        summary["StockCode"].isin(["23843", "23166"])
    ].to_string(index=False)
)

# Preserve detailed results
OUTPUT.mkdir(parents=True, exist_ok=True)

summary.to_csv(
    OUTPUT / "net_product_performance.csv",
    index=False
)

print("\nNet product analysis saved successfully!")