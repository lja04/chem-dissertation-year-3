'''
This code took all of my crystal files and collected all of the energy values from the .out files using the following method:

When you add the Debye model, you then need to add the 'Neat vibrational energy' term and the 'Debye contribution to vibrational energy' term to 
get the total vibrational free energy. When doing this, you need to scale the 'Neat vibrational energy' by (n-3)/n, 
where n = the number of phonons: this is reported in the line 'Total number of phonons is:' 
This is because the Debye term models 3 of the phonons in the crystal, so that the other term needs to be re-scaled.

For the model with Debye and KDE, add 'Epanechnikov KDE vibrational energy:' to 'Debye contribution to vibrational energy', and 
the 'Epanechnikov KDE vibrational energy:' needs to be re-scaled by (n-3)/n.
'''

import os
import csv
from glob import glob
from collections import defaultdict

def format_number(number):
    return f"{number:.6f}"

def calculate_energies(file_path):
    neat_vib_energy = 0
    debye_contrib = 0
    total_phonons = 0
    kde_energy = 0

    with open(file_path, 'r') as f:
        for line in f:
            if 'Neat vibrational energy =' in line:
                neat_vib_energy = float(line.split('=')[1].split()[0])
            elif 'Debye contribution to vibrational energy:' in line:
                debye_contrib = float(line.split(':')[1].split()[0])
            elif 'Total number of phonons is:' in line:
                total_phonons = int(line.split(':')[1].strip())
            elif 'Epanechnikov KDE vibrational energy:' in line:
                kde_energy = float(line.split(':')[1].split()[0])

    scale_factor = (total_phonons - 3) / total_phonons if total_phonons > 0 else 1

    energy_without_debye_kde = neat_vib_energy
    energy_with_debye = neat_vib_energy * scale_factor + debye_contrib
    energy_with_debye_kde = kde_energy * scale_factor + debye_contrib

    return (format_number(energy_without_debye_kde),
            format_number(energy_with_debye),
            format_number(energy_with_debye_kde))

def main():
    base_dir = 'crystal-files'
    output_file = 'energy_data.csv'

    data = defaultdict(lambda: defaultdict(dict))

    for crystal_dir in glob(os.path.join(base_dir, '*')):
        crystal_name = os.path.basename(crystal_dir)
        for crystal_type_dir in glob(os.path.join(crystal_dir, '*')):
            crystal_type = os.path.basename(crystal_type_dir)
            calc_dir = os.path.join(crystal_type_dir, 'calc')
            
            for k_value_dir in glob(os.path.join(calc_dir, 'k_value_*')):
                k_point = float(os.path.basename(k_value_dir).split('_')[-1])
                
                if 0.1 <= k_point <= 0.4:
                    out_file = glob(os.path.join(k_value_dir, '*.out'))
                    if out_file:
                        energies = calculate_energies(out_file[0])
                        data[f"{crystal_name}_{crystal_type}"][k_point] = energies

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Crystal Type', 'K-Point', 'Energy without Debye or KDE', 'Energy with only Debye', 'Energy with Debye and KDE'])

        for crystal_type in sorted(data.keys()):
            for k_point in sorted(data[crystal_type].keys()):
                energies = data[crystal_type][k_point]
                writer.writerow([crystal_type, f"{k_point:.2f}"] + list(energies))

    print(f"Data has been written to {output_file}")

if __name__ == "__main__":
    main()
