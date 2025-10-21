# Macropad Through-Hole PCB Specifications
## Reference Standard for Macropad Form Factor

**Document Version:** 1.0  
**Date:** 2025-10-17  
**Primary References:** Plaid-Pad, Dumbpad  
**Status:** ✅ Documented from Community Designs

---

## Overview

This document provides reference specifications for through-hole macropad PCBs. Macropads are compact input devices typically featuring 4-16 keys, often with rotary encoders and OLED displays. They serve as programmable shortcut pads for productivity, gaming, or creative applications.

### Compatible Designs

- **Plaid-Pad** (Keycapsss) - 4×4 macropad with VUSB
- **Dumbpad** (imchipwood) - 4×4 macropad with Pro Micro
- Custom macropad through-hole designs

---

## 1. PCB Outline Dimensions

### 1.1 Overall Dimensions

| Dimension | Specification | Tolerance | Notes |
|-----------|--------------|-----------|-------|
| **Length (X-axis)** | 80-100mm | ±0.5mm | Varies by design |
| **Width (Y-axis)** | 80-100mm | ±0.5mm | Often square |
| **Thickness** | 1.6mm | ±0.1mm | Standard PCB thickness |
| **Corner Radius** | 2.0-5.0mm | - | Often rounded or chamfered |
| **Layers** | 2 | - | Standard double-sided |

**Common Sizes:**
- **4×4 (16 keys):** ~95mm × 80mm (Dumbpad)
- **4×4 with encoders:** ~100mm × 85mm (Plaid-Pad)
- **3×3 (9 keys):** ~75mm × 75mm
- **2×4 (8 keys):** ~60mm × 95mm

### 1.2 Layout Characteristics

**Standard Macropad Layouts:**
- **4×4:** 16 keys (most common)
- **3×3:** 9 keys (compact)
- **2×4:** 8 keys (vertical)
- **Encoders:** 1-4 rotary encoders (often replace keys)
- **OLED:** 0.91"-0.96" display (common)


## 2. Mounting Specifications

### 2.1 Mounting System

**Common Mounting Approaches:**
- **4-hole pattern:** Square pattern (40-50mm spacing)
- **Rubber feet:** 4 corners, no screws
- **Integrated plate:** FR4 plate with standoffs
- **3D printed case:** Custom mounting

### 2.2 Recommended Mounting

| Feature | Specification | Notes |
|---------|--------------|-------|
| **Mounting Holes** | 4 positions | Square pattern |
| **Hole Diameter** | 2.0-2.2mm | For M2 screws |
| **Hole Spacing** | 40-50mm | Square pattern |
| **Standoff Height** | 5-8mm | Depends on design |

**Dumbpad Example:**
- 4 mounting holes in 40mm square pattern
- 2mm diameter holes for M2 screws

---

## 3. USB Port Specifications

### 3.1 USB Connector Position

| Feature | Specification | Notes |
|---------|--------------|-------|
| **Connector Type** | USB-C or Mini-USB | Or Pro Micro |
| **Position** | Top or side edge | Varies by design |
| **Distance from Edge** | 5-10mm | From PCB edge |

### 3.2 USB Implementation Options

**Option 1: VUSB (Plaid-Pad style):**
- ATmega328P with VUSB firmware
- USB-C or Mini-B connector
- Minimal external components
- Software USB implementation

**Option 2: Pro Micro (Dumbpad style):**
- Pro Micro / Elite-C / Nice!nano footprint
- USB handled by Pro Micro module
- Simplest PCB design
- Hardware USB support

**Option 3: Direct USB (ATmega32U4):**
- Native USB support
- Requires USB circuit components
- More complex but integrated

---

## 4. Component Clearances

### 4.1 Clearance Below PCB

**Minimum Required:** 5.0mm clearance below PCB

This accommodates:
- Switch pins: 3.3mm
- Diodes: 1.5-2mm (laid flat)
- Pro Micro: 3-4mm (if bottom-mounted)
- Solder joints: 0.5-1mm

**Recommended:** 6.0mm for Pro Micro designs

### 4.2 Clearance Above PCB

**Minimum Required:** 11.0mm clearance above PCB

For exposed component designs:
- **Minimum:** 15-20mm clearance
- Accommodates visible components
- Popular aesthetic for macropads

---

## 5. Electrical Specifications

### 5.1 Microcontroller Options

**Option 1: ATmega328P with VUSB (Plaid-Pad):**
- Through-hole DIP-28
- 16MHz external crystal
- Software USB (VUSB)
- 23 I/O pins

**Option 2: Pro Micro (Dumbpad):**
- ATmega32U4 via Pro Micro module
- Hardware USB support
- 18 usable I/O pins
- Easiest implementation

**Option 3: Teensy 2.0:**
- ATmega32U4
- Hardware USB support
- More I/O pins than Pro Micro
- Alternative to Pro Micro

### 5.2 Matrix Configuration

**4×4 Macropad Matrix:**
- **Rows:** 4
- **Columns:** 4
- **Total positions:** 16
- **Diode per switch:** 1N4148 (DO-35)

**With Encoders:**
- Encoders can replace switch positions
- Or use dedicated pins (not in matrix)

### 5.3 Power Requirements

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| **Input Voltage** | 5V DC | Via USB |
| **Current Draw** | 50-200mA | Depends on LEDs |
| **USB Standard** | USB 2.0 | Full-speed |

---

## 6. Component Specifications

### 6.1 Through-Hole Components

**Diodes:**
- 1N4148 switching diode (DO-35)
- Quantity: 16-17× (one per switch + one for USB)

**Resistors (if VUSB):**
- 2× 68Ω (USB data lines)
- 1× 1.5kΩ (USB pull-up)
- 2× 10kΩ (pull-up resistors)

**Capacitors:**
- 2× 22pF (crystal load caps)
- 2× 0.1µF (decoupling)
- 1× 4.7µF (power filtering)

**Zener Diodes (if VUSB):**
- 2× 3.6V Zener diodes (USB voltage clamp)

**MCU:**
- ATmega328P (DIP-28) or Pro Micro module

**Crystal (if ATmega328P):**
- 1× 16MHz crystal (HC-49S)

### 6.2 Optional Components

**Rotary Encoders:**
- EC11 rotary encoder (most common)
- Quantity: 1-4 encoders
- Can replace key positions

**OLED Display:**
- 0.91"-0.96" OLED (I2C)
- 128×32 or 128×64 resolution
- Shows layer, status, custom graphics

**RGB LEDs:**
- WS2812B per-key RGB
- Or underglow strip
- Quantity: 16× (per-key) or 4-8× (underglow)

**Status LEDs:**
- 2-pin LEDs with resistors
- Caps Lock, Num Lock indicators
- Custom status indicators

---

## 7. Firmware Support

### 7.1 QMK Firmware

**Plaid-Pad:**
- QMK Path: `keycapsss/plaid_pad`
- Bootloader: USBaspLoader
- VIA Support: Yes (no encoder)
- VIAL Support: Yes (with encoder)

**Dumbpad:**
- QMK Path: `imchipwood/dumbpad`
- Bootloader: Caterina (Pro Micro)
- VIA Support: Yes
- Multiple variants supported

### 7.2 Macropad Features

**Common Macropad Functions:**
- **Macros:** Multi-key sequences
- **Layers:** Multiple key mappings
- **Encoder:** Volume, scrolling, layer switching
- **OLED:** Status display, custom graphics
- **RGB:** Per-key or underglow effects
- **Tap Dance:** Multiple functions per key

---

## 8. Rotary Encoder Integration

### 8.1 Encoder Specifications

**EC11 Rotary Encoder:**
- **Footprint:** 5-pin (2 for rotation, 1 for click, 2 for mounting)
- **Rotation:** Quadrature encoding (2 pins)
- **Click:** Optional push button (1 pin)
- **Mounting:** Through-hole, 7mm spacing

### 8.2 Encoder Positions

**Common Positions:**
- **Top corners:** 1-2 encoders
- **Top center:** 1 encoder
- **Replace keys:** Encoders in key positions

**Plaid-Pad Example:**
- Up to 4 encoders (Rev2+)
- Encoder positions interchangeable with switches
- Flexible layout options

### 8.3 Encoder Functions

**Common Uses:**
- **Volume control:** Most popular
- **Scrolling:** Vertical or horizontal
- **Layer switching:** Rotate to change layers
- **Zoom:** In/out for creative apps
- **Brush size:** For digital art
- **Timeline scrubbing:** For video editing

---

## 9. OLED Display Integration

### 9.1 Display Specifications

**Common OLED Sizes:**
- **0.91":** 128×32 pixels (compact)
- **0.96":** 128×64 pixels (more info)

**Interface:**
- **I2C:** 2 pins (SDA, SCL) + power
- **Address:** 0x3C or 0x3D (configurable)

### 9.2 Display Position

**Common Positions:**
- **Top center:** Above keys
- **Top corner:** Next to encoder
- **Side:** Vertical orientation

### 9.3 Display Content

**Common Displays:**
- **Layer indicator:** Current layer name/number
- **WPM:** Words per minute counter
- **Logo:** Custom graphics
- **Status:** Caps Lock, Num Lock, etc.
- **Animation:** Custom animations

---

## 10. Case Design Guidelines

### 10.1 Case Dimensions

**For 4×4 Macropad (~95mm × 80mm PCB):**

| Feature | Specification | Reasoning |
|---------|--------------|-----------|
| **Case Length** | 105mm | PCB + 5mm border per side |
| **Case Width** | 90mm | PCB + 5mm border per side |
| **Border** | 5mm | Aesthetic + structural |
| **Wall Thickness** | 3.0mm | Adequate for small case |

### 10.2 Case Height Options

| Style | Total Height | Notes |
|-------|-------------|-------|
| **Low-Profile** | 12-15mm | Minimal clearance |
| **Standard** | 18-22mm | Comfortable clearance |
| **Exposed Component** | 25-30mm | Showcases components |

### 10.3 Case Features

**Common Features:**
- **Rubber feet:** 4 corners, 10mm diameter
- **Encoder knob:** Aluminum or 3D printed
- **OLED window:** Cutout or clear acrylic
- **USB cutout:** 16-18mm wide
- **Tenting:** Angled feet for ergonomics

---

## 11. Manufacturing Specifications

### 11.1 PCB Manufacturing

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| **Layers** | 2 | Standard |
| **Material** | FR4 | Standard |
| **Thickness** | 1.6mm | Standard |
| **Surface Finish** | HASL or ENIG | ENIG preferred |
| **Solder Mask** | Both sides | Custom colors popular |

### 11.2 Design Rules

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| **Minimum Trace Width** | 6 mil (0.15mm) | Standard |
| **Minimum Trace Spacing** | 6 mil (0.15mm) | Standard |
| **Minimum Drill Size** | 0.3mm | For vias |

---

## 12. Common Variations

### 12.1 Layout Variations

**Key Count:**
- 4×4 (16 keys) - Most common
- 3×3 (9 keys) - Compact
- 2×4 (8 keys) - Vertical
- 5×4 (20 keys) - Extended

**Encoder Count:**
- No encoders - Keys only
- 1 encoder - Most common
- 2 encoders - Popular
- 4 encoders - Maximum (Plaid-Pad)

**Display:**
- No display - Minimal
- OLED - Most common
- Multiple OLEDs - Advanced

### 12.2 Special Features

**Hot-Swap Sockets:**
- Kailh hot-swap sockets
- Easy switch replacement
- No soldering required

**RGB Lighting:**
- Per-key RGB (WS2812B)
- Underglow RGB strip
- Status LEDs

**Wireless:**
- Nice!nano for Bluetooth
- Battery connector
- Power switch

---

## 13. Design Checklist

### PCB Design
- [ ] PCB dimensions appropriate for macropad
- [ ] Matrix: 3-4 rows × 3-4 columns
- [ ] USB connector or Pro Micro footprint
- [ ] All switches have diodes
- [ ] Encoder footprints (if used)
- [ ] OLED footprint (if used)
- [ ] Mounting holes (4 positions)

### Components
- [ ] All through-hole components specified
- [ ] BOM complete with part numbers
- [ ] Encoder specified (if used)
- [ ] OLED specified (if used)
- [ ] RGB LEDs specified (if used)

### Firmware
- [ ] QMK firmware configured
- [ ] Matrix pins defined
- [ ] Encoder support (if used)
- [ ] OLED support (if used)
- [ ] RGB support (if used)
- [ ] VIA/VIAL support (if desired)

### Case
- [ ] Case dimensions accommodate PCB
- [ ] Mounting holes aligned
- [ ] USB cutout positioned
- [ ] Encoder knob clearance (if used)
- [ ] OLED window (if used)
- [ ] Rubber feet positions

---

## 14. Reference Resources

**Design References:**
1. **Plaid-Pad** - https://github.com/Keycapsss/Plaid-Pad
2. **Dumbpad** - https://github.com/imchipwood/dumbpad
3. **QMK Firmware** - https://docs.qmk.fm

**Component Sources:**
- Pro Micro: SparkFun, AliExpress
- EC11 Encoders: Mouser, Digikey, AliExpress
- OLED Displays: AliExpress, Adafruit
- WS2812B LEDs: AliExpress, Adafruit
- Encoder Knobs: AliExpress, Amazon

---

## 15. Known Issues and Solutions

### 15.1 Common Issues

**Issue: Encoder not working**
- **Cause:** Incorrect wiring or firmware config
- **Solution:** Verify encoder pins, check QMK config

**Issue: OLED not displaying**
- **Cause:** I2C address mismatch or wiring
- **Solution:** Check I2C address (0x3C/0x3D), verify SDA/SCL

**Issue: USB not detected (VUSB)**
- **Cause:** Incorrect resistor values or Zener diodes
- **Solution:** Verify 68Ω, 1.5kΩ resistors and 3.6V Zeners

### 15.2 Design Tips

1. **Test encoder:** Verify encoder works before case assembly
2. **Test OLED:** Verify display works before case assembly
3. **Prototype case:** 3D print before final production
4. **Consider knob:** Choose encoder knob that fits design
5. **Test macros:** Verify macro functionality before deployment
6. **Document layout:** Create clear layout diagram for users

---

**Document Status:** ✅ Complete  
**Last Updated:** 2025-10-17  
**Maintained By:** Through-Hole Keyboard Library

---

## Appendix: Common Macropad Layouts

### 4×4 Standard Layout
```
┌───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │
├───┼───┼───┼───┤
│ 5 │ 6 │ 7 │ 8 │
├───┼───┼───┼───┤
│ 9 │10 │11 │12 │
├───┼───┼───┼───┤
│13 │14 │15 │16 │
└───┴───┴───┴───┘
```

### 4×4 with Encoder
```
┌───┬───┬───┬───┐
│ENC│ 2 │ 3 │ 4 │  ENC = Rotary Encoder
├───┼───┼───┼───┤
│ 5 │ 6 │ 7 │ 8 │
├───┼───┼───┼───┤
│ 9 │10 │11 │12 │
├───┼───┼───┼───┤
│13 │14 │15 │16 │
└───┴───┴───┴───┘
```

---

**End of Document**
