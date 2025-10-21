# Requirements Document

## Introduction

This project aims to create a comprehensive Through-Hole Keyboard PCB Design Resource Library that consolidates design files, documentation, components, and tools from multiple open-source through-hole keyboard projects. The library will enable makers, hobbyists, and keyboard enthusiasts to easily access reference designs, understand component requirements, and create their own through-hole mechanical keyboards with minimal friction.

## Glossary

- **THT (Through-Hole Technology)**: Electronic components with leads that pass through holes in the PCB and are soldered on the opposite side
- **Gerber Files**: Standard file format for PCB manufacturing containing layer information
- **KiCad**: Open-source PCB design software
- **BOM (Bill of Materials)**: List of components required to build a keyboard
- **QMK**: Open-source keyboard firmware
- **MCU (Microcontroller Unit)**: The processor that runs keyboard firmware (e.g., ATmega328P, Pro Micro)
- **Resource Library**: Organized collection of design files, documentation, and tools
- **DXF**: CAD file format for 2D drawings (plates, cases)
- **STL**: 3D model file format for printing
- **Form Factor**: Keyboard size/layout (60%, 65%, TKL, 40%, macropad)

## Requirements

### Requirement 1: Repository File Collection

**User Story:** As a keyboard designer, I want access to all design files from multiple through-hole keyboard projects, so that I can reference proven designs and reuse components.

#### Acceptance Criteria

1. WHEN the Resource Library is initialized, THE System SHALL download design files from all documented GitHub repositories
2. WHEN design files are downloaded, THE System SHALL organize files by project name and file type
3. WHEN organizing files, THE System SHALL create separate directories for Gerber files, KiCad files, Eagle files, STL files, DXF files, and documentation
4. WHEN a repository contains multiple file types, THE System SHALL extract and categorize each file type into its appropriate directory
5. WHERE a project has multiple revisions, THE System SHALL preserve the latest revision with clear version labeling

### Requirement 2: Component Database

**User Story:** As a keyboard builder, I want a unified component database with specifications and sources, so that I can quickly identify and purchase the parts I need.

#### Acceptance Criteria

1. THE System SHALL create a master BOM database containing all components from documented projects
2. WHEN components are cataloged, THE System SHALL include component name, value, footprint, typical vendor part number, and quantity ranges
3. WHEN duplicate components exist across projects, THE System SHALL deduplicate entries and list all projects using that component
4. THE System SHALL organize components by category (microcontrollers, diodes, resistors, capacitors, connectors, optional components)
5. WHERE vendor part numbers are available, THE System SHALL include them in the component database

### Requirement 3: Documentation Organization

**User Story:** As a first-time keyboard builder, I want organized build guides and documentation, so that I can learn how to assemble through-hole keyboards.

#### Acceptance Criteria

1. THE System SHALL collect build guides from all documented projects
2. WHEN build guides are collected, THE System SHALL organize them by project name in a dedicated documentation directory
3. THE System SHALL create a master index document linking to all build guides
4. WHEN projects include flashing instructions, THE System SHALL include them in the documentation collection
5. THE System SHALL preserve original documentation formatting and images

### Requirement 4: Design File Accessibility

**User Story:** As a PCB designer, I want easy access to source design files in native formats, so that I can modify and adapt existing designs.

#### Acceptance Criteria

1. THE System SHALL preserve native design files (KiCad .kicad_pcb, .sch, Eagle .brd, .sch)
2. WHEN design files are stored, THE System SHALL maintain the original directory structure for each project
3. THE System SHALL include footprint libraries and custom components where available
4. WHERE projects include case files, THE System SHALL store them in a dedicated cases directory
5. THE System SHALL create a catalog document listing all available design files by project

### Requirement 5: Manufacturing File Preparation

**User Story:** As someone ordering PCBs, I want ready-to-manufacture Gerber files, so that I can quickly send files to PCB fabricators.

#### Acceptance Criteria

1. THE System SHALL organize Gerber files by project in a dedicated gerbers directory
2. WHEN Gerber files are stored, THE System SHALL preserve the original ZIP archives where available
3. THE System SHALL document PCB specifications (dimensions, layer count, thickness) for each project
4. WHERE plate Gerber files exist, THE System SHALL store them separately from main PCB Gerbers
5. THE System SHALL create a manufacturing guide document with recommended PCB settings

### Requirement 6: 3D Model Library

**User Story:** As a case designer, I want access to 3D models and mechanical drawings, so that I can design compatible cases and accessories.

#### Acceptance Criteria

1. THE System SHALL collect all STL files from documented projects
2. WHEN STL files are collected, THE System SHALL organize them by project and component type (case, plate, accessories)
3. THE System SHALL collect all DXF files for laser cutting and CNC machining
4. WHERE projects include STEP files, THE System SHALL include them in the 3D model library
5. THE System SHALL create a catalog of available 3D models with descriptions

### Requirement 7: Reference Specifications

**User Story:** As a keyboard designer, I want standardized specifications and dimensions, so that I can ensure compatibility with existing cases and components.

#### Acceptance Criteria

1. THE System SHALL document standard form factor dimensions (60%, 65%, TKL, 40%)
2. WHEN documenting dimensions, THE System SHALL include PCB outline, mounting hole positions, and USB cutout locations
3. THE System SHALL document clearance requirements for through-hole components
4. THE System SHALL include switch spacing and plate specifications
5. WHERE multiple standards exist for a form factor, THE System SHALL document all variants

### Requirement 8: Project Metadata

**User Story:** As a library user, I want searchable project metadata, so that I can quickly find projects matching my requirements.

#### Acceptance Criteria

1. THE System SHALL create a project inventory document with metadata for each project
2. WHEN cataloging projects, THE System SHALL include layout type, key count, MCU type, USB connector type, and special features
3. THE System SHALL document firmware support (QMK, VIA, VIAL, ZMK) for each project
4. THE System SHALL include license information for each project
5. THE System SHALL provide links to original repositories and maintainer information

### Requirement 9: Component Sourcing Guide

**User Story:** As a keyboard builder, I want component sourcing recommendations, so that I can purchase parts from reliable vendors.

#### Acceptance Criteria

1. THE System SHALL create a vendor guide listing recommended suppliers for common components
2. WHEN listing vendors, THE System SHALL include vendor names, URLs, and component categories
3. THE System SHALL document typical lead times and minimum order quantities where applicable
4. THE System SHALL include alternative part numbers for common components
5. WHERE projects use specialized components, THE System SHALL document specific sourcing information

### Requirement 10: Design Pattern Documentation

**User Story:** As a PCB designer, I want documented design patterns and best practices, so that I can create reliable through-hole keyboard designs.

#### Acceptance Criteria

1. THE System SHALL document common matrix wiring patterns used across projects
2. WHEN documenting patterns, THE System SHALL include schematic examples and explanations
3. THE System SHALL document USB connector implementations (through-hole USB-C, Mini, Micro)
4. THE System SHALL document MCU integration patterns (DIP AVR, Pro Micro footprint)
5. THE System SHALL document optional feature implementations (rotary encoders, OLEDs, LEDs)
