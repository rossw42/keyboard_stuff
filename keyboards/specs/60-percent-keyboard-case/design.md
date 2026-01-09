# Design Document: 60% Wooden Keyboard Case

## Overview

This design document details a two-piece wooden keyboard case for 60% mechanical keyboards (GH60, BM60, Pok3r PCBs) manufactured via CNC machining. The case consists of a top frame piece and a bottom tray piece, both machined from hardwood stock. The design prioritizes manufacturing efficiency, structural integrity, and precise PCB fitment while maintaining aesthetic appeal of natural wood construction.

## Architecture

### Case Structure

The case uses a sandwich-style construction with two main components:

1. **Top Frame (Switch Plate Layer)**
   - Provides switch plate mounting surface
   - Creates the visible top border around keycaps
   - Houses the USB port cutout
   - Thickness: 5mm

2. **Bottom Tray**
   - Contains PCB mounting standoffs
   - Provides switch pin clearance cavity
   - Includes rubber feet recesses
   - Thickness: 15mm
   - Internal cavity depth: 8mm

### Assembly Method

The two pieces connect via:
- 6x M3 screws from bottom, threading into brass inserts in the top frame
- Brass inserts (M3 x 5.7mm OD x 4mm length) pressed into top frame
- Screw positions aligned with PCB mounting points for structural efficiency

## Components and Interfaces

### 1. Top Frame Component

**External Dimensions:**
- Length: 295mm
- Width: 105mm  
- Height: 5mm
- Corner radius: 3mm

**PCB Opening:**
- Length: 286mm (PCB width + 1mm clearance)
- Width: 95.6mm (PCB height + 1mm clearance)
- Positioned: Centered with 4.5mm border on all sides

**USB Port Cutout:**
- Width: 16mm
- Height: 10mm (extends through full 5mm thickness)
- Position: Centered on top edge, 7mm from PCB opening edge
- Shape: Rectangular with 1mm radius corners

**Brass Insert Holes (6 positions):**
- Diameter: 5.8mm (for 5.7mm OD brass inserts, press-fit)
- Depth: 4mm
- Positions match PCB mounting holes (see Requirements section)
- Counterbore from bottom surface

### 2. Bottom Tray Component

**External Dimensions:**
- Length: 295mm
- Width: 105mm
- Height: 15mm
- Corner radius: 3mm (matches top frame)

**Internal Cavity:**
- Length: 287mm
- Width: 96.6mm
- Depth: 8mm (from top surface)
- Wall thickness: 4mm minimum
- Corner radius: 2mm (internal corners, limited by 4mm endmill)

**PCB Standoff Pillars (6 positions):**
- Diameter: 6mm
- Height: 3mm (from cavity floor)
- Through-hole: 2.2mm diameter (for M2 screws)
- Positions match PCB mounting holes
- Integrated into cavity floor

**Screw Holes for Assembly (6 positions):**
- Diameter: 3.2mm (clearance for M3 screws)
- Position: Concentric with PCB standoff pillars
- Extends through full 15mm height
- Counterbore on bottom: 6mm diameter x 3mm depth (for screw head)

**Rubber Feet Recesses (4 corners):**
- Diameter: 10mm
- Depth: 2mm
- Position: 10mm from each corner (measured to center)
- For adhesive rubber feet (8mm diameter recommended)

**Typing Angle:**
- Front height: 15mm
- Rear height: 15mm (no angle in base design)
- Optional: Can be modified to 18mm rear height for 6-degree angle

## Data Models

### CNC Toolpath Data Structure

```
CaseProfile {
  component: "top_frame" | "bottom_tray"
  operations: [
    {
      type: "profile" | "pocket" | "drill" | "bore"
      tool: {
        diameter: number (mm)
        type: "endmill" | "drill"
        flutes: number
      }
      depth: number (mm)
      feedRate: number (mm/min)
      spindleSpeed: number (RPM)
      geometry: {
        paths: [Point2D[]]
        islands: [Point2D[]]?
      }
    }
  ]
  material: {
    type: "hardwood"
    thickness: number (mm)
    workpieceSize: {length, width, height}
  }
  origin: Point3D
  tolerances: {
    critical: ±0.1mm
    standard: ±0.2mm
  }
}
```

### Dimensional Reference Model

```
PCBLayout {
  dimensions: {
    length: 285mm
    width: 94.6mm
    thickness: 1.6mm
  }
  mountingHoles: [
    {id: "TL", x: 19, y: 9.5},
    {id: "TR", x: 266, y: 9.5},
    {id: "ML", x: 28.5, y: 47.3},
    {id: "MR", x: 256.5, y: 47.3},
    {id: "BL", x: 57, y: 85},
    {id: "BR", x: 228, y: 85}
  ]
  usbPort: {
    centerX: 142.5,
    offsetFromTop: 7mm
  }
}
```

## Manufacturing Process

### Material Preparation

1. **Stock Selection:**
   - Hardwood: Walnut, maple, or cherry recommended
   - Top frame: 295mm x 105mm x 5mm (can mill from 6mm stock)
   - Bottom tray: 295mm x 105mm x 15mm (can mill from 20mm stock)
   - Grain orientation: Length-wise for maximum strength

2. **Stock Preparation:**
   - Surface plane both sides
   - Ensure parallel faces within 0.05mm
   - Check for defects, knots, or cracks

### CNC Operations Sequence

#### Top Frame Machining

**Setup:** Secure workpiece with double-sided tape or vacuum table

**Operation 1: Face surfacing**
- Tool: 6mm flat endmill
- Depth: 0.5mm (ensure consistent thickness)
- Purpose: Create reference surface

**Operation 2: Brass insert counterbores (6x)**
- Tool: 6mm flat endmill
- Diameter: 5.8mm
- Depth: 4mm from bottom surface
- Requires workpiece flip or 5-axis

**Operation 3: PCB opening pocket**
- Tool: 6mm flat endmill (roughing), 3mm flat endmill (finishing)
- Depth: Through full 5mm thickness
- Dimensions: 286mm x 95.6mm
- Leave 0.5mm for finishing pass

**Operation 4: USB cutout**
- Tool: 3mm flat endmill
- Dimensions: 16mm x 10mm
- Position: Centered on top edge
- Corner radius: 1mm

**Operation 5: External profile**
- Tool: 6mm flat endmill (roughing), 3mm flat endmill (finishing)
- Corner radius: 3mm
- Leave tabs for final separation
- Finish pass: 0.2mm stock removal

#### Bottom Tray Machining

**Setup:** Secure workpiece with clamps or fixture

**Operation 1: Face surfacing**
- Tool: 6mm flat endmill
- Depth: 0.5mm

**Operation 2: Rubber feet recesses (4x)**
- Tool: 10mm flat endmill or 10mm drill
- Depth: 2mm
- Position: 10mm from corners

**Operation 3: Assembly screw counterbores (6x)**
- Tool: 6mm flat endmill
- Diameter: 6mm
- Depth: 3mm from bottom surface

**Operation 4: Assembly screw through-holes (6x)**
- Tool: 3.2mm drill
- Depth: Through full thickness
- Position: Concentric with counterbores

**Operation 5: Internal cavity pocket**
- Tool: 6mm flat endmill (roughing), 4mm flat endmill (finishing)
- Depth: 8mm from top surface
- Dimensions: 287mm x 96.6mm
- Corner radius: 2mm (limited by 4mm tool)
- Leave standoff pillars (6x positions)

**Operation 6: Standoff through-holes (6x)**
- Tool: 2.2mm drill
- Depth: Through standoff pillars into counterbore
- Position: Center of each standoff pillar

**Operation 7: External profile**
- Tool: 6mm flat endmill (roughing), 3mm flat endmill (finishing)
- Corner radius: 3mm
- Leave tabs for final separation

### Post-Machining Operations

1. **Tab removal:** Cut tabs with flush-cut saw, sand smooth
2. **Sanding:** Progress through 120, 220, 320 grit
3. **Brass insert installation:** Press-fit into top frame counterbores using arbor press
4. **Finishing:** Apply wood oil, wax, or polyurethane (3 coats minimum)
5. **Rubber feet:** Apply adhesive rubber feet to bottom recesses

## Tolerances and Fit

### Critical Dimensions (±0.1mm)
- PCB opening dimensions
- Mounting hole positions
- Brass insert hole diameter
- Standoff pillar positions

### Standard Dimensions (±0.2mm)
- External case dimensions
- Wall thicknesses
- USB cutout position
- Rubber feet recess positions

### Clearance Specifications
- PCB to case opening: 0.5mm per side (1mm total)
- USB connector to cutout: 2mm per side (4mm total width margin)
- Switch pins to cavity floor: 5mm minimum
- M2 screw to standoff hole: 0.1mm clearance (2.2mm hole for 2mm screw)
- M3 screw to assembly hole: 0.6mm clearance (3.2mm hole for 2.6mm screw)

## Error Handling

### Manufacturing Defects

**Wood Defects:**
- Issue: Knots, cracks, or voids in critical areas
- Prevention: Inspect stock before machining, avoid defects in mounting areas
- Recovery: Reject workpiece if defects in mounting or structural areas

**Dimensional Errors:**
- Issue: Out-of-tolerance dimensions
- Prevention: Verify tool diameter, check first-article measurements
- Recovery: If PCB opening too small, re-machine with offset; if too large, reject workpiece

**Tool Breakage:**
- Issue: Broken endmill during operation
- Prevention: Use appropriate feeds/speeds, check tool condition
- Recovery: Replace tool, restart operation from last safe position

**Tear-out:**
- Issue: Wood fiber tear-out on edges
- Prevention: Use sharp tools, climb milling, backing board
- Recovery: Fill with wood filler and sand, or reject if excessive

### Assembly Issues

**Brass Insert Misalignment:**
- Issue: Insert not perpendicular or not fully seated
- Prevention: Use insertion jig, press slowly
- Recovery: Heat insert and re-press, or drill out and use larger insert

**PCB Fit Issues:**
- Issue: PCB doesn't fit in opening
- Prevention: Verify dimensions before assembly
- Recovery: Carefully file or sand opening edges

**Screw Interference:**
- Issue: Assembly screws bottom out before tightening
- Prevention: Verify hole depths match screw lengths
- Recovery: Use shorter screws or deepen counterbores

## Testing Strategy

### Dimensional Verification

**First Article Inspection:**
1. Measure external dimensions with calipers (±0.2mm tolerance)
2. Measure PCB opening with calipers (±0.1mm tolerance)
3. Verify mounting hole positions with CMM or precision measurement (±0.1mm)
4. Check brass insert hole diameter with pin gauges (5.7-5.8mm)
5. Measure standoff heights with depth micrometer (3mm ±0.1mm)

**Functional Testing:**
1. Test-fit PCB in case opening (should slide in with minimal resistance)
2. Verify USB connector access (plug/unplug cable 10x without interference)
3. Check mounting screw engagement (all 6 screws should thread smoothly)
4. Verify assembly screw function (case halves should join flush)
5. Test switch installation (install 4 corner switches, verify clearance)

### Quality Assurance Checklist

**Visual Inspection:**
- [ ] No visible cracks, splits, or defects
- [ ] Clean edges, no tear-out
- [ ] Smooth surfaces (no tool marks)
- [ ] Brass inserts flush with surface
- [ ] Corner radii consistent

**Fit Testing:**
- [ ] PCB fits with 0.5mm clearance per side
- [ ] USB cable inserts without binding
- [ ] All 6 M2 screws thread into standoffs
- [ ] All 6 M3 assembly screws engage brass inserts
- [ ] Case halves mate flush (no gaps)
- [ ] Rubber feet sit flush in recesses

**Functional Testing:**
- [ ] PCB mounts securely without wobble
- [ ] Switches clear cavity floor (5mm minimum)
- [ ] Keycaps don't contact case when pressed
- [ ] Case sits stable on flat surface
- [ ] No sharp edges or splinters

### Production Testing Protocol

**Sample Rate:** First article + 1 per 10 units

**Test Sequence:**
1. Dimensional verification (5 minutes)
2. Visual inspection (2 minutes)
3. Fit testing with actual PCB (5 minutes)
4. Functional assembly test (5 minutes)

**Pass Criteria:**
- All critical dimensions within ±0.1mm
- All standard dimensions within ±0.2mm
- PCB fits and mounts securely
- No visual defects in critical areas
- All hardware engages properly

**Failure Response:**
- Document defect type and location
- Determine root cause (tooling, material, process)
- Implement corrective action
- Re-verify next unit

## Design Files Output

### Required Deliverables

1. **2D Technical Drawings (PDF + DXF)**
   - Top frame profile with dimensions
   - Bottom tray profile with dimensions
   - Assembly view with hardware callouts
   - Detail views of mounting features

2. **CNC Toolpaths (DXF or G-code)**
   - Top frame operations (separate file per operation)
   - Bottom tray operations (separate file per operation)
   - Tool list with specifications
   - Setup sheets with work holding instructions

3. **3D Models (STEP format)**
   - Top frame solid model
   - Bottom tray solid model
   - Assembly model with PCB reference
   - Hardware models (screws, inserts, feet)

4. **Manufacturing Documentation**
   - Bill of materials (wood, hardware, finishing supplies)
   - Operation sequence sheets
   - Quality control checklist
   - Assembly instructions

## Design Variations

### Optional Modifications

**Typing Angle Variant:**
- Increase rear height to 18mm (6-degree angle)
- Adjust cavity depth to maintain 8mm
- Modify rubber feet positions for stability

**High-Profile Variant:**
- Increase top frame height to 10mm
- Creates more prominent border around keycaps
- Requires deeper brass insert counterbores (9mm)

**Integrated Plate Variant:**
- Add switch plate cutouts to top frame
- Requires 14mm x 14mm openings for each switch position
- Increases machining time significantly
- Provides plate-mount switch support

**Wrist Rest Extension:**
- Extend bottom tray forward by 80mm
- Add contoured wrist rest surface
- Requires larger stock material
- Optional magnetic attachment

## Material Alternatives

**Hardwood Options:**
- Walnut: Dark, premium appearance, moderate hardness
- Maple: Light color, very hard, excellent stability
- Cherry: Medium tone, ages beautifully, moderate hardness
- Oak: Prominent grain, very hard, traditional look

**Exotic Options:**
- Padauk: Bright orange-red, very hard
- Purpleheart: Purple hue, extremely hard
- Zebrawood: Striped pattern, decorative

**Considerations:**
- Hardness: Affects machining speed and tool wear
- Grain: Open grain (oak) requires pore filling
- Stability: Maple most stable, avoid species prone to movement
- Cost: Exotic woods significantly more expensive
