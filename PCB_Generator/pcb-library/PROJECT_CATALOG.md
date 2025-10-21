# Through-Hole Keyboard Project Catalog

**Library Version:** 1.0.0  
**Last Updated:** 2025-10-20  
**Total Projects:** 11

---

## Quick Reference Table

| Project | Layout | MCU | Firmware | License | Tags |
|---------|--------|-----|----------|---------|------|
| [Discipline](#discipline) | 65% | ATmega32A | QMK | CC BY-NC 4.0 | 65%, usb-c, tht-dip, led |
| [Mysterium](#mysterium) | TKL | ATmega32A | QMK | GPL-3.0 | tkl, usb-c, tht-dip, led |
| [Lumberjack](#lumberjack) | 60% Ortho | ATmega328P | QMK, VIA | MIT | 60%, ortholinear, usb-c, tht-dip, via-support |
| [Rosaline](#rosaline) | 40% | ATmega328P | QMK | MIT | 40%, staggered, usb-c, tht-dip |
| [Litl](#litl) | 40% | Pro Micro | QMK, VIA, VIAL | CC BY-NC 4.0 | 40%, pro-micro, encoder, oled, wireless |
| [KBIC65](#kbic65) | 65% | Pro Micro | QMK, ZMK | MIT | 65%, pro-micro, wireless, encoder, oled |
| [Plaid](#plaid) | Ortho 4x12 | ATmega328P | QMK | MIT | ortholinear, macropad, tht-dip |
| [Tartan](#tartan) | 60% | ATmega328P | QMK | MIT | 60%, tht-dip |
| [Plaid-Pad](#plaid-pad) | 4x4 Macropad | ATmega328P | QMK, VIA, VIAL | MIT | macropad, usb-c, encoder, oled, via-support |
| [Dumbpad](#dumbpad) | 4x4 Macropad | ATmega32U4 | QMK, VIA | GPL-2.0 | macropad, usb-c, encoder, oled, hotswap, led |
| [GH60](#gh60) | 60% | N/A | N/A | Unknown | reference, 60%, specifications |

---

## Search by Category

### By Form Factor
- **60%:** Lumberjack, Tartan, GH60
- **65%:** Discipline, KBIC65
- **TKL:** Mysterium
- **40%:** Rosaline, Litl
- **Ortholinear:** Lumberjack, Plaid
- **Macropad:** Plaid-Pad, Dumbpad

### By MCU Type
- **ATmega328P (DIP):** Lumberjack, Rosaline, Plaid, Tartan, Plaid-Pad
- **ATmega32A (DIP):** Discipline, Mysterium
- **ATmega32U4 (Pro Micro):** Litl, KBIC65, Dumbpad

### By Features
- **USB-C:** Discipline, Mysterium, Lumberjack, Rosaline, Litl, Plaid-Pad, Dumbpad
- **Rotary Encoder:** Litl, KBIC65, Plaid-Pad, Dumbpad
- **OLED Display:** Litl, KBIC65, Plaid-Pad, Dumbpad
- **Wireless Support:** Litl, KBIC65
- **VIA Support:** Lumberjack, Litl, KBIC65, Plaid-Pad, Dumbpad
- **VIAL Support:** Litl, Plaid-Pad
- **Hotswap:** Dumbpad
- **LED/RGB:** Discipline, Mysterium, Lumberjack, Rosaline, Litl, KBIC65, Plaid-Pad, Dumbpad

### By Firmware Support
- **QMK:** All projects (except GH60 reference)
- **VIA:** Lumberjack, Litl, KBIC65, Plaid-Pad, Dumbpad
- **VIAL:** Litl, Plaid-Pad
- **ZMK:** KBIC65

### By License
- **MIT:** Lumberjack, Rosaline, KBIC65, Plaid, Tartan, Plaid-Pad
- **GPL-2.0:** Dumbpad
- **GPL-3.0:** Mysterium
- **CC BY-NC 4.0:** Discipline, Litl (personal use only)
- **Unknown:** GH60

---

## Detailed Project Information

### Discipline
**65% Through-Hole Keyboard with USB-C**

- **Repository:** https://github.com/coseyfannitutti/discipline
- **Layout:** 65% (68 keys)
- **Form Factor:** Standard 65% mounting
- **MCU:** ATmega32A (through-hole DIP-40)
- **USB:** USB-C (through-hole)
- **Firmware:** QMK
- **VIA/VIAL:** Unknown / Unknown
- **License:** CC BY-NC 4.0 (personal use only, kits sold by CFTKB.com)
- **Revision:** f3b8871 (2020-08-25)

**Available Files:**
- ✅ Gerber files (PCB + Plate)
- ✅ KiCad design files
- ✅ Build guide
- ✅ 3D models (case)
- ✅ DXF drawings (plate, case)
- ❌ BOM (available in original repo)

**Key Components:**
- 68× 1N4148 diodes
- Resistors: 10kΩ, 5.1kΩ, 1.5kΩ, 75Ω
- Zener diodes
- Capacitors: 22pF, 0.1µF, 4.7µF
- 16MHz crystal
- Through-hole USB-C connector

**Special Features:**
- High-profile acrylic case option
- Through-hole USB-C implementation
- LED support
- Visible component aesthetic

**Tags:** `65%`, `usb-c`, `tht-dip`, `atmega32a`, `led`, `acrylic-case`, `qmk`

---

### Mysterium
**TKL Through-Hole Keyboard**

- **Repository:** https://github.com/coseyfannitutti/mysterium
- **Layout:** TKL (87-104 keys)
- **Form Factor:** Tenkeyless
- **MCU:** ATmega32A (through-hole DIP-40)
- **USB:** USB-C
- **Firmware:** QMK
- **VIA/VIAL:** Unknown / Unknown
- **License:** GPL-3.0
- **Revision:** 5e5ab18 (2020-04-24)

**Available Files:**
- ✅ Gerber files (PCB + Plate)
- ✅ KiCad design files
- ✅ Build guide
- ✅ DXF drawings (plate, case, acrylic guard)
- ❌ BOM (available in original repo)
- ❌ 3D models

**Key Components:**
- 87× 1N4148 diodes
- Similar passive components to Discipline
- 16MHz crystal
- Through-hole USB-C connector

**Special Features:**
- Acrylic component guard
- Multiple case options
- LED support
- Visible component aesthetic

**Tags:** `tkl`, `usb-c`, `tht-dip`, `atmega32a`, `led`, `acrylic-guard`, `qmk`

---

### Lumberjack
**5x12 Ortholinear, 60% Case Compatible**

- **Repository:** https://github.com/peej/lumberjack-keyboard
- **Layout:** Split 5x12 ortholinear (60 keys)
- **Form Factor:** Fits standard 60% tray mount cases
- **MCU:** ATmega328P (through-hole DIP-28)
- **USB:** USB-C or JST connector (12-pin)
- **Firmware:** QMK (`peej/lumberjack`)
- **VIA/VIAL:** Yes / Unknown
- **License:** MIT
- **Revision:** 53bfb50 (2025-09-28)

**Available Files:**
- ✅ Gerber files (PCB + FR4 Plate)
- ✅ KiCad design files
- ✅ BOM
- ✅ Build guide
- ✅ 3D models (component cradles)
- ✅ DXF drawings (component cover)

**Key Components:**
- 60× 1N4148 diodes
- ATmega328P DIP-28
- 16MHz crystal
- USB-C connector or JST
- Molex Pico-EZmate connector

**Special Features:**
- Bakeneko 60 and Singa Unikorn case cutouts
- MX/Alps/Choc combined footprint (earlier revisions)
- Universal daughterboard support
- 3D printable component cradles
- FR4 plate option
- VIA support

**Tags:** `60%`, `ortholinear`, `usb-c`, `tht-dip`, `atmega328p`, `via-support`, `case-compatible`, `qmk`

---

### Rosaline
**40% Staggered, 60% Case Compatible**

- **Repository:** https://github.com/peej/rosaline-keyboard
- **Layout:** 40% staggered (fits 60% cases)
- **Form Factor:** Fits standard 60% tray mount cases
- **MCU:** ATmega328P (through-hole DIP-28)
- **USB:** USB Mini or USB-C
- **Firmware:** QMK
- **VIA/VIAL:** Unknown / Unknown
- **License:** MIT
- **Revision:** a40d60e (2021-10-10)
- **Matrix:** 7 rows × 8 columns

**Available Files:**
- ✅ Gerber files (PCB + Plate)
- ✅ KiCad design files
- ✅ Build guide
- ✅ DXF drawings (plate)
- ❌ BOM
- ❌ 3D models

**Special Features:**
- Fits standard 60% tray mount cases
- Split spacebar or 7u bottom row
- Split right shift
- Arrow cluster support
- Ortholinear variant available

**Tags:** `40%`, `staggered`, `usb-c`, `tht-dip`, `atmega328p`, `case-compatible`, `qmk`

---

### Litl
**40% Compact with Optional Features**

- **Repository:** https://github.com/mohoyt/litl
- **Layout:** 40% (up to 45 keys)
- **Form Factor:** Compact 40%
- **MCU:** Pro Micro / Elite-C / nice!nano footprint
- **USB:** USB-C (via Pro Micro)
- **Firmware:** QMK
- **VIA/VIAL:** Yes / Yes
- **License:** CC BY-NC 4.0 (personal use only, kits sold by sthlmkb.com)
- **Revision:** e14aa8b (2025-03-21)

**Available Files:**
- ✅ Gerber files (PCB + FR4 Plate + FR4 Base)
- ✅ KiCad design files
- ✅ Build guide
- ✅ 3D models
- ✅ DXF drawings
- ❌ BOM (available in original repo)

**Key Components:**
- 47× diodes
- Pro Micro / Elite-C / nice!nano
- Optional 1-2 rotary encoders (EC11)
- Optional OLED display (0.91"-0.96")

**Special Features:**
- Only through-hole components
- 1 or 2 rotary encoders
- OLED screen support
- Multiple layout options (split space, split shift, stepped capslock)
- Open component aesthetic
- Wireless support (with nice!nano)
- VIA and VIAL support

**Tags:** `40%`, `pro-micro`, `usb-c`, `encoder`, `oled`, `wireless`, `via-support`, `vial-support`, `qmk`

---

### KBIC65
**65% with Wireless Support**

- **Repository:** https://github.com/b-karl/KBIC65
- **Layout:** 65%/70 keys with spaced arrows
- **Form Factor:** 65% with custom mounting
- **MCU:** Pro Micro footprint (supports nice!nano for wireless)
- **USB:** USB-C (via Pro Micro)
- **Firmware:** QMK, ZMK (wireless)
- **VIA/VIAL:** Yes / Unknown
- **License:** MIT
- **Revision:** d024555 (2021-08-26)
- **Matrix:** 8x9 duplex matrix (17 pins)

**Available Files:**
- ✅ Gerber files (PCB + Plate)
- ✅ KiCad design files
- ✅ Build guide (build log)
- ✅ 3D models
- ✅ DXF drawings (SVG format)
- ❌ BOM

**Special Features:**
- Reduced copper for better Bluetooth signal
- Plate-mounted with screws
- Two alternative bottom designs (glasses rim / NASA sun dithered art)
- Includes dithered PCB art tutorial
- Wireless support with nice!nano
- Optional rotary encoder
- Optional OLED display

**Tags:** `65%`, `pro-micro`, `wireless`, `encoder`, `oled`, `via-support`, `zmk`, `qmk`, `pcb-art`

---

### Plaid
**4x12 Ortholinear - Original Through-Hole Design**

- **Repository:** https://github.com/hsgw/plaid
- **Layout:** 4×12 ortholinear (48 keys)
- **Form Factor:** Ortholinear macropad/keyboard
- **MCU:** ATmega328P (through-hole DIP-28)
- **USB:** USB Mini/Micro
- **Firmware:** QMK
- **VIA/VIAL:** Unknown / Unknown
- **License:** MIT
- **Revision:** 758419c (2020-08-22)

**Available Files:**
- ✅ KiCad design files
- ✅ BOM
- ✅ Build guide
- ✅ DXF drawings
- ❌ Gerber files (available in original repo)
- ❌ 3D models

**Special Features:**
- Original inspiration for many through-hole designs
- Visible component aesthetic
- VUSB implementation

**Tags:** `ortholinear`, `macropad`, `tht-dip`, `atmega328p`, `vusb`, `qmk`

---

### Tartan
**60% Through-Hole Design**

- **Repository:** https://github.com/hsgw/tartan
- **Layout:** 60%
- **Form Factor:** Standard 60%
- **MCU:** ATmega328P (through-hole DIP-28)
- **USB:** USB Mini/Micro
- **Firmware:** QMK
- **VIA/VIAL:** Unknown / Unknown
- **License:** MIT
- **Revision:** f863f6b (2020-12-05)

**Available Files:**
- ✅ KiCad design files
- ✅ BOM
- ✅ Build guide
- ❌ Gerber files (available in original repo)
- ❌ 3D models
- ❌ DXF drawings

**Special Features:**
- Visible component aesthetic
- VUSB implementation

**Tags:** `60%`, `tht-dip`, `atmega328p`, `vusb`, `qmk`

---

### Plaid-Pad
**4x4 Macropad with Encoders and OLED**

- **Repository:** https://github.com/Keycapsss/Plaid-Pad
- **Layout:** 4x4 numpad/macropad
- **Form Factor:** Compact macropad
- **MCU:** ATmega328P with VUSB
- **USB:** USB-C
- **Firmware:** QMK (`keycapsss/plaid_pad`)
- **VIA/VIAL:** Yes (no encoder) / Yes (with encoder)
- **License:** MIT
- **Revision:** df84d16 (2022-06-29)
- **Bootloader:** USBaspLoader

**Available Files:**
- ✅ Build guide
- ✅ 3D models (printable cases)
- ✅ DXF drawings (laser cut files)
- ❌ Gerber files (available in original repo)
- ❌ KiCad design files (available in original repo)
- ❌ BOM (available in original repo)

**Special Features:**
- Up to 4 rotary encoders (Rev2+)
- Encoder positions interchangeable with switches
- OLED display support (Rev3)
- Choc V2 switch support (Rev2.1+)
- VIA support (no encoder)
- VIAL support (with encoder)

**Tags:** `macropad`, `usb-c`, `tht-dip`, `atmega328p`, `encoder`, `oled`, `via-support`, `vial-support`, `choc`, `qmk`

---

### Dumbpad
**4x4 Macropad with Multiple Variants**

- **Repository:** https://github.com/imchipwood/dumbpad
- **Layout:** 4x4 macropad
- **Form Factor:** Compact macropad
- **MCU:** Pro Micro or Teensy 2.0
- **USB:** USB-C (via Pro Micro)
- **Firmware:** QMK
- **VIA/VIAL:** Yes / Unknown
- **License:** GPL-2.0
- **Revision:** 091f4eb (2024-06-19)
- **PCB Dimensions:** 97mm × 78.5mm with chamfered corners
- **Mounting:** Four 2mm holes in 40mm square pattern

**Available Files:**
- ✅ Gerber files (PCB + Plate)
- ✅ Eagle/KiCad design files (multiple versions)
- ✅ Build guide
- ✅ 3D models (printable cases)
- ❌ BOM (available in original repo)
- ❌ DXF drawings

**Key Components:**
- 16× switches
- 17× 1N4148 diodes
- Pro Micro or Teensy 2.0
- Optional rotary encoders
- Optional OLED display

**Variants:**
- **combo:** Up to 2 rotary encoders, 3 status LEDs
- **combo_oled:** OLED display instead of LEDs
- **combo_teensy:** Teensy 2.0 version
- **reversible:** Single encoder, reversible sockets
- **hotswap_rgb:** Per-key RGB, hotswap sockets

**Special Features:**
- Multiple PCB variants
- Hotswap socket support
- Per-key RGB option
- 3D printable cases
- VIA support

**Tags:** `macropad`, `usb-c`, `pro-micro`, `encoder`, `oled`, `hotswap`, `led`, `via-support`, `qmk`

---

### GH60
**Reference Design for 60% Specifications**

- **Repository:** https://github.com/komar007/gh60
- **Layout:** 60% (61 keys)
- **Form Factor:** Standard 60%
- **Purpose:** Reference for standard 60% PCB dimensions
- **License:** Unknown
- **Revision:** e7948cf (2019-07-02)

**Available Files:**
- ✅ KiCad design files
- ✅ BOM
- ✅ Build guide
- ❌ Gerber files (available in original repo)
- ❌ 3D models
- ❌ DXF drawings

**Key Dimensions:**
- PCB: 285mm × 94.6mm × 1.6mm
- Mounting holes: 6 positions (M2 screws)
- USB cutout: 16mm wide, centered at 142.5mm

**Special Features:**
- Industry-standard 60% dimensions
- Reference for case compatibility
- Mounting hole specifications

**Tags:** `reference`, `60%`, `specifications`, `dimensions`

---

## File Availability Matrix

| Project | Gerbers | Design Files | BOM | Build Guide | 3D Models | DXF/CAD |
|---------|---------|--------------|-----|-------------|-----------|---------|
| Discipline | ✅ | ✅ KiCad | ❌ | ✅ | ✅ | ✅ |
| Mysterium | ✅ | ✅ KiCad | ❌ | ✅ | ❌ | ✅ |
| Lumberjack | ✅ | ✅ KiCad | ✅ | ✅ | ✅ | ✅ |
| Rosaline | ✅ | ✅ KiCad | ❌ | ✅ | ❌ | ✅ |
| Litl | ✅ | ✅ KiCad | ❌ | ✅ | ✅ | ✅ |
| KBIC65 | ✅ | ✅ KiCad | ❌ | ✅ | ✅ | ✅ |
| Plaid | ❌ | ✅ KiCad | ✅ | ✅ | ❌ | ✅ |
| Tartan | ❌ | ✅ KiCad | ✅ | ✅ | ❌ | ❌ |
| Plaid-Pad | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Dumbpad | ✅ | ✅ Eagle/KiCad | ❌ | ✅ | ✅ | ❌ |
| GH60 | ❌ | ✅ KiCad | ✅ | ✅ | ❌ | ❌ |

**Note:** ❌ indicates files are available in original repository but not yet included in this library.

---

## Component Compatibility

### Microcontroller Families
- **ATmega328P Projects:** Lumberjack, Rosaline, Plaid, Tartan, Plaid-Pad
- **ATmega32A Projects:** Discipline, Mysterium
- **Pro Micro Projects:** Litl, KBIC65, Dumbpad

### Switch Compatibility
- **MX Only:** Most projects
- **MX/Alps/Choc:** Lumberjack (earlier revisions)
- **Choc V2:** Plaid-Pad (Rev2.1+)
- **Hotswap:** Dumbpad (hotswap_rgb variant)

### Case Compatibility
- **60% Case Compatible:** Lumberjack, Rosaline
- **Custom Cases:** Discipline, Mysterium, Litl, KBIC65, Plaid-Pad, Dumbpad

---

## Beginner-Friendly Projects

Recommended for first-time through-hole keyboard builders:

1. **Plaid-Pad** - Small, simple, great introduction
2. **Dumbpad** - Well-documented, multiple variants
3. **Lumberjack** - Good documentation, VIA support, 60% case compatible
4. **Discipline** - Popular, well-supported, beautiful design

---

## Advanced Projects

For experienced builders:

1. **KBIC65** - Wireless support, PCB art, advanced features
2. **Mysterium** - Large TKL layout, complex assembly
3. **Litl** - Multiple optional features, compact design

---

## License Summary

### Open Source (Commercial Use Allowed)
- **MIT:** Lumberjack, Rosaline, KBIC65, Plaid, Tartan, Plaid-Pad
- **GPL-2.0:** Dumbpad
- **GPL-3.0:** Mysterium

### Personal Use Only
- **CC BY-NC 4.0:** Discipline (kits by CFTKB.com), Litl (kits by sthlmkb.com)

### Unknown
- **GH60:** License not specified

**Important:** Always check the original repository for the most current license information and respect the creator's terms.

---

## Contributing to This Catalog

To suggest additions or corrections:

1. Verify project uses through-hole components
2. Confirm open-source license
3. Check that design files are publicly available
4. Submit issue or pull request with project information

---

## Additional Resources

- **Master BOM:** `PCB/boms/master-bom.csv`
- **Repository Inventory:** `PCB/docs/repository_inventory.md`
- **Design Patterns:** `PCB/docs/design_patterns.md`
- **GH60 Specifications:** `PCB/docs/gh60_pcb_specifications.md`
- **Manufacturing Guide:** `PCB/docs/manufacturing_guide.md`
- **Component Sourcing:** `PCB/docs/component_sourcing_guide.md`

---

**Catalog Maintained By:** Through-Hole Keyboard Library Project  
**Contributions Welcome:** See original repositories for project-specific questions
