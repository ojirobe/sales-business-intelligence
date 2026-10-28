from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    ROOT / "data" / "processed"
    / "rfm_segments_preliminary.csv"
)

OUTPUT_DIR = ROOT / "dashboards"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load customer segmentation data
df = pd.read_csv(DATA_FILE)

# Count customers in each segment
segment_counts = (
    df["Segment"]
    .value_counts()
    .sort_values()
)

total_customers = len(df)

# Create the chart
fig, ax = plt.subplots(figsize=(11, 6))

bars = ax.barh(
    segment_counts.index,
    segment_counts.values
)

# Add customer count and percentage labels
for bar in bars:
    count = int(bar.get_width())
    percentage = count / total_customers * 100

    ax.text(
        count + 15,
        bar.get_y() + bar.get_height() / 2,
        f"{count:,} ({percentage:.1f}%)",
        va="center",
        fontsize=10
    )

ax.set_title(
    "Customer Segmentation | RFM Analysis",
    fontsize=16,
    fontweight="bold",
    pad=18
)

ax.set_xlabel("Number of Customers")
ax.set_ylabel("Customer Segment")

ax.set_xlim(0, segment_counts.max() * 1.25)
ax.grid(axis="x", alpha=0.25)

# Add a methodology note
fig.text(
    0.5, 0.01,
    "Preliminary RFM segments; partial and ambiguous "
    "cancellations not fully resolved.",
    ha="center",
    fontsize=9
)

plt.tight_layout(rect=[0, 0.05, 1, 1])

chart_file = (
    OUTPUT_DIR / "rfm_customer_segments.png"
)

plt.savefig(
    chart_file,
    dpi=300,
    bbox_inches="tight"
)

print("RFM visualization saved successfully!")
print("Location:", chart_file)

plt.show()