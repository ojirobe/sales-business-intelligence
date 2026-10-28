from pathlib import Path
import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

SQL_FILE = ROOT / "sql" / "04_geographical_sales.sql"
DATA_FILE = ROOT / "data" / "processed" / "classified_sales.csv"

# Read the SQL query
query = SQL_FILE.read_text(encoding="utf-8")

if not query.strip():
    raise ValueError("The SQL file is empty.")

# Replace the relative dataset path
query = query.replace(
    "data/processed/classified_sales.csv",
    DATA_FILE.as_posix()
)

# Execute SQL
with duckdb.connect(database=":memory:") as con:
    results = con.sql(query).df()

# Calculate each country's percentage
total = results["GrossMerchandiseValue"].sum()

results["SalesSharePercent"] = (
    results["GrossMerchandiseValue"] / total * 100
).round(2)

# Display results
print("\nGEOGRAPHICAL SALES ANALYSIS")
print("=" * 85)

print("\nTOP 15 COUNTRIES")
print(
    results.head(15).to_string(
        index=False,
        formatters={
            "GrossMerchandiseValue":
                lambda x: f"£{x:,.2f}",
            "SalesSharePercent":
                lambda x: f"{x:.2f}%"
        }
    )
)

# Validate total against our merchandise KPI
expected_total = 10_270_918.87

assert abs(total - expected_total) < 0.10, (
    f"Reconciliation failed: £{total:,.2f}"
)

# Save for dashboards
OUTPUT = (
    ROOT / "data" / "processed"
    / "geographical_sales.csv"
)

results.to_csv(OUTPUT, index=False)

print("\nGeographical analysis saved successfully!")
print(f"Reconciled total: £{total:,.2f}")