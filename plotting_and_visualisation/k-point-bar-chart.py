import matplotlib.pyplot as plt
import pandas as pd

# Data
data = {
    "Refcode": ["IZIJOQ", "ZUMKUN"],
    "Rank at k=0.30 Å⁻¹": [46, 9],
    "Rank at k=0.12 Å⁻¹": [25, 9]
}

# Create DataFrame
df = pd.DataFrame(data)

# Plot setup
fig, ax = plt.subplots(figsize=(6, 5))
bar_width = 0.35
x = range(len(df))

# Bar plots (removed edgecolor and linewidth)
bars1 = ax.bar([i - bar_width/2 for i in x], df["Rank at k=0.30 Å⁻¹"], 
               width=bar_width, label='k = 0.30 Å⁻¹')

bars2 = ax.bar([i + bar_width/2 for i in x], df["Rank at k=0.12 Å⁻¹"], 
               width=bar_width, label='k = 0.12 Å⁻¹')

# Labels and formatting
ax.set_ylabel("Observed Structure Rank")
ax.set_xticks(x)
ax.set_xticklabels(df["Refcode"])
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

# Save and show
plt.tight_layout()
output_path = "kpoint_rank_comparison_clean.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Plot saved as {output_path}")
plt.show()