# Through-Hole Keyboard PCB Library

A curated collection of 11 open-source through-hole mechanical keyboard PCB designs. All designs are manufacturing-ready with complete documentation, BOMs, and firmware support.

## Overview

This library contains proven PCB designs for various keyboard form factors, all using through-hole components for easy assembly and aesthetic appeal.

## Available Designs

### 60% Keyboards
- **Discipline** - ATmega32A, USB-C, QMK/VIA
- **Mysterium** - ATmega328P, USB-C, QMK/VIA
- **Lumberjack** - ATmega328P, ortholinear

### 65% Keyboards
- **KBD67 Lite** - Through-hole variant

### 40% Keyboards
- **Plaid** - ATmega328P, minimal design
- **Litl** - Pro Micro, compact

### Numpads
- **Discipline Numpad** - Standalone numpad
- **Plaid Numpad** - Minimal numpad

### Macropads
- **9-Key Macropad** - 3x3 grid
- **12-Key Macropad** - 3x4 grid
- **16-Key Macropad** - 4x4 grid

## Directory Structure

```
pcb-library/
├── design-files/          # KiCad source files
│   ├── discipline/
│   ├── mysterium/
│   └── ...
│
├── gerbers/               # Manufacturing files
│   ├── discipline/
│   └── ...
│
├── boms/                  # Bills of materials
│   ├── master-bom.csv    # Consolidated BOM
│   └── individual/
│
├── firmware/              # QMK firmware configs
│   ├── discipline/
│   └── ...
│
├── docs/                  # Documentation
│   ├── build-guides/
│   ├── compatible_pcbs.md
│   └── gh60_pcb_specifications.md
│
├── 3d-models/             # 3D models (STEP, STL)
├── templates/             # Circuit templates
└── scripts/               # Utility scripts
```

## Quick Start

### Browse Designs
```bash
cat PROJECT_CATALOG.md
```

### View a Design
```bash
# Open in KiCad
kicad design-files/discipline/discipline.kicad_pro
```

### Order PCBs
```bash
# Gerbers are ready to upload to:
# - JLCPCB
# - PCBWay
# - OSH Park
# - etc.

# Find gerbers in: gerbers/[project-name]/
```

## Features

### All Designs Include
- ✅ Complete KiCad schematics
- ✅ Manufacturing-ready Gerbers
- ✅ Detailed BOMs with part numbers
- ✅ QMK firmware support
- ✅ Build guides
- ✅ 3D models

### Common Specifications
- **Components:** Through-hole only
- **MCUs:** ATmega328P, ATmega32A, Pro Micro
- **USB:** USB-C, Mini, Micro (through-hole)
- **Firmware:** QMK, VIA, VIAL support
- **Diodes:** 1N4148 through-hole
- **Switches:** Cherry MX compatible

## Documentation

### Library Documentation
- **Project Catalog:** [PROJECT_CATALOG.md](PROJECT_CATALOG.md)
- **File Index:** [FILE_INDEX.md](FILE_INDEX.md)
- **Project Status:** [PROJECT_STATUS.md](PROJECT_STATUS.md)
- **Component Reference:** [components.md](components.md)
- **References:** [references.md](references.md)
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

### PCB Design Guides
- **📘 PCB Design Guide:** [docs/PCB_DESIGN_GUIDE.md](docs/PCB_DESIGN_GUIDE.md) - Comprehensive wired keyboard PCB design
- **📻 Wireless PCB Guide:** [docs/WIRELESS_PCB_DESIGN.md](docs/WIRELESS_PCB_DESIGN.md) - nRF52840/ZMK wireless design
- **✅ Design Checklist:** [docs/PCB_DESIGN_CHECKLIST.md](docs/PCB_DESIGN_CHECKLIST.md) - Step-by-step checklist
- **🔌 Schematic Patterns:** [docs/SCHEMATIC_PATTERNS.md](docs/SCHEMATIC_PATTERNS.md) - Actual circuit examples from library projects

## Using These Designs

### For Building
1. Choose a design from PROJECT_CATALOG.md
2. Download Gerbers from gerbers/[project]/
3. Order PCBs from your preferred manufacturer
4. Follow build guide in docs/build-guides/
5. Flash firmware from firmware/[project]/

### For Modification
1. Open design-files/[project]/ in KiCad
2. Modify as needed
3. Export new Gerbers
4. Update BOM if components changed

### For Reference
- Use as templates for new designs
- Extract circuit blocks (see templates/)
- Study proven implementations

## Component Sourcing

See [boms/master-bom.csv](boms/master-bom.csv) for:
- Consolidated component list
- Vendor part numbers (Mouser, Digikey)
- Pricing information
- Alternative parts

## Firmware

All designs support QMK firmware. Pre-configured firmware available in firmware/ directory.

### Flash Firmware
```bash
# Using QMK CLI
qmk flash -kb [keyboard] -km default

# Or use QMK Toolbox (GUI)
```

## Manufacturing Notes

- **PCB Thickness:** 1.6mm standard
- **Copper Weight:** 1oz (35μm)
- **Surface Finish:** HASL or ENIG
- **Solder Mask:** Any color
- **Silkscreen:** White recommended

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Adding new designs
- Improving documentation
- Reporting issues
- Submitting corrections

## License

Each design has its own license. See individual project directories for details. Most are open-source (MIT, GPL, CC-BY-SA).

## Credits

These designs are from the open-source keyboard community. Original designers are credited in each project directory.

---

**Need Help?**
- Build issues? Check docs/build-guides/
- Component questions? See components.md
- PCB compatibility? See docs/compatible_pcbs.md
