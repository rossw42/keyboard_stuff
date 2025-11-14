"""
Dimensional constants for 60% keyboard case design.

All dimensions in millimeters (mm).
Coordinate system origin: top-left corner of case external profile.
"""

# PCB Specifications (Requirements 1.1, 1.2, 1.3)
PCB_LENGTH = 285.0  # mm
PCB_WIDTH = 94.6  # mm
PCB_THICKNESS = 1.6  # mm

# Case External Dimensions (Requirement 5.1)
CASE_LENGTH = 295.0  # mm
CASE_WIDTH = 105.0  # mm
CASE_CORNER_RADIUS = 3.0  # mm

# Top Frame Specifications
TOP_FRAME_HEIGHT = 5.0  # mm

# Bottom Tray Specifications
BOTTOM_TRAY_HEIGHT = 15.0  # mm
CAVITY_DEPTH = 10.0  # mm (increased from 8.0mm to provide 5mm+ clearance below PCB)
WALL_THICKNESS = 4.0  # mm

# PCB Opening (centered with border)
PCB_BORDER = 4.5  # mm (on all sides)
PCB_OPENING_LENGTH = 286.0  # mm (PCB + 1mm clearance)
PCB_OPENING_WIDTH = 95.6  # mm (PCB + 1mm clearance)
PCB_CLEARANCE = 0.5  # mm per side

# Internal Cavity Dimensions
CAVITY_LENGTH = 287.0  # mm
CAVITY_WIDTH = 96.6  # mm
CAVITY_CORNER_RADIUS = 2.0  # mm (limited by 4mm endmill)

# USB Port Cutout (Requirement 3.1, 3.2, 3.3)
USB_CUTOUT_WIDTH = 16.0  # mm
USB_CUTOUT_HEIGHT = 10.0  # mm (through full top frame thickness)
USB_CUTOUT_CORNER_RADIUS = 1.0  # mm
USB_OFFSET_FROM_PCB_EDGE = 7.0  # mm

# PCB Mounting Hole Positions (Requirement 2.2)
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
BRASS_INSERT_DIAMETER = 5.8  # mm (for 5.7mm OD inserts, press-fit)
BRASS_INSERT_DEPTH = 4.0  # mm
BRASS_INSERT_THREAD = 'M3'  # metric thread size

# PCB Standoff Specifications (Requirement 2.3, 2.4)
STANDOFF_DIAMETER = 6.0  # mm
STANDOFF_HEIGHT = 3.0  # mm (from cavity floor)
STANDOFF_HOLE_DIAMETER = 2.2  # mm (for M2 screws)

# Assembly Screw Specifications (Requirement 7.1)
ASSEMBLY_SCREW_DIAMETER = 3.2  # mm (clearance for M3 screws)
ASSEMBLY_SCREW_COUNTERBORE_DIAMETER = 6.0  # mm
ASSEMBLY_SCREW_COUNTERBORE_DEPTH = 3.0  # mm

# Rubber Feet Specifications (Requirement 5.4)
RUBBER_FEET_DIAMETER = 10.0  # mm
RUBBER_FEET_DEPTH = 2.0  # mm
RUBBER_FEET_CORNER_OFFSET = 10.0  # mm (from corner to center)

# Rubber feet positions (4 corners)
RUBBER_FEET_POSITIONS = [
    (RUBBER_FEET_CORNER_OFFSET, RUBBER_FEET_CORNER_OFFSET),  # Top-left
    (CASE_LENGTH - RUBBER_FEET_CORNER_OFFSET, RUBBER_FEET_CORNER_OFFSET),  # Top-right
    (RUBBER_FEET_CORNER_OFFSET, CASE_WIDTH - RUBBER_FEET_CORNER_OFFSET),  # Bottom-left
    (CASE_LENGTH - RUBBER_FEET_CORNER_OFFSET, CASE_WIDTH - RUBBER_FEET_CORNER_OFFSET),  # Bottom-right
]

# Tolerances (Requirement 6.3)
TOLERANCE_CRITICAL = 0.1  # mm (±0.1mm for mounting holes, PCB opening)
TOLERANCE_STANDARD = 0.2  # mm (±0.2mm for external dimensions, non-critical features)

# CNC Tool Specifications (Requirement 6.1)
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

# Material Specifications (Requirement 6.2)
MATERIAL = {
    'type': 'hardwood',
    'recommended_species': ['walnut', 'maple', 'cherry'],
    'top_frame_stock': {
        'length': 295.0,
        'width': 105.0,
        'thickness': 6.0,  # mill down to 5mm
    },
    'bottom_tray_stock': {
        'length': 295.0,
        'width': 105.0,
        'thickness': 20.0,  # mill down to 15mm
    },
}

# Coordinate System
ORIGIN = (0.0, 0.0, 0.0)  # Top-left corner of case external profile, top surface
COORDINATE_SYSTEM = {
    'origin': 'top-left corner of case',
    'x_axis': 'positive to the right (length direction)',
    'y_axis': 'positive downward (width direction)',
    'z_axis': 'positive downward (depth into material)',
}

# USB Cutout Position (centered on top edge)
USB_CUTOUT_CENTER_X = CASE_LENGTH / 2.0
USB_CUTOUT_CENTER_Y = PCB_BORDER + USB_OFFSET_FROM_PCB_EDGE
