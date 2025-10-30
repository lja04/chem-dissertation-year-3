import re
import os

def parse_autofree_output(filename):
    with open(filename, 'r') as file:
        content = file.read()

    # Function to safely extract values
    def safe_extract(patterns, default=0.0):
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return float(match.group(1))
        return default

    # Extract required values
    neat_vib_energy = safe_extract([
        r'Neat vibrational energy:\s+([-\d.]+)',
        r'Neat vibrational energy\s*=\s*([-\d.]+)\s*kJ/mol'
    ])
    total_phonons = int(safe_extract([
        r'Total number of phonons is:\s+(\d+)',
        r'Total number of phonons:\s+(\d+)'
    ], 1))
    debye_contribution = safe_extract([
        r'Debye contribution to vibrational energy:\s+([-\d.]+)',
        r'Debye contribution to vibrational energy\s*=\s*([-\d.]+)\s*kJ/mol'
    ])
    kde_energy = safe_extract([
        r'Epanechnikov KDE vibrational energy:\s+([-\d.]+)',
        r'Epanechnikov KDE vibrational energy\s*=\s*([-\d.]+)\s*kJ/mol'
    ])

    # Calculate scaling factor
    scaling_factor = (total_phonons - 3) / total_phonons if total_phonons > 3 else 1

    # Calculate energy totals
    no_debye_kde = neat_vib_energy
    only_debye = (neat_vib_energy * scaling_factor) + debye_contribution
    debye_kde = (kde_energy * scaling_factor) + debye_contribution

    return no_debye_kde, only_debye, debye_kde

def save_energy_values(output_filename, energies):
    with open(output_filename, 'w') as outfile:
        outfile.write(f"Energy without Debye or KDE: {energies[0]:.6f} kJ/mol\n")
        outfile.write(f"Energy with only Debye: {energies[1]:.6f} kJ/mol\n")
        outfile.write(f"Energy with Debye and KDE: {energies[2]:.6f} kJ/mol\n")

# Directory containing .out files
input_directory = 'original-out-files'

# Create the energy-files directory if it doesn't exist
output_directory = os.path.join(input_directory, 'energy-files')
os.makedirs(output_directory, exist_ok=True)

# Loop through all .out files in the directory
for filename in os.listdir(input_directory):
    if filename.endswith('.out'):
        input_path = os.path.join(input_directory, filename)
        output_filename = f"{os.path.splitext(filename)[0]}_energies.out"
        output_path = os.path.join(output_directory, output_filename)

        try:
            energies = parse_autofree_output(input_path)
            save_energy_values(output_path, energies)
            print(f"Energy values saved to {output_path}")
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

print("Processing complete.")
