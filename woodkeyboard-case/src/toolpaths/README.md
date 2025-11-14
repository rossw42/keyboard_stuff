# CNC Toolpath Generation

This directory contains modules for generating CNC toolpaths for the 60% keyboard case components.

## Modules

### top_frame.py
Generates CNC toolpaths for the top frame component (5mm thick).

**Operations:**
1. Face surfacing (6mm endmill, 0.5mm depth)
2. Brass insert counterbores (6mm endmill, 5.8mm dia, 4mm deep, 6x)
3. PCB opening pocket (6mm roughing, 3mm finishing)
4. USB cutout (3mm endmill)
5. External profile (6mm roughing, 3mm finishing)

**Key Features:**
- Two-stage operations (roughing + finishing)
- Helical boring for accurate holes
- Tab retention for external profile
- Critical tolerances (±0.1mm) for mounting features

### bottom_tray.py
Generates CNC toolpaths for the bottom tray component (15mm thick).

**Operations:**
1. Face surfacing (6mm endmill, 0.5mm depth)
2. Rubber feet recesses (10mm endmill, 2mm deep, 4x)
3. Assembly screw counterbores (6mm endmill, 3mm deep, 6x)
4. Assembly screw through-holes (3.2mm drill, 15mm deep, 6x)
5. Internal cavity pocket (6mm roughing, 4mm finishing, 8mm deep)
6. Standoff through-holes (2.2mm drill, 6mm deep, 6x)
7. External profile (6mm roughing, 3mm finishing)

**Key Features:**
- Adaptive clearing for cavity pocket
- Standoff pillars preserved as islands
- Peck drilling for deep holes
- Workpiece flip required (operations 2-3 from bottom)
- Critical tolerances (±0.1mm) for standoff holes

## Usage

### Generate Top Frame Toolpaths

```python
from src.constants import *
from src.geometry.profiles import generate_top_frame_profile
from src.toolpaths.top_frame import generate_top_frame_toolpaths

# Generate geometry
geometry = generate_top_frame_profile(
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

# Generate toolpaths
toolpaths = generate_top_frame_toolpaths(
    case_length=CASE_LENGTH,
    case_width=CASE_WIDTH,
    external_profile=geometry['external_profile'],
    pcb_opening_profile=geometry['pcb_opening'],
    usb_cutout_profile=geometry['usb_cutout'],
    mounting_holes=MOUNTING_HOLES,
    top_frame_height=TOP_FRAME_HEIGHT
)
```

### Generate Bottom Tray Toolpaths

```python
from src.constants import *
from src.geometry.profiles import generate_bottom_tray_profile
from src.toolpaths.bottom_tray import generate_bottom_tray_toolpaths

# Generate geometry
geometry = generate_bottom_tray_profile(
    case_length=CASE_LENGTH,
    case_width=CASE_WIDTH,
    case_corner_radius=CASE_CORNER_RADIUS,
    cavity_length=CAVITY_LENGTH,
    cavity_width=CAVITY_WIDTH,
    cavity_corner_radius=CAVITY_CORNER_RADIUS,
    wall_thickness=WALL_THICKNESS,
    mounting_holes=MOUNTING_HOLES,
    standoff_pillar_diameter=STANDOFF_DIAMETER,
    standoff_hole_diameter=STANDOFF_HOLE_DIAMETER,
    assembly_screw_diameter=ASSEMBLY_SCREW_DIAMETER,
    assembly_counterbore_diameter=ASSEMBLY_SCREW_COUNTERBORE_DIAMETER,
    rubber_feet_positions=RUBBER_FEET_POSITIONS,
    rubber_feet_diameter=RUBBER_FEET_DIAMETER
)

# Generate toolpaths
toolpaths = generate_bottom_tray_toolpaths(
    case_length=CASE_LENGTH,
    case_width=CASE_WIDTH,
    external_profile=geometry['external_profile'],
    internal_cavity_profile=geometry['internal_cavity'],
    standoff_pillars=geometry['standoff_pillars'],
    mounting_holes=MOUNTING_HOLES,
    rubber_feet_positions=RUBBER_FEET_POSITIONS,
    bottom_tray_height=BOTTOM_TRAY_HEIGHT,
    cavity_depth=CAVITY_DEPTH
)
```

## Toolpath Data Structure

All toolpath functions return dictionaries with the following structure:

```python
{
    'component': 'top_frame' | 'bottom_tray',
    'operations': {
        '1_operation_name': {
            'operation': 'operation_type',
            'tool': {
                'diameter': float,  # mm
                'type': 'flat_endmill' | 'drill',
                'flutes': int,
                'description': str
            },
            'parameters': {
                'depth': float,  # mm
                'feed_rate': float,  # mm/min
                'spindle_speed': float,  # RPM
                'plunge_rate': float,  # mm/min
                'tolerance': float,  # mm
                # ... operation-specific parameters
            },
            'toolpath': [
                [(x, y), (x, y), ...],  # 2D paths
                # or
                [(x, y, z), (x, y, z), ...]  # 3D paths
            ]
        },
        # ... more operations
    },
    'setup': {
        'material': str,
        'stock_dimensions': {
            'length': float,
            'width': float,
            'thickness': float
        },
        'work_holding': str,
        'origin': str,
        'notes': [str, ...]
    },
    'summary': {
        'total_operations': int,
        'tools_required': [str, ...],
        'estimated_time_minutes': float,
        'critical_tolerances': [str, ...],
        'standard_tolerances': [str, ...]
    }
}
```

## Feed Rates & Speeds

All feed rates and spindle speeds are optimized for hardwood machining:

### Endmill Operations
- **Roughing**: 1200 mm/min feed, 18000 RPM
- **Finishing**: 800 mm/min feed, 16000 RPM
- **Plunge rate**: 200-300 mm/min

### Drilling Operations
- **3.2mm drill**: 400 mm/min feed, 12000 RPM
- **2.2mm drill**: 300 mm/min feed, 10000 RPM
- **Plunge rate**: 150-200 mm/min

### Peck Drilling
- **Deep holes (>10mm)**: 5mm peck depth
- **Shallow holes (<10mm)**: 3mm peck depth
- **Retract height**: 2mm between pecks

## Tolerances

### Critical Tolerances (±0.1mm)
- PCB opening dimensions
- Mounting hole positions
- Brass insert hole diameter
- Standoff pillar positions
- Standoff hole diameter (M2 screw fit)

### Standard Tolerances (±0.2mm)
- External case dimensions
- Wall thicknesses
- USB cutout position
- Rubber feet recess positions
- Assembly screw holes
- Cavity dimensions

## Machining Strategies

### Adaptive Clearing
Used for cavity pocket roughing. Efficiently removes bulk material while avoiding standoff pillars.

### Helical Interpolation
Used for counterbores and recesses. Creates smooth, accurate circular features.

### Profile Following
Used for finishing passes. Follows geometry with tool radius compensation.

### Peck Drilling
Used for deep holes. Provides chip evacuation and prevents tool breakage.

### Two-Stage Operations
Roughing removes bulk material quickly, finishing achieves final dimensions and tolerances.

## Examples

See the `examples/` directory for complete usage examples:
- `generate_top_frame_toolpaths.py` - Generate and export top frame toolpaths
- `generate_bottom_tray_toolpaths.py` - Generate and export bottom tray toolpaths
- `visualize_top_frame.py` - Visualize top frame geometry
- `visualize_bottom_tray_toolpaths.py` - Visualize bottom tray machining sequence

## Testing

Comprehensive test suite in `tests/`:
- `test_top_frame_toolpaths.py` - Top frame toolpath tests
- `test_bottom_tray_toolpaths.py` - Bottom tray toolpath tests

Run tests:
```bash
python -m pytest tests/test_*_toolpaths.py -v
```

## Notes

- All coordinates are in millimeters (mm)
- Origin is at top-left corner of case external profile, top surface
- Z-axis is positive downward (into material)
- Feed rates assume hardwood (walnut, maple, cherry)
- Adjust speeds for different materials or tool conditions
- Always verify first article dimensions before production runs
