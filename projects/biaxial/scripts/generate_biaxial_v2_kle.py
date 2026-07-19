#!/usr/bin/env python3
"""Generate V2 KLE from V1:
- Remove the leftmost column (Esc, Tab, Caps, Shift)
- Remove the original vertical 1.25u Space key
- Push the left/right halves outward (matches EDGE_SHIFT in the DXF generator)
- Add two 1u space keys side by side in the center gap at bottom-row height,
  each rotated to match its adjacent cluster (left +6, right -6 in KLE terms)

Anchoring: shift all rotation origins left by one column pitch so the layout
stays flush at the origin with all-positive coordinates.
"""
import json

UNIT_MM = 19.05
EDGE_SHIFT_MM = 8.0                      # matches generate_biaxial_dxf.py
SPACE_CAP_U = 1.25                       # matches SPACE_CAP_U in the DXF generator
SPACE_SEP_MM = SPACE_CAP_U * UNIT_MM + 3.5  # matches SPACE_SEP in the DXF generator
SPACE_ROW_OFFSET_U = 0.75                # 0.25u below home row (DXF: -0.75u from center)
EDGE_SHIFT_U = round(EDGE_SHIFT_MM / UNIT_MM, 4)   # 0.4199
SPACE_SEP_U = round(SPACE_SEP_MM / UNIT_MM, 4)     # 1.4337

# Read V1 KLE
with open('kle/biaxial_v1.kle.json', 'r') as f:
    v1_kle = json.load(f)

# V1 row layout: index 0 = Space, indices 1-4 = Esc/Tab/Caps/Shift (leftmost column)
esc_props = v1_kle[1][0]        # {"r":2, "rx":0.7093, "ry":2.0443, ...}
backtick_props = v1_kle[5][0]   # {"r":4, "rx":1.788, ...} (ry inherited from Esc row)

# Column pitch between the removed column and its neighbor
shift = round(backtick_props['rx'] - esc_props['rx'], 4)  # 1.0787
ry = esc_props['ry']  # 2.0443 — must be re-declared once the Esc row is gone

# Remove the old Space (0) and Esc/Tab/Caps/Shift (1-4) rows
indices_to_remove = {0, 1, 2, 3, 4}
v2_kle = [row for i, row in enumerate(v1_kle) if i not in indices_to_remove]

# Shift rotation origins: re-anchor everything left by one column pitch, then
# widen the center gap by moving ONLY the right half (r<0 clusters) further
# right by 2x the edge shift. This keeps all coordinates positive (KLE can't
# render negative origins) while producing the same relative geometry as the
# DXF (each half 8mm further from center).
# Track the current r since inherited-r rows don't redeclare it.
current_r = None
for row in v2_kle:
    props = row[0]
    if isinstance(props, dict) and 'rx' in props:
        if 'r' in props:
            current_r = props['r']
        edge = 2 * EDGE_SHIFT_U if current_r < 0 else 0.0
        props['rx'] = round(props['rx'] - shift + edge, 4)

# First rotated cluster (backtick) must declare ry explicitly (was inherited
# from the removed Esc row).
first_props = v2_kle[0][0]
if 'ry' not in first_props:
    ordered = {}
    for k in ('r', 'rx'):
        if k in first_props:
            ordered[k] = first_props[k]
    ordered['ry'] = ry
    for k, v in first_props.items():
        if k not in ordered:
            ordered[k] = v
    v2_kle[0][0] = ordered

# --- Two center space keys ---
# Gap center = midpoint of the inner cluster pivots (after edge shift).
# Inner-left pivot: last cluster with r>0; inner-right: first with r<0.
rx_vals = []
current_r = None
for row in v2_kle:
    props = row[0]
    if isinstance(props, dict) and 'rx' in props:
        if 'r' in props:
            current_r = props['r']
        rx_vals.append((current_r, props['rx']))
inner_left_rx = max(rx for r, rx in rx_vals if r > 0)
inner_right_rx = min(rx for r, rx in rx_vals if r < 0)
gap_cx = round((inner_left_rx + inner_right_rx) / 2, 4)

space_cy = round(ry + SPACE_ROW_OFFSET_U, 4)  # 0.25u below home-row centerline
left_cx = round(gap_cx - SPACE_SEP_U / 2, 4)
right_cx = round(gap_cx + SPACE_SEP_U / 2, 4)

# Each space rotates about its own center: rx/ry at the key center, key placed
# at (-w/2, -0.5) relative offset. KLE r sign: left cluster = positive.
half_w = SPACE_CAP_U / 2
space_rows = [
    [{"r": 6, "rx": left_cx, "ry": space_cy, "x": -half_w, "y": -0.5, "a": 7, "w": SPACE_CAP_U}, "Space"],
    [{"r": -6, "rx": right_cx, "ry": space_cy, "x": -half_w, "y": -0.5, "a": 7, "w": SPACE_CAP_U}, "Space"],
]
# Insert left space before the right-half clusters (KLE requires rotation
# sections in a consistent order; keep r descending: +6...-2, so put the +6
# space right after the last +6 cluster and the -6 space before the first -6
# cluster to be safe -- simplest valid ordering: append at the end.
v2_kle.extend(space_rows)

# Write V2 KLE
output = json.dumps(v2_kle, separators=(',', ':'))
with open('kle/biaxial_v2.kle.json', 'w') as f:
    f.write(output)

n_keys = sum(1 for row in v2_kle for item in row if isinstance(item, str))
print(f"Generated V2 KLE with {n_keys} keys")
print("Removed leftmost column (Esc, Tab, Caps, Shift) and the vertical Space")
print(f"Edge-shifted each half outward by {EDGE_SHIFT_U}u ({EDGE_SHIFT_MM}mm)")
print(f"Added 2 rotated {SPACE_CAP_U}u space keys at ({left_cx}, {space_cy}) r=+6 and ({right_cx}, {space_cy}) r=-6")
