import os
import re
import pandas as pd

# Define the input and output paths
input_folder = "autofree-out-files"
output_file = "k_points_phonons_summary.csv"

# Initialize a list to store the extracted data
data = []

# Loop through all .out files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".out"):
        file_path = os.path.join(input_folder, filename)
        
        # Extract the name without the .out extension
        name = filename.replace(".out", "")
        
        # Initialize variables to store k-points and phonons
        k_points = None
        phonons = None
        
        # Open and read the file line by line
        with open(file_path, "r") as file:
            for line in file:
                # Search for the line containing k-points
                if "Total number of sampled unique k-points:" in line:
                    k_points_match = re.search(r"Total number of sampled unique k-points:\s+(\d+)", line)
                    if k_points_match:
                        k_points = int(k_points_match.group(1))
                
                # Search for the line containing phonons
                if "Total number of phonons is:" in line:
                    phonons_match = re.search(r"Total number of phonons is:\s+(\d+)", line)
                    if phonons_match:
                        phonons = int(phonons_match.group(1))
                
                # Break early if both values are found
                if k_points is not None and phonons is not None:
                    break
        
        # Append the extracted information to the data list
        if k_points is not None and phonons is not None:
            data.append({"Name": name, "Number of k-points": k_points, "Number of Phonons": phonons})

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

# Extract k-value from the Name column for sorting purposes
df["k-value"] = df["Name"].str.extract(r"k-value-(\d+\.\d+)").astype(float)

# Sort by Name alphabetically and then by k-value numerically (ascending)
df_sorted = df.sort_values(by=["Name", "k-value"], ascending=[True, True])

# Drop the temporary 'k-value' column (not needed in output)
df_sorted = df_sorted.drop(columns=["k-value"])

# Save the sorted DataFrame to a CSV file without headers or index
df_sorted.to_csv(output_file, index=False)

print(f"CSV file created successfully at {output_file}")
