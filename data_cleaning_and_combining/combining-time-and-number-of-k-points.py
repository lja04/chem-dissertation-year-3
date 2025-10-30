import csv
import os

def reformat_name(name):
    # Extract parts from the original name
    parts = name.split('/')
    crystal = parts[0]
    polymer_number = parts[1]
    k_point = parts[-1].split('-')[-1]  # Extract the k-point value (e.g., "0.10")
    return f"{crystal}_{polymer_number}_{k_point}"

def combine_csvs(time_file, k_points_file, output_file):
    # Read the time data
    time_data = {}
    with open(time_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            reformatted_name = reformat_name(row['Name'])
            time_data[reformatted_name] = {
                'Total Time (seconds)': row['Total Time (seconds)'],
                'Total Time (minutes)': row['Total Time (minutes)'],
                'Total Time (hours)': row['Total Time (hours)']
            }

    # Read the k-points data and merge with time data
    combined_data = []
    with open(k_points_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            reformatted_name = reformat_name(row['Crystal Name'])
            if reformatted_name in time_data:
                combined_row = {
                    'Name': reformatted_name,
                    'Total Time (seconds)': time_data[reformatted_name]['Total Time (seconds)'],
                    'Total Time (minutes)': time_data[reformatted_name]['Total Time (minutes)'],
                    'Total Time (hours)': time_data[reformatted_name]['Total Time (hours)'],
                    'Number of Sampled Unique K-Points': row['Number of Sampled Unique K-Points']
                }
                combined_data.append(combined_row)

    # Write the combined data to a new CSV file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', newline='') as file:
        fieldnames = ['Name', 'Total Time (seconds)', 'Total Time (minutes)', 
                      'Total Time (hours)', 'Number of Sampled Unique K-Points']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(combined_data)

    print(f"Combined CSV saved to: {output_file}")

def main():
    # File paths
    time_file = "total_run_times.csv"  # Replace with your actual path
    k_points_file = "number-of-sampled-k-points.csv"  # Replace with your actual path
    output_file = "time-and-number-of-k-points.csv"  # Replace with your actual path

    # Combine the CSVs
    combine_csvs(time_file, k_points_file, output_file)

if __name__ == "__main__":
    main()
