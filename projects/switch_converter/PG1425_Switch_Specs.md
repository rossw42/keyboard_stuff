# PG1425 Switch - Detailed Specification Sheet

**Manufacturer**: Kaihua Electronics (东莞市凯华电子有限公司)  
**Part Number**: CP6142501D02  
**Document Date**: 2017-04-18  
**Scale**: 1:1  
**Compliance**: WEEE & ROHS Compliant

---

## Table of Contents
1. [PCB Land Pattern](#pcb-land-pattern)
2. [PCB Hole Pattern](#pcb-hole-pattern)
3. [Physical Dimensions - Top Shell](#physical-dimensions---top-shell)
4. [Physical Dimensions - Bottom Shell](#physical-dimensions---bottom-shell)
5. [Side Profile Dimensions](#side-profile-dimensions)
6. [Mounting Dimensions](#mounting-dimensions)
7. [Circuit Diagram](#circuit-diagram)
8. [Tolerances](#tolerances)
9. [Drawing Information](#drawing-information)

---

## PCB Land Pattern (Full Color LED)

```
        ┌─────────────────────┐
        │                     │ 5.50mm
        │      ┌───────┐      │
        │      │       │      │
        │      │ LED   │      │
        │      │       │      │
        │      └───────┘      │
        │                     │
        └─────────────────────┘

Pin Spacing: 2.90mm center-to-center
```

| Dimension | Value |
|-----------|-------|
| Overall Width | 5.50mm |
| Overall Height | 5.50mm |
| Pin Center-to-Center | 2.90mm |
| LED Position (X) | 4.10mm from left pin |
| LED Position (Y) | 1.15mm from bottom pin |
| Top Land Width | 5.10mm |
| Bottom Land Width | 5.50mm |

---

## PCB Hole Pattern (Copper Clad Side View)

```
        ┌─────────────────────┐
        │    ⊕       ⊕        │ 5.50mm
        │   /             \   │
        │  /               \  │
        │ /                 \ │
        │/                   \│
        └─────────────────────┘

Top Holes: 2 × φ1.30mm
Bottom Holes: 2 × φ1.10mm
```

| Dimension | Value |
|-----------|-------|
| Top Hole Diameter | φ1.30mm (2 holes) |
| Bottom Hole Diameter | φ1.10mm (2 holes) |
| Hole Spacing (X) | 5.10mm |
| Hole Spacing (Y) | 5.50mm |

---

## Physical Dimensions - Top Shell

```
         ┌─────────────────────┐
         │                     │ 14.00mm
         │   ┌───────────────┐  │
         │   │               │  │ 10.20mm
         │   │               │  │
         │   │               │  │
         │   │               │  │
         │   └───────────────┘  │
         │                     │ 10.20mm
         └─────────────────────┘

Top Shell Width: 14.00mm
Top Shell Height: 14.80mm
Internal Opening: 10.20mm × 10.20mm
```

| Dimension | Value |
|-----------|-------|
| Top Shell Width | 14.00mm |
| Top Shell Height | 14.80mm |
| Internal Opening Width | 10.20mm |
| Internal Opening Height | 10.20mm |

---

## Physical Dimensions - Bottom Shell

```
         ┌─────────────────────┐
         │                     │ 14.00mm
         │   ┌───────────────┐  │
         │   │               │  │ 10.20mm
         │   │               │  │
         │   │      [ ]      │  │ 10.20mm
         │   │               │  │
         │   └───────────────┘  │
         │                     │
         └─────────────────────┘

Stem Diameter: 0.90mm
```

| Dimension | Value |
|-----------|-------|
| Bottom Shell Width | 14.00mm |
| Bottom Shell Height | 14.00mm |
| Internal Opening Width | 10.20mm |
| Internal Opening Height | 10.20mm |
| Stem Diameter | 0.90mm |

---

## Side Profile Dimensions

```
        ┌───────────────┐
        │               │ 0.60mm
        │    ┌───────┐  │
        │    │       │  │ 14.00mm
        │    │       │  │
        │    │       │  │
        │    └───────┘  │
        │               │
        └───────────────┘

Side Height: 14.00mm
Top Flange Width: 2.50mm
Top Flange Thickness: 0.60mm
Bottom Flange Width: 0.70mm
```

| Dimension | Value |
|-----------|-------|
| Side Profile Height | 14.00mm |
| Top Flange Width | 2.50mm |
| Top Flange Thickness | 0.60mm |
| Bottom Flange Width | 0.70mm |

---

## Mounting Dimensions

```
        ┌───────────────┐
        │               │ 14.80mm
        │    ┌───────┐  │
        │    │       │  │ 10.20mm
        │    │       │  │
        │    │       │  │
        │    └───────┘  │
        │               │
        └───────────────┘

Top Mounting Height: 5.00mm
Bottom Mounting Height: 5.00mm
```

| Dimension | Value |
|-----------|-------|
| Top Mounting Height | 5.00mm |
| Bottom Mounting Height | 5.00mm |
| Total Mounting Height | 10.00mm |
| Overall Height (with flanges) | 14.80mm |

---

## Circuit Diagram

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

---

## Tolerances

| Parameter | Tolerance |
|-----------|-----------|
| Pretravel | ±0.3mm |
| Total Travel | ±0.3mm |
| Force Measurements | ±10gf |

---

## Drawing Information

| Field | Value |
|-------|-------|
| DRAWN | IvPanhao |
| DATE | 2017-04-18 |
| TITLE | PG1425 键盘开关 (茶轴 T=2.0mm) |
| PART NO. | CP6142501D02 |
| UNIT | mm |
| SCALE | 1:1 |
| SHEET | 1 OF 1 |

---

## Notes

1. All dimensions are in millimeters (mm) unless otherwise specified
2. Tolerances apply to mechanical dimensions where not explicitly stated
3. Switch complies with WEEE and RoHS directives
4. PCB hole pattern shown is for copper clad side view
5. LED position is for full color LED variant

---

*Document generated from Kaihua Electronics datasheet*