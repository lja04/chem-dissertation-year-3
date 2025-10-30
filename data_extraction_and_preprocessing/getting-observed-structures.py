import pandas as pd

# Define paths
input_file = "final_ranks_with_Sohncke.csv"
output_file = "observed_structures.csv"

# List of crystals to extract
crystals_to_extract = [
    "ADPRLA", "BEVCEK", "BEXGAM", "BOFWEZ", "BOQQUT", 
    "BUHMOH", "BUKLOK", "BZCOCT", "CUMJOJ", "DATJOA",
    "DIHIXL", "DIJDAE", "FAJGUS", "FECKIK", "FOCNIU",
    "FUCOUN", "FURPOP", "GEZKOL", "GILXAD", "GILXUX",
    "GINPIF", "GOCWEA", "GOLHAQ", "HIKFOW", "HOBBOP",
    "HQOXDO", "IZIJOQ", "JONVOX", "KEJYOP", "KIMCOY",
    "KISGUQ", "LENYOS", "NAHFOR", "NIHZOT", "PAZROZ",
    "PECWOK", "PHTHAO", "PIGTUX", "SALLIB", "SELCES",
    "TANMAT", "TAXNIR", "TOHZUL", "VENYUI", "VIGTUA",
    "WOCGOK", "XEZHAL", "ZUMKUN", "ZZZRNY"
]

try:
    # Read the input file (assuming comma-separated)
    df = pd.read_csv(input_file, header=None,
                   names=["Refcode", "CSP_Match", "Compack_RMSD", "Delta_E", "Density", "Numerical_Rank"])
    
    # Filter for exact uppercase matches
    filtered_df = df[df['Refcode'].isin(crystals_to_extract)]
    
    # Add the proper header with (0-indexed) notation
    header = "Refcode,CSP_Match,Compack_RMSD,Delta_E,Density,Numerical_Rank_(0-indexed)"
    
    # Save to new CSV file with header
    with open(output_file, 'w') as f:
        f.write(header + '\n')
        filtered_df.to_csv(f, index=False, header=False, line_terminator='\n')
    
    print(f"Success! Created {output_file} with {len(filtered_df)}/{len(crystals_to_extract)} crystals")
    
    # Check for missing crystals
    found = set(filtered_df['Refcode'])
    missing = [c for c in crystals_to_extract if c not in found]
    
    if missing:
        print("\nMissing crystals:")
        for crystal in missing:
            print(f"  - {crystal}")

except Exception as e:
    print(f"Error: {str(e)}")