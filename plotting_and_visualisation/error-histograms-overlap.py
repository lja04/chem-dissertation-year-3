import os
import csv
from collections import defaultdict
import sys
import numpy as np
import matplotlib.pyplot as plt

def calculate_statistics(errors):
    mean_signed_error = np.mean(errors)
    mean_absolute_error = np.mean(np.abs(errors))
    max_absolute_error = np.max(np.abs(errors))
    return mean_signed_error, mean_absolute_error, max_absolute_error

def main():
    input_dir = "split-files"
    output_dir = "energy-difference-error-data"
    stats_output_file = "k_point_error_statistics.csv"

    data = defaultdict(lambda: defaultdict(dict))
    crystal_statistics = {}
    k_point_errors = defaultdict(list)

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

    # Calculate errors and statistics for each crystal
    for crystal_name, k_points in sorted(data.items()):
        errors = []
        reference_difference = None
        
        for k_point in sorted(k_points.keys()):
            polymorphs = list(k_points[k_point].keys())
            if len(polymorphs) == 2:
                energy_difference = abs(k_points[k_point][polymorphs[0]] - k_points[k_point][polymorphs[1]])
                
                if k_point == 0.10:
                    reference_difference = energy_difference
                
                if reference_difference is not None:
                    error = energy_difference - reference_difference
                    errors.append(error)
                    if k_point != 0.10:
                        k_point_errors[k_point].append(error)
            else:
                print(f"Warning: Expected 2 polymorphs for crystal {crystal_name} at K-Point {k_point}, found {len(polymorphs)}")
        
        # Calculate statistics
        mean_signed_error, mean_absolute_error, max_absolute_error = calculate_statistics(errors)
        crystal_statistics[crystal_name] = {
            'Mean Signed Error': mean_signed_error,
            'Mean Absolute Error': mean_absolute_error,
            'Max Absolute Error': max_absolute_error
        }

    # Write statistics to a single CSV file
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, stats_output_file)
        with open(output_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Crystal', 'Mean Signed Error', 'Mean Absolute Error', 'Max Absolute Error'])
            
            for crystal, stats in sorted(crystal_statistics.items()):
                csv_writer.writerow([
                    crystal, 
                    stats['Mean Signed Error'], 
                    stats['Mean Absolute Error'], 
                    stats['Max Absolute Error']
                ])
            
        print(f"Statistics saved to {output_path}")
    except IOError as e:
        print(f"Error writing statistics file: {e}")

    # Create overlapping histograms
    plt.figure(figsize=(12, 8))

    for k_point, errors in sorted(k_point_errors.items()):
        plt.hist(errors, bins=20, alpha=0.5, label=f'K-point {k_point}')

    plt.xlabel('Error')
    plt.ylabel('Frequency')
    plt.title('Histogram of Errors at Each K-point Spacing')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'k_point_error_histograms_overlap.png'))
    plt.close()

if __name__ == "__main__":
    main()
