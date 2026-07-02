import os
from pathlib import Path, PureWindowsPath

csv_path = r"D:\GitHub\keyboard_stuff\scripts\vial-research\vial_keyboard_pairs.csv"
rows = list(csv.reader(open(csv_path)))[1:]

def get_dir_name_from_path(filepath_str):
    """Get directory name from full path string"""
    try:
        # Handle Windows paths with double backslashes
        normalized = filepath_str.replace("\\\\", "/").replace("\\", "/")
        if normalized.endswith("/"):
            normalized = normalized[:-1]
       
        p = Path(normalized)
        parts = p.parent.parts  # Get all directory components
        parent_name = parts[0] if not parts else ""  # First non-empty part
        return parent_name
    except:
        # Fallback: try simple split by / or \\
        path_str = filepath_str.replace("\\\\", "/").replace("\\", "/")
        if "/" in path_str:
            return path_str.split("/")[-2]
        elif "\\" in filepath_str:
            return filepath_str.replace("\\\\", "/").split("/")[-2]
        else:
            return "UNKNOWN"

def get_keymap_name(path_str):
    """Get just the key name (last directory)"""
    try:
        path_str = path_str.replace(r"\\", "/")
        if "/" in path_str:
            last_dir = path_str.rsplit("/", 1)[0][-5:].upper()[-3:]
            return last_dir
        elif "\\" in path_str:
            last_dir = path_str.rsplit("\\", 1)[-2].upper()[-3:]
            return last_dir
    except:
        pass
    return "UNKNOWN"

print(f"Total keyboard pairs in CSV: {len(rows)}")
print()
print("="*100)
print("SAMPLE - FIRST 5 KEYBOARDS:")
print("="*100)

for i, row in enumerate(rows[:5]):
    kb_path = row[0].strip() if len(row) > 0 else ""
    vial_path = row[1].strip() if len(row) > 1 else ""
    
    kb_name = get_dir_name_from_path(kb_path) if kb_path else "UNKNOWN"
    
    print(f"Line {i+2}: Keyboard='{kb_name}'")

print("\n\n--- CHECKING PARSING AGAIN with direct string operations ---")

for i, (kb_p, vial_p) in enumerate(rows[:3]):
    # Clean up path
    if kb_p.startswith(r"D:\"):
        print(f"Line {i+2}: Path exists - {kb_path}")
    else:
        print(f"Line {i+2}: Unknown path format")
