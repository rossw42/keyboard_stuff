"""Fix invalid keyboard.json files in vial-qmk repo"""

import json
import re

# List of files with trailing comma issues (already fixed: jlw/bruce_the_keyboard, cuttlefish)
files_to_fix = [
    "D:/GitHub2/vial-qmk/keyboards/ymdk/ymd09/keyboard.json",
    "D:/GitHub2/vial-qmk/keyboards/splitkb/kyria/rev3/keyboard.json",
    "D:/GitHub2/vial-qmk/keyboards/splitkb/aurora/lily58/rev1/keyboard.json",
    "D:/GitHub2/vial-qmk/keyboards/smithrune/magnus/m75s/keyboard.json",
    "D:/GitHub2/vial-qmk/keyboards/reviung/reviung34/keyboard.json",
    "D:/GitHub2/vial-qmk/keyboards/mzmkb/slimdash/rev1/keyboard.json",
    "D:/GitHub2/vial-qmk/keyboards/monsgeek/m6/keyboard.json",
    "D:/GitHub2/vial-qmk/keyboards/keyhive/lattice60/keyboard.json",
    "D:/GitHub2/vial-qmk/keyboards/handwired/jotlily60/keyboard.json",
    "D:/GitHub2/vial-qmk/keyboards/era/sirind/klein_hs/keyboard.json",
    "D:/GitHub2/vial-qmk/keyboards/1upkeyboards/pi60_rgb_v2/keyboard.json",
]

for fpath in files_to_fix:
    print(f"Processing: {fpath}")
    
    # Read raw content
    with open(fpath, 'r', encoding='utf-8') as f:
        raw = f.read()
    
    # Step 1: Remove comment-style lines (// comments) that aren't valid JSON
    # These look like: // some comment at end of line
    raw_lines = raw.split('\n')
    fixed_lines = []
    for line in raw_lines:
        # Remove trailing // style comments but keep content
        comment_match = re.search(r'//\s*(?=\S|$)', line)
        if comment_match:
            comment_pos = comment_match.start()
            line = line[:comment_pos].rstrip()
        
        fixed_lines.append(line)
    
    raw = '\n'.join(fixed_lines)
    
    # Step 2: Parse as JSON (may fail on other issues)
    try:
        data = json.loads(raw)
        print(f"  -> Successfully parsed!")
    except json.JSONDecodeError as e:
        print(f"  -> Parsing error: {e}")
        continue
    
    # Step 3: Re-serialize with proper formatting and remove trailing commas
    fixed_json = json.dumps(data, indent=2)
    
    # Write back
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(fixed_json)
        f.write('\n')
    
    print(f"  -> Saved fixed file")

print("\nDone!")
