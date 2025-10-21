# Through-Hole Keyboard Generator (THKG)

An automated design tool for generating complete keyboard designs from high-level specifications.

## Features

- **Multiple Layout Types**: Keyboards, numpads, macropads
- **Layout Styles**: Staggered, ortholinear, custom KLE import
- **Automatic Generation**: PCB, plate, case, firmware
- **Template-Based**: Uses proven circuits from the Through-Hole Keyboard Library
- **Interactive CLI**: Guided configuration builder

## Installation

```bash
cd PCB/tools/keyboard-generator
pip install -e .
```

## Quick Start

### 1. Interactive Configuration

```bash
thkg interactive
```

This will guide you through creating a configuration file.

### 2. Generate Design

```bash
thkg generate config.yaml
```

This will generate all design files in the `output/` directory.

### 3. List Available Presets

```bash
thkg list-presets
```

## Configuration

Configuration files are in YAML format. See `examples/` for complete examples.

### Basic Configuration

```yaml
keyboard:
  name: "MyKeyboard"
  description: "My custom keyboard"
  version: "1.0"

layout:
  type: "60-ansi"  # Or use KLE file

hardware:
  mcu:
    type: "atmega328p"
  usb:
    type: "usb-c-tht"

plate:
  enabled: true
  switch_type: "mx"
  thickness: 1.5

firmware:
  qmk: true
  via: true
```

## Available Layouts

### Keyboards (Staggered)
- `60-ansi` - 60% ANSI (61 keys)
- `60-iso` - 60% ISO (62 keys)
- `65-ansi` - 65% with arrows (68 keys)
- `tkl` - Tenkeyless (87 keys)
- `40-ansi` - 40% (47 keys)

### Keyboards (Ortholinear)
- `60-ortho` - 5x12 grid (60 keys)
- `40-ortho` - 4x12 grid (48 keys)
- `50-ortho` - 5x10 grid (50 keys)

### Numpads
- `numpad-standard` - 4x5 (20 keys)
- `numpad-compact` - 4x4 (16 keys)
- `numpad-extended` - 5x4 (20 keys)

### Macropads
- `macropad-3x3` - 3x3 grid (9 keys)
- `macropad-4x4` - 4x4 grid (16 keys)
- `macropad-2x3` - 2x3 grid (6 keys)

## Custom Layouts

You can import custom layouts from KLE (Keyboard Layout Editor):

```yaml
layout:
  type: "custom"
  kle_file: "path/to/layout.json"
```

## Output Files

Generated files are organized in the output directory:

```
output/MyKeyboard/
├── pcb/
│   ├── MyKeyboard.kicad_sch
│   ├── MyKeyboard.kicad_pcb
│   └── gerbers/
├── plate/
│   └── plate.dxf
├── case/
│   ├── top.dxf
│   ├── bottom.dxf
│   └── case.stl
├── firmware/
│   ├── config.h
│   ├── rules.mk
│   └── keymap.c
├── BOM.csv
└── README.md
```

## PCB Design Knowledge

The generator incorporates industry-standard PCB design practices from:
- **ai03's PCB Design Guide** - Proven wired keyboard circuits
- **ebastler's ZMK Design Guide** - Advanced wireless designs

See [PCB_IMPROVEMENTS.md](PCB_IMPROVEMENTS.md) for details on:
- Accurate pin assignments with proper reservations
- USB protection circuits (ESD, ferrite beads, polyfuse)
- MCU support circuits (crystal, decoupling, ISP)
- Component library with real part numbers
- Automatic BOM generation
- PCB layout rules

## Development

### Running Tests

```bash
pytest tests/
python test_pcb_improvements.py  # Test PCB design features
```

### Project Structure

```
thkg/
├── input/          # Configuration parsing
├── layout/         # Layout engine
├── plate/          # Plate generation
├── pcb/            # PCB generation
├── case/           # Case generation
├── firmware/       # Firmware generation
└── cli.py          # Command-line interface
```

## Requirements

- Python 3.8+
- KiCad (for PCB generation)
- OpenSCAD (for case generation, optional)

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please see CONTRIBUTING.md for guidelines.
