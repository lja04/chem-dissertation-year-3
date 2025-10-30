import os
import csv
import pandas as pd  # For reading CSV files easily

# Define the input directory for averaged timing files and output file path
averages_dir = "averages"
output_csv = "consolidated_total_run_time.csv"

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# Initialize a list to store rows for the consolidated CSV
consolidated_data = []

# Loop through all files in the averages directory
for root, _, files in os.walk(averages_dir):
    for file_name in files:
        if file_name.endswith(".csv"):  # Only process CSV files
            file_path = os.path.join(root, file_name)

            # Extract metadata from the file name (crystal, polymorph, k-value)
            base_name = os.path.splitext(file_name)[0]  # Remove .csv extension
            parts = base_name.split("_")  # Split by underscores
            
            if len(parts) >= 4:  # Ensure there are enough parts to extract metadata
                crystal = parts[0]
                polymorph = parts[1]
                k_value = parts[2] + "_" + parts[3]  # Combine k-value prefix (e.g., "k-value-0.10")
                
                # Read the CSV file to get the total run time
                try:
                    df = pd.read_csv(file_path)
                    total_run_time_row = df[df["Metric"] == "Total run time"]  # Filter for "Total run time"
                    
                    if not total_run_time_row.empty:
                        total_run_time = total_run_time_row["Time (CPU seconds)"].values[0]  # Get the value

                        # Append data to the consolidated list
                        consolidated_data.append({
                            "Name": f"{crystal}_{polymorph}_{k_value}",
                            "Total Run Time": total_run_time,
                        })
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

# Write consolidated data to a new CSV file
with open(output_csv, mode="w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["Name", "Total Run Time"])
    writer.writeheader()  # Write header row
    writer.writerows(consolidated_data)  # Write all rows

print(f"Consolidated data saved to {output_csv}")
