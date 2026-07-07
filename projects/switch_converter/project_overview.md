# PG1350 to PG1425 Switch Adapter - Project Overview

## What This Project Is About

This project aims to create a **3D-printed adapter that allows PG1350 switches to work with PG1425 PCB footprints**. 

### The Core Challenge

- **PG1350 switches** have a 13.8 × 13.8 mm body with flat stamped contacts
- **PG1425 PCB footprint** is only about 10.2 × 10.2 mm (internal opening)
- The switch bodies don't match, so we need an intermediary solution

---

## Key Technical Insights

### Size Comparison

| Feature | PG1350 | PG1425 | Difference |
|---------|---------|--------|------------|
| Body size | 13.8 × 13.8 mm | ~10.2 × 10.2 mm | ~1.8 mm per side |
| PCB footprint | 5.90 × 11.00 mm | 5.50 × 5.50 mm | ~0.4mm width, ~5.5mm height |
| Pin spacing (X) | 3.80mm | 2.90mm | 0.90mm offset |
| Pin spacing (Y) | 5.00mm | 5.50mm | 0.50mm offset |
| Top hole diameter | φ1.90mm | φ1.30mm | -0.60mm |
| Bottom hole diameter | φ1.20mm | φ1.10mm | -0.10mm |
| Contact style | Flat stamped | Flat stamped | Compatible! |

**Good news:** The contact styles are already compatible - both use flat blade contacts instead of round pins. This means we can design spring contacts that wipe against the flat blade for reliable electrical connection.

---

## Design Approach: 3D Printed Adapter with Spring Contacts

### Architecture

```
┌─────────────────────────┐
│   PG1350 Switch         │
│   (sits on top)         │
├─────────────────────────┤
│   3D Printed Shell      │
│   ┌───────────────────┐ │
│   │ Spring Contacts   │ │ ← Touch PG1350 pins, extend to PCB holes
│   │ (or hot-swap)     │ │
│   └───────────────────┘ │
├─────────────────────────┤
│   PG1425 PCB            │
│   (fits under adapter)  │
└─────────────────────────┘
```

### Design Options

#### Option A: Press-Fit Spring Plates (Recommended for Simplicity)

**Concept:** 
- 3D printed spring-loaded plates that press-fit into the PCB holes
- Top surface contacts PG1350 pins when switch is inserted
- Springs provide consistent contact pressure

**Advantages:**
- No soldering required
- Easy to assemble/disassemble
- Replaceable springs if they wear out
- Simple 3D printing (no complex metal parts)

**Design Considerations:**
- Spring material: TPU or flexible filament, or printed-in-place flexure
- Contact pressure: Need ~10-20gf per contact for reliable connection
- Hole tolerance: PCB holes are φ1.30mm top / φ1.10mm bottom
- Spring plate outer diameter: ~1.45mm to fit snugly in hole

#### Option B: Hot-Swap Socket Contacts (Salvaged)

**Concept:**
- Extract contacts from existing PG1350 hot-swap sockets
- 3D print retention features to hold contacts in place
- Contacts press-fit into PCB holes and contact switch pins

**Advantages:**
- Uses off-the-shelf components
- Proven reliability (hot-swap contacts are designed for this)
- Easy to source replacement contacts

**Design Considerations:**
- Need to extract contacts from sockets without damaging them
- 3D print needs to hold contacts securely but allow removal
- Contact orientation must match PG1350 pin layout

---

## Detailed Design Requirements

### Mechanical Interface (PG1350 Side)

The adapter top surface must:
1. **Accommodate PG1350 body**: 13.8 × 13.8 mm internal opening minimum
2. **Contact switch pins**: Top holes φ1.90mm, bottom holes φ1.20mm
3. **Provide retention**: Keep switch seated properly
4. **Allow easy insertion/removal**: No excessive friction

**Top Shell Dimensions:**
- External: ~15 × 15 mm (to match PG1350 top shell)
- Internal opening: ≥13.8 × 13.8 mm
- Pin contact area: Centered on each pin location

### Electrical Interface (PG1425 Side)

The adapter bottom must interface with PG1425 PCB:
1. **PCB footprint**: 5.50 × 5.50 mm overall, 10.2 × 10.2 mm internal opening
2. **Pin locations**: 
   - X spacing: 2.90mm (vs PG1350's 3.80mm)
   - Y spacing: 5.50mm (vs PG1350's 5.00mm)
3. **Hole sizes**: Top φ1.30mm, bottom φ1.10mm

**Critical:** The adapter must bridge the gap between PG1350 pin positions and PG1425 PCB pad positions while maintaining electrical continuity.

### Spring Contact Design Parameters

For press-fit spring plates:
- **Spring constant**: ~5-10 N/mm for reliable contact
- **Contact pressure**: 10-20 gf per contact point
- **Plate thickness**: 1.5-2.0 mm (printed in single or dual extrusion)
- **Hole fit tolerance**: +0.15mm to +0.20mm over PCB hole size

### Material Recommendations

| Component | Recommended Material | Reason |
|-----------|---------------------|--------|
| Main shell | PLA/PETG/ABS | Structural strength, easy printing |
| Spring plates | TPU 95A or printed flexure | Flexibility for spring action |
| Contact retention | ABS/PLA | Rigid hold for contacts |

---

## Implementation Plan

### Phase 1: CAD Design (OpenSCAD/Fusion 360)

1. **Model PG1350 switch** using specifications from `PG1350_Switch_Specs.md`
2. **Model PG1425 PCB footprint** using specifications from `PG1425_Switch_Specs.md`
3. **Design adapter shell**:
   - Top: Matches PG1350 dimensions (15 × 15 mm external)
   - Bottom: Matches PG1425 PCB footprint (5.5 × 5.5 mm)
   - Side walls: Bridge the gap between switch and PCB
4. **Design spring contact mechanism**:
   - Press-fit plates OR hot-swap socket retention features
   - Calculate spring force requirements
   - Design flexure geometry if using printed springs

### Phase 2: Prototyping

1. **Print adapter components** (test prints with PLA first)
2. **Prepare spring contacts**:
   - For Option A: Print flexible spring plates or use TPU filament
   - For Option B: Extract contacts from existing hot-swap sockets
3. **Assemble prototype**
4. **Test electrical continuity** between PG1350 pins and PCB pads
5. **Verify mechanical fit** with actual PG1425 PCB

### Phase 3: Iteration

1. **Refine spring force** if contacts are too loose or too tight
2. **Adjust hole tolerances** for better fit
3. **Test with multiple switches** to verify consistency
4. **Document final design** with CAD files and assembly instructions

---

## Testing Guidelines

### Before Assembly

1. Verify PG1350 switch specifications match design assumptions
2. Confirm PG1425 footprint dimensions from official documentation
3. Check hot-swap contact compatibility (if using Option B)

### After Assembly

1. Test electrical continuity between all pins (multimeter check)
2. Verify mechanical fit with PG1425 PCB
3. Test switch actuation feel and consistency
4. Check for any short circuits or loose connections
5. Measure contact resistance under various forces

---

## Critical Constraints

### NEVER Write To

- **D:\GitHub2\vial-qmk** - This is a read-only repository (upstream vial-qmk)
- Only write to local working directories for prototyping and testing

### ALWAYS Backup

- Any modified CAD designs before committing
- Any 3D printed parts before final assembly
- Test results and measurements for reproducibility

---

## Project Goals

- Create an open-source, reproducible solution
- Enable PG1350 switches to work in PG1425-based keyboards
- Establish a simpler architecture without interposer PCB complexity
- Document everything for community contribution

---

## Summary

This is a hardware engineering project to create a 3D-printed adapter that bridges two incompatible switch footprints. The solution uses:
- **3D printing** for the mechanical shell and/or spring contacts
- **Either press-fit spring plates** or **salvaged hot-swap socket contacts** as the electrical interface

The end result is a simpler, serviceable, and open-source adapter that can be replicated by anyone with access to a 3D printer and basic electronics tools. No custom metal forming or PCB design required.

---

## Files in This Project

| File | Purpose |
|------|---------|
| `PG1350_Switch_Specs.md` | PG1350 switch detailed specifications |
| `PG1425_Switch_Specs.md` | PG1425 PCB footprint detailed specifications |
| `project_overview.md` | This document - project summary and design approach |

---

*Document generated from Kaihua Electronics datasheets*