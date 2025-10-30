import os
from collections import defaultdict

def check_dmain_dmaout_counts(root_dir):
    """
    Check if each subdirectory has the same number of dmain and dmaout files.
    
    Args:
        root_dir (str): The root directory to search through.
    """
    results = defaultdict(dict)
    
    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dmain_count = 0
        dmaout_count = 0
        
        # Count dmain and dmaout files in the current directory
        for filename in filenames:
            if filename == 'dmain':
                dmain_count += 1
            elif filename == 'dmaout':
                dmaout_count += 1
        
        # Only record directories that have at least one of these files
        if dmain_count > 0 or dmaout_count > 0:
            results[dirpath] = {
                'dmain': dmain_count,
                'dmaout': dmaout_count,
                'match': dmain_count == dmaout_count
            }
    
    # Print results
    print(f"\nResults for directory: {root_dir}")
    print("-" * 60)
    
    all_match = True
    for dirpath, counts in results.items():
        status = "MATCH" if counts['match'] else "MISMATCH"
        print(f"{dirpath}")
        print(f"  dmain files: {counts['dmain']}, dmaout files: {counts['dmaout']} - {status}")
        print("-" * 60)
        
        if not counts['match']:
            all_match = False
    
    if all_match:
        print("\nAll directories have matching dmain and dmaout counts!")
    else:
        print("\nWarning: Some directories have mismatched counts.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python check_dmain_dmaout.py <directory_path>")
        sys.exit(1)
    
    root_directory = sys.argv[1]
    
    if not os.path.isdir(root_directory):
        print(f"Error: {root_directory} is not a valid directory")
        sys.exit(1)
    
    check_dmain_dmaout_counts(root_directory)