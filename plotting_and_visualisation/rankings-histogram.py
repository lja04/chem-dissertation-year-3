import os
import pandas as pd
import matplotlib.pyplot as plt

# Define folder with CSV files
rankings_folder = "rankings"

# Verify folder exists
if not os.path.exists(rankings_folder):
    raise FileNotFoundError(f"Folder not found: {rankings_folder}")

# Store all rank changes
rank_changes = []
failed_files = []

# Loop through all CSV files
for filename in os.listdir(rankings_folder):
    if filename.endswith(".csv"):
        try:
            molecule_id = os.path.splitext(filename)[0]
            file_path = os.path.join(rankings_folder, filename)
            
            # Load CSV
            df = pd.read_csv(file_path)
            
            # Verify required columns exist
            if not all(col in df.columns for col in ["new rank", "original rank"]):
                print(f"Missing columns in {filename}: {df.columns}")
                failed_files.append(filename)
                continue
            
            # Compute rank change
            df["RankChange"] = df["new rank"] - df["original rank"]
            df["Molecule"] = molecule_id
            
            # Add to list
            rank_changes.extend(df["RankChange"].tolist())
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            failed_files.append(filename)

if not rank_changes:
    raise ValueError("No rank change data found in any files")

# Convert to DataFrame for plotting
df_changes = pd.DataFrame(rank_changes, columns=["RankChange"])

# Plot histogram
plt.figure(figsize=(8, 5))
min_change = int(df_changes["RankChange"].min())
max_change = int(df_changes["RankChange"].max())
bins = range(min_change - 1, max_change + 2)
plt.hist(df_changes["RankChange"], bins=bins, edgecolor='black', color='b')
plt.xlabel("Change in Rank Position")
plt.ylabel("Number of Structures")

# Set x-axis limits to exclude zero (shift slightly to the left/right)
plt.xlim(left=min_change - 0.5, right=max_change + 0.5)

plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

# Save plot
output_path = os.path.join(rankings_folder, "rank_change_histogram.png")
plt.savefig(output_path, dpi=300)
print(f"Plot saved to {output_path}")

plt.show()

# Print any failed files
if failed_files:
    print("\nFailed to process these files:")
    for f in failed_files:
        print(f)