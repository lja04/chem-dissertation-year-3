import os
import re
import csv
import glob

def extract_sorting_keys(filename):
    crystal_name = filename.split('_')[0]
    type_number = int(re.search(r'_(\d+)-', filename).group(1))
    k_value = float(re.search(r'k-value-([\d.]+)', filename).group(1))
    ld_number = int(re.search(r'ld-(\d+)', filename).group(1))
    return (crystal_name, type_number, k_value, ld_number)

input_dir = 'raw-timing-data'
output_file = 'combined_timing_data.csv'

headers = [
    'crystal name',
    'time to set things up',
    'reciprocal space part of ewald sum',
    'real space part of ewald sum',
    'short range potential calculation',
    'energy calculation',
    'first derivative chain rule',
    'second derivative chain rule',
    'all other program sections',
    'total run time'
]

data_list = []

for filename in os.listdir(input_dir):
    if filename.endswith('.txt'):
        filepath = os.path.join(input_dir, filename)
        crystal_name = os.path.splitext(filename)[0]
        data = {'crystal name': crystal_name}
        
        with open(filepath, 'r') as f:
            for line in f:
                key, value = line.strip().split(': ')
                data[key.lower()] = value
        
        data_list.append(data)

sorted_data = sorted(data_list, key=lambda x: extract_sorting_keys(x['crystal name']))

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    writer.writerows(sorted_data)

print(f"Combined and sorted CSV file created: {output_file}")
