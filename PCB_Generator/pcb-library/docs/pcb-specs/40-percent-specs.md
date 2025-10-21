# 40% Through-Hole Keyboard PCB Specifications
## Reference Standard for 40% Form Factor

**Document Version:** 1.0  
**Date:** 2025-10-17  
**Primary References:** Rosaline, Litl  
**Status:** ✅ Documented from Community Designs

---

## Overview

This document provides reference specifications for 40% through-hole keyboard PCBs. The 40% form factor is a compact keyboard layout typically featuring 40-48 keys, eliminating the number row and often using layers for function keys and numbers.

### Compatible Designs

- **Rosaline** (peej) - 40% staggered, fits 60% cases
- **Litl** (mohoyt) - 40% compact with optional features
- Custom 40% through-hole designs

---

## 1. PCB Outline Dimensions

### 1.1 Overall Dimensions

| Dimension | Specification | Tolerance | Notes |
|-----------|--------------|-----------|-------|
| **Length (X-axis)** | 230-285mm | ±0.5mm | Varies significantly |
| **Width (Y-axis)** | 95-100mm | ±0.5mm | Similar to 60% |
| **Thickness** | 1.6mm | ±0.1mm | Standard PCB thickness |
| **Corner Radius** | 2.0-3.0mm | - | Rounded corners |
| **Layers** | 2 | - | Standard double-sided |

**Note:** 40% keyboards have highly variable dimensions:
- **Compact 40%:** ~230-250mm (Litl style)
- **60% Case Compatible:** ~285mm (Rosaline style)

### 1.2 Layout Characteristics

**Standard 40% Layout:**
- **Alphanumeric cluster:** 3-4 rows
- **No number row:** Numbers accessed via layer
- **Total keys:** 40-48 keys (varies by design)
- **Bottom row:** Multiple spacebar configurations common

---

## 2. Component Clearances

### 2.1 Clearance Below PCB

**Minimum Required:** 5.0mm clearance below PCB bottom surface

**Recommended:** 5.5-6.0mm clearance for safety margin

### 2.2 Clearance Above PCB

**Minimum Required:** 11.0mm clearance above PCB top surface

**For Exposed Component Designs (Litl style):**
- **Minimum:** 15-20mm clearance
- Accommodates visible MCU, diodes, resistors


## 3. Electrical Specifications

### 3.1 Microcontroller Options

**Option 1: ATmega328P (Rosaline style):**
- Through-hole DIP-28
- 16MHz external crystal
- 5V operation via USB
- 23 I/O pins for matrix

**Option 2: Pro Micro Footprint (Litl style):**
- ATmega32U4 via Pro Micro module
- Built-in USB (no external circuit needed)
- Wireless option (Nice!nano)
- 18 usable I/O pins

### 3.2 Matrix Configuration

**Compact 40% Matrix:**
- Typical: 4 rows × 12 columns (48 positions)
- Or: 7 rows × 8 columns (56 positions)
- Actual keys: 40-48 keys
- Diode per switch: 1N4148 (DO-35)

---

## 4. Component Specifications

### 4.1 Through-Hole Components

**Diodes:**
- 1N4148 switching diode (DO-35)
- Quantity: 40-48× (one per switch)

**Resistors (if direct USB):**
- 2× 10kΩ, 2× 5.1kΩ, 1× 1.5kΩ, 1× 75Ω

**Capacitors:**
- 2× 22pF (crystal load caps)
- 1× 0.1µF (decoupling)
- 1× 4.7µF (power filtering)

**MCU:**
- ATmega328P (DIP-28) or Pro Micro module

### 4.2 Optional Components

- **Rotary Encoder:** EC11 (1-2 encoders common)
- **OLED Display:** 0.91"-0.96" (I2C)
- **RGB Underglow:** WS2812B strip
- **Battery Connector:** For wireless builds

---

## 5. Firmware Support

### 5.1 QMK Firmware

**Essential for 40% Keyboards:**
- **Layer 0 (Base):** Letters, common punctuation
- **Layer 1 (Lower):** Numbers, symbols
- **Layer 2 (Raise):** Function keys, navigation
- **Layer 3 (Adjust):** RGB, settings, reset

**Layer Access:**
- Hold key (e.g., Space, Enter) to access layer
- Toggle key to lock layer
- Combo keys (Lower + Raise = Adjust)

---

## 6. Case Design Guidelines

### 6.1 Case Dimensions

**For 60% Case Compatible (Rosaline):**
- Use GH60 case dimensions (295mm × 105mm)
- Uses GH60 mounting pattern

**For Compact 40% (Litl):**
- Case Length: 240-260mm
- Case Width: 105-110mm
- Border: 5-7mm per side
- Wall Thickness: 3.0mm minimum

### 6.2 Case Height Options

| Style | Total Height | Notes |
|-------|-------------|-------|
| **Low-Profile** | 11-13mm | Minimal clearance |
| **Standard** | 16-20mm | Comfortable clearance |
| **Exposed Component** | 20-28mm | Showcases components |

---

## 7. Common Variations

### 7.1 Layout Variations

**Spacebar Options:**
- Single 6.25u spacebar
- Split spacebar (2.25u + 1.25u + 2.75u)
- Multiple 2u spacebars
- All 1u bottom row

**Alpha Cluster:**
- Standard stagger (Rosaline)
- Ortholinear grid (Planck-style)

**Arrow Keys:**
- No arrows (layer only)
- Dedicated arrows (bottom right)

---

## 8. Design Checklist

### PCB Design
- [ ] PCB dimensions appropriate for 40% layout
- [ ] Matrix: 4-7 rows × 8-12 columns
- [ ] USB connector or Pro Micro footprint
- [ ] All switches have diodes (1N4148)
- [ ] Reset switch included

### Firmware
- [ ] QMK firmware configured
- [ ] Layers configured (essential for 40%)
- [ ] Matrix pins defined correctly
- [ ] VIA support (if desired)

### Documentation
- [ ] Build guide created
- [ ] Layer configuration documented
- [ ] Keycap requirements documented

---

## 9. Reference Resources

**Design References:**
1. **Rosaline** - https://github.com/peej/rosaline-keyboard
2. **Litl** - https://github.com/mohoyt/litl
3. **QMK Firmware** - https://docs.qmk.fm

**Component Sources:**
- Pro Micro: SparkFun, AliExpress
- Nice!nano: Nice Keyboards (wireless)
- Rotary Encoders: EC11 (Mouser, Digikey)
- OLED Displays: 0.91" I2C (AliExpress, Adafruit)

---

**Document Status:** ✅ Complete  
**Last Updated:** 2025-10-17  
**Maintained By:** Through-Hole Keyboard Library

---

## Appendix: Common 40% Layouts

### Ortholinear 4×12 (Planck-style)
48 keys in 4 rows × 12 columns grid layout

### Staggered 40% (Rosaline-style)
45 keys with traditional stagger, fits 60% cases

---

**End of Document**
