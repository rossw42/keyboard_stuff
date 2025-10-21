# PCB Specifications Index
## Through-Hole Keyboard Reference Standards

**Last Updated:** 2025-10-17  
**Status:** ✅ Complete Reference Library

---

## Overview

This directory contains comprehensive reference specifications for through-hole keyboard PCB designs. These documents provide standardized dimensions, clearances, and design guidelines for all common keyboard form factors and components.

---

## Form Factor Specifications

### [60% Keyboard Specifications](gh60_pcb_specifications.md)
**Status:** ✅ Complete and Verified

The definitive reference for 60% keyboard PCBs based on the GH60 standard.

**Key Information:**
- PCB Dimensions: 285.0mm × 94.6mm × 1.6mm
- Mounting Holes: 6 positions (GH60 standard pattern)
- USB Cutout: 16mm wide, centered at 142.5mm
- Clearances: 5mm below, 11mm above PCB
- Compatible PCBs: GH60, DZ60, BM60, HS60, Instant60

**Use When:**
- Designing 60% keyboard cases
- Creating 60% PCB layouts
- Verifying GH60 compatibility
- Planning mounting systems

---

### [65% Keyboard Specifications](65-percent-specs.md)
**Status:** ✅ Complete

Reference specifications for 65% through-hole keyboards based on Discipline V2.

**Key Information:**
- PCB Dimensions: ~310-320mm × 95-100mm × 1.6mm
- Layout: 68-70 keys (alphas + arrows + nav cluster)
- MCU: ATmega32A (DIP-40) typical
- USB: Through-hole USB-C implementation
- Clearances: 5mm below, 11mm above PCB

**Use When:**
- Designing 65% keyboards
- Planning Discipline-style builds
- Understanding USB-C through-hole circuits
- Creating custom 65% layouts

---

### [TKL (Tenkeyless) Specifications](tkl-specs.md)
**Status:** ✅ Complete

Reference specifications for TKL through-hole keyboards based on Mysterium.

**Key Information:**
- PCB Dimensions: ~360-375mm × 140-150mm × 1.6mm
- Layout: 87-88 keys (full layout minus numpad)
- MCU: ATmega32A (DIP-40) typical
- Mounting: 8-12 mounting points recommended
- Clearances: 6mm below (for DIP-40), 11mm above PCB

**Use When:**
- Designing TKL keyboards
- Planning Mysterium-style builds
- Understanding larger PCB support requirements
- Creating full-size layouts without numpad

---

### [40% Keyboard Specifications](40-percent-specs.md)
**Status:** ✅ Complete

Reference specifications for 40% through-hole keyboards based on Rosaline and Litl.

**Key Information:**
- PCB Dimensions: 230-285mm × 95-100mm × 1.6mm (varies widely)
- Layout: 40-48 keys (compact, layer-dependent)
- MCU: ATmega328P (DIP-28) or Pro Micro footprint
- Variants: 60% case compatible (Rosaline) or compact (Litl)
- Clearances: 5mm below, 11-20mm above (for exposed components)

**Use When:**
- Designing compact 40% keyboards
- Planning layer-based layouts
- Creating 60% case-compatible 40% boards
- Designing exposed component aesthetics

---

### [Macropad Specifications](macropad-specs.md)
**Status:** ✅ Complete

Reference specifications for through-hole macropads based on Plaid-Pad and Dumbpad.

**Key Information:**
- PCB Dimensions: 80-100mm × 80-100mm × 1.6mm
- Layout: 4-16 keys (typically 4×4)
- MCU: ATmega328P (VUSB) or Pro Micro footprint
- Optional: Rotary encoders (1-4), OLED displays
- Clearances: 5mm below, 11-20mm above (for exposed components)

**Use When:**
- Designing macropads or numpads
- Integrating rotary encoders
- Adding OLED displays
- Creating compact input devices

---

## Universal Specifications

### [Clearance Requirements](clearance-requirements.md)
**Status:** ✅ Complete

Universal clearance standards for all keyboard form factors.

**Key Information:**
- Vertical Clearances: 5mm below PCB, 11mm above PCB (minimum)
- Horizontal Clearances: PCB opening, mounting holes, USB cutouts
- Component Clearances: MCU, switches, stabilizers, encoders, OLEDs
- Case Design: Wall thickness, standoffs, brass inserts
- Manufacturing Tolerances: ±0.1mm (critical), ±0.2mm (standard)

**Use When:**
- Designing any keyboard case
- Verifying component fit
- Planning case internal features
- Troubleshooting clearance issues

---

### [Switch and Plate Specifications](switch-plate-specs.md)
**Status:** ✅ Complete

Universal standards for mechanical keyboard switches and mounting plates.

**Key Information:**
- Switch Dimensions: 15.6mm × 15.6mm housing, 5mm above PCB
- Switch Spacing: 19.05mm (1u) center-to-center
- Plate Thickness: 1.5mm standard (1.2-2.0mm range)
- Plate Cutouts: 14.0mm × 14.0mm (±0.05mm tolerance)
- Stabilizers: Cherry-style, 2u to 7u sizes
- Keycap Profiles: Cherry, OEM, DSA, XDA, SA, MT3

**Use When:**
- Designing switch plates
- Planning PCB switch footprints
- Selecting plate materials and thickness
- Understanding stabilizer requirements
- Verifying keycap compatibility

---

### [Template Specifications](template_specs.md)
**Status:** ✅ Template

Blank template for creating new PCB specifications.

**Use When:**
- Documenting a new keyboard design
- Creating specifications for custom form factors
- Standardizing project documentation

---

## Quick Reference Tables

### Form Factor Comparison

| Form Factor | Typical Size | Key Count | Common MCU | Mounting |
|-------------|-------------|-----------|------------|----------|
| **60%** | 285×95mm | 61 keys | ATmega32A | 6 holes (GH60 standard) |
| **65%** | 315×95mm | 68-70 keys | ATmega32A | 6-8 holes (custom) |
| **TKL** | 365×145mm | 87-88 keys | ATmega32A | 8-12 holes (custom) |
| **40%** | 230-285×95mm | 40-48 keys | ATmega328P / Pro Micro | 4-6 holes (varies) |
| **Macropad** | 80-100×80mm | 4-16 keys | ATmega328P / Pro Micro | 4 holes (square) |

### Clearance Quick Reference

| Clearance Type | Minimum | Recommended | Notes |
|---------------|---------|-------------|-------|
| **Below PCB** | 5.0mm | 5.4-6.0mm | For components + solder |
| **Above PCB** | 11.0mm | 12-15mm | For switches + keycaps |
| **PCB Opening** | PCB + 1mm | PCB + 1mm | 0.5mm per side |
| **Mounting Holes** | 3mm radius | 5mm radius | Clear zone around holes |
| **USB Cutout** | 16mm wide | 16-18mm wide | For connector + cable |
| **Wall Thickness** | 3.0mm | 4.0mm | For structural integrity |

### MCU Comparison

| MCU | Package | I/O Pins | USB | Typical Use |
|-----|---------|----------|-----|-------------|
| **ATmega328P** | DIP-28 | 23 | VUSB (software) | 40%, macropads |
| **ATmega32A** | DIP-40 | 32 | VUSB (software) | 65%, TKL |
| **Pro Micro** | Module | 18 | Hardware (ATmega32U4) | 40%, macropads |
| **Teensy 2.0** | Module | 25 | Hardware (ATmega32U4) | Alternative to Pro Micro |
| **Nice!nano** | Module | 18 | Bluetooth | Wireless builds |

---

## Usage Guidelines

### For PCB Designers

1. **Start with form factor specs:** Choose the appropriate form factor specification document
2. **Review clearance requirements:** Ensure adequate clearances for all components
3. **Check switch/plate specs:** Verify switch footprints and plate compatibility
4. **Validate against checklist:** Use the design checklist in each specification
5. **Prototype before production:** Test fit with actual components

### For Case Designers

1. **Review form factor specs:** Understand PCB dimensions and mounting requirements
2. **Study clearance requirements:** Ensure adequate internal clearances
3. **Check mounting specifications:** Verify standoff positions and brass insert locations
4. **Validate USB cutout:** Ensure proper USB connector clearance
5. **Prototype before production:** 3D print or test cut before final manufacturing

### For Builders

1. **Identify your PCB:** Determine form factor and specifications
2. **Check compatibility:** Verify case, plate, and keycap compatibility
3. **Review assembly notes:** Understand stabilizer and switch installation
4. **Follow build guide:** Use project-specific build guides when available
5. **Test before final assembly:** Verify all components work before case assembly

---

## Document Maintenance

### Version Control

All specification documents include:
- Document version number
- Last updated date
- Status indicator (✅ Complete, 🚧 In Progress, 📝 Draft)
- Maintained by information

### Updates and Revisions

Specifications are updated when:
- New community designs emerge
- Standards evolve
- Errors or omissions are discovered
- User feedback suggests improvements

### Contributing

To suggest improvements or report issues:
1. Document the issue or suggestion
2. Include specific section references
3. Provide supporting evidence (measurements, datasheets, etc.)
4. Submit via project repository

---

## Additional Resources

### External References

**Standards and Tools:**
- [Keyboard Layout Editor](http://www.keyboard-layout-editor.com/) - Layout planning
- [ai03 Plate Generator](https://kbplate.ai03.com/) - Automated plate generation
- [Swillkb Plate Builder](http://builder.swillkb.com/) - Alternative plate generator
- [QMK Firmware](https://docs.qmk.fm/) - Keyboard firmware documentation

**Component Datasheets:**
- Cherry MX Switch Datasheet
- ATmega328P Datasheet (Microchip)
- ATmega32A Datasheet (Microchip)
- USB-C Connector Datasheets (GCT, Molex, etc.)

**Community Resources:**
- [r/MechanicalKeyboards](https://reddit.com/r/MechanicalKeyboards) - Community discussion
- [GeekHack](https://geekhack.org/) - Keyboard enthusiast forum
- [Deskthority](https://deskthority.net/) - Keyboard wiki and forum

### Related Documentation

**In This Library:**
- [Repository Inventory](../repository_inventory.md) - Catalog of available designs
- [Master BOM](../../boms/master-bom.csv) - Unified component database
- [Component Sourcing Guide](../component_sourcing_guide.md) - Vendor recommendations
- [Design Patterns](../design_patterns.md) - Common design patterns
- [Manufacturing Guide](../manufacturing_guide.md) - PCB ordering guide

---

## Specification Status

| Document | Status | Last Updated | Completeness |
|----------|--------|--------------|--------------|
| 60% Specs | ✅ Complete | 2025-10-14 | 100% |
| 65% Specs | ✅ Complete | 2025-10-17 | 100% |
| TKL Specs | ✅ Complete | 2025-10-17 | 100% |
| 40% Specs | ✅ Complete | 2025-10-17 | 100% |
| Macropad Specs | ✅ Complete | 2025-10-17 | 100% |
| Clearance Requirements | ✅ Complete | 2025-10-17 | 100% |
| Switch/Plate Specs | ✅ Complete | 2025-10-17 | 100% |
| Template | ✅ Complete | 2025-10-17 | 100% |

---

**Document Status:** ✅ Complete  
**Last Updated:** 2025-10-17  
**Maintained By:** Through-Hole Keyboard Library  
**Next Review:** When new form factors or standards emerge

---

**End of Document**
