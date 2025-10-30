import os
import shutil
import subprocess
from pathlib import Path

# Define the root directory containing your folders
ROOT_DIR = "structure-files"
CRYSTAL_NAME = "izijoq"  # Change this to your desired crystal name

# Fixed file paths
BONDLENGTHS_PATH = "bondlengths"
FITPOTS_PATH = "fit.pots"
DMA_SOURCE_DIR = "all-mults-mols-xyzs-files"
SCRIPTS_TO_COPY = [
    "AutoFree.py",
    "AutoLD.py",
]

def organize_res_files(target_dir):
    """Organize .res files into folders."""
    os.chdir(target_dir)
    for filename in os.listdir():
        if filename.endswith('.res'):
            base_name = os.path.splitext(filename)[0]
            os.makedirs(base_name, exist_ok=True)
            shutil.move(filename, os.path.join(base_name, filename))
    print("All .res files have been organized into their respective folders.")

def organize_crystal_files(target_dir):
    """Copy required files into each .res folder."""
    dma_file = os.path.join(DMA_SOURCE_DIR, f"{CRYSTAL_NAME}.dma")
    mols_file = os.path.join(DMA_SOURCE_DIR, f"{CRYSTAL_NAME}.mols")

    required_files = {
        "bondlengths": BONDLENGTHS_PATH,
        "fit.pots": FITPOTS_PATH,
        f"{CRYSTAL_NAME}.dma": dma_file,
        f"{CRYSTAL_NAME}.mols": mols_file
    }

    for name, path in required_files.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing required file: {name} at {path}")

    for folder in os.listdir(target_dir):
        folder_path = os.path.join(target_dir, folder)
        if os.path.isdir(folder_path):
            shutil.copy2(BONDLENGTHS_PATH, folder_path)
            shutil.copy2(FITPOTS_PATH, folder_path)
            shutil.copy2(dma_file, os.path.join(folder_path, f"{CRYSTAL_NAME}.dma"))
            shutil.copy2(mols_file, os.path.join(folder_path, f"{CRYSTAL_NAME}.mols"))
    print(f"All files moved to .res folders for {CRYSTAL_NAME}")

def create_fort22_files(target_dir):
    """Create fort.22 files in each folder."""
    for folder in os.listdir(target_dir):
        folder_path = os.path.join(target_dir, folder)
        if os.path.isdir(folder_path):
            res_filename = folder
            crystal_name = res_filename.split('-')[0]
            content = f"""I
{res_filename}.res
bondlengths
  4.0000
n
n
f
n
 0
y
{crystal_name}.dma
y
{crystal_name}.mols
n
y
fit.pots
"""
            with open(os.path.join(folder_path, "fort.22"), "w") as f:
                f.write(content)
    print("fort.22 files created in all folders")

def process_folders(root_dir):
    """Run neighcrys on each fort.22 file."""
    for folder in Path(root_dir).iterdir():
        if folder.is_dir():
            fort22_path = folder / "fort.22"
            if fort22_path.exists():
                print(f"Processing: {folder.name}")
                try:
                    process = subprocess.Popen(
                        ["neighcrys", "fort.22"],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        cwd=folder
                    )
                    stdout, stderr = process.communicate(input="\n\n")
                    print(f"Completed: {folder.name}\n{stdout}")
                    dmain_file = folder / f"{folder.name}.res.dmain"
                    if not dmain_file.exists():
                        print(f"Warning: No .dmain file created in {folder.name}")
                except subprocess.CalledProcessError as e:
                    print(f"Error in {folder.name}:\n{e.stderr}")
            else:
                print(f"Skipping {folder.name}: fort.22 not found")
    print("All folders processed")

def remove_spli_lines(file_path):
    """Remove lines starting with 'SPLI' from the given file."""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        filtered_lines = [line for line in lines if not line.startswith("SPLI")]
        with open(file_path, 'w') as file:
            file.writelines(filtered_lines)
        print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_dmain_files(root_dir):
    """Remove 'SPLI' lines from all .res.dmain files."""
    for folder in Path(root_dir).iterdir():
        if folder.is_dir():
            dmain_file = folder / f"{folder.name}.res.dmain"
            if dmain_file.exists():
                remove_spli_lines(dmain_file)
            else:
                print(f"Skipping {folder.name}: .res.dmain file not found")
    print("All .res.dmain files processed")

def copy_scripts_to_folders(root_dir, scripts):
    """Copy scripts into each folder."""
    for folder in Path(root_dir).iterdir():
        if folder.is_dir():
            print(f"Copying scripts to: {folder.name}")
            for script in scripts:
                try:
                    shutil.copy(script, folder)
                    print(f"Copied {Path(script).name} to {folder.name}")
                except Exception as e:
                    print(f"Error copying {Path(script).name} to {folder.name}: {e}")
        else:
            print(f"Skipping {folder.name}: Not a directory")
    print("Script copying completed")

def run_autold_in_folders(root_dir):
    """Run AutoLD.py in each folder."""
    for folder in Path(root_dir).iterdir():
        if folder.is_dir():
            autold_script = folder / "AutoLD.py"
            if autold_script.exists():
                print(f"Running AutoLD.py in: {folder.name}")
                try:
                    result = subprocess.run(
                        ["python", str(autold_script), "-k", "0.12"],
                        cwd=folder,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    if result.stdout:
                        print(f"Output from {folder.name}:\n{result.stdout}")
                    if result.stderr:
                        print(f"Errors from {folder.name}:\n{result.stderr}")
                except Exception as e:
                    print(f"Error running AutoLD.py in {folder.name}: {e}")
            else:
                print(f"Skipping {folder.name}: AutoLD.py not found")
        else:
            print(f"Skipping {folder.name}: Not a directory")
    print("AutoLD.py execution completed")

def run_dmacrys_on_dmain(root_dir):
    """Run dmacrys2.2.1 on each .dmain file."""
    for folder in Path(root_dir).iterdir():
        if folder.is_dir():
            print(f"\nProcessing folder: {folder.name}")
            dmain_files = list(folder.glob("*.dmain"))
            if not dmain_files:
                print(f"No .dmain files found in {folder.name}")
                continue
            for dmain_file in dmain_files:
                output_file = dmain_file.with_suffix(".dmaout")
                print(f"\nRunning dmacrys2.2.1 on: {dmain_file}")
                try:
                    with open(dmain_file, "r") as infile, open(output_file, "w") as outfile:
                        result = subprocess.run(
                            ["dmacrys2.2.1"],
                            stdin=infile,
                            stdout=outfile,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                    print(f"Output saved to: {output_file}")
                    if result.stderr:
                        print(f"Errors from {dmain_file}:\n{result.stderr}")
                except Exception as e:
                    print(f"Error processing {dmain_file}: {e}")
        else:
            print(f"Skipping {folder.name}: Not a directory")
    print("\nDMACRYS processing completed")

def run_autofree_in_folders(root_dir):
    """Run AutoFree.py in each folder."""
    for folder in Path(root_dir).iterdir():
        if folder.is_dir():
            autofree_script = folder / "AutoFree.py"
            if autofree_script.exists():
                output_file = folder / f"{folder.name}.out"
                print(f"Running AutoFree.py in: {folder.name}")
                try:
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
    print("AutoFree.py execution completed")

if __name__ == "__main__":
    # Step 1: Organize .res files into folders
    print("Organising .res files.")
    organize_res_files(ROOT_DIR)
    print("Completed Task.")

    # Step 2: Copy required files into each folder
    print("Fetching required files.")
    organize_crystal_files(ROOT_DIR)
    print("Completed Task.")

    # Step 3: Create fort.22 files in each folder
    print("Creating fort.22 files.")
    create_fort22_files(ROOT_DIR)
    print("Completed Task.")

    # Step 4: Run neighcrys on each fort.22 file
    print("Starting NEIGHCRYS calculations.")
    process_folders(ROOT_DIR)
    print("Completed Task.")

    # Step 5: Remove 'SPLI' lines from .res.dmain files
    print("Removing SPLI line from all .dmain files.")
    process_dmain_files(ROOT_DIR)
    print("Completed Task.")

    # Step 6: Copy AutoFree.py and AutoLD.py into each folder
    print("Fetching required files.")
    copy_scripts_to_folders(ROOT_DIR, SCRIPTS_TO_COPY)
    print("Completed Task.")

    # Step 7: Run AutoLD.py in each folder
    print("Running AutoLD.")
    run_autold_in_folders(ROOT_DIR)
    print("Completed Task.")

    # Step 8: Run dmacrys2.2.1 on each .dmain file
    # print("Starting DMACRYS calculations.")
    # run_dmacrys_on_dmain(ROOT_DIR)
    # print("Completed Task.")

    # Step 9: Run AutoFree.py in each folder
    # print("Running AutoFree.")
    # run_autofree_in_folders(ROOT_DIR)
    # print("Completed Task.")

    # print("All tasks completed!")