from pathlib import Path
import duckdb

# STEP 1: Locate the project files
ROOT = Path(__file__).resolve().parents[1]

SQL_FILE = ROOT / "sql" / "03_customer_analysis.sql"
DATA_FILE = ROOT / "data" / "processed" / "classified_sales.csv"

# STEP 2: Check that both files exist
if not SQL_FILE.exists():
    raise FileNotFoundError(f"SQL file missing: {SQL_FILE}")

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset missing: {DATA_FILE}")

# STEP 3: Read the SQL query
query = SQL_FILE.read_text(encoding="utf-8")
if not query.strip():
    raise ValueError(
        "The customer analysis SQL file is empty. "
        "Please add the SQL query and save the file."
    )

query = query.replace(
    "data/processed/classified_sales.csv",
    DATA_FILE.as_posix()
)

# STEP 4: Connect to DuckDB and execute
con = duckdb.connect(database=":memory:")

try:
    # Execute only the SELECT query and retrieve its results
    print("\nSQL QUERY BEING EXECUTED:")
    print("=" * 60)
    print(repr(query))
    print("=" * 60)
    results = con.sql(query).df()
finally:
    con.close()

# STEP 5: Display customer analysis
print("\nCUSTOMER BEHAVIOUR ANALYSIS")
print("=" * 85)

print(f"Identifiable customers: {len(results):,}")

print("\nTOP 10 CUSTOMERS BY GROSS PURCHASE VALUE")

print(
    results.head(10).to_string(
        index=False,
        formatters={
            "GrossPurchaseValue": lambda x: f"£{x:,.2f}",
            "AverageOrderValue": lambda x: f"£{x:,.2f}"
        }
    )
)

# STEP 6: Save results
OUTPUT = ROOT / "data" / "processed" / "customer_analysis.csv"

results.to_csv(OUTPUT, index=False)

print("\nCustomer analysis completed successfully!")
print("Saved to:", OUTPUT)