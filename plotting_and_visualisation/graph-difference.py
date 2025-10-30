import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# Define the directory containing your combined CSV files
input_directory = 'split-files'
output_directory = 'difference-energy-graphs'
os.makedirs(output_directory, exist_ok=True)

# List all combined CSV files in the input directory
combined_files = os.listdir(input_directory)

# Debugging output: Print all filenames found
print("Files found in directory:")
for file in combined_files:
    print(file)

# Group files by their base species name
species_files = {}
for combined_file in combined_files:
    # Extract base species name (e.g., 'boqqut' from 'boqqut_14-9355.csv')
    match = re.match(r'([a-zA-Z]+)_\d+-\d+\.csv', combined_file)
    if match:
        base_species = match.group(1)
        if base_species not in species_files:
            species_files[base_species] = []
        species_files[base_species].append(combined_file)
    else:
        print(f"No match for file: {combined_file}")  # Debugging output for unmatched files

# Debugging output: Check the grouping of species files
print("Grouped Species Files:")
for species, files in species_files.items():
    print(f"{species}: {files}")

# Loop through each species group to calculate differences and plot
for base_species, files in species_files.items():
    # Ensure there are exactly two polymorphs for comparison
    if len(files) != 2:
        print(f"Warning: Expected 2 polymorphs for {base_species}, found {len(files)}.")
        continue

    # Read data from both CSV files
    data1 = pd.read_csv(os.path.join(input_directory, files[0]))
    data2 = pd.read_csv(os.path.join(input_directory, files[1]))

    # Debugging output: Check if data is read correctly
    print(f"Data from {files[0]}:")
    print(data1.head())  # Display first few rows of data1
    print(f"Data from {files[1]}:")
    print(data2.head())  # Display first few rows of data2

    # Ensure 'K-Point' is numeric; no need to replace '-' since it's already numeric.
    # If 'K-Point' is a string with '-' (e.g., '0.35'), you would convert it here.
    
    # Sort both datasets by K-Point
    data1 = data1.sort_values(by='K-Point')
    data2 = data2.sort_values(by='K-Point')

    # Check if both datasets have matching lengths after sorting
    if len(data1) != len(data2):
        print(f"Warning: Mismatched lengths for {files[0]} and {files[1]}.")
        continue

    # Calculate differences in energy values between the two datasets for each energy type
    energy_no_debye_diff = data1['Energy without Debye or KDE'].values - data2['Energy without Debye or KDE'].values
    energy_debye_diff = data1['Energy with only Debye'].values - data2['Energy with only Debye'].values
    energy_debye_kde_diff = data1['Energy with Debye and KDE'].values - data2['Energy with Debye and KDE'].values

    # Create the plot for differences
    plt.figure(figsize=(10, 6))
    
    plt.plot(data1['K-Point'], energy_no_debye_diff, marker='o', label='Difference No Debye or KDE')
    plt.plot(data1['K-Point'], energy_debye_diff, marker='s', label='Difference Only Debye')
    plt.plot(data1['K-Point'], energy_debye_kde_diff, marker='^', label='Difference Debye and KDE')

    # Customize the plot with capitalized titles
    plt.title(f"Energy Differences Between {files[0].replace('.csv', '').upper()} and {files[1].replace('.csv', '').upper()}")
    plt.xlabel('Target K-Point distance (Å⁻¹)')
    plt.ylabel('Energy Difference (kJ/mol)')
    
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')  # Add a horizontal line at y=0 for reference
    plt.legend()
    plt.grid(True)

    # Invert x-axis to display k-points from large to small
    plt.gca().invert_xaxis()
    
    # Save the figure with an appropriate name
    output_filename = f"{output_directory}/{files[0].replace('.csv', '')}_vs_{files[1].replace('.csv', '')}_energy_difference_graph.png"
    plt.savefig(output_filename)
    
    # Close the plot to free memory
    plt.close()

print(f"Graphs of energy differences have been created and saved in the '{output_directory}' directory.")
