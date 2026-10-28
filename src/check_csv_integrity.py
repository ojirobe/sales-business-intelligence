
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILE = ROOT / "data" / "processed" / "classified_sales.csv"

# Read the file in binary mode
with open(FILE, "rb") as file:
    content = file.read()

# Count null bytes
null_count = content.count(b"\x00")

print("\nCSV INTEGRITY CHECK")
print("=" * 50)
print(f"File size: {len(content):,} bytes")
print(f"Null bytes found: {null_count:,}")

if null_count > 0:
    print("\nWARNING: The CSV contains null bytes.")
    print("The processed file should be regenerated.")
else:
    print("\nNo null bytes were found.")
    print("Further CSV parsing checks may be required.")