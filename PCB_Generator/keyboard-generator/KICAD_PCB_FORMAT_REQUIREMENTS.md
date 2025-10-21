# KiCad PCB File Format Requirements

Based on official KiCad documentation: https://dev-docs.kicad.org/en/file-formats/sexpr-pcb/

## Required Sections for a Valid .kicad_pcb File

### 1. Header (REQUIRED)
```
(kicad_pcb
  (version 20221018)
  (generator "your_generator_name")
```

### 2. General Section (REQUIRED)
```
  (general
    (thickness 1.6)
  )
```

### 3. Layers Section (REQUIRED)
```
  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (32 "B.Adhes" user "B.Adhesive")
    ...
    (44 "Edge.Cuts" user)
    ...
  )
```

### 4. Setup Section (REQUIRED)
```
  (setup
    (pad_to_mask_clearance 0)
    (pcbplotparams ...)
  )
```

### 5. Nets Section (REQUIRED)
```
  (net 0 "")
  (net 1 "GND")
  (net 2 "VCC")
  ...
```

### 6. Footprints Section (REQUIRED for components)
Each footprint MUST include:
- Library link
- Layer
- Position (at x y rotation)
- Properties (Reference, Value, Sheetfile, Sheetname)
- **Graphics items** (fp_text, fp_line, fp_circle, fp_arc)
  - Reference text (fp_text reference)
  - Value text (fp_text value)
  - Silkscreen graphics (layer "F.SilkS")
  - Fab layer graphics (layer "F.Fab")
  - Courtyard (layer "F.CrtYd")
- **Pads** with complete definitions
- UUID (tstamp)

### 7. Graphic Items (for board outline)
```
  (gr_line (start x y) (end x y) (stroke ...) (layer "Edge.Cuts") (tstamp ...))
```

### 8. Tracks Section (for routing)
```
  (segment (start x y) (end x y) (width w) (layer "F.Cu") (net n) (tstamp ...))
  (via (at x y) (size s) (drill d) (layers "F.Cu" "B.Cu") (net n) (tstamp ...))
```

### 9. Zones Section (for ground planes)
```
  (zone (net n) (net_name "GND") (layer "B.Cu") ...)
```

## What Makes a Footprint COMPLETE

A footprint is NOT just pads! It requires:

### Minimum Required Elements:
1. **Library link**: `"Library:Footprint_Name"`
2. **Layer**: `(layer "F.Cu")`
3. **Position**: `(at x y rotation)`
4. **Properties**:
   - `(property "Reference" "R1" ...)`
   - `(property "Value" "10k" ...)`
   - `(property "Footprint" "..." ...)`
5. **Graphics** (THIS IS WHAT WE'RE MISSING):
   - `(fp_text reference ...)` - Reference designator
   - `(fp_text value ...)` - Component value
   - `(fp_line ...)` - Silkscreen outlines
   - `(fp_circle ...)` - Silkscreen circles
   - `(fp_arc ...)` - Silkscreen arcs
   - Fab layer graphics
   - Courtyard layer graphics
6. **Pads**: `(pad "1" thru_hole ...)`
7. **UUID**: `(tstamp ...)`

## Why Our Generated PCBs Don't Work

### Problem:
Our footprints only have:
- Basic properties
- Pads

### Missing:
- **ALL graphics** (silkscreen, fab, courtyard)
- Complete property definitions
- Proper library links
- Fab layer information
- Courtyard definitions

### Result:
KiCad shows only ratsnest (airwires) because footprints have no visual representation.

## Solution

### Option 1: Extract Complete Footprints from Library
- Parse library PCBs (dumbpad, lumberjack, etc.)
- Extract ENTIRE footprint definitions (including all graphics)
- Store as templates
- Reuse in generated PCBs

### Option 2: Use KiCad Footprint Libraries
- Reference standard KiCad footprint libraries
- Use footprint names like "Button_Switch_Keyboard:SW_Cherry_MX_PCB_1.00u"
- KiCad will load complete footprint definitions from its libraries
- This requires KiCad libraries to be installed

### Option 3: Generate Complete Footprints
- Create footprints with ALL required graphics
- Add silkscreen outlines
- Add fab layer graphics
- Add courtyard
- This is complex and error-prone

## Recommended Approach

**Extract complete footprints from library PCBs** (Option 1):

1. Parse `pcb-library/design-files/dumbpad/kicad/dumbpad.kicad_pcb`
2. Extract complete footprint definitions (all 62 footprints)
3. Store in a footprint library JSON file
4. When generating new PCBs, copy complete footprints
5. Update positions and net assignments
6. Add routing (traces, vias, zones)

This gives us real, working footprints with all graphics.

## File Size Comparison

- **Real PCB** (dumbpad): 46,802 lines
- **Our generated PCB**: ~500 lines
- **Difference**: We're missing 98% of the data!

Most of the missing data is:
- Complete footprint graphics (silkscreen, fab, courtyard)
- Detailed pad definitions
- Zone fill polygons
- Proper formatting and metadata

## Next Steps

1. Create footprint extractor that pulls complete footprints from library PCBs
2. Store extracted footprints as templates
3. Modify PCB generator to use complete footprints
4. Add routing from routing extraction system
5. Generate complete, manufacturable PCBs
