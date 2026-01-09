# Requirements Document

## Introduction

This document outlines the requirements for designing and manufacturing a wooden keyboard case for 60% mechanical keyboard PCBs via CNC machining. The case must be compatible with GH60, BM60, and Pok3r PCBs, which share identical dimensions, mounting points, and USB port placement. The design will focus on creating precise CNC toolpaths for wooden case production with proper tolerances for PCB mounting, switch clearance, and USB connectivity.

## Requirements

### Requirement 1: PCB Compatibility

**User Story:** As a keyboard builder, I want the case to fit standard 60% PCBs (GH60, BM60, Pok3r), so that I can use any of these interchangeable PCBs without modification.

#### Acceptance Criteria

1. WHEN the PCB is placed in the case THEN the case SHALL accommodate a PCB measuring 285mm x 94.6mm with ±0.2mm tolerance
2. WHEN the PCB is installed THEN the case SHALL provide clearance for the standard 1.6mm PCB thickness
3. WHEN any of the three PCB types (GH60, BM60, Pok3r) is used THEN the case SHALL fit without requiring modifications

### Requirement 2: Mounting System

**User Story:** As a keyboard builder, I want secure PCB mounting points, so that the PCB remains stable during typing and doesn't shift or flex.

#### Acceptance Criteria

1. WHEN the case is manufactured THEN it SHALL include 6 mounting points matching the standard 60% PCB layout
2. WHEN mounting holes are positioned THEN they SHALL be located at:
   - Top-left: 19mm from left edge, 9.5mm from top edge
   - Top-right: 266mm from left edge, 9.5mm from top edge
   - Middle-left: 28.5mm from left edge, 47.3mm from top edge
   - Middle-right: 256.5mm from left edge, 47.3mm from top edge
   - Bottom-left: 57mm from left edge, 85mm from top edge
   - Bottom-right: 228mm from left edge, 85mm from top edge
3. WHEN mounting hardware is specified THEN the case SHALL support M2 screws with appropriate standoff heights
4. WHEN the PCB is mounted THEN the mounting system SHALL provide ±0.1mm positional accuracy for each mounting point
5. WHEN screws are tightened THEN the case SHALL prevent over-tightening damage through integrated standoffs or brass inserts

### Requirement 3: USB Port Access

**User Story:** As a keyboard user, I want unobstructed access to the USB port, so that I can connect and disconnect the cable without interference.

#### Acceptance Criteria

1. WHEN the USB cutout is positioned THEN it SHALL be centered on the top edge of the case
2. WHEN the USB port location is measured THEN the cutout SHALL be positioned approximately 7mm from the top edge of the PCB
3. WHEN the USB cutout dimensions are specified THEN it SHALL provide adequate clearance for Mini-USB, Micro-USB, or USB-C connectors with ±0.5mm tolerance
4. WHEN a USB cable is inserted THEN the cutout SHALL allow full insertion without cable strain or case interference
5. WHEN different USB connector types are used THEN the cutout SHALL accommodate the largest common connector type

### Requirement 4: Switch and Keycap Clearance

**User Story:** As a keyboard builder, I want proper clearance for mechanical switches and keycaps, so that keys can be pressed without bottoming out on the case.

#### Acceptance Criteria

1. WHEN switches are installed THEN the case SHALL provide minimum 5mm clearance below the PCB for switch pins and components
2. WHEN keycaps are installed THEN the case top surface SHALL be positioned to allow full key travel without interference
3. WHEN the switch plate is considered THEN the case SHALL accommodate both plate-mounted and PCB-mounted switch configurations
4. WHEN stabilizers are installed THEN the case SHALL provide clearance for Cherry-style PCB-mounted stabilizers

### Requirement 5: Case Dimensions and Structure

**User Story:** As a keyboard builder, I want a structurally sound case with appropriate dimensions, so that the keyboard is stable and aesthetically pleasing.

#### Acceptance Criteria

1. WHEN external dimensions are specified THEN the case SHALL have outer dimensions of approximately 295mm x 105mm (allowing 5mm border around PCB)
2. WHEN case height is determined THEN it SHALL be sufficient to accommodate PCB, switches, and provide typing angle options
3. WHEN wall thickness is specified THEN it SHALL be minimum 3mm for structural integrity in wooden construction
4. WHEN the case bottom is designed THEN it SHALL include provisions for rubber feet or anti-slip material
5. WHEN typing angle is considered THEN the case SHALL support a 5-7 degree typing angle

### Requirement 6: CNC Manufacturing Specifications

**User Story:** As a CNC operator, I want precise toolpath specifications, so that I can manufacture the case accurately and efficiently.

#### Acceptance Criteria

1. WHEN CNC toolpaths are generated THEN they SHALL account for tool diameter and provide appropriate offsets
2. WHEN material is specified THEN the design SHALL accommodate common hardwoods (walnut, maple, cherry) with 12-20mm thickness
3. WHEN tolerances are specified THEN critical dimensions SHALL maintain ±0.1mm accuracy and non-critical dimensions ±0.2mm
4. WHEN machining operations are planned THEN the design SHALL minimize tool changes and optimize cutting efficiency
5. WHEN internal corners are specified THEN they SHALL use appropriate radius fillets matching available tool sizes (minimum 1.5mm radius for 3mm endmill)

### Requirement 7: Assembly and Finishing

**User Story:** As a keyboard builder, I want straightforward assembly and finishing options, so that I can complete the build efficiently.

#### Acceptance Criteria

1. WHEN assembly is performed THEN the case SHALL require no more than basic hand tools (screwdriver, hex keys)
2. WHEN case components are designed THEN they SHALL allow for wood finishing (sanding, oiling, or sealing) before assembly
3. WHEN the design includes multiple pieces THEN alignment features SHALL ensure proper component positioning
4. WHEN disassembly is needed THEN the case SHALL allow non-destructive disassembly for maintenance or modifications

### Requirement 8: Design Documentation

**User Story:** As a case manufacturer, I want complete technical documentation, so that I can produce the case without ambiguity.

#### Acceptance Criteria

1. WHEN documentation is provided THEN it SHALL include 2D technical drawings with all critical dimensions
2. WHEN CNC files are delivered THEN they SHALL be in standard formats (DXF, SVG, or G-code)
3. WHEN tolerances are documented THEN they SHALL be clearly marked on all technical drawings
4. WHEN assembly is documented THEN it SHALL include exploded views and hardware specifications
5. WHEN material specifications are provided THEN they SHALL include recommended wood types, grain orientation, and thickness requirements
