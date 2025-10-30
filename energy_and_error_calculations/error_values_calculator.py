import pandas as pd
import numpy as np

# Read the original CSV file
df = pd.read_csv('all_energy_values.csv')

# Group by crystal base name and k-point
crystal_groups = df.groupby(df['Crystal Type'].str.split('_').str[0])

results = []

for crystal, group in crystal_groups:
    # Get the two polymorphs for each crystal
    polymorphs = group['Crystal Type'].unique()
    if len(polymorphs) != 2:
        continue
    
    # Calculate free energy differences at each k-point
    energy_diffs = group.pivot(index='K-Point', columns='Crystal Type', values='Energy with Debye and KDE')
    energy_diffs['Difference'] = energy_diffs[polymorphs[1]] - energy_diffs[polymorphs[0]]
    
    # Calculate error relative to 0.10 k-point spacing
    reference_diff = energy_diffs.loc[0.10, 'Difference']
    energy_diffs['Error'] = energy_diffs['Difference'] - reference_diff
    
    # Add results to the list
    for k_value, row in energy_diffs.iterrows():
        results.append({
            'crystal': crystal,
            'k-value': k_value,
            'error': row['Error']
        })

# Create DataFrame from results
results_df = pd.DataFrame(results)

# Calculate statistics for each k-value
stats = results_df.groupby('k-value').agg({
    'error': [
        ('mean absolute error', lambda x: np.abs(x).mean()),
        ('mean signed error', np.mean),
        ('max absolute error', lambda x: np.abs(x).max())
    ]
})

stats.columns = stats.columns.droplevel()
stats = stats.reset_index()

# Save the results to a CSV file
output_file = 'k_point_error_statistics.csv'
stats.to_csv(output_file, index=False)

print(f"CSV file with k-point error statistics has been saved to {output_file}")
