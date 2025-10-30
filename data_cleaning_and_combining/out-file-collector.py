import os
import shutil
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the base directory and the temp directory
base_dir = Path('crystal-files')
temp_dir = Path('energies-test/temp')

# Create the temp directory if it doesn't exist
try:
    temp_dir.mkdir(parents=True, exist_ok=True)
    logging.info(f"Created or confirmed temp directory at {temp_dir}")
except Exception as e:
    logging.error(f"Failed to create temp directory: {e}")
    exit(1)

# Counter for copied files
copied_files = 0

# Loop through crystal directories
for crystal in base_dir.iterdir():
    if crystal.is_dir():
        logging.info(f"Processing crystal: {crystal.name}")
        # Loop through polymorph directories
        for polymorph in crystal.iterdir():
            if polymorph.is_dir():
                logging.info(f"Processing polymorph: {polymorph.name}")
                # Loop through k-point values
                for k_value in [f'{i/100:.2f}' for i in range(10, 45, 5)]:
                    k_dir = polymorph / 'calc' / f'k_value_{k_value}'
                    if k_dir.exists():
                        logging.info(f"Processing k-value: {k_value}")
                        # Find and copy .out files
                        for out_file in k_dir.glob('*.out'):
                            try:
                                # Create new filename
                                new_filename = f"{crystal.name}_{polymorph.name}_k-value-{k_value}.out"
                                new_filepath = temp_dir / new_filename
                                
                                shutil.copy(out_file, new_filepath)
                                copied_files += 1
                                logging.info(f"Copied and renamed: {new_filename}")
                            except Exception as e:
                                logging.error(f"Failed to copy {out_file}: {e}")

logging.info(f"Total files copied: {copied_files}")
print(f"Process completed. {copied_files} files were copied to the temp directory.")
