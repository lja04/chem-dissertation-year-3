import os
import csv
import re

# Define input and output directories
input_dir = "crystal-files"
output_dir = "raw-energy-files"

def safe_float_convert(value):
    try:
        return float(re.search(r'-?\d+\.?\d*', value).group())
    except (ValueError, AttributeError):
        print(f"Warning: Could not convert '{value}' to float. Returning None.")
        return None

def parse_out_file(file_path):
    data = {
        "Neat vibrational energy": None,
        "Debye contribution to vibrational energy": None,
        "Epanechnikov KDE vibrational energy": None,
        "Total number of phonons": None,
        "Total number of sampled unique k-points": None
    }
    
    with open(file_path, 'r') as file:
        for line in file:
            if "Neat vibrational energy" in line:
                data["Neat vibrational energy"] = safe_float_convert(line.split("=")[1].strip())
            elif "Debye contribution to vibrational energy:" in line:
                data["Debye contribution to vibrational energy"] = safe_float_convert(line.split(":")[1].strip())
            elif "Epanechnikov KDE vibrational energy:" in line:
                data["Epanechnikov KDE vibrational energy"] = safe_float_convert(line.split(":")[1].strip())
            elif "Total number of phonons is:" in line:
                data["Total number of phonons"] = int(line.split(":")[1].strip())
            elif "Total number of sampled unique k-points:" in line:
                data["Total number of sampled unique k-points"] = int(line.split(":")[1].strip())
    
    return data


# Loop through all subdirectories and process .out files
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".out"):
            # Extract crystal name, ID, and k-point value from the path
            parts = root.split(os.sep)
            crystal_name = parts[-4]  # Changed from -3 to -4
            crystal_id = parts[-3]    # Changed from -2 to -3
            k_value = parts[-1].split("_")[-1]
            
            # Parse the .out file
            file_path = os.path.join(root, file)
            parsed_data = parse_out_file(file_path)
            
            # Create a suitable CSV filename
            csv_filename = f"{crystal_name}_{crystal_id}_k-value-{k_value}.csv"
            
            # Create crystal-specific output directory
            crystal_output_dir = os.path.join(output_dir, crystal_name)
            os.makedirs(crystal_output_dir, exist_ok=True)
            
            csv_path = os.path.join(crystal_output_dir, csv_filename)
            
            # Write the extracted data to the CSV file
            with open(csv_path, mode="w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Property", "Value"])
                for key, value in parsed_data.items():
                    writer.writerow([key, value])

print("Processing complete. CSV files saved and organized by crystal.")
