import os
import pandas as pd

# Define the base directory containing the crystal data
base_directory = "crystals"

# Initialize a list to store the results
results = []

# Loop through each crystal directory
for crystal in os.listdir(base_directory):
    crystal_path = os.path.join(base_directory, crystal)
    
    # Check if it's a directory
    if os.path.isdir(crystal_path):
        # Loop through each polymorph directory
        for polymorph in os.listdir(crystal_path):
            polymorph_path = os.path.join(crystal_path, polymorph)
            
            # Check if it's a directory
            if os.path.isdir(polymorph_path):
                # Loop through each k-value directory
                for k_value in os.listdir(polymorph_path):
                    k_value_path = os.path.join(polymorph_path, k_value)
                    
                    # Check if it's a directory
                    if os.path.isdir(k_value_path):
                        total_run_time = 0.0  # Initialize total run time for this k-value

                        print(f"Processing: {crystal}/{polymorph}/{k_value}")
                        
                        # Look for CSV files in the k-value directory
                        csv_found = False  # Track if any CSV file is found
                        for file in os.listdir(k_value_path):
                            if file.endswith(".csv"):
                                csv_found = True
                                file_path = os.path.join(k_value_path, file)
                                
                                try:
                                    # Read the CSV file
                                    df = pd.read_csv(file_path)
                                    
                                    # Check if 'Metric' and 'Time (CPU seconds)' columns exist
                                    if 'Metric' in df.columns and 'Time (CPU seconds)' in df.columns:
                                        # Extract 'Total run time' value from the file
                                        total_time_row = df[df['Metric'] == 'Total run time']
                                        if not total_time_row.empty:
                                            total_run_time += total_time_row['Time (CPU seconds)'].iloc[0]
                                        else:
                                            print(f"Warning: 'Total run time' not found in {file_path}")
                                    else:
                                        print(f"Warning: Required columns missing in {file_path}")
                                except Exception as e:
                                    print(f"Error reading {file_path}: {e}")
                        
                        if not csv_found:
                            print(f"Warning: No CSV files found in {k_value_path}")
                        
                        # Prepare the name for output
                        name = f"{crystal}/{polymorph}/{k_value}"
                        
                        # Append the result to the list
                        results.append({"Name": name, "Total Time (seconds)": total_run_time})

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Extract k-value from the Name column for sorting purposes
results_df["k-value"] = results_df["Name"].str.extract(r"k-value-(\d+\.\d+)").astype(float)

# Sort by Name alphabetically and then by k-value numerically (ascending)
results_df_sorted = results_df.sort_values(by=["Name", "k-value"], ascending=[True, True])

# Drop the temporary 'k-value' column (not needed in output)
results_df_sorted = results_df_sorted.drop(columns=["k-value"])

# Calculate minutes and hours from total seconds and round to 2 decimal places
results_df_sorted["Total Time (minutes)"] = (results_df_sorted["Total Time (seconds)"] / 60).round(2)
results_df_sorted["Total Time (hours)"] = (results_df_sorted["Total Time (seconds)"] / 3600).round(2)

# Save the sorted DataFrame to a CSV file with additional time columns
output_file = "total_run_times.csv"
results_df_sorted.to_csv(output_file, index=False)

print(f"Total run times saved to {output_file}")
