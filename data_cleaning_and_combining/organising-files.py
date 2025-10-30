import os
import re

# Define the directory containing your .out files
main_directory = 'out-files-output'
output_file = 'energy_data.csv'  # Changed to .csv for clarity

# Initialize a dictionary to hold energy data for each crystal type
energy_data = {}

# Loop through all files in the main directory
for filename in os.listdir(main_directory):
    if filename.endswith('.out'):
        # Extract crystal type and k-point value from the filename
        match = re.search(r'([^/]+)_k-value-(\d+\-\d+)', filename)
        if match:
            crystal_type_species = match.group(1)  # e.g., boqqut_14-9355 or boqqut_61-15699
            k_point = match.group(2)

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

            # Store the values in the dictionary
            if crystal_type_species not in energy_data:
                energy_data[crystal_type_species] = []
            energy_data[crystal_type_species].append((k_point, energies))

# Write the collected data to a new CSV file
with open(output_file, 'w') as out_file:
    out_file.write("Crystal Type,K-Point,Energy without Debye or KDE,Energy with only Debye,Energy with Debye and KDE\n")
    for crystal_type_species, values in energy_data.items():
        for value in values:
            k_point, energies = value
            e_no_debye = energies.get('no_debye', 'N/A')
            e_debye = energies.get('debye', 'N/A')
            e_debye_kde = energies.get('debye_kde', 'N/A')
            out_file.write(f"{crystal_type_species},{k_point},{e_no_debye},{e_debye},{e_debye_kde}\n")

print(f"Data extraction complete. Results saved to {output_file}.")
