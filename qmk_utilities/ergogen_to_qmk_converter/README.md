# Ergogen to QMK Converter

A utility for converting Ergogen hardware definition files (.yaml) to QMK firmware keyboard configurations, bridging the gap between hardware design and firmware setup.

## 🎯 Purpose

This converter takes comprehensive Ergogen keyboard hardware definitions and generates the complete set of QMK firmware files needed for a custom keyboard, including:

- `config.h` - Hardware pin definitions, matrix configuration, feature flags
- `keyboard.h` - Physical layout matrix mapping  
- `rules.mk` - Build configuration for hardware features
- `info.json` - QMK Configurator support with physical key positions

## 🔄 Conversion Flow

```
Ergogen YAML → Parser → QMK Hardware Model → Generators → QMK Files
     ↓            ↓           ↓              ↓          ↓
config_4x5.yaml → Extract → Matrix/Pins → Generate → config.h
                   Features   Hardware     Files     keyboard.h
                   Positions  Config                 rules.mk
                   MCU Info                          info.json
```

## 📋 What Ergogen Provides

From a typical ergogen file like `config_4x5.yaml`, we can extract:

✅ **Matrix Configuration**
```yaml
points:
  zones:
    numpad:
      columns: col0, col1, col2, col3
      rows: row0, row1, row2, row3, row4
```

✅ **Pin Assignments** 
```yaml
controller:
  what: promicro
  params:
    P0: col0, P1: col1, P10: row0, P14: row1
    P2: SCL, P3: SDA  # OLED pins
    P18: row_enc_left  # Encoder pins
```

✅ **Hardware Features**
```yaml
footprints:
  encoder_left: rotary encoder
  oled_screen: OLED display
  mx_switches: hotswap switches
```

✅ **Physical Layout**
```yaml
points: # Key positions and sizes
  anchor.shift: [kx*3, ky*2]
  width: capx, height: capy
```

## 🏗 Architecture

### Components
- **`ergogen_parser.py`** - Parse Ergogen YAML files
- **`qmk_hardware_model.py`** - Intermediate representation
- **`config_generator.py`** - Generate config.h
- **`keyboard_generator.py`** - Generate keyboard.h
- **`rules_generator.py`** - Generate rules.mk
- **`info_generator.py`** - Generate info.json

### Data Flow
```python
# Load and parse Ergogen file
ergogen_data = ErgogenParser().parse("config_4x5.yaml")

# Convert to QMK hardware model
qmk_model = QMKHardwareModel.from_ergogen(ergogen_data)

# Generate QMK configuration files
ConfigGenerator().generate(qmk_model, "config.h")
KeyboardGenerator().generate(qmk_model, "keyboard.h")
RulesGenerator().generate(qmk_model, "rules.mk")
InfoGenerator().generate(qmk_model, "info.json")
```

## 🚀 Planned Features

### Phase 1: Core Conversion
- [x] Project structure setup
- [ ] Ergogen YAML parser
- [ ] QMK hardware data model
- [ ] Basic config.h generation
- [ ] Matrix definition extraction

### Phase 2: Hardware Features
- [ ] Encoder support detection and config
- [ ] OLED/Display configuration
- [ ] RGB lighting configuration
- [ ] Audio/Speaker configuration
- [ ] Advanced pin mapping

### Phase 3: Layout Generation
- [ ] Physical layout matrix mapping
- [ ] Keyboard.h layout definitions
- [ ] Info.json coordinate conversion
- [ ] Special key size handling (2U, etc.)

### Phase 4: Advanced Features
- [ ] Custom PCB footprint support
- [ ] Multiple controller types (Pro Micro, Elite-C, etc.)
- [ ] Validation and error checking
- [ ] CLI interface
- [ ] Integration tests

## 📁 Project Structure

```
ergogen_to_qmk_converter/
├── README.md
├── __init__.py
├── cli.py                 # Command line interface
├── ergogen_converter.py   # Main converter class
├── parsers/
│   ├── __init__.py
│   └── ergogen_parser.py  # Parse Ergogen YAML
├── generators/
│   ├── __init__.py
│   ├── config_generator.py    # Generate config.h
│   ├── keyboard_generator.py  # Generate keyboard.h
│   ├── rules_generator.py     # Generate rules.mk
│   └── info_generator.py      # Generate info.json
├── data_models/
│   ├── __init__.py
│   ├── qmk_hardware_model.py  # QMK hardware representation
│   └── ergogen_model.py       # Ergogen data structures
├── docs/
│   ├── ARCHITECTURE.md
│   ├── ERGOGEN_REFERENCE.md
│   ├── QMK_OUTPUT_SPEC.md
│   └── DEVELOPMENT_TASKS.md
└── tests/
    ├── __init__.py
    ├── test_parser.py
    ├── test_generators.py
    └── sample_files/
        └── config_4x5.yaml
```

## 🔧 Usage (Planned)

### Command Line
```bash
# Convert ergogen file to QMK configuration
python cli.py config_4x5.yaml --output-dir ./keyboard_config

# Validate ergogen file
python cli.py config_4x5.yaml --validate

# Generate specific files only
python cli.py config_4x5.yaml --only config,keyboard
```

### Python API
```python
from ergogen_to_qmk_converter import ErgogenConverter

converter = ErgogenConverter()

# Convert file
converter.convert_file("config_4x5.yaml", output_dir="./my_keyboard")

# Convert to specific formats
hardware_model = converter.parse_ergogen("config_4x5.yaml")
converter.generate_config_h(hardware_model, "config.h")
converter.generate_info_json(hardware_model, "info.json")
```

## 🤝 Integration with Existing Tools

This converter complements the existing QMK utilities:

```
KLE → kle_to_ergogen → Ergogen → ergogen_to_qmk → QMK Config
                                      ↓
                              qmk_format_converter
                                      ↓
                              VIA/Keymap Files
```

## 🎮 Test Case: config_4x5.yaml

Our first implementation will target the `config_4x5.yaml` file which defines:

- **21 keys**: Numpad (17) + Navigation (5) + Thumb (1) 
- **3 encoders**: Left, right, bottom with click functionality
- **1 OLED**: 128x64 I2C display
- **Pro Micro**: Controller with full pin mapping
- **Special keys**: 2U wide zero, 2U tall plus/enter keys

Expected QMK output:
- 5×6 matrix configuration
- 3 encoder pins + 3 encoder switch pins  
- I2C OLED on pins 2/3
- Hotswap socket support
- Complete physical layout for QMK Configurator

## 📝 Development Status

- **Status**: Planning/Setup Phase
- **Next Steps**: See `docs/DEVELOPMENT_TASKS.md`
- **Target**: Working conversion for config_4x5.yaml
- **Timeline**: Development ready to start

## 🔗 Related Projects

- [QMK Format Converter](../qmk_format_converter/) - Keymap format conversion
- [KLE to Ergogen](../kle_to_ergogen/) - Layout to hardware conversion
- [QMK Firmware](https://github.com/qmk/qmk_firmware) - Target firmware platform
- [Ergogen](https://github.com/ergogen/ergogen) - Source hardware definition format

---

**Made for the mechanical keyboard community** 🔥⌨️
