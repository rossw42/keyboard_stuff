# TKL (Tenkeyless) Through-Hole Keyboard PCB Specifications
## Reference Standard for TKL Form Factor

**Document Version:** 1.0  
**Date:** 2025-10-17  
**Primary Reference:** Mysterium (coseyfannitutti)  
**Status:** ✅ Documented from Community Designs

---

## Overview

This document provides reference specifications for TKL (Tenkeyless) through-hole keyboard PCBs. The TKL form factor is a full-size keyboard without the numpad, typically featuring 87-88 keys including function row, navigation cluster, and full arrow keys. This specification is based primarily on the Mysterium design, a popular open-source through-hole TKL keyboard.

### Compatible Designs

- **Mysterium** (coseyfannitutti) - Primary reference
- Custom TKL through-hole designs following similar layout

---

## 1. PCB Outline Dimensions

### 1.1 Overall Dimensions

| Dimension | Specification | Tolerance | Notes |
|-----------|--------------|-----------|-------|
| **Length (X-axis)** | ~360-375mm | ±0.5mm | Varies by design |
| **Width (Y-axis)** | ~140-150mm | ±0.5mm | Includes nav cluster |
| **Thickness** | 1.6mm | ±0.1mm | Standard PCB thickness |
| **Corner Radius** | 2.0-3.0mm | - | Rounded corners |
| **Layers** | 2 | - | Standard double-sided |

**Note:** TKL keyboards do not have a universal mounting standard. Each design may have unique mounting hole positions and case requirements.

### 1.2 Layout Characteristics

**Standard TKL Layout:**
- **Alphanumeric cluster:** 60% standard (14.25u width)
- **Function row:** F1-F12 (12 keys)
- **Navigation cluster:** 6 keys (Ins, Home, PgUp, Del, End, PgDn)
- **Arrow cluster:** 4 keys in inverted-T arrangement
- **Modifier cluster:** 3 keys (PrtSc, ScrLk, Pause)
- **Total keys:** 87 keys (ANSI) to 88 keys (ISO)

---

## 2. Mounting Specifications

### 2.1 Mounting System

**Important:** TKL keyboards typically use **tray mount** or **integrated plate mounting** systems. Mounting hole positions vary significantly by design.

**Mysterium Mounting:**
- Uses acrylic case with standoffs
- Multiple mounting points for structural support
- Typically 8-12 mounting points distributed across PCB

### 2.2 Recommended Mounting Approach

| Feature | Specification | Notes |
|---------|--------------|-------|
| **Mounting Style** | Tray mount or integrated plate | Design-dependent |
| **Hole Diameter** | 2.0-2.2mm | For M2 screws |
| **Standoff Height** | 5-10mm | Depends on case design |
| **Positional Tolerance** | ±0.2mm | Structural support |
| **Mounting Points** | 8-12 recommended | Distributed for stability |

**Design Tip:** TKL boards are longer and require more mounting points than 60% boards to prevent PCB flex. Position mounting holes to provide balanced support, especially in the center of the board.

---

## 3. USB Port Specifications

### 3.1 USB Connector Position

| Feature | Specification | Notes |
|---------|--------------|-------|
| **Connector Type** | USB-C or Mini-USB | Through-hole preferred |
| **Position** | Top edge, typically left-center | Varies by design |
| **Distance from Edge** | 5-10mm | From PCB top edge |
| **Connector Width** | ~8-10mm | Actual connector footprint |

### 3.2 Through-Hole USB Implementation

**Mysterium Style (ATmega32A with USB-C):**

**Components:**
- USB-C connector (through-hole, 12-pin)
- 2× 5.1kΩ resistors (CC pull-down for USB-C)
- 2× 3.6V Zener diodes (ESD protection)
- 1× 1.5kΩ resistor (D- pull-up for USB 2.0)
- 1× 75Ω resistor (series termination)
- 2× 22pF capacitors (crystal load caps)
- 1× 0.1µF capacitor (decoupling)
- 1× 4.7µF capacitor (power filtering)

**Alternative: USB Mini-B (older designs):**
- USB Mini-B connector (through-hole, 5-pin)
- Similar passive components
- Simpler circuit (no CC resistors needed)

### 3.3 Case USB Cutout Recommendations

| Feature | Specification | Reasoning |
|---------|--------------|-----------|
| **Cutout Width** | 16-18mm | Accommodates connector + cable |
| **Cutout Height** | 8-10mm | Through case thickness |
| **Corner Radius** | 1.0-2.0mm | Smooth edges |
| **Position** | Verify from PCB design | Not standardized |

---

## 4. Component Clearances

### 4.1 Clearance Below PCB

**Minimum Required:** 5.0mm clearance below PCB bottom surface

This accommodates:
- Switch pins: 3.3mm protrusion
- Through-hole diodes: 1.5-2mm height (when laid flat)
- Through-hole resistors: 1.5-2mm height (when laid flat)
- MCU socket (if used): 3-4mm height
- Solder joints: 0.5-1mm

**Recommended:** 6.0mm clearance for safety margin (especially with DIP-40 MCU)

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
4. **MCU Area:** 40mm × 20mm zone (for DIP-40 ATmega32A)
5. **Navigation Cluster:** Ensure adequate spacing between main and nav clusters
6. **PCB Edges:** 2mm minimum from PCB edge

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
| **2u** | Backspace, Enter, Shifts, Numpad keys | 6.65mm × 13.5mm |
| **6.25u** | Spacebar (standard) | 6.65mm × 13.5mm |
| **7u** | Spacebar (alternative) | 6.65mm × 13.5mm |

**Stabilizer Positions (TKL):**
- Backspace: 2u (standard)
- Left Shift: 2.25u (standard)
- Right Shift: 2.75u (standard)
- Enter: 2.25u (ANSI) or ISO Enter
- Spacebar: 6.25u (standard) or 7u
- Numpad Enter: 2u (if present)
- Numpad Plus: 2u (if present)
- Numpad 0: 2u (if present)

---

## 6. Electrical Specifications

### 6.1 Microcontroller

**Mysterium Reference:**

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| **MCU** | ATmega32A | Through-hole DIP-40 |
| **Clock Speed** | 16MHz | External crystal |
| **Operating Voltage** | 5V | Via USB |
| **I/O Pins** | 32 | Sufficient for 87-key matrix |
| **Flash Memory** | 32KB | For firmware |

**Matrix Configuration:**
- Typical: 6 rows × 16 columns (96 positions)
- Actual keys: 87-88 keys
- Diode per switch: 1N4148 (DO-35)

### 6.2 Power Requirements

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| **Input Voltage** | 5V DC | Via USB |
| **Current Draw (No LEDs)** | 50-100mA | MCU + switches |
| **Current Draw (With LEDs)** | 300-500mA | Depends on LED count |
| **USB Standard** | USB 2.0 | Full-speed (12 Mbps) |

### 6.3 Crystal Oscillator

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| **Frequency** | 16MHz | Standard for AVR |
| **Load Capacitance** | 18-22pF | Typically 22pF |
| **Package** | HC-49S (through-hole) | Standard crystal package |

---

## 7. Component Specifications

### 7.1 Through-Hole Components (Mysterium BOM)

**Diodes:**
- **Part:** 1N4148 switching diode
- **Package:** DO-35 (through-hole)
- **Quantity:** 87× (one per switch)
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
- 1× USB-C through-hole connector (12-pin) or USB Mini-B
- Optional: JST connector for daughterboard

**Switches:**
- 2× Tactile switches (Reset, Boot)

**MCU:**
- 1× ATmega32A (DIP-40)
- Optional: DIP-40 socket for easy replacement

**Crystal:**
- 1× 16MHz crystal (HC-49S through-hole)

### 7.2 Optional Components

- **LEDs:** Per-key backlighting (2-pin LEDs)
- **RGB Underglow:** WS2812B or similar
- **Status LEDs:** Caps Lock, Scroll Lock, Num Lock indicators
- **Rotary Encoder:** EC11 (some designs)
- **OLED Display:** 0.91"-0.96" (some designs)

---

## 8. Firmware Support

### 8.1 QMK Firmware

**Mysterium:**
- **QMK Path:** `coseyfannitutti/mysterium`
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

**Command Line Flashing:**
```bash
# Flash firmware
qmk flash -kb coseyfannitutti/mysterium -km default

# Or with avrdude directly
avrdude -c usbasp -p m32 -U flash:w:mysterium_default.hex
```

---

## 9. Case Design Guidelines

### 9.1 Recommended Case Dimensions

Based on typical TKL PCB (~365mm × 145mm):

| Feature | Specification | Reasoning |
|---------|--------------|-----------|
| **Case Length** | 375-380mm | PCB + 5mm border per side |
| **Case Width** | 155-160mm | PCB + 5mm border per side |
| **Border (Left/Right)** | 5-7mm | Aesthetic + structural |
| **Border (Front/Back)** | 5-7mm | Aesthetic + structural |
| **Wall Thickness** | 4.0mm minimum | Structural integrity |

### 9.2 Case Height Options

| Style | Top Frame | Bottom Tray | Total Height | Notes |
|-------|-----------|-------------|--------------|-------|
| **Low-Profile** | 3-4mm | 12-14mm | 15-18mm | Minimal clearance |
| **Standard** | 5-6mm | 16-20mm | 21-26mm | Comfortable clearance |
| **High-Profile** | 8-10mm | 22-28mm | 30-38mm | Maximum clearance |

### 9.3 Typing Angle

| Feature | Specification | Notes |
|---------|--------------|-------|
| **Front Height** | Case height (15-38mm) | Depends on style |
| **Rear Height** | Front + 8-12mm | Creates typing angle |
| **Typing Angle** | 5-7° | Ergonomic standard |
| **Rubber Feet** | 2mm thick, 10mm diameter | 4-6 positions |

### 9.4 TKL-Specific Considerations

**Structural Support:**
- TKL boards are longer and require more mounting points
- Recommend 8-12 mounting points distributed across PCB
- Consider center support to prevent PCB flex
- Thicker case walls (4-5mm) for rigidity

**Weight Distribution:**
- TKL boards are heavier than 60% boards
- Consider weight distribution when positioning mounting points
- Add rubber feet at strategic positions for stability

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

**Typical TKL Matrix:**
- **Rows:** 6 (standard)
- **Columns:** 16 (to accommodate 87-88 keys)
- **Diode Orientation:** Cathode to column (COL2ROW) or row (ROW2COL)

**Matrix Example (Mysterium style):**
```
Row 0: Esc, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, PrtSc, ScrLk, Pause
Row 1: `, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, -, =, Backspace, Ins, Home, PgUp
Row 2: Tab, Q, W, E, R, T, Y, U, I, O, P, [, ], \, Del, End, PgDn
Row 3: Caps, A, S, D, F, G, H, J, K, L, ;, ', Enter
Row 4: Shift, Z, X, C, V, B, N, M, ,, ., /, RShift, Up
Row 5: Ctrl, Win, Alt, Space, RAlt, Fn, Ctrl, Left, Down, Right
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

### 11.4 LED Indicators

**Status LEDs (Optional):**
- Caps Lock LED: Typically on Caps Lock key or separate indicator
- Scroll Lock LED: Typically separate indicator
- Num Lock LED: N/A for TKL (no numpad)

**Implementation:**
- LED + current limiting resistor (220Ω-1kΩ)
- Connected to MCU GPIO pin
- Controlled by firmware

---

## 12. Common Variations

### 12.1 Layout Variations

**Function Row:**
- Standard: F1-F12 with gaps (F4|F5, F8|F9)
- Compact: F1-F12 without gaps

**Navigation Cluster:**
- Standard: 2×3 grid (Ins/Home/PgUp, Del/End/PgDn)
- Compact: Reduced spacing

**Modifier Keys:**
- Standard: PrtSc, ScrLk, Pause above nav cluster
- Alternative: Combined or omitted

### 12.2 Special Features

**Optional Features:**
- **Rotary Encoder:** Typically top-right position
- **OLED Display:** Typically top-right or center
- **Per-Key RGB:** WS2812B or similar
- **Underglow RGB:** WS2812B strip
- **Split Spacebar:** Multiple spacebar configurations
- **Blocker:** Aesthetic element between clusters

---

## 13. Compatibility Notes

### 13.1 Keycap Compatibility

**Standard Keycap Sets:**
- Most keycap sets include TKL support (base kit)
- Verify function row included (F1-F12)
- Check for 2.75u right shift
- Verify navigation cluster keys included

**Profile Compatibility:**
- Cherry profile: Standard
- OEM profile: Standard
- SA profile: Requires higher case clearance
- MT3 profile: Requires higher case clearance

### 13.2 Case Compatibility

**Important:** TKL keyboards do NOT have universal case compatibility. Each design typically requires a custom case.

**Design Considerations:**
- Verify mounting hole positions
- Check PCB dimensions (especially length)
- Confirm USB cutout position
- Ensure adequate support for longer PCB
- Test fit before final production

---

## 14. Reference Resources

### 14.1 Design References

1. **Mysterium** (coseyfannitutti)
   - Repository: https://github.com/coseyfannitutti/mysterium
   - License: GPL-3.0
   - Files: KiCad, Gerbers, BOM, Build Guide

2. **QMK Firmware**
   - Documentation: https://docs.qmk.fm
   - Mysterium firmware: `keyboards/coseyfannitutti/mysterium`

### 14.2 Component Sources

**Recommended Vendors:**
- **Diodes, Resistors, Capacitors:** Mouser, Digikey, LCSC
- **USB-C Connectors:** GCT USB4085 (Mouser, Digikey)
- **ATmega32A:** Microchip Direct, Mouser, Digikey
- **Crystals:** Standard 16MHz HC-49S (any major vendor)
- **DIP Sockets:** 40-pin DIP socket (optional, for easy MCU replacement)

---

## 15. Design Checklist

Use this checklist when designing a TKL through-hole keyboard:

### PCB Design
- [ ] PCB dimensions accommodate 87-88 keys
- [ ] Matrix: 6 rows × 16 columns (or similar)
- [ ] USB connector positioned and routed correctly
- [ ] All switches have diodes (1N4148)
- [ ] MCU (ATmega32A or similar) with crystal circuit
- [ ] Reset and boot switches included
- [ ] ISP header for programming
- [ ] 8-12 mounting holes for structural support

### Clearances
- [ ] 6mm+ clearance below PCB (for DIP-40 MCU)
- [ ] 11mm+ clearance above PCB
- [ ] 5mm clearance around mounting holes
- [ ] USB connector area clear
- [ ] Adequate spacing between main and nav clusters

### Components
- [ ] All through-hole components specified
- [ ] BOM complete with part numbers
- [ ] Alternative parts documented
- [ ] Optional components clearly marked
- [ ] DIP socket for MCU (optional but recommended)

### Firmware
- [ ] QMK firmware configured
- [ ] Matrix pins defined correctly
- [ ] Bootloader selected
- [ ] VIA support (if desired)
- [ ] LED indicators configured (if present)

### Manufacturing
- [ ] Gerber files generated
- [ ] Design rules checked (DRC)
- [ ] Electrical rules checked (ERC)
- [ ] BOM exported
- [ ] PCB flex tested (important for TKL length)

### Documentation
- [ ] Build guide created
- [ ] Flashing instructions included
- [ ] Component sourcing guide
- [ ] License information clear
- [ ] Assembly tips for longer PCB

---

## 16. Known Issues and Solutions

### 16.1 Common Issues

**Issue: PCB flex in center**
- **Cause:** Insufficient mounting points or support
- **Solution:** Add center mounting points, use thicker PCB (2.0mm), or add plate support

**Issue: USB-C connector not detected**
- **Cause:** Missing or incorrect CC pull-down resistors
- **Solution:** Verify 5.1kΩ resistors on CC1 and CC2 pins

**Issue: Keys not registering**
- **Cause:** Diode orientation incorrect
- **Solution:** Verify diode cathode orientation matches firmware

**Issue: MCU not programming**
- **Cause:** ISP header wiring incorrect
- **Solution:** Verify ISP pinout, check connections

**Issue: Case doesn't fit PCB**
- **Cause:** PCB dimensions or mounting holes don't match case
- **Solution:** Verify dimensions before manufacturing, prototype first

### 16.2 Design Tips

1. **Test USB-C circuit:** Prototype USB section first
2. **Verify matrix:** Test matrix with multimeter before assembly
3. **Check clearances:** Measure actual components before finalizing case
4. **Prototype case:** 3D print or test cut before final production
5. **Test PCB flex:** Ensure adequate support for longer PCB
6. **Document everything:** Future you will thank present you
7. **Use DIP socket:** Makes MCU replacement easier if needed

---

**Document Status:** ✅ Complete  
**Last Updated:** 2025-10-17  
**Maintained By:** Through-Hole Keyboard Library  
**Next Review:** When new TKL designs emerge

---

## Appendix A: Mysterium Specifications

### A.1 Exact Dimensions

**PCB Outline:**
- Length: ~365mm (verify from KiCad files)
- Width: ~145mm (verify from KiCad files)
- Thickness: 1.6mm

**Mounting Holes:**
- Count: 8-10 (typical for acrylic case design)
- Positions: See KiCad PCB files for exact coordinates

**USB Connector:**
- Type: USB-C through-hole or USB Mini-B
- Position: Top left-center (verify exact position from PCB)

### A.2 Complete BOM

See `PCB/boms/mysterium/` for complete bill of materials.

**Key Components:**
- 87× 1N4148 diodes
- 1× ATmega32A (DIP-40)
- 1× 16MHz crystal (HC-49S)
- 1× USB connector (through-hole)
- Resistors: 10kΩ (2×), 5.1kΩ (2×), 1.5kΩ (1×), 75Ω (1×)
- Capacitors: 22pF (2×), 0.1µF (1×), 4.7µF (1×)
- 2× 3.6V Zener diodes
- 2× Tactile switches (reset, boot)
- Optional: DIP-40 socket

---

## Appendix B: Layout Diagrams

### B.1 Standard TKL Layout (ANSI)

```
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐ ┌───┬───┬───┐
│Esc│F1 │F2 │F3 │F4 │F5 │F6 │F7 │F8 │F9 │F10│F11│F12│ │PSc│SLk│Pau│
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘ └───┴───┴───┘
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───────┐ ┌───┬───┬───┐
│ ` │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │ 0 │ - │ = │ Bkspc │ │Ins│Hom│PgU│
├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─────┤ ├───┼───┼───┤
│ Tab │ Q │ W │ E │ R │ T │ Y │ U │ I │ O │ P │ [ │ ] │  \  │ │Del│End│PgD│
├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─────┤ └───┴───┴───┘
│ Caps │ A │ S │ D │ F │ G │ H │ J │ K │ L │ ; │ ' │  Enter │
├──────┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴────────┤     ┌───┐
│ Shift  │ Z │ X │ C │ V │ B │ N │ M │ , │ . │ / │   Shift  │     │ ↑ │
├────┬───┴┬──┴─┬─┴───┴───┴───┴───┴───┴──┬┴───┼───┴┬────┬────┤ ┌───┼───┼───┐
│Ctrl│Win │Alt │         Space          │ Alt│ Fn │Menu│Ctrl│ │ ← │ ↓ │ → │
└────┴────┴────┴────────────────────────┴────┴────┴────┴────┘ └───┴───┴───┘
```

**Key Count:** 87 keys (ANSI standard)

---

**End of Document**
