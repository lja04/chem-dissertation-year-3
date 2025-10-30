import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# Define the directory containing your combined CSV files
input_directory = 'split-files'
output_directory = 'debye-kde-difference-energy-graphs'
os.makedirs(output_directory, exist_ok=True)

# Define a list of colors and markers for different polymorph pairs
colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown']
markers = ['o', 's', '^', 'D', 'p', '*']

# Group files by their base species name
species_files = {}
for combined_file in os.listdir(input_directory):
    if combined_file.endswith('.csv'):
        # Extract base species name (e.g., 'buhmoh' from 'buhmoh_19-4929.csv')
        match = re.match(r'([a-zA-Z]+)_\d+-\d+\.csv', combined_file)
        if match:
            base_species = match.group(1)
            if base_species not in species_files:
                species_files[base_species] = []
            species_files[base_species].append(combined_file)

# Debugging output: Check the grouping of species files
print("Grouped Species Files:")
for species, files in species_files.items():
    print(f"{species}: {files}")

# Read all CSV files and calculate differences
all_differences = []
for base_species, files in species_files.items():
    if len(files) != 2:
        print(f"Warning: Expected 2 polymorphs for {base_species}, found {len(files)}. Skipping.")
        continue

    # Read data from both CSV files
    data1 = pd.read_csv(os.path.join(input_directory, files[0]))
    data2 = pd.read_csv(os.path.join(input_directory, files[1]))

    # Check K-Point data type and convert if necessary
    if data1['K-Point'].dtype == object:
        data1['K-Point'] = data1['K-Point'].str.replace('-', '.').astype(float)
    if data2['K-Point'].dtype == object:
        data2['K-Point'] = data2['K-Point'].str.replace('-', '.').astype(float)

    # Sort both datasets by K-Point
    data1 = data1.sort_values(by='K-Point')
    data2 = data2.sort_values(by='K-Point')

    # Check if both datasets have matching lengths after sorting
    if len(data1) != len(data2):
        print(f"Warning: Mismatched lengths for {files[0]} and {files[1]}. Skipping.")
        continue

    # Calculate differences in energy values between the two datasets for Debye and KDE
    energy_debye_kde_diff = data1['Energy with Debye and KDE'].values - data2['Energy with Debye and KDE'].values

    all_differences.append({
        'pair': f"{files[0].replace('.csv', '')} vs {files[1].replace('.csv', '')}",
        'k_points': data1['K-Point'].values,
        'differences': energy_debye_kde_diff
    })
    print(f"Added difference data for {files[0]} vs {files[1]}")  # Debug print

print(f"Total polymorph pairs processed: {len(all_differences)}")  # Debug print

if not all_differences:
    print("No valid data found to plot. Check your input files and data structure.")
else:
    # Create the plot
    plt.figure(figsize=(12, 8))

    for i, diff_data in enumerate(all_differences):
        # Capitalize the pair names for the legend
        capitalized_pair = diff_data['pair'].upper()
        plt.plot(diff_data['k_points'], diff_data['differences'], 
                color=colors[i % len(colors)], 
                marker=markers[i % len(markers)], 
                label=capitalized_pair)

    plt.title("Energy Differences (Debye and KDE) for Polymorph Pairs")
    plt.xlabel('K-Point')
    plt.ylabel('Energy Difference (kJ/mol)')
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.gca().invert_xaxis()  # Invert x-axis to display k-points from large to small

    # Adjust layout to prevent cutting off the legend
    plt.tight_layout()

    # Save the figure
    output_filename = f"{output_directory}/combined_energy_difference_debye_kde.png"
    plt.savefig(output_filename, bbox_inches='tight')

    plt.close()

    print(f"Combined graph of energy differences (Debye and KDE) has been created and saved as {output_filename}.")
