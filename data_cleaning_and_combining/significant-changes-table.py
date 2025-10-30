import pandas as pd

# Configuration
input_csv = "observed-structures-from-csvs.csv"
output_csv = "all_crystals_rank_changes.csv"

# Load data
df = pd.read_csv(input_csv)

# Calculate metrics
df['Rank Change'] = df['new rank'] - df['original rank']
df['Abs Rank Change'] = df['Rank Change'].abs()
df['Energy Difference (kJ/mol)'] = df['new energy'] - df['energy']

# Get one representative row per crystal (the structure with largest absolute rank change)
all_crystals = df.sort_values('Abs Rank Change', ascending=False).groupby('Refcode').first().reset_index()

# Select and order columns
result_cols = [
    'Refcode',
    'original rank',
    'new rank', 
    'Abs Rank Change',
    'energy',
    'new energy',
    'Energy Difference (kJ/mol)'
]

# Format numeric columns
all_crystals['energy'] = all_crystals['energy'].round(2)
all_crystals['new energy'] = all_crystals['new energy'].round(2)
all_crystals['Energy Difference (kJ/mol)'] = all_crystals['Energy Difference (kJ/mol)'].round(2)

# Save full results
all_crystals[result_cols].to_csv(output_csv, index=False)

print(f"Processed {len(all_crystals)} crystals")
print("\nTop 10 largest rank changes:")
print(all_crystals[result_cols].head(10).to_string(index=False))
print(f"\nComplete results saved to {output_csv}")