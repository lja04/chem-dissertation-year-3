import pandas as pd
import os
import re

# Define the main directory containing your .out files
main_directory = 'out-files-output'
output_directory = 'different'
os.makedirs(output_directory, exist_ok=True)

# Initialize a dictionary to hold combined data for each crystal type
combined_data = {}

# Loop through all .out files in the main directory
for filename in os.listdir(main_directory):
    if filename.endswith('.out'):
        # Extract crystal type and k-point value from the filename
        match = re.search(r'(boqqut|feckik|buhmoh|phthao|tohzul|other_crystal_type)_\d+-\d+_k-value-(\d+\-\d+)', filename)
        if match:
            crystal_type = match.group(0)  # e.g., boqqut_14-9355
            k_point = match.group(2)  # e.g., 0-10

            # Open and read the .out file
            with open(os.path.join(main_directory, filename), 'r') as file:
                energies = {}
                for line in file:
                    # Extract energy values from the lines
                    if "Energy without Debye or KDE:" in line:
                        energies['no_debye'] = float(re.search(r'[-+]?\d*\.\d+|\d+', line).group())
                    elif "Energy with only Debye:" in line:
                        energies['debye'] = float(re.search(r'[-+]?\d*\.\d+|\d+', line).group())
                    elif "Energy with Debye and KDE:" in line:
                        energies['debye_kde'] = float(re.search(r'[-+]?\d*\.\d+|\d+', line).group())

            # Store energy values in a DataFrame
            if crystal_type not in combined_data:
                combined_data[crystal_type] = []
            
            combined_data[crystal_type].append({
                'K-Point': k_point,
                'Energy without Debye or KDE': energies['no_debye'],
                'Energy with only Debye': energies['debye'],
                'Energy with Debye and KDE': energies['debye_kde'],
                'Species': crystal_type.split('_')[0]  # Extract species name
            })

# Convert dictionary to DataFrames and save to CSV files
for crystal_type, records in combined_data.items():
    df = pd.DataFrame(records)
    output_filename = f"{output_directory}/{crystal_type}_combined.csv"
    df.to_csv(output_filename, index=False)
    print(f"Saved {output_filename}")

print("Species data has been combined into separate CSV files.")
