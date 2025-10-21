# Phase 2 Quick Start Guide

**Goal:** Get started with Phase 2 (PCB Generation) in 5 minutes

---

## What You Need to Know

### Phase 1 Status ✅
- Plate generation: **COMPLETE**
- All tests passing: **100%**
- Documentation: **COMPLETE**
- Ready for Phase 2: **YES**

### Phase 2 Goal 🎯
Generate complete, manufacturing-ready PCB designs automatically.

---

## Quick Commands

### Verify Phase 1 Works
```bash
cd keyboard-generator
python demo.py
# Should see: ✓ THKG Phase 1 - COMPLETE AND READY FOR USE!
```

### Install Phase 2 Dependencies
```bash
pip install sexpdata networkx shapely
```

### Explore PCB Library
```bash
cd ../pcb-library
ls design-files/  # See available designs
cat PROJECT_CATALOG.md  # Read project details
```

### Examine a KiCad File
```bash
# Look at Discipline schematic (ATmega32A + USB-C)
head -100 design-files/discipline/discipline.kicad_sch
```

---

## Phase 2 Tasks Overview

### Task 5: Template Extraction (Week 1)
**What:** Parse KiCad files and extract circuit templates  
**Why:** Reuse proven circuits from library  
**Output:** Cached templates for MCU, USB, etc.

### Task 6: Schematic Generation (Week 2)
**What:** Generate KiCad schematic files  
**Why:** Create the electrical design  
**Output:** .kicad_sch file with matrix + templates

### Task 7: PCB Layout (Week 3)
**What:** Place components and route traces  
**Why:** Create the physical board design  
**Output:** .kicad_pcb file with aesthetic layout

### Task 8: Gerber Export (Week 4)
**What:** Export manufacturing files  
**Why:** Send to PCB manufacturer  
**Output:** Gerber files + preview images

---

## First Task: KiCad File Parser (Task 5.1)

### Goal
Parse .kicad_sch files into Python data structures

### Approach
1. Study KiCad S-expression format
2. Use `sexpdata` library
3. Create data models
4. Test with real schematic

### Example KiCad Structure
```lisp
(kicad_sch (version 20230121)
  (lib_symbols
    (symbol "Device:R"
      (property "Reference" "R")
      (property "Value" "10k")
      ...
    )
  )
  (symbol (lib_id "Device:R") (at 100 100 0)
    (property "Reference" "R1")
    (property "Value" "10k")
  )
  (wire (pts (xy 100 100) (xy 150 100)))
)
```

### Create Parser Module
```bash
cd keyboard-generator

# Create parser module
cat > thkg/pcb/kicad_parser.py << 'EOF'
"""KiCad schematic file parser."""

import sexpdata
from typing import Dict, List, Any
from pathlib import Path

class KiCadSchematicParser:
    """Parse KiCad .kicad_sch files."""
    
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.data = None
    
    def parse(self) -> Dict[str, Any]:
        """Parse schematic file."""
        with open(self.filepath, 'r') as f:
            content = f.read()
        
        # Parse S-expression
        self.data = sexpdata.loads(content)
        
        return {
            'version': self._get_version(),
            'symbols': self._get_symbols(),
            'wires': self._get_wires(),
            'components': self._get_components()
        }
    
    def _get_version(self) -> str:
        """Extract KiCad version."""
        # TODO: Implement
        return "20230121"
    
    def _get_symbols(self) -> List[Dict]:
        """Extract symbol definitions."""
        # TODO: Implement
        return []
    
    def _get_wires(self) -> List[Dict]:
        """Extract wire connections."""
        # TODO: Implement
        return []
    
    def _get_components(self) -> List[Dict]:
        """Extract placed components."""
        # TODO: Implement
        return []

if __name__ == "__main__":
    # Test with Discipline schematic
    parser = KiCadSchematicParser(
        Path("../../pcb-library/design-files/discipline/discipline.kicad_sch")
    )
    result = parser.parse()
    print(f"Parsed schematic: {result['version']}")
    print(f"Found {len(result['components'])} components")
EOF

# Test the parser
python thkg/pcb/kicad_parser.py
```

---

## Key Resources

### Documentation
- **PHASE2_KICKOFF.md** - Complete Phase 2 plan
- **PCB_DESIGN_GUIDE.md** - Circuit design patterns
- **PROJECT_CATALOG.md** - Available PCB designs

### PCB Library Designs
- **Discipline** - ATmega32A + USB-C (65%)
- **Lumberjack** - ATmega328P + USB-C (60% ortho)
- **Litl** - Pro Micro (40%)

### Circuit Templates to Extract
- ATmega328P supporting circuit
- ATmega32A supporting circuit
- USB-C protection circuit
- USB Mini circuit
- Pro Micro footprint

---

## Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b phase2-task5-kicad-parser
```

### 2. Implement Feature
```bash
# Edit thkg/pcb/kicad_parser.py
# Add tests in tests/pcb/test_kicad_parser.py
```

### 3. Test Feature
```bash
pytest tests/pcb/test_kicad_parser.py -v
```

### 4. Commit Changes
```bash
git add thkg/pcb/kicad_parser.py tests/pcb/test_kicad_parser.py
git commit -m "feat: implement KiCad schematic parser (Task 5.1)"
```

---

## Success Criteria

### Task 5.1 Complete When:
- [ ] Can parse .kicad_sch files
- [ ] Extract components with properties
- [ ] Extract wire connections
- [ ] Extract symbol definitions
- [ ] Tests pass with real schematic
- [ ] Documentation updated

### Phase 2 Complete When:
- [ ] Generate valid KiCad schematic
- [ ] Generate valid PCB layout
- [ ] Export complete Gerber files
- [ ] Pass DRC with zero errors
- [ ] Generate visual preview
- [ ] Order and test PCB

---

## Next Steps

1. **Read PHASE2_KICKOFF.md** - Understand full plan
2. **Install dependencies** - `pip install sexpdata networkx shapely`
3. **Explore PCB library** - Study existing designs
4. **Start Task 5.1** - Implement KiCad parser
5. **Test with real files** - Use Discipline schematic

---

## Questions?

### Where to find help:
- **PCB_DESIGN_GUIDE.md** - Circuit design patterns
- **PROJECT_CATALOG.md** - Available designs
- **PHASE2_KICKOFF.md** - Detailed plan
- **KiCad docs** - https://docs.kicad.org/

### Common issues:
- **Can't parse KiCad file:** Check KiCad version (need 7.0+)
- **Missing dependencies:** Run `pip install -r requirements.txt`
- **Test failures:** Check file paths are correct

---

**Ready to build Phase 2!** 🚀

Start with: `python thkg/pcb/kicad_parser.py`
