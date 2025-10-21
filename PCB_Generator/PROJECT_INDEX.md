# Through-Hole Keyboard Project - Complete Index

Quick navigation to all tools, libraries, and documentation.

## 📁 Project Structure

```
/
├── keyboard-generator/      # THKG - Automated keyboard design tool
├── case-generator/          # CNC case design tool
├── pcb-library/            # PCB design library (11 designs)
├── .kiro/                  # Kiro IDE configuration & specs
├── archive/                # Historical documents
└── README.md               # This file
```

---

## 🎹 Keyboard Generator (THKG)

**Location:** `keyboard-generator/`  
**Status:** Phase 1 Complete ✅  
**Purpose:** Automated generation of keyboard plates, PCBs, cases, and firmware

### Quick Links
- **Start Here:** [keyboard-generator/START_HERE.md](keyboard-generator/START_HERE.md)
- **Quick Start:** [keyboard-generator/QUICKSTART.md](keyboard-generator/QUICKSTART.md)
- **Full Docs:** [keyboard-generator/README.md](keyboard-generator/README.md)
- **Complete Report:** [keyboard-generator/FINAL_REPORT.md](keyboard-generator/FINAL_REPORT.md)

### Key Files
- `thkg/` - Main Python package
- `examples/` - Example configurations
- `tests/` - Test suite
- `output/` - Generated files

### Quick Start
```bash
cd keyboard-generator
pip install -e .
thkg generate examples/macropad-3x3.yaml
```

---

## 🏗️ Case Generator

**Location:** `case-generator/`  
**Status:** Operational  
**Purpose:** CNC case design for GH60-compatible keyboards

### Quick Links
- **Main Docs:** [case-generator/README.md](case-generator/README.md)
- **Examples:** [case-generator/examples/](case-generator/examples/)
- **Specifications:** [case-generator/docs/gh60_pcb_specifications.md](case-generator/docs/gh60_pcb_specifications.md)

### Key Files
- `src/` - Source code (geometry, toolpaths, export)
- `examples/` - Generation scripts
- `output/` - Generated STL, DXF, G-code
- `docs/` - Documentation

### Quick Start
```bash
cd case-generator
pip install -r requirements.txt
python examples/generate_top_frame.py
```

---

## 📚 PCB Library

**Location:** `pcb-library/`  
**Status:** ✅ Complete (11 designs, 100% validated)  
**Purpose:** Reference PCB designs for through-hole keyboards

### Quick Links
- **Main Docs:** [pcb-library/README.md](pcb-library/README.md)
- **Project Catalog:** [pcb-library/PROJECT_CATALOG.md](pcb-library/PROJECT_CATALOG.md)
- **File Index:** [pcb-library/FILE_INDEX.md](pcb-library/FILE_INDEX.md)
- **Build Guides:** [pcb-library/docs/build-guides/](pcb-library/docs/build-guides/)

### Key Directories
- `design-files/` - KiCad source files
- `gerbers/` - Manufacturing files
- `boms/` - Bills of materials
- `firmware/` - QMK firmware configs
- `docs/` - Documentation

### Available Designs
- 60%: Discipline, Mysterium, Lumberjack
- 65%: KBD67 Lite
- 40%: Plaid, Litl
- Numpads: Discipline Numpad, Plaid Numpad
- Macropads: 9-key, 12-key, 16-key

---

## 📖 Documentation

### Keyboard Generator Docs
- [START_HERE.md](keyboard-generator/START_HERE.md) - Welcome & overview
- [QUICKSTART.md](keyboard-generator/QUICKSTART.md) - 5-minute guide
- [README.md](keyboard-generator/README.md) - Full documentation
- [FINAL_REPORT.md](keyboard-generator/FINAL_REPORT.md) - Implementation report
- [INDEX.md](keyboard-generator/INDEX.md) - Navigation index

### Case Generator Docs
- [README.md](case-generator/README.md) - Main documentation
- [gh60_pcb_specifications.md](case-generator/docs/gh60_pcb_specifications.md) - PCB specs
- [compatible_pcbs.md](case-generator/docs/compatible_pcbs.md) - Compatible PCBs
- [implementation/](case-generator/docs/implementation/) - Implementation docs
- [manufacturing/](case-generator/docs/manufacturing/) - Manufacturing guides

### PCB Library Docs
- [README.md](pcb-library/README.md) - Library overview
- [PROJECT_CATALOG.md](pcb-library/PROJECT_CATALOG.md) - All designs
- [components.md](pcb-library/components.md) - Component reference
- [CONTRIBUTING.md](pcb-library/CONTRIBUTING.md) - Contribution guide

### Specifications
- [.kiro/specs/keyboard-design-automation/](.kiro/specs/keyboard-design-automation/) - THKG specs
  - [requirements.md](.kiro/specs/keyboard-design-automation/requirements.md)
  - [design.md](.kiro/specs/keyboard-design-automation/design.md)
  - [tasks.md](.kiro/specs/keyboard-design-automation/tasks.md)

---

## 🚀 Quick Start Guides

### Generate a Keyboard Plate
```bash
cd keyboard-generator
pip install -e .
thkg list-presets                      # See available layouts
thkg generate examples/macropad-3x3.yaml  # Generate plate
# Output: keyboard-generator/output/3x3-Macropad/plate.dxf
```

### Generate a CNC Case
```bash
cd case-generator
pip install -r requirements.txt
python examples/generate_all_3d_models.py
# Output: case-generator/output/60_percent_standard/
```

### Use a PCB Design
```bash
cd pcb-library
cat PROJECT_CATALOG.md                 # Browse designs
# Gerbers ready to order: pcb-library/gerbers/[project]/
```

---

## 🔧 Development

### Keyboard Generator
- **Language:** Python 3.8+
- **Dependencies:** pyyaml, click, ezdxf, kle-serial
- **Tests:** `pytest keyboard-generator/tests/`
- **Demo:** `python keyboard-generator/demo.py`

### Case Generator
- **Language:** Python 3.8+
- **Dependencies:** cadquery, ezdxf
- **Tests:** `pytest case-generator/tests/`

### PCB Library
- **Tool:** KiCad 7.0+
- **Firmware:** QMK
- **Format:** Gerber RS-274X

---

## 📊 Project Status

| Component | Status | Phase | Output |
|-----------|--------|-------|--------|
| **Keyboard Generator** | ✅ Complete | Phase 1 | Plates (DXF) |
| **Case Generator** | ✅ Operational | - | STL, DXF, G-code |
| **PCB Library** | ✅ Complete (100%) | - | 11 designs + BOMs |

### Keyboard Generator Roadmap
- ✅ Phase 1: Plate Generation (COMPLETE)
- 🔲 Phase 2: PCB Generation (Ready to start)
- 🔲 Phase 3: Case Generation
- 🔲 Phase 4: Firmware Generation

---

## 📦 File Counts

| Directory | Files | Purpose |
|-----------|-------|---------|
| keyboard-generator/ | 48 | THKG tool |
| case-generator/ | 50+ | CNC case tool |
| pcb-library/ | 200+ | PCB designs |
| .kiro/ | 10+ | IDE config & specs |

---

## 🎯 Common Tasks

### I want to...

**...generate a keyboard plate**
→ [keyboard-generator/QUICKSTART.md](keyboard-generator/QUICKSTART.md)

**...design a CNC case**
→ [case-generator/README.md](case-generator/README.md)

**...build a keyboard from scratch**
→ [pcb-library/PROJECT_CATALOG.md](pcb-library/PROJECT_CATALOG.md)

**...understand the project**
→ [README.md](README.md) (root)

**...contribute**
→ [pcb-library/CONTRIBUTING.md](pcb-library/CONTRIBUTING.md)

**...see specifications**
→ [.kiro/specs/keyboard-design-automation/](.kiro/specs/keyboard-design-automation/)

---

## 🔗 External Links

- **QMK Firmware:** https://qmk.fm/
- **KiCad:** https://www.kicad.org/
- **CadQuery:** https://cadquery.readthedocs.io/
- **Keyboard Layout Editor:** http://www.keyboard-layout-editor.com/

---

## 📝 Notes

- All paths are relative to project root
- Python 3.8+ required for all tools
- KiCad 7.0+ required for PCB work
- See individual READMEs for detailed instructions

---

**Last Updated:** October 20, 2025  
**Project Version:** 1.0  
**Status:** Organized and operational
