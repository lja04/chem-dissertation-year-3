import os
import csv

def extract_k_points(directory):
    # List to store extracted data
    results = []

    # Walk through the directory and process each file
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".out"):  # Process all .out files
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        for line in f:
                            if "Total number of sampled unique k-points:" in line:
                                # Extract the number of k-points from the line
                                k_points = int(line.split(":")[1].strip())
                                
                                # Extract crystal name from the directory structure
                                relative_path = os.path.relpath(file_path, directory)
                                parts = relative_path.split(os.sep)
                                crystal_name = '/'.join(parts[:-1])  # Crystal name is derived from the folder structure

                                # Extract k-point value from the parent directory name
                                k_point_value_str = parts[-2]  # Assuming it's in the parent directory
                                k_point_value = float(k_point_value_str.split('_')[-1])  # Extracting from 'k_value_0.25'

                                # Append to results
                                results.append([f"{crystal_name}/k-value-{k_point_value:.2f}", k_point_value, k_points])
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return results

def save_to_csv(data, output_file):
    # Sort data alphabetically by crystal name and numerically by k-point value
    data.sort(key=lambda x: (x[0], x[1]))

    # Write to CSV file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Crystal Name', 'K-Point', 'Number of Sampled Unique K-Points'])
        csv_writer.writerows(data)

def main():
    input_directory = "crystal-files"
    output_file = "number-of-sampled-k-points.csv"

    # Extract data
    data = extract_k_points(input_directory)

    # Save to CSV
    save_to_csv(data, output_file)

    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
