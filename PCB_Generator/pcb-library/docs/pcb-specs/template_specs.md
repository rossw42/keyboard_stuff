# [Project Name] PCB Specifications

## PCB Dimensions

- **Length:** [value]mm (±0.2mm)
- **Width:** [value]mm (±0.2mm)
- **Thickness:** 1.6mm (±0.1mm)
- **Corner Radius:** [value]mm
- **Layers:** 2
- **Material:** FR4
- **Surface Finish:** HASL / ENIG

## Mounting Holes

- **Count:** [number]
- **Diameter:** 2.0-2.2mm (for M2 screws)
- **Positional Tolerance:** ±0.1mm

### Positions (from PCB top-left corner)

- **TL** (Top-Left): [x]mm, [y]mm
- **TR** (Top-Right): [x]mm, [y]mm
- **ML** (Middle-Left): [x]mm, [y]mm
- **MR** (Middle-Right): [x]mm, [y]mm
- **BL** (Bottom-Left): [x]mm, [y]mm
- **BR** (Bottom-Right): [x]mm, [y]mm

## USB Cutout

- **Width:** 16.0mm
- **Height:** 8-10mm
- **Position:** [x]mm from PCB left edge
- **Distance from Top:** [y]mm from PCB top edge

## Clearances

- **Below PCB:** 5.0mm minimum (5.4mm+ recommended)
  - Accommodates switch pins (3.3mm), diodes, SMD components, solder joints
- **Above PCB:** 11.0mm minimum (12-15mm recommended)
  - Accommodates switches (5mm), keycaps (7.5mm), key travel (4mm)
- **Around Mounting Holes:** 3mm minimum, 5mm radius clear zone

## Manufacturing Specifications

- **Minimum Trace Width:** 6 mil (0.15mm)
- **Minimum Trace Spacing:** 6 mil (0.15mm)
- **Minimum Drill Size:** 0.3mm
- **Silkscreen:** Both sides
- **Solder Mask:** Both sides
- **Copper Weight:** 1 oz (35 µm)

## Component Specifications

### Through-Hole Components

- **Diodes:** 1N4148 (DO-35 package)
- **Resistors:** Axial through-hole
- **Capacitors:** Radial/axial through-hole
- **MCU:** [Specify type and package]
- **USB Connector:** [Specify type]

### Switch Specifications

- **Switch Type:** Cherry MX compatible
- **Switch Spacing:** 19.05mm (0.75") center-to-center
- **Plate Thickness:** 1.5mm standard
- **Stabilizer Type:** Cherry-style

## Electrical Specifications

- **Operating Voltage:** 5V (USB)
- **Current Draw:** [Specify typical/max]
- **USB Standard:** USB 2.0
- **Polling Rate:** [Specify if known]

## Firmware Support

- **QMK:** [Yes/No with path]
- **VIA:** [Yes/No]
- **VIAL:** [Yes/No]
- **ZMK:** [Yes/No]

## Notes

- [Add any project-specific notes]
- [Manufacturing considerations]
- [Known issues or limitations]
- [Compatibility notes]

## Source

Specifications [extracted/documented/standard]

## References

- Original Repository: [GitHub URL]
- Build Guide: [Link if available]
- License: [License type]

---

**Last Updated:** [Date]
**Specification Version:** 1.0
