
from pathlib import Path
import duckdb

# 1. Locate the project folder
ROOT = Path(__file__).resolve().parents[1]

SQL_FILE = ROOT / "sql" / "01_monthly_sales.sql"
DATA_FILE = ROOT / "data" / "processed" / "classified_sales.csv"

# 2. Confirm both files exist
if not SQL_FILE.exists():
    raise FileNotFoundError(f"SQL file not found: {SQL_FILE}")

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

# 3. Read the SQL query
query = SQL_FILE.read_text(encoding="utf-8")

query = query.replace(
    "data/processed/classified_sales.csv",
    DATA_FILE.as_posix()
)

# 4. Show the query for debugging
print("\nEXECUTING SQL QUERY")
print("=" * 60)
print(query)

# 5. Connect to DuckDB and run SQL
con = duckdb.connect(database=":memory:")

try:
    con.execute(query)

    # Retrieve the results after execution
    results = con.fetchdf()

finally:
    con.close()

# 6. Display monthly sales
print("\nMONTHLY MERCHANDISE SALES")
print("=" * 70)

print(
    results.to_string(
        index=False,
        formatters={
            "GrossMerchandiseValue": lambda x: f"£{x:,.2f}"
        }
    )
)

# 7. Validate monthly totals
monthly_total = results["GrossMerchandiseValue"].sum()

print(f"\nSum of monthly sales: £{monthly_total:,.2f}")

# 8. Save results
OUTPUT = ROOT / "data" / "processed" / "monthly_sales.csv"

results.to_csv(OUTPUT, index=False)

print("\nMonthly sales analysis completed successfully!")
print("Output saved to:", OUTPUT)