# 60% Keyboard Case - CNC Design Project

A parametric design system for manufacturing wooden keyboard cases for 60% mechanical keyboards (GH60, BM60, Pok3r PCBs) via CNC machining.

## Project Structure

```
.
├── src/                    # Source code for CAD generation
│   ├── constants.py        # Dimensional constants and specifications
│   ├── geometry/           # 2D geometry generation modules
│   ├── toolpaths/          # CNC toolpath generation modules
│   └── export/             # Export utilities for CAD formats
├── output/                 # Generated output files
│   ├── drawings/           # 2D technical drawings (PDF, DXF)
│   ├── toolpaths/          # CNC toolpath files (DXF, G-code)
│   ├── models/             # 3D models (STEP)
│   └── documentation/      # Manufacturing documentation
├── docs/                   # Project documentation
│   └── manufacturing/      # Manufacturing guides and procedures
└── tests/                  # Test files for validation
```

## Coordinate System

- **Origin**: Top-left corner of case external profile, top surface
- **X-axis**: Positive to the right (length direction, 0-295mm)
- **Y-axis**: Positive downward (width direction, 0-105mm)
- **Z-axis**: Positive downward (depth into material)

## Key Dimensions

- **Case External**: 295mm × 105mm
- **PCB**: 285mm × 94.6mm × 1.6mm
- **Top Frame Height**: 5mm
- **Bottom Tray Height**: 15mm
- **Cavity Depth**: 8mm

## Requirements

- Python 3.8+
- Required libraries:
  - `ezdxf>=1.0.0` - DXF file generation
  - `reportlab>=4.0.0` - PDF technical drawings
  - `build123d>=0.5.0` - 3D solid modeling and STEP export

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Generate 3D Models

Generate all 3D solid models (top frame, bottom tray, and assembly):

```bash
python examples/generate_all_3d_models.py
```

This will create STEP and STL files in `output/3d_models/`:
- `top_frame.step` / `top_frame.stl` - Top frame component
- `bottom_tray.step` / `bottom_tray.stl` - Bottom tray component
- `assembly.step` / `assembly.stl` - Complete assembly with PCB reference

Individual components can be generated separately:
```bash
python examples/generate_top_frame_3d.py
python examples/generate_bottom_tray_3d.py
python examples/generate_assembly_3d.py
```

**STEP files** can be imported into CAD software (FreeCAD, Fusion 360, SolidWorks, OnShape, etc.)  
**STL files** are provided for quick visualization

### Generate CNC Toolpaths

Generate CNC toolpaths for machining:

```bash
# Top frame toolpaths
python examples/generate_top_frame_toolpaths.py

# Bottom tray toolpaths
python examples/generate_bottom_tray_toolpaths.py
```

Export toolpaths to DXF format:
```bash
python examples/export_top_frame_toolpaths.py
python examples/export_bottom_tray_toolpaths.py
```

### Generate Technical Drawings

Generate 2D technical drawings with dimensions:

```bash
python examples/export_top_frame_drawing.py
python examples/export_bottom_tray_drawing.py
python examples/export_assembly_drawing.py
```

Outputs PDF and DXF files to `output/drawings/`

### Generate Manufacturing Documentation

Generate complete manufacturing documentation:

```bash
python examples/generate_tool_list.py
python examples/generate_setup_sheets.py
```

See `docs/manufacturing/` for:
- Bill of materials
- Operation sequences
- Quality control checklist
- Assembly instructions

### CNC Toolpath Operations

**Top Frame** (5 operations):
1. Face Surfacing - 6mm endmill, 0.5mm depth
2. Brass Insert Counterbores - 6mm endmill, 5.8mm dia, 4mm deep (6x)
3. PCB Opening Pocket - 6mm roughing, 3mm finishing
4. USB Cutout - 3mm endmill
5. External Profile - 6mm roughing, 3mm finishing

**Bottom Tray** (7 operations):
1. Face Surfacing - 6mm endmill, 0.5mm depth
2. Rubber Feet Recesses - 10mm endmill, 2mm deep (4x)
3. Assembly Screw Counterbores - 6mm endmill, 3mm deep (6x)
4. Assembly Screw Through-holes - 3.2mm drill (6x)
5. Internal Cavity Pocket - 6mm roughing, 4mm finishing
6. Standoff Through-holes - 2.2mm drill (6x)
7. External Profile - 6mm roughing, 3mm finishing

## Documentation

See `.kiro/specs/60-percent-keyboard-case/` for complete requirements, design, and implementation plan.

## License

(To be determined)
