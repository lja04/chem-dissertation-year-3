import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kendalltau

# Configuration
rankings_folder = "rankings"
output_csv = "kendall_tau_results.csv"
output_plot = "kendall_tau_distribution.png"
tau_threshold = 0.8  # Threshold for significant changes

# Store results
tau_results = []

# Process files
for filename in os.listdir(rankings_folder):
    if filename.endswith(".csv"):
        # Clean molecule ID
        molecule_id = filename.replace("-ranking.csv", "")
        file_path = os.path.join(rankings_folder, filename)

        try:
            df = pd.read_csv(file_path)
            
            # Calculate Kendall's tau
            static_order = df.sort_values("original rank")["id"].tolist()
            corrected_order = df.sort_values("new rank")["id"].tolist()
            structure_ids = df["id"].tolist()
            static_ranks = [static_order.index(s) for s in structure_ids]
            corrected_ranks = [corrected_order.index(s) for s in structure_ids]
            tau, _ = kendalltau(static_ranks, corrected_ranks)

            tau_results.append({
                "Molecule": molecule_id,
                "Kendall_tau": tau,
                "SignificantChange": tau < tau_threshold
            })
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

# Create and save results dataframe
df_tau = pd.DataFrame(tau_results).sort_values("Molecule")
df_tau.to_csv(output_csv, index=False)

# Generate histogram
plt.figure(figsize=(10, 6))

# Split data into significant and non-significant changes
sig_data = df_tau[df_tau['SignificantChange']]['Kendall_tau']
non_sig_data = df_tau[~df_tau['SignificantChange']]['Kendall_tau']

# Create bins
bins = np.linspace(0, 1, 11)  # 0.0 to 1.0 in 0.1 increments

# Plot both groups
plt.hist(non_sig_data, bins=bins, color='green', alpha=0.7, 
         edgecolor='black', label=f'τ ≥ {tau_threshold}')
plt.hist(sig_data, bins=bins, color='red', alpha=0.7, 
         edgecolor='black', label=f'τ < {tau_threshold}')

# Add threshold line and annotations
plt.axvline(tau_threshold, color='blue', linestyle='--', 
            label=f'Threshold (τ = {tau_threshold})')
plt.xlabel("Kendall's τ")
plt.ylabel("Number of Molecules")
plt.legend()

# Add count of significant changes
sig_count = len(sig_data)
plt.text(0.05, 0.95, f'{sig_count} molecules (τ < {tau_threshold})',
         transform=plt.gca().transAxes, ha='left', va='top',
         bbox=dict(facecolor='white', alpha=0.8))

plt.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig(output_plot, dpi=300)
plt.show()

# Print summary
print(f"\nAnalysis complete:")
print(f"- {len(df_tau)} molecules processed")
print(f"- {sig_count} molecules show significant ranking changes (τ < {tau_threshold})")
print(f"- Results saved to {output_csv}")
print(f"- Visualization saved to {output_plot}")

# Optional: Print molecules with significant changes
if sig_count > 0:
    print("\nMolecules with significant ranking changes:")
    print(df_tau[df_tau['SignificantChange']][['Molecule', 'Kendall_tau']].to_string(index=False))