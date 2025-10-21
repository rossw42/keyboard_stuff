# 🚀 Phase 2 Kickoff - PCB Generation

**Date:** October 20, 2025  
**Status:** Ready to Begin  
**Phase:** Phase 2 - PCB Generation (Core Value)

---

## 🎯 Phase 2 Overview

Phase 2 focuses on **PCB generation** - the core value proposition of THKG. We'll build on the solid Phase 1 foundation to generate complete, manufacturing-ready PCB designs.

### What We're Building

**Input:** Configuration file (from Phase 1)  
**Output:** Complete PCB design with:
- KiCad schematic files
- PCB layout with auto-routing
- Gerber files for manufacturing
- Visual preview images
- Bill of Materials (BOM)

---

## 📋 Phase 2 Tasks

### Task 5: Template Extraction System
**Goal:** Extract proven circuit patterns from our PCB library

- [ ] 5.1 Implement KiCad file parser (.kicad_sch format)
- [ ] 5.2 Implement circuit block identifier (MCU, USB, reset, crystal)
- [ ] 5.3 Implement template extractor (components, nets, pins)
- [ ] 5.4 Create template cache system
- [ ] 5.5 Extract templates from library:
  - ATmega328P circuit (from Lumberjack)
  - ATmega32A circuit (from Discipline)
  - Pro Micro footprint (from Litl)
  - USB-C circuit (from Discipline)
  - USB Mini circuit (from Tartan)

### Task 6: PCB Generation - Schematic
**Goal:** Generate KiCad schematic files

- [ ] 6.1 Implement schematic generator (KiCad file structure)
- [ ] 6.2 Implement matrix schematic generator (switches + diodes)
- [ ] 6.3 Implement circuit combiner (templates + matrix)
- [ ] 6.4 Implement schematic validator (connectivity checks)

### Task 7: PCB Generation - Layout
**Goal:** Generate PCB layout with aesthetic component placement

- [ ] 7.1 Implement component placement (aesthetic algorithms)
  - Place switches at calculated positions
  - Place diodes in aesthetic grid patterns
  - Place MCU centrally with visual balance
  - Place USB connector at edge
- [ ] 7.2 Implement trace routing (auto-route)
  - Auto-route matrix rows/columns
  - Auto-route power traces
  - Auto-route USB traces
  - Add ground plane
- [ ] 7.3 Implement board outline (PCB shape, mounting holes)
- [ ] 7.4 Implement design rule check (DRC validation)

### Task 8: PCB Generation - Gerber Export
**Goal:** Export manufacturing files and documentation

- [ ] 8.1 Implement Gerber exporter (all layers + drill files)
- [ ] 8.2 Implement Gerber validator (completeness checks)
- [ ] 8.3 Create manufacturing documentation
- [ ] 8.5 Visual preview generation (CHALLENGING)
  - 8.5.1 PCB rendering (top/bottom views)
  - 8.5.2 Preview image generation (PNG/SVG)
  - 8.5.3 3D preview (optional)

---

## 🎨 Key Focus Areas

### 1. Artistic Component Placement (Task 7.1)
**Why it matters:** Through-hole keyboards are visible art pieces

**Aesthetic Principles:**
- Diodes in perfect grid patterns
- Symmetric component placement
- Visual balance and alignment
- Clean, organized layout

**Implementation:**
- Grid-based diode placement algorithms
- Symmetry detection and enforcement
- Visual weight balancing
- Alignment helpers

### 2. Auto-Routing (Task 7.2)
**Why it matters:** Manual routing is time-consuming and error-prone

**Routing Strategy:**
- Grid-based routing for matrix
- Shortest path for power
- Differential pairs for USB
- Ground plane fill

**Implementation:**
- A* pathfinding for traces
- Obstacle avoidance
- Via placement optimization
- Trace width rules

### 3. Visual Preview (Task 8.5)
**Why it matters:** Users need to see before manufacturing

**Preview Types:**
- Top view (component placement)
- Bottom view (traces)
- 3D render (optional)
- Thumbnail for quick reference

**Implementation:**
- KiCad plot/export functions
- Image generation (PNG/SVG)
- Annotation overlay
- Interactive preview (stretch goal)

---

## 📚 Available Resources

### PCB Library Templates
We have **11 proven designs** to extract templates from:

**ATmega328P Designs:**
- Lumberjack (60% ortho, USB-C)
- Rosaline (40% staggered, USB-C)
- Plaid (ortho 4x12)
- Tartan (60%, USB Mini)
- Plaid-Pad (macropad)

**ATmega32A Designs:**
- Discipline (65%, USB-C)
- Mysterium (TKL, USB-C)

**Pro Micro Designs:**
- Litl (40%, USB-C)
- KBIC65 (65%, wireless)
- Dumbpad (macropad)

### Design Knowledge
We have comprehensive guides:
- PCB Design Guide (wired keyboards)
- Wireless PCB Design Guide (battery management)
- PCB Design Checklist (validation)
- GH60 PCB Specifications (reference)

### Circuit Patterns Documented

**USB-C Protection:**
```
USB-C Connector
├── R1, R2: 5.1kΩ (CC configuration)
├── L1, L2: Ferrite beads 600Ω@100MHz
├── D1: USBLC6-2SC6 (ESD protection)
├── F1: Polyfuse 500mA
└── C1, C2: 100nF (decoupling)
```

**ATmega328P Supporting Circuit:**
```
ATmega328P
├── C1-C4: 100nF (decoupling)
├── R1: 10kΩ (RESET pull-up)
├── X1: 16MHz crystal
├── C5, C6: 22pF (crystal load caps)
└── ISP Header: 6-pin
```

---

## 🛠️ Technical Approach

### KiCad File Format
**KiCad 7.0+ uses S-expression format:**
- Human-readable text files
- Easy to parse and generate
- Version control friendly
- Well-documented structure

**Example schematic structure:**
```lisp
(kicad_sch (version 20230121) (generator eeschema)
  (uuid "...")
  (paper "A4")
  (lib_symbols ...)
  (symbol (lib_id "Device:R") ...)
  (wire (pts (xy 100 100) (xy 150 100)))
  ...
)
```

### Python Libraries
**For KiCad integration:**
- `sexpdata` - Parse S-expressions
- `pcbnew` - KiCad Python API (if available)
- Custom parsers for file generation

**For routing:**
- `networkx` - Graph algorithms for pathfinding
- `shapely` - Geometric operations
- `numpy` - Matrix operations

### Design Rules
**From PCB Design Guide:**
- Trace width: 0.25mm min, 0.4mm recommended
- Clearance: 0.2mm min, 0.3mm recommended
- Via size: 0.8mm drill, 1.6mm pad
- USB differential: 90Ω impedance

---

## 📊 Success Criteria

### Minimum Viable Product (MVP)
- [ ] Generate valid KiCad schematic
- [ ] Generate valid PCB layout
- [ ] Export complete Gerber files
- [ ] Pass DRC with zero errors
- [ ] Generate BOM

### Stretch Goals
- [ ] Aesthetic component placement
- [ ] Auto-routing with optimization
- [ ] Visual preview generation
- [ ] 3D render export

### Validation
- [ ] Generate test PCB for 3x3 macropad
- [ ] Validate Gerbers with online viewer
- [ ] Order test PCB from manufacturer
- [ ] Assemble and test functionality

---

## 🎯 Implementation Strategy

### Week 1: Template Extraction (Task 5)
**Focus:** Parse KiCad files and extract circuit templates

**Deliverables:**
- KiCad schematic parser
- Circuit block identifier
- Template extractor
- Cached templates for 3 MCU types

**Validation:**
- Successfully parse Discipline schematic
- Extract ATmega32A circuit template
- Extract USB-C circuit template
- Cache templates for reuse

### Week 2: Schematic Generation (Task 6)
**Focus:** Generate KiCad schematic files

**Deliverables:**
- Schematic file generator
- Matrix schematic generator
- Circuit combiner
- Schematic validator

**Validation:**
- Generate schematic for 3x3 macropad
- Open in KiCad without errors
- Pass ERC (Electrical Rule Check)
- All nets properly connected

### Week 3: PCB Layout (Task 7)
**Focus:** Component placement and routing

**Deliverables:**
- Component placement algorithm
- Auto-routing engine
- Board outline generator
- DRC validator

**Validation:**
- Generate PCB layout for 3x3 macropad
- Components placed aesthetically
- All traces routed successfully
- Pass DRC with zero errors

### Week 4: Gerber Export & Preview (Task 8)
**Focus:** Manufacturing files and visualization

**Deliverables:**
- Gerber exporter
- Gerber validator
- Manufacturing documentation
- Visual preview generator

**Validation:**
- Export complete Gerber set
- Validate with online viewer
- Generate preview images
- Ready for manufacturing

---

## 🚦 Getting Started

### Step 1: Set Up Development Environment
```bash
cd keyboard-generator

# Install additional dependencies for Phase 2
pip install sexpdata networkx shapely

# Verify KiCad installation
which kicad  # Should show KiCad path
```

### Step 2: Explore PCB Library
```bash
cd ../pcb-library

# List available designs
cat PROJECT_CATALOG.md

# Examine a design file
cat design-files/discipline/discipline.kicad_sch | head -50
```

### Step 3: Create Phase 2 Structure
```bash
cd ../keyboard-generator

# Create new modules for Phase 2
mkdir -p thkg/pcb/templates
mkdir -p thkg/pcb/schematic
mkdir -p thkg/pcb/layout
mkdir -p thkg/pcb/export

# Create test directory
mkdir -p tests/pcb
```

### Step 4: Start with Task 5.1
**First task:** Implement KiCad file parser

**Goal:** Parse .kicad_sch files into Python data structures

**Approach:**
1. Study KiCad S-expression format
2. Use `sexpdata` library for parsing
3. Create data models for schematic elements
4. Test with Discipline schematic

---

## 📝 Notes

### Design Philosophy
- **Proven patterns first:** Use tested circuits from library
- **Aesthetic by default:** Make beautiful PCBs automatically
- **Fail gracefully:** Warn and continue when possible
- **Validate thoroughly:** Catch errors before manufacturing

### Challenges to Expect
- **KiCad file format:** Complex S-expression structure
- **Auto-routing:** Difficult to get right
- **Visual preview:** May require KiCad API or external tools
- **Component placement:** Balancing aesthetics and functionality

### Success Factors
- **Incremental development:** Test each component thoroughly
- **Use library examples:** Learn from proven designs
- **Validate early:** Catch issues before they compound
- **Document decisions:** Explain why things are done certain ways

---

## 🎉 Ready to Begin!

Phase 1 gave us a solid foundation. Phase 2 will deliver the core value: **automatic PCB generation**.

**Next step:** Start with Task 5.1 - Implement KiCad file parser

Let's build something amazing! 🚀

---

**Last Updated:** October 20, 2025  
**Status:** Ready to Start Phase 2
