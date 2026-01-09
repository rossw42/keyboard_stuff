# Requirements Document: 60% Keyboard Case - Low-Profile Variant

## Introduction

This document specifies the requirements for a low-profile variant of the 60% keyboard case. The low-profile design aims to reduce the overall height while maintaining compatibility with the same PCB and mounting system. The primary goals are improved portability, sleeker aesthetics, and a more ergonomic typing experience with reduced wrist strain.

Key differences from the standard variant:
- Reduced overall height (14mm total vs 20mm standard - 30% reduction)
- Thinner top frame design (3mm vs 5mm)
- Shallower cavity depth in bottom tray (8mm vs 10mm)
- Maintained PCB compatibility and mounting system
- Same external footprint (295mm x 105mm)
- Safe component clearance (4.4mm below PCB)

## Requirements

### Requirement 1: PCB Compatibility

**User Story:** As a keyboard builder, I want the low-profile case to be compatible with the same 60% PCB, so that I can use either case variant with my existing PCB.

#### Acceptance Criteria

1. WHEN the PCB opening is specified THEN the case SHALL provide a 286mm x 95.6mm opening (285mm PCB + 1mm clearance total)
2. WHEN the PCB is installed THEN the case SHALL provide 0.5mm clearance per side with ±0.2mm tolerance
3. WHEN the PCB thickness is considered THEN the case SHALL accommodate standard 1.6mm PCB thickness
4. WHEN the PCB is positioned THEN it SHALL be centered in the case with consistent border on all sides

### Requirement 2: Low-Profile Mounting System

**User Story:** As a keyboard builder, I want a low-profile mounting system that maintains secure PCB attachment, so that the keyboard remains stable despite reduced height.

#### Acceptance Criteria

1. WHEN mounting points are specified THEN the case SHALL use the same 6 mounting hole positions as the standard variant
2. WHEN mounting hole positions are defined THEN they SHALL match the PCB specification exactly with ±0.1mm positional accuracy
3. WHEN PCB screws are specified THEN the case SHALL use M2 screws with 2.2mm clearance holes
4. WHEN standoff height is determined THEN it SHALL be reduced to 2mm (from 3mm standard) to lower PCB position
5. WHEN brass inserts are specified THEN the top frame SHALL use M3 brass inserts (5.7mm OD, 3mm depth minimum)

### Requirement 3: USB Port Access

**User Story:** As a keyboard user, I want easy USB cable access in the low-profile case, so that I can connect my keyboard without interference.

#### Acceptance Criteria

1. WHEN the USB cutout position is specified THEN it SHALL be centered on the top edge of the case
2. WHEN the USB cutout offset is determined THEN it SHALL be 7mm from the PCB opening edge (same as standard)
3. WHEN the USB cutout dimensions are specified THEN it SHALL be 16mm wide with ±0.5mm tolerance
4. WHEN a USB cable is inserted THEN the cutout SHALL allow full insertion without cable strain or case interference
5. WHEN different USB connector types are used THEN the cutout SHALL accommodate Mini-USB, Micro-USB, and USB-C connectors

### Requirement 4: Low-Profile Clearances

**User Story:** As a keyboard builder, I want proper clearances in the low-profile design, so that switches and components fit without interference despite reduced height.

#### Acceptance Criteria

1. WHEN switches are installed THEN the case SHALL provide minimum 4mm clearance below the PCB for switch pins and components (exceeds GH60 low-profile minimum)
2. WHEN the cavity depth is determined THEN it SHALL be 8mm (reduced from 10mm standard) to accommodate low-profile design while maintaining safe clearances
3. WHEN keycaps are installed THEN the case top surface SHALL be positioned to allow full key travel without interference
4. WHEN stabilizers are installed THEN the case SHALL provide clearance for Cherry-style PCB-mounted stabilizers
5. WHEN the PCB position is calculated THEN it SHALL provide 4.4mm clearance: cavity (8mm) - standoff (2mm) - PCB (1.6mm) = 4.4mm

### Requirement 5: Low-Profile Case Dimensions

**User Story:** As a keyboard builder, I want a compact low-profile case, so that the keyboard is more portable and takes up less desk space vertically.

#### Acceptance Criteria

1. WHEN external dimensions are specified THEN the case SHALL maintain 295mm x 105mm footprint (same as standard)
2. WHEN total height is determined THEN the case SHALL be 12-15mm total (reduced from 20mm standard)
3. WHEN wall thickness is specified THEN it SHALL be minimum 3mm for structural integrity in wooden construction
4. WHEN the case bottom is designed THEN it SHALL include provisions for rubber feet or anti-slip material
5. WHEN typing angle is considered THEN the case SHALL support a minimal 0-3 degree typing angle (flatter than standard)

### Requirement 6: Low-Profile Component Heights

**User Story:** As a keyboard builder, I want clearly defined component heights for the low-profile variant, so that I can manufacture the case accurately.

#### Acceptance Criteria

1. WHEN the top frame height is specified THEN it SHALL be 3mm (reduced from 5mm standard, minimum for brass insert depth)
2. WHEN the bottom tray height is specified THEN it SHALL be 11mm (reduced from 15mm standard)
3. WHEN the cavity depth is specified THEN it SHALL be 8mm (reduced from 10mm standard, provides 4.4mm clearance)
4. WHEN the base thickness is calculated THEN it SHALL be 3mm (11mm bottom tray - 8mm cavity = 3mm minimum)
5. WHEN total height is verified THEN top frame (3mm) + bottom tray (11mm) SHALL equal 14mm total

### Requirement 7: CNC Manufacturing Specifications

**User Story:** As a CNC operator, I want precise toolpath specifications for the low-profile variant, so that I can manufacture the case accurately and efficiently.

#### Acceptance Criteria

1. WHEN toolpaths are generated THEN they SHALL account for tool diameter with proper offsets
2. WHEN material stock is specified THEN the design SHALL accommodate 12-20mm hardwood stock
3. WHEN tolerances are specified THEN critical dimensions SHALL maintain ±0.1mm tolerance (mounting holes, PCB opening)
4. WHEN tolerances are specified THEN standard dimensions SHALL maintain ±0.2mm tolerance (external dimensions, non-critical features)
5. WHEN internal corners are machined THEN corner radii SHALL match tool sizes (2mm radius for 4mm endmill)
6. WHEN machining efficiency is considered THEN toolpaths SHALL minimize tool changes and optimize cutting sequences

### Requirement 8: Structural Integrity

**User Story:** As a keyboard user, I want the low-profile case to be structurally sound despite reduced height, so that it doesn't flex or crack during use.

#### Acceptance Criteria

1. WHEN wall thickness is verified THEN it SHALL be minimum 3mm in all areas
2. WHEN base thickness is verified THEN it SHALL be minimum 3mm for adequate strength
3. WHEN material is selected THEN hardwood (walnut, maple, cherry) SHALL be used for strength
4. WHEN stress points are identified THEN mounting areas SHALL have adequate material support
5. WHEN the design is reviewed THEN there SHALL be no thin sections below 3mm that could crack

### Requirement 9: Assembly and Disassembly

**User Story:** As a keyboard builder, I want easy assembly and maintenance of the low-profile case, so that I can build and service my keyboard efficiently.

#### Acceptance Criteria

1. WHEN assembly tools are specified THEN only basic hand tools SHALL be required (hex keys, screwdriver)
2. WHEN finishing is considered THEN components SHALL be finishable before assembly
3. WHEN alignment is considered THEN the design SHALL include features to ensure proper component positioning
4. WHEN disassembly is needed THEN the case SHALL allow non-destructive disassembly for maintenance

### Requirement 10: Documentation and Deliverables

**User Story:** As a keyboard builder and CNC operator, I want comprehensive documentation for the low-profile variant, so that I can manufacture and assemble the case correctly.

#### Acceptance Criteria

1. WHEN technical drawings are created THEN they SHALL include all critical dimensions with tolerances
2. WHEN CNC files are generated THEN they SHALL include toolpaths in standard G-code or JSON format
3. WHEN tolerances are documented THEN critical (±0.1mm) and standard (±0.2mm) tolerances SHALL be clearly marked
4. WHEN assembly instructions are created THEN they SHALL include step-by-step procedures with diagrams
5. WHEN material specifications are documented THEN they SHALL include wood species, grain orientation, and stock dimensions

### Requirement 11: Compatibility with Standard Variant

**User Story:** As a keyboard builder, I want the low-profile variant to share components with the standard variant where possible, so that I can reduce manufacturing complexity and cost.

#### Acceptance Criteria

1. WHEN PCB compatibility is verified THEN both variants SHALL use the same PCB without modification
2. WHEN mounting positions are verified THEN both variants SHALL use identical mounting hole positions
3. WHEN hardware is specified THEN both variants SHALL use the same M2 and M3 screws where possible
4. WHEN external dimensions are verified THEN both variants SHALL have the same 295mm x 105mm footprint
5. WHEN manufacturing is considered THEN both variants SHALL use the same CNC tools and processes where possible

## Design Constraints

### Height Constraints
- Total height: 14mm (within 12-15mm target range)
- Top frame: 3mm (minimum for brass insert depth)
- Bottom tray: 11mm
- Cavity depth: 8mm
- Base thickness: 3mm (meets minimum)

### Clearance Constraints
- Below PCB: 4.4mm (exceeds 4mm recommended, reduced from 5.4mm standard)
- Standoff height: 2mm (reduced from 3mm standard)
- PCB thickness: 1.6mm (standard)
- Accommodates: switch pins (3.3mm), diodes (2mm), SMD components (1mm)

### Manufacturing Constraints
- Same CNC tools as standard variant
- Same material (hardwood)
- Same tolerance specifications
- Fits within 12-20mm stock

## Success Criteria

The low-profile variant will be considered successful when:

1. Total height is 14mm (30% reduction from 20mm standard, within 12-15mm target)
2. PCB compatibility is maintained (same PCB, same mounting positions)
3. All clearances meet recommended requirements (4.4mm below PCB exceeds 4mm minimum)
4. Structural integrity is verified (3mm base thickness, no flex, no thin sections)
5. Manufacturing is feasible with existing CNC tools
6. Assembly process is straightforward with basic hand tools
7. Design validation passes 95%+ of automated checks
8. Compatible with standard GH60/DZ60/BM60 PCBs including bottom-mounted components

## Out of Scope

The following are explicitly out of scope for this variant:

- Different PCB sizes (remains 60% form factor)
- Integrated wrist rest
- Adjustable typing angle mechanism
- RGB lighting integration
- Different mounting systems (remains screw-based)
- Metal construction (remains wooden)
