import pandas as pd
import matplotlib.pyplot as plt

# Load the consolidated CSV data
df = pd.read_csv("observed-structures-from-csvs.csv")  # Replace with your actual file path or variable

# Verify required columns exist
if not all(col in df.columns for col in ["new rank", "original rank"]):
    raise ValueError("Input data is missing required columns ('new rank' and/or 'original rank')")

# Compute rank change
df["RankChange"] = df["new rank"] - df["original rank"]
rank_changes = df["RankChange"].tolist()

# Plot histogram
plt.figure(figsize=(8, 5))
df_changes = pd.DataFrame(rank_changes, columns=["RankChange"])

# Set bins dynamically
min_change = df_changes["RankChange"].min()
max_change = df_changes["RankChange"].max()
bins = range(int(min_change) - 1, int(max_change) + 2)

plt.hist(df_changes["RankChange"], bins=bins, edgecolor='black')
plt.xlabel("Change in Rank Position")
plt.ylabel("Number of Structures")

plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

# Save plot
output_path = "rank_change_histogram_observed.png"
plt.savefig(output_path, dpi=300)
print(f"Plot saved to {output_path}")
plt.show()