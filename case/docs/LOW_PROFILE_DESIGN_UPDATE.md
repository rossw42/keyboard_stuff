# Low-Profile Design Update - GH60 Compliance

**Date:** 2025-10-14  
**Status:** ✅ Updated and Verified  
**Reason:** Improved component clearance to meet GH60 specifications

---

## Summary

Updated the low-profile variant design to provide safer component clearance while maintaining the compact form factor. The design now better accommodates standard GH60/DZ60/BM60 PCBs with bottom-mounted components.

## Changes Made

### Height Adjustments

| Parameter | Previous | Updated | Change |
|-----------|----------|---------|--------|
| **Total Height** | 13mm | 14mm | +1mm |
| **Bottom Tray Height** | 10mm | 11mm | +1mm |
| **Cavity Depth** | 7mm | 8mm | +1mm |
| **Clearance Below PCB** | 3.4mm | 4.4mm | +1mm |
| **Base Thickness** | 3mm | 3mm | No change |
| **Top Frame Height** | 3mm | 3mm | No change |

### Rationale

**Previous Design (13mm total):**
- 3.4mm clearance below PCB
- Met minimum 3mm requirement
- Tight fit for some components
- Risk of interference with taller diodes or SMD components

**Updated Design (14mm total):**
- 4.4mm clearance below PCB
- Exceeds 4mm recommended clearance
- Safe margin for standard components:
  - Switch pins: 3.3mm (1.1mm margin)
  - Diodes: 1.5-2mm (2.4-2.9mm margin)
  - SMD components: 0.5-1mm (3.4-3.9mm margin)
  - Solder joints: 0.5mm (3.9mm margin)
- Better compatibility with aftermarket PCBs

## Benefits

1. **Improved Compatibility:** Works with more PCB variants including those with bottom-mounted components
2. **Safer Manufacturing:** Larger margin reduces risk of component interference
3. **Still Compact:** 14mm is still 30% reduction from 20mm standard variant
4. **Within Target:** 14mm falls within 12-15mm low-profile target range
5. **Structural Integrity:** Maintains 3mm base thickness (meets minimum)

## Files Updated

### Constants
- ✅ `src/constants_lp.py` - Updated all dimensional constants

### Specifications
- ✅ `.kiro/specs/60-percent-keyboard-case-low-profile/requirements.md` - Updated requirements
- ✅ `.kiro/specs/60-percent-keyboard-case-low-profile/design.md` - Updated design document

### Verification
- ✅ All assertions pass
- ✅ Clearance verification: 4.4mm ≥ 4mm ✓
- ✅ Base thickness: 3mm ≥ 3mm ✓
- ✅ Total height: 14mm within 12-15mm range ✓

## Design Validation

```python
# Low-Profile Clearance Calculation
cavity_depth = 8.0mm
standoff_height = 2.0mm
pcb_thickness = 1.6mm
clearance_below_pcb = 8.0 - 2.0 - 1.6 = 4.4mm ✓

# Base Thickness Calculation
bottom_tray_height = 11.0mm
cavity_depth = 8.0mm
base_thickness = 11.0 - 8.0 = 3.0mm ✓

# Total Height
top_frame = 3.0mm
bottom_tray = 11.0mm
total_height = 3.0 + 11.0 = 14.0mm ✓
```

## Material Requirements

**Updated Stock Dimensions:**
- Top frame: 295mm × 105mm × 4mm (mill to 3mm) - No change
- Bottom tray: 295mm × 105mm × **13mm** (mill to 11mm) - Changed from 12mm

## Comparison: Standard vs Low-Profile

| Feature | Standard | Low-Profile | Reduction |
|---------|----------|-------------|-----------|
| Total Height | 20mm | 14mm | 30% |
| Top Frame | 5mm | 3mm | 40% |
| Bottom Tray | 15mm | 11mm | 27% |
| Cavity Depth | 10mm | 8mm | 20% |
| Clearance Below PCB | 5.4mm | 4.4mm | 19% |
| Base Thickness | 5mm | 3mm | 40% |

## GH60 Specification Compliance

### ✅ Fully Compliant

- **PCB Dimensions:** 285mm × 94.6mm × 1.6mm ✓
- **PCB Opening:** 286mm × 95.6mm ✓
- **Mounting Holes:** 6 positions at exact coordinates ✓
- **USB Cutout:** 16mm wide, centered ✓
- **Clearance Below PCB:** 4.4mm (exceeds 4mm recommended) ✓
- **Tolerances:** ±0.1mm critical, ±0.2mm standard ✓
- **Wall Thickness:** 4mm (exceeds 3mm minimum) ✓
- **Base Thickness:** 3mm (meets minimum) ✓

## Next Steps

1. ✅ Constants updated
2. ✅ Spec documents updated
3. ✅ Design validation passed
4. ⏳ Regenerate 3D models with new dimensions
5. ⏳ Regenerate CNC toolpaths
6. ⏳ Update technical drawings
7. ⏳ Test with actual PCB (recommended before production)

## Recommendations

1. **Prototype First:** 3D print or CNC a test piece to verify fit with actual PCB
2. **Component Check:** Measure tallest components on your specific PCB
3. **Material Selection:** Use quality hardwood with proper grain orientation for 3mm base
4. **Documentation:** Update any external documentation referencing 13mm height

---

**Design Status:** ✅ Ready for Implementation  
**Compliance:** ✅ Meets GH60 Specifications  
**Safety Margin:** ✅ 4.4mm clearance (1.1mm above switch pins)  
**Structural Integrity:** ✅ 3mm base thickness maintained
