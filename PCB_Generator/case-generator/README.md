# CNC Case Generator

Parametric case design tool for GH60-compatible 60% mechanical keyboards. Generates CNC-ready toolpaths, 3D models, and technical drawings for both standard and low-profile designs.

## Features

- **Parametric Design** - Adjust dimensions via constants files
- **Two Profiles** - Standard (12mm) and low-profile (8mm) heights
- **Complete Outputs** - STL models, DXF drawings, G-code toolpaths
- **CNC Ready** - Optimized toolpaths for 3-axis CNC mills
- **GH60 Compatible** - Follows authoritative GH60 PCB specifications

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate standard profile case
python examples/generate_top_frame.py
python examples/generate_bottom_tray.py

# Generate low-profile case
python examples/generate_top_frame_3d_lp.py
python examples/generate_bottom_tray_3d_lp.py

# Output in: output/60_percent_standard/ or output/60_percent_low_profile/
```

## Project Structure

```
case-generator/
├── src/                    # Source code
│   ├── geometry/          # Geometry generation
│   ├── toolpaths/         # CNC toolpath generation
│   ├── export/            # File export utilities
│   ├── constants.py       # Standard profile parameters
│   └── constants_lp.py    # Low-profile parameters
│
├── examples/              # Example scripts
│   ├── generate_*.py     # Generation scripts
│   ├── validate_*.py     # Validation scripts
│   └── visualize_*.py    # Visualization scripts
│
├── tests/                 # Test suite
├── output/                # Generated files
├── docs/                  # Documentation
└── scripts/               # Utility scripts
```

## Outputs

### Standard Profile (12mm height)
- Top frame: 286mm × 95.6mm × 12mm
- Bottom tray: 286mm × 95.6mm × 12mm
- Total height: ~24mm

### Low Profile (8mm height)
- Top frame: 286mm × 95.6mm × 8mm
- Bottom tray: 286mm × 95.6mm × 8mm
- Total height: ~16mm

### File Types
- **STL** - 3D models for visualization/3D printing
- **DXF** - 2D drawings for documentation
- **G-code** - CNC toolpaths (roughing, finishing, drilling)
- **PDF** - Setup sheets and tool lists

## Examples

### Generate Complete Case
```bash
python examples/generate_all_3d_models.py
```

### Generate Toolpaths
```bash
python examples/generate_top_frame_toolpaths.py
python examples/generate_bottom_tray_toolpaths.py
```

### Validate Design
```bash
python examples/validate_design.py
```

## Configuration

Edit `src/constants.py` or `src/constants_lp.py` to adjust:
- PCB dimensions
- Mounting hole positions
- Wall thickness
- Corner radii
- Clearances
- Tool specifications

## Documentation

- **GH60 Specifications:** [docs/gh60_pcb_specifications.md](docs/gh60_pcb_specifications.md)
- **Compatible PCBs:** [docs/compatible_pcbs.md](docs/compatible_pcbs.md)
- **Manufacturing:** [docs/manufacturing/](docs/manufacturing/)
- **Implementation:** [docs/implementation/](docs/implementation/)

## Requirements

- Python 3.8+
- cadquery >= 2.0
- ezdxf >= 1.0

## Testing

```bash
pytest tests/
```

## License

See LICENSE file for details.
