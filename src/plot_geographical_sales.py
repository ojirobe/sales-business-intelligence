from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# 1. Locate project files
ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "processed" / "geographical_sales.csv"
OUTPUT = ROOT / "dashboards"

OUTPUT.mkdir(parents=True, exist_ok=True)

# 2. Load geographical sales results
df = pd.read_csv(FILE)

# 3. Calculate UK and international sales
total_sales = df["GrossMerchandiseValue"].sum()

uk_sales = df.loc[
    df["Country"] == "United Kingdom",
    "GrossMerchandiseValue"
].sum()

uk_share = uk_sales / total_sales * 100

# 4. Select the top 10 markets outside the UK
international = (
    df.loc[df["Country"] != "United Kingdom"]
    .nlargest(10, "GrossMerchandiseValue")
    .sort_values("GrossMerchandiseValue")
)

# 5. Create a horizontal bar chart
fig, ax = plt.subplots(figsize=(12, 7))

bars = ax.barh(
    international["Country"],
    international["GrossMerchandiseValue"]
)

# 6. Label each bar
for bar in bars:
    value = bar.get_width()

    ax.text(
        value + 3500,
        bar.get_y() + bar.get_height() / 2,
        f"£{value:,.0f}",
        va="center",
        fontsize=10
    )

# 7. Format the chart
ax.set_title(
    "Top 10 International Markets by Merchandise Sales",
    fontsize=16,
    fontweight="bold",
    pad=18
)

ax.set_xlabel("Positive Merchandise Sales (£)")
ax.set_ylabel("Country")

ax.xaxis.set_major_formatter(
    ticker.FuncFormatter(
        lambda value, _: f"£{value / 1000:.0f}k"
    )
)

ax.set_xlim(
    0,
    international["GrossMerchandiseValue"].max() * 1.25
)

ax.grid(axis="x", alpha=0.25)

# 8. Include UK market context
fig.text(
    0.5, 0.025,
    f"UK accounts for {uk_share:.2f}% of total positive "
    "merchandise sales. Figures exclude returns.",
    ha="center",
    fontsize=10
)

# 9. Save and display
plt.tight_layout(rect=[0, 0.06, 1, 1])

chart_file = OUTPUT / "international_sales.png"

plt.savefig(
    chart_file,
    dpi=300,
    bbox_inches="tight"
)

print("International sales chart saved successfully!")
print("Location:", chart_file)

plt.show()