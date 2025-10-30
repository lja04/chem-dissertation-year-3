import os
import glob
import pandas as pd

# Define paths
results_dir = "results-3"
structures_csv = os.path.join(results_dir, "structures.csv")
output_csv = os.path.join(results_dir, "izijoq-ranking-0_12.csv")

# Step 1: Parse all .out files and extract vibrational energies
vibrational_energies = {}

# Search for all .out files in the results directory
out_files = glob.glob(os.path.join(results_dir, "**/*.out"), recursive=True)

for out_file in out_files:
    # Extract the ID from the filename (assuming format izijoq-QR-2-1566-3.out)
    file_id = os.path.basename(out_file).replace('.out', '')
    
    # Read the file and look for the vibrational energy line
    with open(out_file, 'r') as f:
        content = f.read()
        
        # Find the vibrational energy line
        start_idx = content.find("Neat vibrational energy = ")
        if start_idx != -1:
            end_idx = content.find(" kJ/mol", start_idx)
            energy_str = content[start_idx:end_idx].split("=")[1].strip()
            vibrational_energies[file_id] = float(energy_str)

# Step 2: Load the original CSV and add new columns
df = pd.read_csv(structures_csv)

# Add the vibrational energy column
df['free energy'] = df['id'].map(vibrational_energies)

# Step 3: Remove rows with N/A in free energy
df = df.dropna(subset=['free energy'])

# Step 4: Calculate new energy
df['new energy'] = df['energy'] + df['free energy']

# Step 5: Rank based on original energy (ascending=True for lower energy = better rank)
df['original rank'] = df['energy'].rank(ascending=True, method='min').astype(int)

# Step 6: Rank based on new energy (ascending=True for lower energy = better rank)
df['new rank'] = df['new energy'].rank(ascending=True, method='min').astype(int)

# Sort by new rank (ascending order - lowest energy first)
df = df.sort_values('new rank')

# Reorder columns as requested
columns_order = ['id', 'spacegroup', 'density', 'energy', 'minimization_step', 
                 'trial_number', 'minimization_time', 'free energy', 'new energy', 
                 'original rank', 'new rank']
df = df[columns_order]

# Save the updated CSV
df.to_csv(output_csv, index=False)

print(f"Processed {len(df)} structures. Results saved to {output_csv}")