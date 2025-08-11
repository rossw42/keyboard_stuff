# Ergogen Mounting Style Examples

This document provides practical Ergogen configuration examples for implementing different keyboard mounting styles. Each example uses a simple 2x2 keyboard layout to clearly demonstrate the mounting concepts without complexity.

## Base Configuration Template

All examples build on this common foundation:

```yaml
meta:
  engine: 4.1.0
  name: mounting_style_example
  version: 1.0

units:
  # Standard MX key spacing
  kx: 19.05
  ky: 19.05
  
  # Case parameters
  case_wall_thickness: 2.5
  case_height: 12
  plate_thickness: 1.6
  pcb_thickness: 1.6
  
  # Mounting parameters (varies by style)
  mount_hole_diameter: 2.2
  screw_head_diameter: 6

points:
  zones:
    matrix:
      anchor:
        shift: [50, -50]  # Position for KiCad
      key:
        padding: ky
        spread: kx
        tags: [key, switch]
      columns:
        col0:
          key.column_net: col0
        col1:
          key.column_net: col1
      rows:
        row0:
          row_net: row0
        row1:
          row_net: row1
```

---

## 1. Tray Mount

**Concept**: PCB screws directly to mounting posts in the bottom case.

**Key Features**:
- Simplest mounting method
- Standardized screw positions
- PCB bears all mounting stress
- Most cost-effective

```yaml
# Tray Mount Example
units:
  $extends: meta.base_units
  tray_post_height: 8  # Height of mounting posts

points:
  $extends: meta.base_points
  zones:
    # Add mounting posts at corners
    mount_posts:
      anchor:
        ref: matrix_col0_row0
        shift: [-kx/2, ky/2]
      key:
        tags: [mount_post]
      columns:
        post_tl:  # Top-left
        post_tr:  # Top-right
          key.shift: [kx, 0]
        post_bl:  # Bottom-left
          key.shift: [0, -ky]
        post_br:  # Bottom-right
          key.shift: [kx, -ky]

outlines:
  # Switch cutouts
  _switch_cutouts:
    - what: rectangle
      where: [switch]
      size: [14, 14]  # MX switch cutout
  
  # Mounting holes in PCB
  _mount_holes:
    - what: circle
      where: [mount_post]
      radius: mount_hole_diameter/2
  
  # PCB outline
  pcb_outline:
    - what: rectangle
      where: [switch]
      bound: true
      size: [kx, ky]
      fillet: 2
    - what: outline
      name: _mount_holes
      operation: subtract
  
  # Bottom case with mounting posts
  case_bottom:
    - what: outline
      name: pcb_outline
      expand: case_wall_thickness
      fillet: 3
    - what: outline
      name: _mount_holes
      operation: subtract

cases:
  # Tray mount case - posts integrated into bottom
  tray_case:
    - what: outline
      name: case_bottom
      extrude: case_height
    # Add mounting posts
    - what: circle
      where: [mount_post]
      radius: 3  # Post diameter
      extrude: tray_post_height
      operation: add

pcbs:
  tray_mount_pcb:
    outlines:
      main:
        outline: pcb_outline
    footprints:
      switches:
        what: mx
        where: [switch]
        params:
          hotswap: true
          from: "{{column_net}}"
          to: "{{colrow}}"
      mount_holes:
        what: mounting_hole
        where: [mount_post]
        params:
          drill: mount_hole_diameter
```

---

## 2. Top Mount

**Concept**: Plate attaches to mounting tabs on the top case.

**Key Features**:
- Plate bears mounting stress
- Better typing feel than tray mount
- Requires custom plate design
- Popular in mid-range keyboards

```yaml
# Top Mount Example
units:
  $extends: meta.base_units
  plate_tab_width: 8
  plate_tab_length: 6

points:
  $extends: meta.base_points
  zones:
    # Plate mounting tabs
    plate_tabs:
      anchor:
        ref: matrix_col0_row0
        shift: [-kx/2 - plate_tab_length/2, ky/2]
      key:
        width: plate_tab_length
        height: plate_tab_width
        tags: [plate_tab]
      columns:
        tab_tl:  # Top-left tab
        tab_tr:  # Top-right tab
          key.shift: [kx + plate_tab_length, 0]
        tab_bl:  # Bottom-left tab
          key.shift: [0, -ky]
        tab_br:  # Bottom-right tab
          key.shift: [kx + plate_tab_length, -ky]

outlines:
  # Switch plate with mounting tabs
  switch_plate:
    - what: rectangle
      where: [switch]
      bound: true
      size: [kx, ky]
      fillet: 1
    # Add mounting tabs
    - what: rectangle
      where: [plate_tab]
      size: [plate_tab_length, plate_tab_width]
      operation: add
    # Subtract switch cutouts
    - what: rectangle
      where: [switch]
      size: [14, 14]
      operation: subtract
    # Subtract mounting holes in tabs
    - what: circle
      where: [plate_tab]
      radius: mount_hole_diameter/2
      operation: subtract
  
  # Top case with mounting points
  case_top:
    - what: outline
      name: switch_plate
      expand: case_wall_thickness
      fillet: 3
    # Add mounting boss areas
    - what: rectangle
      where: [plate_tab]
      size: [plate_tab_length + 4, plate_tab_width + 4]
      operation: add
  
  # Bottom case (simple)
  case_bottom:
    - what: outline
      name: switch_plate
      expand: case_wall_thickness
      fillet: 3

cases:
  top_mount_case:
    # Bottom case
    - what: outline
      name: case_bottom
      extrude: case_height - plate_thickness
    # Top case with mounting bosses
    - what: outline
      name: case_top
      extrude: plate_thickness
      shift: [0, 0, case_height - plate_thickness]
      operation: add
    # Subtract mounting holes
    - what: circle
      where: [plate_tab]
      radius: mount_hole_diameter/2
      extrude: plate_thickness + 2
      shift: [0, 0, case_height - plate_thickness - 1]
      operation: subtract
```

---

## 3. Bottom Mount

**Concept**: Plate attaches to mounting points on the bottom case.

**Key Features**:
- More consistent stiffness than top mount
- Allows floating top case design
- Better support for flexible plates
- Common in premium keyboards

```yaml
# Bottom Mount Example
units:
  $extends: meta.base_units
  bottom_mount_boss_height: 6

points:
  $extends: meta.base_points
  zones:
    # Bottom mounting points
    bottom_mounts:
      anchor:
        ref: matrix_col0_row0
        shift: [-kx/2, ky/2]
      key:
        tags: [bottom_mount]
      columns:
        mount_tl:
        mount_tr:
          key.shift: [kx, 0]
        mount_bl:
          key.shift: [0, -ky]
        mount_br:
          key.shift: [kx, -ky]

outlines:
  # Plate with bottom mounting holes
  switch_plate:
    - what: rectangle
      where: [switch]
      bound: true
      size: [kx, ky]
      fillet: 1
    # Switch cutouts
    - what: rectangle
      where: [switch]
      size: [14, 14]
      operation: subtract
    # Bottom mounting holes
    - what: circle
      where: [bottom_mount]
      radius: mount_hole_diameter/2
      operation: subtract
  
  # Bottom case with mounting bosses
  case_bottom:
    - what: outline
      name: switch_plate
      expand: case_wall_thickness
      fillet: 3
    # Add mounting boss areas
    - what: circle
      where: [bottom_mount]
      radius: 4  # Boss diameter
      operation: add
  
  # Floating top case
  case_top:
    - what: rectangle
      where: [switch]
      bound: true
      size: [kx - 2, ky - 2]  # Slightly smaller for floating effect
      expand: case_wall_thickness - 1
      fillet: 3

cases:
  bottom_mount_case:
    # Bottom case with mounting bosses
    - what: outline
      name: case_bottom
      extrude: case_height
    # Add mounting bosses
    - what: circle
      where: [bottom_mount]
      radius: 4
      extrude: bottom_mount_boss_height
      shift: [0, 0, case_height - bottom_mount_boss_height]
      operation: add
    # Floating top case
    - what: outline
      name: case_top
      extrude: 2
      shift: [0, 0, case_height - 2]
      operation: add
    # Mounting holes through bosses
    - what: circle
      where: [bottom_mount]
      radius: mount_hole_diameter/2
      extrude: case_height + 2
      shift: [0, 0, -1]
      operation: subtract
```

---

## 4. Sandwich Mount

**Concept**: Screws pass through bottom case, plate, and top case.

**Key Features**:
- Even force distribution
- Balanced typing experience
- Requires precise alignment
- Good acoustic properties

```yaml
# Sandwich Mount Example
units:
  $extends: meta.base_units
  sandwich_screw_length: 16  # Must span entire assembly

points:
  $extends: meta.base_points
  zones:
    # Sandwich mounting points
    sandwich_mounts:
      anchor:
        ref: matrix_col0_row0
        shift: [-kx/2, ky/2]
      key:
        tags: [sandwich_mount]
      columns:
        mount_tl:
        mount_tr:
          key.shift: [kx, 0]
        mount_bl:
          key.shift: [0, -ky]
        mount_br:
          key.shift: [kx, -ky]

outlines:
  # Plate with through-holes
  switch_plate:
    - what: rectangle
      where: [switch]
      bound: true
      size: [kx, ky]
      fillet: 1
    # Switch cutouts
    - what: rectangle
      where: [switch]
      size: [14, 14]
      operation: subtract
    # Through-holes for sandwich screws
    - what: circle
      where: [sandwich_mount]
      radius: mount_hole_diameter/2
      operation: subtract
  
  # Top and bottom cases (identical for sandwich)
  case_shell:
    - what: outline
      name: switch_plate
      expand: case_wall_thickness
      fillet: 3
    # Screw boss areas
    - what: circle
      where: [sandwich_mount]
      radius: screw_head_diameter/2 + 1
      operation: add

cases:
  sandwich_mount_case:
    # Bottom case
    - what: outline
      name: case_shell
      extrude: case_height/2
    # Top case
    - what: outline
      name: case_shell
      extrude: case_height/2
      shift: [0, 0, case_height/2 + plate_thickness]
      operation: add
    # Through-holes for sandwich screws
    - what: circle
      where: [sandwich_mount]
      radius: mount_hole_diameter/2
      extrude: case_height + plate_thickness + 2
      shift: [0, 0, -1]
      operation: subtract
    # Countersink for screw heads (bottom)
    - what: circle
      where: [sandwich_mount]
      radius: screw_head_diameter/2
      extrude: 3
      operation: subtract
```

---

## 5. Integrated Plate

**Concept**: Plate and top case are one piece.

**Key Features**:
- Very rigid construction
- Simplified assembly
- Cost-effective for production
- No plate customization

```yaml
# Integrated Plate Example
units:
  $extends: meta.base_units

points:
  $extends: meta.base_points
  zones:
    # Simple mounting points
    integrated_mounts:
      anchor:
        ref: matrix_col0_row0
        shift: [-kx/2, ky/2]
      key:
        tags: [integrated_mount]
      columns:
        mount_tl:
        mount_tr:
          key.shift: [kx, 0]
        mount_bl:
          key.shift: [0, -ky]
        mount_br:
          key.shift: [kx, -ky]

outlines:
  # Integrated top case/plate
  integrated_top:
    - what: rectangle
      where: [switch]
      bound: true
      size: [kx, ky]
      expand: case_wall_thickness
      fillet: 3
    # Mounting boss areas
    - what: circle
      where: [integrated_mount]
      radius: 4
      operation: add
  
  # Bottom case
  case_bottom:
    - what: outline
      name: integrated_top
      fillet: 3

cases:
  integrated_plate_case:
    # Bottom case
    - what: outline
      name: case_bottom
      extrude: case_height - plate_thickness
    # Integrated top case/plate
    - what: outline
      name: integrated_top
      extrude: plate_thickness
      shift: [0, 0, case_height - plate_thickness]
      operation: add
    # Switch cutouts (cut through integrated plate)
    - what: rectangle
      where: [switch]
      size: [14, 14]
      extrude: plate_thickness + 1
      shift: [0, 0, case_height - plate_thickness - 0.5]
      operation: subtract
    # Mounting holes
    - what: circle
      where: [integrated_mount]
      radius: mount_hole_diameter/2
      extrude: case_height + 2
      shift: [0, 0, -1]
      operation: subtract
```

---

## 6. Gasket Mount

**Concept**: Plate floats on gaskets between case halves.

**Key Features**:
- Superior typing comfort
- Excellent sound dampening
- Most complex to design
- Premium keyboard experience

```yaml
# Gasket Mount Example
units:
  $extends: meta.base_units
  gasket_thickness: 2
  gasket_width: 4
  gasket_compression: 0.5  # How much gasket compresses

points:
  $extends: meta.base_points
  zones:
    # Gasket contact points
    gasket_points:
      anchor:
        ref: matrix_col0_row0
        shift: [-kx/2 - gasket_width/2, ky/2]
      key:
        width: gasket_width
        height: gasket_width
        tags: [gasket_contact]
      columns:
        gasket_tl:
        gasket_tr:
          key.shift: [kx + gasket_width, 0]
        gasket_bl:
          key.shift: [0, -ky]
        gasket_br:
          key.shift: [kx + gasket_width, -ky]
    
    # Case mounting points (screws only connect case halves)
    case_mounts:
      anchor:
        ref: matrix_col0_row0
        shift: [-kx/2 - 10, ky/2 + 10]
      key:
        tags: [case_mount]
      columns:
        case_tl:
        case_tr:
          key.shift: [kx + 20, 0]
        case_bl:
          key.shift: [0, -ky - 20]
        case_br:
          key.shift: [kx + 20, -ky - 20]

outlines:
  # Floating plate (no direct mounting)
  switch_plate:
    - what: rectangle
      where: [switch]
      bound: true
      size: [kx, ky]
      fillet: 1
    # Switch cutouts
    - what: rectangle
      where: [switch]
      size: [14, 14]
      operation: subtract
    # Gasket contact areas on plate
    - what: rectangle
      where: [gasket_contact]
      size: [gasket_width, gasket_width]
      operation: add
  
  # Top case with gasket channels
  case_top:
    - what: outline
      name: switch_plate
      expand: case_wall_thickness + 5
      fillet: 3
    # Gasket channels (recessed areas)
    - what: rectangle
      where: [gasket_contact]
      size: [gasket_width + 1, gasket_width + 1]
      operation: subtract
    # Case mounting holes
    - what: circle
      where: [case_mount]
      radius: mount_hole_diameter/2
      operation: subtract
  
  # Bottom case with gasket channels
  case_bottom:
    - what: outline
      name: case_top  # Same as top for gasket mount

cases:
  gasket_mount_case:
    # Bottom case with gasket channels
    - what: outline
      name: case_bottom
      extrude: case_height/2
    # Gasket channels (bottom)
    - what: rectangle
      where: [gasket_contact]
      size: [gasket_width + 1, gasket_width + 1]
      extrude: gasket_thickness
      shift: [0, 0, case_height/2 - gasket_thickness]
      operation: subtract
    
    # Top case with gasket channels
    - what: outline
      name: case_top
      extrude: case_height/2
      shift: [0, 0, case_height/2 + plate_thickness + gasket_thickness]
      operation: add
    # Gasket channels (top)
    - what: rectangle
      where: [gasket_contact]
      size: [gasket_width + 1, gasket_width + 1]
      extrude: gasket_thickness
      shift: [0, 0, case_height/2 + plate_thickness]
      operation: subtract
    
    # Case mounting holes (only through case, not plate)
    - what: circle
      where: [case_mount]
      radius: mount_hole_diameter/2
      extrude: case_height + 2
      shift: [0, 0, -1]
      operation: subtract
```

---

## 7. Spring Mount

**Concept**: Springs provide cushioning between plate and case.

**Key Features**:
- Dynamic response
- Sound dampening
- Complex to design
- Unique typing feel

```yaml
# Spring Mount Example
units:
  $extends: meta.base_units
  spring_diameter: 6
  spring_height: 4
  spring_compression: 1

points:
  $extends: meta.base_points
  zones:
    # Spring mounting points
    spring_points:
      anchor:
        ref: matrix_col0_row0
        shift: [-kx/2, ky/2]
      key:
        tags: [spring_mount]
      columns:
        spring_tl:
        spring_tr:
          key.shift: [kx, 0]
        spring_bl:
          key.shift: [0, -ky]
        spring_br:
          key.shift: [kx, -ky]

outlines:
  # Plate with spring mounting posts
  switch_plate:
    - what: rectangle
      where: [switch]
      bound: true
      size: [kx, ky]
      fillet: 1
    # Switch cutouts
    - what: rectangle
      where: [switch]
      size: [14, 14]
      operation: subtract
    # Spring mounting posts on plate
    - what: circle
      where: [spring_mount]
      radius: 2  # Small post for spring centering
      operation: add
  
  # Case with spring wells
  case_bottom:
    - what: outline
      name: switch_plate
      expand: case_wall_thickness
      fillet: 3
    # Spring wells
    - what: circle
      where: [spring_mount]
      radius: spring_diameter/2 + 0.5
      operation: subtract

cases:
  spring_mount_case:
    # Bottom case with spring wells
    - what: outline
      name: case_bottom
      extrude: case_height
    # Spring wells
    - what: circle
      where: [spring_mount]
      radius: spring_diameter/2 + 0.5
      extrude: spring_height + 1
      shift: [0, 0, case_height - spring_height - 1]
      operation: subtract
    
    # Top case (simple)
    - what: rectangle
      where: [switch]
      bound: true
      size: [kx - 2, ky - 2]
      expand: case_wall_thickness - 1
      fillet: 3
      extrude: 2
      shift: [0, 0, case_height - 2]
      operation: add
```

---

## 8. Plateless Mount

**Concept**: No plate - switches mount directly to PCB.

**Key Features**:
- Unique elastic feel
- Requires precise PCB design
- Direct force transmission
- Cost savings potential

```yaml
# Plateless Mount Example
units:
  $extends: meta.base_units
  pcb_reinforcement_thickness: 3.2  # Double thickness PCB

points:
  $extends: meta.base_points
  zones:
    # PCB mounting points (more needed for stability)
    pcb_mounts:
      anchor:
        ref: matrix_col0_row0
        shift: [-kx/2, ky/2]
      key:
        tags: [pcb_mount]
      columns:
        mount_tl:
        mount_tr:
          key.shift: [kx, 0]
        mount_bl:
          key.shift: [0, -ky]
        mount_br:
          key.shift: [kx, -ky]
        # Additional center mounts for PCB support
        mount_tc:
          key.shift: [kx/2, 0]
        mount_bc:
          key.shift: [kx/2, -ky]

outlines:
  # Reinforced PCB outline (no separate plate)
  pcb_outline:
    - what: rectangle
      where: [switch]
      bound: true
      size: [kx, ky]
      fillet: 2
    # PCB mounting holes
    - what: circle
      where: [pcb_mount]
      radius: mount_hole_diameter/2
      operation: subtract
  
  # Case with PCB support ledge
  case_bottom:
    - what: outline
      name: pcb_outline
      expand: case_wall_thickness
      fillet: 3
    # PCB support ledge
    - what: outline
      name: pcb_outline
      expand: 1
      operation: add

cases:
  plateless_mount_case:
    # Bottom case with PCB ledge
    - what: outline
      name: case_bottom
      extrude: case_height - pcb_reinforcement_thickness
    # PCB support ledge
    - what: outline
      name: pcb_outline
      expand: 1
      extrude: 1
      shift: [0, 0, case_height - pcb_reinforcement_thickness - 1]
      operation: add
    
    # Top case (minimal)
    - what: outline
      name: pcb_outline
      expand: case_wall_thickness
      fillet: 3
      extrude: 2
      shift: [0, 0, case_height - 2]
      operation: add
    
    # PCB mounting holes
    - what: circle
      where: [pcb_mount]
      radius: mount_hole_diameter/2
      extrude: case_height + 2
      shift: [0, 0, -1]
      operation: subtract

pcbs:
  plateless_pcb:
    outlines:
      main:
        outline: pcb_outline
    footprints:
      # 5-pin switches for better PCB stability
      switches:
        what: mx
        where: [switch]
        params:
          hotswap: false  # Soldered for better support
          from: "{{column_net}}"
          to: "{{colrow}}"
      pcb_mounts:
        what: mounting_hole
        where: [pcb_mount]
        params:
          drill: mount_hole_diameter
```

---

## Design Complexity Ranking

From simplest to most complex to implement in Ergogen:

1. **Tray Mount** - Basic mounting posts, standard approach
2. **Integrated Plate** - Single-piece design, straightforward
3. **Plateless Mount** - No plate needed, but requires PCB reinforcement
4. **Top/Bottom Mount** - Custom plate tabs, moderate complexity
5. **Sandwich Mount** - Through-hole alignment critical
6. **Spring Mount** - Spring integration and wells
7. **Gasket Mount** - Most complex with gasket channels and floating plate

## Usage Notes

- All examples use a 2x2 matrix for clarity
- Adjust `case_wall_thickness`, `case_height`, and mounting parameters for your needs
- Test fit with 3D printed prototypes before final production
- Consider switch type (3-pin vs 5-pin) for plateless designs
- Gasket material selection is critical for gasket mount success

---

## Physical Case Design Workflow

After generating your Ergogen configuration, you'll need to create the physical 3D case. This section provides a detailed workflow adapted from Sadek Baroudi's comprehensive case design guide.

### Prerequisites

- Basic understanding of KiCad
- Inkscape installed (for SVG to DXF conversion)
- Fusion 360 installed
- Completed PCB design from Ergogen

### Complete Workflow: Ergogen → KiCad → Fusion 360 → 3D Print

#### Step 1: Prepare KiCad PCB for Case Design

After generating your PCB from Ergogen, you need to identify key elements for case design:

**Essential Elements to Consider:**
- PCB outline (Edge.Cuts layer)
- Switch locations and cutouts
- Controller placement and cutouts
- Reset switch location
- TRRS/USB connector openings
- Rotary encoders (if present)
- OLED displays (if present)
- Mounting holes for standoffs

**Layer Management for Export:**
1. Hide copper layers to see PCB structure clearly
2. Show only essential layers:
   - `User.Eco2` (for custom markings)
   - `Edge.Cuts` (PCB outline)
   - `F.Courtyard` (component boundaries)

**Add Mounting Hole Indicators:**
If mounting holes aren't visible on your selected layers:
1. Edit each mounting hole footprint
2. Add a circle on the `User.Eco2` layer centered on the hole
3. Save the footprint updates

#### Step 2: Export PCB Data for Case Design

**Export SVG from KiCad:**
1. Plot → SVG
2. Include only the layers identified above
3. Ensure proper scaling and units

**Convert SVG to DXF:**
1. Open SVG in Inkscape
2. Save As → DXF
3. Use R14 format
4. Set units to millimeters

#### Step 3: Fusion 360 Case Design Process

**Initial Setup:**
1. Enable "Capture Design History" in Fusion 360
2. Import the DXF file
3. Verify all elements imported correctly

**Critical Dimension Checks:**
```yaml
# Switch hole dimensions to verify:
choc_switches: 13.95mm
mx_switches: 14mm
mx_hotswap_compatible: 14mm  # Works for both MX and Choc

# Mounting hole dimensions:
m2_screws: 2.5mm diameter
m3_screws: 3.5mm diameter
```

**Adjust Switch Holes if Needed:**
1. Select all switch holes
2. Use Offset tool to adjust to correct dimensions
3. Confirm measurements with Dimension tool

**Clean Up PCB Outline:**
1. Check perimeter for continuity
2. Fix any broken lines or unwanted curves
3. Ensure clean geometric shapes

**Fix Mounting Holes:**
1. Find center point of each mounting hole
2. Delete imported circles
3. Create new circles with correct diameter (2.5mm for M2)

#### Step 4: Create Case Structure

**Case Wall Design:**
```yaml
# Typical case parameters
inner_wall_offset: 1mm      # Clearance for PCB manufacturing tolerance
outer_wall_offset: 3mm      # For 2mm thick walls (1mm + 2mm)
wall_thickness: 2-3mm       # Structural strength
case_height: varies_by_mount_style
```

**Wall Creation Process:**
1. Offset PCB outline by 1mm inward (inner wall clearance)
2. Offset again by wall thickness amount (outer wall)
3. This creates the case wall profile

**Switch Plate Extrusion:**
```yaml
# Plate thickness guidelines
standard_plate: 1.6mm
thick_plate: 2.0mm        # Maximum recommended
thin_plate: 1.2mm         # Minimum for stability
```

Extrude the plate area (excluding switch holes and component cutouts).

**Case Wall Heights by Mount Style:**
```yaml
# From mounting style examples above
tray_mount:
  choc_soldered: 3mm
  choc_hotswap: 4.5mm
  mx_soldered: 6.5mm
  mx_hotswap: 8mm

top_mount:
  varies: "depends on plate attachment method"

bottom_mount:
  varies: "depends on boss height and plate thickness"

gasket_mount:
  varies: "depends on gasket thickness and compression"
```

#### Step 5: Component Accommodations

**Controller/MCU Cutouts:**
1. Measure controller dimensions from PCB layout
2. Create cutout with 1-2mm clearance on all sides
3. Consider cable routing and connector access

**TRRS/USB Connector Openings:**
```yaml
# Common connector clearances
trrs_3.5mm: 
  width: 8mm
  height: 6mm
  depth: 12mm    # For cable clearance

usb_c:
  width: 10mm
  height: 4mm
  depth: 8mm

micro_usb:
  width: 8mm
  height: 3mm
  depth: 6mm
```

**Reset Button Access:**
- Create small hole or channel for reset button access
- Typical diameter: 2-3mm
- Consider adding a funnel shape for easier access

#### Step 6: Bottom Plate Design

**Create Bottom Plate:**
1. Copy case outer outline
2. Copy mounting holes
3. Extrude to desired thickness (typically 2mm)

**Optional Enhancements:**
- Chamfer mounting holes for countersunk screws
- Add rubber bumper recesses
- Include cable routing channels
- Add ventilation holes if needed

#### Step 7: Case Assembly Integration

**Mounting System Design:**
Depending on your chosen mounting style:

**Tray Mount:**
- Integrate mounting posts into bottom case
- Posts should align with PCB mounting holes
- Post height = case height - plate thickness - PCB thickness

**Top/Bottom Mount:**
- Create mounting tabs or bosses
- Ensure proper screw access
- Consider tool clearance for assembly

**Gasket Mount:**
- Design gasket channels with proper tolerances
- Account for gasket compression
- Create separate mounting for case halves

#### Step 8: Finalization and Export

**Add Style Elements:**
- Chamfer sharp edges (0.5-1mm typical)
- Add texture or branding elements
- Consider ergonomic improvements

**Final Checks:**
1. Verify all mounting holes align
2. Check component clearances
3. Confirm switch hole dimensions
4. Test fit with 3D printed prototype

**Export for 3D Printing:**
- Export as STL or 3MF
- Separate files for each case component
- Include assembly instructions/BOM

### Case Design Best Practices

**Tolerances:**
```yaml
# 3D printing tolerances
tight_fit: 0.1-0.2mm      # Press fit
loose_fit: 0.3-0.5mm      # Easy assembly
clearance: 0.5-1.0mm      # Component movement
```

**Structural Considerations:**
- Minimum wall thickness: 1.5mm for PLA
- Add ribs for large flat surfaces
- Consider print orientation for strength
- Design for your printer's capabilities

**Assembly Considerations:**
- Minimize support material needs
- Design screw access carefully
- Consider cable routing from start
- Plan for disassembly/maintenance

**Material Selection:**
```yaml
PLA: 
  pros: "Easy to print, rigid"
  cons: "Can deform with heat"
  
PETG:
  pros: "Chemical resistance, flexibility"
  cons: "Harder to print"
  
ABS:
  pros: "Strong, heat resistant"
  cons: "Requires heated bed, fumes"
```

### Common Design Issues and Solutions

**Problem: Switch holes too tight/loose**
- Solution: Measure and adjust offset in Fusion 360
- Test with single switch before full print

**Problem: PCB doesn't fit in case**
- Solution: Increase inner wall offset
- Check for component interference

**Problem: Mounting holes misaligned**
- Solution: Export fresh DXF from KiCad
- Verify mounting hole footprint placement

**Problem: Case too tall/short**
- Solution: Adjust extrusion heights
- Consider switch type and mounting style

### Testing and Iteration

**Prototype Testing Process:**
1. Print single corner section first
2. Test PCB fit and switch alignment
3. Print full case with cheap filament
4. Test assembly and function
5. Iterate design as needed
6. Final print with quality filament

**Common Iterations:**
- Mounting hole position tweaks
- Component clearance adjustments
- Wall thickness optimization
- Aesthetic improvements

## Next Steps

1. Choose a mounting style based on your priorities (cost, feel, complexity)
2. Adapt the example to your specific keyboard layout
3. Add electronics (MCU, connectors) to the design
4. Follow the physical case design workflow above
5. Generate and test with 3D printed prototypes
6. Iterate on tolerances and fit

Each mounting style offers different trade-offs between cost, complexity, typing feel, and sound characteristics. Start with simpler designs and work up to more complex implementations as you gain experience with Ergogen and keyboard design.

### Additional Resources

- [Sadek Baroudi's Complete Case Design Guide](https://github.com/sadekbaroudi/keyboard-guides)
- [Ergogen Documentation](https://docs.ergogen.xyz/)
- [KiCad PCB Design Best Practices](https://docs.kicad.org/)
- [Fusion 360 Learning Resources](https://www.autodesk.com/products/fusion-360/learning-training-certification)
