import pandas as pd

# Define the input file path
input_file = "total_run_times.csv"

# Read the existing total run times CSV file
df = pd.read_csv(input_file)

# Split the Name column to extract polymorph names
df['Polymorph'] = df['Name'].apply(lambda x: '/'.join(x.split('/')[:-1]))

# Group by Polymorph and sum the total times
aggregated_df = df.groupby('Polymorph').agg({
    'Total Time (seconds)': 'sum',
    'Total Time (minutes)': 'sum',
    'Total Time (hours)': 'sum'
}).reset_index()

# Prepare the final DataFrame with the desired output format
final_df = aggregated_df.rename(columns={'Polymorph': 'Name'})

# Save the aggregated DataFrame to a new CSV file
output_file = "aggregated_total_run_times.csv"
final_df.to_csv(output_file, index=False)

print(f"Aggregated total run times saved to {output_file}")
