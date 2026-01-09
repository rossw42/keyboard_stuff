# Design Document

## Overview

The Through-Hole Keyboard Generator (THKG) is a Python-based automation tool that generates complete keyboard designs from high-level specifications. The system uses a modular pipeline architecture where each component handles a specific aspect of design generation (PCB, plate, case, firmware). The tool leverages proven circuit templates extracted from the Through-Hole Keyboard Library and combines them with programmatically generated switch matrices to produce reliable, manufacturable designs.

The generator is designed to be:
- **Modular**: Independent components for each output type
- **Template-based**: Uses proven circuits from library
- **Extensible**: Easy to add new MCUs, layouts, features
- **Validated**: Automatic design rule checking
- **Documented**: Generates build guides and BOMs

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    THKG Main Controller                      │
│  - Orchestrates pipeline                                     │
│  - Manages configuration                                     │
│  - Handles error recovery                                    │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌────────▼────────┐
│ Input Parser   │   │ Layout Engine   │
│ - YAML         │   │ - Matrix calc   │
│ - KLE JSON     │   │ - Positioning   │
│ - CLI          │   │ - Pin assign    │
└────────────────┘   └────────┬────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐   ┌────────▼────────┐   ┌───────▼────────┐
│ Template Mgr   │   │ PCB Generator   │   │ Plate Gen      │
│ - Extract      │──▶│ - KiCad API     │   │ - DXF output   │
│ - Validate     │   │ - Routing       │   │ - Cutouts      │
│ - Cache        │   │ - Gerbers       │   │ - Mounting     │
└────────────────┘   └─────────────────┘   └────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐   ┌────────▼────────┐   ┌───────▼────────┐
│ Case Generator │   │ Firmware Gen    │   │ Validator      │
│ - OpenSCAD     │   │ - QMK configs   │   │ - DRC          │
│ - STL/DXF      │   │ - Keymaps       │   │ - Clearance    │
│ - Parametric   │   │ - VIA support   │   │ - Compile test │
└────────────────┘   └─────────────────┘   └────────────────┘
                              │
                     ┌────────▼────────┐
                     │ Output Packager │
                     │ - Organize      │
                     │ - Document      │
                     │ - BOM           │
                     └─────────────────┘
```


### Directory Structure

```
PCB/tools/keyboard-generator/
├── thkg/                          # Main package
│   ├── __init__.py
│   ├── cli.py                     # Command-line interface
│   ├── config.py                  # Configuration management
│   ├── controller.py              # Main orchestrator
│   │
│   ├── input/                     # Input parsers
│   │   ├── __init__.py
│   │   ├── yaml_parser.py         # YAML config parser
│   │   ├── kle_parser.py          # KLE JSON parser
│   │   └── validator.py           # Input validation
│   │
│   ├── layout/                    # Layout engine
│   │   ├── __init__.py
│   │   ├── matrix.py              # Matrix calculation
│   │   ├── positioning.py         # Switch positioning
│   │   ├── pins.py                # Pin assignment
│   │   └── presets.py             # Standard layouts
│   │
│   ├── templates/                 # Circuit templates
│   │   ├── __init__.py
│   │   ├── extractor.py           # Extract from library
│   │   ├── manager.py             # Template management
│   │   ├── atmega328p/            # MCU templates
│   │   ├── atmega32a/
│   │   ├── pro_micro/
│   │   ├── usb/                   # USB templates
│   │   └── features/              # Optional features
│   │
│   ├── pcb/                       # PCB generation
│   │   ├── __init__.py
│   │   ├── schematic.py           # Schematic generation
│   │   ├── layout.py              # PCB layout
│   │   ├── router.py              # Trace routing
│   │   └── gerber.py              # Gerber export
│   │
│   ├── plate/                     # Plate generation
│   │   ├── __init__.py
│   │   ├── generator.py           # Main plate generator
│   │   ├── cutouts.py             # Switch/stab cutouts
│   │   └── dxf_writer.py          # DXF file writing
│   │
│   ├── case/                      # Case generation
│   │   ├── __init__.py
│   │   ├── sandwich.py            # Sandwich mount
│   │   ├── tray.py                # Tray mount
│   │   ├── scad_generator.py     # OpenSCAD code gen
│   │   └── renderer.py            # STL rendering
│   │
│   ├── firmware/                  # Firmware generation
│   │   ├── __init__.py
│   │   ├── qmk_config.py          # QMK config files
│   │   ├── keymap.py              # Keymap generation
│   │   ├── via_config.py          # VIA support
│   │   └── compiler.py            # Firmware validation
│   │
│   ├── validation/                # Design validation
│   │   ├── __init__.py
│   │   ├── drc.py                 # Design rule check
│   │   ├── clearance.py           # Clearance checking
│   │   └── electrical.py          # Electrical validation
│   │
│   └── output/                    # Output packaging
│       ├── __init__.py
│       ├── organizer.py           # File organization
│       ├── bom_generator.py       # BOM creation
│       └── docs_generator.py      # Documentation
│
├── examples/                      # Example configurations
│   ├── 60-ansi.yaml
│   ├── 65-standard.yaml
│   ├── macropad-4x4.yaml
│   └── custom-layout.yaml
│
├── output/                        # Generated designs
│   └── [project-name]/
│       ├── pcb/
│       ├── plate/
│       ├── case/
│       ├── firmware/
│       └── README.md
│
├── tests/                         # Test suite
│   ├── test_input/
│   ├── test_layout/
│   ├── test_pcb/
│   └── test_integration/
│
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup
└── README.md                      # Tool documentation
```


## Data Models

### Configuration Schema (YAML)

```yaml
# Keyboard metadata
keyboard:
  name: "MyKeyboard60"           # Project name
  description: "Custom 60% keyboard"
  version: "1.0"

# Layout definition
layout:
  type: "60-ansi"                # Preset or "custom"
  kle_file: null                 # Optional KLE JSON path
  switches:                      # Custom switch positions
    - {row: 0, col: 0, x: 0, y: 0, width: 1, height: 1}
    # ... more switches

# Hardware configuration
hardware:
  mcu:
    type: "atmega328p"           # atmega328p, atmega32a, pro_micro
    bootloader: "usbasp"         # usbasp, caterina, dfu
  usb:
    type: "usb-c-tht"            # usb-c-tht, usb-mini, usb-micro
    position: "center"           # center, left, right
  crystal:
    frequency: 16                # MHz
    load_capacitance: 22         # pF
  features:
    rotary_encoders: []          # List of encoder positions
    oled: null                   # OLED configuration
    leds: []                     # LED positions
    rgb: false                   # RGB underglow

# Matrix configuration
matrix:
  rows: 5                        # Auto-calculated if not specified
  cols: 14
  diode_direction: "COL2ROW"    # COL2ROW or ROW2COL
  row_pins: ["D0", "D1", "D2", "D3", "D4"]
  col_pins: ["F0", "F1", "F4", "F5", "F6", "F7", "B6", "B5", "B4", "D7", "D6", "D4", "C6", "C7"]

# PCB specifications
pcb:
  dimensions:
    length: 285.0                # mm
    width: 94.6
    thickness: 1.6
  mounting_holes:
    type: "gh60"                 # Use standard pattern
    diameter: 2.0
  edge_cuts:
    corner_radius: 2.0           # mm

# Plate configuration
plate:
  enabled: true
  switch_type: "mx"              # mx, alps, choc
  thickness: 1.5                 # mm
  material: "fr4"                # fr4, acrylic, aluminum

# Case configuration
case:
  enabled: true
  type: "sandwich"               # sandwich, tray, integrated
  layers:
    - {type: "top", thickness: 3, material: "acrylic"}
    - {type: "plate", thickness: 1.5, material: "fr4"}
    - {type: "spacer", thickness: 7, material: "acrylic"}
    - {type: "bottom", thickness: 3, material: "acrylic"}
  feet:
    type: "rubber"               # rubber, screw-in
    positions: 4                 # Number of feet

# Firmware configuration
firmware:
  qmk: true
  via: true
  vial: false
  default_keymap: "ansi"         # ansi, iso, custom

# Output options
output:
  gerbers: true
  kicad_files: true
  plate_dxf: true
  case_stl: true
  case_dxf: true
  firmware: true
  bom: true
  build_guide: true
```


### Internal Data Structures

```python
@dataclass
class Switch:
    """Represents a single switch in the layout"""
    row: int
    col: int
    x: float          # Physical X position (mm)
    y: float          # Physical Y position (mm)
    width: float      # Key width (units)
    height: float     # Key height (units)
    rotation: float   # Rotation angle (degrees)
    stabilizer: Optional[str]  # None, "2u", "6.25u", "7u"

@dataclass
class Matrix:
    """Matrix configuration"""
    rows: int
    cols: int
    diode_direction: str  # "COL2ROW" or "ROW2COL"
    row_pins: List[str]
    col_pins: List[str]
    switch_map: Dict[Tuple[int, int], Switch]  # (row, col) -> Switch

@dataclass
class CircuitTemplate:
    """Reusable circuit block"""
    name: str
    type: str         # "mcu", "usb", "reset", "crystal"
    components: List[Component]
    connections: List[Connection]
    input_pins: List[str]
    output_pins: List[str]
    power_requirements: Dict[str, float]

@dataclass
class Component:
    """Electronic component"""
    reference: str    # "U1", "R1", "C1"
    value: str        # "ATmega328P", "10kΩ", "0.1µF"
    footprint: str    # "DIP-28", "Axial-0.3", "C_Disc_D3.0mm"
    position: Tuple[float, float]  # (x, y) in mm
    rotation: float   # degrees

@dataclass
class PCBDesign:
    """Complete PCB design"""
    schematic: Schematic
    layout: Layout
    components: List[Component]
    traces: List[Trace]
    dimensions: Dimensions
    mounting_holes: List[MountingHole]

@dataclass
class PlateDesign:
    """Plate design"""
    switches: List[Switch]
    cutouts: List[Cutout]
    mounting_holes: List[MountingHole]
    dimensions: Dimensions
    material: str
    thickness: float

@dataclass
class CaseDesign:
    """Case design"""
    layers: List[CaseLayer]
    mounting_posts: List[MountingPost]
    usb_cutout: Cutout
    dimensions: Dimensions
```


## Components and Interfaces

### 1. Input Parser

**Purpose:** Parse and validate user configuration

**Interface:**
```python
class InputParser:
    def parse_yaml(self, yaml_path: str) -> Configuration:
        """Parse YAML configuration file"""
        
    def parse_kle(self, kle_json: str) -> Layout:
        """Parse KLE JSON layout"""
        
    def validate(self, config: Configuration) -> ValidationResult:
        """Validate configuration completeness and correctness"""
        
    def interactive_prompt(self) -> Configuration:
        """Interactive CLI configuration builder"""
```

**Process:**
1. Load configuration file (YAML or KLE JSON)
2. Parse into internal data structures
3. Validate required fields present
4. Check value ranges and constraints
5. Apply defaults for missing optional fields
6. Return validated Configuration object

**Error Handling:**
- Missing required fields → Clear error with field name
- Invalid values → Error with valid options
- File not found → Helpful path suggestion
- Malformed YAML/JSON → Syntax error with line number


### 2. Layout Engine

**Purpose:** Calculate switch positions and matrix configuration

**Interface:**
```python
class LayoutEngine:
    def calculate_positions(self, layout: Layout) -> List[Switch]:
        """Calculate physical switch positions from layout"""
        
    def optimize_matrix(self, switches: List[Switch]) -> Matrix:
        """Determine optimal matrix dimensions and assignments"""
        
    def assign_pins(self, matrix: Matrix, mcu: MCU) -> Matrix:
        """Assign MCU pins to matrix rows/columns"""
```

**Matrix Optimization Algorithm:**
1. Count total switches
2. Calculate factors close to square root (minimize rows+cols)
3. Assign switches to matrix positions
4. Verify no ghosting issues
5. Optimize for minimal trace length

### 3. Template Manager

**Purpose:** Extract and manage circuit templates from library

**Interface:**
```python
class TemplateManager:
    def extract_template(self, design_path: str, template_type: str) -> CircuitTemplate:
        """Extract circuit template from KiCad file"""
        
    def get_template(self, template_name: str) -> CircuitTemplate:
        """Retrieve cached template"""
        
    def list_templates(self) -> List[str]:
        """List available templates"""
```

**Template Extraction Process:**
1. Parse KiCad schematic file
2. Identify circuit block boundaries
3. Extract components and connections
4. Document input/output pins
5. Validate template completeness
6. Cache for reuse

### 4. PCB Generator

**Purpose:** Generate KiCad PCB files using templates and matrix

**Interface:**
```python
class PCBGenerator:
    def generate_schematic(self, config: Configuration, matrix: Matrix, templates: List[CircuitTemplate]) -> Schematic:
        """Generate complete schematic"""
        
    def generate_layout(self, schematic: Schematic, switches: List[Switch]) -> Layout:
        """Generate PCB layout with component placement"""
        
    def route_traces(self, layout: Layout) -> Layout:
        """Route matrix traces"""
        
    def export_gerbers(self, layout: Layout, output_dir: str):
        """Export Gerber manufacturing files"""
```

**Generation Process:**
1. Load circuit templates (MCU, USB, etc.)
2. Generate switch matrix schematic
3. Connect matrix to MCU pins
4. Place components on PCB
5. Route traces (matrix, power, USB)
6. Run DRC (Design Rule Check)
7. Export Gerbers

### 5. Plate Generator

**Purpose:** Generate DXF plate files

**Interface:**
```python
class PlateGenerator:
    def generate_plate(self, switches: List[Switch], config: PlateConfig) -> Plate:
        """Generate plate design"""
        
    def export_dxf(self, plate: Plate, output_path: str):
        """Export plate as DXF file"""
```

**Generation Process:**
1. Create plate outline from PCB dimensions
2. Add switch cutouts at calculated positions
3. Add stabilizer cutouts where needed
4. Add mounting holes
5. Export as DXF

### 6. Case Generator

**Purpose:** Generate case models (STL and DXF)

**Interface:**
```python
class CaseGenerator:
    def generate_case(self, pcb: PCBDesign, config: CaseConfig) -> Case:
        """Generate case design"""
        
    def export_stl(self, case: Case, output_dir: str):
        """Export 3D printable STL files"""
        
    def export_dxf(self, case: Case, output_dir: str):
        """Export laser-cuttable DXF layers"""
```

**Generation Process (Sandwich Mount):**
1. Create layers based on configuration
2. Add mounting posts
3. Add USB cutout
4. Generate screw holes
5. Export each layer as DXF
6. Generate 3D model as STL

### 7. Firmware Generator

**Purpose:** Generate QMK firmware configuration

**Interface:**
```python
class FirmwareGenerator:
    def generate_config(self, matrix: Matrix, config: FirmwareConfig) -> QMKConfig:
        """Generate QMK configuration files"""
        
    def generate_keymap(self, layout: Layout) -> Keymap:
        """Generate default keymap"""
        
    def validate_firmware(self, qmk_dir: str) -> bool:
        """Validate firmware compiles"""
```

**Generation Process:**
1. Create config.h with matrix configuration
2. Create rules.mk with MCU and features
3. Generate info.json for VIA
4. Create default keymap
5. Validate with QMK CLI


## Error Handling

### Input Validation Errors
- **Missing required fields** → List missing fields with examples
- **Invalid values** → Show valid options and current value
- **Conflicting settings** → Explain conflict and suggest resolution

### Generation Errors
- **Template not found** → List available templates
- **Pin assignment failure** → Show pin conflicts and suggest alternatives
- **Routing failure** → Provide manual routing guidance
- **DRC violations** → List violations with locations and fixes

### Output Errors
- **File write failure** → Check permissions and disk space
- **Gerber export failure** → Validate PCB before export
- **Firmware compile failure** → Show QMK error messages

## Testing Strategy

### Unit Tests
- Input parser validation
- Matrix calculation algorithms
- Template extraction
- Pin assignment logic
- DXF generation
- Firmware config generation

### Integration Tests
- End-to-end generation from YAML
- Template + matrix combination
- Multi-component generation
- Error recovery

### Validation Tests
- Generated PCBs pass DRC
- Gerbers are valid
- Firmware compiles
- Plates have correct dimensions
- Cases fit PCBs

## Design Decisions

### Decision 1: Hybrid Template + Generation Approach
**Choice:** Use templates for circuits, generate matrix programmatically
**Rationale:** Proven circuits are reliable, matrix is repetitive and automatable

### Decision 2: KiCad Python API
**Choice:** Use pcbnew for PCB generation
**Rationale:** Native KiCad output, full control, no conversion needed

### Decision 3: Modular Pipeline
**Choice:** Independent components for each output type
**Rationale:** Easier testing, can generate components separately, extensible

### Decision 4: YAML Configuration
**Choice:** YAML as primary config format
**Rationale:** Human-readable, supports comments, widely used, easy to edit

### Decision 5: Library Integration
**Choice:** Reference library for templates, don't duplicate
**Rationale:** Single source of truth, library updates benefit generator

## Future Enhancements

### Phase 2 Features
- Auto-routing optimization
- Multiple MCU support (RP2040, STM32)
- Split keyboard support
- Wireless (nice!nano) support

### Phase 3 Features
- Web-based configuration UI
- Visual layout editor
- Real-time preview
- Cloud generation service

### Phase 4 Features
- AI-assisted routing
- Component placement optimization
- Cost optimization
- Manufacturing partner integration


## Updated Design Decisions (Based on Review)

### Decision 6: Layout Selection (Not Natural Language)
**Choice:** Predefined common layouts with guided selection
**Rationale:** 
- No external LLM dependency
- Predictable, reliable parsing
- Clear options for users
- Can add natural language later as enhancement

**Common Layouts:**
- **Keyboards:** 60% ANSI, 60% ISO, 65%, TKL, 40%
- **Numpads:** Standard 4x5, Compact 4x4, Extended 5x4
- **Macropads:** 3x3, 4x4, 2x3, custom grid

### Decision 7: Auto-Routing Strategy
**Choice:** Auto-route everything
**Rationale:**
- Faster generation
- Consistent results
- Matrix routing is straightforward (grid pattern)
- Users can manually refine if needed

**Routing Priority:**
1. Matrix traces (rows/columns)
2. Power traces (VCC, GND)
3. USB data lines
4. Feature connections (encoder, OLED)

### Decision 8: Artistic Component Placement
**Choice:** Aesthetic-aware placement algorithm
**Rationale:**
- Through-hole keyboards are art pieces
- Visible components should look intentional
- Balance aesthetics with functionality

**Placement Strategies:**
- Grid patterns for resistors/capacitors
- Symmetrical arrangements
- Component alignment
- Visual balance
- Color coordination (future: specify component colors)

### Decision 9: Visual Preview
**Choice:** Generate preview images before fabrication
**Rationale:**
- Critical for artistic designs
- Catch layout issues early
- User confidence before ordering

**Preview Types:**
1. PCB top view (component placement)
2. PCB bottom view (traces)
3. 3D render (if possible)
4. Schematic diagram

**Implementation:** Use KiCad's plot/export functions or external rendering

### Decision 10: Template Management
**Choice:** Use existing extracted templates, cache them
**Rationale:**
- Library already has proven designs
- Extract once, reuse many times
- Faster generation

**Roadmap Item:** Add template re-extraction system for library updates

### Decision 11: Validation Approach
**Choice:** Iterative - adjust as we build
**Rationale:**
- Unknown what warnings are acceptable until we test
- Different users have different tolerance
- Start permissive, tighten as needed

**Initial Approach:**
- Warn on non-critical issues
- Fail only on critical errors (no power, disconnected matrix)
- Log all warnings for review
- Allow user to set strictness level



## Roadmap

### Phase 1: Core PCB Generation (Current Focus)
- ✅ Predefined layout selection
- ✅ Template-based circuit generation
- ✅ Auto-routing
- ✅ Basic component placement
- ✅ Gerber export

### Phase 2: Artistic Enhancements
- 🔲 Aesthetic component placement algorithms
- 🔲 Visual preview generation
- 🔲 Component color/finish specification
- 🔲 Silkscreen artwork support
- 🔲 Custom PCB graphics

### Phase 3: Additional Outputs
- 🔲 Plate generation (DXF)
- 🔲 Case generation (STL/DXF)
- 🔲 Firmware generation (QMK)

### Phase 4: Advanced Features
- 🔲 Natural language input (LLM-based)
- 🔲 Template re-extraction system
- 🔲 Library update detection
- 🔲 Advanced routing optimization
- 🔲 Split keyboard support
- 🔲 Wireless support (nice!nano)

### Phase 5: User Experience
- 🔲 Web-based interface
- 🔲 Real-time 3D preview
- 🔲 Interactive component placement
- 🔲 Design sharing/collaboration
- 🔲 Manufacturing partner integration



## KLE (Keyboard Layout Editor) Integration

### KLE JSON Format Support

**Yes, we can read KLE presets!** KLE uses a JSON format that we can parse using the `kle-serial` library.

**KLE JSON Structure:**
```json
[
  { "name": "60% ANSI", "author": "User" },
  ["Esc", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", {w:2}, "Backspace"],
  [{w:1.5}, "Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", {w:1.5}, "\\"],
  // ... more rows
]
```

**Implementation:**
```python
import json

def parse_kle_json(kle_file):
    """Parse KLE JSON file"""
    with open(kle_file) as f:
        data = json.load(f)
    
    # First element is metadata (optional)
    metadata = data[0] if isinstance(data[0], dict) else {}
    
    # Remaining elements are rows of keys
    rows = data[1:] if metadata else data
    
    # Convert to internal Switch format
    switches = []
    y = 0
    for row in rows:
        x = 0
        for key in row:
            if isinstance(key, dict):
                # Key properties (width, height, etc.)
                width = key.get('w', 1)
                height = key.get('h', 1)
                x += key.get('x', 0)  # X offset
                y += key.get('y', 0)  # Y offset
            else:
                # Key label
                switches.append(Switch(
                    x=x * 19.05,  # Convert units to mm
                    y=y * 19.05,
                    width=width,
                    height=height,
                    label=key
                ))
                x += width
        y += 1
    
    return switches, metadata
```

### Common Layout Presets

**Keyboards (Staggered):**
- 60% ANSI (61 keys) - Standard staggered
- 60% ISO (62 keys) - European staggered
- 65% (68 keys) - Staggered with arrows
- TKL (87 keys) - Tenkeyless staggered
- 40% (47 keys) - Compact staggered

**Keyboards (Ortholinear):**
- 60% Ortho (5x12 = 60 keys) - Grid layout
- 40% Ortho (4x12 = 48 keys) - Planck-style
- 50% Ortho (5x10 = 50 keys) - Preonic-style

**Numpads:**
- Standard (4x5 = 20 keys) - Traditional
- Compact (4x4 = 16 keys) - No top row
- Extended (5x4 = 20 keys) - Extra column

**Macropads:**
- 3x3 (9 keys) - Small
- 4x4 (16 keys) - Medium
- 2x3 (6 keys) - Minimal
- Custom grid (user specifies)

### Layout Selection Flow

```python
def select_layout_interactive():
    # Step 1: Category
    category = prompt_choice("What are you building?",
                            ["Keyboard", "Numpad", "Macropad"])
    
    # Step 2: Layout style (for keyboards)
    if category == "Keyboard":
        style = prompt_choice("Layout style?",
                             ["Staggered (traditional)", 
                              "Ortholinear (grid)",
                              "Custom (import KLE JSON)"])
        
        if style == "Staggered (traditional)":
            layout = prompt_choice("Which size?",
                                  ["60% ANSI", "60% ISO", "65%", "TKL", "40%"])
        elif style == "Ortholinear (grid)":
            layout = prompt_choice("Which size?",
                                  ["60% Ortho (5x12)", "40% Ortho (4x12)", "50% Ortho (5x10)"])
        else:  # Custom
            kle_file = prompt_file("Select KLE JSON file")
            layout = parse_kle_json(kle_file)
    
    elif category == "Numpad":
        layout = prompt_choice("Which layout?",
                              ["Standard (4x5)", "Compact (4x4)", "Extended (5x4)"])
    
    elif category == "Macropad":
        layout = prompt_choice("Which layout?",
                              ["3x3 (9 keys)", "4x4 (16 keys)", "2x3 (6 keys)", 
                               "Custom grid", "Custom (import KLE JSON)"])
        
        if layout == "Custom grid":
            rows = prompt_number("How many rows?", min=2, max=6)
            cols = prompt_number("How many columns?", min=2, max=6)
            layout = generate_grid_layout(rows, cols)
        elif layout == "Custom (import KLE JSON)":
            kle_file = prompt_file("Select KLE JSON file")
            layout = parse_kle_json(kle_file)
    
    return layout
```

### Staggered vs Ortholinear

**Staggered Layouts:**
- Traditional keyboard layout
- Rows offset horizontally
- Matches typing muscle memory
- Examples: Most commercial keyboards

**Ortholinear Layouts:**
- Grid-based layout
- No horizontal offset
- Claimed ergonomic benefits
- Examples: Planck, Preonic, Lumberjack

**Implementation Difference:**
```python
# Staggered: Each row has X offset
def generate_staggered_60():
    offsets = [0, 0.25, 0.5, 0.75, 0]  # Row offsets in units
    # Apply offset when calculating positions
    
# Ortholinear: No offset, pure grid
def generate_ortho_60():
    # Simple grid calculation
    for row in range(5):
        for col in range(12):
            x = col * 19.05
            y = row * 19.05
```

