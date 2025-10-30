import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re

# Read the CSV data
df = pd.read_csv('all_energy_values.csv')

# Define the output directory
output_dir = 'energy-difference-plots'
os.makedirs(output_dir, exist_ok=True)

# Group crystal types by base name
crystal_groups = df['Crystal Type'].apply(lambda x: re.match(r'(.+)_\d+', x).group(1)).unique()

plt.figure(figsize=(12, 8))

for base_name in crystal_groups:
    crystal_pair = df[df['Crystal Type'].str.startswith(base_name)]
    if len(crystal_pair['Crystal Type'].unique()) == 2:
        crystal_1, crystal_2 = crystal_pair['Crystal Type'].unique()
        
        merged = pd.merge(
            crystal_pair[crystal_pair['Crystal Type'] == crystal_1],
            crystal_pair[crystal_pair['Crystal Type'] == crystal_2],
            on='K-Point', suffixes=('_1', '_2')
        )
        
        merged['Diff_Debye_KDE'] = abs(merged['Energy with Debye and KDE_2'] - merged['Energy with Debye and KDE_1'])
        
        # Capitalize the names for the legend
        plt.scatter(merged['K-Point'], merged['Diff_Debye_KDE'], label=f"{crystal_1.upper()} vs {crystal_2.upper()}")
        plt.plot(merged['K-Point'], merged['Diff_Debye_KDE'], '-')

plt.xlabel('K-Point')
plt.ylabel('Energy Difference (kJ/mol)')
plt.xticks(np.arange(0.10, 0.45, 0.05))
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'energy_diff_all_crystals.png'), bbox_inches='tight')
plt.close()

print(f"Plot has been saved in {output_dir}")
