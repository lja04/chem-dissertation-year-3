import csv
import sys
from pathlib import Path
import traceback

# Define directories
CRYSTALS_ROOT = "results-3"
RESULTS_DIR = "results-3"

def extract_free_energy(output_file):
    """Extract free energy with better debugging"""
    try:
        with open(output_file, "r") as file:
            content = file.read()
            print(f"DEBUG: Checking {output_file}")
            
            # More flexible energy pattern matching
            for line in content.split('\n'):
                if "Epanechnikov KDE vibrational energy:" in line:
                    try:
                        energy = float(line.split()[-2])
                        print(f"DEBUG: Found energy: {energy}")
                        return energy
                    except (IndexError, ValueError):
                        print(f"DEBUG: Couldn't parse energy from line: {line.strip()}")
    except IOError:
        print(f"DEBUG: Couldn't read {output_file}")
    return None

def process_crystal(crystal_name):
    try:
        root_dir = Path(CRYSTALS_ROOT) / crystal_name / "structure-files"
        csv_file = Path(CRYSTALS_ROOT) / crystal_name / "structures.csv"
        output_csv = Path(RESULTS_DIR) / f"{crystal_name}-ranking.csv"
        
        print(f"\nProcessing {crystal_name}")
        print(f"CSV path: {csv_file}")
        print(f"Structure-files path: {root_dir}")

        if not csv_file.exists():
            print("ERROR: Missing structures.csv")
            return
            
        data = []
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            print(f"DEBUG: CSV headers: {reader.fieldnames}")
            
            for row_num, row in enumerate(reader, 1):
                folder_name = row.get("id", "").strip()
                if not folder_name:
                    print(f"WARNING: Row {row_num} has empty/missing ID")
                    continue
                
                # Handle case sensitivity and formatting
                out_file_name = f"{folder_name}.out"
                output_file = root_dir / folder_name / out_file_name
                
                print(f"\nDEBUG: Processing structure {row_num}: {folder_name}")
                print(f"DEBUG: Expected .out path: {output_file}")
                
                free_energy = None
                if output_file.exists():
                    free_energy = extract_free_energy(output_file)
                else:
                    print(f"DEBUG: Alternate path attempt for {folder_name}")
                    # Try case-insensitive search
                    matching_dirs = [d for d in root_dir.iterdir() 
                                   if d.is_dir() and d.name.lower() == folder_name.lower()]
                    if matching_dirs:
                        alt_path = matching_dirs[0] / f"{matching_dirs[0].name}.out"
                        if alt_path.exists():
                            print(f"DEBUG: Found alternate path: {alt_path}")
                            free_energy = extract_free_energy(alt_path)
                
                if free_energy is not None:
                    row["free energy"] = free_energy
                    row["new energy"] = float(row["energy"]) + free_energy
                    data.append(row)
                else:
                    print(f"WARNING: No valid energy data for {folder_name}")
                    # Include anyway with 0 free energy
                    row["free energy"] = 0.0
                    row["new energy"] = float(row["energy"])
                    data.append(row)
        
        if not data:
            print("ERROR: No data processed - check debug output above")
            return

        # Calculate ranks
        data.sort(key=lambda x: float(x["energy"]))
        original_ranks = {row["id"]: i+1 for i, row in enumerate(data)}
        data.sort(key=lambda x: float(x["new energy"]))
        new_ranks = {row["id"]: i+1 for i, row in enumerate(data)}

        # Write output
        fieldnames = [
            "id", "spacegroup", "density", "energy", "minimization_step",
            "trial_number", "minimization_time", "free energy", "new energy",
            "original rank", "new rank"
        ]
        
        with open(output_csv, "w") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                row["original rank"] = original_ranks[row["id"]]
                row["new rank"] = new_ranks[row["id"]]
                writer.writerow(row)
        
        print(f"\nSUCCESS: Created {output_csv}")
        print(f"Processed {len(data)} structures")

    except Exception as e:
        print(f"\nERROR processing {crystal_name}:")
        traceback.print_exc()

if __name__ == "__main__":
    crystal_dirs = [d for d in Path(CRYSTALS_ROOT).iterdir() if d.is_dir()]
    if not crystal_dirs:
        print(f"No crystal directories found in {CRYSTALS_ROOT}")
        sys.exit(1)
    
    for crystal_dir in crystal_dirs:
        process_crystal(crystal_dir.name)