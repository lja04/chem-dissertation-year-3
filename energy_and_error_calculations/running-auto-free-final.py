import subprocess
import csv
from pathlib import Path

# Define the root directory containing your folders
CRYSTAL_NAME = "cumjoj"
ROOT_DIR = f"{CRYSTAL_NAME}/structure-files"
CSV_FILE = f"{CRYSTAL_NAME}/structures.csv"
OUTPUT_CSV = f"{CRYSTAL_NAME}/structures-ranking.csv"

def run_autofree_in_folders(root_dir):
    """Run 'python AutoFree.py > {name}.out' in each folder."""
    for folder in Path(root_dir).iterdir():
        if folder.is_dir():  # Check if it's a directory
            autofree_script = folder / "AutoFree.py"
            if autofree_script.exists():
                output_file = folder / f"{folder.name}.out"  # Output file named after the folder
                print(f"Running AutoFree.py in: {folder.name}")
                try:
                    # Run the command and redirect output to the output file
                    with open(output_file, "w") as outfile:
                        subprocess.run(
                            ["python", str(autofree_script)],
                            stdout=outfile,
                            stderr=subprocess.PIPE,
                            text=True,
                            cwd=folder
                        )
                    print(f"Output saved to: {output_file}")
                except Exception as e:
                    print(f"Error running AutoFree.py in {folder.name}: {e}")
            else:
                print(f"Skipping {folder.name}: AutoFree.py not found")
        else:
            print(f"Skipping {folder.name}: Not a directory")

def extract_free_energy(output_file):
    """Extract the free energy from the .out file."""
    free_energy = None
    with open(output_file, "r") as file:
        for line in file:
            if "Epanechnikov KDE vibrational energy:" in line:
                free_energy = float(line.split()[-2])  # Extract the free energy value
                break
    return free_energy

def process_csv(csv_file, output_csv, root_dir):
    """Process the CSV file and calculate rankings."""
    data = []
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames  # Get all column names from the input CSV
        for row in reader:
            data.append(row)

    # Sort by energy and add original rank
    data.sort(key=lambda x: float(x["energy"]))
    for i, row in enumerate(data):
        row["original rank"] = i + 1

    # Add free energy, new energy, and new rank
    for row in data:
        folder_name = row["id"]
        output_file = Path(root_dir) / folder_name / f"{folder_name}.out"
        if output_file.exists():
            free_energy = extract_free_energy(output_file)
            if free_energy is not None:
                row["free energy"] = free_energy
                row["new energy"] = float(row["energy"]) + free_energy
            else:
                row["free energy"] = "N/A"
                row["new energy"] = "N/A"
        else:
            row["free energy"] = "N/A"
            row["new energy"] = "N/A"

    # Sort by new energy and add new rank
    data.sort(key=lambda x: float(x["new energy"]) if x["new energy"] != "N/A" else float('inf'))
    for i, row in enumerate(data):
        row["new rank"] = i + 1 if row["new energy"] != "N/A" else "N/A"

    # Define the desired column order
    desired_fieldnames = [
        "id",
        "spacegroup",
        "density",
        "energy",
        "minimization_step",
        "trial_number",
        "minimization_time",
        "free energy",
        "new energy",
        "original rank",
        "new rank",
    ]

    # Write to the new CSV file with the desired column order
    with open(output_csv, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=desired_fieldnames)
        writer.writeheader()
        for row in data:
            # Ensure all desired columns are present in the row
            writer.writerow({field: row.get(field, "N/A") for field in desired_fieldnames})

if __name__ == "__main__":
    # Step 1: Run AutoFree.py in each folder
    #run_autofree_in_folders(ROOT_DIR)

    # Step 2: Process the CSV file and calculate rankings
    process_csv(CSV_FILE, OUTPUT_CSV, ROOT_DIR)

    print("AutoFree.py execution and CSV processing completed")