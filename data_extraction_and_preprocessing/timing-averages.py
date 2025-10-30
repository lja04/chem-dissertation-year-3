import os
import csv
from tqdm import tqdm  # For progress bar
import pandas as pd  # For easier CSV manipulation

# Define the base directory for timing data and output directory for averages
timing_data_dir = "time-data"
averages_output_dir = "averages"

# Ensure the averages output directory exists
os.makedirs(averages_output_dir, exist_ok=True)

# Function to calculate averages for each k-value folder
def calculate_averages(timing_data_dir, averages_output_dir):
    # Traverse through the crystal, polymorph, and k-value directories
    for crystal in tqdm(os.listdir(timing_data_dir), desc="Processing crystals", unit="crystal"):
        crystal_path = os.path.join(timing_data_dir, crystal)
        if not os.path.isdir(crystal_path):
            continue  # Skip if it's not a directory

        for polymorph in os.listdir(crystal_path):
            polymorph_path = os.path.join(crystal_path, polymorph)
            if not os.path.isdir(polymorph_path):
                continue  # Skip if it's not a directory

            for k_value_folder in os.listdir(polymorph_path):
                k_value_path = os.path.join(polymorph_path, k_value_folder)
                if not os.path.isdir(k_value_path):
                    continue  # Skip if it's not a directory

                # Collect all CSV files in this k-value folder
                csv_files = [
                    os.path.join(k_value_path, f)
                    for f in os.listdir(k_value_path)
                    if f.endswith(".csv")
                ]

                # Read and combine all CSV files into a single DataFrame
                combined_data = []
                for csv_file in csv_files:
                    try:
                        df = pd.read_csv(csv_file)
                        combined_data.append(df)
                    except Exception as e:
                        print(f"Error reading {csv_file}: {e}")

                if combined_data:
                    combined_df = pd.concat(combined_data)

                    # Calculate the average for each metric
                    averages_df = combined_df.groupby("Metric", as_index=False).mean()

                    # Prepare the output file name and path
                    output_file_name = f"{crystal}_{polymorph}_{k_value_folder}_time-averages.csv"
                    output_file_path = os.path.join(averages_output_dir, crystal)

                    # Ensure crystal-specific directory exists in the averages folder
                    os.makedirs(output_file_path, exist_ok=True)

                    # Save the averages to a new CSV file
                    averages_df.to_csv(os.path.join(output_file_path, output_file_name), index=False)

# Run the function to calculate averages
calculate_averages(timing_data_dir, averages_output_dir)

print("Average calculation complete. Results saved.")
