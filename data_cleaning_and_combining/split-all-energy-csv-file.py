import os
import re
import csv
from collections import defaultdict

# Directory containing the .out files
directory = 'energy-files'

# Output directory for individual CSV files
output_directory = 'split_csv_files'
os.makedirs(output_directory, exist_ok=True)

# Regular expressions to match the energy values
energy_patterns = [
    r'Energy without Debye or KDE:\s*([-\d.]+)',
    r'Energy with only Debye:\s*([-\d.]+)',
    r'Energy with Debye and KDE:\s*([-\d.]+)'
]

# Dictionary to store the data grouped by crystal type
data_by_crystal = defaultdict(list)

# Loop through all .out files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.out'):
        filepath = os.path.join(directory, filename)
        
        # Extract crystal type and k-point from filename
        match = re.search(r'(\w+_\d+-\d+).*k-value-([\d.]+)', filename)
        if match:
            crystal_type = match.group(1)
            k_point = float(match.group(2))  # Convert to float
            
            # Read the file content
            with open(filepath, 'r') as file:
                content = file.read()
            
            # Extract energy values
            energies = []
            for pattern in energy_patterns:
                match = re.search(pattern, content)
                if match:
                    energies.append(match.group(1))
                else:
                    energies.append('')  # If energy value not found
            
            # Add the data to the dictionary under the appropriate crystal type
            data_by_crystal[crystal_type].append([crystal_type, f"{k_point:.2f}"] + energies)

# Write each crystal type's data to its own CSV file
for crystal_type, entries in data_by_crystal.items():
    output_file = os.path.join(output_directory, f"{crystal_type}.csv")
    
    # Write to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Crystal Type', 'K-Point', 'Energy without Debye or KDE', 'Energy with only Debye', 'Energy with Debye and KDE'])
        writer.writerows(entries)

print(f"CSV files have been created successfully in '{output_directory}'. Each file contains both polymorphs for each crystal type.")
