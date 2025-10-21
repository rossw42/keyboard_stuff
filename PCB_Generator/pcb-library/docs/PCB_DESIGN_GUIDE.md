# PCB Design Guide for Through-Hole Keyboards

Comprehensive guide for designing keyboard PCBs, integrating best practices from ai03's guide and ebastler's ZMK design guide.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Design Workflow](#design-workflow)
3. [Component Selection](#component-selection)
4. [Circuit Design](#circuit-design)
5. [PCB Layout](#pcb-layout)
6. [Manufacturing](#manufacturing)
7. [Testing & Validation](#testing--validation)

---

## Prerequisites

### Required Software

**KiCad 7.0+** (Recommended)
- Download: https://www.kicad.org/download/
- Stable, modern, open-source
- Better library management than 5.x
- Improved routing tools

**Alternative: KiCad 5.1.4** (Legacy)
- Use if following older guides
- Avoid 5.1.5 (router issues) and 5.1.6 (position output issues)

### Required Libraries

**marbastlib** - Keyboard-focused KiCad library
- Repository: https://github.com/ebastler/marbastlib
- Install via KiCad Package Manager (KiCad 7+)
- Contains tested footprints and symbols

### Version Control

**Git/GitHub** - Essential for PCB projects
- Rollback capability
- Collaboration
- Open-source sharing
- Use .gitignore for KiCad projects

---

## Design Workflow

### 1. Project Setup

```
project/
├── project.kicad_pro      # Project file
├── project.kicad_sch      # Schematic
├── project.kicad_pcb      # PCB layout
├── libraries/             # Custom libraries
├── gerbers/              # Manufacturing files
└── README.md             # Documentation
```

### 2. Schematic Design

**Order of Operations:**
1. USB connector and protections
2. Power management (if wireless)
3. MCU and supporting circuitry
4. Switch matrix
5. Optional features (LEDs, encoders, etc.)

### 3. PCB Layout

**Best Practices:**
1. Component placement first
2. Route critical signals (USB, crystal)
3. Route matrix
4. Ground plane
5. Design rule check (DRC)

---

## Component Selection

### MCUs for Through-Hole Keyboards

**ATmega328P** (Arduino Uno compatible)
- Package: DIP-28 (through-hole)
- Pins: 23 I/O
- Flash: 32KB
- Firmware: QMK
- Use case: Simple keyboards, learning

**ATmega32A** (QMK standard)
- Package: DIP-40 (through-hole)
- Pins: 32 I/O
- Flash: 32KB
- Firmware: QMK, VIA
- Use case: Most through-hole keyboards

**Pro Micro** (Module)
- MCU: ATmega32U4
- Package: Through-hole module
- Pins: 18 I/O
- USB: Built-in
- Use case: Quick prototypes, modular designs

**nRF52840** (Wireless - Advanced)
- Package: Module (Holyiot, nice!nano)
- Bluetooth: 5.0 LE
- Firmware: ZMK
- Use case: Wireless keyboards
- Note: Requires battery management

### USB Connectors

**USB-C (Recommended)**
- Part: HRO Type-C-31-M-12 (top mount)
- Part: HRO Type-C-31-M-14 (mid mount)
- Pros: Modern, reversible, robust
- Through-hole variants available

**USB Mini/Micro** (Legacy)
- Easier to solder
- Cheaper
- Less robust

### Diodes

**1N4148** (Standard)
- Package: DO-35 (through-hole)
- Forward voltage: 1V
- Use: One per switch (anti-ghosting)

**1N4007** (Alternative)
- Larger, easier to solder
- Same function

### Switches

**Cherry MX Compatible**
- Standard: 5-pin through-hole
- Spacing: 19.05mm (0.75")
- Footprint: MX_PCB_1.00u

---

## Circuit Design

### USB Protection Circuit

**Essential Components:**
```
USB-C Connector
├── R1, R2: 5.1kΩ (CC pull-down, identifies as UFP)
├── L1, L2: Ferrite beads (EMI filtering)
├── D1: ESD protection (USBLC6-2SC6 or similar)
├── F1: Polyfuse 500mA (overcurrent protection)
└── C1, C2: 100nF (decoupling)
```

**Why Each Component:**
- **5.1kΩ resistors**: Tell USB-C host we're a device
- **Ferrite beads**: Filter high-frequency noise
- **ESD diode**: Protect against electrostatic discharge
- **Polyfuse**: Prevent overcurrent damage
- **Capacitors**: Smooth power, filter noise

### MCU Supporting Circuit (ATmega328P)

**Minimum Required:**
```
ATmega328P
├── C1-C4: 100nF (decoupling on VCC/AVCC/AREF)
├── R1: 10kΩ (pull-up on RESET)
├── X1: 16MHz crystal
├── C5, C6: 22pF (crystal load capacitors)
└── ISP Header: 6-pin (programming)
```

**Crystal Circuit:**
- 16MHz for USB timing
- 22pF load caps (check crystal datasheet)
- Keep traces short (<10mm)
- Ground plane underneath

### Switch Matrix

**Diode Configuration:**
```
COL2ROW (Recommended for through-hole):
  Switch → Diode (cathode to switch) → Row
  Column connects directly to switch

ROW2COL (Alternative):
  Switch → Diode (anode to switch) → Column  
  Row connects directly to switch
```

**Matrix Optimization:**
- Minimize rows + columns
- Typical: 5 rows × 14 cols = 70 keys
- Avoid: More than 8 rows or 18 columns
- Check: MCU has enough pins

### Power Circuit (Wired)

**Simple 5V Design:**
```
USB 5V → Polyfuse → MCU VCC
              ↓
         Decoupling caps
```

**With 3.3V Regulator:**
```
USB 5V → LDO (AMS1117-3.3) → 3.3V devices
         ├── C_in: 10µF
         └── C_out: 10µF
```

---

## PCB Layout

### Layer Stack (2-layer)

```
Top Layer:
- Components
- Signal traces
- Ground fills

Bottom Layer:
- Ground plane (primary)
- Signal traces (minimal)
- Power traces
```

### Component Placement

**Priority Order:**
1. **USB connector** - Edge of board, accessible
2. **MCU** - Central location
3. **Crystal** - Close to MCU (<10mm)
4. **Switches** - Grid layout, precise spacing
5. **Diodes** - Near switches
6. **Decoupling caps** - Near MCU pins

**Through-Hole Specific:**
- Components on top, solder on bottom
- Keep tall components away from switches
- Consider case clearance (12mm+ above PCB)

### Routing Guidelines

**Critical Traces:**
- **USB D+/D-**: Differential pair, 90Ω impedance
  - Keep equal length (±5mm)
  - Avoid vias
  - Route away from noisy signals
  
- **Crystal**: Short, direct, ground plane underneath
  - No vias in crystal traces
  - Guard ring optional but recommended

**Matrix Routing:**
- Rows: Horizontal traces
- Columns: Vertical traces
- Width: 0.25mm minimum, 0.4mm recommended
- Clearance: 0.2mm minimum

**Ground Plane:**
- Fill all unused space
- Connect with vias (every 10-20mm)
- Avoid splits under high-speed signals

### Design Rules

**Minimum Values:**
- Trace width: 0.25mm (signal), 0.5mm (power)
- Clearance: 0.2mm
- Via size: 0.8mm drill, 1.2mm pad
- Hole size: 1.0mm (through-hole components)

**Recommended Values:**
- Trace width: 0.4mm (signal), 0.8mm (power)
- Clearance: 0.3mm
- Via size: 0.8mm drill, 1.4mm pad

---

## Manufacturing

### PCB Specifications

**Standard 2-Layer:**
- Thickness: 1.6mm
- Copper weight: 1oz (35µm)
- Surface finish: HASL or ENIG
- Solder mask: Any color
- Silkscreen: White (best contrast)

**Manufacturers:**
- JLCPCB (cheap, fast)
- PCBWay (good quality)
- OSH Park (USA, purple PCBs)

### Gerber Export

**Required Files:**
- F.Cu (top copper)
- B.Cu (bottom copper)
- F.Mask (top solder mask)
- B.Mask (bottom solder mask)
- F.Silkscreen (top silkscreen)
- B.Silkscreen (bottom silkscreen)
- Edge.Cuts (board outline)
- PTH.drl (plated through holes)
- NPTH.drl (non-plated holes)

**KiCad Export:**
1. File → Fabrication Outputs → Gerbers
2. Select all layers above
3. Plot format: Gerber
4. Include extended attributes
5. Generate drill files

---

## Testing & Validation

### Pre-Manufacturing Checks

**DRC (Design Rule Check):**
- Run in KiCad: Inspect → Design Rules Checker
- Fix all errors
- Review warnings

**ERC (Electrical Rule Check):**
- Run in schematic
- Check for unconnected pins
- Verify power connections

**Visual Inspection:**
- Check component footprints
- Verify pin assignments
- Review silkscreen text

### Post-Manufacturing Testing

**Visual Inspection:**
- Check for shorts (multimeter continuity)
- Verify component orientation
- Check solder joints

**Power-On Test:**
1. Measure voltage at MCU (should be 5V)
2. Check for shorts (current <50mA idle)
3. Program bootloader
4. Flash test firmware

**Matrix Test:**
- Short each switch position
- Verify key registration
- Check for ghosting

---

## Common Issues & Solutions

### Issue: USB Not Recognized
**Causes:**
- D+/D- swapped
- Missing 5.1kΩ resistors (USB-C)
- Crystal not oscillating
- Bootloader not flashed

**Solutions:**
- Check USB traces with multimeter
- Verify resistor values
- Check crystal with oscilloscope
- Flash bootloader via ISP

### Issue: Keys Not Registering
**Causes:**
- Matrix trace broken
- Diode orientation wrong
- Pin assignment mismatch

**Solutions:**
- Test continuity on matrix traces
- Check diode bands (cathode marking)
- Verify firmware pin configuration

### Issue: Ghosting
**Causes:**
- Missing diodes
- Diode orientation wrong

**Solutions:**
- Install diodes on all switches
- Check diode orientation (band to row in COL2ROW)

---

## References

### Essential Reading
- **ai03 PCB Guide**: https://wiki.ai03.com/books/pcb-design
- **ZMK Design Guide**: https://github.com/ebastler/zmk-designguide
- **QMK Documentation**: https://docs.qmk.fm/
- **KiCad Documentation**: https://docs.kicad.org/

### Component Datasheets
- ATmega328P: https://ww1.microchip.com/downloads/en/DeviceDoc/ATmega328P-Datasheet.pdf
- ATmega32A: https://ww1.microchip.com/downloads/en/DeviceDoc/doc8155.pdf
- 1N4148: Standard diode datasheet

### Community Resources
- **Keyboard Atelier Discord**: https://discord.gg/b7vwhHS
- **QMK Discord**: https://discord.gg/qmk
- **ZMK Discord**: https://zmk.dev/community/discord/invite

---

**Last Updated:** October 20, 2025  
**Version:** 1.0  
**Status:** Comprehensive guide for through-hole keyboard PCB design
