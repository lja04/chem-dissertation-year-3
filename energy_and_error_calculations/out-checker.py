import os
from collections import defaultdict

def check_out_files(root_dir):
    """
    Check if each subdirectory has exactly one .out file.
    
    Args:
        root_dir (str): The root directory to search through.
    """
    results = defaultdict(dict)
    
    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(root_dir):
        out_files = [f for f in filenames if f.endswith('.out')]
        out_count = len(out_files)
        
        # Record directories that have .out files
        if out_count > 0:
            results[dirpath] = {
                'out_count': out_count,
                'valid': out_count == 1,
                'out_files': out_files
            }
    
    # Print results
    print(f"\nResults for directory: {root_dir}")
    print("-" * 60)
    
    all_valid = True
    for dirpath, counts in results.items():
        status = "VALID (1 .out file)" if counts['valid'] else f"INVALID ({counts['out_count']} .out files)"
        print(f"{dirpath}")
        print(f"  .out files found: {counts['out_count']} - {status}")
        if counts['out_count'] > 1:
            print(f"  Files: {', '.join(counts['out_files'])}")
        print("-" * 60)
        
        if not counts['valid']:
            all_valid = False
    
    if all_valid:
        print("\nAll directories have exactly one .out file!")
    else:
        print("\nWarning: Some directories have incorrect number of .out files")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python check_out_files.py <directory_path>")
        sys.exit(1)
    
    root_directory = sys.argv[1]
    
    if not os.path.isdir(root_directory):
        print(f"Error: {root_directory} is not a valid directory")
        sys.exit(1)
    
    check_out_files(root_directory)