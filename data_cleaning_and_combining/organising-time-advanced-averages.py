import pandas as pd

# Define file paths
input_file = "consolidated_total_run_time.csv"
output_file = "sorted_total_run_time.csv"

# Load the CSV file into a DataFrame
df = pd.read_csv(input_file, names=["Name", "Total Run Time"])

# Extract k-value from the Name column and add it as a new column for sorting
df["k-value"] = df["Name"].str.extract(r"k-value-(\d+\.\d+)").astype(float)

# Sort by Name alphabetically and k-value numerically (ascending)
df_sorted = df.sort_values(by=["Name", "k-value"], ascending=[True, True])

# Select only the relevant columns for output
df_output = df_sorted[["Name", "Total Run Time"]]

# Save the sorted DataFrame to a new CSV file without header and index
df_output.to_csv(output_file, index=False, header=False)

print(f"Sorted data saved to {output_file}")
