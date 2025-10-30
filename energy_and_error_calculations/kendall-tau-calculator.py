import os
import pandas as pd
from scipy.stats import kendalltau

# Path to your ranking CSVs
rankings_folder = "rankings"

# Store results
tau_results = []

# Loop through all CSV files
for filename in os.listdir(rankings_folder):
    if filename.endswith(".csv"):
        # Remove '-ranking.csv' and keep just the base name
        molecule_id = filename.replace("-ranking.csv", "")
        file_path = os.path.join(rankings_folder, filename)

        df = pd.read_csv(file_path)

        # Sort by static rank and assign position
        static_order = df.sort_values("original rank")["id"].tolist()
        corrected_order = df.sort_values("new rank")["id"].tolist()

        # Build rank vectors (same length, same elements)
        structure_ids = df["id"].tolist()
        static_ranks = [static_order.index(s) for s in structure_ids]
        corrected_ranks = [corrected_order.index(s) for s in structure_ids]

        # Calculate Kendall τ
        tau, _ = kendalltau(static_ranks, corrected_ranks)

        # Save result
        tau_results.append({
            "Molecule": molecule_id,
            "Kendall_tau": tau
        })

# Convert to DataFrame, sort alphabetically, and save
df_tau = pd.DataFrame(tau_results)
df_tau = df_tau.sort_values("Molecule")  # Sort alphabetically
df_tau.to_csv("kendall_tau_results.csv", index=False)
print(df_tau.head())