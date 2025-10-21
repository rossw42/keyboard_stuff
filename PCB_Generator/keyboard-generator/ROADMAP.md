# Through-Hole Keyboard Generator - Roadmap

**Last Updated:** October 21, 2025

---

## Phase 1: Plate Generation ✅ COMPLETE

- ✅ YAML/KLE input parsing
- ✅ Matrix calculation
- ✅ Pin assignment
- ✅ Plate geometry generation
- ✅ DXF export
- ✅ 14 layout presets

**Status:** Production ready, fully tested

---

## Phase 2: PCB Generation 🔄 IN PROGRESS

### Current Status: 17% Complete

**Completed:**
- ✅ Task 5.1: KiCad parser (S-expression format)
- ✅ Task 5.2: Circuit block identifier

**In Progress:**
- 🔄 Task 5.3: Template extraction
- ⏳ Task 5.4: Template cache system
- ⏳ Task 5.5: Extract all templates

**Remaining:**
- ⏳ Task 6: Schematic generation
- ⏳ Task 7: PCB layout (artistic placement + auto-routing)
- ⏳ Task 8: Gerber export + visual preview

### Known Limitations

**KiCad Version Support:**
- ✅ KiCad 6/7 (S-expression format) - Fully supported
- ❌ KiCad 5 (text format) - Not yet supported

**Projects Currently Parseable:**
- ✅ Lumberjack (181 components, ATmega328P, USB-C)
- ✅ Litl (115 components, Pro Micro)
- ✅ Dumbpad (67 components, Pro Micro, macropad)

**Projects Requiring KiCad 5 Parser:**
- ⏳ Discipline (ATmega32A, USB-C, 65%)
- ⏳ Mysterium (ATmega32A, TKL)
- ⏳ Tartan (ATmega328P, 60%)
- ⏳ Plaid (ATmega328P, ortholinear)
- ⏳ KBIC65 (Pro Micro, 65%)
- ⏳ Rosaline (ATmega328P, 40%)
- ⏳ GH60 (reference design)

---

## Phase 3: Case Generation ⏳ PLANNED

- ⏳ Sandwich case generation
- ⏳ Tray mount case generation
- ⏳ OpenSCAD code generation
- ⏳ STL rendering
- ⏳ DXF layer export

**Dependencies:** Phase 2 complete

---

## Phase 4: Firmware Generation ⏳ PLANNED

- ⏳ QMK config generation
- ⏳ Keymap generation
- ⏳ VIA support
- ⏳ Firmware validation

**Dependencies:** Phase 2 complete

---

## Phase 5: Integration & Polish ⏳ PLANNED

- ⏳ Output packaging
- ⏳ BOM generation (using library master BOM)
- ⏳ Build guide generation
- ⏳ Documentation generation
- ⏳ Validation system (warn-and-continue)

**Dependencies:** Phases 2-4 complete

---

## Future Enhancements

### High Priority

**KiCad 5 Support**
- **Goal:** Parse KiCad 5 schematic files (text format)
- **Approach:** Either write KiCad 5 parser OR automate conversion to KiCad 6/7
- **Benefit:** Unlock 7 additional library projects
- **Effort:** 2-3 hours for parser, or 1 hour for automated conversion
- **Status:** Deferred until Phase 2 complete

**Recommended Approach:**
```bash
# KiCad has built-in conversion tool
kicad-cli sch upgrade discipline-pcb.sch discipline-pcb.kicad_sch
```

We could create a script to batch-convert all KiCad 5 files in the library:
```python
# scripts/convert_kicad5_to_kicad7.py
for project in kicad5_projects:
    run_kicad_converter(project)
```

**Template Library Expansion**
- Extract templates from all 11 projects
- Build comprehensive template database
- Document all MCU types (ATmega328P, ATmega32A, Pro Micro)
- Document all USB types (USB-C, Mini, Micro)

### Medium Priority

**Additional MCU Support**
- RP2040 (Raspberry Pi Pico)
- STM32 (ARM Cortex-M)
- Nice!nano (wireless)

**Split Keyboard Support**
- Split matrix generation
- TRRS/USB-C interconnect
- Master/slave configuration

**Advanced Routing**
- Routing optimization algorithms
- Aesthetic scoring for trace placement
- Manual routing hints

**Web Interface**
- Browser-based configuration
- Visual layout editor
- Real-time preview
- Cloud generation service

### Low Priority

**AI-Assisted Features**
- Component placement optimization
- Routing suggestions
- Design validation
- Cost optimization

**Manufacturing Integration**
- Direct PCB ordering (JLCPCB, PCBWay)
- Component sourcing automation
- Assembly service integration

**Community Features**
- Design sharing platform
- Template marketplace
- Collaboration tools

---

## Technical Debt

### Current Issues

**None identified** - Code is clean and well-tested

### Future Considerations

**Performance:**
- Current parsing is fast (<100ms per project)
- May need optimization for very large projects (100+ keys)

**Memory:**
- Current memory usage is minimal
- Template caching may need limits for large libraries

**Compatibility:**
- Need to test with KiCad 8 when released
- May need updates for format changes

---

## Milestones

### Milestone 1: Template System ✅ (Week 1)
- ✅ KiCad parser working
- ✅ Circuit block identifier working
- 🔄 Template extraction (in progress)

### Milestone 2: Schematic Generation (Week 2)
- ⏳ Generate valid KiCad schematics
- ⏳ Combine templates
- ⏳ Create switch matrix

### Milestone 3: PCB Layout (Week 3)
- ⏳ Artistic component placement
- ⏳ Auto-routing
- ⏳ Visual preview

### Milestone 4: Phase 2 Complete (Week 3-4)
- ⏳ Gerber export
- ⏳ Order test PCB
- ⏳ Validate design

### Milestone 5: Full System (Week 6-8)
- ⏳ Case generation
- ⏳ Firmware generation
- ⏳ Complete end-to-end workflow

---

## Success Metrics

### Phase 2 Success Criteria
- [ ] Generate valid KiCad PCB files
- [ ] Export manufacturable Gerbers
- [ ] Pass DRC with acceptable warnings
- [ ] Components placed aesthetically
- [ ] All traces routed successfully
- [ ] Visual previews generated
- [ ] Test PCB ordered and validated

### Overall Project Success
- [ ] Generate complete keyboard from YAML config
- [ ] PCB, plate, case, firmware all generated
- [ ] Designs are manufacturable
- [ ] Build guides are clear
- [ ] Community adoption

---

## Community Feedback

**Requested Features:**
- (None yet - project in development)

**Bug Reports:**
- (None yet - project in development)

---

## Version History

**v0.1.0** - Phase 1 Complete (October 2025)
- Plate generation working
- 14 layout presets
- DXF export

**v0.2.0** - Phase 2 In Progress (October 2025)
- KiCad parser
- Circuit block identifier
- Template extraction (in progress)

**v1.0.0** - Target (December 2025)
- Complete PCB generation
- Case generation
- Firmware generation
- Full documentation

---

## Contributing

See individual phase documentation for contribution guidelines.

**Current Focus:** Phase 2 - PCB Generation

**Help Wanted:**
- KiCad 5 parser or conversion script
- Additional template extraction
- Testing with different configurations

---

## Resources

**Documentation:**
- [Phase 2 Tasks](.kiro/specs/keyboard-design-automation/phase-2-tasks.md)
- [Design Document](.kiro/specs/keyboard-design-automation/design.md)
- [Progress Report](PHASE2_PROGRESS.md)

**Library:**
- [PCB Library](../pcb-library/)
- [Master BOM](../pcb-library/boms/master-bom-summary.md)
- [GH60 Specifications](../pcb-library/docs/gh60_pcb_specifications.md)

---

**Last Updated:** October 21, 2025  
**Next Review:** End of Phase 2
