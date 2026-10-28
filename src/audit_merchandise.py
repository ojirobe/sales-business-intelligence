from pathlib import Path
import pandas as pd

# 1. Locate the classified dataset
ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "processed" / "classified_sales.csv"

df = pd.read_csv(
    FILE,
    dtype={
        "InvoiceNo": "string",
        "StockCode": "string",
        "CustomerID": "string"
    },
    low_memory=False
)

# 2. Select provisionally classified merchandise
merchandise = df.loc[
    df["TransactionCategory"] == "Merchandise"
].copy()

# 3. Define terms that may indicate non-product entries
keywords = (
    r"POSTAGE|CARRIAGE|SHIPPING|BANK CHARGE|"
    r"DISCOUNT|ADJUST|BAD DEBT|FEE|"
    r"MANUAL|SAMPLE|COMMISSION"
)

# 4. Find descriptions requiring review
review_mask = merchandise["Description"].str.contains(
    keywords,
    case=False,
    regex=True,
    na=False
)

candidates = merchandise.loc[review_mask].copy()

# 5. Summarize suspicious descriptions
summary = (
    candidates.groupby(
        ["StockCode", "Description"],
        dropna=False
    )
    .agg(
        Records=("Revenue", "size"),
        TotalValue=("Revenue", "sum")
    )
    .reset_index()
    .sort_values("TotalValue", ascending=False)
)

print("\nMERCHANDISE CLASSIFICATION AUDIT")
print("=" * 65)

print(f"Provisional merchandise rows: {len(merchandise):,}")
print(f"Rows flagged for review: {len(candidates):,}")

print("\nTOP DESCRIPTIONS FOR MANUAL REVIEW")
print(
    summary.head(30).to_string(
        index=False,
        formatters={
            "TotalValue": lambda x: f"£{x:,.2f}"
        }
    )
)

# 6. Export for review
OUTPUT = (
    ROOT / "data" / "processed"
    / "merchandise_audit_candidates.csv"
)

candidates.to_csv(OUTPUT, index=False)

print("\nAudit candidates exported successfully.")
print("No additional records have been deleted.")