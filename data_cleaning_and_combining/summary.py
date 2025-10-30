import csv
from pathlib import Path
import traceback

# Define directories
CRYSTALS_ROOT = "crystals-2"
RESULTS_DIR = "totalset"
OUTPUT_TXT = Path(RESULTS_DIR) / "summary_ranking.txt"

def process_ranking_csv(csv_file):
    """Extract top-ranked structures from a ranking CSV file"""
    try:
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)
            
            if not data:
                print(f"WARNING: Empty CSV file {csv_file}")
                return None, None, None
            
            # Find structure with best new energy (lowest value)
            best_new = min(data, key=lambda x: float(x["new energy"]))
            
            # Find structure with best original energy (lowest value)
            best_original = min(data, key=lambda x: float(x["energy"]))
            
            crystal_name = csv_file.stem.replace("-ranking", "")
            
            return crystal_name, best_original, best_new
            
    except Exception as e:
        print(f"ERROR processing {csv_file}:")
        traceback.print_exc()
        return None, None, None

def create_summary_txt():
    """Create a summary text file from all ranking CSV files"""
    try:
        # Find all ranking CSV files
        ranking_files = list(Path(RESULTS_DIR).glob("*-ranking.csv"))
        
        if not ranking_files:
            print(f"No ranking CSV files found in {RESULTS_DIR}")
            return
        
        print(f"Found {len(ranking_files)} ranking files to process")
        
        # Process each CSV file and collect results
        results = []
        for csv_file in ranking_files:
            crystal_name, best_original, best_new = process_ranking_csv(csv_file)
            if crystal_name:
                results.append((crystal_name, best_original, best_new))
        
        # Write summary text file
        with open(OUTPUT_TXT, "w") as txt_file:
            txt_file.write("Summary of Top-Ranked Structures\n")
            txt_file.write("="*40 + "\n\n")
            
            for crystal_name, best_original, best_new in results:
                txt_file.write(f"Crystal: {crystal_name}\n")
                txt_file.write("-"*40 + "\n")
                
                txt_file.write("Best Original Energy Structure:\n")
                txt_file.write(f"  ID: {best_original['id']}\n")
                txt_file.write(f"  Spacegroup: {best_original['spacegroup']}\n")
                txt_file.write(f"  Density: {best_original['density']}\n")
                txt_file.write(f"  Energy: {best_original['energy']}\n")
                txt_file.write(f"  Rank: {best_original['original rank']}\n\n")
                
                txt_file.write("Best New Energy Structure (with vibrational correction):\n")
                txt_file.write(f"  ID: {best_new['id']}\n")
                txt_file.write(f"  Spacegroup: {best_new['spacegroup']}\n")
                txt_file.write(f"  Density: {best_new['density']}\n")
                txt_file.write(f"  Energy: {best_new['energy']}\n")
                txt_file.write(f"  Free Energy: {best_new['free energy']}\n")
                txt_file.write(f"  New Energy: {best_new['new energy']}\n")
                txt_file.write(f"  Rank: {best_new['new rank']}\n\n")
                
                txt_file.write("="*40 + "\n\n")
        
        print(f"\nSUCCESS: Created summary file at {OUTPUT_TXT}")
        
    except Exception as e:
        print("\nERROR creating summary:")
        traceback.print_exc()

if __name__ == "__main__":
    create_summary_txt()