# Ergogen Keyboard Layout Design Guide

## Lessons Learned from Keyboard Development

This document captures key insights and best practices for designing keyboard layouts in Ergogen, based on practical experience building a 4x4 macropad and 3x8 keyboard. **All techniques have been validated and tested.**

## 1. Mounting Hole Placement

### ❌ Common Mistakes
- Placing holes too close to switch cutouts
- Positioning holes outside the PCB boundary
- Using arbitrary positions without considering component interference

### ✅ Best Practices
**Position mounting holes in the "dead space" between switches:**

```yaml
mounting_holes:
  - what: circle
    where:
      ref: matrix_col0_row0
      shift: [kx/2, ky/2]  # Between col0/col1, row0/row1
    radius: 1.1
```

**Key Lesson:** Use `shift: [kx/2, ky/2]` to place holes exactly between adjacent keys in the matrix grid. This ensures:
- No interference with switch cutouts
- Proper structural support
- Clean, professional appearance

## 2. Board Outline Design

### ❌ Problematic Approaches
- Using `where: true` (creates huge rectangles around entire workspace)
- Complex polygon definitions that break STL generation
- Not accounting for component placement

### ✅ Reliable Method
**Use simple rectangles with calculated dimensions, but keep borders TIGHT:**

```yaml
units:
  # Keep board dimensions minimal - just enough for components
  board_width: 4*kx + 10   # Minimal padding
  board_height: 4*ky + 20  # Just enough for MCU, not excessive

outlines:
  board:
    - what: rectangle
      where:
        ref: matrix_col1_row1  # Center reference
        shift: [kx/2, 0]
      size: [board_width, board_height]
      corner: 3
```

**Key Lessons:** 
- Simple rectangles are more reliable than complex polygons for STL generation
- **CRITICAL: Keep board borders tight!** Excessive padding makes MCU appear to float in empty space
- Use calculated dimensions for maintainability, but be conservative with padding

## 3. Diode Placement for Space Efficiency

### ❌ Space-Wasting Approach
```yaml
# Vertical diodes take too much space
adjust:
  shift: [0, -8]
  rotate: 90  # Vertical orientation
```

### ✅ Space-Efficient Approach
```yaml
# Horizontal diodes save vertical space
adjust:
  shift: [0, -6]  # Below switch but closer
  rotate: 0       # Horizontal orientation
```

**Key Lesson:** Rotate diodes horizontally (`rotate: 0`) to minimize vertical space usage. This prevents diodes from extending beyond the PCB edge, especially for bottom row switches.

## 4. MCU Placement and Rotation

### Calculated Positioning
**Use dimensions and calculations instead of magic numbers:**

```yaml
units:
  mcu_width: 18
  mcu_height: 33
  board_height: 4*ky + 25

footprints:
  mcu:
    what: promicro
    where:
      ref: matrix_col1_row1  # Same reference as board
      shift: [kx/2, board_height/2 - mcu_height/2 - 3]  # Calculated position
      rotate: 270  # USB pointing toward keys
```

**Key Lessons:**
- **Reference consistency:** Use the same reference point as your board outline
- **Edge positioning:** `board_height/2 - mcu_height/2 - margin` places MCU at board edge
- **USB accessibility:** `rotate: 270` points USB connector toward keys for easy access
- **Maintainable:** Changes to board size automatically adjust MCU position
- **✅ VALIDATED:** This formula works correctly - MCU stays at proper edge when board dimensions change

## 5. KiCad Sheet Positioning

### Standard Practice
**Use consistent anchor shifts for proper KiCad placement:**

```yaml
points:
  zones:
    matrix:
      anchor:
        shift: [50, -150]  # Standard KiCad positioning
```

**Key Lesson:** Most keyboards use `[50, -150]` or similar values. This positions the PCB properly on the KiCad sheet for easy viewing and editing.

## 6. Component Footprint Selection

### Mounting Holes
```yaml
what: ceoloide/mounting_hole_npth  # Non-plated through holes
```

### Switches
```yaml
what: mx  # For MX switches with hotswap support
params:
  hotswap: true
  keycaps: true
```

## 7. Case Design Considerations

### STL Generation
**Keep case definitions simple for reliable STL output:**

```yaml
cases:
  switch_plate:
    - name: plate      # Use pre-defined outline
      extrude: 1.6     # Simple extrusion
```

**Key Lesson:** Complex boolean operations in cases can break STL generation. Start simple and add complexity gradually.

## 8. Troubleshooting Checklist

When components appear off the PCB:
1. **Check diode orientation** - Use horizontal (`rotate: 0`) for space efficiency
2. **Verify board outline size** - Ensure it encompasses all components BUT keep borders tight
3. **Review mounting hole positions** - Use `kx/2, ky/2` shifts between switches
4. **Validate MCU calculations** - Use board dimensions, not magic numbers

When MCU appears to "float" in empty space:
1. **Reduce board padding** - Use minimal values (10-20mm total extra space)
2. **Check board_height calculation** - Should be just enough for MCU, not excessive
3. **Verify MCU positioning** - Should be at actual board edge, not in empty space

When STLs generate incorrectly:
1. **Simplify outlines** - Use rectangles instead of complex polygons
2. **Check case syntax** - Ensure proper `operation: subtract` syntax
3. **Verify extrude values** - Must be numbers, not strings (watch for typos like `1.6a`)

## 9. Units and Calculations

### Essential Units
```yaml
units:
  kx: 19.05          # MX key spacing
  ky: 19.05          # MX key spacing
  mcu_width: 18      # Pro Micro width
  mcu_height: 33     # Pro Micro height
  board_width: 4*kx + 10
  board_height: 4*ky + 25
```

**Key Lesson:** Define dimensions as units for maintainability. Use calculations instead of hardcoded values.

## 10. Template Configuration

### KiCad Compatibility
```yaml
pcbs:
  macropad:
    template: kicad8  # Ensures KiCad 8+ compatibility
```

**Key Lesson:** Always specify `template: kicad8` to avoid compatibility issues with modern KiCad versions.

---

## Summary

The key to successful Ergogen layouts is:
1. **Calculated positioning** over magic numbers
2. **Simple, reliable geometries** over complex shapes
3. **Space-efficient component placement**
4. **Consistent reference points** throughout the design
5. **Proper component orientation** for accessibility

These principles ensure maintainable, manufacturable, and professional keyboard designs.
#
# 11. Board Sizing Guidelines - CRITICAL LESSON

### ❌ Common Mistake: Excessive Board Padding
```yaml
# This creates too much empty space!
board_width: 8*kx + 30   # Too much padding
board_height: 3*ky + 50  # MCU will float in empty space
```

### ✅ Correct Approach: Tight Board Borders
```yaml
# Keep it minimal - just enough for components
board_width: 8*kx + 10   # 5mm padding each side
board_height: 3*ky + 20  # Just enough for MCU placement
```

**Key Lesson from 3x8 Keyboard:** Excessive board padding makes the MCU appear to "float" in empty space instead of being positioned at the actual board edge. Keep borders tight!

### Board Sizing Formula
- **Width:** `columns * kx + 10mm` (5mm padding each side)
- **Height:** `rows * ky + 20mm` (minimal space for MCU)
- **MCU Space:** Only add what's actually needed (~15-20mm)

### Component Simplification
- **Reset buttons:** Can be omitted from keyboard designs
- **Unnecessary footprints:** Remove to keep PCB clean and focused
- **Focus on essentials:** Switches, diodes, MCU, mounting holes

This lesson learned from the 3x8 keyboard is crucial for professional-looking PCB layouts!
#
# 12. Validation Results - 3x8 Keyboard Success

### ✅ Confirmed Working Techniques
All the following have been **tested and validated** on a 3x8 keyboard layout:

1. **MCU Positioning Formula:** `board_height/2 - mcu_height/2 - 3` correctly places MCU at top edge
2. **Mounting Hole Placement:** `shift: [kx/2, ky/2]` positions holes perfectly between switches
3. **Board Sizing:** Tight borders (`columns*kx + 10`, `rows*ky + 20`) prevent floating components
4. **Diode Orientation:** Horizontal placement (`rotate: 0`) keeps all components on PCB
5. **Reference Points:** Using matrix center as board reference works reliably

### Scalability Confirmed
- **4x4 macropad:** ✅ Working
- **3x8 keyboard:** ✅ Working  
- **Formula adapts automatically** when board dimensions change

### Next Steps Ready
With these validated techniques, we can confidently tackle:
- Different matrix sizes (4x12, 5x6, etc.)
- Additional features (rotary encoders, RGB, etc.)
- Split keyboard layouts
- Custom key arrangements

**The foundation is solid and proven.**

# 13. Case Design and USB Cutout Positioning - CRITICAL LESSON

### ❌ Common USB Cutout Mistakes
```yaml
# WRONG: Cutout positioned inside board boundary
usb_cutout:
  - what: rectangle
    where:
      ref: matrix_col3_row1
      shift: [kx/2, board_height/2 - 5]  # Inside board area!
    size: [12, 8]
```

**Problems with this approach:**
- Cutout is positioned within the board outline, not in the case wall
- No visible opening in the case wall
- USB connector remains inaccessible

### ✅ Correct USB Cutout Positioning
```yaml
# CORRECT: Cutout positioned in case wall area
usb_cutout:
  - what: rectangle
    where:
      ref: matrix_col3_row1
      shift: [kx/2, board_height/2 + case_wall_thickness/2]  # In wall area!
    size: [usb_cutout_width, usb_cutout_height]
    corner: usb_cutout_corner_radius
```

### Case Wall Cutout Implementation
```yaml
cases:
  case_bottom:
    - name: case_outer
      extrude: case_height
    - operation: subtract
      name: case_inner
      extrude: case_height - bottom_plate_thickness
      shift: [0, 0, bottom_plate_thickness]
    # CRITICAL: USB cutout in wall only, not through bottom
    - operation: subtract
      name: usb_cutout
      extrude: case_height - bottom_plate_thickness  # Wall height only
      shift: [0, 0, bottom_plate_thickness]          # Start above bottom plate
```

### Key Lessons Learned

1. **Cutout Positioning:** USB cutouts must be positioned **outside** the board boundary, in the case wall area
2. **Wall-Only Cutting:** Cutouts should only cut through the wall portion, not the bottom plate
3. **Height Management:** Use `case_height - bottom_plate_thickness` to avoid cutting through the bottom
4. **Z-Offset:** Start cutouts at `bottom_plate_thickness` height to preserve the bottom plate

### Formula for USB Cutout Position
- **X Position:** Same as MCU (`kx/2` from center reference)
- **Y Position:** `board_height/2 + case_wall_thickness/2` (in the wall area)
- **Z Position:** Start at `bottom_plate_thickness`, extrude for wall height only

### Validation
- ✅ **3x8 Keyboard:** USB cutout now visible in case wall
- ✅ **Side Access:** USB connector accessible from case side
- ✅ **Structural Integrity:** Bottom plate remains intact

**This lesson is crucial for functional case designs with proper connector access!**