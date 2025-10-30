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

# Group files by their base species name
species_files = {}
for combined_file in combined_files:
    match = re.match(r'([a-zA-Z]+)_\d+-\d+\.csv', combined_file)
    if match:
        base_species = match.group(1)
        if base_species not in species_files:
            species_files[base_species] = []
        species_files[base_species].append(combined_file)

# Create a 2x3 subplot figure
fig, axs = plt.subplots(3, 2, figsize=(20, 15))

# Flatten the axs array for easier indexing
axs = axs.flatten()

# Loop through each species group to calculate differences and plot
for idx, (base_species, files) in enumerate(species_files.items()):
    if len(files) != 2:
        print(f"Warning: Expected 2 polymorphs for {base_species}, found {len(files)}.")
        continue

    # Read data from both CSV files
    data1 = pd.read_csv(os.path.join(input_directory, files[0]))
    data2 = pd.read_csv(os.path.join(input_directory, files[1]))

    # Sort both datasets by K-Point
    data1 = data1.sort_values(by='K-Point')
    data2 = data2.sort_values(by='K-Point')

    if len(data1) != len(data2):
        print(f"Warning: Mismatched lengths for {files[0]} and {files[1]}.")
        continue

    # Calculate differences in energy values
    energy_no_debye_diff = data1['Energy without Debye or KDE'].values - data2['Energy without Debye or KDE'].values
    energy_debye_diff = data1['Energy with only Debye'].values - data2['Energy with only Debye'].values
    energy_debye_kde_diff = data1['Energy with Debye and KDE'].values - data2['Energy with Debye and KDE'].values

    # Plot on the corresponding subplot
    ax = axs[idx]
    ax.plot(data1['K-Point'], energy_no_debye_diff, marker='o', label='Difference No Debye or KDE')
    ax.plot(data1['K-Point'], energy_debye_diff, marker='s', label='Difference Only Debye')
    ax.plot(data1['K-Point'], energy_debye_kde_diff, marker='^', label='Difference Debye and KDE')

    # Customize the subplot
    ax.set_title(f"{base_species.upper()}")
    ax.set_xlabel('Target K-Point distance (Å⁻¹)')
    ax.set_ylabel('Energy Difference (kJ/mol)')
    ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
    ax.legend()
    ax.grid(True)
    ax.invert_xaxis()

# Adjust the layout
plt.tight_layout()

# Save the combined plot
output_filename = f"{output_directory}/combined_energy_difference_plot.png"
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
plt.close()

print(f"Combined plot of energy differences has been created and saved as '{output_filename}'.")
