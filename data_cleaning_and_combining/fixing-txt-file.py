import re
import pandas as pd

# Input and output file paths
input_file = "final_ranks_with_Sohncke.txt"
output_file = "final_ranks_with_Sohncke.csv"

def convert_spaces_to_csv(input_path, output_path):
    with open(input_path, 'r') as f_in, open(output_path, 'w') as f_out:
        for line in f_in:
            # Replace multiple spaces/tabs with single comma
            cleaned_line = re.sub(r'\s+', ',', line.strip())
            f_out.write(cleaned_line + '\n')

try:
    # Convert the file
    convert_spaces_to_csv(input_file, output_file)
    
    # Verify the conversion
    df = pd.read_csv(output_file, header=None, 
                    names=["Refcode", "CSP_Match", "Compack_RMSD", "Delta_E", "Density", "Numerical_Rank"])
    
    print(f"Successfully converted to CSV: {output_file}")
    print(f"Found {len(df)} records")
    print("\nFirst 5 rows:")
    print(df.head())

except Exception as e:
    print(f"Error: {str(e)}")