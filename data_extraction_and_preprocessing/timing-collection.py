import os
import csv
from tqdm import tqdm  # For progress bar

# Define the base directory and output directory
base_dir = "crystal-files"
output_dir = "time-data"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to parse the dmaout file and extract timing information
def parse_dmaout(file_path):
    timings = {}
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if "Time to set things up" in line:
                timings["Time to set things up"] = float(line.split()[-1])
            elif "Reciprocal space part of Ewald sum" in line:
                timings["Reciprocal space part of Ewald sum"] = float(line.split()[-1])
            elif "Real space part of Ewald sum" in line:
                timings["Real space part of Ewald sum"] = float(line.split()[-1])
            elif "Short range potential calculation" in line:
                timings["Short range potential calculation"] = float(line.split()[-1])
            elif "Energy calculation" in line:
                timings["Energy calculation"] = float(line.split()[-1])
            elif "First derivative chain rule" in line:
                timings["First derivative chain rule"] = float(line.split()[-1])
            elif "Second derivative chain rule" in line:
                timings["Second derivative chain rule"] = float(line.split()[-1])
            elif "All other program sections" in line:
                timings["All other program sections"] = float(line.split()[-1])
            elif "Total run time" in line:
                timings["Total run time"] = float(line.split()[-1])
    return timings

# Function to process all dmaout files and save timing data
def process_dmaout_files(base_dir, output_dir):
    # Collect all dmaout files and their paths
    dmaout_files = []
    for root, _, files in os.walk(base_dir):
        for file_name in files:
            if file_name.endswith(".dmaout"):
                dmaout_files.append(os.path.join(root, file_name))
    
    # Process each dmaout file with a progress bar
    for file_path in tqdm(dmaout_files, desc="Processing dmaout files", unit="file"):
        # Extract metadata from the file path
        relative_path = os.path.relpath(os.path.dirname(file_path), base_dir)
        parts = relative_path.split(os.sep)
        
        if len(parts) >= 4:  # Ensure we have enough parts to extract metadata
            crystal = parts[0]
            polymorph = parts[1]
            k_value_folder = parts[3]
            k_value = k_value_folder.replace("k_value_", "")
            
            # Extract ld value from the file name
            file_name = os.path.basename(file_path)
            if ".res_" in file_name:
                ld_value = file_name.split(".res_")[1].split(".dmaout")[0]
            else:
                print(f"Warning: '{file_name}' does not contain '.res_', skipping this file.")
                continue  # Skip this iteration and move to the next file
            
            # Parse the dmaout file
            timing_data = parse_dmaout(file_path)
            
            # Prepare output CSV path with separated directories for polymorph and k-value
            output_file_name = f"{crystal}_{polymorph}_{ld_value}_k-value-{k_value}_timings.csv"
            output_file_path = os.path.join(output_dir, crystal, polymorph, f"k-value-{k_value}")
            
            # Ensure polymorph-specific and k-value-specific directories exist
            os.makedirs(output_file_path, exist_ok=True)
            
            # Write timing data to CSV
            with open(os.path.join(output_file_path, output_file_name), mode="w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Metric", "Time (CPU seconds)"])
                for key, value in timing_data.items():
                    writer.writerow([key, value])

# Run the processing function with a progress bar
process_dmaout_files(base_dir, output_dir)

print("Processing complete. Timing data saved.")
