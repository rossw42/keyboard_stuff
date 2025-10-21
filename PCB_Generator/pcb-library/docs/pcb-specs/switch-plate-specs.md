# Switch and Plate Specifications
## Universal Standards for Mechanical Keyboard Switches and Plates

**Document Version:** 1.0  
**Date:** 2025-10-17  
**Status:** ✅ Standard Reference

---

## Overview

This document provides universal specifications for mechanical keyboard switches and mounting plates. These standards apply to all form factors (60%, 65%, TKL, 40%, macropads) and are essential for ensuring compatibility between PCBs, plates, switches, and keycaps.

---

## 1. Cherry MX Switch Specifications

### 1.1 Physical Dimensions

| Feature | Specification | Tolerance | Notes |
|---------|--------------|-----------|-------|
| **Housing Size** | 15.6mm × 15.6mm | ±0.1mm | External dimensions |
| **Housing Height** | 11.6mm | - | From bottom to top |
| **Height Above PCB** | 5.0mm | - | PCB-mounted switch |
| **Height Above Plate** | 6.6mm | - | Plate-mounted switch |
| **Pin Spacing** | 5.08mm | - | Center-to-center |
| **Pin Diameter** | 1.5mm | - | Through-hole pins |
| **Pin Length** | 3.3mm | - | Below PCB (soldered) |

### 1.2 Switch Spacing (Keyboard Unit)

| Feature | Specification | Notes |
|---------|--------------|-------|
| **Standard Unit (1u)** | 19.05mm (0.75") | Center-to-center |
| **Horizontal Spacing** | 19.05mm | Between adjacent switches |
| **Vertical Spacing** | 19.05mm | Between rows |
| **Tolerance** | ±0.05mm | Critical for plate fit |

**Key Sizes:**
- 1u: 19.05mm spacing (letters, numbers)
- 1.25u: 23.81mm (Ctrl, Alt, Win)
- 1.5u: 28.58mm (Tab, some layouts)
- 1.75u: 33.34mm (Caps Lock, Right Shift)
- 2u: 38.10mm (Backspace, Enter, Shifts)
- 2.25u: 42.86mm (Left Shift, Enter)
- 2.75u: 52.39mm (Right Shift, some layouts)
- 6.25u: 119.06mm (Spacebar, standard)
- 7u: 133.35mm (Spacebar, alternative)


### 1.3 Switch Mounting Types

**PCB-Mounted (5-pin):**
- 2 electrical pins (switch contacts)
- 2 plastic stabilizer pins (2.54mm spacing)
- 1 center pin (LED, optional)
- Mounts directly to PCB
- More stable, no plate required

**Plate-Mounted (3-pin):**
- 2 electrical pins only
- No plastic stabilizer pins
- Requires plate for stability
- Compatible with PCB-mount holes (pins can be clipped)

### 1.4 Switch Pin Configuration

**Standard 2-Pin (Electrical):**
- Pin 1: Switch contact (left)
- Pin 2: Switch contact (right)
- Spacing: 5.08mm center-to-center
- Diameter: 1.5mm

**5-Pin (PCB-Mount):**
- Pin 1: Switch contact (left)
- Pin 2: Switch contact (right)
- Pin 3: Stabilizer pin (top-left)
- Pin 4: Stabilizer pin (top-right)
- Pin 5: LED pin (center, optional)

---

## 2. Plate Specifications

### 2.1 Plate Dimensions

**Plate Size:**
- Matches PCB outline dimensions
- Example (60%): 285mm × 94.6mm
- Tolerance: ±0.2mm

### 2.2 Plate Thickness

| Thickness | Usage | Notes |
|-----------|-------|-------|
| **1.2mm** | Minimum | Flexible, less stable |
| **1.5mm** | Standard | Most common, good balance |
| **1.6mm** | Standard | Also common, slightly stiffer |
| **2.0mm** | Thick | Very stiff, less flex |
| **3.0mm** | Maximum | Extremely stiff, may affect feel |

**Recommended:** 1.5mm (standard, widely compatible)

### 2.3 Plate Materials

| Material | Characteristics | Notes |
|----------|----------------|-------|
| **FR4** | Stiff, affordable, easy to manufacture | PCB material, laser-cut |
| **Aluminum** | Stiff, premium feel, good sound | CNC or laser-cut |
| **Brass** | Very stiff, heavy, premium sound | CNC or laser-cut |
| **Polycarbonate** | Flexible, softer feel, quiet | Laser-cut or CNC |
| **Carbon Fiber** | Stiff, lightweight, premium | Expensive, CNC |
| **Acrylic** | Flexible, affordable, clear options | Laser-cut |

### 2.4 Switch Cutout Specifications

**Standard Cherry MX Cutout:**
- Size: 14.0mm × 14.0mm
- Tolerance: ±0.05mm (tight fit for stability)
- Corner radius: 0.5mm (optional, for laser cutting)

**Cutout Positioning:**
- Center-to-center: 19.05mm (1u spacing)
- Alignment: Critical for switch fit
- Tolerance: ±0.05mm (affects switch alignment)

**Cutout Variations:**
- **Tight fit:** 14.0mm × 14.0mm (most stable)
- **Loose fit:** 14.1mm × 14.1mm (easier assembly)
- **Very loose:** 14.2mm × 14.2mm (may rattle)

---

## 3. Stabilizer Specifications

### 3.1 Cherry-Style Stabilizers

**Types:**
- **PCB-Mount:** Snap into PCB holes
- **Plate-Mount:** Clip into plate cutouts
- **Screw-In:** Screw into PCB (most stable)

### 3.2 Stabilizer Sizes

| Key Size | Stabilizer Size | Wire Length | Usage |
|----------|----------------|-------------|-------|
| **2u** | 2u | ~12mm | Backspace, Enter, Shifts |
| **2.25u** | 2u | ~12mm | Enter, Left Shift |
| **2.75u** | 2u | ~12mm | Right Shift |
| **6.25u** | 6.25u | ~100mm | Spacebar (standard) |
| **7u** | 7u | ~115mm | Spacebar (alternative) |

### 3.3 Stabilizer Cutout Specifications

**PCB-Mount Stabilizer Holes:**
- Cutout size: 6.65mm × 13.5mm (per side)
- Position: Varies by key size
- Spacing from switch center:
  - 2u: ±11.95mm
  - 6.25u: ±50mm
  - 7u: ±57.15mm

**Plate-Mount Stabilizer Cutouts:**
- Cutout size: 6.65mm × 13.5mm (per side)
- Position: Same as PCB-mount
- Clips into plate instead of PCB

**Screw-In Stabilizer Holes:**
- Screw holes: 2.0mm diameter (M2 screws)
- Position: At stabilizer cutout corners
- Requires PCB support for screws

---

## 4. Keycap Specifications

### 4.1 Keycap Profiles

**Common Profiles:**

| Profile | Height | Sculpt | Notes |
|---------|--------|--------|-------|
| **Cherry** | Low | Yes | Most common, comfortable |
| **OEM** | Medium | Yes | Standard on pre-builts |
| **DSA** | Low | No | Uniform height, popular for 40% |
| **XDA** | Medium | No | Uniform height, larger top |
| **SA** | High | Yes | Tall, retro aesthetic |
| **MT3** | High | Yes | Deep dish, ergonomic |

### 4.2 Keycap Dimensions

**Standard 1u Keycap:**
- Top surface: ~13mm × 13mm (varies by profile)
- Base: ~18mm × 18mm (fits 19.05mm spacing)
- Height: 7.5-12mm (varies by profile and row)

**Clearance Requirements:**
- Switch to keycap: 0mm (keycap sits on switch)
- Keycap to case: 2mm minimum (for key travel)
- Keycap to keycap: 1mm minimum (between adjacent keys)

### 4.3 Keycap Compatibility

**Standard Layouts:**
- ANSI: Most common in North America
- ISO: Common in Europe (different Enter key)
- JIS: Common in Japan

**Non-Standard Keys:**
- 1.75u Right Shift (65%, 75% layouts)
- 1u modifiers (40% layouts)
- Split spacebar (40% layouts)
- Stepped Caps Lock (some layouts)

---

## 5. PCB Design Specifications

### 5.1 Switch Footprint

**Standard Cherry MX Footprint:**
- 2 electrical holes: 1.5mm diameter
- Spacing: 5.08mm center-to-center
- Pad size: 2.0mm diameter (for soldering)

**5-Pin PCB-Mount Footprint:**
- 2 electrical holes: 1.5mm diameter
- 2 stabilizer holes: 1.7mm diameter
- 1 LED hole: 1.0mm diameter (optional)
- Stabilizer hole spacing: 2.54mm from center

### 5.2 Diode Placement

**Per-Switch Diode:**
- Position: Near switch footprint
- Orientation: Consistent across PCB (COL2ROW or ROW2COL)
- Footprint: DO-35 (through-hole) or SOD-123 (SMD)

**Through-Hole Diode (DO-35):**
- Hole diameter: 0.8mm
- Pad size: 1.5mm diameter
- Spacing: 7.62mm (standard) or 10.16mm

### 5.3 Plate Mounting

**Plate-Mount Design:**
- Plate sits between switches and PCB
- Switches clip into plate
- Plate provides stability
- PCB mounts to case via standoffs

**Plateless Design:**
- Switches mount directly to PCB
- Requires 5-pin switches for stability
- More flexible typing feel
- Simpler assembly

---

## 6. Manufacturing Specifications

### 6.1 Plate Manufacturing

**Laser Cutting:**
- Minimum kerf: 0.1mm
- Corner radius: 0.5mm (beam width)
- Materials: FR4, acrylic, polycarbonate
- Tolerance: ±0.1mm

**CNC Machining:**
- Minimum tool diameter: 2mm (1mm radius)
- Corner radius: Matches tool radius
- Materials: Aluminum, brass, carbon fiber
- Tolerance: ±0.05mm

**Waterjet Cutting:**
- No corner radius (sharp corners possible)
- Materials: Aluminum, brass, steel
- Tolerance: ±0.1mm

### 6.2 PCB Manufacturing

**Switch Holes:**
- Plated through-holes
- Diameter: 1.5mm (electrical), 1.7mm (stabilizer)
- Pad size: 2.0mm diameter
- Tolerance: ±0.05mm

**Plate Mounting Holes:**
- Diameter: 2.0-2.2mm (M2 screws)
- Plated or non-plated
- Tolerance: ±0.1mm

---

## 7. Assembly Specifications

### 7.1 Switch Installation

**Plate-Mount Assembly:**
1. Insert switches into plate
2. Align switch pins with PCB holes
3. Press switches into PCB
4. Solder switch pins

**PCB-Mount Assembly:**
1. Insert switches directly into PCB
2. Ensure stabilizer pins align
3. Press switches firmly
4. Solder switch pins

### 7.2 Stabilizer Installation

**PCB-Mount Stabilizers:**
1. Insert stabilizer housing into PCB holes
2. Snap into place (should click)
3. Install stabilizer wire
4. Test stabilizer movement

**Plate-Mount Stabilizers:**
1. Clip stabilizers into plate cutouts
2. Install stabilizer wire
3. Install plate with stabilizers
4. Test stabilizer movement

**Screw-In Stabilizers:**
1. Insert stabilizer housing into PCB holes
2. Screw into PCB from bottom
3. Install stabilizer wire
4. Test stabilizer movement (most stable)

---

## 8. Testing and Validation

### 8.1 Plate Fit Test

**Verify:**
- [ ] Switches fit snugly in plate cutouts
- [ ] No excessive play or rattling
- [ ] Switches align with PCB holes
- [ ] Plate sits flat on switches

### 8.2 Switch Alignment Test

**Verify:**
- [ ] All switches aligned in rows
- [ ] No tilted or crooked switches
- [ ] Switch pins align with PCB holes
- [ ] Switches press smoothly

### 8.3 Stabilizer Test

**Verify:**
- [ ] Stabilizers move smoothly
- [ ] No binding or sticking
- [ ] Wire doesn't pop out
- [ ] Keycaps sit level

---

## 9. Common Issues and Solutions

### 9.1 Switch Doesn't Fit Plate

**Cause:** Plate cutout too small or too large
**Solution:** Verify cutout is 14.0mm × 14.0mm (±0.05mm)

### 9.2 Switch Pins Don't Align with PCB

**Cause:** Plate misaligned or switch spacing incorrect
**Solution:** Verify switch spacing is 19.05mm, check plate alignment

### 9.3 Stabilizer Rattles

**Cause:** Loose fit or poor lubrication
**Solution:** Lube stabilizer, use band-aid mod, or upgrade to screw-in

### 9.4 Keycap Hits Case

**Cause:** Insufficient top clearance
**Solution:** Increase case height or use lower-profile keycaps

---

## 10. Design Checklist

### Plate Design
- [ ] Plate dimensions match PCB
- [ ] Plate thickness: 1.5mm (standard)
- [ ] Switch cutouts: 14.0mm × 14.0mm
- [ ] Switch spacing: 19.05mm (1u)
- [ ] Stabilizer cutouts positioned correctly
- [ ] Mounting holes aligned with PCB

### PCB Design
- [ ] Switch footprints: 1.5mm holes, 5.08mm spacing
- [ ] 5-pin support (if PCB-mount)
- [ ] Diodes positioned near switches
- [ ] Stabilizer holes positioned correctly
- [ ] Plate mounting holes (if plate-mount)

### Assembly
- [ ] Switches fit plate cutouts
- [ ] Switch pins align with PCB holes
- [ ] Stabilizers installed correctly
- [ ] Stabilizers move smoothly
- [ ] Keycaps fit without interference

---

## 11. Reference Resources

**Standards:**
- Cherry MX datasheet (switch dimensions)
- Keyboard Layout Editor (layout planning)
- ai03 Plate Generator (automated plate generation)
- Swillkb Plate Builder (alternative plate generator)

**Component Sources:**
- Cherry MX switches: Novelkeys, KBDfans, Divinikey
- Stabilizers: Durock, C3, TX, Zeal
- Keycaps: GMK, ePBT, Drop, KBDfans

---

**Document Status:** ✅ Complete  
**Last Updated:** 2025-10-17  
**Maintained By:** Through-Hole Keyboard Library

---

## Appendix: Switch Cutout Diagram

```
┌─────────────────────┐
│                     │
│   14.0mm × 14.0mm   │  ← Plate cutout
│                     │
│    ┌─────────┐      │
│    │         │      │
│    │ Switch  │      │  ← Switch housing (15.6mm × 15.6mm)
│    │         │      │
│    └─────────┘      │
│                     │
└─────────────────────┘

Switch spacing: 19.05mm (1u) center-to-center
```

## Appendix: Stabilizer Positioning

```
2u Key (Backspace, Enter, Shifts):
┌─────────────────────────────────┐
│                                 │
│  ●                         ●    │  ← Stabilizer positions
│              ●                  │  ← Switch center
│                                 │
└─────────────────────────────────┘
   ±11.95mm from switch center

6.25u Spacebar:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ●                                                 ●    │  ← Stabilizer positions
│                          ●                              │  ← Switch center
│                                                         │
└─────────────────────────────────────────────────────────┘
   ±50mm from switch center
```

---

**End of Document**
