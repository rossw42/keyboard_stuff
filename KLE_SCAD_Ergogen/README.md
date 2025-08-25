# KLE to Ergogen Converter

Convert Keyboard Layout Editor (KLE) JSON files to Ergogen YAML format for PCB generation.

## Overview

This tool bridges the gap between Keyboard Layout Editor (KLE) and Ergogen, allowing you to:
- Design your keyboard layout visually in KLE
- Convert the layout to Ergogen YAML format
- Generate PCBs, cases, and plates using Ergogen

Inspired by the `hotswap_pcb_generator` project, this converter leverages the same KLE parsing approach but outputs Ergogen-compatible YAML instead of OpenSCAD.

## Features

- ✅ Parse KLE JSON files with full layout support
- ✅ Transform KLE coordinates to Ergogen coordinate system
- ✅ Support for various key sizes and stabilizers
- ✅ Generate proper matrix wiring layout
- ✅ Include switch footprints (MX, Choc, Choc v2)
- ✅ Add diode footprints with configurable direction
- ✅ Support for hotswap sockets
- ✅ Microcontroller placement (Pro Micro, Elite-C, etc.)
- ✅ Optional case generation
- ✅ Generate OpenSCAD files (hotswap_pcb_generator compatible)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd KLE_SCAD_Ergogen

# Install dependencies
npm install

# Make CLI executable (optional)
npm link
```

## Usage

### Basic Usage

```bash
# Convert a KLE JSON file to Ergogen YAML
node index.js <input.json>

# Or if you've run npm link
kle-to-ergogen <input.json>
```

### Command Line Options

```bash
kle-to-ergogen <input.json> [options]

Options:
  -o, --output <path>           Output file path (default: input.yaml)
  -s, --switch-type <type>      Switch type: mx, choc, choc_v2 (default: mx)
  -k, --key-spacing <mm>        Key spacing in mm (default: 19)
  -m, --microcontroller <type>  Microcontroller type (default: promicro)
  --hotswap                     Use hotswap sockets (default: true)
  --no-hotswap                  Use soldered switches
  --split                       Generate split keyboard configuration
  --diode-direction <dir>       Diode direction: row, column (default: row)
  --center-layout               Center layout around origin (default: true)
  --no-center-layout            Keep original KLE positioning
  --include-case                Include case generation
  --include-scad                Generate OpenSCAD file (hotswap_pcb_generator compatible)
  -v, --verbose                 Verbose output
  -h, --help                    Display help
```

### Examples

#### Simple 2x2 Macropad
```bash
node index.js examples/macropad_2x2.json
```

#### Numpad with Custom Options
```bash
node index.js examples/numpad.json \
  --switch-type choc \
  --key-spacing 18 \
  --include-case
```

#### Split Keyboard with Hotswap
```bash
node index.js my_split_keyboard.json \
  --split \
  --hotswap \
  --microcontroller elite_c
```

## KLE JSON Format

The converter supports standard KLE JSON format. You can create layouts using:
- [Keyboard Layout Editor](http://www.keyboard-layout-editor.com/)
- Raw JSON arrays following KLE format

### Example KLE JSON

```json
[
  ["Q", "W", "E", "R"],
  ["A", "S", "D", "F"],
  [{"w": 2}, "Space", "Enter"]
]
```

## Output Format

The converter generates Ergogen v4 compatible YAML with:

### Structure
- **meta**: Project metadata
- **units**: Key spacing and dimensions
- **points**: Key positions organized in zones and columns
- **outlines**: PCB and plate outlines
- **pcbs**: PCB configuration with footprints
- **cases**: Optional case generation

### Example Output

```yaml
meta:
  engine: v4
  name: My Keyboard
  version: '1.0'
  
units:
  kx: 19  # Key spacing X
  ky: 19  # Key spacing Y
  
points:
  zones:
    matrix:
      columns:
        col0:
          rows:
            Q: {}
            A: {}
            
pcbs:
  main:
    footprints:
      switches:
        what: mx
        where: true
        params:
          hotswap: true
```

## Architecture

### Modules

1. **kleParser.js**: Parses KLE JSON using @ijprest/kle-serial
2. **coordinateTransform.js**: Transforms KLE coordinates to Ergogen system
3. **ergogenGenerator.js**: Generates Ergogen YAML configuration
4. **index.js**: CLI interface and orchestration

### Coordinate System

- **KLE**: Origin at top-left, Y+ pointing down, units in keyboard units (1u = 19.05mm)
- **Ergogen**: Origin at center, Y+ pointing up, units in mm
- **Transformation**: Automatic centering and axis flipping

## Advanced Features

### Matrix Generation
The converter automatically analyzes key positions to generate an optimal matrix layout, grouping keys into rows and columns based on physical position.

### Stabilizer Detection
Keys 2u and wider are automatically detected as requiring stabilizers, with appropriate configuration added to the output.

### Split Keyboard Support
Use the `--split` flag to generate configurations for split keyboards with proper matrix routing.

### OpenSCAD Compatibility
The `--include-scad` option generates OpenSCAD files compatible with the `hotswap_pcb_generator` project format.

## Development

### Project Structure
```
KLE_SCAD_Ergogen/
├── src/
│   ├── kleParser.js         # KLE JSON parsing
│   ├── coordinateTransform.js # Coordinate transformation
│   └── ergogenGenerator.js  # YAML generation
├── examples/                # Example KLE files
├── docs/                    # Documentation
├── test/                    # Test files
└── index.js                 # CLI entry point
```

### Testing

```bash
# Test with simple macropad
npm test

# Test with numpad
npm run test:numpad

# Test with your own file
node index.js path/to/your/layout.json -v
```

## Comparison with hotswap_pcb_generator

While `hotswap_pcb_generator` converts KLE → OpenSCAD for 3D-printed PCBs, this tool converts KLE → Ergogen for:
- Professional PCB manufacturing
- More complex routing options
- Integration with KiCad
- Advanced footprint management

Both tools can be used together - design in KLE, prototype with hotswap_pcb_generator, then produce with Ergogen.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Future Improvements
- [ ] Better zone detection for complex layouts
- [ ] Support for rotated keys
- [ ] Automatic thumb cluster detection
- [ ] Support for ISO enter and other special keys
- [ ] Integration with Ergogen CLI
- [ ] Web-based converter interface

## License

MIT License - See LICENSE file for details

## Acknowledgments

- [hotswap_pcb_generator](https://github.com/50an6xy06r6n/hotswap_pcb_generator) for inspiration and KLE parsing approach
- [@ijprest/kle-serial](https://github.com/ijprest/kle-serial) for KLE JSON parsing
- [Ergogen](https://github.com/ergogen/ergogen) for the PCB generation framework
- The mechanical keyboard community

## Support

For issues, questions, or suggestions, please open an issue on GitHub.