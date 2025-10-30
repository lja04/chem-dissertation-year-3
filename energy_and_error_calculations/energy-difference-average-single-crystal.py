import os
import csv
from collections import defaultdict

# Directory containing your CSV files
directory = 'energy-data'

# Dictionary to store sums and counts for averaging
energy_sums = defaultdict(lambda: {'sum': 0, 'count': 0})

# Go through all CSV files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                section = row['Energy Section']
                difference = float(row['Difference'])
                energy_sums[section]['sum'] += difference
                energy_sums[section]['count'] += 1

# Calculate averages
averages = {section: data['sum'] / data['count'] for section, data in energy_sums.items()}

# Write results to a new CSV file
output_file = '/average_differences.csv'
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Energy Section', 'Average Difference'])
    for section, avg in averages.items():
        writer.writerow([section, avg])

print(f"Results written to {output_file}")
