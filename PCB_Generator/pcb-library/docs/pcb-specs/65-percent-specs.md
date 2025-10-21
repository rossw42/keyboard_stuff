# 65% Through-Hole Keyboard PCB Specifications
## Reference Standard for 65% Form Factor

**Document Version:** 1.0  
**Date:** 2025-10-17  
**Primary Reference:** Discipline V2 (coseyfannitutti)  
**Status:** ✅ Documented from Community Designs

---

## Overview

This document provides reference specifications for 65% through-hole keyboard PCBs. The 65% form factor includes dedicated arrow keys and a partial navigation cluster, typically resulting in 68-70 keys. This specification is based primarily on the Discipline V2 design, which has become a popular reference for through-hole 65% keyboards.

### Compatible Designs

- **Discipline V2** (coseyfannitutti) - Primary reference
- Custom 65% through-hole designs following similar layout

---

## 1. PCB Outline Dimensions

### 1.1 Overall Dimensions

| Dimension | Specification | Tolerance | Notes |
|-----------|--------------|-----------|-------|
| **Length (X-axis)** | ~310-320mm | ±0.5mm | Varies by design |
| **Width (Y-axis)** | ~95-100mm | ±0.5mm | Similar to 60% |
| **Thickness** | 1.6mm | ±0.1mm | Standard PCB thickness |
| **Corner Radius** | 2.0-3.0mm | - | Rounded corners |
| **Layers** | 2 | - | Standard double-sided |

**Note:** Unlike 60% keyboards, 65% boards do not have a universal mounting standard. Each design may have unique mounting hole positions.

### 1.2 Layout Characteristics

**Standard 65% Layout:**
- **Alphanumeric cluster:** 60% standard (14.25u width)
- **Right column:** 4 keys (typically Del, PgUp, PgDn, End)
- **Arrow cluster:** 4 keys in inverted-T arrangement
- **Total keys:** 68 keys (standard) to 70 keys (with split shifts)
- **Bottom row:** 6.25u or 7u spacebar options

---

## 2. Mounting Specifications

### 2.1 Mounting System

**Important:** 65% keyboards typically use **integrated plate mounting** or **tray mount** systems. Mounting hole positions vary by design.

**Discipline V2 Mounting:**
- Uses acrylic case with standoffs
- Mounting holes positioned for structural support
- Typically 6-8 mounting points

### 2.2 Recommended Mounting Approach

| Feature | Specification | Notes |
|---------|--------------|-------|
| **Mounting Style** | Tray mount or integrated plate | Design-dependent |
| **Hole Diameter** | 2.0-2.2mm | For M2 screws |
| **Standoff Height** | 5-8mm | Depends on case design |
| **Positional Tolerance** | ±0.2mm | Less critical than 60% |

**Design Tip:** When creating a 65% design, position mounting holes to avoid switch positions and provide balanced support across the PCB.

---

## 3. USB Port Specifications

### 3.1 USB Connector Position

| Feature | Specification | Notes |
|---------|--------------|-------|
| **Connector Type** | USB-C (through-hole preferred) | Modern standard |
| **Position** | Top edge, typically centered | Varies by design |
| **Distance from Edge** | 5-10mm | From PCB top edge |
| **Connector Width** | ~8-10mm | Actual connector footprint |

### 3.2 Through-Hole USB-C Implementation

**Discipline V2 Style (Recommended):**

**Components:**
- USB-C connector (12-pin through-hole, e.g., GCT USB4085)
- 2× 5.1kΩ resistors (CC pull-down for USB-C)
- 2× 3.6V Zener diodes (ESD protection)
- 1× 1.5kΩ resistor (D- pull-up for USB 2.0)
- 1× 75Ω resistor (series termination)
- 2× 22pF capacitors (crystal load caps)
- 1× 0.1µF capacitor (decoupling)
- 1× 4.7µF capacitor (power filtering)

### 3.3 Case USB Cutout Recommendations

| Feature | Specification | Reasoning |
|---------|--------------|-----------|
| **Cutout Width** | 16-18mm | Accommodates connector + cable |
| **Cutout Height** | 8-10mm | Through case thickness |
| **Corner Radius** | 1.0-2.0mm | Smooth edges |

---

## 4. Component Clearances

### 4.1 Clearance Below PCB

**Minimum Required:** 5.0mm clearance below PCB bottom surface

This accommodates:
- Switch pins: 3.3mm protrusion
- Through-hole diodes: 1.5-2mm height (when laid flat)
- Through-hole resistors: 1.5-2mm height (when laid flat)
- Solder joints: 0.5-1mm

**Recommended:** 5.5-6.0mm clearance for safety margin

### 4.2 Clearance Above PCB

**Minimum Required:** 11.0mm clearance above PCB top surface

This accommodates:
- Switch housing: 5.0mm
- Keycap base: 7.5mm (Cherry profile)
- Key travel: 4.0mm
- Total stack height: ~11mm minimum

**Recommended:** 12-15mm for compatibility with all keycap profiles (SA, MT3, etc.)

### 4.3 Component Keep-Out Zones

Avoid placing case features in these areas:

1. **Around Mounting Holes:** 5mm radius clear zone
2. **USB Connector Area:** 20mm × 15mm zone at connector location
3. **Switch Matrix Area:** Entire PCB top surface
4. **MCU Area:** 35mm × 15mm zone (for DIP-40 ATmega32A)
5. **PCB Edges:** 2mm minimum from PCB edge

---

## 5. Switch and Stabilizer Specifications

### 5.1 Switch Specifications

| Feature | Specification | Notes |
|---------|--------------|-------|
| **Switch Type** | Cherry MX compatible | Standard |
| **Switch Spacing** | 19.05mm (0.75") | Standard keyboard unit |
| **Plate Thickness** | 1.5mm | Standard (1.2-1.6mm acceptable) |
| **Plate Material** | FR4, Aluminum, Brass, PC | Varies by preference |

### 5.2 Stabilizer Specifications

**Cherry-Style Stabilizers (PCB Mount):**

| Size | Usage | Cutout Dimensions |
|------|-------|-------------------|
| **2u** | Backspace, Enter, Shifts | 6.65mm × 13.5mm |
| **6.25u** | Spacebar (standard) | 6.65mm × 13.5mm |
| **7u** | Spacebar (alternative) | 6.65mm × 13.5mm |

**Stabilizer Positions:**
- Backspace: 2u (standard) or 1u split
- Left Shift: 2.25u (standard)
- Right Shift: 1.75u or 2.75u (with arrow keys)
- Enter: 2.25u (ANSI) or ISO Enter
- Spacebar: 6.25u (standard) or 7u

---

## 6. Electrical Specifications

### 6.1 Microcontroller

**Discipline V2 Reference:**

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| **MCU** | ATmega32A | Through-hole DIP-40 |
| **Clock Speed** | 16MHz | External crystal |
| **Operating Voltage** | 5V | Via USB |
| **I/O Pins** | 32 | Sufficient for 68-key matrix |
| **Flash Memory** | 32KB | For firmware |

**Matrix Configuration:**
- Typical: 5 rows × 15 columns (75 positions)
- Actual keys: 68-70 keys
- Diode per switch: 1N4148 (DO-35)

### 6.2 Power Requirements

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| **Input Voltage** | 5V DC | Via USB |
| **Current Draw (No LEDs)** | 50-100mA | MCU + switches |
| **Current Draw (With LEDs)** | 200-500mA | Depends on LED count |
| **USB Standard** | USB 2.0 | Full-speed (12 Mbps) |

### 6.3 Crystal Oscillator

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| **Frequency** | 16MHz | Standard for AVR |
| **Load Capacitance** | 18-22pF | Typically 22pF |
| **Package** | HC-49S (through-hole) | Standard crystal package |

---

## 7. Component Specifications

### 7.1 Through-Hole Components (Discipline V2 BOM)

**Diodes:**
- **Part:** 1N4148 switching diode
- **Package:** DO-35 (through-hole)
- **Quantity:** 68× (one per switch)
- **Purpose:** Matrix isolation

**Resistors (1/4W through-hole):**
- 2× 10kΩ (pull-up resistors)
- 2× 5.1kΩ (USB-C CC pull-down)
- 1× 1.5kΩ (USB D- pull-up)
- 1× 75Ω (USB series termination)

**Capacitors:**
- 2× 22pF ceramic (crystal load caps)
- 1× 0.1µF ceramic (decoupling)
- 1× 4.7µF electrolytic (power filtering)

**Zener Diodes:**
- 2× 3.6V Zener diodes (ESD protection)

**Connectors:**
- 1× USB-C through-hole connector (12-pin)
- Optional: JST connector for daughterboard

**Switches:**
- 2× Tactile switches (Reset, Boot)

### 7.2 Optional Components

- **LEDs:** Per-key backlighting (2-pin LEDs)
- **RGB Underglow:** WS2812B or similar
- **Rotary Encoder:** EC11 (some designs)
- **OLED Display:** 0.91"-0.96" (some designs)

---

## 8. Firmware Support

### 8.1 QMK Firmware

**Discipline V2:**
- **QMK Path:** `coseyfannitutti/discipline`
- **Bootloader:** USBasp or similar
- **VIA Support:** Yes (with VIA-enabled firmware)
- **VIAL Support:** Community builds available

### 8.2 Flashing Instructions

**ATmega32A Flashing:**
1. Install USBasp drivers
2. Connect USBasp programmer to ISP header
3. Flash bootloader (if needed)
4. Flash firmware via QMK Toolbox or command line

**ISP Header Pinout (Standard):**
```
MISO  VCC
SCK   MOSI
RST   GND
```

---

## 9. Case Design Guidelines

### 9.1 Recommended Case Dimensions

Based on typical 65% PCB (~315mm × 95mm):

| Feature | Specification | Reasoning |
|---------|--------------|-----------|
| **Case Length** | 325-330mm | PCB + 5mm border per side |
| **Case Width** | 105-110mm | PCB + 5mm border per side |
| **Border (Left/Right)** | 5-7mm | Aesthetic + structural |
| **Border (Front/Back)** | 5-7mm | Aesthetic + structural |
| **Wall Thickness** | 4.0mm minimum | Structural integrity |

### 9.2 Case Height Options

| Style | Top Frame | Bottom Tray | Total Height | Notes |
|-------|-----------|-------------|--------------|-------|
| **Low-Profile** | 3-4mm | 10-12mm | 13-16mm | Minimal clearance |
| **Standard** | 5-6mm | 15-18mm | 20-24mm | Comfortable clearance |
| **High-Profile** | 8-10mm | 20-25mm | 28-35mm | Maximum clearance |

### 9.3 Typing Angle

| Feature | Specification | Notes |
|---------|--------------|-------|
| **Front Height** | Case height (13-35mm) | Depends on style |
| **Rear Height** | Front + 5-10mm | Creates typing angle |
| **Typing Angle** | 5-7° | Ergonomic standard |
| **Rubber Feet** | 2mm thick, 10mm diameter | 4-6 positions |

---

## 10. Manufacturing Specifications

### 10.1 PCB Manufacturing

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| **Layers** | 2 | Standard double-sided |
| **Material** | FR4 | Standard PCB material |
| **Thickness** | 1.6mm | Standard |
| **Copper Weight** | 1 oz (35 µm) | Standard |
| **Surface Finish** | HASL or ENIG | ENIG preferred for longevity |
| **Silkscreen** | Both sides | Component labels |
| **Solder Mask** | Both sides | Standard green or custom |

### 10.2 Design Rules

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| **Minimum Trace Width** | 6 mil (0.15mm) | Standard |
| **Minimum Trace Spacing** | 6 mil (0.15mm) | Standard |
| **Minimum Drill Size** | 0.3mm | For vias |
| **Through-Hole Pad Size** | 1.5-2.0mm | For component leads |
| **Via Pad Size** | 0.6-0.8mm | Standard |

---

## 11. Design Patterns

### 11.1 Matrix Wiring

**Typical 65% Matrix:**
- **Rows:** 5 (standard)
- **Columns:** 15 (to accommodate 68-70 keys)
- **Diode Orientation:** Cathode to column (COL2ROW) or row (ROW2COL)

**Matrix Example (Discipline V2 style):**
```
Row 0: Esc, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, -, =, Backspace, Del
Row 1: Tab, Q, W, E, R, T, Y, U, I, O, P, [, ], \, PgUp
Row 2: Caps, A, S, D, F, G, H, J, K, L, ;, ', Enter, PgDn
Row 3: Shift, Z, X, C, V, B, N, M, ,, ., /, RShift, Up, End
Row 4: Ctrl, Win, Alt, Space, RAlt, Fn, Left, Down, Right
```

### 11.2 Reset Circuit

**Standard Reset Circuit:**
- 10kΩ pull-up resistor on RESET pin
- Tactile switch to GND
- Optional: 0.1µF capacitor for debouncing

### 11.3 ISP Header

**Standard 6-pin ISP Header:**
- Position: Near MCU
- Pinout: MISO, SCK, RST, VCC, MOSI, GND
- Connector: 2×3 pin header (2.54mm pitch)

---

## 12. Common Variations

### 12.1 Layout Variations

**Right Shift Options:**
- 1.75u Shift + Fn (standard with arrows)
- 2.75u Shift (no Fn key)
- Split right shift (1.75u + 1u)

**Spacebar Options:**
- 6.25u spacebar (standard)
- 7u spacebar (alternative)
- Split spacebar (2.25u + 1.25u + 2.75u)

**Backspace Options:**
- 2u backspace (standard)
- Split backspace (1u + 1u)

### 12.2 Special Features

**Optional Features:**
- **Rotary Encoder:** Typically top-right position
- **OLED Display:** Typically top-right or center
- **Per-Key RGB:** WS2812B or similar
- **Underglow RGB:** WS2812B strip
- **Split Spacebar:** Multiple spacebar configurations

---

## 13. Compatibility Notes

### 13.1 Keycap Compatibility

**Standard Keycap Sets:**
- Most keycap sets include 65% support
- Verify 1.75u right shift included
- Check for 1u keys (Fn, Del, etc.)

**Profile Compatibility:**
- Cherry profile: Standard
- OEM profile: Standard
- SA profile: Requires higher case clearance
- MT3 profile: Requires higher case clearance

### 13.2 Case Compatibility

**Important:** Unlike 60% keyboards, 65% boards do NOT have universal case compatibility. Each design typically requires a custom case.

**Design Considerations:**
- Verify mounting hole positions
- Check PCB dimensions
- Confirm USB cutout position
- Test fit before final production

---

## 14. Reference Resources

### 14.1 Design References

1. **Discipline V2** (coseyfannitutti)
   - Repository: https://github.com/coseyfannitutti/discipline
   - License: CC BY-NC 4.0 (personal use only)
   - Files: KiCad, Gerbers, BOM, Build Guide

2. **QMK Firmware**
   - Documentation: https://docs.qmk.fm
   - Discipline firmware: `keyboards/coseyfannitutti/discipline`

### 14.2 Component Sources

**Recommended Vendors:**
- **Diodes, Resistors, Capacitors:** Mouser, Digikey, LCSC
- **USB-C Connectors:** GCT USB4085 (Mouser, Digikey)
- **ATmega32A:** Microchip Direct, Mouser, Digikey
- **Crystals:** Standard 16MHz HC-49S (any major vendor)

---

## 15. Design Checklist

Use this checklist when designing a 65% through-hole keyboard:

### PCB Design
- [ ] PCB dimensions accommodate 68-70 keys
- [ ] Matrix: 5 rows × 15 columns (or similar)
- [ ] USB-C connector positioned and routed correctly
- [ ] All switches have diodes (1N4148)
- [ ] MCU (ATmega32A or similar) with crystal circuit
- [ ] Reset and boot switches included
- [ ] ISP header for programming

### Clearances
- [ ] 5mm+ clearance below PCB
- [ ] 11mm+ clearance above PCB
- [ ] 5mm clearance around mounting holes
- [ ] USB connector area clear

### Components
- [ ] All through-hole components specified
- [ ] BOM complete with part numbers
- [ ] Alternative parts documented
- [ ] Optional components clearly marked

### Firmware
- [ ] QMK firmware configured
- [ ] Matrix pins defined correctly
- [ ] Bootloader selected
- [ ] VIA support (if desired)

### Manufacturing
- [ ] Gerber files generated
- [ ] Design rules checked (DRC)
- [ ] Electrical rules checked (ERC)
- [ ] BOM exported

### Documentation
- [ ] Build guide created
- [ ] Flashing instructions included
- [ ] Component sourcing guide
- [ ] License information clear

---

## 16. Known Issues and Solutions

### 16.1 Common Issues

**Issue: USB-C connector not detected**
- **Cause:** Missing or incorrect CC pull-down resistors
- **Solution:** Verify 5.1kΩ resistors on CC1 and CC2 pins

**Issue: Keys not registering**
- **Cause:** Diode orientation incorrect
- **Solution:** Verify diode cathode orientation matches firmware

**Issue: MCU not programming**
- **Cause:** ISP header wiring incorrect
- **Solution:** Verify ISP pinout, check connections

### 16.2 Design Tips

1. **Test USB-C circuit:** Prototype USB section first
2. **Verify matrix:** Test matrix with multimeter before assembly
3. **Check clearances:** Measure actual components before finalizing case
4. **Prototype case:** 3D print or test cut before final production
5. **Document everything:** Future you will thank present you

---

**Document Status:** ✅ Complete  
**Last Updated:** 2025-10-17  
**Maintained By:** Through-Hole Keyboard Library  
**Next Review:** When new 65% designs emerge

---

## Appendix A: Discipline V2 Specifications

### A.1 Exact Dimensions

**PCB Outline:**
- Length: ~315mm (verify from KiCad files)
- Width: ~95mm (verify from KiCad files)
- Thickness: 1.6mm

**Mounting Holes:**
- Count: 6 (typical for acrylic case design)
- Positions: See KiCad PCB files for exact coordinates

**USB Connector:**
- Type: USB-C through-hole (GCT USB4085 or similar)
- Position: Top center (verify exact position from PCB)

### A.2 Complete BOM

See `PCB/boms/discipline/` for complete bill of materials.

**Key Components:**
- 68× 1N4148 diodes
- 1× ATmega32A (DIP-40)
- 1× 16MHz crystal (HC-49S)
- 1× USB-C connector (through-hole)
- Resistors: 10kΩ (2×), 5.1kΩ (2×), 1.5kΩ (1×), 75Ω (1×)
- Capacitors: 22pF (2×), 0.1µF (1×), 4.7µF (1×)
- 2× 3.6V Zener diodes
- 2× Tactile switches (reset, boot)

---

## Appendix B: Layout Diagrams

### B.1 Standard 65% Layout

```
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───────┬───┐
│Esc│ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │ 0 │ - │ = │ Bkspc │Del│
├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─────┼───┤
│ Tab │ Q │ W │ E │ R │ T │ Y │ U │ I │ O │ P │ [ │ ] │  \  │PgU│
├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─────┼───┤
│ Caps │ A │ S │ D │ F │ G │ H │ J │ K │ L │ ; │ ' │  Enter │PgD│
├──────┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴────┬───┼───┤
│ Shift  │ Z │ X │ C │ V │ B │ N │ M │ , │ . │ / │Shift │ ↑ │End│
├────┬───┴┬──┴─┬─┴───┴───┴───┴───┴───┴──┬┴───┼───┴┬─┬───┼───┼───┤
│Ctrl│Win │Alt │        Space           │RAlt│ Fn │ │ ← │ ↓ │ → │
└────┴────┴────┴────────────────────────┴────┴────┘ └───┴───┴───┘
```

**Key Count:** 68 keys (standard)

---

**End of Document**
