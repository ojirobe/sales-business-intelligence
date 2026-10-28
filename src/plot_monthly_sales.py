from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# 1. Locate project files
ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = ROOT / "data" / "processed" / "monthly_sales.csv"
OUTPUT_DIR = ROOT / "dashboards"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 2. Load monthly sales results
df = pd.read_csv(DATA_FILE)

# 3. Convert month labels into dates
df["SalesMonth"] = pd.to_datetime(
    df["SalesMonth"],
    format="%Y-%m"
)

df = df.sort_values("SalesMonth")

# 4. Identify complete reporting months
# December 2011 contains only nine days
complete = df[
    df["SalesMonth"] < "2011-12-01"
].copy()

partial = df[
    df["SalesMonth"] >= "2011-12-01"
].copy()

# 5. Create chart
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    complete["SalesMonth"],
    complete["GrossMerchandiseValue"],
    marker="o",
    linewidth=2.5,
    label="Complete reporting months"
)

# Show incomplete December separately
ax.scatter(
    partial["SalesMonth"],
    partial["GrossMerchandiseValue"],
    marker="x",
    s=110,
    label="Incomplete December 2011"
)

# 6. Add labels and formatting
ax.set_title(
    "Monthly Merchandise Sales | Online Retail",
    fontsize=16,
    fontweight="bold",
    pad=18
)

ax.set_xlabel("Month")
ax.set_ylabel("Positive Merchandise Sales (£)")

ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(
        lambda value, _: f"£{value/1_000_000:.1f}M"
    )
)

ax.set_xticks(df["SalesMonth"])
ax.set_xticklabels(
    df["SalesMonth"].dt.strftime("%b %Y"),
    rotation=45,
    ha="right"
)

ax.grid(axis="y", alpha=0.3)
ax.legend()

# 7. Save chart
plt.tight_layout()

output_file = OUTPUT_DIR / "monthly_sales_trend.png"

plt.savefig(output_file, dpi=300, bbox_inches="tight")

print("Chart saved successfully!")
print("Location:", output_file)

# 8. Display chart
plt.show()