import os
import pandas as pd
from pathlib import Path

# Define paths
results_dir = Path("results-2")
totalset_dir = results_dir / "totalset"
final_ranks_file = Path("final_ranks_with_Sohncke.txt")
output_file = results_dir / "energy_rank_changes.txt"

def parse_final_ranks(file_path):
    """Parse the final ranks file and extract crystal names and their ranks"""
    observed_crystals = {}
    with open(file_path, 'r') as f:
        # Skip header
        next(f)
        for line in f:
            parts = line.split()
            if len(parts) >= 2 and "None" not in parts[1]:
                refcode = parts[0]
                crystal_name = parts[1]
                numerical_rank = int(parts[-1]) if parts[-1] != "None" else None
                observed_crystals[crystal_name] = {
                    'refcode': refcode,
                    'numerical_rank': numerical_rank
                }
    return observed_crystals

def process_totalset_data(totalset_dir, observed_crystals):
    """Process all CSV files in totalset directory and collect rank change info"""
    rank_changes = []
    
    # Get all CSV files in totalset directory
    csv_files = [f for f in totalset_dir.glob('*.csv') if f.is_file()]
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            
            # Check if we have the required columns
            required_cols = ['id', 'original rank', 'new rank']
            if not all(col in df.columns for col in required_cols):
                continue
                
            # Find matching crystals
            for crystal_name in observed_crystals:
                if crystal_name in df['id'].values:
                    crystal_data = df[df['id'] == crystal_name].iloc[0]
                    observed_data = observed_crystals[crystal_name]
                    
                    rank_change = {
                        'refcode': observed_data['refcode'],
                        'crystal_name': crystal_name,
                        'original_rank': int(crystal_data['original rank']),
                        'new_rank': int(crystal_data['new rank']),
                        'observed_rank': observed_data['numerical_rank'],
                        'rank_change': int(crystal_data['original rank']) - int(crystal_data['new rank']),
                        'file': csv_file.name
                    }
                    rank_changes.append(rank_change)
                    
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")
            continue
            
    return rank_changes

def save_results(rank_changes, output_file):
    """Save the rank change analysis to a file"""
    with open(output_file, 'w') as f:
        # Write header
        f.write("Refcode\tCrystal Name\tOriginal Rank\tNew Rank\tObserved Rank\tRank Change (Original-New)\tFile\n")
        
        # Sort by refcode
        rank_changes_sorted = sorted(rank_changes, key=lambda x: x['refcode'])
        
        for change in rank_changes_sorted:
            f.write(f"{change['refcode']}\t{change['crystal_name']}\t{change['original_rank']}\t")
            f.write(f"{change['new_rank']}\t{change['observed_rank']}\t{change['rank_change']}\t")
            f.write(f"{change['file']}\n")
            
    print(f"Results saved to {output_file}")

def main():
    # Parse the observed crystals
    observed_crystals = parse_final_ranks(final_ranks_file)
    print(f"Found {len(observed_crystals)} observed crystals in the final ranks file.")
    
    # Process the totalset data
    rank_changes = process_totalset_data(totalset_dir, observed_crystals)
    print(f"Found rank data for {len(rank_changes)} observed crystals in the totalset directory.")
    
    # Save results
    save_results(rank_changes, output_file)

if __name__ == "__main__":
    main()