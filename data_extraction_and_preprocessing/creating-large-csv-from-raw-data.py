import pandas as pd
import os

# Define the directory containing the CSV files
input_dir = "raw-energy-files"

# Create an empty list to store dataframes
dfs = []

# Loop through all subdirectories and CSV files
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".csv"):
            # Extract crystal and crystal type from the file name
            parts = file.split("_")
            crystal = parts[0]
            crystal_type = parts[1]
            k_point = float(parts[2].split("-")[-1].replace(".csv", ""))
            
            # Read the CSV file
            df = pd.read_csv(os.path.join(root, file))
            
            # Extract required data
            total_phonons = df[df["Property"] == "Total number of phonons"]["Value"].values[0]
            total_k_points = df[df["Property"] == "Total number of sampled unique k-points"]["Value"].values[0]
            
            # Create a new dataframe with the extracted data
            new_df = pd.DataFrame({
                "crystal": [crystal],
                "crystal_type": [crystal_type],
                "k_point": [k_point],
                "Total number of phonons": [total_phonons],
                "Total number of sampled unique k-points": [total_k_points]
            })
            
            dfs.append(new_df)

# Combine all dataframes
combined_df = pd.concat(dfs, ignore_index=True)

# Sort the combined dataframe
combined_df = combined_df.sort_values(by=["crystal", "crystal_type", "k_point"])

# Save the combined dataframe to a new CSV file
output_file = "combined_data_sorted.csv"
combined_df.to_csv(output_file, index=False)

print(f"Sorted combined data saved to {output_file}")
