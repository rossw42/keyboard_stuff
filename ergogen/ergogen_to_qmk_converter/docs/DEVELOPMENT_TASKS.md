# Development Tasks: Ergogen to QMK Converter

## 🎯 Project Goal
Create a utility that converts Ergogen hardware definition YAML files to complete QMK keyboard configurations.

## 📋 Task Breakdown

### Phase 1: Foundation & Parsing (Priority: High)

#### Task 1.1: Project Setup
- [x] Create directory structure
- [x] Create README.md with project overview
- [x] Create documentation framework
- [ ] Create `__init__.py` files
- [ ] Setup basic CLI structure
- [ ] Create sample test files

**Estimated Time**: 2-3 hours
**Dependencies**: None
**Files to create**: `__init__.py`, `cli.py`, `ergogen_converter.py`

#### Task 1.2: Ergogen Parser Development
- [ ] Create `ErgogenParser` class in `parsers/ergogen_parser.py`
- [ ] Implement YAML parsing with error handling
- [ ] Extract matrix configuration (rows/columns)
- [ ] Extract pin assignments from controller section
- [ ] Extract physical layout coordinates
- [ ] Parse hardware features (encoders, OLED, etc.)

**Estimated Time**: 6-8 hours
**Dependencies**: Task 1.1
**Key Functions**:
```python
def parse_matrix_config(zones_data) -> MatrixConfig
def parse_pin_assignments(controller_data) -> PinMapping  
def parse_physical_layout(points_data) -> LayoutCoordinates
def parse_hardware_features(footprints_data) -> HardwareFeatures
```

#### Task 1.3: QMK Hardware Model
- [ ] Create `QMKHardwareModel` class in `data_models/qmk_hardware_model.py`
- [ ] Define matrix configuration structure
- [ ] Define pin mapping structure
- [ ] Define hardware feature flags
- [ ] Define physical layout representation
- [ ] Implement validation methods

**Estimated Time**: 4-5 hours  
**Dependencies**: Task 1.2
**Key Classes**:
```python
@dataclass
class MatrixConfig:
    rows: int
    cols: int
    row_pins: List[str]
    col_pins: List[str]

@dataclass  
class QMKHardwareModel:
    matrix: MatrixConfig
    pins: PinMapping
    features: HardwareFeatures
    layout: PhysicalLayout
```

### Phase 2: QMK File Generation (Priority: High)

#### Task 2.1: Config.h Generator
- [ ] Create `ConfigGenerator` class in `generators/config_generator.py`
- [ ] Generate matrix size definitions
- [ ] Generate pin assignments
- [ ] Generate feature flags (ENCODER_ENABLE, OLED_ENABLE)
- [ ] Generate I2C and SPI configurations
- [ ] Template-based generation system

**Estimated Time**: 5-6 hours
**Dependencies**: Task 1.3
**Output Example**:
```c
#define MATRIX_ROWS 5
#define MATRIX_COLS 6
#define MATRIX_ROW_PINS { GP10, GP14, GP15, GP16, GP21 }
#define MATRIX_COL_PINS { GP0, GP1, GP2, GP4, GP5, GP7 }
#define ENCODER_ENABLE
#define ENCODERS_PAD_A { GP18, GP19, GP20 }
```

#### Task 2.2: Keyboard.h Generator  
- [ ] Create `KeyboardGenerator` class in `generators/keyboard_generator.py`
- [ ] Generate LAYOUT macro definitions
- [ ] Map physical positions to matrix positions
- [ ] Handle special key sizes (2U, 2U tall, etc.)
- [ ] Generate multiple layout variants if needed

**Estimated Time**: 4-5 hours
**Dependencies**: Task 1.3
**Output Example**:
```c
#define LAYOUT_numpad( \
    k00, k01, k02, k03, \
    k10, k11, k12, k13, \
    k20, k21, k22,      \
    k30, k31, k32, k33, \
    k40,      k42       \
) { \
    { k00, k01, k02, k03, KC_NO, KC_NO }, \
    { k10, k11, k12, k13, KC_NO, KC_NO }, \
    /* ... */ \
}
```

#### Task 2.3: Rules.mk Generator
- [ ] Create `RulesGenerator` class in `generators/rules_generator.py`
- [ ] Detect required QMK features from hardware
- [ ] Generate feature enable flags
- [ ] Set MCU type and F_CPU
- [ ] Configure build options

**Estimated Time**: 3-4 hours
**Dependencies**: Task 1.3
**Output Example**:
```makefile
MCU = atmega32u4
F_CPU = 16000000
ENCODER_ENABLE = yes
OLED_ENABLE = yes
OLED_DRIVER = ssd1306
```

#### Task 2.4: Info.json Generator
- [ ] Create `InfoGenerator` class in `generators/info_generator.py`
- [ ] Convert Ergogen coordinates to QMK coordinates
- [ ] Generate keyboard metadata
- [ ] Create layout definitions with physical positions
- [ ] Handle special key shapes and sizes

**Estimated Time**: 6-7 hours
**Dependencies**: Task 1.3
**Complex because**: Coordinate system conversion, key shape handling

### Phase 3: Integration & Testing (Priority: Medium)

#### Task 3.1: Main Converter Class
- [ ] Create `ErgogenConverter` class in `ergogen_converter.py`
- [ ] Integrate all parsers and generators
- [ ] Implement file conversion workflow
- [ ] Add error handling and validation
- [ ] Create progress reporting

**Estimated Time**: 3-4 hours
**Dependencies**: Tasks 2.1-2.4

#### Task 3.2: CLI Interface
- [ ] Create command-line interface in `cli.py`
- [ ] Add argument parsing (input file, output dir, options)
- [ ] Implement file validation mode
- [ ] Add verbose/debug output options
- [ ] Create help documentation

**Estimated Time**: 4-5 hours
**Dependencies**: Task 3.1

#### Task 3.3: Testing Framework
- [ ] Copy `config_4x5.yaml` to `tests/sample_files/`
- [ ] Create unit tests for parser components
- [ ] Create integration tests for full conversion
- [ ] Test against expected QMK output
- [ ] Create validation tests for edge cases

**Estimated Time**: 5-6 hours
**Dependencies**: Tasks 1.2, 2.1-2.4

### Phase 4: Advanced Features (Priority: Low)

#### Task 4.1: Multi-Controller Support
- [ ] Add Elite-C controller support
- [ ] Add STM32 controller support  
- [ ] Create controller abstraction layer
- [ ] Update pin mapping system

**Estimated Time**: 4-6 hours

#### Task 4.2: Advanced Hardware Features
- [ ] RGB LED strip configuration
- [ ] Audio/Speaker configuration
- [ ] Split keyboard support
- [ ] Custom matrix configurations

**Estimated Time**: 8-10 hours

## 🚀 Quick Start Sequence (Day 1)

### Morning Session (3-4 hours)
1. **Setup** (30 min): Create all `__init__.py` files, basic structure
2. **Parser Start** (3 hours): Begin `ErgogenParser` class, focus on YAML loading and basic structure extraction
3. **Test**: Load `config_4x5.yaml` and print parsed sections

### Afternoon Session (3-4 hours)  
1. **Parser Complete** (2 hours): Finish matrix config and pin parsing
2. **Data Model** (2 hours): Create basic `QMKHardwareModel` structure
3. **Test**: Successfully parse config_4x5.yaml into model

### End of Day 1 Target
- [ ] Can parse `config_4x5.yaml` completely
- [ ] Data is structured in `QMKHardwareModel` 
- [ ] Basic validation working
- [ ] Ready to start generators

## 📊 Progress Tracking

### Completion Metrics
- **Phase 1**: Parser can extract all data from config_4x5.yaml
- **Phase 2**: All 4 QMK files generate successfully
- **Phase 3**: CLI tool works end-to-end
- **Phase 4**: Advanced features (stretch goals)

### Testing Milestones
1. **Parser Test**: Successfully parse config_4x5.yaml
2. **Generator Test**: Generate valid config.h from parsed data
3. **Integration Test**: Full conversion produces buildable QMK config
4. **Validation Test**: Generated files compile in QMK

## 🔧 Development Environment

### Required Tools
- Python 3.7+
- PyYAML for YAML parsing
- Jinja2 for template generation (optional)
- QMK CLI for validation testing

### Recommended Setup
```bash
cd ergogen_to_qmk_converter
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install pyyaml jinja2
```

### Test Files Needed
- Copy `../kle_to_ergogen/config_4x5.yaml` to `tests/sample_files/`
- Create expected output samples for comparison testing

## 📝 Notes & Decisions

### Technical Decisions
- **YAML Parser**: Use PyYAML for ergogen file parsing
- **Template Engine**: Consider Jinja2 for QMK file generation
- **Coordinate System**: Ergogen uses mm coordinates, QMK uses matrix positions
- **Pin Format**: Convert GP10 format to QMK pin names

### Known Challenges
1. **Coordinate Conversion**: Ergogen physical coordinates → QMK layout positions
2. **Special Keys**: 2U and 2U tall keys need special matrix handling  
3. **Pin Mapping**: Different controllers use different pin naming
4. **Feature Detection**: Automatically detect required QMK features

### Future Enhancements
- GUI interface for non-technical users
- Integration with KLE → Ergogen → QMK workflow
- Support for custom PCB footprints
- Automatic QMK compilation and validation

---

**Ready to start development! 🚀**
