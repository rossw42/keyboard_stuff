# Through-Hole Keyboard Clearance Requirements
## Universal Clearance Standards for All Form Factors

**Document Version:** 1.0  
**Date:** 2025-10-17  
**Status:** ✅ Standard Reference

---

## Overview

This document provides universal clearance requirements for through-hole keyboard PCB designs. Proper clearances ensure compatibility with switches, keycaps, components, and cases across all form factors (60%, 65%, TKL, 40%, macropads).

---

## 1. Vertical Clearances

### 1.1 Clearance Below PCB (Bottom Surface)

**Minimum Required:** 5.0mm from PCB bottom surface to case floor

**Component Heights Below PCB:**
- Switch pins (soldered): 3.3mm protrusion
- Through-hole diodes (DO-35, laid flat): 1.5-2.0mm
- Through-hole resistors (1/4W, laid flat): 1.5-2.0mm
- Through-hole capacitors (radial): 2.0-3.0mm
- Solder joints: 0.5-1.0mm
- Pro Micro (if bottom-mounted): 3.0-4.0mm

**Recommended Clearances:**
- **Standard designs:** 5.4mm (adds 0.4mm safety margin)
- **With Pro Micro:** 6.0mm minimum
- **With DIP-40 MCU:** 6.0mm minimum (socket adds height)
- **Generous clearance:** 7.0mm (maximum compatibility)

**Critical:** Measure actual component heights before finalizing case design. Component variations exist between manufacturers.

### 1.2 Clearance Above PCB (Top Surface)

**Minimum Required:** 11.0mm from PCB top surface to case top

**Component Heights Above PCB:**
- Cherry MX switch housing: 5.0mm (from PCB to top of switch)
- Keycap base (Cherry profile): 7.5mm (from switch top to keycap bottom)
- Key travel: 4.0mm (full depression)
- Total minimum: 11.0mm

**Recommended Clearances by Keycap Profile:**

| Profile | Height Above PCB | Total Clearance Needed |
|---------|-----------------|----------------------|
| **Cherry** | 7.5mm | 11.0mm minimum |
| **OEM** | 8.0mm | 12.0mm minimum |
| **DSA** | 7.5mm | 11.0mm minimum |
| **XDA** | 8.5mm | 12.5mm minimum |
| **SA** | 11.0mm | 15.0mm minimum |
| **MT3** | 12.0mm | 16.0mm minimum |

**For Exposed Component Designs:**
- Minimum: 15-20mm clearance
- Accommodates visible MCU, diodes, resistors on top surface
- Popular aesthetic for 40% keyboards and macropads

---

## 2. Horizontal Clearances

### 2.1 PCB Edge Clearances

**Minimum from PCB Edge:**
- Case features: 2.0mm minimum
- Mounting holes: 5.0mm minimum (from PCB edge to hole center)
- Components: 1.0mm minimum (for manufacturability)

**Recommended:**
- Case features: 3.0mm (safer for machining tolerances)
- Critical features: 5.0mm (USB cutouts, mounting holes)

### 2.2 PCB Opening in Case

**Standard Clearance:**
- PCB length + 1.0mm (0.5mm per side)
- PCB width + 1.0mm (0.5mm per side)

**Example (GH60 - 285mm × 94.6mm PCB):**
- Case opening: 286mm × 95.6mm
- Clearance: 0.5mm per side

**Tolerance:**
- Opening tolerance: ±0.2mm
- Allows easy PCB insertion/removal
- Prevents rattling

---

## 3. Component-Specific Clearances

### 3.1 Mounting Hole Clearances

**Around Each Mounting Hole:**
- Minimum clear zone: 3mm radius (6mm diameter)
- Recommended clear zone: 5mm radius (10mm diameter)
- No components within clear zone
- No case features within clear zone

**Standoff Specifications:**
- Standoff diameter: 6.0mm (for M2 screw)
- Standoff height: Matches bottom clearance (5-7mm)
- Through-hole: 2.2mm (M2 clearance)

### 3.2 USB Connector Clearances

**USB Cutout Area:**
- Width: 16-18mm (connector + cable strain relief)
- Height: 8-10mm (through case thickness)
- Clear zone: 20mm × 15mm (no case features)

**Connector Protrusion:**
- USB-C through-hole: ~3-4mm above PCB
- USB Mini-B: ~3-4mm above PCB
- Pro Micro: ~3-4mm above PCB (USB connector on module)

**Cable Clearance:**
- Consider cable bend radius
- Some cables have bulky strain relief (test fit)
- Angled cables may require different cutout

### 3.3 MCU Clearances

**DIP Package MCUs:**

| MCU | Package | Footprint | Clear Zone |
|-----|---------|-----------|-----------|
| **ATmega328P** | DIP-28 | 35mm × 15mm | 40mm × 20mm |
| **ATmega32A** | DIP-40 | 50mm × 15mm | 55mm × 20mm |

**Pro Micro Footprint:**
- Footprint: 18mm × 33mm
- Clear zone: 20mm × 35mm
- Height: 3-4mm (if bottom-mounted)

**Clearance Considerations:**
- No case features within clear zone
- Allow access for programming (if ISP header)
- Consider heat dissipation (ventilation)

### 3.4 Switch Matrix Clearances

**Switch Spacing:**
- Standard: 19.05mm (0.75") center-to-center
- Minimum: 19.00mm (tight fit)
- Tolerance: ±0.05mm (critical for plate fit)

**Switch Footprint:**
- Switch housing: 15.6mm × 15.6mm
- Plate cutout: 14.0mm × 14.0mm
- Clearance: 0.8mm per side

**Keep-Out Zone:**
- Entire switch matrix area on top surface
- No case features interfering with switches
- No components interfering with switch pins

### 3.5 Stabilizer Clearances

**Cherry-Style Stabilizer Cutouts:**
- Cutout size: 6.65mm × 13.5mm
- Position: Varies by key size (2u, 6.25u, 7u)
- Clearance below PCB: 3.0mm (stabilizer wire)

**Plate-Mounted Stabilizers:**
- Require plate cutouts
- No PCB clearance needed (except for wire)

**PCB-Mounted Stabilizers:**
- Require PCB holes
- Clearance below PCB: 3.0mm minimum

### 3.6 Optional Component Clearances

**Rotary Encoder (EC11):**
- Footprint: 13mm × 13mm
- Height above PCB: 15mm (with knob)
- Clear zone: 15mm × 15mm × 20mm (height)

**OLED Display (0.91"-0.96"):**
- Footprint: 27mm × 27mm (typical)
- Height above PCB: 10mm (typical)
- Clear zone: 30mm × 30mm × 12mm (height)
- Viewing angle: Consider case window position

**RGB LEDs (WS2812B):**
- Footprint: 5mm × 5mm (per LED)
- Height: 1.6mm (SMD) or 8mm (through-hole)
- Light diffusion: Consider case material/design

---

## 4. Case Design Clearances

### 4.1 Wall Thickness

**Minimum Wall Thickness:**
- 3.0mm (absolute minimum for structural integrity)
- 4.0mm (recommended for most designs)
- 5.0mm (for larger keyboards like TKL)

**Considerations:**
- Thicker walls = more rigidity
- Thinner walls = lighter weight
- Material affects required thickness (wood vs. acrylic vs. aluminum)

### 4.2 Internal Features

**Standoff Clearances:**
- Standoff to PCB edge: 5mm minimum
- Standoff to standoff: 10mm minimum (avoid interference)
- Standoff to case wall: 3mm minimum

**Brass Insert Clearances:**
- Insert diameter: 5.7mm (M3 press-fit)
- Hole diameter: 5.8mm (tight fit)
- Depth: 4mm minimum (for M3 thread engagement)
- Clear zone: 8mm diameter (no interference)

### 4.3 Assembly Clearances

**Screw Access:**
- Screwdriver clearance: 10mm diameter minimum
- Depth: Case height + 5mm (for tool access)

**Cable Routing:**
- Internal cable routing: 5mm × 5mm channel minimum
- USB cable exit: 20mm × 10mm minimum

---

## 5. Manufacturing Tolerances

### 5.1 Critical Tolerances (±0.1mm)

Apply to features requiring precise fit:
- PCB opening dimensions
- Mounting hole positions
- Standoff positions
- Brass insert hole positions

### 5.2 Standard Tolerances (±0.2mm)

Apply to non-critical features:
- External case dimensions
- USB cutout position
- Rubber feet positions
- Decorative features

### 5.3 Machining Considerations

**Corner Radii:**
- Minimum: 2mm (limited by endmill diameter)
- Recommended: 3mm (safer for machining)
- Internal corners: Match tool radius (4mm endmill = 2mm radius)

**Pocket Depth:**
- Maximum per pass: 2-2.5mm (for hardwood)
- Total depth: As required by design
- Consider tool deflection for deep pockets

---

## 6. Verification Checklist

Use this checklist to verify clearances in your design:

### Vertical Clearances
- [ ] 5mm+ clearance below PCB (measure tallest component)
- [ ] 11mm+ clearance above PCB (or more for SA/MT3 keycaps)
- [ ] Adequate clearance for Pro Micro (if used)
- [ ] Adequate clearance for DIP MCU (if used)

### Horizontal Clearances
- [ ] PCB opening = PCB size + 1mm (0.5mm per side)
- [ ] 2mm+ from PCB edge to case features
- [ ] 5mm+ from PCB edge to mounting holes

### Component Clearances
- [ ] 5mm radius clear zone around mounting holes
- [ ] 20mm × 15mm clear zone for USB connector
- [ ] MCU clear zone (no case features)
- [ ] Switch matrix clear zone (entire top surface)
- [ ] Stabilizer clearances (3mm below PCB)

### Optional Component Clearances
- [ ] Rotary encoder clear zone (if used)
- [ ] OLED display clear zone (if used)
- [ ] RGB LED clearances (if used)

### Case Design
- [ ] Wall thickness ≥3mm (4mm recommended)
- [ ] Standoff clearances adequate
- [ ] Brass insert clearances adequate
- [ ] Screw access clearances adequate

### Manufacturing
- [ ] Corner radii ≥2mm (match tool radius)
- [ ] Critical features: ±0.1mm tolerance
- [ ] Standard features: ±0.2mm tolerance

---

## 7. Common Clearance Issues

### 7.1 Insufficient Bottom Clearance

**Symptoms:**
- Switch pins hit case floor
- Diodes hit case floor
- PCB doesn't sit flat

**Solutions:**
- Increase standoff height
- Recess case floor
- Use shorter component leads

### 7.2 Insufficient Top Clearance

**Symptoms:**
- Keycaps hit case top
- Keys don't travel fully
- Keycaps rub on case

**Solutions:**
- Increase case height
- Use lower-profile keycaps
- Adjust case top frame thickness

### 7.3 PCB Doesn't Fit Opening

**Symptoms:**
- PCB too tight in case
- PCB rattles in case
- PCB corners catch on case

**Solutions:**
- Adjust opening size (±0.5mm per side)
- Check PCB dimensions
- Verify corner radii match

### 7.4 Mounting Holes Misaligned

**Symptoms:**
- Screws don't align with standoffs
- PCB doesn't sit flat
- Forced assembly damages PCB

**Solutions:**
- Verify mounting hole positions (±0.1mm)
- Check standoff positions
- Use alignment jig for assembly

---

## 8. Design Tips

### 8.1 Measure Actual Components

- Don't rely solely on datasheets
- Measure actual component heights
- Account for solder joint height
- Consider component variations between manufacturers

### 8.2 Add Safety Margins

- Add 0.4mm to minimum clearances
- Use 5.4mm instead of 5.0mm below PCB
- Use 12mm instead of 11mm above PCB
- Better safe than sorry

### 8.3 Prototype Before Production

- 3D print case prototype
- Test fit with actual PCB and components
- Verify all clearances
- Test assembly process
- Adjust design based on prototype

### 8.4 Document Clearances

- Create clearance diagrams
- Document critical dimensions
- Include in build guide
- Help future designers

---

**Document Status:** ✅ Complete  
**Last Updated:** 2025-10-17  
**Maintained By:** Through-Hole Keyboard Library

---

## Appendix: Clearance Diagrams

### Vertical Clearance (Side View)

```
┌─────────────────────────────────────┐
│         Case Top Frame              │ ← Top surface
├─────────────────────────────────────┤
│                                     │
│         11mm+ clearance             │ ← Keycap + switch + travel
│                                     │
├═════════════════════════════════════┤ ← PCB top surface
│         PCB (1.6mm)                 │
├═════════════════════════════════════┤ ← PCB bottom surface
│                                     │
│         5mm+ clearance              │ ← Components + solder
│                                     │
├─────────────────────────────────────┤
│         Case Bottom Tray            │ ← Bottom surface
└─────────────────────────────────────┘
```

### Horizontal Clearance (Top View)

```
┌─────────────────────────────────────┐
│  Case Wall (4mm thick)              │
│  ┌───────────────────────────────┐  │
│  │ 0.5mm clearance               │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │                         │  │  │
│  │  │      PCB                │  │  │
│  │  │                         │  │  │
│  │  └─────────────────────────┘  │  │
│  │ 0.5mm clearance               │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

---

**End of Document**
