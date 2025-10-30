import os
import math

# Define the main directory and the output file path
main_directory = "results-3"  # Root directory
output_file_path = "commands.txt"

# List of crystal directories to process
crystal_directories = [
    "zumkun/structure-files",
    "izijoq/structure-files",
]

# Collect all commands in a list
all_commands = []

# Iterate over each crystal directory
for crystal_dir in crystal_directories:
    full_crystal_path = os.path.join(main_directory, crystal_dir)
    
    # Debugging: Print the current directory being searched
    print(f"Searching in: {full_crystal_path}")
    
    # Check if the directory exists
    if not os.path.exists(full_crystal_path):
        print(f"Directory does not exist: {full_crystal_path}")
        continue  # Skip to the next directory
    
    # Walk through the directory
    for root, dirs, files in os.walk(full_crystal_path):
        for file in files:
            if file.endswith(".dmain"):
                # Extract the base name without extension
                base_name = os.path.splitext(file)[0]
                # Construct the full path for the cd command
                full_cd_path = root
                # Construct the command with absolute paths
                command = f"cd {full_cd_path} ; dmacrys2.2.1 < {file} > {base_name}.dmaout\n"
                # Add the command to the list
                all_commands.append(command)

# Split the commands into 10 equal parts
num_files = 3
commands_per_file = math.ceil(len(all_commands) / num_files)

# Write the commands to 10 separate files
for i in range(num_files):
    start_index = i * commands_per_file
    end_index = start_index + commands_per_file
    split_commands = all_commands[start_index:end_index]
    
    # Define the output file name
    split_file_path = f"commands_{i + 1}.txt"
    
    # Write the commands to the split file
    with open(split_file_path, 'w') as split_file:
        split_file.writelines(split_commands)
    
    print(f"Written {len(split_commands)} commands to {split_file_path}")

print("All commands have been split into 10 files.")