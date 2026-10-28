from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "potential_full_cancellations.csv"
OUTPUT = ROOT / "data" / "processed"

# Load candidate purchase-cancellation pairs
df = pd.read_csv(
    INPUT,
    dtype={
        "InvoiceNo_Purchase": "string",
        "InvoiceNo_Return": "string"
    },
    low_memory=False
)

# Remove duplicate representations of exactly the same pair
df = df.drop_duplicates(
    subset=["InvoiceNo_Purchase", "InvoiceNo_Return"]
).copy()

# Count possible matches for each purchase
df["PurchaseMatchCount"] = (
    df.groupby("InvoiceNo_Purchase")["InvoiceNo_Return"]
    .transform("nunique")
)

# Count possible matches for each cancellation
df["ReturnMatchCount"] = (
    df.groupby("InvoiceNo_Return")["InvoiceNo_Purchase"]
    .transform("nunique")
)

# Retain only unambiguous one-to-one candidate matches
unique_matches = df.loc[
    (df["PurchaseMatchCount"] == 1)
    & (df["ReturnMatchCount"] == 1)
].copy()

# Set aside cases requiring further investigation
ambiguous = df.loc[
    (df["PurchaseMatchCount"] > 1)
    | (df["ReturnMatchCount"] > 1)
].copy()

# Check that invoices are not reused
assert unique_matches["InvoiceNo_Purchase"].is_unique
assert unique_matches["InvoiceNo_Return"].is_unique

print("\nCANCELLATION MATCH VALIDATION")
print("=" * 65)

print("Distinct candidate pairs:", len(df))
print("Unambiguous one-to-one pairs:", len(unique_matches))
print("Ambiguous candidate pairs:", len(ambiguous))

print("\nSAMPLE ONE-TO-ONE MATCHES")
print(
    unique_matches[
        [
            "CustomerID",
            "InvoiceNo_Purchase",
            "InvoiceNo_Return",
            "QuantityMagnitude"
        ]
    ].head(15).to_string(index=False)
)

# Check the previously investigated customer
print("\nCHECKING CUSTOMER 12346")
print(
    unique_matches.loc[
        unique_matches["CustomerID"] == 12346,
        [
            "CustomerID",
            "InvoiceNo_Purchase",
            "InvoiceNo_Return"
        ]
    ].to_string(index=False)
)

# Export results
unique_matches.to_csv(
    OUTPUT / "unique_cancellation_candidates.csv",
    index=False
)

ambiguous.to_csv(
    OUTPUT / "ambiguous_cancellation_candidates.csv",
    index=False
)

print("\nValidation files saved successfully!")