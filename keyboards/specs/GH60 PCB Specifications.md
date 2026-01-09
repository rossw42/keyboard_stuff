---
# GH60 / 60% PCB Specifications Reference
---

When working on 60% keyboard case designs, always reference the authoritative GH60 PCB specifications.

## Critical PCB Dimensions

### PCB Outline
- **Length:** 285.0mm (±0.2mm)
- **Width:** 94.6mm (±0.2mm)
- **Thickness:** 1.6mm (±0.1mm)
- **Corner Radius:** 2.0mm

### Case Opening Requirements
- **Opening Length:** 286.0mm (PCB + 1mm clearance)
- **Opening Width:** 95.6mm (PCB + 1mm clearance)
- **Clearance Per Side:** 0.5mm minimum
- **Tolerance:** ±0.2mm

### Mounting Holes (6 positions, from PCB top-left corner)
- **TL** (Top-Left): 19.0mm, 9.5mm
- **TR** (Top-Right): 266.0mm, 9.5mm
- **ML** (Middle-Left): 28.5mm, 47.3mm
- **MR** (Middle-Right): 256.5mm, 47.3mm
- **BL** (Bottom-Left): 57.0mm, 85.0mm
- **BR** (Bottom-Right): 228.0mm, 85.0mm
- **Hole Diameter:** 2.0-2.2mm (for M2 screws)
- **Positional Tolerance:** ±0.1mm (critical)

### USB Port
- **Center Position:** 142.5mm from PCB left edge (centered)
- **Distance from Top:** 7.0mm from PCB top edge
- **Recommended Cutout Width:** 16.0mm
- **Recommended Cutout Height:** 8-10mm

### Critical Clearances
- **Below PCB:** 5.0mm minimum (5.4mm+ recommended)
  - Accommodates switch pins (3.3mm), diodes, SMD components, solder joints
- **Above PCB:** 11.0mm minimum (12-15mm recommended)
  - Accommodates switches (5mm), keycaps (7.5mm), key travel (4mm)
- **Around Mounting Holes:** 3mm minimum, 5mm radius clear zone

## Design Validation Checklist

When designing or modifying case geometry, verify:

- [ ] PCB opening is 286mm × 95.6mm (±0.2mm)
- [ ] All 6 mounting holes at exact positions (±0.1mm tolerance)
- [ ] Standoffs: 6mm diameter, 2.2mm through-hole for M2 screws
- [ ] Brass inserts: M3 thread, 5.8mm hole, 4mm depth minimum
- [ ] USB cutout: 16mm wide, centered at 142.5mm from case left
- [ ] Clearance below PCB ≥5mm (measure from cavity floor to PCB bottom)
- [ ] Wall thickness ≥3mm (4mm recommended)
- [ ] Corner radii ≥2mm (match tool radius)

## Coordinate System

**Case Origin:** Top-left corner of case external profile

**PCB-to-Case Conversion:**
```
Case_X = PCB_X + PCB_BORDER
Case_Y = PCB_Y + PCB_BORDER
```

Where `PCB_BORDER` is the border width (typically 4.5-5mm)

**Example:** PCB mounting hole at (19.0, 9.5) with 4.5mm border:
```
Case_X = 19.0 + 4.5 = 23.5mm
Case_Y = 9.5 + 4.5 = 14.0mm
```

## Compatible PCBs

This specification applies to:
- GH60 (original, komar007 design)
- DZ60 (all variants)
- BM60 RGB
- HS60
- 1UP RGB HTE
- Instant60
- Most aftermarket 60% PCBs

**Always verify mounting hole positions** when using non-GH60 PCBs.

## Full Specification Document

For complete specifications, detailed drawings, and reference resources:

#[[file:docs/gh60_pcb_specifications.md]]

This includes:
- Detailed dimensional drawings
- Switch plate specifications
- Electrical specifications
- Manufacturing tolerances
- Common pitfalls and solutions
- Coordinate conversion formulas
- Design validation tables

## When to Reference

Reference these specifications when:
- Creating or modifying case geometry
- Positioning mounting holes or standoffs
- Designing USB cutouts
- Calculating clearances
- Validating PCB compatibility
- Troubleshooting fit issues
- Generating toolpaths for critical features

## Design Philosophy

**Tolerance Strategy:**
- **Critical features (±0.1mm):** PCB opening, mounting holes, standoff positions
- **Standard features (±0.2mm):** External dimensions, USB cutout, decorative features

**Clearance Strategy:**
- **Minimum:** Meets specification exactly (risky)
- **Recommended:** Adds 0.4mm safety margin (5.4mm vs 5.0mm below PCB)
- **Generous:** Adds 1-2mm for maximum compatibility

**Verification Strategy:**
1. Check dimensions against this specification
2. Run validation script (`examples/validate_design.py`)
3. Prototype critical features (3D print or test cut)
4. Test fit with actual PCB before final production
