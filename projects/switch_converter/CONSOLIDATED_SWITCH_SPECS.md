# PG1350 to PG1425 Switch Adapter - Consolidated Specifications

**Project**: PG1350 Switch Adapter for PG1425 PCB Footprints  
**Purpose**: Enable PG1350 switches to work with PG1425-based keyboards  
**Design Approach**: Plate-mounted bezel with dual-ended stamped contacts  
**CAD Tool**: OpenSCAD (D:\Program Files\OpenSCAD (Nightly)\openscad.exe)

---

## Executive Summary

This document consolidates all critical specifications for the PG1350 and PG1425 switches to enable design of an adapter that bridges the ~1.4mm gap per side between the two switch types.

| Feature | PG1350 | PG1425 | Gap (Per Side) |
|---------|---------|--------|----------------|
| Body size | 13.8 × 13.8 mm | 10.2 × 10.2 mm | ~1.8 mm per side |
| PCB width | 5.90 mm | 5.50 mm | 0.40 mm total |
| Contact style | Flat stamped | Flat stamped | Compatible! |
| Contact count | 2 | 2 | Compatible! |
| Center post | Yes | Yes | Compatible! |

---

## PG1350 Switch Specifications

### Part Information
- **Manufacturer**: Kaihua Electronics (东莞市凯华电子有限公司)
- **Part Number**: CP6135001D02-1
- **Document Date**: 2017-09-15
- **Scale**: 4:1
- **Compliance**: WEEE & ROHS Compliant

### PCB Interface (Pattern Side)
| Dimension | Value |
|-----------|-------|
| Overall Width | 5.90mm |
| Overall Height | 11.00mm |
| Pin Center-to-Center (X) | 3.80mm |
| Pin Center-to-Center (Y) | 5.00mm |
| Top Hole Diameter | φ1.90mm (2 holes) |
| Bottom Hole Diameter | φ1.20mm (2 holes) |

### Physical Dimensions - Top Shell
| Dimension | Value |
|-----------|-------|
| Top Shell Width | 15.00mm |
| Top Shell Height | 15.00mm |
| Internal Opening Width | 13.80mm |
| Internal Opening Height | 13.80mm |

### Physical Dimensions - Bottom Shell
| Dimension | Value |
|-----------|-------|
| Bottom Shell Width | 15.00mm |
| Bottom Shell Height | 15.00mm |
| Internal Opening Width | 13.80mm |
| Internal Opening Height | 13.80mm |
| Stem Diameter | φ3.20mm |

### Side Profile Dimensions
| Dimension | Value |
|-----------|-------|
| Side Profile Height | 14.50mm |
| Top Flange Width | 2.65mm |
| Top Flange Thickness | 0.50mm |
| Bottom Flange Width | 3.00mm |

### Mounting Dimensions
| Dimension | Value |
|-----------|-------|
| Top Mounting Height | 5.00mm |
| Bottom Mounting Height | 5.80mm |
| Total Mounting Height | 10.80mm |
| Overall Height (with flanges) | 15.00mm |

### Circuit Diagram
```
    ┌─────┐
    │ ①──○───┐
    └─────┘  │
             ├── Switch Contacts
    ┌─────┐  │
    │ ②──○───┘
    └─────┘
```
- **Terminal 1**: Positive contact
- **Terminal 2**: Negative contact
- **Switch Type**: SPST (Single Pole Single Throw)

### Tolerances
| Parameter | Tolerance |
|-----------|-----------|
| Conduction Travel | ±0.5mm |
| Total Travel | +0 / -0.5mm |
| Force Measurements | ±10gf |

---

## PG1425 Switch Specifications

### Part Information
- **Manufacturer**: Kaihua Electronics (东莞市凯华电子有限公司)
- **Part Number**: CP6142501D02
- **Document Date**: 2017-04-18
- **Scale**: 1:1
- **Compliance**: WEEE & ROHS Compliant

### PCB Interface (Copper Clad Side)
| Dimension | Value |
|-----------|-------|
| Overall Width | 5.50mm |
| Overall Height | 5.50mm |
| Pin Center-to-Center | 2.90mm |
| Top Land Width | 5.10mm |
| Bottom Land Width | 5.50mm |

### PCB Hole Pattern
| Dimension | Value |
|-----------|-------|
| Top Hole Diameter | φ1.30mm (2 holes) |
| Bottom Hole Diameter | φ1.10mm (2 holes) |
| Hole Spacing (X) | 5.10mm |
| Hole Spacing (Y) | 5.50mm |

### Physical Dimensions - Top Shell
| Dimension | Value |
|-----------|-------|
| Top Shell Width | 14.00mm |
| Top Shell Height | 14.80mm |
| Internal Opening Width | 10.20mm |
| Internal Opening Height | 10.20mm |

### Physical Dimensions - Bottom Shell
| Dimension | Value |
|-----------|-------|
| Bottom Shell Width | 14.00mm |
| Bottom Shell Height | 14.00mm |
| Internal Opening Width | 10.20mm |
| Internal Opening Height | 10.20mm |
| Stem Diameter | φ0.90mm |

### Side Profile Dimensions
| Dimension | Value |
|-----------|-------|
| Side Profile Height | 14.00mm |
| Top Flange Width | 2.50mm |
| Top Flange Thickness | 0.60mm |
| Bottom Flange Width | 0.70mm |

### Mounting Dimensions
| Dimension | Value |
|-----------|-------|
| Top Mounting Height | 5.00mm |
| Bottom Mounting Height | 5.00mm |
| Total Mounting Height | 10.00mm |
| Overall Height (with flanges) | 14.80mm |

### Circuit Diagram
```
    ┌─────┐
    │ ①──●───┐
    └─────┘  │
             ├── Switch Contacts
    ┌─────┐  │
    │ ②──●───┘
    └─────┘
```
- **Terminal 1**: Positive contact
- **Terminal 2**: Negative contact
- **Switch Type**: SPST (Single Pole Single Throw)

### Tolerances
| Parameter | Tolerance |
|-----------|-----------|
| Pretravel | ±0.3mm |
| Total Travel | ±0.3mm |
| Force Measurements | ±10gf |

---

## Critical Adapter Design Dimensions

### Body Size Difference (Adapter Must Bridge)
| Dimension | PG1350 | PG1425 | Gap to Bridge |
|-----------|---------|--------|---------------|
| Internal Opening Width | 13.80mm | 10.20mm | 3.60mm total (1.80mm per side) |
| Internal Opening Height | 13.80mm | 10.20mm | 3.60mm total (1.80mm per side) |

### PCB Interface Gap
| Dimension | PG1350 | PG1425 | Gap to Bridge |
|-----------|---------|--------|---------------|
| Overall Width | 5.90mm | 5.50mm | 0.40mm total (0.20mm per side) |

### Mounting Height Difference
| Dimension | PG1350 | PG1425 | Difference |
|-----------|---------|--------|------------|
| Top Mounting Height | 5.00mm | 5.00mm | 0.00mm |
| Bottom Mounting Height | 5.80mm | 5.00mm | 0.80mm |
| Total Mounting Height | 10.80mm | 10.00mm | 0.80mm |

### Hole Diameter Differences (Adapter Must Accommodate)
| Location | PG1350 | PG1425 | Adapter Requirement |
|----------|---------|--------|---------------------|
| Top Holes | φ1.90mm | φ1.30mm | Must fit both: φ1.90mm max |
| Bottom Holes | φ1.20mm | φ1.10mm | Must fit both: φ1.20mm max |

### Stem Diameter (Adapter Contact Interface)
| Switch | PG1350 | PG1425 | Adapter Requirement |
|--------|---------|--------|---------------------|
| Stem Diameter | φ3.20mm | φ0.90mm | Dual-ended contacts needed |

---

## Design Constraints Summary

### Mechanical Shell (3D Printed)
- Must accommodate PG1350 body: 15.00 × 15.00mm external, 13.80 × 13.80mm internal opening
- Must bridge ~1.80mm gap per side to PG1425 footprint (10.20 × 10.20mm)
- Must provide mounting interface for both switch types

### Dual-Ended Stamped Contacts
- **PG1350 End**: 
  - Pin spacing: 3.80mm X, 5.00mm Y
  - Top holes: φ1.90mm (2 holes)
  - Bottom holes: φ1.20mm (2 holes)
  - Stem interface: φ3.20mm
  
- **PG1425 End**:
  - Pin spacing: 2.90mm X, 5.50mm Y
  - Top land width: 5.10mm
  - Bottom land width: 5.50mm
  - Top holes: φ1.30mm (2 holes)
  - Bottom holes: φ1.10mm (2 holes)
  - Stem interface: φ0.90mm

### Electrical Requirements
- SPST switch contacts (positive/negative terminals)
- Center post compatibility (both switches have center posts)
- Flat stamped contact style (compatible between both types)

---

## Design Recommendations

### Contact Design
1. **Dual-ended stamped contacts** with:
   - PG1350-compatible end on one side
   - PG1425-compatible end on other side
   - Center post pass-through for mechanical stability

2. **Contact mounting**: 
   - Plate-mounted design allows contact replacement without reflowing solder
   - Contacts should be serviceable components

### Shell Design
1. **3D printed mechanical shell** with:
   - Internal cavity for PG1350 body (13.80 × 13.80mm opening)
   - External interface for PG1425 PCB (10.20 × 10.20mm footprint)
   - Bridge features to span ~1.80mm gap per side

2. **Mounting interface**:
   - Top: 5.00mm mounting height (matches both switches)
   - Bottom: 5.80mm for PG1350, 5.00mm for PG1425 (adapter must accommodate both)

### Tolerance Considerations
- Mechanical tolerances: ±0.5mm (PG1350), ±0.3mm (PG1425)
- Design with ~0.2mm clearance on critical interfaces
- Account for 3D printing layer height and overhang limitations

---

## Bill of Materials (BOM)

### Primary Components
| Item | Description | Quantity | Notes |
|------|-------------|----------|-------|
| 1 | PG1350 Switch Body | 1 per adapter | Kaihua CP6135001D02-1 |
| 2 | Dual-ended stamped contacts | 1 per switch position | Custom design |
| 3 | 3D printed mechanical shell | 1 per adapter | OpenSCAD design |

### Materials
| Material | Application | Notes |
|----------|-------------|-------|
| PLA/PETG/ABS | Mechanical shell | Choose based on use case |
| Phosphor Bronze | Stamped contacts | Good conductivity and spring |
| Stainless Steel | Center post (optional) | For added mechanical stability |

---

## Testing Checklist

### Before Assembly
- [ ] Verify PG1350 switch specifications match design assumptions
- [ ] Confirm PG1425 footprint dimensions from official documentation
- [ ] Check hot-swap contact compatibility with PG1350 pins

### After Assembly
- [ ] Test electrical continuity between all pins
- [ ] Verify mechanical fit with PG1425 PCB
- [ ] Test switch actuation feel and consistency
- [ ] Check for any short circuits or loose connections

---

## Document Information

| Field | Value |
|-------|-------|
| Project | PG1350 to PG1425 Switch Adapter |
| Version | 1.0 |
| Date | 2026-07-06 |
| CAD Tool | OpenSCAD |
| Status | Ready for CAD Design Phase |

---

*Document generated from Kaihua Electronics datasheets*