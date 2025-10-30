import os
import re
import csv

# Directory containing the .out files
directory = 'energy-files'

# Output CSV file
output_file = 'energy_summary.csv'

# Regular expressions to match the energy values
energy_patterns = [
    r'Energy without Debye or KDE:\s*([-\d.]+)',
    r'Energy with only Debye:\s*([-\d.]+)',
    r'Energy with Debye and KDE:\s*([-\d.]+)'
]

# CSV header
header = ['Crystal Type', 'K-Point', 'Energy without Debye or KDE', 'Energy with only Debye', 'Energy with Debye and KDE']

# List to store the data
data = []

# Loop through all .out files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.out'):
        filepath = os.path.join(directory, filename)
        
        # Extract crystal type and k-point from filename
        match = re.search(r'(\w+_\d+-\d+).*k-value-([\d.]+)', filename)
        if match:
            crystal_type = match.group(1)
            k_point = match.group(2)
            
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
            
            # Add the data to the list
            data.append([crystal_type, k_point] + energies)

# Write the data to CSV file
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(data)

print(f"CSV file '{output_file}' has been created successfully.")
