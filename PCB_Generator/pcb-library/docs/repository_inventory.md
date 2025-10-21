# Through-Hole Keyboard Repository Inventory

## Overview
This document catalogs available through-hole keyboard PCB designs with their design files, documentation, and key features.

---

## Full-Size Keyboards (60%+)

### Lumberjack (5x12 Ortholinear, 60% Case Compatible)
- **Repository:** https://github.com/peej/lumberjack-keyboard
- **Layout:** Split 5x12 ortholinear (60 keys)
- **Form Factor:** Fits standard 60% tray mount cases
- **MCU:** ATmega328P (through-hole DIP)
- **USB:** USB-C or JST connector (12-pin)
- **Available Files:**
  - ✅ Gerber files (gerber/lumberjack.zip)
  - ✅ BOM (BOM.md)
  - ✅ Build guide (guide.md)
  - ✅ FR4 plate gerbers (plates/gerbers)
  - ✅ Component cover DXF (cover.dxf)
  - ✅ 3D printable component cradles
- **QMK Support:** Yes (`peej/lumberjack`)
- **VIA Support:** Yes
- **Revisions:** Rev 1.8 (latest with SMD USB-C)
- **Special Features:**
  - Bakeneko 60 and Singa Unikorn case cutouts
  - MX/Alps/Choc combined footprint (earlier revs)
  - Molex Pico-EZmate connector for universal daughterboard

### Discipline V2 (65%)
- **Repository:** https://github.com/coseyfannitutti/discipline
- **Layout:** 65% (68 keys)
- **MCU:** ATmega32A (through-hole DIP)
- **USB:** USB-C (through-hole)
- **Available Files:**
  - ✅ Gerber files
  - ✅ BOM (doc/)
  - ✅ Build guide (doc/)
  - ✅ Flashing instructions (doc/)
  - ✅ KiCad files
  - ✅ Optional high-profile acrylic case (acrylic-case/)
- **QMK Support:** Yes
- **License:** CC BY-NC 4.0 (personal use only, kits sold by CFTKB.com)
- **Components:** 68× 1N4148 diodes, resistors (10k, 5.1k, 1.5k, 75Ω), zener diodes, capacitors (22pF, 0.1µF, 4.7µF)

### Mysterium (TKL)
- **Repository:** https://github.com/coseyfannitutti/mysterium
- **Layout:** TKL (87-104 keys)
- **MCU:** ATmega32A (through-hole DIP)
- **Available Files:**
  - ✅ Gerber files (Gerber/)
  - ✅ KiCad files (.kicad_pcb, .sch)
  - ✅ BOM (doc/)
  - ✅ Build guide (doc/)
  - ✅ Acrylic guard DXF (mysterium-acrylic-guard.dxf)
  - ✅ Plate DXF (mysterium-kit-plate.dxf)
  - ✅ Case files (case/)
- **Components:** 87× 1N4148 diodes, similar passive components to Discipline

### KBIC65 (65%)
- **Repository:** https://github.com/b-karl/KBIC65
- **Layout:** 65%/70 keys with spaced arrows
- **MCU:** Pro Micro footprint (supports nice!nano for wireless)
- **Available Files:**
  - ✅ KiCad PCB design files
  - ✅ Gerber files (v1.0 release)
  - ✅ SVG drawings (PCB, bottom plate, switch plate, acrylic window)
  - ✅ Build log (build_log.md)
- **Matrix:** 8x9 duplex matrix (17 pins)
- **Firmware:** ZMK (wireless) or QMK
- **Special Features:**
  - Reduced copper for better Bluetooth signal
  - Plate-mounted with screws
  - Two alternative bottom designs (glasses rim / NASA sun dithered art)
  - Includes dithered PCB art tutorial

---

## 40% Keyboards

### Rosaline (40% Staggered)
- **Repository:** https://github.com/peej/rosaline-keyboard
- **Layout:** 40% staggered (fits 60% cases)
- **MCU:** ATmega328P (through-hole DIP)
- **USB:** USB Mini or USB-C
- **Available Files:**
  - ✅ Gerber files
  - ✅ PCB design files
  - ✅ Layout diagrams
- **Matrix:** 7 rows × 8 columns
- **Special Features:**
  - Fits standard 60% tray mount cases
  - Split spacebar or 7u bottom row
  - Split right shift
  - Arrow cluster support
  - Ortholinear variant available

### Litl (40%)
- **Repository:** https://github.com/mohoyt/litl
- **Layout:** 40% (up to 45 keys)
- **MCU:** Pro Micro / Elite C / Nice!nano footprint
- **Available Files:**
  - ✅ PCB files
  - ✅ FR4 switch plate
  - ✅ FR4 base
  - ✅ Build guide (build_guide.md)
  - ✅ Layout diagram
- **Components:** 47× diodes, optional 1-2 rotary encoders, optional OLED
- **QMK Support:** Yes
- **License:** CC BY-NC 4.0 (personal use only, kits sold by sthlmkb.com)
- **Special Features:**
  - Only through-hole components
  - 1 or 2 rotary encoders
  - OLED screen support
  - Multiple layout options (split space, split shift, stepped capslock)
  - Open component aesthetic
- **Known Issues:** Fixed in v3 (gerbers updated)

---

## Macropads

### Plaid-Pad (4x4)
- **Repository:** https://github.com/Keycapsss/Plaid-Pad
- **Layout:** 4x4 numpad/macropad
- **MCU:** ATmega328P with VUSB
- **Available Files:**
  - ✅ Gerber files
  - ✅ Build guide (buildguide_en.md)
  - ✅ 3D printing files (3d-print/)
  - ✅ Laser cut drawings (lasercut/)
- **QMK Support:** Yes (`keycapsss/plaid_pad`)
- **VIA Support:** Yes (no encoder support)
- **VIAL Support:** Yes (with encoder support)
- **Special Features:**
  - Up to 4 rotary encoders (Rev2+)
  - Encoder positions interchangeable with switches
  - OLED display support (Rev3)
  - Choc V2 switch support (Rev2.1+)
- **Bootloader:** USBaspLoader (same as Plaid)
- **Revisions:** Rev3 (latest with OLED)

### Dumbpad (4-6 switches)
- **Repository:** https://github.com/imchipwood/dumbpad
- **Layout:** 4x4 macropad
- **MCU:** Pro Micro or Teensy2.0
- **Available Files:**
  - ✅ Eagle/KiCad files (multiple versions)
  - ✅ Gerber files
  - ✅ 3D printable cases (./case)
- **Variants:**
  - combo: Up to 2 rotary encoders, 3 status LEDs
  - combo_oled: OLED display instead of LEDs
  - combo_teensy: Teensy2.0 version
  - reversible: Single encoder, reversible sockets
  - hotswap_rgb: Per-key RGB, hotswap sockets
- **QMK Support:** Yes
- **Components:** 16× switches, 17× 1n4148 diodes, optional encoders, optional OLED
- **PCB Dimensions:** 97mm × 78.5mm with chamfered corners
- **Mounting:** Four 2mm holes in 40mm square pattern

---

## Reference Designs (Not Through-Hole)

### GH60
- **Repository:** https://github.com/komar007/gh60
- **Layout:** 60% (61 keys)
- **Purpose:** Reference for standard 60% PCB dimensions
- **Key Dimensions:**
  - PCB: 285mm × 94.6mm × 1.6mm
  - Mounting holes: 6 positions (M2 screws)
  - USB cutout: 16mm wide, centered at 142.5mm

---

## Additional Projects (Limited Info Retrieved)

### Plaid (4x12 Ortholinear)
- **Repository:** https://github.com/hsgw/plaid
- **Layout:** 4×12 ortholinear (48 keys)
- **Note:** Original inspiration for many through-hole designs
- **Available:** Build guide and BOM in repo

### Tartan (60%)
- **Repository:** https://github.com/hsgw/tartan
- **Layout:** 60%
- **Available:** Build guide and BOM referenced in README

---

## File Type Summary

### Available Across Projects:
- **Gerber Files:** ✅ All projects (for PCB manufacturing)
- **KiCad Files:** ✅ Most projects (Discipline, Mysterium, KBIC65, Plaid-Pad)
- **Eagle Files:** ✅ Some projects (Dumbpad)
- **BOM (Bill of Materials):** ✅ Most projects
- **Build Guides:** ✅ Most projects
- **DXF Files:** ✅ Several (plates, cases, acrylic covers)
- **STL Files:** ✅ Some (Lumberjack cradles, Dumbpad cases, Plaid-Pad cases)
- **SVG Files:** ✅ Some (KBIC65)
- **Firmware:** ✅ All have QMK support

---

## Common Components Across Projects

### Microcontrollers:
- ATmega328P (DIP) - Lumberjack, Rosaline, Plaid-Pad
- ATmega32A (DIP) - Discipline, Mysterium
- Pro Micro footprint - Litl, KBIC65, Dumbpad

### Diodes:
- 1N4148 (DO-35) - Universal across all projects
- Quantity: 1 per switch

### Passive Components:
- Resistors: 10kΩ, 5.1kΩ, 1.5kΩ, 75Ω (varies by design)
- Capacitors: 0.1µF, 4.7µF, 22pF (for crystal)
- Crystal: 16MHz (for AVR MCUs)

### Connectors:
- USB-C (through-hole or SMD)
- USB Mini (some designs)
- JST connectors (some designs)

### Optional:
- Rotary encoders (EC11)
- OLED displays (0.91"-0.96")
- Status LEDs
- Reset/Boot tactile switches

---

## Next Steps for Resource Collection

1. **Clone repositories** to get full file access
2. **Extract and organize:**
   - Gerber files → PCB/gerbers/[project-name]/
   - KiCad/Eagle files → PCB/design-files/[project-name]/
   - STL files → PCB/3d-models/[project-name]/
   - DXF files → PCB/cad-drawings/[project-name]/
   - BOMs → PCB/boms/[project-name]/
   - Build guides → PCB/docs/build-guides/[project-name]/
3. **Create unified BOM** from all projects
4. **Document common design patterns**
5. **Create design templates** for new through-hole keyboards

## Discipline

- **Repository:** https://github.com/coseyfannitutti/discipline
- **Layout:** 65%
- **MCU:** Unknown
- **USB:** USB-C
- **Available Files:**
  - ✅ Gerber files
  - ✅ KiCad/Eagle files
  - ❌ BOM
  - ✅ Build guide
  - ✅ 3D models
  - ✅ DXF drawings
- **QMK Support:** Unknown
- **VIA/VIAL Support:** Unknown / Unknown
- **License:** CC (Creative Commons)
- **Special Features:** RGB/LED
- **Revision:** f3b8871 (2020-08-25)


## Mysterium

- **Repository:** https://github.com/coseyfannitutti/mysterium
- **Layout:** TKL
- **MCU:** Unknown
- **USB:** USB-C
- **Available Files:**
  - ✅ Gerber files
  - ✅ KiCad/Eagle files
  - ❌ BOM
  - ✅ Build guide
  - ❌ 3D models
  - ✅ DXF drawings
- **QMK Support:** Unknown
- **VIA/VIAL Support:** Unknown / Unknown
- **License:** GPL-3.0
- **Special Features:** RGB/LED
- **Revision:** 5e5ab18 (2020-04-24)


## Lumberjack

- **Repository:** https://github.com/peej/lumberjack-keyboard
- **Layout:** 60%
- **MCU:** ATmega328P
- **USB:** USB-C
- **Available Files:**
  - ✅ Gerber files
  - ✅ KiCad/Eagle files
  - ✅ BOM
  - ✅ Build guide
  - ✅ 3D models
  - ✅ DXF drawings
- **QMK Support:** Unknown
- **VIA/VIAL Support:** Yes / Unknown
- **License:** MIT
- **Special Features:** RGB/LED
- **Revision:** 53bfb50 (2025-09-28)


## Rosaline

- **Repository:** https://github.com/peej/rosaline-keyboard
- **Layout:** 60%
- **MCU:** Unknown
- **USB:** USB-C
- **Available Files:**
  - ✅ Gerber files
  - ✅ KiCad/Eagle files
  - ❌ BOM
  - ✅ Build guide
  - ❌ 3D models
  - ✅ DXF drawings
- **QMK Support:** Unknown
- **VIA/VIAL Support:** Unknown / Unknown
- **License:** MIT
- **Special Features:** RGB/LED
- **Revision:** a40d60e (2021-10-10)


## Litl

- **Repository:** https://github.com/mohoyt/litl
- **Layout:** 60%
- **MCU:** Pro Micro
- **USB:** USB-C
- **Available Files:**
  - ✅ Gerber files
  - ✅ KiCad/Eagle files
  - ❌ BOM
  - ✅ Build guide
  - ✅ 3D models
  - ✅ DXF drawings
- **QMK Support:** Yes
- **VIA/VIAL Support:** Yes / Yes
- **License:** CC (Creative Commons)
- **Special Features:** Rotary encoder, OLED display, RGB/LED, Wireless
- **Revision:** e14aa8b (2025-03-21)


## Kbic65

- **Repository:** https://github.com/b-karl/KBIC65
- **Layout:** 60%
- **MCU:** Pro Micro
- **USB:** Unknown
- **Available Files:**
  - ✅ Gerber files
  - ✅ KiCad/Eagle files
  - ❌ BOM
  - ✅ Build guide
  - ✅ 3D models
  - ✅ DXF drawings
- **QMK Support:** Unknown
- **VIA/VIAL Support:** Yes / Unknown
- **License:** MIT
- **Special Features:** Rotary encoder, OLED display, RGB/LED, Wireless
- **Revision:** d024555 (2021-08-26)


## Plaid

- **Repository:** https://github.com/hsgw/plaid
- **Layout:** Ortholinear
- **MCU:** ATmega328P
- **USB:** Unknown
- **Available Files:**
  - ❌ Gerber files
  - ✅ KiCad/Eagle files
  - ✅ BOM
  - ✅ Build guide
  - ❌ 3D models
  - ✅ DXF drawings
- **QMK Support:** Unknown
- **VIA/VIAL Support:** Unknown / Unknown
- **License:** MIT
- **Special Features:** None documented
- **Revision:** 758419c (2020-08-22)


## Tartan

- **Repository:** https://github.com/hsgw/tartan
- **Layout:** 60%
- **MCU:** ATmega328P
- **USB:** Unknown
- **Available Files:**
  - ❌ Gerber files
  - ✅ KiCad/Eagle files
  - ✅ BOM
  - ✅ Build guide
  - ❌ 3D models
  - ❌ DXF drawings
- **QMK Support:** Unknown
- **VIA/VIAL Support:** Unknown / Unknown
- **License:** Unknown
- **Special Features:** None documented
- **Revision:** f863f6b (2020-12-05)


## Gh60

- **Repository:** https://github.com/komar007/gh60
- **Layout:** Unknown
- **MCU:** Unknown
- **USB:** Unknown
- **Available Files:**
  - ❌ Gerber files
  - ✅ KiCad/Eagle files
  - ✅ BOM
  - ✅ Build guide
  - ❌ 3D models
  - ❌ DXF drawings
- **QMK Support:** Unknown
- **VIA/VIAL Support:** Unknown / Unknown
- **License:** Unknown
- **Special Features:** None documented
- **Revision:** e7948cf (2019-07-02)


## Plaid-pad

- **Repository:** https://github.com/Keycapsss/Plaid-Pad
- **Layout:** Macropad
- **MCU:** ATmega328P
- **USB:** USB-C
- **Available Files:**
  - ❌ Gerber files
  - ❌ KiCad/Eagle files
  - ❌ BOM
  - ✅ Build guide
  - ✅ 3D models
  - ✅ DXF drawings
- **QMK Support:** Unknown
- **VIA/VIAL Support:** Yes / Yes
- **License:** MIT
- **Special Features:** Rotary encoder, OLED display, RGB/LED
- **Revision:** df84d16 (2022-06-29)


## Dumbpad

- **Repository:** https://github.com/imchipwood/dumbpad
- **Layout:** Macropad
- **MCU:** ATmega32U4
- **USB:** USB-C
- **Available Files:**
  - ✅ Gerber files
  - ✅ KiCad/Eagle files
  - ❌ BOM
  - ✅ Build guide
  - ✅ 3D models
  - ❌ DXF drawings
- **QMK Support:** Unknown
- **VIA/VIAL Support:** Yes / Unknown
- **License:** GPL-2.0
- **Special Features:** Rotary encoder, OLED display, RGB/LED, Hot-swap
- **Revision:** 091f4eb (2024-06-19)

