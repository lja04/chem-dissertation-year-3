import csv
import sys
from pathlib import Path
import traceback

# Define directories
CRYSTALS_ROOT = "crystals-2"
RESULTS_DIR = "results-2/set5"
OBSERVED_CRYSTALS_FILE = "final_ranks_with_Sohncke.txt"

def extract_free_energy(output_file):
    """Extract the free energy from the .out file."""
    free_energy = None
    try:
        with open(output_file, "r") as file:
            for line in file:
                if "Epanechnikov KDE vibrational energy:" in line:
                    free_energy = float(line.split()[-2])
                    break
    except FileNotFoundError:
        print(f"Warning: Output file not found - {output_file}")
    return free_energy

def load_observed_structures():
    """Load the observed crystal structure IDs from file."""
    observed = set()
    try:
        with open(OBSERVED_CRYSTALS_FILE, "r") as f:
            for line in f:
                # Skip empty lines and header-like lines
                if not line.strip() or line.startswith("Refcode"):
                    continue
                
                # Extract the structure ID (second column)
                parts = line.split()
                if len(parts) >= 2:
                    structure_id = parts[1].strip()
                    if '-QR-' in structure_id:  # Validate it's a structure ID
                        observed.add(structure_id)
    except FileNotFoundError:
        print(f"Warning: Observed structures file not found - {OBSERVED_CRYSTALS_FILE}")
    return observed

def process_crystal(crystal_name, observed_structures, summary_file):
    """Process a single crystal's data and return statistics."""
    stats = {
        'total_observed': 0,
        'improved': 0,
        'worsened': 0,
        'unchanged': 0,
        'not_found': 0
    }
    
    try:
        root_dir = Path(CRYSTALS_ROOT) / crystal_name / "structure-files"
        csv_file = Path(CRYSTALS_ROOT) / crystal_name / "structures.csv"
        output_csv = Path(RESULTS_DIR) / f"{crystal_name}-ranking.csv"
        
        if not root_dir.exists() or not csv_file.exists():
            return stats
            
        # Read and process data
        data = []
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                folder_name = row["id"]
                output_file = root_dir / folder_name / f"{folder_name}.out"
                if output_file.exists():
                    free_energy = extract_free_energy(output_file)
                    if free_energy is not None:
                        row["free energy"] = free_energy
                        row["new energy"] = float(row["energy"]) + free_energy
                        data.append(row)
        
        if not data:
            return stats

        # Calculate ranks
        data.sort(key=lambda x: float(x["energy"]))
        original_ranks = {row["id"]: i+1 for i, row in enumerate(data)}
        data.sort(key=lambda x: float(x["new energy"]))
        new_ranks = {row["id"]: i+1 for i, row in enumerate(data)}

        # Check for observed structures
        crystal_observed = [s for s in observed_structures if s.startswith(f"{crystal_name}-")]
        if not crystal_observed:
            return stats
            
        stats['total_observed'] = len(crystal_observed)
        
        with open(summary_file, "a") as f:
            f.write(f"\nObserved structure(s) for {crystal_name}:\n")
            for struct_id in crystal_observed:
                if struct_id in original_ranks and struct_id in new_ranks:
                    old_rank = original_ranks[struct_id]
                    new_rank = new_ranks[struct_id]
                    change = new_rank - old_rank
                    
                    if change < 0:
                        result = "improved"
                        stats['improved'] += 1
                    elif change > 0:
                        result = "worsened"
                        stats['worsened'] += 1
                    else:
                        result = "unchanged"
                        stats['unchanged'] += 1
                        
                    f.write(f"- {struct_id}\n")
                    f.write(f"  Rank: {old_rank} → {new_rank} ({result})\n")
                    f.write(f"  Energy: {float([r['energy'] for r in data if r['id'] == struct_id][0]):.4f}")
                    f.write(f" → {float([r['new energy'] for r in data if r['id'] == struct_id][0]):.4f}\n")
                else:
                    f.write(f"- {struct_id} (not found in rankings)\n")
                    stats['not_found'] += 1

        # Write the output CSV
        desired_fieldnames = [
            "id", "spacegroup", "density", "energy", "minimization_step",
            "trial_number", "minimization_time", "free energy", "new energy",
            "original rank", "new rank"
        ]
        
        with open(output_csv, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=desired_fieldnames)
            writer.writeheader()
            for row in data:
                row["original rank"] = original_ranks[row["id"]]
                row["new rank"] = new_ranks[row["id"]]
                writer.writerow({field: row.get(field, "N/A") for field in desired_fieldnames})

        print(f"Processed {crystal_name}")

    except Exception as e:
        print(f"Error processing {crystal_name}:")
        traceback.print_exc()
    
    return stats

def process_all_crystals():
    """Main function to process all crystals and generate summary statistics."""
    # Ensure results directory exists
    Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)
    
    # Load observed structures
    observed_structures = load_observed_structures()
    print(f"Loaded {len(observed_structures)} observed structures")
    
    # Create summary file
    summary_file = Path(RESULTS_DIR) / "free_energy_impact_summary.txt"
    with open(summary_file, "w") as f:
        f.write("Impact of Free Energy Correction on Observed Crystal Structures\n")
        f.write("="*80 + "\n\n")
    
    # Initialize counters
    stats = {
        'total_observed': 0,
        'improved': 0,
        'worsened': 0,
        'unchanged': 0,
        'not_found': 0
    }
    
    # Get list of all crystal directories
    crystal_dirs = [d.name for d in Path(CRYSTALS_ROOT).iterdir() if d.is_dir()]
    
    if not crystal_dirs:
        print(f"No crystal directories found in {CRYSTALS_ROOT}")
        sys.exit(1)
    
    for crystal_name in crystal_dirs:
        print(f"\n{'='*50}")
        print(f"Processing crystal: {crystal_name}")
        print(f"{'='*50}")
        
        # Process crystal and update statistics
        crystal_stats = process_crystal(crystal_name, observed_structures, summary_file)
        for key in stats:
            stats[key] += crystal_stats.get(key, 0)
    
    # Write final statistics to summary file
    with open(summary_file, "a") as f:
        f.write("\n" + "="*80 + "\n")
        f.write("SUMMARY STATISTICS\n")
        f.write("="*80 + "\n")
        f.write(f"Total observed structures processed: {stats['total_observed']}\n")
        f.write(f"Structures with improved ranking: {stats['improved']} ({stats['improved']/stats['total_observed']:.1%})\n")
        f.write(f"Structures with worsened ranking: {stats['worsened']} ({stats['worsened']/stats['total_observed']:.1%})\n")
        f.write(f"Structures with unchanged ranking: {stats['unchanged']} ({stats['unchanged']/stats['total_observed']:.1%})\n")
        if stats['not_found'] > 0:
            f.write(f"\nWarning: {stats['not_found']} observed structures were not found in rankings\n")
    
    print("\nProcessing complete for all crystals")
    print(f"Summary saved to: {summary_file}")
    print("\nFinal Statistics:")
    print(f"- Improved: {stats['improved']} ({stats['improved']/stats['total_observed']:.1%})")
    print(f"- Worsened: {stats['worsened']} ({stats['worsened']/stats['total_observed']:.1%})")
    print(f"- Unchanged: {stats['unchanged']} ({stats['unchanged']/stats['total_observed']:.1%})")
    if stats['not_found'] > 0:
        print(f"- Not found: {stats['not_found']}")

if __name__ == "__main__":
    process_all_crystals()