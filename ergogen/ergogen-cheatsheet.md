# Ergogen AI Cheatsheet

**Quick reference for AI-assisted Ergogen keyboard design**

---

## Core Concepts

### What is Ergogen?

Ergogen is a parametric keyboard design framework that generates PCBs, cases, and outlines from YAML configuration. It's NOT a visual tool—it's code-driven.

**Output:** PCB files (KiCad), case geometry, keyboard outlines
**Input:** YAML config + footprint definitions

---

## Project Structure

```
my-keyboard/
├── ergogen.yaml          # Main config
├── footprints/           # Custom footprint definitions
├── cases/                # Case geometry files  
└── outputs/              # Generated files (PCB, SVG, DXF, etc)
```

---

## Configuration Hierarchy

1. **Metadata** - Project info, author, description
2. **Units** - Define measurement shortcuts (mm, px, etc)
3. **Points** - Define key positions [x, y, rotation]
4. **Outlines** - Use points to create board perimeter
5. **PCBs** - Add traces, pads, footprints to outlines
6. **Cases** - Create 3D case geometry

---

## Key YAML Sections

### Metadata
```yaml
metadata:
  name: My Keyboard
  author: Your Name
  description: A custom keyboard design
```

### Units
```yaml
units:
  u: 19.05                    # Standard key unit
  pad_size: 2.0               # Default pad size
```

### Points (Coordinates)

Points define key positions: `[x, y, rotation°]`

**Anchor Methods:**
- `ref: <point_name>` - Reference existing point as base
- `shift: [x, y]` - Translate relative to rotation
- `rotate: <degrees>` - Post-rotation after shift
- `orient: <degrees>` or `<point>` - Pre-rotation before shift
- `aggregate: {parts: [...], method: average}` - Combine multiple points

**Example:**
```yaml
points:
  key:
    ref: [0, 0]              # Start at origin
    rows: 4
    cols: 6
    spread: u                # Space keys 19.05mm apart
```

---

## Coordinate System

```
      +Y (up)
        |
        → Key rotation 0° points up
        
-X (left) ← → +X (right)
        |
      -Y (down)
```

**Rotation Rules:**
- 0° = pointing up
- +90° = pointing left (counter-clockwise)
- -90° = pointing right (clockwise)
- Shifts apply AFTER rotation

---

## Outlines (Board Perimeter)

Create keyboard boundary by connecting points or tracing polygons.

**Methods:**
- `ref` - Reference point(s)
- `path` - Draw lines connecting points
- `polygon` - Create filled or unfilled shapes
- `corners` - Round corners with radius

**Example:**
```yaml
outlines:
  board:
    ref: key
    offset: 5                 # Expand by 5mm
    polygon: true
```

---

## PCBs (Traces & Footprints)

Defines electrical design.

**Key Components:**
- **Footprints** - Where components go (switches, diodes, MCU)
- **Traces** - Electrical connections
- **Pads** - Mounting points
- **Via** - Through-hole connections

**Footprint Types:**
- `mx` / `alps` - Keyboard switch footprints
- `diode` - Protection diodes under switches
- `smd` - Surface-mount components (MCU, resistors, capacitors)
- `pad` - Simple copper pads

---

## Cases (3D Geometry)

Generates case files in STL, STEP, or DXF format.

**Key Parameters:**
- `extrude` - Height of case walls
- `fillet` - Round edges (radius in mm)
- `etch` - Add design details to case
- `cnc` - CNC cutting profiles

---

## File Formats

**Ergogen can export to:**
- `.kicad_pcb` - KiCad PCB editor format
- `.kicad_sch` - KiCad schematic format
- `.svg` - Vector graphics (outlines, cases)
- `.dxf` - CAD format (cutting/engraving)
- `.step` / `.stp` - 3D model format
- `.json` - Ergogen native format

**Convert to other formats using:**
- Inkscape (SVG → PDF, PNG, DXF)
- FreeCAD (STEP → STL)
- KiCad (PCB → Gerbers for manufacturing)

---

## Common Patterns

### Create a Grid of Keys
```yaml
points:
  key:
    ref: [0, 0]
    rows: 4
    cols: 6
    spread: u              # 19.05mm apart
```

### Mirror Keys (Split Keyboard)
```yaml
points:
  key:
    ref: [0, 0]
    rows: 4
    cols: 3
    spread: u
  
  key_mirror:
    ref: key
    shift: [20, 0]         # Offset right
    rotate: 180            # Flip horizontally
```

### Staggered Columns
```yaml
points:
  key:
    ref: [0, 0]
    rows: 4
    cols: 5
    spread: u
    row_offset: [0, u*0.5]  # Offset each row by half unit
```

### Thumb Cluster
```yaml
points:
  thumb:
    ref: key               # Reference main key grid
    shift: [-u*2, -u*4]    # Position below and left
    rows: 2
    cols: 3
    spread: u
```

---

## Preprocessing

Optional YAML processing before main config execution.

**Use for:**
- Conditionally include/exclude sections
- Generate repeated structures programmatically
- Define variables that can be reused

---

## Metadata Tags (Point Metadata)

Add custom data to points:

```yaml
points:
  key:
    ref: [0, 0]
    rows: 4
    cols: 6
    tags:                  # Custom metadata
      - socket             # Mark as hotswap socket
      - rgb                # Mark as RGB LED position
```

Use tags to:
- Filter which points get which footprints
- Identify special key positions
- Create custom component placement rules

---

## Tips for AI-Assisted Design

### ✓ DO:
- Specify exact measurements in units
- Use anchors to avoid repetitive calculations
- Reference existing points when possible
- Start with simple rectangular layouts, then add complexity
- Use consistent naming (e.g., `key_left`, `key_right`, `thumb`)
- Comment your YAML for clarity

### ✗ DON'T:
- Manually calculate coordinates (use anchors instead)
- Mix different units in same config
- Assume standard PCB dimensions without checking
- Skip footprint validation in KiCad
- Use hardcoded offsets for symmetry (use rotate + shift instead)

---

## Common Footprints

| Footprint | Purpose | Common Variants |
|---|---|---|
| `mx` | Keyboard switch | mx-1.0u, mx-2.0u, mx-stab |
| `diode` | Protection diode | sod-123, sod-323 |
| `smd` | Surface mount IC | qfp, bga, tsop |
| `pad` | Simple mounting pad | circle, square, obround |
| `alps` | Alps keyboard switch | alps-1.0u |

---

## QMK Integration

Once PCB is generated in KiCad:

1. **Export PCB dimensions** from KiCad
2. **Create QMK keyboard definition** for your MCU
3. **Define matrix layout** based on Ergogen point positions
4. **Map keycodes** to switch positions
5. **Test with Vial-QMK** for layout verification

---

## Debugging Checklist

| Issue | Likely Cause | Fix |
|---|---|---|
| Points don't align | Rotation or shift direction incorrect | Check coordinate system diagram above |
| Outlines too small/large | Wrong offset value | Adjust `offset` parameter |
| Footprints missing | Not referenced in PCB section | Add `ref` and `anchor` |
| Case geometry wrong | Extrude height or polygon incorrect | Verify `extrude` and `polygon` settings |
| KiCad import fails | Format incompatibility | Verify `.kicad_pcb` format, check for syntax errors |

---

## Key Resources

- **Coordinate System** - X right/left, Y up/down, rotation counter-clockwise
- **Anchors** - The secret to avoiding manual calculations
- **Points → Outlines → PCB** - The design pipeline
- **Footprints** - Control what gets placed where
- **Tags** - Add metadata for advanced filtering

---

## Example: Minimal Split Keyboard

```yaml
metadata:
  name: MinimalSplit

units:
  u: 19.05

points:
  key:
    ref: [0, 0]
    rows: 3
    cols: 3
    spread: u
  
  key_right:
    ref: key
    shift: [12u, 0]
    rotate: 180

outlines:
  left:
    ref: key
    offset: 5
    polygon: true
  
  right:
    ref: key_right
    offset: 5
    polygon: true

pcbs:
  main:
    outlines:
      main: left
    footprints:
      key:
        what: mx
        where: key
      diode:
        what: diode
        where: key
```

This creates a 3×3 split keyboard with switch and diode footprints ready for KiCad.
