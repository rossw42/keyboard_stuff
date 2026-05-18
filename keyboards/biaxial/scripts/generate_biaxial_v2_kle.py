#!/usr/bin/env python3
"""Generate V2 KLE by removing Esc, Tab, Caps, Shift and centering properly."""
import json

# Read V1 KLE
with open('kle/biaxial_v1.kle.json', 'r') as f:
    v1_kle = json.load(f)

# Remove Esc, Tab, Caps, Shift (indices 1, 2, 3, 4)
indices_to_remove = {1, 2, 3, 4}
v2_kle = [key for i, key in enumerate(v1_kle) if i not in indices_to_remove]

# Transfer Esc's rotation to backtick
esc_rotation = v1_kle[1][0]
if isinstance(v2_kle[1], list) and len(v2_kle[1]) >= 1:
    backtick_obj = v2_kle[1][0]
    if isinstance(backtick_obj, dict):
        backtick_obj['r'] = esc_rotation.get('r')
        backtick_obj['rx'] = esc_rotation.get('rx')
        backtick_obj['ry'] = esc_rotation.get('ry')

# Get the Space key's x position - this should be at center (0)
space_x = v2_kle[0][0]['x']
target_center = space_x

# Apply centering to move Space to x=0
for key in v2_kle:
    if isinstance(key, list) and len(key) >= 1:
        key_obj = key[0]
        if isinstance(key_obj, dict):
            if 'x' in key_obj:
                key_obj['x'] -= target_center
            if 'rx' in key_obj:
                key_obj['rx'] -= target_center

# Write V2 KLE
output = json.dumps(v2_kle, separators=(',', ':'))
with open('kle/biaxial_v2.kle.json', 'w') as f:
    f.write(output)

print(f"Generated V2 KLE with {len(v2_kle)} keys")
print(f"Removed 4 keys: Esc, Tab, Caps, Shift")
print(f"Centered layout around rx center: {target_center:.4f}")
