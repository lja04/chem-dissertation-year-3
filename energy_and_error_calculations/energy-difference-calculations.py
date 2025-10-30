import pandas as pd
import os

# Read the CSV file
input_file = 'all_energy_values.csv'
output_file = 'energy_difference_calculations.csv'

df = pd.read_csv(input_file)

# Prepare a list to store the new data
new_data = []

# Group crystal types by base name
crystal_groups = df['Crystal Type'].apply(lambda x: x.split('_')[0]).unique()

for base_name in crystal_groups:
    crystal_pair = df[df['Crystal Type'].str.startswith(base_name)]
    if len(crystal_pair['Crystal Type'].unique()) == 2:
        crystal_1, crystal_2 = crystal_pair['Crystal Type'].unique()
        
        # Merge the two crystals by K-Point
        merged = pd.merge(
            crystal_pair[crystal_pair['Crystal Type'] == crystal_1],
            crystal_pair[crystal_pair['Crystal Type'] == crystal_2],
            on='K-Point', suffixes=('_1', '_2')
        )
        
        # Calculate the absolute energy values and energy difference
        merged['Absolute_Energy_1'] = abs(merged['Energy with Debye and KDE_1'])
        merged['Absolute_Energy_2'] = abs(merged['Energy with Debye and KDE_2'])
        merged['Energy_Difference'] = abs(merged['Energy with Debye and KDE_2'] - merged['Energy with Debye and KDE_1'])
        
        # Append rows to new data
        for _, row in merged.iterrows():
            new_data.append([
                crystal_1,
                crystal_2,
                row['Energy with Debye and KDE_1'],
                row['Energy with Debye and KDE_2'],
                row['Absolute_Energy_1'],
                row['Absolute_Energy_2'],
                row['Energy_Difference']
            ])

# Create a new DataFrame for the output
output_df = pd.DataFrame(new_data, columns=[
    'Crystal 1',
    'Crystal 2',
    'Crystal 1 Energy with Debye and KDE (kJ/mol)',
    'Crystal 2 Energy with Debye and KDE (kJ/mol)',
    'Absolute Crystal 1 Energy with Debye and KDE (kJ/mol)',
    'Absolute Crystal 2 Energy with Debye and KDE (kJ/mol)',
    'Energy Difference (kJ/mol)'
])

# Save the output to a CSV file
os.makedirs(os.path.dirname(output_file), exist_ok=True)
output_df.to_csv(output_file, index=False)

print(f"New CSV file has been saved at {output_file}")
