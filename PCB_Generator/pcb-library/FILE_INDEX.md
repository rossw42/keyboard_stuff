# Through-Hole Keyboard Library - File Type Index

**Library Version:** 1.0.0  
**Last Updated:** 2025-10-20

This document provides quick reference indexes for all file types in the library, organized by category.

---

## Table of Contents

1. [Gerber Files Index](#gerber-files-index)
2. [Design Files Index](#design-files-index)
3. [3D Model Files Index](#3d-model-files-index)
4. [CAD Drawing Files Index](#cad-drawing-files-index)
5. [Documentation Index](#documentation-index)
6. [BOM Files Index](#bom-files-index)
7. [Firmware Files Index](#firmware-files-index)

---

## Gerber Files Index

Manufacturing-ready Gerber files for PCB fabrication.

### PCB Gerbers

| Project | Path | Notes |
|---------|------|-------|
| Discipline | `gerbers/discipline/pcb/` | 65% PCB, 2-layer |
| Mysterium | `gerbers/mysterium/pcb/` | TKL PCB, 2-layer |
| Lumberjack | `gerbers/lumberjack/pcb/` | 60% ortho PCB, 2-layer |
| Rosaline | `gerbers/rosaline/pcb/` | 40% PCB, 2-layer |
| Litl | `gerbers/litl/pcb/` | 40% PCB, 2-layer |
| KBIC65 | `gerbers/kbic65/pcb/` | 65% PCB, 2-layer |
| Plaid | `gerbers/plaid/pcb/` | 4x12 ortho PCB, 2-layer |
| Tartan | `gerbers/tartan/pcb/` | 60% PCB, 2-layer |
| Plaid-Pad | `gerbers/plaid-pad/pcb/` | 4x4 macropad PCB, 2-layer |
| Dumbpad | `gerbers/dumbpad/pcb/` | 4x4 macropad PCB, 2-layer |
| GH60 | `gerbers/gh60/pcb/` | 60% reference PCB, 2-layer |

### Plate Gerbers (FR4)

| Project | Path | Notes |
|---------|------|-------|
| Discipline | `gerbers/discipline/plate/` | 65% switch plate |
| Mysterium | `gerbers/mysterium/plate/` | TKL switch plate |
| Lumberjack | `gerbers/lumberjack/plate/` | 60% ortho switch plate |
| Rosaline | `gerbers/rosaline/plate/` | 40% switch plate |
| Litl | `gerbers/litl/plate/` | 40% switch plate |
| KBIC65 | `gerbers/kbic65/plate/` | 65% switch plate |
| Plaid | `gerbers/plaid/plate/` | 4x12 ortho switch plate |
| Tartan | `gerbers/tartan/plate/` | 60% switch plate |
| Plaid-Pad | `gerbers/plaid-pad/plate/` | 4x4 macropad switch plate |
| Dumbpad | `gerbers/dumbpad/plate/` | 4x4 macropad switch plate |
| GH60 | `gerbers/gh60/plate/` | 60% reference switch plate |

### Gerber File Contents

Each Gerber directory typically contains:
- `*.GTL` - Top copper layer
- `*.GBL` - Bottom copper layer
- `*.GTS` - Top soldermask
- `*.GBS` - Bottom soldermask
- `*.GTO` - Top silkscreen
- `*.GBO` - Bottom silkscreen
- `*.GKO` / `*.GM1` - Board outline
- `*.TXT` - Drill file

### Manufacturing Specifications

**Standard PCB Specs:**
- Layers: 2
- Thickness: 1.6mm
- Material: FR4
- Surface Finish: HASL or ENIG
- Min Trace/Space: 6/6 mil (0.15mm)
- Min Drill: 0.3mm

**Standard Plate Specs:**
- Layers: 2
- Thickness: 1.5mm
- Material: FR4
- Surface Finish: HASL
- Min Trace/Space: N/A (no traces)

---

## Design Files Index

Native design files for modification and study.

### KiCad Projects

| Project | Path | Version | Files |
|---------|------|---------|-------|
| Discipline | `design-files/discipline/kicad/` | KiCad 5.x | .kicad_pcb, .sch, .pro |
| Mysterium | `design-files/mysterium/kicad/` | KiCad 5.x | .kicad_pcb, .sch, .pro |
| Lumberjack | `design-files/lumberjack/kicad/` | KiCad 6.x | .kicad_pcb, .kicad_sch, .kicad_pro |
| Rosaline | `design-files/rosaline/kicad/` | KiCad 6.x | .kicad_pcb, .kicad_sch, .kicad_pro |
| Litl | `design-files/litl/kicad/` | KiCad 6.x | .kicad_pcb, .kicad_sch, .kicad_pro |
| KBIC65 | `design-files/kbic65/kicad/` | KiCad 6.x | .kicad_pcb, .kicad_sch, .kicad_pro |
| Plaid | `design-files/plaid/kicad/` | KiCad 5.x | .kicad_pcb, .sch, .pro |
| Tartan | `design-files/tartan/kicad/` | KiCad 5.x | .kicad_pcb, .sch, .pro |
| Plaid-Pad | `design-files/plaid-pad/kicad/` | KiCad 5.x | .kicad_pcb, .sch, .pro |
| Dumbpad | `design-files/dumbpad/kicad/` | KiCad 6.x | .kicad_pcb, .kicad_sch, .kicad_pro |
| GH60 | `design-files/gh60/kicad/` | KiCad 5.x | .kicad_pcb, .sch, .pro |

### Eagle Projects

| Project | Path | Version | Files |
|---------|------|---------|-------|
| Dumbpad | `design-files/dumbpad/eagle/` | Eagle 9.x | .brd, .sch |

### Custom Libraries

| Project | Path | Contents |
|---------|------|----------|
| Discipline | `design-files/discipline/libraries/` | Custom footprints, symbols |
| Mysterium | `design-files/mysterium/libraries/` | Custom footprints, symbols |
| Lumberjack | `design-files/lumberjack/libraries/` | Custom footprints, symbols |
| Rosaline | `design-files/rosaline/libraries/` | Custom footprints, symbols |
| Litl | `design-files/litl/libraries/` | Custom footprints, symbols |
| KBIC65 | `design-files/kbic65/libraries/` | Custom footprints, symbols |
| Plaid | `design-files/plaid/libraries/` | Custom footprints, symbols |
| Tartan | `design-files/tartan/libraries/` | Custom footprints, symbols |
| Plaid-Pad | `design-files/plaid-pad/libraries/` | Custom footprints, symbols |
| Dumbpad | `design-files/dumbpad/libraries/` | Custom footprints, symbols |
| GH60 | `design-files/gh60/libraries/` | Custom footprints, symbols |

### Design File Usage

**To Open KiCad Projects:**
1. Install KiCad (version 5.x or 6.x as noted)
2. Open `.kicad_pro` (v6) or `.pro` (v5) file
3. Libraries are included in project directories

**To Open Eagle Projects:**
1. Install Autodesk Eagle (or use KiCad import)
2. Open `.brd` for PCB layout
3. Open `.sch` for schematic

---

## 3D Model Files Index

STL and STEP files for 3D printing and CAD.

### Cases

| Project | Path | Format | Description |
|---------|------|--------|-------------|
| Discipline | `3d-models/cases/discipline/` | STL | High-profile acrylic case |
| Mysterium | `3d-models/cases/mysterium/` | STL | TKL case options |
| Lumberjack | `3d-models/cases/lumberjack/` | STL | 60% compatible case |
| Rosaline | `3d-models/cases/rosaline/` | STL | 40% case |
| Litl | `3d-models/cases/litl/` | STL | Compact 40% case |
| KBIC65 | `3d-models/cases/kbic65/` | STL | 65% case with art |
| Plaid | `3d-models/cases/plaid/` | STL | Ortho case |
| Tartan | `3d-models/cases/tartan/` | STL | 60% case |
| Plaid-Pad | `3d-models/cases/plaid-pad/` | STL | Macropad case |
| Dumbpad | `3d-models/cases/dumbpad/` | STL | Multiple case variants |
| GH60 | `3d-models/cases/gh60/` | STL | Reference case |

### Plates

| Project | Path | Format | Description |
|---------|------|--------|-------------|
| Discipline | `3d-models/plates/discipline/` | STL, STEP | 65% switch plate |
| Mysterium | `3d-models/plates/mysterium/` | STL, STEP | TKL switch plate |
| Lumberjack | `3d-models/plates/lumberjack/` | STL, STEP | 60% ortho switch plate |
| Rosaline | `3d-models/plates/rosaline/` | STL, STEP | 40% switch plate |
| Litl | `3d-models/plates/litl/` | STL, STEP | 40% switch plate |
| KBIC65 | `3d-models/plates/kbic65/` | STL, STEP | 65% switch plate |
| Plaid | `3d-models/plates/plaid/` | STL, STEP | 4x12 ortho switch plate |
| Tartan | `3d-models/plates/tartan/` | STL, STEP | 60% switch plate |
| Plaid-Pad | `3d-models/plates/plaid-pad/` | STL, STEP | 4x4 macropad switch plate |
| Dumbpad | `3d-models/plates/dumbpad/` | STL, STEP | 4x4 macropad switch plate |
| GH60 | `3d-models/plates/gh60/` | STL, STEP | 60% reference switch plate |

### Accessories

| Item | Path | Format | Description |
|------|------|--------|-------------|
| Component Cradles | `3d-models/accessories/component-cradles/` | STL | Lumberjack component holders |
| Component Covers | `3d-models/accessories/covers/` | STL | Acrylic component guards |

### 3D Printing Guidelines

**Recommended Settings:**
- Layer Height: 0.2mm
- Infill: 20-30%
- Supports: As needed for overhangs
- Material: PLA or PETG

**Case Printing:**
- Print orientation: Bottom face down
- Support: Enable for screw posts
- Post-processing: Sand and finish as desired

---

## CAD Drawing Files Index

DXF and SVG files for laser cutting and CNC.

### Plate DXF Files

| Project | Path | Material | Thickness |
|---------|------|----------|-----------|
| Discipline | `cad-drawings/plates/discipline/` | Acrylic, FR4, Metal | 1.5mm |
| Mysterium | `cad-drawings/plates/mysterium/` | Acrylic, FR4, Metal | 1.5mm |
| Lumberjack | `cad-drawings/plates/lumberjack/` | Acrylic, FR4, Metal | 1.5mm |
| Rosaline | `cad-drawings/plates/rosaline/` | Acrylic, FR4, Metal | 1.5mm |
| Litl | `cad-drawings/plates/litl/` | Acrylic, FR4, Metal | 1.5mm |
| KBIC65 | `cad-drawings/plates/kbic65/` | Acrylic, FR4, Metal | 1.5mm |
| Plaid | `cad-drawings/plates/plaid/` | Acrylic, FR4, Metal | 1.5mm |
| Tartan | `cad-drawings/plates/tartan/` | Acrylic, FR4, Metal | 1.5mm |
| Plaid-Pad | `cad-drawings/plates/plaid-pad/` | Acrylic, FR4, Metal | 1.5mm |
| Dumbpad | `cad-drawings/plates/dumbpad/` | Acrylic, FR4, Metal | 1.5mm |
| GH60 | `cad-drawings/plates/gh60/` | Acrylic, FR4, Metal | 1.5mm |

### Case DXF Files

| Project | Path | Material | Thickness |
|---------|------|----------|-----------|
| Discipline | `cad-drawings/cases/discipline/` | Acrylic | 3-5mm |
| Mysterium | `cad-drawings/cases/mysterium/` | Acrylic | 3-5mm |
| Lumberjack | `cad-drawings/cases/lumberjack/` | Acrylic | 3-5mm |
| Rosaline | `cad-drawings/cases/rosaline/` | Acrylic | 3-5mm |
| Litl | `cad-drawings/cases/litl/` | Acrylic | 3-5mm |
| KBIC65 | `cad-drawings/cases/kbic65/` | Acrylic | 3-5mm |
| Plaid | `cad-drawings/cases/plaid/` | Acrylic | 3-5mm |
| Tartan | `cad-drawings/cases/tartan/` | Acrylic | 3-5mm |
| Plaid-Pad | `cad-drawings/cases/plaid-pad/` | Acrylic | 3-5mm |
| Dumbpad | `cad-drawings/cases/dumbpad/` | Acrylic | 3-5mm |
| GH60 | `cad-drawings/cases/gh60/` | Acrylic | 3-5mm |

### Cover DXF Files

| Project | Path | Material | Thickness |
|---------|------|----------|-----------|
| Lumberjack | `cad-drawings/covers/lumberjack-cover.dxf` | Acrylic | 3mm |
| Mysterium | `cad-drawings/covers/mysterium-guard.dxf` | Acrylic | 3mm |

### SVG Files

| Project | Path | Description |
|---------|------|-------------|
| KBIC65 | `cad-drawings/kbic65/` | PCB art, bottom plate, switch plate, acrylic window |

### Laser Cutting Guidelines

**Recommended Settings (Acrylic):**
- Speed: 10-20 mm/s
- Power: 80-100% (depends on laser)
- Passes: 1-2
- Focus: On material surface

**Material Options:**
- Acrylic: Clear, frosted, colored
- FR4: For plates (order as PCB)
- Metal: Aluminum, brass, stainless steel

---

## Documentation Index

Build guides, specifications, and reference documents.

### Build Guides

| Project | Path | Language | Format |
|---------|------|----------|--------|
| Discipline | `docs/build-guides/discipline/` | English | Markdown, PDF |
| Mysterium | `docs/build-guides/mysterium/` | English | Markdown, PDF |
| Lumberjack | `docs/build-guides/lumberjack/` | English | Markdown |
| Rosaline | `docs/build-guides/rosaline/` | English | Markdown |
| Litl | `docs/build-guides/litl/` | English | Markdown |
| KBIC65 | `docs/build-guides/kbic65/` | English | Markdown |
| Plaid | `docs/build-guides/plaid/` | English | Markdown |
| Tartan | `docs/build-guides/tartan/` | English | Markdown |
| Plaid-Pad | `docs/build-guides/plaid-pad/` | English, German | Markdown |
| Dumbpad | `docs/build-guides/dumbpad/` | English | Markdown |
| GH60 | `docs/build-guides/gh60/` | English | Markdown |

### Technical Documentation

| Document | Path | Description |
|----------|------|-------------|
| Repository Inventory | `docs/repository_inventory.md` | Complete project catalog with metadata |
| GH60 Specifications | `docs/gh60_pcb_specifications.md` | Standard 60% PCB dimensions and specs |
| Compatible PCBs | `docs/compatible_pcbs.md` | PCB compatibility reference |
| Manufacturing Guide | `docs/manufacturing_guide.md` | PCB ordering and fabrication guide |
| Component Sourcing | `docs/component_sourcing_guide.md` | Vendor recommendations and part numbers |
| Design Patterns | `docs/design_patterns.md` | Common circuit implementations |
| Schematic Patterns | `docs/SCHEMATIC_PATTERNS.md` | Detailed circuit examples with component values |
| PCB Design Guide | `docs/PCB_DESIGN_GUIDE.md` | Comprehensive wired keyboard PCB design |
| Wireless PCB Design | `docs/WIRELESS_PCB_DESIGN.md` | nRF52840/ZMK wireless design guide |
| PCB Design Checklist | `docs/PCB_DESIGN_CHECKLIST.md` | Step-by-step design checklist |

### Library Documentation

| Document | Path | Description |
|----------|------|-------------|
| Main README | `README.md` | Library overview and quick start |
| Project Catalog | `PROJECT_CATALOG.md` | Searchable project database |
| File Index | `FILE_INDEX.md` | This document |
| Component Reference | `components.md` | Component specifications and datasheets |
| External References | `references.md` | Links to external resources |

---

## BOM Files Index

Bill of materials for component ordering.

### Project BOMs

| Project | Path | Format | Status |
|---------|------|--------|--------|
| Discipline | `boms/discipline/bom.csv` | CSV | Available in original repo |
| Mysterium | `boms/mysterium/bom.csv` | CSV | Available in original repo |
| Lumberjack | `boms/lumberjack/bom.csv` | CSV | ✅ Included |
| Rosaline | `boms/rosaline/bom.csv` | CSV | Available in original repo |
| Litl | `boms/litl/bom.csv` | CSV | Available in original repo |
| KBIC65 | `boms/kbic65/bom.csv` | CSV | Available in original repo |
| Plaid | `boms/plaid/bom.csv` | CSV | ✅ Included |
| Tartan | `boms/tartan/bom.csv` | CSV | ✅ Included |
| Plaid-Pad | `boms/plaid-pad/bom.csv` | CSV | Available in original repo |
| Dumbpad | `boms/dumbpad/bom.csv` | CSV | Available in original repo |
| GH60 | `boms/gh60/bom.csv` | CSV | ✅ Included |

### Master BOM

| File | Path | Description |
|------|------|-------------|
| Master BOM | `boms/master-bom.csv` | Unified component database across all projects |

### BOM Fields

Standard BOM fields include:
- Component
- Value
- Footprint
- Package
- Vendor Part Number
- Category
- Min/Max Quantity
- Projects Using
- Notes

---

## Firmware Files Index

QMK configurations and flashing guides.

### QMK Configurations

| Project | Path | QMK Path | VIA | VIAL |
|---------|------|----------|-----|------|
| Discipline | `firmware/qmk-configs/discipline/` | `coseyfannitutti/discipline` | ❓ | ❓ |
| Mysterium | `firmware/qmk-configs/mysterium/` | `coseyfannitutti/mysterium` | ❓ | ❓ |
| Lumberjack | `firmware/qmk-configs/lumberjack/` | `peej/lumberjack` | ✅ | ❓ |
| Rosaline | `firmware/qmk-configs/rosaline/` | `peej/rosaline` | ❓ | ❓ |
| Litl | `firmware/qmk-configs/litl/` | `mohoyt/litl` | ✅ | ✅ |
| KBIC65 | `firmware/qmk-configs/kbic65/` | `b-karl/kbic65` | ✅ | ❓ |
| Plaid | `firmware/qmk-configs/plaid/` | `hsgw/plaid` | ❓ | ❓ |
| Tartan | `firmware/qmk-configs/tartan/` | `hsgw/tartan` | ❓ | ❓ |
| Plaid-Pad | `firmware/qmk-configs/plaid-pad/` | `keycapsss/plaid_pad` | ✅ | ✅ |
| Dumbpad | `firmware/qmk-configs/dumbpad/` | `imchipwood/dumbpad` | ✅ | ❓ |

### ZMK Configurations

| Project | Path | Description |
|---------|------|-------------|
| KBIC65 | `firmware/zmk-configs/kbic65/` | Wireless configuration for nice!nano |

### Flashing Guides

| MCU Type | Path | Bootloader | Method |
|----------|------|------------|--------|
| ATmega328P | `firmware/flashing-guides/atmega328p/` | USBaspLoader | USBasp, Arduino as ISP |
| ATmega32A | `firmware/flashing-guides/atmega32a/` | Bootloader | USBasp, Arduino as ISP |
| Pro Micro | `firmware/flashing-guides/pro-micro/` | Caterina | QMK Toolbox, avrdude |
| Elite-C | `firmware/flashing-guides/elite-c/` | DFU | QMK Toolbox, dfu-programmer |
| nice!nano | `firmware/flashing-guides/nice-nano/` | UF2 | Drag-and-drop UF2 file |

### Firmware Resources

| Document | Path | Description |
|----------|------|-------------|
| QMK Setup Guide | `firmware/qmk-setup-guide.md` | Installing and configuring QMK |
| VIA Guide | `firmware/via-guide.md` | Using VIA for keymap configuration |
| VIAL Guide | `firmware/vial-guide.md` | Using VIAL for advanced features |
| ZMK Setup Guide | `firmware/zmk-setup-guide.md` | Wireless keyboard configuration |

---

## File Format Reference

### Common File Extensions

**PCB Design:**
- `.kicad_pcb` - KiCad PCB layout (v6+)
- `.kicad_sch` - KiCad schematic (v6+)
- `.kicad_pro` - KiCad project file (v6+)
- `.sch` - KiCad schematic (v5) or Eagle schematic
- `.brd` - Eagle PCB layout
- `.pro` - KiCad project file (v5)

**Manufacturing:**
- `.GTL` - Gerber top copper
- `.GBL` - Gerber bottom copper
- `.GTS` - Gerber top soldermask
- `.GBS` - Gerber bottom soldermask
- `.GTO` - Gerber top silkscreen
- `.GBO` - Gerber bottom silkscreen
- `.GKO` / `.GM1` - Gerber board outline
- `.TXT` - Drill file

**3D Models:**
- `.STL` - Stereolithography (3D printing)
- `.STEP` / `.STP` - Standard for Exchange of Product Data (CAD)
- `.OBJ` - Wavefront object (3D modeling)

**CAD Drawings:**
- `.DXF` - Drawing Exchange Format (AutoCAD)
- `.SVG` - Scalable Vector Graphics
- `.DWG` - AutoCAD drawing

**Documentation:**
- `.MD` - Markdown
- `.PDF` - Portable Document Format
- `.CSV` - Comma-Separated Values (BOMs)

---

## Quick Access Paths

### For Builders

**Order PCBs:**
```
PCB/gerbers/[project-name]/pcb/
```

**Get Components:**
```
PCB/boms/[project-name]/bom.csv
PCB/boms/master-bom.csv
```

**Build Instructions:**
```
PCB/docs/build-guides/[project-name]/
```

**Flash Firmware:**
```
PCB/firmware/flashing-guides/[mcu-type]/
```

### For Designers

**Study Designs:**
```
PCB/design-files/[project-name]/kicad/
PCB/design-files/[project-name]/eagle/
```

**Reference Specifications:**
```
PCB/docs/gh60_pcb_specifications.md
PCB/docs/design_patterns.md
```

**Custom Cases:**
```
PCB/3d-models/cases/[project-name]/
PCB/cad-drawings/cases/[project-name]/
```

---

## File Organization Standards

### Directory Naming
- Lowercase with hyphens: `plaid-pad`, `kbic65`
- Consistent across all file types
- Matches project name in catalog

### File Naming
- Descriptive names: `discipline-pcb-gerbers.zip`
- Version numbers when applicable: `lumberjack-v1.8.zip`
- Format suffix: `mysterium-plate.dxf`

### Archive Standards
- Gerbers: ZIP format
- Design files: Native format + ZIP backup
- Documentation: Markdown preferred, PDF for complex layouts

---

## Maintenance Notes

### File Status Legend
- ✅ Included in library
- ❌ Available in original repository only
- ❓ Status unknown or varies

### Update Procedures
1. Check original repositories for updates
2. Download new files
3. Verify file integrity
4. Update indexes
5. Update version numbers

### Version Control
- Track file versions in project metadata
- Note significant changes in documentation
- Maintain changelog for major updates

---

**Index Maintained By:** Through-Hole Keyboard Library Project  
**For Missing Files:** Check original project repositories linked in PROJECT_CATALOG.md
