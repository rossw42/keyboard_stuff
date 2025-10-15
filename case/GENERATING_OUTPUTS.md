# Generating Output Files

Quick reference for generating 3D models, toolpaths, and documentation.

## Output Structure

All generated files are organized by project:

```
output/
├── 60_percent_standard/        # Standard height (20mm)
└── 60_percent_low_profile/     # Low-profile (13mm)
```

Each project contains:
- `3d_models/` - STEP and STL files
- `cnc/toolpaths/` - Toolpath JSON and DXF files
- `cnc/drawings/` - Technical drawings (PDF, DXF)
- `cnc/setup/` - Setup sheets and tool lists

## Standard Variant (20mm height)

### 3D Models

```bash
# Generate all 3D models (top frame, bottom tray, assembly)
python examples/generate_all_3d_models.py

# Or generate individually:
python examples/generate_top_frame_3d.py
python examples/generate_bottom_tray_3d.py
python examples/generate_assembly_3d.py
```

Output: `output/60_percent_standard/3d_models/`

### CNC Toolpaths

```bash
# Generate toolpaths
python examples/generate_top_frame_toolpaths.py
python examples/generate_bottom_tray_toolpaths.py

# Export toolpaths to DXF
python examples/export_top_frame_toolpaths.py
python examples/export_bottom_tray_toolpaths.py
```

Output: `output/60_percent_standard/cnc/toolpaths/`

### Technical Drawings

```bash
# Generate technical drawings
python examples/export_top_frame_drawing.py
python examples/export_bottom_tray_drawing.py
python examples/export_assembly_drawing.py
```

Output: `output/60_percent_standard/cnc/drawings/`

### Setup Documentation

```bash
# Generate setup sheets
python examples/generate_setup_sheets.py

# Generate tool list
python examples/generate_tool_list.py
```

Output: `output/60_percent_standard/cnc/setup/`

## Low-Profile Variant (13mm height)

### 3D Models

```bash
# Generate low-profile 3D models
python examples/generate_top_frame_3d_lp.py
python examples/generate_bottom_tray_3d_lp.py
python examples/generate_assembly_3d_lp.py
```

Output: `output/60_percent_low_profile/3d_models/`

### CNC Toolpaths

```bash
# Generate low-profile toolpaths
python examples/generate_top_frame_toolpaths_lp.py
python examples/generate_bottom_tray_toolpaths_lp.py
```

Output: `output/60_percent_low_profile/cnc/toolpaths/`

## Validation

```bash
# Validate standard variant design
python examples/validate_design.py

# Validate low-profile variant design
python examples/validate_design_lp.py
```

## File Types

- **STEP (.step)** - CAD models for editing (Fusion 360, FreeCAD, etc.)
- **STL (.stl)** - 3D models for visualization or 3D printing
- **JSON (.json)** - Toolpath data with operation details
- **DXF (.dxf)** - 2D drawings for CAD import
- **PDF (.pdf)** - Technical drawings for reference
- **MD (.md)** - Setup instructions and documentation

## Viewing Files

### STEP Files (CAD)
- **FreeCAD** (free): `freecad output/60_percent_standard/3d_models/assembly.step`
- **Fusion 360**: File → Open → Select STEP file
- **OnShape**: Import STEP file

### STL Files (Visualization)
- **Online**: Upload to [ViewSTL.com](https://www.viewstl.com/)
- **Blender**: File → Import → STL
- **MeshLab** (free): Open STL file

### DXF Files (CAD)
- **LibreCAD** (free): Open DXF file
- **QCAD** (free): Open DXF file
- **AutoCAD**: Open DXF file

### PDF Files
- Any PDF viewer (Preview, Adobe Reader, etc.)

## Tips

- Run validation scripts before generating final outputs
- Check README files in each project folder for specifications
- Review technical drawings before machining
- Test toolpaths in CAM software before running on CNC
- Use 3D printed prototypes to validate fit before CNC machining

## Troubleshooting

**Import errors:**
```bash
# Make sure you're in the project root
pwd  # Should show /Users/ross/Projects/case

# Install dependencies if needed
pip install -r requirements.txt
```

**Missing output directories:**
- Scripts automatically create directories
- If issues persist, manually create: `mkdir -p output/60_percent_standard/{3d_models,cnc/{toolpaths,drawings,setup}}`

**File permissions:**
```bash
# Make scripts executable
chmod +x examples/*.py
```
