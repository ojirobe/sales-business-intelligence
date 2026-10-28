from pathlib import Path
import pandas as pd

# Locate the dataset relative to this Python script
project_root = Path(__file__).resolve().parents[1]
file_path = project_root / "data" / "raw" / "Online Retail.xlsx"

# Read the Excel dataset into a pandas DataFrame
df = pd.read_excel(file_path)

# Examine the dataset
print("\nFIRST FIVE RECORDS")
print(df.head())

print("\nDATASET DIMENSIONS")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print("\nCOLUMN NAMES")
print(df.columns.tolist())

print("\nDATA TYPES")
print(df.dtypes)

print("\nMISSING VALUES")
print(df.isna().sum())

print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

print("\nQUANTITY AND PRICE SUMMARY")
print(df[["Quantity", "UnitPrice"]].describe())