"""
Generate output directory structure for all keyboards from CSV pairs.
Creates proper subdirectories under D:\GitHub\keyboard_stuff\scripts\vial-research\vials

The folder name is the directory item right before keyboard.json in the path.
Example: "D:\GitHub2\vial-qmk\keyboards\boston\keyboard.json" → output folder = "boston"
"""

import os
import csv

def get_subfolder_from_kb_path(kb_path):
    """Extract immediate parent folder name from keyboard.json path.
    
    Examples:
        "D:\GitHub2\vial-qmk\keyboards\boston\keyboard.json" → "boston"
        "D:\GitHub2\vial-qmk\keyboards\zsa\moonlander\keyboard.json" → "moonlander"
        "D:\GitHub2\vial-qmk\keyboards\ymdk\sp64\keyboard.json" → "sp64"
    """
    # Normalize path separators
    kb_path = kb_path.replace('\\', '/')
    
    # Remove drive letter if present
    if 'D:/keyboards' in kb_path:
        kb_path = kb_path.replace('D:/keyboards', '')
    
    # Split into parts and get the second-to-last (immediate parent folder)
    parts = kb_path.split('/')
    parent_folder = parts[-2]  # The folder containing keyboard.json
    
    return parent_folder

def main():
    csv_path = r"D:\GitHub\keyboard_stuff\scripts\vial-research\vial_keyboard_pairs.csv"
    output_dir = r"D:\GitHub\keyboard_stuff\scripts\vial-research\vials"
    
    print(f"Creating output directory: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        pairs = [(row[0].strip(), row[1].strip()) for row in reader if len(row) >= 2]
    
    print(f"Found {len(pairs)} keyboard pairs")
    
    created_dirs = set()
    
    for kb_path, _ in pairs:
        subfolder = get_subfolder_from_kb_path(kb_path)
        
        dir_path = os.path.join(output_dir, subfolder)
        if subfolder not in created_dirs:
            created_dirs.add(subfolder)
            print(f"Creating directory: {subfolder}")
            os.makedirs(dir_path, exist_ok=True)
    
    # List all created directories  
    dirs = sorted(os.listdir(output_dir))
    print(f"\nTotal subdirectories created: {len(dirs)}")
    print(f"Directories:")
    for d in dirs[:20]:
        print(f"  - {d}")
    if len(dirs) > 20:
        print(f"  ... and {len(dirs) - 20} more")

if __name__ == "__main__":
    main()
