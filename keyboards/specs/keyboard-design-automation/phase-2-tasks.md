# Phase 2: PCB Generation - Task List

**Status:** Ready to Start  
**Goal:** Generate complete, manufacturable PCBs with artistic component placement  
**Timeline:** 2-3 weeks  
**Dependencies:** Phase 1 (Plate Generation) ✅ Complete

---

## Overview

Phase 2 builds on the successful plate generator to create complete PCB designs. We'll leverage the 11 validated designs in the PCB library as templates and reference implementations.

**Key Features:**
- ✅ Template-based circuit generation (use proven designs)
- ✅ Automatic matrix generation and routing
- ✅ Artistic component placement (visible components as art)
- ✅ Visual preview generation
- ✅ Gerber export for manufacturing

---

## Task Breakdown

### 🔧 Task 5: Template Extraction System (Foundation)
**Priority:** HIGH - Required for all PCB generation  
**Estimated Time:** 3-4 days

- [ ] **5.1 Implement KiCad file parser**
  - Parse `.kicad_sch` schematic files
  - Extract components with properties
  - Extract net connections
  - Parse component positions
  - **Test with:** Lumberjack schematic

- [ ] **5.2 Implement circuit block identifier**
  - Identify MCU circuits (ATmega328P, ATmega32A, Pro Micro)
  - Identify USB circuits (USB-C, Mini, Micro)
  - Identify reset circuits (tactile switches)
  - Identify crystal circuits (16MHz + capacitors)
  - **Reference:** All 11 projects in library

- [ ] **5.3 Implement template extractor**
  - Extract component list with values
  - Extract net connections
  - Document input/output pins
  - Calculate power requirements
  - **Output:** Reusable CircuitTemplate objects

- [ ] **5.4 Create template cache system**
  - Store extracted templates as JSON
  - Version templates (track source project)
  - Validate template integrity
  - Quick load from cache
  - **Location:** `thkg/templates/cache/`

- [ ] **5.5 Extract templates from library**
  - Extract ATmega328P circuit from Lumberjack
  - Extract ATmega32A circuit from Discipline
  - Extract Pro Micro footprint from Litl
  - Extract USB-C circuit from Discipline
  - Extract USB Mini circuit from Tartan
  - Extract reset circuit (common pattern)
  - Extract crystal circuit (common pattern)
  - **Deliverable:** 7+ reusable templates

**Success Criteria:**
- Can parse all 11 library projects
- Templates load in <100ms
- Templates validate correctly

---

### 🎨 Task 6: PCB Generation - Schematic
**Priority:** HIGH - Core functionality  
**Estimated Time:** 4-5 days

- [ ] **6.1 Implement schematic generator**
  - Create KiCad schematic file structure
  - Add template circuits (MCU, USB, reset, crystal)
  - Generate switch matrix
  - Connect matrix to MCU pins
  - **Output:** `.kicad_sch` file

- [ ] **6.2 Implement matrix schematic generator**
  - Place switch symbols in grid
  - Place diode symbols (one per switch)
  - Create row nets (connect all switches in row)
  - Create column nets (connect all switches in column)
  - Label nets appropriately (ROW0, COL0, etc.)
  - **Reference:** Plaid matrix (4x12)

- [ ] **6.3 Implement circuit combiner**
  - Combine template circuits into one schematic
  - Connect power nets (VCC, GND)
  - Connect USB data lines (D+, D-)
  - Add decoupling capacitors
  - Connect reset circuit
  - **Test:** Validate all nets connected

- [ ] **6.4 Implement schematic validator**
  - Check all nets connected (no floating pins)
  - Verify power connections (VCC, GND to all ICs)
  - Check for duplicate net names
  - Validate component values
  - **Output:** Validation report

**Success Criteria:**
- Generates valid KiCad schematic
- All components connected
- Passes KiCad ERC (Electrical Rule Check)

---

### 🎯 Task 7: PCB Generation - Layout (ARTISTIC FOCUS)
**Priority:** HIGH - Differentiator  
**Estimated Time:** 5-6 days

- [ ] **7.1 Implement artistic component placement**
  - Place switches at calculated positions (from Phase 1)
  - Place diodes in aesthetic grid patterns near switches
  - Place MCU centrally with visual balance
  - Place USB connector at specified position
  - Place supporting components (resistors, capacitors) in symmetrical patterns
  - Implement aesthetic algorithms:
    - Grid alignment for passive components
    - Symmetrical arrangements
    - Visual balance (weight distribution)
    - Color coordination (future: specify component colors)
  - **Reference:** Plaid, Tartan (visible component aesthetic)

- [ ] **7.2 Implement auto-routing**
  - Auto-route matrix rows (grid-based routing)
  - Auto-route matrix columns
  - Auto-route power traces (VCC, GND)
  - Auto-route USB traces (D+, D-, VBUS)
  - Add ground plane (flood fill)
  - Optimize for aesthetics (clean, organized traces)
  - **Algorithm:** Grid-based routing with aesthetic scoring

- [ ] **7.3 Implement board outline**
  - Create PCB outline from dimensions
  - Add mounting holes at specified positions
  - Add edge cuts with corner radius
  - Add USB cutout
  - **Reference:** GH60 specifications

- [ ] **7.4 Implement design rule check**
  - Run KiCad DRC
  - Check trace clearances (0.15mm minimum)
  - Check component clearances
  - Verify mounting hole clearances
  - **Output:** DRC report (warn-and-continue)

**Success Criteria:**
- Components placed aesthetically
- All traces routed successfully
- Passes DRC with acceptable warnings
- Visual preview looks intentional

---

### 📦 Task 8: PCB Generation - Gerber Export & Preview
**Priority:** HIGH - Manufacturing output  
**Estimated Time:** 3-4 days

- [ ] **8.1 Implement Gerber exporter**
  - Export all copper layers (F.Cu, B.Cu)
  - Export soldermask layers (F.Mask, B.Mask)
  - Export silkscreen layers (F.SilkS, B.SilkS)
  - Export drill files (.drl)
  - Export board outline (Edge.Cuts)
  - **Format:** RS-274X (standard Gerber)

- [ ] **8.2 Implement Gerber validator**
  - Verify all layers present
  - Check file completeness
  - Validate drill file format
  - Test with Gerber viewer (gerbv or KiCad)
  - **Output:** Validation report

- [ ] **8.3 Create manufacturing documentation**
  - Generate fabrication notes (stackup, finish, etc.)
  - Document PCB specifications (thickness, copper weight)
  - List special requirements
  - **Output:** `fabrication_notes.txt`

- [ ] **8.5 Visual preview generation (CHALLENGING)**
  - **8.5.1** Generate top view image (component placement)
  - **8.5.2** Generate bottom view image (traces)
  - **8.5.3** Export as PNG/SVG
  - **8.5.4** Add annotations (dimensions, features)
  - **8.5.5** Generate thumbnail for quick preview
  - **Optional:** 3D render using KiCad 3D viewer
  - **Tool:** KiCad plot/export functions or pcbnew Python API

**Success Criteria:**
- Gerbers pass manufacturer validation
- Preview images show design clearly
- All documentation complete

---

### 🔗 Task 11: Output Packaging (Partial)
**Priority:** MEDIUM - User experience  
**Estimated Time:** 2 days

- [ ] **11.1 Implement file organizer**
  - Create output directory structure
  - Copy generated files to appropriate locations
  - Organize by type (pcb/, gerbers/, docs/)
  - **Structure:**
    ```
    output/[project-name]/
    ├── pcb/
    │   ├── [project].kicad_sch
    │   ├── [project].kicad_pcb
    │   └── preview/
    │       ├── top.png
    │       └── bottom.png
    ├── gerbers/
    │   ├── [project]-F_Cu.gbr
    │   ├── [project]-B_Cu.gbr
    │   └── ... (all Gerber files)
    ├── plate/
    │   └── [project]-plate.dxf
    └── README.md
    ```

- [ ] **11.2 Implement BOM generator**
  - Extract components from schematic
  - Add quantities
  - Add vendor part numbers from library master BOM
  - Format as CSV
  - **Reference:** `pcb-library/boms/master-bom.csv`

- [ ] **11.3 Implement documentation generator**
  - Generate README with build instructions
  - List generated files
  - Add sourcing information
  - Include next steps (ordering PCB, sourcing components)
  - **Template:** Use library build guides as reference

**Success Criteria:**
- Clean, organized output directory
- BOM matches schematic
- Documentation is clear and helpful

---

### ✅ Task 12: Validation System (Warn-and-Continue)
**Priority:** MEDIUM - Quality assurance  
**Estimated Time:** 2-3 days

- [ ] **12.1 Implement electrical validator**
  - Check power connections (FAIL on critical errors)
  - Verify matrix connectivity (FAIL on disconnected switches)
  - Check USB connections (WARN on non-critical issues)
  - Validate pin assignments (WARN on conflicts)
  - **Output:** Categorized issues (CRITICAL, WARNING, INFO)

- [ ] **12.2 Implement clearance checker**
  - Check component clearances (WARN if tight)
  - Verify switch spacing (FAIL if too close)
  - Check mounting hole clearances (WARN if tight)
  - Validate edge clearances (WARN if tight)
  - **Thresholds:** Configurable by user

- [ ] **12.3 Implement specification validator**
  - Check against library specs (WARN on deviations)
  - Verify dimensions (WARN if non-standard)
  - Validate mounting holes (WARN if misaligned)
  - Check USB cutout position (WARN if off-center)
  - **Reference:** `pcb-library/docs/gh60_pcb_specifications.md`

- [ ] **12.4 Implement validation reporting**
  - Categorize issues (CRITICAL, WARNING, INFO)
  - Generate validation report
  - Allow user to set strictness level (--strict, --permissive)
  - Preserve partial outputs on warnings
  - **Output:** `validation_report.txt`

**Success Criteria:**
- Catches critical errors (no power, disconnected matrix)
- Warns on non-critical issues
- User can adjust strictness
- Partial outputs preserved

---

### 🧪 Task 14: Integration and Testing (Partial)
**Priority:** HIGH - Validation  
**Estimated Time:** 2-3 days

- [ ] **14.1 Create integration tests**
  - Test end-to-end PCB generation
  - Test with multiple configurations (60%, 65%, macropad)
  - Test error handling
  - Test with library templates
  - **Framework:** pytest

- [ ] **14.2 Create example configurations**
  - Create 60% ANSI example (using ATmega328P)
  - Create 65% example (using ATmega32A)
  - Create macropad example (3x3, 4x4)
  - **Location:** `examples/`

- [ ] **14.3 Validate generated designs**
  - Generate test PCBs
  - Validate Gerbers with manufacturer
  - Check visual previews
  - Verify BOMs
  - **Goal:** Order test PCB from JLCPCB/PCBWay

- [ ] **14.4 Create documentation**
  - Write Phase 2 user guide
  - Document PCB generation process
  - Add troubleshooting guide
  - Create examples
  - **Location:** `keyboard-generator/docs/`

**Success Criteria:**
- All tests pass
- Example configurations work
- Generated PCBs are manufacturable
- Documentation is clear

---

### 🔗 Task 15: Library Integration
**Priority:** HIGH - Leverage existing work  
**Estimated Time:** Ongoing

- [ ] **15.1 Implement library reference system**
  - Link to library templates
  - Reference library specs
  - Use library components
  - **Path:** `../pcb-library/`

- [ ] **15.2 Use library master BOM**
  - Load master BOM data
  - Match components to library parts
  - Add vendor part numbers
  - **Source:** `pcb-library/boms/master-bom.csv`

- [ ] **15.3 Validate against library specs**
  - Check dimensions against GH60 specs
  - Verify mounting hole positions
  - Validate USB cutout
  - **Reference:** `pcb-library/docs/gh60_pcb_specifications.md`

**Success Criteria:**
- Templates load from library
- BOM uses library data
- Designs match library specs

---

## Phase 2 Milestones

### Milestone 1: Template System Working (Week 1)
- ✅ Task 5 complete
- Can extract and cache templates
- Templates validate correctly

### Milestone 2: Schematic Generation Working (Week 2)
- ✅ Task 6 complete
- Can generate valid schematics
- Matrix connects to MCU

### Milestone 3: PCB Layout Working (Week 2-3)
- ✅ Task 7 complete
- Components placed aesthetically
- Traces routed successfully
- Visual preview generated

### Milestone 4: Gerber Export Working (Week 3)
- ✅ Task 8 complete
- Gerbers export correctly
- Validation passes
- Preview images generated

### Milestone 5: Phase 2 Complete (End of Week 3)
- ✅ All tasks complete
- Integration tests pass
- Example PCBs generated
- Documentation complete
- **Deliverable:** Order test PCB!

---

## Success Criteria for Phase 2

### Technical Success
- [ ] Generates valid KiCad PCB files
- [ ] Exports manufacturable Gerbers
- [ ] Passes DRC with acceptable warnings
- [ ] Components placed aesthetically
- [ ] All traces routed successfully
- [ ] Visual previews generated

### Quality Success
- [ ] Test PCB ordered and validated
- [ ] BOM matches schematic
- [ ] Documentation is clear
- [ ] Examples work correctly

### User Success
- [ ] Easy to use (simple YAML config)
- [ ] Fast generation (<30 seconds)
- [ ] Clear error messages
- [ ] Helpful validation reports

---

## Resources

### Reference Projects (from PCB Library)
- **Lumberjack:** ATmega328P, USB-C, 60 keys
- **Plaid:** ATmega328P, USB Mini, 48 keys, visible components
- **Tartan:** ATmega328P, USB Mini, 64 keys
- **Discipline:** ATmega32A, USB-C, 68 keys
- **Mysterium:** ATmega32A, USB Mini, 87 keys
- **Litl:** Pro Micro, 45 keys

### Key Documents
- `pcb-library/boms/master-bom-summary.md` - Component reference
- `pcb-library/docs/gh60_pcb_specifications.md` - PCB specs
- `pcb-library/PROJECT_CATALOG.md` - Project reference
- `.kiro/specs/keyboard-design-automation/design.md` - Design doc

### Tools & Libraries
- **KiCad Python API:** pcbnew, eeschema
- **File Parsing:** sexpdata (for KiCad S-expressions)
- **Gerber Export:** KiCad built-in
- **Preview Generation:** KiCad plot functions
- **Testing:** pytest

---

## Next Steps

1. **Review this task list** - Confirm approach
2. **Set up development environment** - Install KiCad Python API
3. **Start with Task 5.1** - Parse KiCad schematic files
4. **Test with Lumberjack** - Use as reference implementation
5. **Iterate quickly** - Build, test, validate

---

**Ready to start?** Let's begin with Task 5.1 - parsing KiCad schematic files!

