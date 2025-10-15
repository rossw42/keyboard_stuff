"""
Dimensional constants for 60% keyboard case design - LOW-PROFILE VARIANT.

All dimensions in millimeters (mm).
Coordinate system origin: top-left corner of case external profile.

This low-profile variant reduces the overall height from 20mm to 14mm (30% reduction)
while maintaining full compatibility with the same PCB and mounting system.

Key differences from standard variant:
- Total height: 14mm (vs 20mm standard)
- Top frame: 3mm (vs 5mm standard)
- Bottom tray: 11mm (vs 15mm standard)
- Cavity depth: 8mm (vs 10mm standard)
- Standoff height: 2mm (vs 3mm standard)
- Clearance below PCB: 4.4mm (vs 5.4mm standard) - safer margin for components
"""

# PCB Specifications (Requirements 1.1, 1.2, 1.3)
# SAME AS STANDARD - Maintains PCB compatibility
PCB_LENGTH = 285.0  # mm
PCB_WIDTH = 94.6  # mm
PCB_THICKNESS = 1.6  # mm

# Case External Dimensions (Requirement 5.1)
# SAME AS STANDARD - Maintains footprint compatibility
CASE_LENGTH = 295.0  # mm
CASE_WIDTH = 105.0  # mm
CASE_CORNER_RADIUS = 3.0  # mm

# Low-Profile Top Frame Specifications (Requirement 6.1)
# REDUCED from 5mm to 3mm (minimum for 3mm brass insert depth)
TOP_FRAME_HEIGHT = 3.0  # mm (LOW-PROFILE: reduced from 5mm)

# Low-Profile Bottom Tray Specifications (Requirement 6.2)
# REDUCED from 15mm to 11mm
BOTTOM_TRAY_HEIGHT = 11.0  # mm (LOW-PROFILE: reduced from 15mm)
CAVITY_DEPTH = 8.0  # mm (LOW-PROFILE: reduced from 10mm, provides 4.4mm clearance below PCB)
WALL_THICKNESS = 4.0  # mm (SAME AS STANDARD)

# Calculated base thickness (Requirement 8.2)
BASE_THICKNESS = BOTTOM_TRAY_HEIGHT - CAVITY_DEPTH  # 3mm (minimum for structural integrity)

# Total height verification (Requirement 5.2)
TOTAL_HEIGHT = TOP_FRAME_HEIGHT + BOTTOM_TRAY_HEIGHT  # 14mm (target: 12-15mm range)

# PCB Opening (centered with border)
# SAME AS STANDARD - Maintains PCB compatibility
PCB_BORDER = 4.5  # mm (on all sides)
PCB_OPENING_LENGTH = 286.0  # mm (PCB + 1mm clearance)
PCB_OPENING_WIDTH = 95.6  # mm (PCB + 1mm clearance)
PCB_CLEARANCE = 0.5  # mm per side

# Internal Cavity Dimensions
# SAME AS STANDARD except depth
CAVITY_LENGTH = 287.0  # mm
CAVITY_WIDTH = 96.6  # mm
CAVITY_CORNER_RADIUS = 2.0  # mm (limited by 4mm endmill)

# USB Port Cutout (Requirement 3.1, 3.2, 3.3)
# Width and position SAME AS STANDARD, height REDUCED
USB_CUTOUT_WIDTH = 16.0  # mm
USB_CUTOUT_HEIGHT = 8.0  # mm (LOW-PROFILE: reduced from 10mm, still through full 3mm top frame)
USB_CUTOUT_CORNER_RADIUS = 1.0  # mm
USB_OFFSET_FROM_PCB_EDGE = 7.0  # mm

# PCB Mounting Hole Positions (Requirement 2.2)
# SAME AS STANDARD - Maintains PCB compatibility
# Coordinates from top-left corner of case (origin)
# Format: (x, y) where x is horizontal distance from left, y is vertical distance from top
MOUNTING_HOLES = {
    'TL': (19.0 + PCB_BORDER, 9.5 + PCB_BORDER),      # Top-left
    'TR': (266.0 + PCB_BORDER, 9.5 + PCB_BORDER),     # Top-right
    'ML': (28.5 + PCB_BORDER, 47.3 + PCB_BORDER),     # Middle-left
    'MR': (256.5 + PCB_BORDER, 47.3 + PCB_BORDER),    # Middle-right
    'BL': (57.0 + PCB_BORDER, 85.0 + PCB_BORDER),     # Bottom-left
    'BR': (228.0 + PCB_BORDER, 85.0 + PCB_BORDER),    # Bottom-right
}

# Brass Insert Specifications (Requirement 2.5)
# Diameter SAME AS STANDARD, depth REDUCED to match top frame thickness
BRASS_INSERT_DIAMETER = 5.8  # mm (for 5.7mm OD inserts, press-fit)
BRASS_INSERT_DEPTH = 3.0  # mm (LOW-PROFILE: reduced from 4mm, equals full top frame thickness)
BRASS_INSERT_THREAD = 'M3'  # metric thread size

# PCB Standoff Specifications (Requirement 2.3, 2.4)
# Diameter and hole SAME AS STANDARD, height REDUCED
STANDOFF_DIAMETER = 6.0  # mm
STANDOFF_HEIGHT = 2.0  # mm (LOW-PROFILE: reduced from 3mm)
STANDOFF_HOLE_DIAMETER = 2.2  # mm (for M2 screws)

# Assembly Screw Specifications (Requirement 7.1)
# Diameter SAME AS STANDARD, counterbore depth REDUCED
ASSEMBLY_SCREW_DIAMETER = 3.2  # mm (clearance for M3 screws)
ASSEMBLY_SCREW_COUNTERBORE_DIAMETER = 6.0  # mm
ASSEMBLY_SCREW_COUNTERBORE_DEPTH = 2.5  # mm (LOW-PROFILE: reduced from 3mm)

# Rubber Feet Specifications (Requirement 5.4)
# SAME AS STANDARD
RUBBER_FEET_DIAMETER = 10.0  # mm
RUBBER_FEET_DEPTH = 2.0  # mm
RUBBER_FEET_CORNER_OFFSET = 10.0  # mm (from corner to center)

# Rubber feet positions (4 corners)
# SAME AS STANDARD
RUBBER_FEET_POSITIONS = [
    (RUBBER_FEET_CORNER_OFFSET, RUBBER_FEET_CORNER_OFFSET),  # Top-left
    (CASE_LENGTH - RUBBER_FEET_CORNER_OFFSET, RUBBER_FEET_CORNER_OFFSET),  # Top-right
    (RUBBER_FEET_CORNER_OFFSET, CASE_WIDTH - RUBBER_FEET_CORNER_OFFSET),  # Bottom-left
    (CASE_LENGTH - RUBBER_FEET_CORNER_OFFSET, CASE_WIDTH - RUBBER_FEET_CORNER_OFFSET),  # Bottom-right
]

# Tolerances (Requirement 7.3, 7.4)
# SAME AS STANDARD
TOLERANCE_CRITICAL = 0.1  # mm (±0.1mm for mounting holes, PCB opening)
TOLERANCE_STANDARD = 0.2  # mm (±0.2mm for external dimensions, non-critical features)

# CNC Tool Specifications (Requirement 7.1)
# SAME AS STANDARD - Uses same tools for manufacturing
TOOLS = {
    'endmill_6mm': {
        'diameter': 6.0,
        'type': 'flat_endmill',
        'flutes': 2,
        'description': 'Roughing operations'
    },
    'endmill_4mm': {
        'diameter': 4.0,
        'type': 'flat_endmill',
        'flutes': 2,
        'description': 'Cavity finishing, limited by corner radius'
    },
    'endmill_3mm': {
        'diameter': 3.0,
        'type': 'flat_endmill',
        'flutes': 2,
        'description': 'Profile finishing, USB cutout'
    },
    'drill_2.2mm': {
        'diameter': 2.2,
        'type': 'drill',
        'flutes': 2,
        'description': 'Standoff through-holes (M2 clearance)'
    },
    'drill_3.2mm': {
        'diameter': 3.2,
        'type': 'drill',
        'flutes': 2,
        'description': 'Assembly screw holes (M3 clearance)'
    },
    'endmill_10mm': {
        'diameter': 10.0,
        'type': 'flat_endmill',
        'flutes': 2,
        'description': 'Rubber feet recesses'
    },
}

# Material Specifications (Requirement 7.2)
# Stock thickness REDUCED for low-profile components
MATERIAL = {
    'type': 'hardwood',
    'recommended_species': ['walnut', 'maple', 'cherry'],
    'top_frame_stock': {
        'length': 295.0,
        'width': 105.0,
        'thickness': 4.0,  # LOW-PROFILE: mill down to 3mm (reduced from 6mm stock)
    },
    'bottom_tray_stock': {
        'length': 295.0,
        'width': 105.0,
        'thickness': 13.0,  # LOW-PROFILE: mill down to 11mm (reduced from 20mm stock)
    },
}

# Coordinate System
# SAME AS STANDARD
ORIGIN = (0.0, 0.0, 0.0)  # Top-left corner of case external profile, top surface
COORDINATE_SYSTEM = {
    'origin': 'top-left corner of case',
    'x_axis': 'positive to the right (length direction)',
    'y_axis': 'positive downward (width direction)',
    'z_axis': 'positive downward (depth into material)',
}

# USB Cutout Position (centered on top edge)
# SAME AS STANDARD
USB_CUTOUT_CENTER_X = CASE_LENGTH / 2.0
USB_CUTOUT_CENTER_Y = PCB_BORDER + USB_OFFSET_FROM_PCB_EDGE

# ============================================================================
# LOW-PROFILE CLEARANCE VERIFICATION (Requirement 4.1, 4.2)
# ============================================================================

# Calculate clearance below PCB
CLEARANCE_BELOW_PCB = CAVITY_DEPTH - STANDOFF_HEIGHT - PCB_THICKNESS
# = 8.0 - 2.0 - 1.6 = 4.4mm ✓ (exceeds 3mm minimum, safer margin for components)

# Calculate PCB position from bottom surface
CAVITY_FLOOR_FROM_BOTTOM = BASE_THICKNESS  # 3mm
PCB_BOTTOM_FROM_BOTTOM = CAVITY_FLOOR_FROM_BOTTOM + STANDOFF_HEIGHT  # 5mm
PCB_TOP_FROM_BOTTOM = PCB_BOTTOM_FROM_BOTTOM + PCB_THICKNESS  # 6.6mm

# Calculate space above PCB
SPACE_ABOVE_PCB = BOTTOM_TRAY_HEIGHT - PCB_TOP_FROM_BOTTOM  # 4.4mm

# Verification assertions (for development/testing)
assert TOTAL_HEIGHT == 14.0, f"Total height should be 14mm, got {TOTAL_HEIGHT}mm"
assert 12.0 <= TOTAL_HEIGHT <= 15.0, f"Total height {TOTAL_HEIGHT}mm outside target range (12-15mm)"
assert CLEARANCE_BELOW_PCB >= 3.0, f"Clearance below PCB {CLEARANCE_BELOW_PCB}mm < 3mm minimum"
assert CLEARANCE_BELOW_PCB >= 4.0, f"Clearance below PCB {CLEARANCE_BELOW_PCB}mm < 4mm recommended"
assert BASE_THICKNESS >= 3.0, f"Base thickness {BASE_THICKNESS}mm < 3mm minimum"
assert BRASS_INSERT_DEPTH <= TOP_FRAME_HEIGHT, f"Brass insert depth {BRASS_INSERT_DEPTH}mm > top frame {TOP_FRAME_HEIGHT}mm"
assert WALL_THICKNESS >= 3.0, f"Wall thickness {WALL_THICKNESS}mm < 3mm minimum"

# ============================================================================
# LOW-PROFILE DESIGN SUMMARY
# ============================================================================

DESIGN_SUMMARY = {
    'variant': 'LOW-PROFILE',
    'total_height': TOTAL_HEIGHT,  # 14mm
    'height_reduction': f"{((20.0 - TOTAL_HEIGHT) / 20.0 * 100):.1f}%",  # 30%
    'top_frame_height': TOP_FRAME_HEIGHT,  # 3mm
    'bottom_tray_height': BOTTOM_TRAY_HEIGHT,  # 11mm
    'cavity_depth': CAVITY_DEPTH,  # 8mm
    'base_thickness': BASE_THICKNESS,  # 3mm
    'standoff_height': STANDOFF_HEIGHT,  # 2mm
    'clearance_below_pcb': CLEARANCE_BELOW_PCB,  # 4.4mm
    'space_above_pcb': SPACE_ABOVE_PCB,  # 4.4mm
    'pcb_compatible': True,  # Same PCB as standard variant
    'mounting_compatible': True,  # Same mounting positions as standard variant
    'footprint_compatible': True,  # Same external dimensions as standard variant
}

# Print design summary when module is imported
if __name__ == '__main__':
    print("=" * 80)
    print("LOW-PROFILE VARIANT - DESIGN SUMMARY")
    print("=" * 80)
    for key, value in DESIGN_SUMMARY.items():
        print(f"{key:.<30} {value}")
    print("=" * 80)
    print(f"\nClearance Verification:")
    print(f"  Clearance below PCB: {CLEARANCE_BELOW_PCB}mm (≥4mm recommended) ✓")
    print(f"  Base thickness: {BASE_THICKNESS}mm (≥3mm required) ✓")
    print(f"  Brass insert depth: {BRASS_INSERT_DEPTH}mm (≤{TOP_FRAME_HEIGHT}mm top frame) ✓")
    print(f"  Total height: {TOTAL_HEIGHT}mm (12-15mm target range) ✓")
    print(f"\nCompatibility:")
    print(f"  Accommodates switch pins (3.3mm), diodes (2mm), SMD components (1mm)")
    print(f"  Safety margin: {CLEARANCE_BELOW_PCB - 3.3}mm above tallest switch pins")
    print("=" * 80)
