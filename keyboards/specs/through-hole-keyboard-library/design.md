# Design Document

## Overview

The Through-Hole Keyboard PCB Design Resource Library is a file-based knowledge repository that organizes design files, documentation, and metadata from multiple open-source through-hole keyboard projects. The system uses a structured directory hierarchy with markdown-based catalogs and databases to provide easy access to manufacturing files, component specifications, and design references.

The library is designed to be:
- **Self-contained**: All files stored locally in organized directories
- **Version-controlled**: Compatible with Git for tracking changes
- **Human-readable**: Markdown catalogs and CSV databases
- **Tool-agnostic**: Files usable with standard PCB design and manufacturing tools

## Architecture

### Directory Structure

```
PCB/
├── README.md                          # Library overview and usage guide
├── references.md                      # Existing reference links
├── components.md                      # Existing component tables
├── docs/
│   ├── repository_inventory.md        # Project metadata catalog
│   ├── gh60_pcb_specifications.md     # Standard specifications
│   ├── compatible_pcbs.md             # Compatibility reference
│   ├── manufacturing_guide.md         # PCB ordering guide
│   ├── component_sourcing_guide.md    # Vendor recommendations
│   ├── design_patterns.md             # Common design patterns
│   └── build-guides/
│       ├── discipline/                # Per-project build guides
│       ├── mysterium/
│       ├── lumberjack/
│       └── [other-projects]/
├── gerbers/
│   ├── discipline/
│   │   ├── pcb/                       # Main PCB gerbers
│   │   └── plate/                     # Plate gerbers (if separate)
│   ├── mysterium/
│   ├── lumberjack/
│   └── [other-projects]/
├── design-files/
│   ├── discipline/
│   │   ├── kicad/                     # KiCad project files
│   │   ├── libraries/                 # Custom footprints/symbols
│   │   └── README.md                  # Project-specific notes
│   ├── mysterium/
│   ├── dumbpad/
│   │   └── eagle/                     # Eagle project files
│   └── [other-projects]/
├── 3d-models/
│   ├── cases/
│   │   ├── discipline/
│   │   │   ├── stl/                   # 3D printable files
│   │   │   └── step/                  # CAD-editable files
│   │   └── [other-projects]/
│   ├── plates/
│   │   └── [project-name]/
│   └── accessories/
│       ├── component-cradles/         # Lumberjack-style cradles
│       └── covers/
├── cad-drawings/
│   ├── plates/
│   │   ├── discipline/
│   │   │   └── plate.dxf
│   │   └── [other-projects]/
│   ├── cases/
│   │   └── [project-name]/
│   └── covers/
│       └── [project-name]/
├── boms/
│   ├── master-bom.csv                 # Unified component database
│   ├── discipline/
│   │   └── bom.csv
│   ├── mysterium/
│   │   └── bom.csv
│   └── [other-projects]/
├── firmware/
│   ├── qmk-configs/                   # QMK configuration references
│   │   ├── discipline/
│   │   └── [other-projects]/
│   └── flashing-guides/
│       └── [mcu-type]/
└── templates/
    ├── 60-percent-tht/                # Design templates
    ├── 65-percent-tht/
    └── macropad-tht/
```

### Data Models

#### Project Metadata (repository_inventory.md)

```markdown
## [Project Name]
- **Repository:** [GitHub URL]
- **Layout:** [Form factor and key count]
- **MCU:** [Microcontroller type]
- **USB:** [Connector type]
- **Available Files:**
  - ✅/❌ Gerber files
  - ✅/❌ KiCad/Eagle files
  - ✅/❌ BOM
  - ✅/❌ Build guide
  - ✅/❌ 3D models
  - ✅/❌ DXF drawings
- **QMK Support:** [Yes/No with path]
- **VIA/VIAL Support:** [Yes/No]
- **License:** [License type]
- **Special Features:** [List]
- **Revisions:** [Latest version]
```

#### Master BOM Database (master-bom.csv)

```csv
Component,Value,Footprint,Package,Vendor_Part_No,Category,Min_Qty,Max_Qty,Projects_Using,Notes
Diode,1N4148,DO-35,THT,1N4148,Diodes,47,87,"discipline,mysterium,lumberjack",One per switch
Resistor,10kΩ,Axial,THT,YAGEO RC0603FR-0710KL,Resistors,12,16,"discipline,mysterium,plaid",Pull-up/down
MCU,ATmega328P,DIP-28,THT,ATMEGA328P-PU,Microcontrollers,1,1,"lumberjack,rosaline,plaid-pad",28-pin DIP
...
```

#### Manufacturing Specifications (per project)

```yaml
pcb:
  dimensions:
    length: 285.0mm
    width: 94.6mm
    thickness: 1.6mm
  layers: 2
  material: FR4
  surface_finish: HASL / ENIG
  silkscreen: Both sides
  mounting_holes:
    count: 6
    diameter: 2.0-2.2mm
    positions: [[19.0, 9.5], [266.0, 9.5], ...]
  usb_cutout:
    width: 16.0mm
    position: 142.5mm from left
```

## Components and Interfaces

### File Collection System

**Purpose:** Download and organize files from GitHub repositories

**Components:**
- Repository cloner (Git-based)
- File type detector
- Directory organizer
- Metadata extractor

**Process:**
1. Read repository list from `references.md`
2. Clone each repository to temporary location
3. Identify file types (Gerber, KiCad, STL, DXF, docs)
4. Copy files to appropriate library directories
5. Extract metadata (project name, version, license)
6. Generate project README with file inventory

**Interface:**
```bash
# Script interface
./scripts/collect_repository.sh <github-url> <project-name>

# Example
./scripts/collect_repository.sh https://github.com/coseyfannitutti/discipline discipline
```

### BOM Consolidation System

**Purpose:** Create unified component database from individual project BOMs

**Components:**
- BOM parser (CSV, Markdown, text formats)
- Component normalizer (standardize names/values)
- Deduplicator
- Database generator

**Process:**
1. Scan `boms/[project]/` directories
2. Parse BOM files (multiple formats)
3. Normalize component names and values
4. Deduplicate components across projects
5. Generate `master-bom.csv`
6. Create component category indexes

**Data Normalization Rules:**
- Resistor values: Use kΩ/Ω notation (10kΩ, 5.1kΩ, 75Ω)
- Capacitor values: Use µF/pF notation (0.1µF, 22pF)
- Diode types: Use standard part numbers (1N4148)
- MCU names: Use full part numbers (ATmega328P-PU)

### Documentation Indexer

**Purpose:** Organize and cross-reference documentation

**Components:**
- Markdown parser
- Link validator
- Index generator
- Search metadata creator

**Process:**
1. Scan documentation directories
2. Extract headings and structure
3. Validate internal and external links
4. Generate master index with descriptions
5. Create searchable metadata

**Output:**
```markdown
# Documentation Index

## Build Guides
- [Discipline V2](build-guides/discipline/README.md) - 65% through-hole keyboard
- [Mysterium](build-guides/mysterium/README.md) - TKL through-hole keyboard
...

## Technical Specifications
- [GH60 PCB Specifications](gh60_pcb_specifications.md)
- [Through-Hole Clearances](clearance_requirements.md)
...
```

### Design Pattern Extractor

**Purpose:** Document common design patterns from multiple projects

**Components:**
- Schematic analyzer
- Pattern matcher
- Documentation generator

**Patterns to Extract:**
- Matrix wiring (row/column configurations)
- USB connector implementations
- MCU integration (DIP vs Pro Micro footprint)
- Reset circuit designs
- Crystal oscillator circuits
- Rotary encoder integration
- OLED display connections
- LED indicator circuits

**Output Format:**
```markdown
## USB-C Through-Hole Implementation

### Pattern: Discipline V2 Style

**Components:**
- USB-C connector (12-pin through-hole)
- 2× 5.1kΩ resistors (CC pull-down)
- 2× Zener diodes (3.6V for ESD protection)
- 1× 1.5kΩ resistor (D- pull-up)
- 1× 75Ω resistor (series termination)

**Schematic:**
[Include schematic snippet]

**Used in:** Discipline, Mysterium, Lumberjack (Rev 1.8)
```

## Error Handling

### File Collection Errors

**Missing Files:**
- Log warning with project name and expected file type
- Continue processing other files
- Generate report of missing files

**Invalid File Formats:**
- Skip file with warning
- Log file path and detected format
- Suggest manual review

**Repository Access Errors:**
- Retry with exponential backoff (3 attempts)
- Log error with repository URL
- Continue with next repository

### BOM Processing Errors

**Parse Errors:**
- Log file path and line number
- Skip malformed entries
- Generate error report for manual review

**Component Normalization Failures:**
- Use original component name
- Flag for manual review
- Add to normalization rules for future runs

### Documentation Errors

**Broken Links:**
- Log broken link and source document
- Generate broken link report
- Continue processing

**Missing Images:**
- Log missing image path
- Note in documentation index
- Continue processing

## Testing Strategy

### File Organization Tests

**Test 1: Directory Structure Creation**
- Verify all required directories are created
- Check directory permissions
- Validate naming conventions

**Test 2: File Type Detection**
- Test with known Gerber files (.gbr, .gbl, .gtl, etc.)
- Test with KiCad files (.kicad_pcb, .sch)
- Test with Eagle files (.brd, .sch)
- Test with 3D files (.stl, .step)
- Test with CAD files (.dxf, .svg)

**Test 3: File Organization**
- Verify files copied to correct directories
- Check file naming consistency
- Validate no file overwrites without warning

### BOM Processing Tests

**Test 1: BOM Parsing**
- Test CSV format parsing
- Test Markdown table parsing
- Test plain text BOM parsing
- Verify component extraction accuracy

**Test 2: Component Normalization**
- Test resistor value normalization (10k → 10kΩ)
- Test capacitor value normalization (100nF → 0.1µF)
- Test diode name standardization
- Verify MCU name consistency

**Test 3: Deduplication**
- Test identical component detection
- Test similar component merging
- Verify project list accuracy

### Documentation Tests

**Test 1: Markdown Parsing**
- Test heading extraction
- Test link extraction
- Test table parsing
- Verify metadata extraction

**Test 2: Index Generation**
- Test alphabetical sorting
- Test category grouping
- Verify link accuracy

**Test 3: Search Metadata**
- Test keyword extraction
- Test tag generation
- Verify searchability

### Integration Tests

**Test 1: End-to-End Repository Processing**
- Clone test repository
- Process all file types
- Generate all outputs
- Verify completeness

**Test 2: Multi-Project Processing**
- Process multiple repositories
- Verify no conflicts
- Check master BOM accuracy
- Validate cross-references

**Test 3: Update Handling**
- Process repository twice
- Verify updates detected
- Check version tracking
- Validate no data loss

### Validation Tests

**Test 1: File Integrity**
- Verify Gerber files are valid
- Check KiCad files open correctly
- Validate STL files are printable
- Confirm DXF files are readable

**Test 2: Data Consistency**
- Cross-check BOM quantities
- Verify component references
- Validate project metadata
- Check link integrity

**Test 3: Completeness**
- Verify all documented projects processed
- Check all file types collected
- Validate documentation coverage
- Confirm no missing critical files

## Design Decisions and Rationales

### Decision 1: File-Based Storage vs Database

**Choice:** File-based storage with CSV/Markdown databases

**Rationale:**
- Easy to version control with Git
- Human-readable and editable
- No database server required
- Compatible with standard tools
- Easy to backup and share

### Decision 2: Directory Structure by Project

**Choice:** Organize files by project name, then by file type

**Rationale:**
- Maintains project context
- Easy to find all files for a specific project
- Supports project-specific documentation
- Allows independent project updates

### Decision 3: Master BOM with Project References

**Choice:** Single master BOM with project usage tracking

**Rationale:**
- Easy to see component reuse across projects
- Simplifies bulk ordering
- Identifies common components
- Supports component substitution research

### Decision 4: Preserve Original File Formats

**Choice:** Keep native design files (KiCad, Eagle) without conversion

**Rationale:**
- Maintains full design fidelity
- Supports editing in original tools
- Avoids conversion errors
- Preserves design history

### Decision 5: Markdown for Documentation

**Choice:** Use Markdown for all documentation and catalogs

**Rationale:**
- Human-readable in plain text
- Renders nicely on GitHub
- Easy to edit with any text editor
- Supports tables, links, and formatting
- Version control friendly

### Decision 6: Script-Based Collection

**Choice:** Shell scripts for repository collection and processing

**Rationale:**
- Cross-platform compatible (bash/zsh)
- Easy to understand and modify
- No complex dependencies
- Can be run manually or automated
- Supports incremental updates

## Future Enhancements

### Phase 2 Features

1. **Web-based catalog interface**
   - Searchable project database
   - Component cross-reference tool
   - Visual file browser

2. **Automated component sourcing**
   - Integration with vendor APIs
   - Price comparison
   - Availability checking

3. **Design validation tools**
   - Gerber file viewer
   - DRC (Design Rule Check) automation
   - Compatibility checker

4. **Template generator**
   - Parametric keyboard generator
   - Custom layout support
   - Automated BOM generation

### Phase 3 Features

1. **Community contributions**
   - Submission workflow
   - Review process
   - Version tracking

2. **Advanced search**
   - Component-based search
   - Feature-based filtering
   - Similarity matching

3. **Design comparison**
   - Side-by-side project comparison
   - Component diff tool
   - Feature matrix

4. **Manufacturing integration**
   - Direct PCB ordering
   - Component kit assembly
   - Batch ordering support
