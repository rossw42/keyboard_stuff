# Coordinate System Reference

## Overview

The 60% keyboard case design uses a consistent coordinate system across all components to ensure accurate positioning and alignment.

## Origin Point

**Location**: Top-left corner of the case external profile, at the top surface

**Coordinates**: (0, 0, 0)

## Axis Definitions

### X-Axis (Horizontal)
- **Direction**: Positive to the right (length direction)
- **Range**: 0mm to 295mm
- **Description**: Runs along the length of the keyboard case

### Y-Axis (Vertical)
- **Direction**: Positive downward (width direction)
- **Range**: 0mm to 105mm
- **Description**: Runs along the width of the keyboard case

### Z-Axis (Depth)
- **Direction**: Positive downward (into material)
- **Range**: Varies by component
  - Top frame: 0mm to 5mm
  - Bottom tray: 0mm to 15mm
- **Description**: Represents depth into the material from the top surface

## Reference Points

### PCB Opening Center
- **X**: 147.5mm (CASE_LENGTH / 2)
- **Y**: 52.5mm (CASE_WIDTH / 2)

### USB Cutout Center
- **X**: 147.5mm (centered on top edge)
- **Y**: 11.5mm (PCB_BORDER + USB_OFFSET_FROM_PCB_EDGE)

### Mounting Hole Positions

All positions include the 4.5mm border offset:

| Position | X (mm) | Y (mm) | Description |
|----------|--------|--------|-------------|
| TL | 23.5 | 14.0 | Top-left |
| TR | 270.5 | 14.0 | Top-right |
| ML | 33.0 | 51.8 | Middle-left |
| MR | 261.0 | 51.8 | Middle-right |
| BL | 61.5 | 89.5 | Bottom-left |
| BR | 232.5 | 89.5 | Bottom-right |

## CNC Setup

### Workpiece Positioning
1. Secure workpiece with top-left corner aligned to machine origin
2. Zero X and Y axes at top-left corner of material
3. Zero Z axis at top surface of material

### Verification
Before starting machining operations:
- Verify origin position with edge finder or probe
- Confirm workpiece dimensions match stock specifications
- Check that coordinate system matches CAM software settings

## Notes

- All dimensions in the constants.py file use this coordinate system
- Toolpaths generated will reference this origin point
- When flipping workpiece for bottom operations, re-establish origin at same corner
