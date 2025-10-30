import csv

# Input and output file names
input_file = "output.csv"
output_file = "filtered_rmsd.csv"

# Threshold for filtering
rmsd_threshold = 0.3

# Read, filter, and write
with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    
    # Write header
    writer.writeheader()
    
    for row in reader:
        try:
            # Convert RMSD value to float and compare
            rmsd_value = float(row["RMSD30_of_match"])
            if rmsd_value <= rmsd_threshold:
                writer.writerow(row)
        except ValueError:
            # Skip rows with invalid numerical data
            continue

print(f"Filtered data saved to: {output_file}")
