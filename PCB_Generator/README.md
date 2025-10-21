# Through-Hole Keyboard Project

A comprehensive collection of tools and resources for designing, building, and manufacturing through-hole mechanical keyboards.

## Project Structure

### 🎹 [keyboard-generator/](keyboard-generator/)
**Through-Hole Keyboard Generator (THKG)** - Automated design tool for generating keyboard plates, PCBs, cases, and firmware.

- **Status:** Phase 1 (Plate Generation) COMPLETE ✅
- **Features:** YAML/KLE input, 14 layout presets, DXF export
- **Quick Start:** See [keyboard-generator/START_HERE.md](keyboard-generator/START_HERE.md)

### 🏗️ [case-generator/](case-generator/)
**CNC Case Generator** - Parametric case design tool for GH60-compatible keyboards.

- **Status:** Operational
- **Features:** Top frame & bottom tray generation, toolpath export, 3D models
- **Profiles:** Standard and low-profile designs

### 📚 [pcb-library/](pcb-library/)
**PCB Design Library** - Collection of 11 through-hole keyboard PCB designs.

- **Designs:** 60%, 65%, 40%, numpads, macropads
- **Files:** KiCad schematics, Gerbers, BOMs, firmware
- **Documentation:** Build guides, component sourcing

### 📖 [.kiro/specs/](.kiro/specs/)
**Project Specifications** - Design documents and implementation plans.

- Keyboard generator specifications
- Requirements and design documents
- Task tracking and status

### 📦 [archive/](archive/)
**Archive** - Historical documents and references.

## Quick Start

### Generate a Keyboard Plate
```bash
cd keyboard-generator
pip install -e .
thkg generate examples/macropad-3x3.yaml
```

### Generate a CNC Case
```bash
cd case-generator
pip install -r requirements.txt
python examples/generate_top_frame.py
```

### Browse PCB Library
```bash
cd pcb-library
cat PROJECT_CATALOG.md
```

## Tools Overview

| Tool | Purpose | Status | Output |
|------|---------|--------|--------|
| **THKG** | Automated keyboard design | Phase 1 ✅ | Plates (DXF) |
| **Case Generator** | CNC case design | Operational | STL, DXF, G-code |
| **PCB Library** | Reference designs | Complete | Gerbers, BOMs |

## Documentation

- **Keyboard Generator:** [keyboard-generator/README.md](keyboard-generator/README.md)
- **Case Generator:** [case-generator/README.md](case-generator/README.md)  
- **PCB Library:** [pcb-library/README.md](pcb-library/README.md)
- **Specifications:** [.kiro/specs/keyboard-design-automation/](.kiro/specs/keyboard-design-automation/)

## Project Goals

1. **Automation** - Generate complete keyboard designs from high-level specs
2. **Quality** - Use proven circuits and manufacturing-ready outputs
3. **Accessibility** - Make through-hole keyboard design accessible to everyone
4. **Art** - Celebrate visible components as design elements

## Contributing

See individual project READMEs for contribution guidelines.

## License

See individual project directories for license information.

---

**Start Here:**
- New to the project? → [keyboard-generator/START_HERE.md](keyboard-generator/START_HERE.md)
- Want to generate a plate? → [keyboard-generator/QUICKSTART.md](keyboard-generator/QUICKSTART.md)
- Need a case? → [case-generator/examples/](case-generator/examples/)
- Looking for PCB designs? → [pcb-library/PROJECT_CATALOG.md](pcb-library/PROJECT_CATALOG.md)
