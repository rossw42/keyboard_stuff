# 3D Model and CAD Drawing Catalog

*Generated: 2025-10-16 17:51:30*

## Overview

This catalog provides a comprehensive index of all 3D models and CAD drawings available in the Through-Hole Keyboard PCB Design Resource Library.

### Statistics

- **Total Projects:** 0
- **STL Files:** 0 (3D printing)
- **STEP Files:** 0 (CAD editing)
- **DXF Files:** 0 (laser cutting/CNC)
- **SVG Files:** 0 (vector graphics)

## Table of Contents

- [3D Models](#3d-models)
  - [Cases](#cases)
  - [Plates](#plates)
  - [Accessories](#accessories)
- [CAD Drawings](#cad-drawings)
  - [Plate Drawings](#plate-drawings)
  - [Case Drawings](#case-drawings)
  - [Cover Drawings](#cover-drawings)
- [Usage Guidelines](#usage-guidelines)

## 3D Models

## CAD Drawings

## Usage Guidelines

### 3D Printing (STL Files)

**General Recommendations:**

- **Slicer Software:** Cura, PrusaSlicer, or Simplify3D
- **Layer Height:** 0.2mm standard, 0.1mm for fine details
- **Infill:** 20-30% for structural parts, 15% for large prints
- **Wall Thickness:** 3-4 perimeters recommended
- **Supports:** Enable for overhangs > 45°
- **Bed Adhesion:** Brim or raft for large prints

**Material Selection:**

- **PLA:** Easy to print, rigid, good for most cases
- **PETG:** More durable, slightly flexible, better layer adhesion
- **ABS:** Strong, heat resistant, requires heated enclosure
- **Polycarbonate:** Very strong, excellent for plates

### CAD Editing (STEP Files)

**Compatible Software:**

- FreeCAD (free, open-source)
- Fusion 360 (free for hobbyists)
- SolidWorks (professional)
- OnShape (browser-based)

**Editing Tips:**

- Always keep a backup of the original file
- Check dimensions before making modifications
- Maintain proper clearances for PCB and components
- Export to STL for 3D printing after modifications

### Laser Cutting / CNC (DXF Files)

**Service Providers:**

- Ponoko (laser cutting)
- SendCutSend (laser and CNC)
- Local makerspaces and fab labs

**Material Options:**

- **Acrylic:** 1.5-3mm for plates, 3-5mm for cases
- **FR4 (PCB material):** 1.5mm for plates
- **Aluminum:** 1.5mm for plates, requires CNC
- **Steel:** 1.5mm for plates, requires CNC
- **Wood:** 3-5mm for cases, laser or CNC

## Related Documentation

- [Repository Inventory](repository_inventory.md) - Project metadata
- [Manufacturing Guide](manufacturing_guide.md) - PCB ordering
- [Build Guides](build-guides/) - Assembly instructions

## Contributing

To add new 3D models or CAD drawings:

1. Organize files using `scripts/organize_3d_models.sh <project-name>`
2. Regenerate catalog using `scripts/generate_3d_catalog.py`
3. Verify files are properly categorized
4. Update project documentation as needed

---

*This catalog is automatically generated. Do not edit manually.*
