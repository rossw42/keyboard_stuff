"""Fix all remaining invalid keyboard.json files."""

import json
import re

FILES_TO_FIX = [
    r"D:\GitHub2\vial-qmk\keyboards\ymdk\ymd09\keyboard.json",
    r"D:\GitHub2\vial-qmk\keyboards\smithrune\magnus\m75s\keyboard.json",
    r"D:\GitHub2\vial-qmk\keyboards\reviung\reviung34\keyboard.json",
    r"D:\GitHub2\vial-qmk\keyboards\mzmkb\slimdash\rev1\keyboard.json",
    r"D:\GitHub2\vial-qmk\keyboards\monsgeek\m6\keyboard.json",
    r"D:\GitHub2\vial-qmk\keyboards\handwired\jotlily60\keyboard.json",
    r"D:\GitHub2\vial-qmk\keyboards\era\sirind\klein_hs\keyboard.json",
    r"D:\GitHub2\vial-qmk\keyboards\1upkeyboards\pi60_rgb_v2\keyboard.json",
]

for fpath in FILES_TO_FIX:
    print(f"Processing: {fpath}")
    
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            raw = f.read()
        
        # Step 1: Fix unicode escapes like \u00xx that aren't valid
        raw = re.sub(r'\\u[0-9a-f]{4}', '', raw)
        
        # Step 2: Remove all // style comments
        lines = raw.split('\n')
        cleaned_lines = []
        for line in lines:
            idx = line.find('//')
            if idx >= 0:
                line = line[:idx]
            cleaned_lines.append(line)
        raw = '\n'.join(cleaned_lines)
        
        # Step 3: Fix trailing commas before } or ]
        raw = re.sub(r',(\s*[}\]])', r'\1', raw)
        
        # Step 4: Parse as JSON
        data = json.loads(raw)
        
        # Step 5: Re-serialize with proper formatting
        fixed_json = json.dumps(data, indent=2)
        
        # Write back
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(fixed_json)
            f.write('\n')
        
        print(f"  -> Fixed and saved!")
        
    except Exception as e:
        print(f"  -> ERROR: {type(e).__name__}: {str(e)[:100]}")

print("\nDone!")
