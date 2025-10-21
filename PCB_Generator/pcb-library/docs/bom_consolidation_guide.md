# BOM Consolidation Guide

## Overview

The BOM consolidation system processes individual project BOMs and generates a unified master BOM with component deduplication, normalization, and categorization. This guide explains how to use the system and interpret the results.

## Quick Start

### Process a Single Project

After collecting a repository with `process_repository.sh`, the BOM files are automatically organized into `boms/<project-name>/`. To update the master BOM:

```bash
./scripts/update_master_bom.sh
```

This will:
1. Parse all project BOMs in `boms/*/`
2. Normalize component names and values
3. Deduplicate components across projects
4. Generate master BOM and category indexes

### Manual BOM Consolidation

For more control, use the consolidation script directly:

```bash
python3 scripts/consolidate_bom.py boms scripts/normalization_config.json
```

## BOM File Formats

The system supports three BOM formats:

### CSV Format

Standard comma-separated values with headers:

```csv
Component,Value,Footprint,Quantity,Reference,Vendor Part,Notes
Resistor,10k,Axial,12,R1-R12,YAGEO RC0603FR-0710KL,Pull-up resistors
Diode,1N4148,DO-35,68,D1-D68,1N4148,One per switch
Capacitor,0.1uF,0805,5,C1-C5,TDK C0805C104K5RACTU,Decoupling
```

**Required columns:** At least one of `Component`, `Value`, or `Quantity`

**Optional columns:** `Footprint`, `Reference`, `Vendor Part`, `Notes`

### Markdown Table Format

Pipe-separated tables:

```markdown
| Component | Value | Footprint | Quantity | Notes |
|-----------|-------|-----------|----------|-------|
| Resistor | 10kΩ | Axial | 12 | Pull-up resistors |
| Diode | 1N4148 | DO-35 | 68 | Switch diodes |
| Capacitor | 0.1µF | 0805 | 5 | Decoupling |
```

**Format:** Standard Markdown table with header row and separator

**Flexible columns:** Any column names are accepted (case-insensitive)

### Plain Text Format

Simple quantity-component-value format:

```
12x Resistor 10k Axial
68x Diode 1N4148 DO-35
5x Capacitor 0.1uF 0805
1x Microcontroller ATmega328P DIP-28
```

**Format:** `<quantity>x <component> <value> [footprint] [notes]`

**Quantity:** Optional, defaults to 1 if omitted

## Component Normalization

The system automatically normalizes component names and values for consistency.

### Resistor Normalization

| Input | Normalized Output |
|-------|------------------|
| 10k | 10kΩ |
| 10K | 10kΩ |
| 10000 | 10kΩ |
| 10kohm | 10kΩ |
| 10 kΩ | 10kΩ |
| 5.1k | 5.1kΩ |
| 75 | 75Ω |
| 1M | 1MΩ |

### Capacitor Normalization

| Input | Normalized Output |
|-------|------------------|
| 0.1uF | 0.1µF |
| 100nF | 100.0nF |
| 22pF | 22.0pF |
| 4.7µF | 4.7µF |
| 1000nF | 1.0µF |

### Diode Normalization

| Input | Normalized Output |
|-------|------------------|
| 1n4148 | 1N4148 |
| 1N 4148 | 1N4148 |
| 1N4007 | 1N4007 |

### MCU Normalization

| Input | Normalized Output |
|-------|------------------|
| ATMEGA328P-PU | ATmega328P |
| atmega328 | ATmega328P |
| ATMEGA32U4 | ATmega32U4 |
| Pro Micro | Pro Micro |

### Footprint Normalization

| Input | Normalized Output |
|-------|------------------|
| DO35 | DO-35 |
| DIP28 | DIP-28 |
| 0805 | 0805 |
| axial | Axial |

## Component Categories

Components are automatically categorized:

### Resistors
- Pull-up resistors
- Pull-down resistors
- Current limiting resistors
- Termination resistors

### Capacitors
- Decoupling capacitors (0.1µF, 100nF)
- Power smoothing (4.7µF, 10µF)
- Crystal load capacitors (22pF)

### Diodes
- Switch matrix diodes (1N4148)
- Protection diodes (1N4007)
- Schottky diodes (1N5817)

### Microcontrollers
- ATmega328P (DIP-28)
- ATmega32U4 (DIP-40)
- ATmega32A (DIP-40)
- Pro Micro modules

### Crystals
- 16MHz (most common)
- 8MHz
- Other frequencies

### Connectors
- USB-C (through-hole)
- USB Mini/Micro
- TRRS jacks
- ISP headers
- Pin headers

### Switches
- Reset buttons
- Boot buttons
- Tactile switches

### LEDs
- Status indicators
- Backlight LEDs
- RGB LEDs

### Other
- Rotary encoders
- OLED displays
- Batteries
- Fuses

## Master BOM Structure

The master BOM (`boms/master-bom.csv`) includes:

```csv
Component,Value,Footprint,Package,Vendor_Part_No,Category,Min_Qty,Max_Qty,Projects_Using,Notes
Resistor,10kΩ,Axial,THT,YAGEO RC0603FR-0710KL,Resistors,12,16,discipline; mysterium; plaid,Pull-up resistors
```

### Fields

- **Component:** Normalized component name (Resistor, Capacitor, etc.)
- **Value:** Normalized value (10kΩ, 0.1µF, 1N4148, etc.)
- **Footprint:** Normalized footprint (DO-35, Axial, 0805, etc.)
- **Package:** THT or SMD
- **Vendor_Part_No:** Vendor part number (if available)
- **Category:** Component category (Resistors, Capacitors, etc.)
- **Min_Qty:** Minimum quantity across all projects
- **Max_Qty:** Maximum quantity across all projects
- **Projects_Using:** Semicolon-separated list of projects
- **Notes:** Combined notes from all projects

### Quantity Ranges

The `Min_Qty` and `Max_Qty` fields show the range of quantities used across projects:

- **Min_Qty = Max_Qty:** All projects use the same quantity
- **Min_Qty < Max_Qty:** Different projects use different quantities

**Example:**
```
Diode,1N4148,DO-35,THT,,Diodes,48,87,discipline; mysterium; plaid
```

This means:
- Discipline uses 68 diodes (60% layout)
- Mysterium uses 87 diodes (TKL layout)
- Plaid uses 48 diodes (40% layout)

## Category Indexes

Category-specific indexes are generated in `boms/by-category/`:

```
boms/by-category/
├── resistors.csv
├── capacitors.csv
├── diodes.csv
├── microcontrollers.csv
├── crystals.csv
├── connectors.csv
├── switches.csv
└── leds.csv
```

Each file contains only components from that category, making it easy to:
- Review all resistors across projects
- Compare MCU choices
- Identify common connector types

## Summary Report

The summary report (`boms/master-bom-summary.md`) provides:

### Statistics
- Total unique components
- Total projects processed
- Number of categories

### Components by Category
- Component count per category
- Most common components
- Projects using each component

### Project List
- All processed projects

**Example:**

```markdown
## Statistics

- **Total Unique Components:** 42
- **Total Projects:** 8
- **Categories:** 9

## Components by Category

### Resistors (3 components)

**Most Common:**

- Resistor 10kΩ (8 projects: discipline, mysterium, plaid, ...)
- Resistor 5.1kΩ (2 projects: discipline, mysterium)
- Resistor 1.5kΩ (1 projects: discipline)
```

## Customizing Normalization

### Configuration File

The normalization rules are defined in `scripts/normalization_config.json`:

```json
{
  "resistor_patterns": [
    "(?i)^r\\d+$",
    "(?i)^res",
    "(?i)resistor"
  ],
  "capacitor_patterns": [
    "(?i)^c\\d+$",
    "(?i)^cap",
    "(?i)capacitor"
  ],
  ...
}
```

### Adding Custom Patterns

To add custom component detection patterns:

1. Edit `scripts/normalization_config.json`
2. Add regex patterns to the appropriate category
3. Re-run consolidation

**Example:** Add support for "RES" prefix:

```json
{
  "resistor_patterns": [
    "(?i)^r\\d+$",
    "(?i)^res",
    "(?i)resistor",
    "(?i)^res\\d+"
  ]
}
```

## Troubleshooting

### Components Not Detected

**Problem:** Components are categorized as "Other"

**Solution:**
1. Check component name format
2. Add detection pattern to config
3. Re-run consolidation

### Incorrect Normalization

**Problem:** Values not normalized correctly (e.g., "10k" stays "10k")

**Solution:**
1. Check value format matches expected patterns
2. Update normalization rules in `normalize_components.py`
3. Re-run consolidation

### Missing BOM Files

**Problem:** "No BOM file found for project"

**Solution:**
1. Ensure BOM file is in `boms/<project-name>/`
2. Check file extension (.csv, .md, .txt)
3. Verify file format is supported

### Duplicate Components

**Problem:** Same component appears multiple times

**Solution:**
- This is expected if components have different values or footprints
- Check if normalization is working correctly
- Verify component data is consistent

## Best Practices

### BOM File Naming

Use consistent naming:
- `bom.csv` (preferred)
- `bill_of_materials.csv`
- `parts_list.csv`

### Column Names

Use standard column names for better parsing:
- Component, Value, Footprint, Quantity
- Reference, Vendor Part, Notes

### Value Formats

Use standard formats for better normalization:
- Resistors: `10k`, `10kΩ`, `5.1k`
- Capacitors: `0.1uF`, `100nF`, `22pF`
- Diodes: `1N4148`, `1N4007`

### Vendor Part Numbers

Include vendor part numbers when available:
- Helps with sourcing
- Ensures correct component selection
- Useful for bulk ordering

## Integration with Workflow

### After Processing a Repository

```bash
# 1. Process repository
./scripts/process_repository.sh https://github.com/user/project project-name

# 2. Update master BOM
./scripts/update_master_bom.sh
```

### Batch Processing

```bash
# Process multiple repositories
for repo in discipline mysterium plaid; do
    ./scripts/process_repository.sh "https://github.com/user/$repo" "$repo"
done

# Update master BOM once
./scripts/update_master_bom.sh
```

## Output Files

After consolidation, you'll have:

```
boms/
├── master-bom.csv              # Complete master BOM
├── master-bom-summary.md       # Statistics and summary
├── by-category/                # Category indexes
│   ├── resistors.csv
│   ├── capacitors.csv
│   ├── diodes.csv
│   └── ...
└── <project-name>/             # Individual project BOMs
    └── bom.csv
```

## See Also

- [Scripts README](../scripts/README.md) - Detailed script documentation
- [Repository Inventory](repository_inventory.md) - Project catalog
- [Component Sourcing Guide](component_sourcing_guide.md) - Vendor recommendations
