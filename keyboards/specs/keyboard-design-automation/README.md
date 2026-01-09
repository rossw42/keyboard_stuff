# Through-Hole Keyboard Generator (THKG) - Specification

## Overview

This specification defines the Through-Hole Keyboard Generator (THKG), an automated design tool that generates complete keyboard designs from high-level specifications. The tool leverages the Through-Hole Keyboard Library's reference designs to produce manufacturing-ready files.

## Project Goals

1. **Natural language design** - Describe keyboards in plain English, get complete PCB designs
2. **PCB-first approach** - Focus on PCB generation, with plate/case/firmware as secondary outputs
3. **Artistic expression** - Support through-hole keyboards as art pieces with visible components
4. **Leverage proven designs** - Use circuit templates from the library for reliability
5. **Enable rapid prototyping** - Allow designers to iterate quickly on custom layouts
6. **Maintain quality** - Ensure generated designs are manufacturable and functional

## Specification Documents

### [requirements.md](requirements.md)
Defines what the tool must do:
- 15 requirements with acceptance criteria
- Input configuration system
- Layout processing
- PCB/plate/case/firmware generation
- Validation and error handling
- Library integration

### [design.md](design.md)
Defines how the tool will work:
- System architecture (modular pipeline)
- Component interfaces
- Data models and structures
- Technology stack (Python, KiCad API, OpenSCAD)
- Error handling strategies
- Design decisions and rationale

### [tasks.md](tasks.md)
Defines step-by-step implementation:
- 15 major tasks with sub-tasks
- Phased implementation approach
- 5 phases over 16 weeks
- Testing and validation tasks
- Integration with library

## Key Features

### Input Formats
- **Natural language descriptions** (primary) - "60% keyboard with USB-C and rotary encoder"
- **Guided selection** - Choose from common layouts (keyboard, numpad, macropad) with visual previews
- **KLE JSON import** - For custom layouts
- **Interactive CLI** - Conversational design process
- **YAML configuration** - For advanced users and automation

### Output Files
- KiCad schematic and PCB files
- Gerber manufacturing files
- Plate DXF files
- Case STL and DXF files
- QMK firmware configuration
- Bill of Materials (BOM)
- Build documentation

### Supported Hardware
- **MCUs:** ATmega328P, ATmega32A, Pro Micro
- **USB:** USB-C (through-hole), USB Mini, USB Micro
- **Layouts:** 60%, 65%, TKL, 40%, custom
- **Features:** Rotary encoders, OLEDs, LEDs

## Technology Stack

**Core:**
- Python 3.8+
- KiCad 7.0+ (pcbnew Python API)
- OpenSCAD (case generation)
- QMK CLI (firmware validation)

**Libraries:**
- `pcbnew` - KiCad Python API
- `ezdxf` - DXF file generation
- `solidpython` - OpenSCAD wrapper
- `pyyaml` - Configuration parsing
- `click` - CLI interface

## Implementation Phases

### Phase 1: Plate Generation (MVP)
**Goal:** Generate plate DXF files
- Input parsing
- Layout engine
- Plate generation
- DXF export

### Phase 2: PCB Generation (Core Value)
**Goal:** Complete PCB generation
- Template extraction
- Schematic generation
- PCB layout
- Gerber export

### Phase 3: Case Generation
**Goal:** Case file generation
- Sandwich mount cases
- OpenSCAD generation
- STL and DXF export

### Phase 4: Firmware Generation
**Goal:** QMK firmware configs
- QMK configuration
- Keymap generation
- VIA support
- Compilation validation

### Phase 5: Integration & Polish
**Goal:** Complete tool
- Output packaging
- Documentation generation
- End-to-end testing
- Library integration

## Example Usage

### Natural Language Design
```bash
# Describe your keyboard
$ thkg create "60% keyboard with USB-C and rotary encoder"

# Numpad design
$ thkg create "numpad with 4x4 layout and OLED display"

# Macropad
$ thkg create "macropad with 3x3 switches and two rotary encoders"
```

### Guided Interactive Mode
```bash
# Start interactive design process
$ thkg create --interactive

# System asks:
# "What type of keyboard? (keyboard/numpad/macropad)"
# "What layout? (60%, 65%, TKL, 40%, custom)"
# "Which MCU? (ATmega328P, ATmega32A, Pro Micro)"
# "USB connector? (USB-C through-hole, USB Mini, USB Micro)"
# "Special features? (rotary encoder, OLED, LEDs)"
```

### Advanced Options
```bash
# From KLE JSON for custom layout
$ thkg create --kle layout.json

# Using YAML config (for automation)
$ thkg create --config my-keyboard.yaml

# Generate only PCB (skip plate/case/firmware)
$ thkg create "65% keyboard" --pcb-only
```

## Directory Structure

```
PCB/tools/keyboard-generator/
├── thkg/                      # Main package
│   ├── input/                 # Input parsers
│   ├── layout/                # Layout engine
│   ├── templates/             # Circuit templates
│   ├── pcb/                   # PCB generation
│   ├── plate/                 # Plate generation
│   ├── case/                  # Case generation
│   ├── firmware/              # Firmware generation
│   ├── validation/            # Design validation
│   └── output/                # Output packaging
├── examples/                  # Example configs
├── output/                    # Generated designs
├── tests/                     # Test suite
└── README.md                  # Tool documentation
```

## Integration with Library

The generator integrates with the Through-Hole Keyboard Library:

1. **Templates:** Extracts circuit blocks from library designs
2. **Specifications:** Uses library specs for validation
3. **Components:** References library BOM for component data
4. **Documentation:** Uses library guides as templates

## Success Criteria

A successful implementation will:
1. ✅ Generate working PCB designs from YAML configs
2. ✅ Produce manufacturable Gerber files
3. ✅ Create accurate plate DXF files
4. ✅ Generate buildable case designs
5. ✅ Produce compilable QMK firmware
6. ✅ Pass all validation checks
7. ✅ Generate complete documentation

## Next Steps

1. Review and approve this specification
2. Set up development environment
3. Begin Phase 1 implementation (plate generation)
4. Iterate based on testing and feedback

## Questions or Feedback

This specification is a living document. Please provide feedback on:
- Missing requirements
- Technical approach
- Implementation priorities
- Integration concerns

---

**Specification Version:** 1.0  
**Created:** 2025-10-20  
**Status:** Draft - Awaiting Approval
