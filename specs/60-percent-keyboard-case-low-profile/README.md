# 60% Keyboard Case - Low-Profile Variant Spec

## Overview

This spec defines a low-profile variant of the 60% keyboard case that reduces the overall height from 20mm to 13mm (35% reduction) while maintaining full compatibility with the same PCB and mounting system.

## Spec Status

- **Requirements:** ✅ Complete and Approved
- **Design:** ✅ Complete and Approved  
- **Tasks:** ✅ Complete and Approved
- **Implementation:** ⏳ Ready to Start

## Key Features

### Height Reduction
- **Total Height:** 13mm (vs 20mm standard) - 35% reduction
- **Top Frame:** 3mm (vs 5mm standard) - 40% reduction
- **Bottom Tray:** 10mm (vs 15mm standard) - 33% reduction

### Maintained Compatibility
- Same PCB (285mm x 94.6mm x 1.6mm)
- Same mounting positions (6 holes)
- Same external footprint (295mm x 105mm)
- Same CNC tools and processes

### Design Adjustments
- **Cavity Depth:** 7mm (vs 10mm standard)
- **Standoff Height:** 2mm (vs 3mm standard)
- **Clearance Below PCB:** 3.4mm (vs 5.4mm standard)
- **Base Thickness:** 3mm (vs 5mm standard)

## Files

- **requirements.md** - Complete requirements specification (11 requirements)
- **design.md** - Detailed design document with dimensions and calculations
- **tasks.md** - Implementation task list (11 main tasks, 28 sub-tasks)

## Quick Start

### Review the Spec

1. Read `requirements.md` for functional requirements
2. Read `design.md` for detailed design decisions
3. Read `tasks.md` for implementation plan

### Start Implementation

Begin with Task 1:
```bash
# Task 1: Create low-profile constants file
# Create src/constants_lp.py with low-profile dimensions
```

Or ask Kiro to help implement specific tasks:
```
"Implement task 1 from the low-profile variant spec"
```

## Design Highlights

### Vertical Stack (13mm total)

```
Top Frame (3mm)
├─ Brass Inserts: 3mm deep (full thickness)
└─ PCB Opening: Through full 3mm

Bottom Tray (10mm)
├─ Cavity: 7mm deep
│  ├─ Standoffs: 2mm high
│  ├─ PCB: 1.6mm thick
│  └─ Clearance: 3.4mm below PCB ✓
└─ Base: 3mm thick ✓
```

### Clearance Verification

```python
# Low-Profile Clearances
cavity_depth = 7.0mm
standoff_height = 2.0mm
pcb_thickness = 1.6mm

clearance_below_pcb = 7.0 - 2.0 - 1.6 = 3.4mm ✓ (≥3mm required)
base_thickness = 10.0 - 7.0 = 3.0mm ✓ (≥3mm required)
```

## Comparison: Standard vs Low-Profile

| Feature | Standard | Low-Profile | Change |
|---------|----------|-------------|--------|
| Total Height | 20mm | 13mm | -35% |
| Top Frame | 5mm | 3mm | -40% |
| Bottom Tray | 15mm | 10mm | -33% |
| Cavity Depth | 10mm | 7mm | -30% |
| Standoff Height | 3mm | 2mm | -33% |
| Clearance Below PCB | 5.4mm | 3.4mm | -37% |
| Base Thickness | 5mm | 3mm | -40% |
| External Footprint | 295x105mm | 295x105mm | Same |
| PCB Compatibility | ✓ | ✓ | Same |
| Mounting Positions | 6 holes | 6 holes | Same |

## Implementation Strategy

### Code Reuse
- Copy existing standard variant scripts
- Add `_lp` suffix to low-profile files
- Update to use `constants_lp.py`
- Maintain parallel structure

### File Organization
```
src/
├── constants.py (standard)
├── constants_lp.py (low-profile) ← NEW
├── geometry/
│   ├── profiles.py (standard)
│   ├── profiles_lp.py (low-profile) ← NEW
│   ├── solid_models.py (standard)
│   └── solid_models_lp.py (low-profile) ← NEW

examples/
├── generate_*_toolpaths.py (standard)
├── generate_*_toolpaths_lp.py (low-profile) ← NEW
├── generate_*_3d.py (standard)
├── generate_*_3d_lp.py (low-profile) ← NEW
├── validate_design.py (standard)
└── validate_design_lp.py (low-profile) ← NEW

output/
├── standard/ (existing outputs)
└── low_profile/ (new outputs) ← NEW
    ├── toolpaths/
    ├── 3d_models/
    └── drawings/
```

## Success Criteria

Implementation will be considered successful when:

1. ✅ All validation checks pass (target: 95%+)
2. ✅ Total height is 13mm (within 12-15mm range)
3. ✅ Clearance below PCB is 3.4mm (≥3mm requirement)
4. ✅ Base thickness is 3mm (≥3mm requirement)
5. ✅ PCB compatibility maintained
6. ✅ All output files generated
7. ✅ Manufacturing documentation complete

## Risk Assessment

### Design Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Reduced clearance (3.4mm) | Medium | Validate with actual PCB, document limits |
| Thin base (3mm) | Medium | Use hardwood, proper grain orientation |
| Shallow brass inserts (3mm) | Low | Quality inserts, proper installation |

### Manufacturing Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Thin stock handling (3mm) | Medium | Proper workholding, light cuts |
| Thin base machining | Low | Careful depth control, verify Z-zero |

## Next Steps

1. **Start Implementation:** Begin with Task 1 (create constants file)
2. **Generate Outputs:** Work through tasks 2-9 to create all files
3. **Validate Design:** Run validation script (task 10)
4. **Document Results:** Create summary documentation (task 11)
5. **Prototype:** Machine prototype to verify design

## Questions?

- Review `requirements.md` for detailed functional requirements
- Review `design.md` for design decisions and calculations
- Review `tasks.md` for step-by-step implementation plan

---

**Spec Version:** 1.0  
**Date:** 2025-10-13  
**Status:** Ready for Implementation  
**Estimated Implementation Time:** 4-6 hours
