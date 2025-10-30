import pandas as pd
import matplotlib.pyplot as plt
import os
import re
import numpy as np

# Read the CSV file
df = pd.read_csv('all_energy_values.csv')

# Define the output directory
output_dir = 'energy-difference-plots'
os.makedirs(output_dir, exist_ok=True)

# Group crystal types by base name
crystal_groups = df['Crystal Type'].apply(lambda x: re.match(r'(.+)_\d+', x).group(1)).unique()

for base_name in crystal_groups:
    crystal_pair = df[df['Crystal Type'].str.startswith(base_name)]
    if len(crystal_pair['Crystal Type'].unique()) == 2:
        crystal_1, crystal_2 = crystal_pair['Crystal Type'].unique()
        
        merged = pd.merge(
            crystal_pair[crystal_pair['Crystal Type'] == crystal_1],
            crystal_pair[crystal_pair['Crystal Type'] == crystal_2],
            on='K-Point', suffixes=('_1', '_2')
        )
        
        merged['Diff_No_Debye'] = merged['Energy without Debye or KDE_2'] - merged['Energy without Debye or KDE_1']
        merged['Diff_Only_Debye'] = merged['Energy with only Debye_2'] - merged['Energy with only Debye_1']
        merged['Diff_Debye_KDE'] = merged['Energy with Debye and KDE_2'] - merged['Energy with Debye and KDE_1']
        
        plt.figure(figsize=(10, 6))
        plt.scatter(merged['K-Point'], merged['Diff_No_Debye'], label='Without Debye or KDE')
        plt.plot(merged['K-Point'], merged['Diff_No_Debye'], '-')
        plt.scatter(merged['K-Point'], merged['Diff_Only_Debye'], label='With only Debye')
        plt.plot(merged['K-Point'], merged['Diff_Only_Debye'], '-')
        plt.scatter(merged['K-Point'], merged['Diff_Debye_KDE'], label='With Debye and KDE')
        plt.plot(merged['K-Point'], merged['Diff_Debye_KDE'], '-')
        
        plt.xlabel('K-Point (Å)')
        plt.ylabel('Energy Difference (kJ/mol)')
        plt.xticks(np.arange(0.10, 0.40, 0.05))
        plt.legend()
        plt.grid(True)
        plt.gca().invert_xaxis()
        
        plt.savefig(os.path.join(output_dir, f'energy_diff_{base_name}.png'))
        plt.close()

print(f"Plots have been saved in {output_dir}")
