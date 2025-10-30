import os
import csv
from collections import defaultdict
import sys

def main():
    # Input and output directories
    input_dir = "split-files"
    output_dir = "energy-difference-combined-data"
    output_file = "combined-energy-difference-with-debye-and-kde.csv"

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

    # Calculate differences and prepare output data
    output_data = []
    for crystal_name, k_points in sorted(data.items()):
        for k_point in sorted(k_points.keys()):
            polymorphs = list(k_points[k_point].keys())
            if len(polymorphs) == 2:
                energy1 = k_points[k_point][polymorphs[0]]
                energy2 = k_points[k_point][polymorphs[1]]
                difference = abs(energy1 - energy2)
                output_data.append([crystal_name, k_point, difference])
            else:
                print(f"Warning: Expected 2 polymorphs for crystal {crystal_name} at K-Point {k_point}, found {len(polymorphs)}")

    # Write output to CSV file
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_file)
        with open(output_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Crystal', 'K-Point', 'Energy Difference'])
            csv_writer.writerows(output_data)
        print(f"Output saved to {output_path}")
    except IOError as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
