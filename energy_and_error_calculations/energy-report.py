import os
import csv
from tqdm import tqdm  # For progress bar

# Define the input directory for .out files and output directory for reports
input_dir = "energy-files"
output_dir = "energy-data"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to parse energy values from .out files
def parse_energy_file(file_path):
    energies = {
        "Energy without Debye": None,
        "Energy with only Debye": None,
        "Energy with Debye and KDE": None,
    }
    
    with open(file_path, "r") as file:
        for line in file:
            if "Energy without Debye" in line:
                try:
                    energies["Energy without Debye"] = float(line.split()[-2])  # Extracting numeric value
                except ValueError:
                    print(f"Warning: Could not parse 'Energy without Debye' in {file_path}")
            elif "Energy with only Debye" in line:
                try:
                    energies["Energy with only Debye"] = float(line.split()[-2])  # Extracting numeric value
                except ValueError:
                    print(f"Warning: Could not parse 'Energy with only Debye' in {file_path}")
            elif "Energy with Debye and KDE" in line:
                try:
                    energies["Energy with Debye and KDE"] = float(line.split()[-2])  # Extracting numeric value
                except ValueError:
                    print(f"Warning: Could not parse 'Energy with Debye and KDE' in {file_path}")
    
    return energies

# Function to analyze energy data across all .out files
def analyze_energy_data(input_dir, output_dir):
    # Collect all .out files in the input directory
    out_files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith(".out")
    ]

    # Group files by crystal and polymorph
    grouped_files = {}
    for file_path in out_files:
        file_name = os.path.basename(file_path)
        parts = file_name.split("_")
        
        if len(parts) >= 3:
            crystal = parts[0]
            polymorph = parts[1]
            k_value = parts[2]  # Extract k-value directly from filename
            key = f"{crystal}_{polymorph}"
            
            if key not in grouped_files:
                grouped_files[key] = {}
            grouped_files[key][k_value] = file_path

    # Process each group of files (by crystal and polymorph)
    for group_key, k_value_files in tqdm(grouped_files.items(), desc="Processing groups", unit="group"):
        energy_report = {
            "Energy Section": [],
            "Highest Energy": [],
            "Lowest Energy": [],
            "Difference": [],
            "Highest Source": [],
            "Lowest Source": []
        }

        # Initialize variables to track highest and lowest energies
        max_energies = {
            "Energy without Debye": (float('-inf'), ""),
            "Energy with only Debye": (float('-inf'), ""),
            "Energy with Debye and KDE": (float('-inf'), "")
        }
        
        min_energies = {
            "Energy without Debye": (float('inf'), ""),
            "Energy with only Debye": (float('inf'), ""),
            "Energy with Debye and KDE": (float('inf'), "")
        }

        # Process each .out file in this group
        for k_value, out_file in k_value_files.items():
            try:
                energies = parse_energy_file(out_file)
                for key in max_energies.keys():
                    if energies[key] is not None:
                        # Check for maximum values
                        if energies[key] > max_energies[key][0]:
                            max_energies[key] = (energies[key], k_value)  # Store only k-value
                        # Check for minimum values
                        if energies[key] < min_energies[key][0]:
                            min_energies[key] = (energies[key], k_value)  # Store only k-value
            except Exception as e:
                print(f"Error reading {out_file}: {e}")

        # Store results in the report dictionary
        for key in max_energies.keys():
            energy_report["Energy Section"].append(key)
            energy_report["Highest Energy"].append(max_energies[key][0])
            energy_report["Lowest Energy"].append(min_energies[key][0])
            energy_report["Difference"].append(max_energies[key][0] - min_energies[key][0])
            energy_report["Highest Source"].append(max_energies[key][1])  # This will be just k-value now
            energy_report["Lowest Source"].append(min_energies[key][1])    # This will be just k-value now

        # Prepare output file name and path
        output_file_name = f"{group_key}_energy-report.csv"
        output_file_path = os.path.join(output_dir, output_file_name)

        # Write the report to a new CSV file
        with open(output_file_path, mode="w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Energy Section", "Highest Energy", "Lowest Energy", "Difference", "Highest Source", "Lowest Source"])
            
            for i in range(len(energy_report["Energy Section"])):
                writer.writerow([
                    energy_report["Energy Section"][i],
                    energy_report["Highest Energy"][i],
                    energy_report["Lowest Energy"][i],
                    energy_report["Difference"][i],
                    energy_report["Highest Source"][i],
                    energy_report["Lowest Source"][i]
                ])

# Run the function to analyze energy data
analyze_energy_data(input_dir, output_dir)

print("Energy report generation complete. Reports saved.")
