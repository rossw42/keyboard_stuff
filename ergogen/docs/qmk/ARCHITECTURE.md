# Architecture: Ergogen to QMK Converter

## 🏗 System Overview

The Ergogen to QMK Converter follows a modular pipeline architecture that transforms hardware definitions into firmware configurations through distinct processing stages.

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌──────────────┐
│   Ergogen       │    │    Parser    │    │ QMK Hardware    │    │ Generators   │
│   YAML File     │───▶│   Layer      │───▶│     Model       │───▶│   Layer      │
│                 │    │              │    │                 │    │              │
└─────────────────┘    └──────────────┘    └─────────────────┘    └──────────────┘
                                                    │
                                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          QMK Output Files                                      │
├─────────────────┬─────────────────┬─────────────────┬─────────────────────────┤
│    config.h     │   keyboard.h    │    rules.mk     │      info.json          │
│                 │                 │                 │                         │
│ • Matrix size   │ • LAYOUT macros │ • MCU config    │ • Physical positions    │
│ • Pin defs      │ • Matrix map    │ • Feature flags │ • Key metadata          │
│ • Feature flags │ • Key positions │ • Build options │ • QMK Configurator      │
│ • Hardware cfg  │ • Special keys  │                 │                         │
└─────────────────┴─────────────────┴─────────────────┴─────────────────────────┘
```

## 🎯 Design Principles

### 1. Separation of Concerns
Each component has a single, well-defined responsibility:
- **Parser**: Extract and structure data from Ergogen YAML
- **Data Model**: Provide a clean intermediate representation
- **Generators**: Create specific QMK output files
- **Converter**: Orchestrate the overall conversion process

### 2. Extensibility
The architecture supports easy addition of:
- New hardware features (RGB, Audio, etc.)
- New controller types (Elite-C, STM32, etc.)
- New output formats (additional QMK files)
- Enhanced validation and error checking

### 3. Testability
Each layer can be tested independently:
- Parser unit tests with mock YAML data
- Generator unit tests with mock data models
- Integration tests for end-to-end conversion
- Validation tests against real QMK compilation

## 🔄 Data Flow Architecture

### Stage 1: Input Processing
```python
# Ergogen YAML → Parsed Data Structure
ergogen_file: str → ErgogenData: dict
```

**Responsibilities:**
- YAML syntax validation
- Structure validation (required sections present)
- Basic data type checking
- Error reporting with line numbers

**Key Components:**
- `ErgogenParser.parse_file()`
- YAML error handling
- Schema validation

### Stage 2: Data Extraction
```python
# Parsed YAML → Structured Hardware Configuration
ErgogenData: dict → QMKHardwareModel: object
```

**Extraction Operations:**
1. **Matrix Analysis**: Zones → Rows/Columns → Matrix size
2. **Pin Mapping**: Controller params → Pin assignments
3. **Feature Detection**: Footprints → Hardware features
4. **Layout Extraction**: Points → Physical coordinates

**Key Functions:**
```python
def extract_matrix_config(zones: dict) -> MatrixConfig:
    """Extract matrix rows/cols and pin assignments."""
    
def extract_hardware_features(footprints: dict) -> HardwareFeatures:
    """Detect encoders, OLED, RGB, etc."""
    
def extract_physical_layout(points: dict) -> PhysicalLayout:
    """Convert Ergogen coordinates to layout data."""
```

### Stage 3: QMK Generation
```python
# Hardware Model → QMK Configuration Files
QMKHardwareModel: object → [config.h, keyboard.h, rules.mk, info.json]
```

**Generation Pipeline:**
1. **Config Generator**: Hardware → C preprocessor definitions
2. **Keyboard Generator**: Layout → C layout macros
3. **Rules Generator**: Features → Makefile configuration
4. **Info Generator**: Physical → JSON layout data

## 🏛 Component Architecture

### Parser Layer (`parsers/`)

```python
class ErgogenParser:
    """Main parser for Ergogen YAML files."""
    
    def parse_file(self, filepath: str) -> ErgogenData:
        """Parse YAML file and return structured data."""
        
    def validate_structure(self, data: dict) -> List[str]:
        """Validate required sections are present."""
        
    def extract_metadata(self, data: dict) -> KeyboardMetadata:
        """Extract keyboard name, version, author, etc."""
```

**Sub-parsers:**
- `MatrixParser`: Extract matrix configuration from zones
- `PinParser`: Extract pin assignments from controller
- `FeatureParser`: Detect hardware features from footprints
- `LayoutParser`: Extract physical layout from points

### Data Model Layer (`data_models/`)

```python
@dataclass
class QMKHardwareModel:
    """Complete QMK hardware configuration."""
    metadata: KeyboardMetadata
    matrix: MatrixConfig
    pins: PinMapping
    features: HardwareFeatures
    layout: PhysicalLayout
    
    def validate(self) -> List[str]:
        """Validate the complete hardware model."""
        
    def to_dict(self) -> dict:
        """Export to dictionary for debugging/serialization."""
```

**Sub-models:**
```python
@dataclass
class MatrixConfig:
    rows: int
    cols: int
    row_pins: List[str]
    col_pins: List[str]
    
@dataclass
class HardwareFeatures:
    encoders: List[EncoderConfig]
    displays: List[DisplayConfig] 
    rgb: Optional[RGBConfig]
    audio: Optional[AudioConfig]
    
@dataclass
class PhysicalLayout:
    keys: List[KeyPosition]
    width_mm: float
    height_mm: float
```

### Generator Layer (`generators/`)

```python
class BaseGenerator:
    """Base class for all QMK file generators."""
    
    def generate(self, model: QMKHardwareModel, output_path: str) -> None:
        """Generate QMK file from hardware model."""
        
    def validate_output(self, output_path: str) -> List[str]:
        """Validate generated file syntax."""
```

**Concrete Generators:**
- `ConfigGenerator`: Generate config.h with #defines
- `KeyboardGenerator`: Generate keyboard.h with layouts
- `RulesGenerator`: Generate rules.mk with build config
- `InfoGenerator`: Generate info.json with metadata

### Converter Layer (`ergogen_converter.py`)

```python
class ErgogenConverter:
    """Main orchestrator for the conversion process."""
    
    def __init__(self):
        self.parser = ErgogenParser()
        self.generators = {
            'config': ConfigGenerator(),
            'keyboard': KeyboardGenerator(), 
            'rules': RulesGenerator(),
            'info': InfoGenerator()
        }
    
    def convert_file(self, input_path: str, output_dir: str) -> ConversionResult:
        """Complete conversion from Ergogen to QMK."""
        
    def validate_ergogen_file(self, filepath: str) -> ValidationResult:
        """Validate Ergogen file without conversion."""
```

## 🔍 Key Algorithms

### Matrix Generation Algorithm

```python
def generate_matrix_config(zones: dict) -> MatrixConfig:
    """
    Convert Ergogen zones to QMK matrix configuration.
    
    Algorithm:
    1. Analyze all zones and collect row/column names
    2. Create unified row/column mapping
    3. Determine matrix dimensions
    4. Extract pin assignments from controller
    5. Validate no pin conflicts exist
    """
    all_rows = set()
    all_cols = set()
    
    # Collect all unique row/column identifiers
    for zone_name, zone_data in zones.items():
        for col_name, col_data in zone_data.get('columns', {}).items():
            all_cols.add(col_data.get('key', {}).get('column_net'))
            for row_name in col_data.get('rows', {}):
                all_rows.add(zone_data.get('rows', {}).get(row_name, {}).get('row_net'))
    
    return MatrixConfig(
        rows=len(all_rows),
        cols=len(all_cols),
        row_pins=extract_row_pins(controller_data, all_rows),
        col_pins=extract_col_pins(controller_data, all_cols)
    )
```

### Coordinate Conversion Algorithm

```python
def convert_coordinates(ergogen_points: dict) -> List[KeyPosition]:
    """
    Convert Ergogen mm coordinates to QMK layout positions.
    
    QMK uses key-unit coordinates where 1 unit = 19.05mm
    Ergogen uses absolute mm coordinates with custom anchors
    
    Algorithm:
    1. Calculate absolute position for each key
    2. Find bounding box of all keys  
    3. Normalize to origin (0,0)
    4. Convert mm to key units (÷19.05)
    5. Round to reasonable precision
    """
    KEY_UNIT = 19.05  # mm per key unit
    
    positions = []
    for point_name, point_data in ergogen_points.items():
        # Calculate absolute position considering anchors and shifts
        abs_x, abs_y = calculate_absolute_position(point_data)
        positions.append(KeyPosition(name=point_name, x_mm=abs_x, y_mm=abs_y))
    
    # Normalize and convert to key units
    min_x = min(pos.x_mm for pos in positions)
    min_y = min(pos.y_mm for pos in positions)
    
    return [
        KeyPosition(
            name=pos.name,
            x=round((pos.x_mm - min_x) / KEY_UNIT, 2),
            y=round((pos.y_mm - min_y) / KEY_UNIT, 2)
        ) for pos in positions
    ]
```

## 🛠 Error Handling Strategy

### Hierarchical Error Reporting

1. **Parse Errors**: YAML syntax, missing sections
2. **Validation Errors**: Invalid pin assignments, matrix conflicts  
3. **Generation Errors**: Template rendering, file writing
4. **Post-Generation Validation**: QMK compilation compatibility

```python
@dataclass
class ConversionResult:
    success: bool
    output_files: List[str]
    warnings: List[str]
    errors: List[str]
    
    def has_critical_errors(self) -> bool:
        return len(self.errors) > 0
```

### Error Context Preservation

```python
class ErgogenParseError(Exception):
    def __init__(self, message: str, yaml_path: str, line_number: int):
        self.message = message
        self.yaml_path = yaml_path  # e.g., "points.zones.numpad.columns.col0"
        self.line_number = line_number
        super().__init__(f"{message} at {yaml_path}:{line_number}")
```

## 🧪 Testing Architecture

### Unit Tests
- **Parser Tests**: Mock YAML data → Expected parsed structures
- **Generator Tests**: Mock hardware models → Expected output files
- **Model Tests**: Data validation and transformation

### Integration Tests  
- **End-to-End**: Real Ergogen files → Generated QMK configs
- **QMK Compilation**: Generated configs → Successful QMK build
- **Round-Trip**: Ergogen → QMK → Functional keyboard

### Test Data Management
```
tests/
├── sample_files/
│   ├── config_4x5.yaml        # Primary test case
│   ├── minimal_keyboard.yaml   # Simplest valid case
│   └── complex_split.yaml      # Advanced features test
├── expected_output/
│   ├── config_4x5/
│   │   ├── config.h
│   │   ├── keyboard.h  
│   │   ├── rules.mk
│   │   └── info.json
│   └── ...
└── test_*.py
```

## 🚀 Performance Considerations

### Memory Management
- Stream YAML parsing for large files
- Lazy evaluation of coordinate calculations
- Generator output streaming

### Processing Speed
- Parallel generation of independent files
- Cached template compilation
- Incremental validation (fail fast)

### Scalability
- Support for multiple keyboard definitions in one file
- Batch processing capabilities
- Plugin architecture for custom generators

---

This architecture provides a solid foundation for reliable Ergogen to QMK conversion while maintaining flexibility for future enhancements.
