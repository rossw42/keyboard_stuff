# Master Bill of Materials (BOM) Summary

**Last Updated:** October 21, 2025  
**Projects Covered:** 11 through-hole keyboard designs

---

## Overview

This master BOM consolidates components across all projects in the library. Components are normalized and categorized for easy sourcing and comparison.

### Data Sources
- ✅ **Lumberjack:** Complete BOM extracted
- ✅ **Plaid:** Complete BOM extracted
- ✅ **Plaid-Pad:** Complete BOM extracted from build guide
- ⚠️ **Litl:** Partial BOM from build guide (quantities only)
- ⏳ **Discipline, Mysterium, Tartan, Rosaline, KBIC65, Dumbpad, GH60:** BOMs available in original repositories (not yet extracted)

---

## Component Categories

### 1. Microcontrollers (MCU)

| Component | Package | Projects | Notes |
|-----------|---------|----------|-------|
| ATmega328P-PU | DIP-28 | Lumberjack, Plaid, Plaid-Pad | Most common through-hole MCU |
| ATmega32A | DIP-40 | Discipline, Mysterium | Larger through-hole MCU |
| Pro Micro | Module | Litl, KBIC65, Dumbpad | Arduino-compatible (can use Elite-C, Nice!nano) |

**Sourcing Notes:**
- ATmega328P: Widely available, ~$2-4 USD
- ATmega32A: Less common, ~$3-5 USD
- Pro Micro: $4-8 USD (clones), $15-20 USD (Elite-C), $25+ USD (Nice!nano)

---

### 2. Diodes

#### Switching Diodes (1N4148)
- **Quantity:** 1 per key (45-87 depending on layout)
- **Package:** DO-35 (through-hole)
- **Projects:** All keyboard projects
- **Sourcing:** Very common, ~$0.01-0.02 per unit in bulk

#### Zener Diodes (3.6V)
- **Quantity:** 2 per board
- **Package:** DO-35 (through-hole)
- **Purpose:** USB voltage protection
- **Projects:** Lumberjack, Plaid, Plaid-Pad
- **Sourcing:** Common, ~$0.05-0.10 per unit

---

### 3. Capacitors

#### Ceramic Capacitors
| Value | Pitch | Quantity | Purpose | Projects |
|-------|-------|----------|---------|----------|
| 22pF | 2.5mm | 2 | Crystal load capacitors | Lumberjack, Plaid, Plaid-Pad |
| 100nF (0.1µF) | 5.0mm | 2 | Decoupling | Lumberjack, Plaid, Plaid-Pad |

#### Electrolytic Capacitors
| Value | Pitch | Quantity | Purpose | Projects |
|-------|-------|----------|---------|----------|
| 4.7µF | 1.5mm | 1 | Power filtering | Lumberjack, Plaid, Plaid-Pad |

**Sourcing Notes:**
- Ceramic capacitors: Very common, ~$0.02-0.05 per unit
- Electrolytic: Common, ~$0.05-0.10 per unit
- **Important:** Electrolytic capacitors are polarized!

---

### 4. Resistors

All resistors are 1/6W (or 1/4W) axial through-hole type.

| Value | Quantity | Purpose | Projects |
|-------|----------|---------|----------|
| 1.5kΩ | 3 | USB data lines | Lumberjack, Plaid, Plaid-Pad |
| 75Ω | 2 | USB impedance matching | Lumberjack, Plaid, Plaid-Pad |
| 10kΩ | 1 | Pull-up resistor | Lumberjack, Plaid, Plaid-Pad |
| 5.1kΩ | 2 | USB-C CC pull-down | Lumberjack, Plaid-Pad (USB-C only) |

**Sourcing Notes:**
- Very common values, ~$0.01-0.02 per unit in bulk
- Color codes:
  - 1.5kΩ: Brown-Green-Black-Brown-Brown
  - 75Ω: Violet-Green-Black-Gold-Brown (or Purple-Green-Black-Gold-Brown)
  - 10kΩ: Brown-Black-Black-Red-Brown
  - 5.1kΩ: Green-Brown-Black-Brown-Brown

---

### 5. Crystals

| Value | Package | Quantity | Projects |
|-------|---------|----------|----------|
| 16MHz | HC49-4H | 1 | Lumberjack, Plaid, Plaid-Pad |

**Sourcing Notes:**
- Common frequency for AVR MCUs
- ~$0.20-0.50 per unit
- Requires 22pF load capacitors

---

### 6. Fuses

| Type | Rating | Pitch | Projects |
|------|--------|-------|----------|
| Polyfuse (Resettable) | 100mA | 5mm | Lumberjack, Plaid, Plaid-Pad |

**Sourcing Notes:**
- Protects USB port from overcurrent
- ~$0.10-0.20 per unit

---

### 7. Connectors

#### USB Connectors
| Type | Part Number | Projects | Notes |
|------|-------------|----------|-------|
| USB-C | TYPE-C-31-M-12 | Lumberjack | 12-pin through-hole |
| USB Mini-B | Standard | Plaid | Through-hole |
| USB-C | Various | Plaid-Pad, Discipline, Mysterium | Check specific project |

#### Programming Headers
| Type | Pitch | Projects | Notes |
|------|-------|----------|-------|
| 2x3 pin | 2.54mm | Lumberjack, Plaid | AVR ISP (optional) |

#### Other Connectors
| Type | Part Number | Projects | Notes |
|------|-------------|----------|-------|
| JST SH | SM04B-SRSS-TB | Lumberjack | Daughterboard (optional) |
| Molex Pico-EZmate | 781710004 | Lumberjack | Universal daughterboard (optional) |

---

### 8. Sockets

| Type | Pins | Projects | Notes |
|------|------|----------|-------|
| DIP IC Socket | 28-pin narrow | Lumberjack, Plaid, Plaid-Pad | For ATmega328P |
| DIP IC Socket | 40-pin narrow | Discipline, Mysterium | For ATmega32A |

**Sourcing Notes:**
- Highly recommended for easy MCU replacement
- ~$0.20-0.50 per socket
- Use narrow (0.3") width for standard DIP packages

---

### 9. Switches

#### Tactile Switches
| Type | Size | Quantity | Purpose | Projects |
|------|------|----------|---------|----------|
| Tactile | 6x6mm | 2 | Reset/Boot | Most projects |

#### Keyboard Switches
| Type | Mount | Quantity | Projects |
|------|-------|----------|----------|
| Cherry MX Compatible | PCB Mount (5-pin) | 45-87 | All keyboard projects |

**Sourcing Notes:**
- Tactile switches: Very common, ~$0.10-0.20 per unit
- MX switches: $0.20-1.00+ per switch depending on type
- **Important:** Use PCB mount (5-pin) switches for stability

---

### 10. LEDs

| Type | Size | Quantity | Purpose | Projects |
|------|------|----------|---------|----------|
| LED | 3mm | 2 | Status indicators | Lumberjack, Plaid, Plaid-Pad |

**Sourcing Notes:**
- Common colors: Red (power), Green (status)
- ~$0.05-0.10 per LED
- **Important:** LEDs are polarized (short leg = cathode = square pad)

---

### 11. Hardware

| Type | Size | Quantity | Purpose | Projects |
|------|------|----------|---------|----------|
| M2 Screws | 4-8mm | 8-14 | Standoff mounting | Lumberjack, Plaid |
| M2 Standoffs | 10mm | 4 | Component cover | Lumberjack, Plaid |
| M2 Nuts | - | 0-26 | Assembly | Plaid |
| Rubber Feet | - | 4 | Case bottom | Plaid |

---

### 12. Optional Components

| Component | Type | Projects | Notes |
|-----------|------|----------|-------|
| Rotary Encoder | EC11 | Litl, Plaid-Pad, Dumbpad | 1-4 encoders |
| OLED Display | 0.91"-0.96" I2C | Litl, Plaid-Pad, Dumbpad | Optional display |
| Acrylic Cover | 95x57x2mm | Lumberjack | Component protection |

---

## Common Component Kits

### Basic AVR Kit (ATmega328P projects)
Suitable for: Lumberjack, Plaid, Plaid-Pad

- 1× ATmega328P-PU (DIP-28)
- 1× 28-pin DIP socket
- 48-60× 1N4148 diodes
- 2× 3.6V zener diodes
- 2× 22pF ceramic capacitors
- 2× 100nF ceramic capacitors
- 1× 4.7µF electrolytic capacitor
- 3× 1.5kΩ resistors
- 2× 75Ω resistors
- 1× 10kΩ resistor
- 1× 16MHz crystal (HC49)
- 1× 100mA polyfuse
- 2× 6x6mm tactile switches
- 2× 3mm LEDs
- 1× USB connector (varies by project)

**Estimated Cost:** $10-15 USD (excluding switches and USB connector)

---

## Sourcing Recommendations

### Recommended Vendors

**North America:**
- Mouser Electronics (mouser.com)
- Digikey (digikey.com)
- LCSC (lcsc.com) - Good for bulk orders

**Europe:**
- Reichelt (reichelt.de)
- TME (tme.eu)
- Mouser Europe

**Asia:**
- LCSC (lcsc.com)
- Taobao (for China)
- AliExpress (longer shipping)

### Bulk Ordering Tips

1. **Diodes:** Buy in strips of 100+ for best pricing
2. **Resistors:** Buy assortment kits with common values
3. **Capacitors:** Buy assortment kits
4. **MCUs:** Buy from authorized distributors to avoid counterfeits
5. **Switches:** Group buys or bulk orders from mechanical keyboard vendors

---

## Component Substitutions

### Safe Substitutions
- **1N4148 → 1N4148W:** SMD version (not recommended for through-hole builds)
- **ATmega328P-PU → ATmega328P-AU:** TQFP version (requires adapter or reflow)
- **Pro Micro → Elite-C:** Drop-in replacement with USB-C
- **Pro Micro → Nice!nano:** Drop-in replacement with Bluetooth (requires ZMK firmware)

### Not Recommended
- **ATmega328P ↔ ATmega32A:** Different pinouts, not compatible
- **Different crystal frequencies:** Requires firmware changes
- **Different capacitor types:** Ceramic vs electrolytic have different characteristics

---

## Quality Control

### Component Testing
1. **Diodes:** Test with multimeter in diode mode
2. **Resistors:** Verify values with multimeter
3. **Capacitors:** Check polarity on electrolytics
4. **MCUs:** Flash test firmware before soldering
5. **Crystals:** Test with oscilloscope if available

### Common Issues
- **Counterfeit MCUs:** Buy from authorized distributors
- **Wrong diode orientation:** Check black line matches square pad
- **Wrong capacitor polarity:** Short leg = cathode = square pad
- **Wrong resistor values:** Verify color codes

---

## Next Steps

### To Complete This BOM:
1. Extract BOMs from remaining projects:
   - Discipline
   - Mysterium
   - Tartan
   - Rosaline
   - KBIC65
   - Dumbpad
   - GH60 (reference only)

2. Add vendor part numbers for all components

3. Create project-specific BOM files with exact quantities

4. Add pricing information (approximate)

5. Create sourcing guides for different regions

---

## Related Documents

- [Component Sourcing Guide](../docs/component_sourcing_guide.md)
- [Master BOM CSV](master-bom.csv)
- [Project Catalog](../PROJECT_CATALOG.md)
- [Repository Inventory](../docs/repository_inventory.md)

---

**Generated by:** Through-Hole Keyboard Library Project  
**Version:** 1.0.0
