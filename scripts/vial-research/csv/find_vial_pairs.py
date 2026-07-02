import os
import csv
from pathlib import Path

def find_vial_keyboards(root_dir):
    root_path = Path(root_dir)
    vial_files = []
    
    # Search for all vial.json files recursively
    for path in root_path.rglob('keymaps\\vial\\vial.json'):
        vial_files.append(path)
        
    return vial_files

def find_corresponding_keyboard(vial_path):
    # vial.json is usually in: ...\keyboards\<keyboard_name>\keymaps\vial\vial.json
    # keyboard.json is usually in: ...\keyboards\<keyboard_name>\keyboard.json
    
    # Try to find the keyboard.json in the parent directories of vial.json
    # Usually, it's 3 levels up: keymaps -> vial -> <keyboard_name>
    parts = vial_path.parts
    if len(parts) >= 3:
        # Look for a keyboard.json in the directory containing the keymaps folder
        # e.g. ...\keyboards\egg58\keymaps\vial\vial.json
        # we want ...\keyboards\egg58\keyboard.json
        # parts[-4] is the keyboard folder name
        parent_kb_dir = Path(*parts[:-3])
        kb_file = parent_kb_dir / "keyboard.json"
        
        if kb_file.exists():
            return kb_file
            
    return None

def main():
    root_dir = r"D:\GitHub2\vial-qmk\keyboards"
    output_csv = Path(r"D:\GitHub\keyboard_stuff\scripts\vial_keyboard_pairs.csv")
    
    vial_files = find_vial_keyboards(root_dir)
    
    with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['keyboard.json', 'vial.json'])
        
        for vial_path in vial_files:
            kb_path = find_corresponding_keyboard(vial_path)
            if kb_path:
                writer.writerow([str(kb_path), str(vial_path)])
                print(f"Found: {kb_path.name} <-> {vial_path.name}")
            else:
                print(f"Could not find keyboard.json for: {vial_path}")

if __name__ == "__main__":
    main()
