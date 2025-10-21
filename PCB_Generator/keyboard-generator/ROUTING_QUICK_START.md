# Routing Extraction - Quick Start Guide

## What Is This?

A system that extracts PCB routing patterns (copper traces, vias, zones) from real keyboard PCBs and makes them reusable for generating new PCBs.

## Quick Commands

```bash
# Extract routing from all PCBs in library
python keyboard-generator/extract_routing_patterns.py

# Analyze routing patterns
python keyboard-generator/analyze_routing_topology.py

# Create reusable templates
python keyboard-generator/create_routing_templates.py

# Test templates work
python keyboard-generator/test_routing_templates.py
```

## What You Get

### Routing Data
- **Location**: `keyboard-generator/routing_data/`
- **Files**: 20+ JSON files with extracted routing
- **Contains**: Nets, traces, vias, zones from each PCB

### Routing Templates
- **Location**: `keyboard-generator/routing_templates/`
- **Files**: 3 reusable templates
- **Best for**:
  - `lumberjack_lumberjack_template.json` - Full keyboards
  - `dumbpad_dumbpad_template.json` - Macropads
  - `litl_litl_template.json` - Compact layouts

## Using Templates in Code

```python
from pathlib import Path
from thkg.templates.routing_template import (
    RoutingTemplateExtractor, 
    RoutingTemplateApplicator
)

# Load a template
extractor = RoutingTemplateExtractor(Path("routing_data"))
template = extractor.load_template(Path("routing_templates/dumbpad_dumbpad_template.json"))

# Apply to new layout
applicator = RoutingTemplateApplicator(template)

# Define target area (in mm)
target_bbox = ((10, 10), (100, 80))  # (min_x, min_y), (max_x, max_y)

# Map net names from template to your design
net_mapping = {
    '/ROW0': 'ROW0',
    '/ROW1': 'ROW1',
    '/COL0': 'COL0',
    '/COL1': 'COL1',
    'GND': 'GND',
    'VCC': 'VCC'
}

# Generate routing
new_routing = applicator.apply_to_layout(target_bbox, net_mapping)

# Use new_routing.traces, new_routing.vias in your PCB generator
```

## Template Stats

| Template | Size | Matrix | Traces | Vias | Best For |
|----------|------|--------|--------|------|----------|
| lumberjack | 273.9×86.2mm | 75×85 | 1005 | 16 | Full keyboards |
| dumbpad | 91.1×74.9mm | 25×27 | 337 | 37 | Macropads |
| litl | 237.4×86.2mm | 0×0 | 732 | 9 | Compact layouts |

## Key Files

### Core Implementation
- `thkg/templates/pcb_parser.py` - Parses .kicad_pcb files
- `thkg/templates/routing_template.py` - Template system
- `thkg/templates/models.py` - Data models (Trace, Via, Zone, etc.)

### Scripts
- `extract_routing_patterns.py` - Extract from all PCBs
- `analyze_routing_topology.py` - Analyze patterns
- `create_routing_templates.py` - Create templates
- `test_routing_templates.py` - Validate templates

### Documentation
- `ROUTING_EXTRACTION_COMPLETE.md` - Full documentation
- `SESSION_ROUTING_EXTRACTION.md` - Session summary
- `ROUTING_QUICK_START.md` - This file

## Data Format

### Trace
```python
{
    "start": [x1, y1],      # Start point (mm)
    "end": [x2, y2],        # End point (mm)
    "width": 0.25,          # Trace width (mm)
    "layer": "F.Cu",        # Layer name
    "net": 1,               # Net number
    "net_name": "GND"       # Net name
}
```

### Via
```python
{
    "position": [x, y],     # Position (mm)
    "size": 0.8,            # Outer diameter (mm)
    "drill": 0.4,           # Hole diameter (mm)
    "layers": ["F.Cu", "B.Cu"],
    "net": 1,
    "net_name": "GND"
}
```

## Common Patterns

### Power Routing
- **Trace width**: 0.5-0.8mm (thicker than signals)
- **Nets**: GND, VCC, +5V, +3V3
- **Strategy**: Often uses zones (copper pours) instead of traces

### Matrix Routing
- **Row traces**: Typically horizontal
- **Column traces**: Typically vertical
- **Trace width**: 0.25mm (standard signal)
- **Nets**: /ROW0, /ROW1, /COL0, /COL1, etc.

### USB Routing
- **Differential pair**: D+ and D-
- **Trace width**: ~0.25mm
- **Length matching**: Keep D+ and D- same length
- **Spacing**: Keep traces close together

## Next Steps

1. **Integrate with PCB Generator**
   - Modify `thkg/pcb/pcb_generator.py`
   - Add routing generation from templates
   - Generate KiCad syntax for traces/vias

2. **Test with Simple Design**
   - Generate 3x3 macropad
   - Apply dumbpad template
   - Validate in KiCad

3. **Add Validation**
   - Check traces stay in bounds
   - Verify net connectivity
   - Run design rule checks

## Troubleshooting

### "Routing data directory not found"
Run `extract_routing_patterns.py` first to create routing data.

### "Template file not found"
Run `create_routing_templates.py` to create templates.

### "No traces in template"
Some PCBs use zones instead of traces. Check `routing_topology_analysis.json` for details.

## Statistics

- **PCBs Analyzed**: 20
- **Total Traces**: 2,074
- **Total Vias**: 67
- **Total Zones**: 935
- **Templates Created**: 3
- **Success Rate**: 100% ✅

## Support

See full documentation in:
- `ROUTING_EXTRACTION_COMPLETE.md` - Complete implementation details
- `SESSION_ROUTING_EXTRACTION.md` - Session summary and results
