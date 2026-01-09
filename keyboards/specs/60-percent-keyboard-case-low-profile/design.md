# Design Document: 60% Keyboard Case - Low-Profile Variant

## Overview

This document describes the detailed design for a low-profile variant of the 60% keyboard case. The design reduces the overall height from 20mm to 13mm (35% reduction) while maintaining full compatibility with the same PCB and mounting system used in the standard variant.

### Design Goals

1. **Height Reduction:** Achieve 14mm total height (3mm top frame + 11mm bottom tray) - 30% reduction from standard
2. **PCB Compatibility:** Maintain compatibility with standard 285mm x 94.6mm PCB
3. **Structural Integrity:** Ensure adequate strength despite reduced dimensions
4. **Manufacturing Feasibility:** Use same CNC tools and processes as standard variant
5. **Assembly Simplicity:** Maintain straightforward assembly with basic hand tools
6. **Component Clearance:** Provide 4.4mm clearance below PCB for safe component accommodation

### Key Design Decisions

| Aspect | Standard Variant | Low-Profile Variant | Rationale |
|--------|-----------------|---------------------|-----------|
| Total Height | 20mm | 14mm | 30% reduction for portability |
| Top Frame | 5mm | 3mm | Minimum for brass insert depth |
| Bottom Tray | 15mm | 11mm | Reduced while maintaining clearance |
| Cavity Depth | 10mm | 8mm | Provides safe component clearance |
| Standoff Height | 3mm | 2mm | Lowers PCB position |
| Clearance Below PCB | 5.4mm | 4.4mm | Safe margin for components (exceeds 4mm) |
| Base Thickness | 5mm | 3mm | Maintains structural integrity (meets 3mm min) |

## Architecture

### Component Structure

The low-profile case consists of two main components:

```
Low-Profile Assembly (14mm total height)
├── Top Frame (3mm height)
│   ├── External profile (295mm x 105mm)
│   ├── PCB opening (286mm x 95.6mm)
│   ├── USB cutout (16mm x 8mm)
│   └── Brass insert counterbores (6 locations, 3mm deep)
│
└── Bottom Tray (11mm height)
    ├── External profile (295mm x 105mm)
    ├── Internal cavity (287mm x 96.6mm x 8mm deep)
    ├── PCB standoff pillars (6 locations, 2mm high)
    ├── Standoff through-holes (2.2mm dia)
    ├── Assembly screw holes (3.2mm dia)
    ├── Assembly counterbores (6mm dia, 2.5mm deep)
    └── Rubber feet recesses (10mm dia, 2mm deep)
```

### Dimensional Hierarchy

```
External Dimensions (295mm x 105mm)
  └─ PCB Border (4.5mm all sides)
      └─ PCB Opening (286mm x 95.6mm)
          └─ PCB Clearance (0.5mm per side)
              └─ PCB (285mm x 94.6mm x 1.6mm)

Vertical Stack (14mm total)
  ├─ Top Frame (3mm)
  │   └─ Brass Insert Depth (3mm from bottom)
  │
  └─ Bottom Tray (11mm)
      ├─ Cavity (8mm deep from top)
      │   ├─ Standoff Pillars (2mm high from cavity floor)
      │   │   └─ PCB (1.6mm thick)
      │   └─ Clearance Below PCB (4.4mm) ✓ Safe margin
      │
      └─ Base (3mm thick) ✓ Meets minimum
          └─ Counterbores (2.5mm deep from bottom)
```

## Components and Interfaces

### Top Frame (3mm height)

#### External Profile
- **Dimensions:** 295mm (L) x 105mm (W) x 3mm (H)
- **Corner Radius:** 3mm (external)
- **Material:** Hardwood (walnut, maple, or cherry)
- **Stock:** 295mm x 105mm x 4mm (mill down to 3mm)

#### PCB Opening
- **Dimensions:** 286mm x 95.6mm (centered)
- **Border:** 4.5mm on all sides
- **Depth:** Through full 3mm thickness
- **Corner Type:** Sharp corners for maximum PCB support
- **Tolerance:** ±0.1mm (critical)

#### USB Port Cutout
- **Dimensions:** 16mm (W) x 8mm (H)
- **Position:** Centered horizontally, 7mm from PCB opening edge
- **Corner Radius:** 1mm
- **Depth:** Through full 3mm thickness
- **Tolerance:** ±0.2mm (standard)

#### Brass Insert Counterbores
- **Count:** 6 locations (matching PCB mounting holes)
- **Diameter:** 5.8mm (for 5.7mm OD brass inserts, press-fit)
- **Depth:** 3mm (full thickness of top frame)
- **Thread:** M3 metric
- **Tolerance:** ±0.1mm (critical)
- **Positions:** Same as standard variant (see mounting holes section)

**Design Note:** The 3mm top frame height is the minimum required to accommodate 3mm deep brass inserts. This is a critical constraint that cannot be reduced further without compromising the mounting system.

### Bottom Tray (10mm height)

#### External Profile
- **Dimensions:** 295mm (L) x 105mm (W) x 11mm (H)
- **Corner Radius:** 3mm (external)
- **Material:** Hardwood (walnut, maple, or cherry)
- **Stock:** 295mm x 105mm x 13mm (mill down to 11mm)

#### Internal Cavity
- **Dimensions:** 287mm (L) x 96.6mm (W) x 8mm (D)
- **Corner Radius:** 2mm (internal, limited by 4mm endmill)
- **Wall Thickness:** 4mm (all sides)
- **Base Thickness:** 3mm (11mm total - 8mm cavity)
- **Tolerance:** ±0.2mm (standard)

**Clearance Calculation:**
```
Cavity depth: 8mm
Standoff height: 2mm
PCB thickness: 1.6mm
Clearance below PCB: 8mm - 2mm - 1.6mm = 4.4mm ✓

This provides safe clearance for:
- Switch pins: 3.3mm (1.1mm margin)
- Diodes: 1.5-2mm (2.4-2.9mm margin)
- SMD components: 0.5-1mm (3.4-3.9mm margin)
- Solder joints: 0.5mm (3.9mm margin)

Base thickness: 11mm - 8mm = 3mm ✓ (meets structural minimum)
```

#### PCB Standoff Pillars
- **Count:** 6 locations (matching PCB mounting holes)
- **Diameter:** 6mm
- **Height:** 2mm (from cavity floor) ← REDUCED from 3mm
- **Material:** Integral with bottom tray (islands in cavity)
- **Tolerance:** ±0.1mm (critical)

#### Standoff Through-Holes
- **Count:** 6 locations (through standoff pillars)
- **Diameter:** 2.2mm (M2 screw clearance)
- **Depth:** Through pillar into counterbore (2mm + 2.5mm = 4.5mm)
- **Tolerance:** ±0.1mm (critical)

#### Assembly Screw Holes
- **Count:** 6 locations (concentric with standoffs)
- **Diameter:** 3.2mm (M3 screw clearance)
- **Depth:** Through full 11mm height
- **Tolerance:** ±0.2mm (standard)

#### Assembly Screw Counterbores
- **Count:** 6 locations (bottom surface)
- **Diameter:** 6mm (M3 screw head clearance)
- **Depth:** 2.5mm (from bottom surface) ← REDUCED from 3mm
- **Tolerance:** ±0.2mm (standard)

#### Rubber Feet Recesses
- **Count:** 4 locations (corners)
- **Diameter:** 10mm
- **Depth:** 2mm (from bottom surface)
- **Corner Offset:** 10mm (from corner to center)
- **Tolerance:** ±0.2mm (standard)

### Mounting Hole Positions

The low-profile variant uses identical mounting hole positions as the standard variant for PCB compatibility:

```javascript
// Coordinates from top-left corner of case (origin)
// All dimensions in millimeters
mountingHoles = {
  TL: {x: 23.5, y: 14.0},   // Top-left
  TR: {x: 270.5, y: 14.0},  // Top-right
  ML: {x: 33.0, y: 51.8},   // Middle-left
  MR: {x: 261.0, y: 51.8},  // Middle-right
  BL: {x: 61.5, y: 89.5},   // Bottom-left
  BR: {x: 232.5, y: 89.5}   // Bottom-right
}
```

**Positional Accuracy:** ±0.1mm (critical tolerance)

### USB Port Position

```javascript
usbCutout = {
  centerX: 147.5,  // Horizontal center of case (295mm / 2)
  centerY: 11.5,   // 4.5mm border + 7mm offset
  width: 16.0,     // Accommodates USB-C with margin
  height: 8.0,     // Through 3mm top frame (reduced from 10mm)
  cornerRadius: 1.0
}
```

## Data Models

### Low-Profile Constants

```python
# Low-Profile Variant Constants
# All dimensions in millimeters (mm)

# PCB Specifications (same as standard)
PCB_LENGTH = 285.0
PCB_WIDTH = 94.6
PCB_THICKNESS = 1.6

# Case External Dimensions (same as standard)
CASE_LENGTH = 295.0
CASE_WIDTH = 105.0
CASE_CORNER_RADIUS = 3.0

# Low-Profile Component Heights
TOP_FRAME_HEIGHT_LP = 3.0      # Reduced from 5.0mm
BOTTOM_TRAY_HEIGHT_LP = 11.0   # Reduced from 15.0mm
TOTAL_HEIGHT_LP = 14.0         # Reduced from 20.0mm (30% reduction)

# Low-Profile Cavity Specifications
CAVITY_DEPTH_LP = 8.0          # Reduced from 10.0mm (provides 4.4mm clearance)
BASE_THICKNESS_LP = 3.0        # 11mm - 8mm (meets 3mm minimum for strength)
WALL_THICKNESS = 4.0           # Same as standard

# Low-Profile Standoff Specifications
STANDOFF_HEIGHT_LP = 2.0       # Reduced from 3.0mm
STANDOFF_DIAMETER = 6.0        # Same as standard
STANDOFF_HOLE_DIAMETER = 2.2   # Same as standard (M2 clearance)

# PCB Opening (same as standard)
PCB_BORDER = 4.5
PCB_OPENING_LENGTH = 286.0
PCB_OPENING_WIDTH = 95.6
PCB_CLEARANCE = 0.5

# USB Cutout (adjusted height)
USB_CUTOUT_WIDTH = 16.0
USB_CUTOUT_HEIGHT_LP = 8.0     # Reduced from 10.0mm
USB_CUTOUT_CORNER_RADIUS = 1.0
USB_OFFSET_FROM_PCB_EDGE = 7.0

# Brass Insert Specifications (adjusted depth)
BRASS_INSERT_DIAMETER = 5.8
BRASS_INSERT_DEPTH_LP = 3.0    # Full top frame thickness
BRASS_INSERT_THREAD = 'M3'

# Assembly Screw Specifications (adjusted counterbore)
ASSEMBLY_SCREW_DIAMETER = 3.2
ASSEMBLY_SCREW_COUNTERBORE_DIAMETER = 6.0
ASSEMBLY_SCREW_COUNTERBORE_DEPTH_LP = 2.5  # Reduced from 3.0mm

# Rubber Feet Specifications (same as standard)
RUBBER_FEET_DIAMETER = 10.0
RUBBER_FEET_DEPTH = 2.0
RUBBER_FEET_CORNER_OFFSET = 10.0

# Tolerances (same as standard)
TOLERANCE_CRITICAL = 0.1   # ±0.1mm for mounting holes, PCB opening
TOLERANCE_STANDARD = 0.2   # ±0.2mm for external dimensions

# Clearance Verification
CLEARANCE_BELOW_PCB_LP = CAVITY_DEPTH_LP - STANDOFF_HEIGHT_LP - PCB_THICKNESS
# = 8.0 - 2.0 - 1.6 = 4.4mm ✓ (exceeds 4mm recommended, safe for components)
```

### Vertical Stack Calculation

```python
# Low-Profile Vertical Stack
def calculate_vertical_stack_lp():
    """Calculate and verify low-profile vertical stack dimensions."""
    
    # Bottom tray measurements (from bottom surface)
    counterbore_depth = 2.5  # mm
    base_thickness = 3.0     # mm
    cavity_depth = 8.0       # mm
    standoff_height = 2.0    # mm
    pcb_thickness = 1.6      # mm
    
    # Calculate positions
    cavity_floor = base_thickness  # 3mm from bottom
    standoff_top = cavity_floor + standoff_height  # 5mm from bottom
    pcb_bottom = standoff_top  # 5mm from bottom
    pcb_top = pcb_bottom + pcb_thickness  # 6.6mm from bottom
    bottom_tray_top = base_thickness + cavity_depth  # 11mm from bottom
    
    # Top frame
    top_frame_height = 3.0  # mm
    
    # Total height
    total_height = bottom_tray_top + top_frame_height  # 14mm
    
    # Clearances
    clearance_below_pcb = cavity_depth - standoff_height - pcb_thickness  # 4.4mm
    space_above_pcb = bottom_tray_top - pcb_top  # 4.4mm
    
    return {
        'total_height': total_height,  # 14mm ✓
        'clearance_below_pcb': clearance_below_pcb,  # 4.4mm ✓ (safe margin)
        'space_above_pcb': space_above_pcb,  # 4.4mm ✓
        'base_thickness': base_thickness,  # 3mm ✓
        'pcb_position_from_bottom': pcb_bottom  # 5mm
    }
```

## Error Handling

### Design Validation Checks

The low-profile design must pass the following validation checks:

1. **Minimum Clearance Check**
   - Clearance below PCB ≥ 3mm
   - Current: 3.4mm ✓

2. **Minimum Base Thickness Check**
   - Base thickness ≥ 3mm
   - Current: 3mm ✓

3. **Brass Insert Depth Check**
   - Insert depth ≤ top frame height
   - Current: 3mm = 3mm ✓

4. **Wall Thickness Check**
   - Wall thickness ≥ 3mm
   - Current: 4mm ✓

5. **Total Height Check**
   - Total height = 12-15mm target range
   - Current: 13mm ✓

6. **PCB Compatibility Check**
   - Mounting holes match standard variant
   - PCB opening matches standard variant
   - Current: Identical ✓

### Manufacturing Constraints

1. **Stock Thickness**
   - Top frame: 4mm stock (mill to 3mm)
   - Bottom tray: 12mm stock (mill to 10mm)
   - Both fit within 12-20mm standard stock range ✓

2. **Tool Accessibility**
   - All features accessible with standard CNC tools
   - Same tools as standard variant ✓

3. **Corner Radii**
   - Internal: 2mm (4mm endmill)
   - External: 3mm (3mm endmill)
   - Both achievable ✓

## Testing Strategy

### Design Validation

1. **Dimensional Validation**
   - Run validation script with low-profile constants
   - Verify all clearances meet minimum requirements
   - Check total height is within 12-15mm range

2. **Clearance Validation**
   - Verify 3.4mm clearance below PCB
   - Verify 3.4mm space above PCB
   - Verify 3mm base thickness

3. **Compatibility Validation**
   - Verify mounting hole positions match standard variant
   - Verify PCB opening dimensions match standard variant
   - Verify external dimensions match standard variant

### Manufacturing Validation

1. **Toolpath Generation**
   - Generate toolpaths for both components
   - Verify tool accessibility for all features
   - Verify no tool collisions

2. **3D Model Verification**
   - Generate 3D models (STEP format)
   - Visual inspection for clearances
   - Assembly verification

3. **Technical Drawing Review**
   - Generate technical drawings (DXF/PDF)
   - Verify all dimensions are clearly marked
   - Verify tolerances are specified

### Physical Prototype Testing

1. **Structural Testing**
   - Check for flex under typing pressure
   - Verify no cracking at thin sections
   - Test screw retention in brass inserts

2. **Fit Testing**
   - Verify PCB fits with proper clearance
   - Test USB cable insertion
   - Verify keycap clearance

3. **Assembly Testing**
   - Verify assembly process is straightforward
   - Test disassembly and reassembly
   - Verify alignment features work correctly

## Manufacturing Process

### Material Preparation

1. **Stock Selection:**
   - Hardwood: Walnut, maple, or cherry recommended
   - Top frame: 295mm x 105mm x 4mm (mill to 3mm)
   - Bottom tray: 295mm x 105mm x 12mm (mill to 10mm)
   - Grain orientation: Length-wise for maximum strength

2. **Stock Preparation:**
   - Face both sides flat and parallel
   - Ensure thickness uniformity (±0.1mm)
   - Mark reference edges for workholding

### CNC Machining Sequence

#### Top Frame Operations

1. **Face Surfacing** (Top surface)
   - Tool: 6mm flat endmill
   - Depth: 0.5mm (bring to 3.5mm)
   - Purpose: Ensure flat reference surface

2. **Brass Insert Counterbores** (Bottom surface, requires flip)
   - Tool: 6mm flat endmill
   - Diameter: 5.8mm
   - Depth: 3mm (full thickness)
   - Count: 6 locations

3. **PCB Opening Pocket** (Top surface)
   - Roughing: 6mm flat endmill
   - Finishing: 4mm flat endmill
   - Depth: 3mm (through thickness)
   - Sharp corners

4. **USB Cutout** (Top surface)
   - Tool: 3mm flat endmill
   - Dimensions: 16mm x 8mm
   - Corner radius: 1mm
   - Depth: 3mm (through thickness)

5. **External Profile** (Final operation)
   - Roughing: 6mm flat endmill
   - Finishing: 3mm flat endmill
   - Corner radius: 3mm
   - Depth: 3mm (through-cut)

#### Bottom Tray Operations

1. **Face Surfacing** (Top surface)
   - Tool: 6mm flat endmill
   - Depth: 0.5mm (bring to 10.5mm)
   - Purpose: Ensure flat reference surface

2. **Rubber Feet Recesses** (Bottom surface, requires flip)
   - Tool: 10mm flat endmill
   - Diameter: 10mm
   - Depth: 2mm
   - Count: 4 corners

3. **Assembly Screw Counterbores** (Bottom surface)
   - Tool: 6mm flat endmill
   - Diameter: 6mm
   - Depth: 2.5mm
   - Count: 6 locations

4. **Assembly Screw Through-Holes** (Bottom surface)
   - Tool: 3.2mm drill
   - Diameter: 3.2mm
   - Depth: 10mm (through thickness)
   - Count: 6 locations

5. **Internal Cavity Pocket** (Top surface, flip back)
   - Roughing: 6mm flat endmill
   - Finishing: 4mm flat endmill (determines 2mm corner radius)
   - Depth: 7mm
   - Leave standoff pillars as islands

6. **Standoff Through-Holes** (Top surface)
   - Tool: 2.2mm drill
   - Diameter: 2.2mm
   - Depth: 4.5mm (through pillar into counterbore)
   - Count: 6 locations

7. **External Profile** (Final operation)
   - Roughing: 6mm flat endmill
   - Finishing: 3mm flat endmill
   - Corner radius: 3mm
   - Depth: 10mm (through-cut)

### Quality Control

1. **Dimensional Inspection:**
   - Verify external dimensions (±0.2mm)
   - Verify mounting hole positions (±0.1mm)
   - Verify cavity depth (±0.2mm)
   - Verify base thickness (±0.2mm)

2. **Surface Quality:**
   - Check for tear-out or chipping
   - Verify smooth surfaces (no tool marks)
   - Check corner radii are consistent

3. **Fit Testing:**
   - Test brass insert fit (should be press-fit)
   - Test PCB fit in opening
   - Test assembly screw fit

## Design Comparison: Standard vs Low-Profile

| Feature | Standard Variant | Low-Profile Variant | Change |
|---------|-----------------|---------------------|--------|
| **Total Height** | 20mm | 14mm | -30% |
| **Top Frame** | 5mm | 3mm | -40% |
| **Bottom Tray** | 15mm | 11mm | -27% |
| **Cavity Depth** | 10mm | 8mm | -20% |
| **Standoff Height** | 3mm | 2mm | -33% |
| **Clearance Below PCB** | 5.4mm | 4.4mm | -19% (safe margin) |
| **Base Thickness** | 5mm | 3mm | -40% (meets minimum) |
| **Counterbore Depth** | 3mm | 2.5mm | -17% |
| **USB Cutout Height** | 10mm | 8mm | -20% |
| **External Footprint** | 295x105mm | 295x105mm | No change |
| **PCB Opening** | 286x95.6mm | 286x95.6mm | No change |
| **Mounting Positions** | 6 holes | 6 holes | No change |
| **Wall Thickness** | 4mm | 4mm | No change |

## Risk Assessment

### Design Risks

1. **Component Clearance (Low Risk)**
   - **Risk:** 4.4mm clearance may be tight for some aftermarket PCBs with tall bottom components
   - **Mitigation:** Document compatible PCBs, test with actual hardware
   - **Status:** 4.4mm exceeds recommended 4mm minimum, accommodates standard components

2. **Thin Base (Low Risk)**
   - **Risk:** 3mm base may flex or crack under stress
   - **Mitigation:** Use hardwood with proper grain orientation, quality material selection
   - **Status:** Meets 3mm minimum structural requirement

3. **Shallow Brass Inserts (Low Risk)**
   - **Risk:** 3mm insert depth may not provide adequate thread engagement
   - **Mitigation:** Use quality brass inserts, proper installation technique
   - **Fallback:** Cannot reduce top frame below 3mm

### Manufacturing Risks

1. **Thin Stock Handling (Medium Risk)**
   - **Risk:** 3mm top frame may flex during machining
   - **Mitigation:** Proper workholding, light cuts, sharp tools
   - **Fallback:** Use vacuum table or double-sided tape

2. **Thin Base Machining (Low Risk)**
   - **Risk:** 3mm base may break through during cavity machining
   - **Mitigation:** Careful depth control, verify Z-zero
   - **Fallback:** Leave 0.5mm extra, hand-sand to final thickness

## Next Steps

1. **Create Low-Profile Constants File**
   - Create `src/constants_lp.py` with low-profile dimensions
   - Maintain same structure as standard constants

2. **Generate Geometry**
   - Adapt geometry generation functions for low-profile dimensions
   - Verify clearances and fitment

3. **Generate Toolpaths**
   - Create toolpaths for low-profile components
   - Verify tool accessibility

4. **Create 3D Models**
   - Generate STEP files for visualization
   - Verify assembly clearances

5. **Generate Technical Drawings**
   - Create DXF/PDF drawings with dimensions
   - Mark critical tolerances

6. **Run Validation**
   - Adapt validation script for low-profile variant
   - Verify all requirements are met

7. **Prototype and Test**
   - Machine prototype from hardwood
   - Test fit, clearances, and structural integrity
   - Iterate design if needed

---

**Design Version:** 1.0  
**Date:** 2025-10-13  
**Status:** Ready for Implementation  
**Target Height:** 13mm (35% reduction from standard)
