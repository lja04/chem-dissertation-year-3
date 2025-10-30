import os
from pathlib import Path
import math

# Define directories
CRYSTALS_ROOT = "results-3"
OUTPUT_DIR = "run-6"
BASE_FILENAME = "autofreecommand"

def generate_and_split_commands():
    # Ensure output directory exists
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # First collect all commands
    commands = []
    for crystal_dir in Path(CRYSTALS_ROOT).iterdir():
        if not crystal_dir.is_dir():
            continue
            
        structure_files_dir = crystal_dir / "structure-files"
        if not structure_files_dir.exists():
            continue
            
        for structure_dir in structure_files_dir.iterdir():
            if not structure_dir.is_dir():
                continue
                
            autofree_script = structure_dir / "AutoFree.py"
            if autofree_script.exists():
                cmd = f"cd {structure_dir} ; python AutoFree.py > {structure_dir.name}.out\n"
                commands.append(cmd)
    
    # Calculate how many commands per file
    total_commands = len(commands)
    if total_commands == 0:
        print("No AutoFree.py scripts found!")
        return
        
    # Calculate number of files needed with min 400 and max 800 commands per file
    if total_commands <= 400:
        num_files = 1
        commands_per_file = total_commands
    else:
        num_files = math.ceil(total_commands / 800)
        commands_per_file = math.ceil(total_commands / num_files)
        
        # Ensure we don't go below 400 commands per file
        if commands_per_file < 400:
            num_files = math.floor(total_commands / 400)
            commands_per_file = math.ceil(total_commands / num_files)
    
    print(f"Total commands: {total_commands}")
    print(f"Number of files: {num_files}")
    print(f"Commands per file: ~{commands_per_file}")
    
    # Split commands into files
    for i in range(num_files):
        start_idx = i * commands_per_file
        end_idx = start_idx + commands_per_file
        file_commands = commands[start_idx:end_idx]
        
        output_path = Path(OUTPUT_DIR) / f"{BASE_FILENAME}_{i+1}.txt"
        
        with open(output_path, 'w') as f:
            f.writelines(file_commands)
        
        print(f"Created {output_path} with {len(file_commands)} commands")

if __name__ == "__main__":
    generate_and_split_commands()