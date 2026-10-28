from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "processed" / "net_product_performance.csv"
OUTPUT = ROOT / "dashboards"

OUTPUT.mkdir(parents=True, exist_ok=True)

# Load and select the top 10 products
df = pd.read_csv(FILE, dtype={"StockCode": "string"})

top10 = (
    df.sort_values("NetSales", ascending=False)
      .head(10)
      .sort_values("NetSales", ascending=True)
)

# Create horizontal bar chart
fig, ax = plt.subplots(figsize=(12, 7))

bars = ax.barh(
    top10["ProductName"],
    top10["NetSales"]
)

# Add sales values beside the bars
for bar in bars:
    value = bar.get_width()
    ax.text(
        value + 1500,
        bar.get_y() + bar.get_height() / 2,
        f"£{value:,.0f}",
        va="center",
        fontsize=10
    )

ax.set_title(
    "Top 10 Products by Net Transaction Value",
    fontsize=16,
    fontweight="bold",
    pad=15
)

ax.set_xlabel("Net Transaction Value (£)")
ax.set_ylabel("Product")

ax.xaxis.set_major_formatter(
    ticker.FuncFormatter(
        lambda x, _: f"£{x / 1000:.0f}k"
    )
)

ax.set_xlim(0, top10["NetSales"].max() * 1.20)
ax.grid(axis="x", alpha=0.25)

plt.tight_layout()

# Save chart
chart_file = OUTPUT / "top_10_net_products.png"
plt.savefig(chart_file, dpi=300, bbox_inches="tight")

print("Chart saved successfully!")
print("Location:", chart_file)

plt.show()