from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]

SQL_FILE = ROOT / "sql" / "02_product_performance.sql"
DATA_FILE = ROOT / "data" / "processed" / "classified_sales.csv"

query = SQL_FILE.read_text(encoding="utf-8")

query = query.replace(
    "data/processed/classified_sales.csv",
    DATA_FILE.as_posix()
)

with duckdb.connect(database=":memory:") as con:
    con.execute(query)
    results = con.fetchdf()

print("\nTOP 10 PRODUCTS BY POSITIVE SALES VALUE")
print("=" * 85)

print(
    results.to_string(
        index=False,
        formatters={
            "GrossSalesValue": lambda x: f"£{x:,.2f}"
        }
    )
)

OUTPUT = ROOT / "data" / "processed" / "top_products.csv"
results.to_csv(OUTPUT, index=False)

print("\nProduct performance results saved successfully!")