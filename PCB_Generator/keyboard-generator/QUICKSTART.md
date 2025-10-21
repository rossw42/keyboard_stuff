# THKG Quick Start Guide

Get started with the Through-Hole Keyboard Generator in 5 minutes!

## Installation

```bash
cd PCB/tools/keyboard-generator
pip install -e .
```

## Generate Your First Plate

### Option 1: Use an Example (Fastest)

```bash
# Generate a 3x3 macropad plate
thkg generate examples/macropad-3x3.yaml

# Output will be in: output/3x3-Macropad/plate.dxf
```

### Option 2: Interactive Mode

```bash
# Start interactive configuration
thkg interactive

# Follow the prompts:
# 1. Enter keyboard name
# 2. Choose type (keyboard/numpad/macropad)
# 3. Select layout
# 4. Configuration saved to config.yaml

# Generate the design
thkg generate config.yaml
```

### Option 3: Create Custom Configuration

Create `my-keyboard.yaml`:

```yaml
keyboard:
  name: "MyKeyboard"
  description: "My custom keyboard"
  version: "1.0"

layout:
  type: "60-ansi"  # See available presets below

hardware:
  mcu:
    type: "atmega328p"
  usb:
    type: "usb-c-tht"

plate:
  enabled: true
  switch_type: "mx"
  thickness: 1.5
  material: "fr4"
```

Then generate:

```bash
thkg generate my-keyboard.yaml
```

## Available Presets

View all available layouts:

```bash
thkg list-presets
```

**Keyboards:**
- `60-ansi` - Standard 60% keyboard
- `60-ortho` - 60% ortholinear (5x12 grid)
- `40-ortho` - 40% ortholinear (4x12 grid)

**Numpads:**
- `numpad-standard` - Standard numpad (4x5)
- `numpad-compact` - Compact numpad (4x4)

**Macropads:**
- `macropad-3x3` - 3x3 grid (9 keys)
- `macropad-4x4` - 4x4 grid (16 keys)
- `macropad-2x3` - 2x3 grid (6 keys)

## Output Files

Generated files are organized in `output/[keyboard-name]/`:

```
output/MyKeyboard/
└── plate.dxf          # Plate design (ready for laser cutting)
```

## Next Steps

1. **Open the DXF file** in your CAD software (AutoCAD, LibreCAD, etc.)
2. **Verify dimensions** match your requirements
3. **Send to manufacturer** for laser cutting or CNC

## Tips

- **Switch Types**: Use `mx` for Cherry MX, `alps` for Alps, `choc` for Kailh Choc
- **Plate Material**: Common options are `fr4` (PCB material), `acrylic`, `aluminum`
- **Thickness**: 1.5mm is standard for FR4, 3mm for acrylic

## Troubleshooting

### "Configuration validation failed"
- Check that all required fields are present
- Verify layout preset name is correct
- Ensure MCU and USB types are valid

### "Not enough pins for matrix"
- Choose a different MCU with more pins
- Reduce the number of switches
- Use a different matrix configuration

### "File not found"
- Check the path to your configuration file
- Ensure you're in the correct directory

## Examples

All examples are in the `examples/` directory:

```bash
# 60% keyboard
thkg generate examples/60-ansi.yaml

# 3x3 macropad
thkg generate examples/macropad-3x3.yaml
```

## Getting Help

- Read the full documentation: `README.md`
- Check implementation status: `IMPLEMENTATION_STATUS.md`
- View example configurations: `examples/`
- Run tests: `pytest tests/`

## What's Next?

Phase 1 (Plate Generation) is complete. Coming soon:

- **Phase 2**: PCB generation with KiCad
- **Phase 3**: Case generation (STL/DXF)
- **Phase 4**: Firmware generation (QMK)

---

**Happy building!** 🎹
