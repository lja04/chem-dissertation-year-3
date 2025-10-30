import os
import csv
from collections import defaultdict
import sys

def main():
    # Input and output directories
    input_dir = "split-files"
    output_dir = "energy-difference-error-data"

    # Dictionary to store data
    data = defaultdict(lambda: defaultdict(dict))

    # Read all CSV files in the input directory
    try:
        for filename in os.listdir(input_dir):
            if filename.endswith(".csv"):
                crystal_name, polymorph = filename.split("_")[:2]
                file_path = os.path.join(input_dir, filename)
                try:
                    with open(file_path, 'r') as file:
                        csv_reader = csv.DictReader(file)
                        for row in csv_reader:
                            try:
                                k_point = float(row['K-Point'])
                                energy = float(row['Energy with Debye and KDE'])
                                data[crystal_name][k_point][polymorph] = energy
                            except KeyError as e:
                                print(f"Error: Missing column in file {filename}: {e}")
                            except ValueError as e:
                                print(f"Error: Invalid data in file {filename}: {e}")
                except IOError as e:
                    print(f"Error reading file {filename}: {e}")
    except OSError as e:
        print(f"Error accessing input directory: {e}")
        sys.exit(1)

    # Calculate errors and save to separate CSV files for each crystal
    for crystal_name, k_points in sorted(data.items()):
        output_data = []
        reference_difference = None
        
        for k_point in sorted(k_points.keys()):
            polymorphs = list(k_points[k_point].keys())
            if len(polymorphs) == 2:
                energy_difference = abs(k_points[k_point][polymorphs[0]] - k_points[k_point][polymorphs[1]])
                
                if k_point == 0.10:
                    reference_difference = energy_difference
                
                if reference_difference is not None:
                    error = energy_difference - reference_difference
                    output_data.append([k_point, energy_difference, error])
            else:
                print(f"Warning: Expected 2 polymorphs for crystal {crystal_name} at K-Point {k_point}, found {len(polymorphs)}")
        
        # Write output to CSV file for this crystal
        try:
            os.makedirs(output_dir, exist_ok=True)
            output_file = f"{crystal_name}_k_point_errors.csv"
            output_path = os.path.join(output_dir, output_file)
            with open(output_path, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(['K-Point', 'Energy Difference', 'Error'])
                csv_writer.writerows(output_data)
            print(f"Output saved to {output_path}")
        except IOError as e:
            print(f"Error writing output file for crystal {crystal_name}: {e}")

if __name__ == "__main__":
    main()
