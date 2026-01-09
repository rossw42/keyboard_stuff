# Requirements Document

## Introduction

This project aims to create the Through-Hole Keyboard Generator (THKG), an automated design tool that generates complete keyboard designs from high-level specifications. The tool will leverage the Through-Hole Keyboard Library's reference designs and proven circuit patterns to produce manufacturing-ready PCB files, plate designs, case models, and firmware configurations. This enables advanced users to rapidly prototype and iterate on custom through-hole keyboard designs without manual PCB layout work.

## Glossary

- **THKG (Through-Hole Keyboard Generator)**: The automated design generation tool
- **KLE (Keyboard Layout Editor)**: Web-based tool for defining keyboard layouts, produces JSON format
- **Matrix**: The row/column wiring configuration that connects switches to the MCU
- **Template**: Proven circuit block extracted from reference designs (USB, MCU, reset circuits)
- **Plate**: The mounting plate that holds switches in position
- **Sandwich Mount**: Case style using stacked layers (acrylic, FR4, etc.)
- **Gerber Files**: Manufacturing files for PCB fabrication
- **DXF**: CAD file format for 2D designs (plates, case layers)
- **STL**: 3D model format for printing
- **QMK**: Open-source keyboard firmware
- **VIA**: GUI tool for configuring QMK keyboards
- **pcbnew**: KiCad's Python API for PCB manipulation

## Requirements

### Requirement 1: Input Configuration System

**User Story:** As a keyboard designer, I want to describe my keyboard idea in natural language or select from common layouts, so that I can quickly start a design without learning complex configuration formats.

#### Acceptance Criteria

1. THE System SHALL accept keyboard descriptions in natural language (e.g., "60% keyboard with rotary encoder")
2. WHEN natural language is provided, THE System SHALL parse the description and extract key parameters (layout, features, MCU)
3. THE System SHALL present users with common layout options (keyboard, numpad, macropad) with visual previews
4. THE System SHALL support importing layouts from KLE (Keyboard Layout Editor) JSON format for custom layouts
5. THE System SHALL provide an interactive guided mode that asks questions and shows options with examples
6. WHERE ambiguous descriptions are provided, THE System SHALL ask clarifying questions with visual examples
7. THE System SHALL generate and display a YAML configuration for user review and modification

### Requirement 2: Layout Processing Engine

**User Story:** As a keyboard designer, I want the system to calculate switch positions and matrix wiring automatically, so that I don't have to manually determine optimal row/column configurations.

#### Acceptance Criteria

1. WHEN a layout is provided, THE System SHALL calculate physical switch positions in millimeters
2. THE System SHALL determine optimal matrix dimensions (rows × columns) based on key count
3. THE System SHALL assign each switch to a matrix position (row, column)
4. THE System SHALL calculate MCU pin assignments for matrix rows and columns
5. WHERE stabilizers are needed, THE System SHALL identify stabilizer positions and sizes

### Requirement 3: Circuit Template Management

**User Story:** As a keyboard designer, I want to use proven circuit designs from the library, so that my generated PCBs use reliable, tested circuits.

#### Acceptance Criteria

1. THE System SHALL extract circuit templates from the Through-Hole Keyboard Library reference designs
2. WHEN a MCU type is specified, THE System SHALL select the appropriate circuit template (ATmega328P, ATmega32A, Pro Micro)
3. WHEN a USB connector type is specified, THE System SHALL select the appropriate USB circuit template
4. THE System SHALL maintain a library of reusable circuit blocks (reset circuits, crystal oscillators, voltage regulators)
5. WHERE multiple template options exist, THE System SHALL allow user selection or use sensible defaults

### Requirement 4: PCB Generation

**User Story:** As a keyboard designer, I want to generate complete KiCad PCB files automatically, so that I can order PCBs without manual layout work.

#### Acceptance Criteria

1. THE System SHALL generate KiCad schematic files (.kicad_sch) with complete circuits
2. THE System SHALL generate KiCad PCB layout files (.kicad_pcb) with component placement
3. WHEN generating PCB layouts, THE System SHALL place switches according to calculated positions
4. THE System SHALL route matrix traces connecting switches to MCU pins
5. THE System SHALL generate manufacturing-ready Gerber files from the PCB layout

### Requirement 5: Plate Generation

**User Story:** As a keyboard builder, I want to generate plate files automatically, so that I can laser cut or order plates that match my PCB exactly.

#### Acceptance Criteria

1. THE System SHALL generate DXF files for switch plates
2. WHEN generating plates, THE System SHALL create cutouts for each switch position
3. THE System SHALL support multiple switch types (Cherry MX, Alps, Choc)
4. WHERE stabilizers are present, THE System SHALL create appropriate stabilizer cutouts
5. THE System SHALL include mounting hole positions matching the PCB

### Requirement 6: Case Generation

**User Story:** As a keyboard builder, I want to generate case designs automatically, so that I can 3D print or laser cut cases that fit my PCB.

#### Acceptance Criteria

1. THE System SHALL generate 3D case models in STL format for 3D printing
2. THE System SHALL generate DXF files for laser-cut case layers
3. WHEN generating cases, THE System SHALL use PCB dimensions and mounting hole positions
4. THE System SHALL support sandwich mount case style with configurable layer count
5. WHERE USB cutouts are needed, THE System SHALL position them based on PCB USB connector location

### Requirement 7: Firmware Generation

**User Story:** As a keyboard builder, I want to generate QMK firmware configurations automatically, so that I can flash working firmware without manual configuration.

#### Acceptance Criteria

1. THE System SHALL generate QMK configuration files (config.h, rules.mk, info.json)
2. WHEN generating firmware, THE System SHALL configure matrix dimensions and pin assignments
3. THE System SHALL generate a default keymap matching the physical layout
4. THE System SHALL configure VIA support where requested
5. THE System SHALL validate generated firmware compiles successfully with QMK

### Requirement 8: Design Validation

**User Story:** As a keyboard designer, I want the system to validate generated designs, so that I can catch errors before manufacturing.

#### Acceptance Criteria

1. THE System SHALL run KiCad Design Rule Check (DRC) on generated PCBs
2. WHEN validation errors are found, THE System SHALL report them with clear descriptions
3. THE System SHALL verify all matrix connections are complete
4. THE System SHALL check component clearances meet manufacturing requirements
5. THE System SHALL validate mounting hole positions match standard specifications

### Requirement 9: Output Packaging

**User Story:** As a keyboard designer, I want all generated files organized and documented, so that I can easily manufacture and build the keyboard.

#### Acceptance Criteria

1. THE System SHALL organize all output files in a structured directory
2. WHEN generation is complete, THE System SHALL create a README with build instructions
3. THE System SHALL generate a BOM (Bill of Materials) with component specifications
4. THE System SHALL include links to component sourcing from the library database
5. THE System SHALL create a summary document listing all generated files and next steps

### Requirement 10: Template Extraction

**User Story:** As a system maintainer, I want to extract circuit templates from library designs, so that the generator has proven circuits to work with.

#### Acceptance Criteria

1. THE System SHALL parse KiCad files from the Through-Hole Keyboard Library
2. WHEN parsing designs, THE System SHALL identify reusable circuit blocks
3. THE System SHALL extract component values and connections for each template
4. THE System SHALL document template requirements (input/output pins, power requirements)
5. THE System SHALL validate extracted templates against original designs

### Requirement 11: Multi-Layout Support

**User Story:** As a keyboard designer, I want to generate different keyboard form factors, so that I can create 60%, 65%, TKL, and custom layouts.

#### Acceptance Criteria

1. THE System SHALL support standard layouts (60% ANSI, 65%, TKL, 40%)
2. WHEN a standard layout is specified, THE System SHALL use predefined dimensions and mounting holes
3. THE System SHALL support custom layouts with user-defined switch positions
4. THE System SHALL validate custom layouts meet minimum spacing requirements
5. WHERE layouts require specific features, THE System SHALL configure them automatically (split spacebar, ISO enter, etc.)

### Requirement 12: Incremental Generation

**User Story:** As a keyboard designer, I want to generate individual components separately, so that I can iterate on specific parts without regenerating everything.

#### Acceptance Criteria

1. THE System SHALL support generating only plate files without PCB
2. THE System SHALL support generating only firmware without hardware files
3. THE System SHALL support generating only case files from existing PCB
4. WHEN regenerating components, THE System SHALL preserve previous outputs
5. THE System SHALL detect when inputs have changed and suggest regeneration

### Requirement 13: Error Recovery

**User Story:** As a keyboard designer, I want helpful error messages when generation fails, so that I can fix issues and retry.

#### Acceptance Criteria

1. WHEN generation fails, THE System SHALL provide clear error messages
2. THE System SHALL suggest fixes for common errors
3. THE System SHALL preserve partial outputs for debugging
4. WHERE possible, THE System SHALL continue generation after non-critical errors
5. THE System SHALL log detailed information for troubleshooting

### Requirement 14: Configuration Presets

**User Story:** As a keyboard designer, I want to use preset configurations for common designs, so that I can quickly generate standard keyboards.

#### Acceptance Criteria

1. THE System SHALL provide preset configurations for common layouts (60% ANSI, 65%, etc.)
2. WHEN a preset is selected, THE System SHALL populate all required configuration values
3. THE System SHALL allow overriding preset values with custom settings
4. THE System SHALL document available presets and their specifications
5. THE System SHALL allow saving custom configurations as new presets

### Requirement 15: Library Integration

**User Story:** As a keyboard designer, I want the generator to use information from the library, so that I benefit from proven designs and components.

#### Acceptance Criteria

1. THE System SHALL require the Through-Hole Keyboard Library to be present for template extraction
2. WHEN generating BOMs, THE System SHALL use component data from the library's master BOM
3. THE System SHALL validate generated designs against library specifications
4. THE System SHALL use library documentation to generate build guides
5. WHERE library updates occur, THE System SHALL detect and use updated information

### Requirement 16: Aesthetic and Artistic Design

**User Story:** As a keyboard designer, I want to create visually striking keyboards with exposed components, so that my keyboard is both functional and an art piece.

#### Acceptance Criteria

1. THE System SHALL support component placement that emphasizes visual aesthetics (visible components as design elements)
2. WHEN generating PCB layouts, THE System SHALL provide options for component arrangement (grid patterns, artistic layouts)
3. THE System SHALL support silkscreen artwork and custom PCB graphics
4. THE System SHALL allow specification of component colors and finishes (gold-plated, colored resistors)
5. WHERE through-hole components are used, THE System SHALL optimize placement for visual appeal while maintaining functionality

