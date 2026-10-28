
from pathlib import Path
import pandas as pd

# Locate the project
ROOT = Path(__file__).resolve().parents[1]

CSV_FILE = ROOT / "data" / "processed" / "classified_sales.csv"
PARQUET_FILE = ROOT / "data" / "processed" / "classified_sales.parquet"

# Check the original file
if not CSV_FILE.exists():
    raise FileNotFoundError(
        f"CSV file not found: {CSV_FILE}"
    )

print("Reading original CSV...")

# Preserve identifiers as text
df = pd.read_csv(
    CSV_FILE,
    dtype={
        "InvoiceNo": "string",
        "StockCode": "string",
        "CustomerID": "string"
    },
    low_memory=False
)

original_rows = len(df)

print(f"Original rows: {original_rows:,}")

# Convert to compressed Parquet
print("Converting to Parquet...")

df.to_parquet(
    PARQUET_FILE,
    engine="pyarrow",
    compression="zstd",
    index=False
)

# Validate the saved file
print("Validating Parquet file...")

parquet_df = pd.read_parquet(
    PARQUET_FILE,
    engine="pyarrow"
)

parquet_rows = len(parquet_df)

assert original_rows == parquet_rows, (
    "Row count mismatch during conversion."
)

# Check that every column and value was preserved
pd.testing.assert_frame_equal(
    df,
    parquet_df,
    check_dtype=True
)

# Compare storage sizes
csv_size = CSV_FILE.stat().st_size / (1024 ** 2)
parquet_size = PARQUET_FILE.stat().st_size / (1024 ** 2)

reduction = (
    1 - parquet_size / csv_size
) * 100

print("\nDATA CONVERSION COMPLETED")
print("=" * 55)

print(f"Original CSV rows: {original_rows:,}")
print(f"Parquet rows: {parquet_rows:,}")
print(f"CSV size: {csv_size:.2f} MB")
print(f"Parquet size: {parquet_size:.2f} MB")
print(f"Size reduction: {reduction:.2f}%")

print("\nAll data validation checks passed!")
print(f"File saved to: {PARQUET_FILE}")