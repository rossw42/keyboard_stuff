# Repository Collection Scripts

This directory contains scripts for collecting, organizing, and cataloging through-hole keyboard projects from GitHub repositories.

## Overview

The repository collection system consists of three main scripts that work together to process open-source keyboard projects:

1. **collect_repository.sh** - Clones GitHub repositories with retry logic
2. **organize_files.sh** - Detects file types and organizes them into the library structure
3. **extract_metadata.sh** - Extracts project information and generates documentation

A master script **process_repository.sh** orchestrates all three steps for convenience.

## Quick Start

### Process a Single Repository

```bash
./scripts/process_repository.sh <github-url> <project-name>
```

**Example:**
```bash
./scripts/process_repository.sh https://github.com/coseyfannitutti/discipline discipline
```

This will:
1. Clone the repository to `.temp/discipline/`
2. Organize files into the PCB directory structure
3. Generate project documentation and update the inventory

### Process Multiple Repositories

Create a batch script or loop through repositories:

```bash
#!/bin/bash

# List of repositories to process
repos=(
    "https://github.com/coseyfannitutti/discipline:discipline"
    "https://github.com/coseyfannitutti/mysterium:mysterium"
    "https://github.com/peej/lumberjack-keyboard:lumberjack"
)

for repo in "${repos[@]}"; do
    url="${repo%%:*}"
    name="${repo##*:}"
    ./scripts/process_repository.sh "$url" "$name"
done
```

## Individual Scripts

### collect_repository.sh

Clones a GitHub repository with error handling and retry logic.

**Usage:**
```bash
./scripts/collect_repository.sh <github-url> <project-name>
```

**Features:**
- Network connectivity check
- Exponential backoff retry (3 attempts)
- Git validation
- Repository metadata extraction

**Example:**
```bash
./scripts/collect_repository.sh https://github.com/coseyfannitutti/discipline discipline
```

**Output:**
- Clones repository to `.temp/<project-name>/`
- Displays commit hash and date
- Reports file count

### organize_files.sh

Detects file types and organizes them into appropriate directories.

**Usage:**
```bash
./scripts/organize_files.sh <project-name>
```

**Features:**
- Automatic file type detection based on extensions and content
- Project-specific directory creation
- File naming consistency checks
- Duplicate file handling with backups

**Supported File Types:**
- **Gerber files:** `.gbr`, `.gbl`, `.gtl`, `.drl`, etc.
- **KiCad files:** `.kicad_pcb`, `.kicad_sch`, `.kicad_pro`, etc.
- **Eagle files:** `.brd`, `.sch`
- **3D models:** `.stl`, `.step`, `.stp`
- **CAD drawings:** `.dxf`, `.svg`, `.dwg`
- **BOMs:** CSV files, markdown tables
- **Documentation:** `.md`, `.pdf`, `.txt`
- **Firmware:** QMK configs, keymaps

**Example:**
```bash
./scripts/organize_files.sh discipline
```

**Output:**
- Files organized in `gerbers/`, `design-files/`, `3d-models/`, etc.
- Summary of files processed by type

### extract_metadata.sh

Extracts project information and generates documentation.

**Usage:**
```bash
./scripts/extract_metadata.sh <project-name> <github-url>
```

**Features:**
- README parsing for project description
- License detection (MIT, GPL, Apache, BSD, etc.)
- Layout detection (60%, 65%, TKL, 40%, macropad)
- MCU detection (ATmega32A, ATmega328P, Pro Micro, etc.)
- USB connector detection (USB-C, Mini, Micro)
- Firmware support detection (QMK, VIA, VIAL)
- Special features extraction (encoders, OLED, RGB, etc.)
- File availability checking

**Example:**
```bash
./scripts/extract_metadata.sh discipline https://github.com/coseyfannitutti/discipline
```

**Output:**
- Project README: `docs/build-guides/<project-name>/README.md`
- Updated repository inventory: `docs/repository_inventory.md`

## Directory Structure

After processing, files are organized as follows:

```
PCB/
├── gerbers/<project-name>/
│   ├── pcb/              # Main PCB gerbers
│   └── plate/            # Plate gerbers
├── design-files/<project-name>/
│   ├── kicad/            # KiCad project files
│   ├── eagle/            # Eagle project files
│   └── libraries/        # Custom footprints/symbols
├── 3d-models/
│   ├── cases/<project-name>/
│   │   ├── stl/          # 3D printable files
│   │   └── step/         # CAD-editable files
│   ├── plates/<project-name>/
│   └── accessories/
├── cad-drawings/
│   ├── plates/<project-name>/
│   ├── cases/<project-name>/
│   └── covers/<project-name>/
├── boms/<project-name>/
├── docs/build-guides/<project-name>/
└── firmware/qmk-configs/<project-name>/
```

## Error Handling

### Network Failures

The clone script includes retry logic with exponential backoff:
- Initial retry: 2 seconds
- Second retry: 4 seconds
- Third retry: 8 seconds

### Invalid URLs

The script validates GitHub URL format before attempting to clone.

### Missing Files

If expected files are not found, the script logs warnings but continues processing.

### Duplicate Files

If a file already exists in the destination, the script creates a timestamped backup.

## Configuration

### Retry Settings

Edit `collect_repository.sh` to adjust retry behavior:

```bash
MAX_RETRIES=3           # Number of retry attempts
INITIAL_BACKOFF=2       # Initial backoff in seconds
```

### File Type Detection

Edit `organize_files.sh` to add new file type patterns:

```bash
detect_file_type() {
    # Add custom detection logic here
}
```

## Troubleshooting

### "git is not installed"

Install git:
```bash
# macOS
brew install git

# Ubuntu/Debian
sudo apt-get install git
```

### "Cannot reach github.com"

Check your network connection and firewall settings.

### "Source directory not found"

Ensure you run `collect_repository.sh` before `organize_files.sh` or `extract_metadata.sh`.

### Permission Denied

Make scripts executable:
```bash
chmod +x scripts/*.sh
```

## Cleanup

To remove temporary files after processing:

```bash
rm -rf .temp/
```

To remove a specific project's temporary files:

```bash
rm -rf .temp/<project-name>/
```

## Requirements

- **bash** (version 4.0+)
- **git** (version 2.0+)
- **grep**, **sed**, **find** (standard Unix tools)
- Network connectivity to github.com

## License

These scripts are part of the Through-Hole Keyboard PCB Design Resource Library.

## Contributing

To add support for new file types or improve detection:

1. Edit `organize_files.sh`
2. Add detection patterns in `detect_file_type()`
3. Add corresponding copy logic in `process_files()`
4. Test with sample repositories

## BOM Consolidation

### Overview

The BOM consolidation system processes individual project BOMs and generates a unified master BOM with component deduplication, normalization, and categorization.

### Scripts

#### parse_bom.py

Parses BOM files in multiple formats (CSV, Markdown, plain text).

**Usage:**
```bash
python3 scripts/parse_bom.py <bom-file>
```

**Supported Formats:**
- **CSV:** Standard comma-separated values with headers
- **Markdown:** Tables with pipe-separated columns
- **Plain Text:** Simple quantity-component-value format

**Example:**
```bash
python3 scripts/parse_bom.py boms/discipline/bom.csv
```

#### normalize_components.py

Normalizes component names, values, and categories.

**Usage:**
```bash
# Normalize a component
python3 scripts/normalize_components.py normalize <component> <value> [footprint]

# Create default configuration
python3 scripts/normalize_components.py create-config <output-file>
```

**Normalization Rules:**
- **Resistors:** 10k → 10kΩ, 10000 → 10kΩ
- **Capacitors:** 100nF → 0.1µF, 0.1uF → 0.1µF
- **Diodes:** Various formats → 1N4148
- **MCUs:** ATMEGA328P-PU → ATmega328P

**Example:**
```bash
python3 scripts/normalize_components.py normalize "R1" "10k" "Axial"
# Output: Resistors: Resistor 10kΩ (Axial)
```

#### consolidate_bom.py

Consolidates all project BOMs into a master BOM with deduplication.

**Usage:**
```bash
python3 scripts/consolidate_bom.py <bom-directory> [config-file]
```

**Features:**
- Parses BOMs from all project subdirectories
- Normalizes component names and values
- Deduplicates components across projects
- Tracks min/max quantities per component
- Lists all projects using each component
- Generates category-specific indexes

**Example:**
```bash
python3 scripts/consolidate_bom.py boms scripts/normalization_config.json
```

**Output Files:**
- `boms/master-bom.csv` - Complete master BOM
- `boms/master-bom-summary.md` - Statistics and summary
- `boms/by-category/*.csv` - Category-specific indexes

#### update_master_bom.sh

Convenience script to update the master BOM.

**Usage:**
```bash
./scripts/update_master_bom.sh
```

This script:
1. Checks for required dependencies
2. Creates default config if needed
3. Runs BOM consolidation
4. Reports generated files

### BOM File Formats

#### CSV Format

```csv
Component,Value,Footprint,Quantity,Reference,Vendor Part,Notes
Resistor,10k,Axial,12,R1-R12,YAGEO RC0603FR-0710KL,Pull-up resistors
Diode,1N4148,DO-35,68,D1-D68,1N4148,One per switch
```

#### Markdown Format

```markdown
| Component | Value | Footprint | Quantity | Notes |
|-----------|-------|-----------|----------|-------|
| Resistor | 10kΩ | Axial | 12 | Pull-up resistors |
| Diode | 1N4148 | DO-35 | 68 | Switch diodes |
```

#### Plain Text Format

```
12x Resistor 10k Axial
68x Diode 1N4148 DO-35
5x Capacitor 0.1uF 0805
```

### Master BOM Structure

The master BOM includes:

- **Component:** Normalized component name
- **Value:** Normalized value (10kΩ, 0.1µF, etc.)
- **Footprint:** Normalized footprint (DO-35, Axial, etc.)
- **Package:** THT or SMD
- **Vendor_Part_No:** Vendor part number if available
- **Category:** Component category (Resistors, Capacitors, etc.)
- **Min_Qty:** Minimum quantity across all projects
- **Max_Qty:** Maximum quantity across all projects
- **Projects_Using:** Semicolon-separated list of projects
- **Notes:** Combined notes from all projects

### Component Categories

- **Resistors:** Pull-up, pull-down, current limiting
- **Capacitors:** Decoupling, power smoothing, crystal load
- **Diodes:** Switch matrix, protection
- **Microcontrollers:** ATmega, Pro Micro variants
- **Crystals:** Clock sources
- **Connectors:** USB, headers, TRRS
- **Switches:** Reset, boot, tactile
- **LEDs:** Status indicators, backlighting
- **Other:** Encoders, displays, etc.

### Workflow Integration

To update the master BOM after adding new projects:

```bash
# 1. Process new repository
./scripts/process_repository.sh <github-url> <project-name>

# 2. Update master BOM
./scripts/update_master_bom.sh
```

The master BOM will automatically include the new project's components.

## Documentation Indexing

### Overview

The documentation indexing system scans all markdown files in the library and generates comprehensive indexes organized by category, project, and alphabetically.

### Scripts

#### parse_markdown.py

Parses Markdown files and extracts structure and metadata.

**Usage:**
```bash
python3 scripts/parse_markdown.py <markdown-file> [--validate]
```

**Features:**
- Extracts headings and document structure
- Parses inline and reference-style links
- Extracts tables with headers and rows
- Identifies code blocks with language tags
- Generates document metadata (word count, line count, etc.)
- Validates internal links (with --validate flag)

**Example:**
```bash
python3 scripts/parse_markdown.py docs/repository_inventory.md
python3 scripts/parse_markdown.py docs/build-guides/discipline/README.md --validate
```

**Output:**
- Document title and statistics
- List of headings with hierarchy
- Links (internal and external)
- Tables and code blocks
- Broken link report (if --validate used)

#### index_documentation.py

Generates master documentation indexes for the entire library.

**Usage:**
```bash
python3 scripts/index_documentation.py <base-directory> [output-directory]
```

**Features:**
- Scans all documentation directories recursively
- Categorizes documents (Build Guides, Technical Specifications, etc.)
- Associates documents with projects
- Generates master index with multiple views
- Creates category-specific indexes
- Sorts documents alphabetically and by category

**Example:**
```bash
python3 scripts/index_documentation.py PCB
python3 scripts/index_documentation.py PCB PCB/docs
```

**Output Files:**
- `documentation_index.md` - Master index with all documents
- `build_guides_index.md` - Index of build guides only
- `technical_specifications_index.md` - Index of technical specs
- Additional category indexes as needed

**Index Structure:**
- Statistics (total documents, categories, projects)
- Table of contents
- Documents organized by category
- Documents organized by project
- Alphabetical listing of all documents

### Workflow Integration

To update documentation indexes after adding new documents:

```bash
# 1. Add or update markdown files in docs/ directories

# 2. Regenerate indexes
python3 scripts/index_documentation.py PCB PCB/docs
```

The indexes will automatically include all new documentation.

### Document Categories

- **Build Guides:** Step-by-step assembly instructions for projects
- **Technical Specifications:** PCB dimensions, clearances, standards
- **Firmware Guides:** Flashing instructions and QMK setup
- **Design Templates:** Starter templates for new designs

### Metadata Extraction

For each document, the indexer extracts:
- **Title:** First heading or filename
- **Description:** First paragraph or second heading
- **Project:** Associated keyboard project (from path)
- **Category:** Document type
- **Statistics:** Line count, word count, heading count
- **Links:** Internal and external references

## Manufacturing File Organization

### Overview

The manufacturing file organization system handles Gerber files, PCB specifications, and manufacturing documentation to prepare projects for PCB fabrication.

### Scripts

#### organize_gerbers.sh

Organizes Gerber files by project, separating PCB and plate files.

**Usage:**
```bash
./scripts/organize_gerbers.sh <source_repo_path> <project_name>
```

**Features:**
- Searches for Gerber ZIP archives and loose files
- Automatically detects PCB vs plate Gerbers
- Validates Gerber file completeness
- Checks for required layers (top/bottom copper, drill, outline)
- Extracts ZIP files for validation
- Creates organized directory structure

**Supported Gerber Extensions:**
- `.gbr`, `.gbl`, `.gtl` (copper layers)
- `.gbs`, `.gts` (solder mask)
- `.gbo`, `.gto` (silkscreen)
- `.gm1`, `.gko` (board outline)
- `.drl` (drill files)
- `.txt` (drill reports)

**Example:**
```bash
./scripts/organize_gerbers.sh .temp/discipline discipline
```

**Output:**
- `gerbers/<project>/pcb/` - Main PCB Gerber files
- `gerbers/<project>/plate/` - Plate Gerber files (if found)
- Validation report for each Gerber set

**Validation Checks:**
- ✓ Top copper layer present
- ✓ Bottom copper layer present
- ✓ Drill file present
- ✓ Board outline present

#### extract_pcb_specs.py

Extracts PCB specifications from documentation and design files.

**Usage:**
```bash
python3 scripts/extract_pcb_specs.py <project_name> <source_repo_path>
```

**Features:**
- Parses README files for dimensions and specifications
- Extracts layer count from KiCad files
- Applies standard specifications (GH60, etc.)
- Generates YAML and Markdown specification files
- Documents mounting hole positions
- Records USB cutout dimensions

**Extracted Information:**
- PCB dimensions (length, width, thickness)
- Layer count and material
- Mounting hole count, diameter, and positions
- USB cutout size and position
- Surface finish and silkscreen options

**Example:**
```bash
python3 scripts/extract_pcb_specs.py discipline .temp/discipline
```

**Output:**
- `docs/pcb-specs/<project>_specs.yaml` - Machine-readable specs
- `docs/pcb-specs/<project>_specs.md` - Human-readable specs

**Specification Format:**
```yaml
project_name: discipline
pcb:
  dimensions:
    length: 285.0mm
    width: 94.6mm
    thickness: 1.6mm
  layers: 2
  material: FR4
  mounting_holes:
    count: 6
    diameter: 2.0-2.2mm
    positions:
      - [19.0, 9.5]
      - [266.0, 9.5]
      # ...
```

### Manufacturing Guide

A comprehensive manufacturing guide is available at `docs/manufacturing_guide.md` covering:

- **Quick Start:** Step-by-step ordering process
- **PCB Specifications:** Standard settings for through-hole keyboards
- **Recommended Manufacturers:** JLCPCB, PCBWay, OSH Park, Elecrow
- **Ordering Process:** Detailed walkthrough with screenshots
- **Common Settings:** Budget, standard, and premium configurations
- **Cost Estimation:** Price breakdowns and money-saving tips
- **Quality Control:** What to check when PCBs arrive
- **Common Pitfalls:** File issues, specification problems, ordering mistakes
- **Troubleshooting:** Solutions for fit, component, and electrical issues

### Workflow Integration

To prepare a project for manufacturing:

```bash
# 1. Process repository
./scripts/process_repository.sh <github-url> <project-name>

# 2. Organize Gerber files
./scripts/organize_gerbers.sh .temp/<project-name> <project-name>

# 3. Extract PCB specifications
python3 scripts/extract_pcb_specs.py <project-name> .temp/<project-name>

# 4. Review manufacturing guide
cat docs/manufacturing_guide.md
```

### PCB Specification Template

A template specification file is available at `docs/pcb-specs/template_specs.md` for manual documentation of projects without extractable specifications.

### Directory Structure

After processing, manufacturing files are organized as:

```
PCB/
├── gerbers/<project>/
│   ├── pcb/                    # Main PCB Gerbers
│   │   ├── *.gbr               # Gerber layer files
│   │   ├── *.drl               # Drill files
│   │   └── gerbers.zip         # Original ZIP archive
│   └── plate/                  # Plate Gerbers (if separate)
│       └── *.gbr
├── docs/
│   ├── manufacturing_guide.md  # Complete manufacturing guide
│   └── pcb-specs/              # Per-project specifications
│       ├── template_specs.md   # Specification template
│       ├── <project>_specs.yaml
│       └── <project>_specs.md
```

## 3D Model and CAD Drawing Organization

### Overview

The 3D model organization system collects, validates, and catalogs STL files, STEP files, and CAD drawings (DXF, SVG) from keyboard projects. It provides comprehensive documentation with material recommendations, print settings, and cutting specifications.

### Scripts

#### organize_3d_models.sh

Organizes 3D models and CAD drawings by project and type with file validation.

**Usage:**
```bash
./scripts/organize_3d_models.sh <project-name>
```

**Features:**
- Collects STL files with integrity validation
- Organizes STEP files for CAD editing
- Processes DXF and SVG files for laser cutting/CNC
- Automatic type detection (case, plate, accessory, cover)
- File size validation and duplicate handling
- Generates project-specific inventory

**File Type Detection:**
- **Cases:** Files containing "case", "housing", "enclosure", "shell", "body", "frame", "tray"
- **Plates:** Files containing "plate", "switch plate", "mounting plate"
- **Cradles:** Files containing "cradle", "holder", "support", "socket", "mount"
- **Covers:** Files containing "cover", "lid", "top", "bottom", "cap"

**STL Validation:**
- Checks file readability
- Validates minimum file size (>84 bytes)
- Detects ASCII vs binary STL format
- Reports corrupted or invalid files

**Example:**
```bash
./scripts/organize_3d_models.sh discipline
```

**Output:**
- `3d-models/cases/<project>/stl/` - 3D printable case files
- `3d-models/cases/<project>/step/` - CAD-editable case files
- `3d-models/plates/<project>/` - Plate models (STL/STEP)
- `3d-models/accessories/component-cradles/<project>/` - Component holders
- `3d-models/accessories/covers/<project>/` - Covers and lids
- `cad-drawings/plates/<project>/` - Plate DXF/SVG files
- `cad-drawings/cases/<project>/` - Case DXF/SVG files
- `cad-drawings/covers/<project>/` - Cover DXF/SVG files
- Project-specific README with file inventory

#### generate_3d_catalog.py

Generates a comprehensive catalog of all 3D models and CAD drawings with detailed specifications.

**Usage:**
```bash
python3 scripts/generate_3d_catalog.py
```

**Features:**
- Scans all 3D model and CAD drawing directories
- Generates file statistics and summaries
- Provides material recommendations by component type
- Includes estimated print times based on file size
- Documents recommended print settings
- Provides cutting specifications for DXF files
- Links to source projects
- Organizes by project and category

**Catalog Contents:**
- **Statistics:** Total projects, file counts by type
- **Cases:** STL and STEP files with print settings
- **Plates:** Models with material recommendations
- **Accessories:** Component cradles, covers, etc.
- **CAD Drawings:** DXF/SVG files with cutting settings
- **Usage Guidelines:** 3D printing, CAD editing, laser cutting
- **Material Selection:** PLA, PETG, ABS, Polycarbonate
- **Service Providers:** Ponoko, SendCutSend, local makerspaces

**Example:**
```bash
python3 scripts/generate_3d_catalog.py
```

**Output:**
- `docs/3d_model_catalog.md` - Master catalog with all models

**Catalog Structure:**
```markdown
# 3D Model and CAD Drawing Catalog

## Statistics
- Total Projects: 15
- STL Files: 45 (3D printing)
- STEP Files: 30 (CAD editing)
- DXF Files: 25 (laser cutting/CNC)

## 3D Models
### Cases
#### Discipline
| File | Size | Est. Print Time | Materials |
|------|------|-----------------|-----------|
| case_bottom.stl | 2.5 MB | 3-8 hours | PLA, PETG, ABS |

**Recommended Print Settings:**
- Layer Height: 0.2mm
- Infill: 25%
- Supports: Likely required
- Orientation: Check model

### Plates
### Accessories

## CAD Drawings
### Plate Drawings
### Case Drawings
### Cover Drawings

## Usage Guidelines
...
```

### Material Recommendations

**3D Printing Materials:**
- **PLA:** Easy to print, rigid, good for most cases
- **PETG:** More durable, slightly flexible, better layer adhesion
- **ABS:** Strong, heat resistant, requires heated enclosure
- **Polycarbonate:** Very strong, excellent for plates

**Laser Cutting Materials:**
- **Acrylic:** 1.5-3mm for plates, 3-5mm for cases
- **FR4 (PCB material):** 1.5mm for plates
- **Aluminum:** 1.5mm for plates, requires CNC
- **Steel:** 1.5mm for plates, requires CNC
- **Wood:** 3-5mm for cases, laser or CNC

### Print Settings by Component Type

**Cases:**
- Layer Height: 0.2mm
- Infill: 25%
- Supports: Likely required
- Orientation: Check model

**Plates:**
- Layer Height: 0.15mm
- Infill: 30%
- Supports: Auto
- Orientation: Flat on bed

**Covers/Lids:**
- Layer Height: 0.2mm
- Infill: 15%
- Supports: Minimal
- Orientation: Check model

**Accessories:**
- Layer Height: 0.2mm
- Infill: 20%
- Supports: Auto
- Orientation: Check model

### Cutting Settings

**Plates (DXF):**
- Material: Acrylic, FR4, Aluminum, or Steel
- Thickness: 1.5mm (standard switch plate)
- Method: Laser cutting (acrylic/wood) or CNC (metal)

**Cases (DXF):**
- Material: Acrylic or Wood
- Thickness: 3-5mm
- Method: Laser cutting or CNC routing

### Workflow Integration

To organize 3D models after processing a repository:

```bash
# 1. Process repository
./scripts/process_repository.sh <github-url> <project-name>

# 2. Organize 3D models and CAD drawings
./scripts/organize_3d_models.sh <project-name>

# 3. Regenerate master catalog
python3 scripts/generate_3d_catalog.py
```

The catalog will automatically include all new 3D models and CAD drawings.

### Directory Structure

After processing, 3D files are organized as:

```
PCB/
├── 3d-models/
│   ├── cases/<project>/
│   │   ├── stl/                # 3D printable files
│   │   │   ├── case_top.stl
│   │   │   └── case_bottom.stl
│   │   ├── step/               # CAD-editable files
│   │   │   └── case_assembly.step
│   │   └── README.md           # Project-specific inventory
│   ├── plates/<project>/
│   │   ├── plate.stl
│   │   └── plate.step
│   └── accessories/
│       ├── component-cradles/<project>/
│       │   └── mcu_cradle.stl
│       └── covers/<project>/
│           └── bottom_cover.stl
├── cad-drawings/
│   ├── plates/<project>/
│   │   └── plate.dxf
│   ├── cases/<project>/
│   │   ├── top_panel.dxf
│   │   └── bottom_panel.dxf
│   └── covers/<project>/
│       └── cover.dxf
└── docs/
    └── 3d_model_catalog.md    # Master catalog
```

### File Validation

**STL Validation Checks:**
- File readability
- Minimum file size (>84 bytes)
- Valid STL header (ASCII "solid" or binary format)
- Reports corrupted or invalid files

**Duplicate Handling:**
- Compares file sizes for existing files
- Creates timestamped backups if different
- Skips identical files to avoid duplication

### Service Providers

**3D Printing Services:**
- Shapeways
- Sculpteo
- i.materialise
- Local makerspaces

**Laser Cutting / CNC Services:**
- Ponoko (laser cutting)
- SendCutSend (laser and CNC)
- OSH Cut (PCB-based plates)
- Local makerspaces and fab labs

### CAD Software Compatibility

**STEP File Editing:**
- FreeCAD (free, open-source)
- Fusion 360 (free for hobbyists)
- SolidWorks (professional)
- OnShape (browser-based)

**DXF File Editing:**
- LibreCAD (free, open-source)
- QCAD (free/commercial)
- AutoCAD (professional)
- Inkscape (with DXF plugin)

## See Also

- [Repository Inventory](../docs/repository_inventory.md) - Catalog of processed projects
- [References](../references.md) - List of source repositories
- [Components](../components.md) - Component specifications
- [Master BOM](../boms/master-bom.csv) - Consolidated component database
- [BOM Summary](../boms/master-bom-summary.md) - Component statistics
- [Documentation Index](../docs/documentation_index.md) - Master documentation index
- [Manufacturing Guide](../docs/manufacturing_guide.md) - PCB ordering guide
- [3D Model Catalog](../docs/3d_model_catalog.md) - Complete 3D model and CAD drawing catalog
