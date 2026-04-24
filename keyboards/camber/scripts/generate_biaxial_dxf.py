#!/usr/bin/env python3
"""
Generate a DXF file for the BiAxial plate with Hull-compatible outline.

Layout strategy:
- Ortholinear columns: each column is a straight vertical stack of 4 keys
- Splay: each column rotates around its own center by ±6°
  (left half = -6°, right half = +6°)
- No row stagger — eliminates the boundary violation problem that stagger causes
- 5 left columns + 0.5u center gap + 6 right columns = 11 columns total
- Layout centered within the plate body
- Hull plate outline with tabs from Omnibus_Hull.dxf
- 14mm × 14mm MX switch cutouts
"""

import math
import sys

# === Switch profiles ===
SWITCH_PROFILES = {
    'mx': {
        'name': 'Cherry MX',
        'cutout': 14.0,          # plate cutout size (mm)
        'spacing': 19.05,        # 1u key spacing (mm)
        'plate_thickness': 1.5,  # recommended plate thickness (mm)
    },
    'gateron-lp': {
        'name': 'Gateron KS-33 Low Profile',
        'cutout': 14.0,          # same MX-compatible cutout
        'spacing': 19.05,        # same MX spacing
        'plate_thickness': 1.2,  # thinner plate for LP
    },
    'choc-v1': {
        'name': 'Kailh Choc v1',
        'cutout': 13.8,          # slightly smaller cutout
        'spacing': 18.0,         # Choc spacing (can also use 19.05)
        'plate_thickness': 1.2,
    },
}

# Select switch profile from command line or default to MX
_profile_name = sys.argv[1] if len(sys.argv) > 1 else 'mx'
if _profile_name not in SWITCH_PROFILES:
    print(f"Unknown switch profile '{_profile_name}'. Available: {', '.join(SWITCH_PROFILES.keys())}")
    sys.exit(1)
SWITCH = SWITCH_PROFILES[_profile_name]

# === Constants (derived from switch profile) ===
UNIT     = SWITCH['spacing']
CUTOUT   = SWITCH['cutout']
HALF_CUT = CUTOUT / 2
ANGLE_DEG       = 6.0
ANGLE_RAD       = math.radians(ANGLE_DEG)
OUTER_ANGLE_DEG = 2.0
OUTER_ANGLE_RAD = math.radians(OUTER_ANGLE_DEG)
MID_ANGLE_DEG   = 4.0
MID_ANGLE_RAD   = math.radians(MID_ANGLE_DEG)

# === Plate body bounds (from Omnibus_Hull.dxf) ===
BODY_LEFT   = -233.3625
BODY_RIGHT  =    9.525
BODY_BOTTOM =   -9.525
BODY_TOP    =   66.675
BODY_WIDTH  = BODY_RIGHT - BODY_LEFT    # 242.8875 mm
BODY_HEIGHT = BODY_TOP   - BODY_BOTTOM  # 76.2 mm
BODY_CENTER_X = (BODY_LEFT + BODY_RIGHT) / 2   # -111.9188
BODY_CENTER_Y = (BODY_BOTTOM + BODY_TOP) / 2   #   28.575

# Tab dimensions (for Hull outline)
TAB_LEFT_OUTER      = -235.6875
TAB_RIGHT_OUTER     =   11.85
TAB_TOP             =   59.825
TAB_BOTTOM          =   -2.675
TAB_SHOULDER_TOP    =   61.325
TAB_SHOULDER_BOTTOM =   -4.175

# === Layout parameters ===
LEFT_COLS  = 5  # V2: removed leftmost column (6 → 5)
RIGHT_COLS = 5
NUM_ROWS   = 4
CENTER_GAP = 1.25 * UNIT   # 23.8125 mm

# Row offsets from column center Y (ortholinear — no stagger)
# 4 rows centered on BODY_CENTER_Y
ROW_OFFSETS = [
    +1.5 * UNIT,   # row 0 — number row  (top)
    +0.5 * UNIT,   # row 1 — Q row
    -0.5 * UNIT,   # row 2 — home row
    -1.5 * UNIT,   # row 3 — bottom row  (Z row)
]

# === Column center X positions ===
# Extra spacing on outer columns to prevent bottom-row keycap collision from splay.
# Col 0 and col 1 get pushed outward by OUTER_COL_EXTRA each.
OUTER_COL_EXTRA = 1.5  # mm extra between col 0-1 and col 1-2

# Left half: col 0 = outermost, col 4 = innermost
# Right half: col 0 = innermost, col 5 = outermost
_total_span = (LEFT_COLS + RIGHT_COLS) * UNIT + CENTER_GAP + 4 * OUTER_COL_EXTRA
_left_start = BODY_CENTER_X - _total_span / 2 + UNIT / 2

# Left half column centers with extra outer spacing
LEFT_COL_X = []
for i in range(LEFT_COLS):
    extra = 0
    if i == 0:
        extra = -2 * OUTER_COL_EXTRA  # col 0 pushed further left
    elif i == 1:
        extra = -1 * OUTER_COL_EXTRA  # col 1 pushed slightly left
    LEFT_COL_X.append(_left_start + i * UNIT + extra)

# Right half column centers with extra outer spacing (mirrored)
RIGHT_COL_X = []
_right_start = LEFT_COL_X[-1] + CENTER_GAP + UNIT
for i in range(RIGHT_COLS):
    extra = 0
    ri = RIGHT_COLS - 1 - i  # distance from outermost
    if ri == 0:
        extra = 2 * OUTER_COL_EXTRA  # outermost pushed further right
    elif ri == 1:
        extra = 1 * OUTER_COL_EXTRA  # second-from-outer pushed slightly right
    RIGHT_COL_X.append(_right_start + i * UNIT + extra)

# Equalize side margins: shift everything so left and right margins match
_ext = HALF_CUT * (math.cos(OUTER_ANGLE_RAD) + math.sin(OUTER_ANGLE_RAD))
_left_margin  = (LEFT_COL_X[0]  - _ext) - BODY_LEFT
_right_margin = BODY_RIGHT - (RIGHT_COL_X[-1] + _ext)
_shift = (_left_margin - _right_margin) / 2
LEFT_COL_X  = [x - _shift for x in LEFT_COL_X]
RIGHT_COL_X = [x - _shift for x in RIGHT_COL_X]

# All column centers sit at the plate vertical center
COL_CENTER_Y = BODY_CENTER_Y


# === Key position computation ===

def rotate_point(x, y, cx, cy, angle_rad):
    dx, dy = x - cx, y - cy
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    return cx + dx * cos_a - dy * sin_a, cy + dx * sin_a + dy * cos_a


def column_keys(col_cx, angle_rad):
    """Return list of (key_cx, key_cy, angle_rad) for one splayed column."""
    keys = []
    for offset in ROW_OFFSETS:
        # Pre-rotation key center: directly above/below column center
        pre_x = col_cx
        pre_y = COL_CENTER_Y + offset
        # Rotate around column center
        rx, ry = rotate_point(pre_x, pre_y, col_cx, COL_CENTER_Y, angle_rad)
        keys.append((rx, ry, angle_rad))
    return keys


def center_spacebar():
    """Space key centered in the gap, slid up so the 1.25u keycap (rotated 90°)
    clears the plate bottom edge with 0.5mm to spare.
    Unrotated standard MX cutout (14x14mm)."""
    cx = (LEFT_COL_X[-1] + RIGHT_COL_X[0]) / 2
    cy = BODY_BOTTOM + 0.5 + (1.25 * UNIT / 2)  # 2.881mm
    return [(cx, cy, 0.0)]


def all_keys():
    keys = []
    for i, cx in enumerate(LEFT_COL_X):
        if i == 0:
            angle = -OUTER_ANGLE_RAD
        elif i == 1:
            angle = -MID_ANGLE_RAD
        else:
            angle = -ANGLE_RAD
        keys.extend(column_keys(cx, angle))
    for i, cx in enumerate(RIGHT_COL_X):
        ri = len(RIGHT_COL_X) - 1 - i  # distance from outermost
        if ri == 0:
            angle = OUTER_ANGLE_RAD
        elif ri == 1:
            angle = MID_ANGLE_RAD
        else:
            angle = ANGLE_RAD
        keys.extend(column_keys(cx, angle))
    keys.extend(center_spacebar())
    return keys


# === Bounds checking ===

def rotated_cutout_corners(cx, cy, angle_rad):
    corners = [(-HALF_CUT, -HALF_CUT), (HALF_CUT, -HALF_CUT),
               (HALF_CUT,  HALF_CUT), (-HALF_CUT,  HALF_CUT)]
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    return [(cx + dx * cos_a - dy * sin_a,
             cy + dx * sin_a + dy * cos_a) for dx, dy in corners]


def check_bounds(keys):
    violations = []
    for cx, cy, angle in keys:
        for px, py in rotated_cutout_corners(cx, cy, angle):
            if px < BODY_LEFT - 0.001:
                violations.append(f"LEFT  key({cx:.2f},{cy:.2f}) corner({px:.2f},{py:.2f}) by {BODY_LEFT-px:.3f}mm")
            if px > BODY_RIGHT + 0.001:
                violations.append(f"RIGHT key({cx:.2f},{cy:.2f}) corner({px:.2f},{py:.2f}) by {px-BODY_RIGHT:.3f}mm")
            if py < BODY_BOTTOM - 0.001:
                violations.append(f"BOT   key({cx:.2f},{cy:.2f}) corner({px:.2f},{py:.2f}) by {BODY_BOTTOM-py:.3f}mm")
            if py > BODY_TOP + 0.001:
                violations.append(f"TOP   key({cx:.2f},{cy:.2f}) corner({px:.2f},{py:.2f}) by {py-BODY_TOP:.3f}mm")
    return violations


# === DXF Writer ===

class DXFWriter:
    def __init__(self):
        self.entities = []
        self.handle = 0x100

    def _h(self):
        h = self.handle; self.handle += 1; return f"{h:X}"

    def add_line(self, x1, y1, x2, y2, layer="SWITCHES"):
        h = self._h()
        self.entities.append(
            f"0\nLINE\n5\n{h}\n100\nAcDbEntity\n8\n{layer}\n100\nAcDbLine\n"
            f"10\n{x1:.6f}\n20\n{y1:.6f}\n30\n0\n11\n{x2:.6f}\n21\n{y2:.6f}\n31\n0")

    def add_cutout(self, cx, cy, angle_rad, layer="SWITCHES"):
        corners = rotated_cutout_corners(cx, cy, angle_rad)
        for i in range(4):
            x1, y1 = corners[i]
            x2, y2 = corners[(i + 1) % 4]
            self.add_line(x1, y1, x2, y2, layer)

    def add_arc(self, cx, cy, r, sa, ea, layer="OUTLINE"):
        h = self._h()
        self.entities.append(
            f"0\nARC\n5\n{h}\n100\nAcDbEntity\n8\n{layer}\n100\nAcDbCircle\n"
            f"10\n{cx:.6f}\n20\n{cy:.6f}\n30\n0\n40\n{r:.6f}\n100\nAcDbArc\n"
            f"50\n{sa:.6f}\n51\n{ea:.6f}")

    def add_circle(self, cx, cy, r, layer="MOUNTING"):
        h = self._h()
        self.entities.append(
            f"0\nCIRCLE\n5\n{h}\n100\nAcDbEntity\n8\n{layer}\n100\nAcDbCircle\n"
            f"10\n{cx:.6f}\n20\n{cy:.6f}\n30\n0\n40\n{r:.6f}")

    def write(self, filename):
        header = ("0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n4\n"
                  "9\n$ACADVER\n1\nAC1014\n9\n$HANDSEED\n5\nFFFF\n0\nENDSEC\n")
        tables = (
            "0\nSECTION\n2\nTABLES\n"
            "0\nTABLE\n2\nLTYPE\n5\n5\n100\nAcDbSymbolTable\n"
            "0\nLTYPE\n5\n14\n100\nAcDbSymbolTableRecord\n100\nAcDbLinetypeTableRecord\n2\nBYBLOCK\n70\n0\n"
            "0\nLTYPE\n5\n15\n100\nAcDbSymbolTableRecord\n100\nAcDbLinetypeTableRecord\n2\nBYLAYER\n70\n0\n"
            "0\nENDTAB\n"
            "0\nTABLE\n2\nLAYER\n5\n2\n100\nAcDbSymbolTable\n70\n4\n"
            "0\nLAYER\n5\n50\n100\nAcDbSymbolTableRecord\n100\nAcDbLayerTableRecord\n2\n0\n70\n0\n6\nCONTINUOUS\n"
            "0\nLAYER\n5\n51\n100\nAcDbSymbolTableRecord\n100\nAcDbLayerTableRecord\n2\nOUTLINE\n70\n0\n62\n7\n6\nCONTINUOUS\n"
            "0\nLAYER\n5\n52\n100\nAcDbSymbolTableRecord\n100\nAcDbLayerTableRecord\n2\nSWITCHES\n70\n0\n62\n1\n6\nCONTINUOUS\n"
            "0\nLAYER\n5\n53\n100\nAcDbSymbolTableRecord\n100\nAcDbLayerTableRecord\n2\nMOUNTING\n70\n0\n62\n3\n6\nCONTINUOUS\n"
            "0\nENDTAB\n"
            "0\nTABLE\n2\nSTYLE\n5\n3\n100\nAcDbSymbolTable\n70\n0\n0\nENDTAB\n"
            "0\nTABLE\n2\nBLOCK_RECORD\n5\n1\n100\nAcDbSymbolTable\n70\n1\n"
            "0\nBLOCK_RECORD\n5\n1F\n100\nAcDbSymbolTableRecord\n100\nAcDbBlockTableRecord\n2\n*MODEL_SPACE\n"
            "0\nBLOCK_RECORD\n5\n1B\n100\nAcDbSymbolTableRecord\n100\nAcDbBlockTableRecord\n2\n*PAPER_SPACE\n"
            "0\nENDTAB\n0\nENDSEC\n")
        blocks = (
            "0\nSECTION\n2\nBLOCKS\n"
            "0\nBLOCK\n5\n20\n100\nAcDbEntity\n100\nAcDbBlockBegin\n2\n*MODEL_SPACE\n"
            "0\nENDBLK\n5\n21\n100\nAcDbEntity\n100\nAcDbBlockEnd\n"
            "0\nBLOCK\n5\n1C\n100\nAcDbEntity\n100\nAcDbBlockBegin\n2\n*PAPER_SPACE\n"
            "0\nENDBLK\n5\n1D\n100\nAcDbEntity\n100\nAcDbBlockEnd\n0\nENDSEC\n")
        ent = "0\nSECTION\n2\nENTITIES\n"
        for e in self.entities:
            ent += e + "\n"
        ent += "0\nENDSEC\n"
        obj = "0\nSECTION\n2\nOBJECTS\n0\nDICTIONARY\n5\nC\n100\nAcDbDictionary\n0\nENDSEC\n"
        with open(filename, 'w') as f:
            f.write(header + tables + blocks + ent + obj + "0\nEOF\n")


def add_hull_outline(dxf):
    """Hull plate outline with exact tab geometry from Omnibus_Hull.dxf.
    Each tab corner has a 5-arc compound profile:
    2.675mm outer → 0.5mm transition → 1.25mm inner → 0.5mm transition → 2.675mm outer
    """
    # Exact values from the original DXF
    # Left tab center Y = 64.0 (top), -6.85 (bottom)
    # Right tab center Y = 64.0 (top), -6.85 (bottom)
    R1 = 2.675   # outer arc radius
    R2 = 0.5     # transition arc radius
    R3 = 1.25    # inner arc radius (the actual tab neck)
    R_inner = 1.5  # inner corner radius (tab-to-body)

    # --- Top edge ---
    dxf.add_line(TAB_RIGHT_OUTER, BODY_TOP, TAB_LEFT_OUTER, BODY_TOP, "OUTLINE")

    # --- Left side: top tab corner (5-arc compound) ---
    # Center of compound arcs at (-235.6875, 64.0)
    ltc_x, ltc_y = -235.6875, 64.0
    dxf.add_arc(ltc_x, ltc_y, R1, 90, 127.8792, "OUTLINE")
    dxf.add_arc(-237.0229, 65.7167, R2, 127.8792, 258.8119, "OUTLINE")
    dxf.add_arc(-237.3625, ltc_y, R3, -78.8119, 78.8119, "OUTLINE")
    dxf.add_arc(-237.0229, 62.2833, R2, 101.1881, 232.1208, "OUTLINE")
    dxf.add_arc(ltc_x, ltc_y, R1, 232.1208, 270, "OUTLINE")

    # --- Left shoulder + inner tab ---
    dxf.add_line(-235.6875, 61.325, -234.8625, 61.325, "OUTLINE")
    dxf.add_arc(-234.8625, 59.825, R_inner, 0, 90, "OUTLINE")
    dxf.add_line(-233.3625, 59.825, -233.3625, -2.675, "OUTLINE")
    dxf.add_arc(-234.8625, -2.675, R_inner, -90, 0, "OUTLINE")
    dxf.add_line(-234.8625, -4.175, -235.6875, -4.175, "OUTLINE")

    # --- Left side: bottom tab corner (5-arc compound) ---
    lbc_x, lbc_y = -235.6875, -6.85
    dxf.add_arc(lbc_x, lbc_y, R1, 90, 127.8792, "OUTLINE")
    dxf.add_arc(-237.0229, -5.1333, R2, 127.8792, 258.8119, "OUTLINE")
    dxf.add_arc(-237.3625, lbc_y, R3, -78.8119, 78.8119, "OUTLINE")
    dxf.add_arc(-237.0229, -8.5667, R2, 101.1881, 232.1208, "OUTLINE")
    dxf.add_arc(lbc_x, lbc_y, R1, 232.1208, 270, "OUTLINE")

    # --- Bottom edge ---
    dxf.add_line(-235.6875, -9.525, 11.85, -9.525, "OUTLINE")

    # --- Right side: bottom tab corner (5-arc compound) ---
    rbc_x, rbc_y = 11.85, -6.85
    dxf.add_arc(rbc_x, rbc_y, R1, 270, 307.8792, "OUTLINE")
    dxf.add_arc(13.1854, -8.5667, R2, -52.1208, 78.8119, "OUTLINE")
    dxf.add_arc(13.525, rbc_y, R3, 101.1881, 258.8119, "OUTLINE")
    dxf.add_arc(13.1854, -5.1333, R2, -78.8119, 52.1208, "OUTLINE")
    dxf.add_arc(rbc_x, rbc_y, R1, 52.1208, 90, "OUTLINE")

    # --- Right shoulder + inner tab ---
    dxf.add_line(11.85, -4.175, 11.025, -4.175, "OUTLINE")
    dxf.add_arc(11.025, -2.675, R_inner, 180, 270, "OUTLINE")
    dxf.add_line(9.525, -2.675, 9.525, 59.825, "OUTLINE")
    dxf.add_arc(11.025, 59.825, R_inner, 90, 180, "OUTLINE")
    dxf.add_line(11.025, 61.325, 11.85, 61.325, "OUTLINE")

    # --- Right side: top tab corner (5-arc compound) ---
    rtc_x, rtc_y = 11.85, 64.0
    dxf.add_arc(rtc_x, rtc_y, R1, 270, 307.8792, "OUTLINE")
    dxf.add_arc(13.1854, 62.2833, R2, -52.1208, 78.8119, "OUTLINE")
    dxf.add_arc(13.525, rtc_y, R3, 101.1881, 258.8119, "OUTLINE")
    dxf.add_arc(13.1854, 65.7167, R2, -78.8119, 52.1208, "OUTLINE")
    dxf.add_arc(rtc_x, rtc_y, R1, 52.1208, 90, "OUTLINE")


def main():
    print("=== BiAxial V2 Plate Generator (5 left + 5 right columns, leftmost removed) ===\n")
    print(f"Switch:       {SWITCH['name']} (cutout: {CUTOUT}mm, spacing: {UNIT}mm)")
    print(f"Plate body:   {BODY_WIDTH:.4f} x {BODY_HEIGHT:.4f} mm")
    print(f"Splay angle:  ±{ANGLE_DEG}°")
    print(f"Columns:      {LEFT_COLS} left + {RIGHT_COLS} right = {LEFT_COLS+RIGHT_COLS} total (V2: leftmost removed)")
    print(f"Rows:         {NUM_ROWS} (ortholinear, no stagger)")
    print(f"Center gap:   {CENTER_GAP:.4f} mm ({CENTER_GAP/UNIT:.2f}u)")

    total_span = (LEFT_COLS + RIGHT_COLS) * UNIT + CENTER_GAP
    h_margin = (BODY_WIDTH - total_span) / 2
    print(f"\nHorizontal span: {total_span:.4f} mm  (margin: {h_margin:.4f} mm per side)")

    # Vertical clearance check
    max_y_extent = 1.5 * UNIT * math.cos(ANGLE_RAD) + HALF_CUT * (math.cos(ANGLE_RAD) + math.sin(ANGLE_RAD))
    v_margin = BODY_HEIGHT / 2 - max_y_extent
    print(f"Vertical half-extent: {max_y_extent:.4f} mm  (margin: {v_margin:.4f} mm per side)")

    print(f"\nLeft  col X:  {[f'{x:.2f}' for x in LEFT_COL_X]}")
    print(f"Right col X:  {[f'{x:.2f}' for x in RIGHT_COL_X]}")

    # Generate keys
    keys = all_keys()
    sb = center_spacebar()[0]
    L4_right = LEFT_COL_X[-1] + HALF_CUT * (math.cos(ANGLE_RAD) + math.sin(ANGLE_RAD))
    R0_left  = RIGHT_COL_X[0] - HALF_CUT * (math.cos(ANGLE_RAD) + math.sin(ANGLE_RAD))
    print(f"\nCenter spacebar (1.25u rotated 90°):")
    print(f"  Cutout center: ({sb[0]:.3f}, {sb[1]:.3f})")
    print(f"  X clearance from inner columns: {(sb[0]-7.0) - L4_right:.3f}mm each side")
    print(f"  Keycap spans Y: {sb[1]-1.25*UNIT/2:.2f} to {sb[1]+1.25*UNIT/2:.2f}mm")
    print(f"\nTotal keys: {len(keys)} (44 alpha + 1 spacebar)")

    # Check bounds
    violations = check_bounds(keys)
    if violations:
        print(f"\n⚠️  {len(violations)} boundary violations:")
        for v in violations:
            print(f"  {v}")
    else:
        print("✅ All cutout corners within plate body bounds")

    # Build DXF
    dxf = DXFWriter()
    add_hull_outline(dxf)

    for cx, cy, angle in keys:
        dxf.add_cutout(cx, cy, angle)

    # Mounting holes (Rev 2+ standard, from SteamVan KiCad source)
    mounting_holes = [
        (31.65, 19.05), (30.10, 53.80), (77.00, 65.35),
        (107.85, 19.05), (138.34, 38.15), (210.89, 16.75), (182.59, 65.55),
    ]
    for hx, hy in mounting_holes:
        dxf.add_circle(BODY_LEFT + hx, BODY_TOP - hy, 1.0)

    output = f"dxf/biaxial_v2_hull_plate_{_profile_name}.dxf"
    dxf.write(output)
    print(f"✅ Written to {output}")

    # Print all key positions
    row_names = ["Num", "Q", "Home", "Z"]
    left_key_names  = [f"L{col}-{row}" for row in row_names for col in range(LEFT_COLS)]
    right_key_names = [f"R{col}-{row}" for row in row_names for col in range(RIGHT_COLS)]
    key_names = left_key_names + right_key_names

    print()
    for i, (cx, cy, a) in enumerate(keys):
        name = key_names[i] if i < len(key_names) else f"key{i}"
        print(f"  {name:10s}  ({cx:9.3f}, {cy:8.3f})  angle={math.degrees(a):+.1f}°")


if __name__ == "__main__":
    main()
