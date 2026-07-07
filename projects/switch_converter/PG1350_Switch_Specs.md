# PG1350 Switch - Detailed Specification Sheet

**Manufacturer**: Kaihua Electronics (东莞市凯华电子有限公司)  
**Part Number**: CP6135001D02-1  
**Document Date**: 2017-09-15  
**Scale**: 4:1  
**Compliance**: WEEE & ROHS Compliant

---

## Table of Contents
1. [PCB Layout Pattern](#pcb-layout-pattern)
2. [PCB Hole Pattern Details](#pcb-hole-pattern-details)
3. [Physical Dimensions - Top Shell](#physical-dimensions---top-shell)
4. [Physical Dimensions - Bottom Shell](#physical-dimensions---bottom-shell)
5. [Side Profile Dimensions](#side-profile-dimensions)
6. [Mounting Dimensions](#mounting-dimensions)
7. [Additional Dimensions](#additional-dimensions)
8. [Circuit Diagram](#circuit-diagram)
9. [Tolerances](#tolerances)
10. [Drawing Information](#drawing-information)

---

## PCB Layout Pattern (Pattern Side)

```
        ┌─────────────────────┐
        │    ⊕       ⊕        │ 5.90mm
        │   /             \   │
        │  /               \  │
        │ /                 \ │
        │/                   \│
        └─────────────────────┘

Pin Spacing: 3.80mm center-to-center
```

| Dimension | Value |
|-----------|-------|
| Overall Width | 5.90mm |
| Overall Height | 11.00mm |
| Pin Center-to-Center (X) | 3.80mm |
| Pin Center-to-Center (Y) | 5.00mm |
| Top Hole Diameter | φ1.90mm (2 holes) |
| Bottom Hole Diameter | φ1.20mm (2 holes) |
| LED Position | Offset from pins |

---

## PCB Hole Pattern Details

```
        ┌─────────────────────┐
        │    ⊕       ⊕        │ 5.90mm
        │   /             \   │
        │  /               \  │
        │ /                 \ │
        │/                   \│
        └─────────────────────┘

Top Holes: 2 × φ1.90mm
Bottom Holes: 2 × φ1.20mm
```

| Dimension | Value |
|-----------|-------|
| Top Hole Diameter | φ1.90mm (2 holes) |
| Bottom Hole Diameter | φ1.20mm (2 holes) |
| Hole Spacing (X) | 3.80mm |
| Hole Spacing (Y) | 5.00mm |

---

## Physical Dimensions - Top Shell

```
         ┌─────────────────────┐
         │                     │ 15.00mm
         │   ┌───────────────┐  │
         │   │               │  │ 13.80mm
         │   │               │  │
         │   │               │  │
         │   │               │  │
         │   └───────────────┘  │
         │                     │ 13.80mm
         └─────────────────────┘

Top Shell Width: 15.00mm
Top Shell Height: 15.00mm
Internal Opening: 13.80mm × 13.80mm
```

| Dimension | Value |
|-----------|-------|
| Top Shell Width | 15.00mm |
| Top Shell Height | 15.00mm |
| Internal Opening Width | 13.80mm |
| Internal Opening Height | 13.80mm |

---

## Physical Dimensions - Bottom Shell

```
         ┌─────────────────────┐
         │                     │ 15.00mm
         │   ┌───────────────┐  │
         │   │               │  │ 13.80mm
         │   │               │  │
         │   │      [ ]      │  │ 13.80mm
         │   │               │  │
         │   └───────────────┘  │
         │                     │
         └─────────────────────┘

Stem Diameter: φ3.20mm
```

| Dimension | Value |
|-----------|-------|
| Bottom Shell Width | 15.00mm |
| Bottom Shell Height | 15.00mm |
| Internal Opening Width | 13.80mm |
| Internal Opening Height | 13.80mm |
| Stem Diameter | φ3.20mm |

---

## Side Profile Dimensions

```
        ┌───────────────┐
        │               │ 2.65mm
        │    ┌───────┐  │
        │    │       │  │ 14.50mm
        │    │       │  │
        │    │       │  │
        │    └───────┘  │
        │               │
        └───────────────┘

Side Height: 14.50mm
Top Flange Width: 2.65mm
Top Flange Thickness: 0.50mm
Bottom Flange Width: 3.00mm
```

| Dimension | Value |
|-----------|-------|
| Side Profile Height | 14.50mm |
| Top Flange Width | 2.65mm |
| Top Flange Thickness | 0.50mm |
| Bottom Flange Width | 3.00mm |

---

## Mounting Dimensions

```
        ┌───────────────┐
        │               │ 15.00mm
        │    ┌───────┐  │
        │    │       │  │ 13.80mm
        │    │       │  │
        │    │       │  │
        │    └───────┘  │
        │               │
        └───────────────┘

Top Mounting Height: 5.00mm
Bottom Mounting Height: 5.80mm
```

| Dimension | Value |
|-----------|-------|
| Top Mounting Height | 5.00mm |
| Bottom Mounting Height | 5.80mm |
| Total Mounting Height | 10.80mm |
| Overall Height (with flanges) | 15.00mm |

---

## Additional Dimensions

```
        ┌───────────────┐
        │               │ 13.80mm
        │    ┌───────┐  │
        │    │       │  │ 11.00mm
        │    │       │  │
        │    │       │  │
        │    └───────┘  │
        │               │
        └───────────────┘

Top Mounting Height: 5.00mm
Bottom Mounting Height: 3.80mm
```

| Dimension | Value |
|-----------|-------|
| Top Mounting Height | 5.00mm |
| Bottom Mounting Height | 3.80mm |
| LED Hole Diameter | φ3.15mm (5 holes) |

---

## Circuit Diagram

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

---

## Tolerances

| Parameter | Tolerance |
|-----------|-----------|
| Conduction Travel | ±0.5mm |
| Total Travel | +0 / -0.5mm |
| Force Measurements | ±10gf |

---

## Drawing Information

| Field | Value |
|-------|-------|
| DRAWN | Lu Panhao |
| DATE | 2017.09.15 |
| TITLE | PG1350 Keyboard Switch (Burnt Orange) |
| PART NO. | CP6135001D02-1 |
| UNIT | mm |
| SCALE | 4:1 |
| SHEET | 1 OF 1 |

---

## Notes

1. All dimensions are in millimeters (mm) unless otherwise specified
2. Tolerances apply to mechanical dimensions where not explicitly stated
3. Switch complies with WEEE and RoHS directives
4. PCB layout shown is for pattern side view
5. LED hole diameter: φ3.15mm (5 holes)

---

*Document generated from Kaihua Electronics datasheet*