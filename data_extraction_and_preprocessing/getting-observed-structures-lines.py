import os
import pandas as pd

# Define paths
csv_folder = "rankings"
observed_csv = "final_ranks_with_Sohncke.csv"
output_file = "observed-structures-from-csvs.csv"

# Load the list of observed crystals
observed_df = pd.read_csv(observed_csv)
observed_csp_matches = set(observed_df['CSP_Match'].str.lower())

# Store all found structures
found_structures = []
missing_csp_matches = observed_csp_matches.copy()

# Process each CSV file in the rankings folder
for filename in os.listdir(csv_folder):
    if filename.endswith(".csv"):
        filepath = os.path.join(csv_folder, filename)
        
        try:
            df = pd.read_csv(filepath)
            
            # Check if 'id' column exists (some files might have different column names)
            id_col = 'id' if 'id' in df.columns else None
            
            if id_col:
                # Find matching rows
                matches = df[df[id_col].str.lower().isin(observed_csp_matches)]
                
                if not matches.empty:
                    # Add filename for reference
                    matches = matches.copy()
                    matches['SourceFile'] = filename
                    
                    found_structures.append(matches)
                    
                    # Update missing CSP matches
                    found_in_file = set(matches[id_col].str.lower())
                    missing_csp_matches -= found_in_file
                    
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

# Combine all found structures
if found_structures:
    final_df = pd.concat(found_structures, ignore_index=True)
    
    # Merge with observed data to get Refcodes
    final_df = pd.merge(
        final_df,
        observed_df[['CSP_Match', 'Refcode']],
        left_on='id',
        right_on='CSP_Match',
        how='left'
    )
    
    # Reorder columns to put Refcode first
    cols = ['Refcode', 'id'] + [col for col in final_df.columns if col not in ['Refcode', 'id', 'CSP_Match']]
    final_df = final_df[cols]
    
    # Save to CSV
    final_df.to_csv(output_file, index=False)
    print(f"Success! Found {len(final_df)} structures from {len(found_structures)} files.")
    print(f"Saved to: {output_file}")
    
    # Report missing CSP matches
    if missing_csp_matches:
        print(f"\nCould not find {len(missing_csp_matches)} CSP matches in any CSV files:")
        for csp in sorted(missing_csp_matches)[:10]:  # Show first 10
            print(f"  - {csp}")
        if len(missing_csp_matches) > 10:
            print(f"  ... and {len(missing_csp_matches)-10} more")
else:
    print("No matching structures found in any CSV files.")

# Show sample of output
if os.path.exists(output_file):
    sample_df = pd.read_csv(output_file)
    print("\nSample of output:")
    print(sample_df.head())