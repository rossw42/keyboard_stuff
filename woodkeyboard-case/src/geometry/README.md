# Geometry Module

This module provides 2D profile geometry generation for CNC machining operations.

## Overview

The geometry module generates precise 2D profiles (lists of x,y coordinates) for all features of the keyboard case components. These profiles are used as input for CNC toolpath generation and technical drawing export.

## Coordinate System

- **Origin**: Top-left corner of case external profile (0, 0)
- **X-axis**: Positive to the right (length direction, 0-295mm)
- **Y-axis**: Positive downward (width direction, 0-105mm)
- **Units**: All dimensions in millimeters (mm)

## Modules

### profiles.py

Core geometry generation functions for 2D profiles.

#### Basic Shapes

- `generate_rounded_rectangle(length, width, corner_radius, origin)` - Rectangular profile with rounded corners
- `generate_circle(center, diameter, segments)` - Circular profile

#### Top Frame Features

- `generate_external_profile(case_length, case_width, corner_radius)` - External case profile (295×105mm, 3mm radius)
- `generate_pcb_opening(opening_length, opening_width, case_length, case_width, border)` - PCB opening pocket (286×95.6mm, centered)
- `generate_usb_cutout(cutout_width, cutout_height, corner_radius, center_x, center_y)` - USB port cutout (16×10mm, centered on top edge)
- `generate_brass_insert_holes(mounting_holes, insert_diameter)` - Brass insert hole positions (6 locations, 5.8mm diameter)

#### Complete Profiles

- `generate_top_frame_profile(...)` - Complete top frame profile with all features

## Usage

### Basic Example

```python
from constants import *
from geometry import generate_top_frame_profile

# Generate complete top frame profile
profile = generate_top_frame_profile(
    case_length=CASE_LENGTH,
    case_width=CASE_WIDTH,
    case_corner_radius=CASE_CORNER_RADIUS,
    pcb_opening_length=PCB_OPENING_LENGTH,
    pcb_opening_width=PCB_OPENING_WIDTH,
    pcb_border=PCB_BORDER,
    usb_cutout_width=USB_CUTOUT_WIDTH,
    usb_cutout_height=USB_CUTOUT_HEIGHT,
    usb_corner_radius=USB_CUTOUT_CORNER_RADIUS,
    usb_center_x=USB_CUTOUT_CENTER_X,
    usb_center_y=USB_CUTOUT_CENTER_Y,
    mounting_holes=MOUNTING_HOLES,
    brass_insert_diameter=BRASS_INSERT_DIAMETER
)

# Access individual features
external = profile['external_profile']  # List of (x, y) points
pcb_opening = profile['pcb_opening']    # List of (x, y) points
usb_cutout = profile['usb_cutout']      # List of (x, y) points
brass_holes = profile['brass_insert_holes']  # Dict of hole_id: [(x, y), ...]
```

### Individual Features

```python
from geometry import generate_external_profile, generate_pcb_opening

# Generate just the external profile
external = generate_external_profile(
    case_length=295.0,
    case_width=105.0,
    corner_radius=3.0
)

# Generate just the PCB opening
pcb_opening = generate_pcb_opening(
    opening_length=286.0,
    opening_width=95.6,
    case_length=295.0,
    case_width=105.0,
    border=4.5
)
```

## Data Structures

### Profile

A profile is represented as a list of 2D points:

```python
Profile = List[Tuple[float, float]]

# Example:
profile = [
    (0.0, 0.0),      # First point
    (10.0, 0.0),     # Second point
    (10.0, 10.0),    # Third point
    (0.0, 10.0),     # Fourth point
    (0.0, 0.0),      # Close path (duplicate of first point)
]
```

### Top Frame Profile Dictionary

The complete top frame profile is returned as a dictionary:

```python
{
    'external_profile': [(x, y), ...],           # External boundary
    'pcb_opening': [(x, y), ...],                # PCB opening pocket
    'usb_cutout': [(x, y), ...],                 # USB port cutout
    'brass_insert_holes': {                      # Brass insert holes
        'TL': [(x, y), ...],  # Top-left
        'TR': [(x, y), ...],  # Top-right
        'ML': [(x, y), ...],  # Middle-left
        'MR': [(x, y), ...],  # Middle-right
        'BL': [(x, y), ...],  # Bottom-left
        'BR': [(x, y), ...],  # Bottom-right
    }
}
```

## Tolerances

The geometry module generates nominal dimensions. Tolerances are documented but not applied to the geometry itself:

- **Critical dimensions** (±0.1mm): PCB opening, mounting holes, brass insert holes
- **Standard dimensions** (±0.2mm): External profile, USB cutout, other features

Tolerance compensation is applied during CNC toolpath generation (Task 4).

## Testing

Run the test suite to verify geometry generation:

```bash
python tests/test_top_frame_geometry.py
```

Tests verify:
- Dimensional accuracy
- Position accuracy
- Feature completeness
- Coordinate system consistency

## Examples

See the `examples/` directory for usage examples:

- `generate_top_frame.py` - Generate and display top frame profile summary
- `visualize_top_frame.py` - ASCII visualization of top frame layout

## Requirements Traceability

| Function | Requirements |
|----------|--------------|
| `generate_external_profile` | 5.1, 6.5 |
| `generate_pcb_opening` | 1.1, 2.4 |
| `generate_usb_cutout` | 3.1, 3.2, 3.3 |
| `generate_brass_insert_holes` | 2.2, 2.4, 2.5 |

See `.kiro/specs/60-percent-keyboard-case/requirements.md` for full requirement details.

#### Bottom Tray Features

- `generate_internal_cavity(cavity_length, cavity_width, corner_radius, wall_thickness)` - Internal cavity pocket (287×96.6mm, 8mm deep, 2mm radius)
- `generate_standoff_pillars(mounting_holes, pillar_diameter)` - PCB standoff pillar positions (6 locations, 6mm diameter)
- `generate_standoff_holes(mounting_holes, hole_diameter)` - Standoff through-holes (6 locations, 2.2mm diameter for M2 screws)
- `generate_assembly_screw_holes(mounting_holes, hole_diameter)` - Assembly screw holes (6 locations, 3.2mm diameter for M3 screws)
- `generate_assembly_screw_counterbores(mounting_holes, counterbore_diameter)` - Assembly screw counterbores (6 locations, 6mm diameter, 3mm deep)
- `generate_rubber_feet_recesses(feet_positions, recess_diameter)` - Rubber feet recesses (4 corners, 10mm diameter, 2mm deep)
- `generate_bottom_tray_profile(...)` - Complete bottom tray profile with all features

## Future Enhancements

- DXF export functionality (Task 6)
- 3D solid model generation (Task 9)
- Profile validation and error checking
- Alternative coordinate system support
