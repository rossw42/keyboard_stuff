# 60% Through-Hole Keyboard References

A curated collection of documentation, specifications, and resources for designing a 60% mechanical keyboard case with through-hole PCB components.

## Project Overview
- **Form Factor:** 60% (61-key layout)
- **PCB Type:** Through-hole components (requires additional clearance below PCB)
- **Case Material:** Wood (hardwood/plywood)
- **Manufacturing:** CNC milling with 3D printed prototypes

---

## PCB Specifications

### Official Specifications
- [GH60 PCB Specifications](docs/gh60_pcb_specifications.md) - Authoritative dimensions and tolerances
- [Compatible PCBs List](docs/compatible_pcbs.md) - Verified compatible 60% PCBs

### Key Dimensions (Quick Reference)
- PCB: 285mm × 94.6mm × 1.6mm
- Case Opening: 286mm × 95.6mm (0.5mm clearance per side)
- Mounting Holes: 6 positions (M2 screws, 2.0-2.2mm diameter)
- USB Cutout: 16mm wide, centered at 142.5mm from left edge

### Critical Clearances for Through-Hole PCBs
- **Below PCB:** 5.4mm minimum (through-hole components + solder joints)
- **Above PCB:** 12mm minimum (switches + keycaps + travel)
- **Around mounting holes:** 5mm radius clear zone

---

## GitHub Repositories
https://github.com/coseyfannitutti/discipline
https://github.com/coseyfannitutti/mysterium
https://github.com/coseyfannitutti/discipad
https://github.com/coseyfannitutti/romeo
https://github.com/peej/rosaline-keyboard
https://github.com/mohoyt/litl


https://keyboardsexpert.com/through-hole-keyboards-guide/

Gingham Keyboard Kit from Novelkeys
Lattice from Keyhive
Barleycorn from P3DStore

Discipline (65%) — GitHub: https://github.com/coseyfannitutti/discipline

  • Includes “BOM, Build Guide, and Flashing Information” in the repo. 
  • The build guide lists included components such as 68× 1N4148 diodes, resistors (10 k, 5.1 k, 1.5 k, 75 Ω), zener diodes, capacitors (22 pF, 0.1 µF, 4.7 µF), ATmega32A, USB-C parts, etc. 
Scribd

Mysterium (TKL) — GitHub: https://github.com/coseyfannitutti/mysterium
  • The repository includes a BOM, build guide, and flashing instructions. 

Plaid (4×12 ortholinear) — GitHub: https://github.com/hsgw/plaid
  • The README / docs include a “build guide and BOM.” 

Gingham (60%) — GitHub: https://github.github.com/yiancar/gingham_pcb
  • The repo includes design files; however, I did not immediately see a standalone BOM file in the root. 

Tartan (60%) — GitHub: https://github.com/hsgw/tartan
  • The project includes a build guide and BOM (“Build guide and bom is here”) per the README. 

Lumberjack (split 5×12 ortholinear) — GitHub: https://github.com/peej/lumberjack-keyboard

Nice — I pulled the repos and the BOM/build-guide pointers they include and made a deduped list of the through-hole components those projects use (common names + typical values where the projects list them). Sources: the GitHub repos I checked (Discipline, Mysterium, Plaid, Gingham, Tartan, Lumberjack). 
GitHub
+5
GitHub
+5
GitHub
+5

Below is the deduplicated component list (grouped by function). I list a short note when a project explicitly names the part/value in its BOM/readme.

Microcontroller / core

ATmega32A / ATmega32U4 / ATmega328P (through-hole DIP or socketed SOIC-to-DIP options commonly referenced). — used by Discipline / Mysterium / Plaid / Tartan references. 
GitHub
+2
GitHub
+2

Clock / crystals

16 MHz crystal (or resonator) + 2 × 22 pF caps (where listed). 
GitHub
+1

Power / USB

USB connector: USB-C or USB-Micro-B / 12-pin USB-C header (through-hole or panel mount) — many projects support USB-C or specify a through-hole USB connector. 
GitHub
+1

Zener diodes or discrete components used for VUSB circuits (projects that expose VUSB mention zeners / resistors). 
GitHub
+1

Switches & key hardware

Mechanical switches (Cherry MX style or equivalent) — quantity varies by layout (e.g., 60% ≈ 61, 65% ≈ 67, TKL ≈ 87–104, Plaid = 48 for 12×4). 
GitHub
+2
GitHub
+2

Switch plate / standoffs / screws / washers (hardware listed in build guides). 
GitHub
+1

Diodes

1N4148 (or similar small signal) — one per switch for diode-scanned matrices (commonly listed). 
GitHub
+1

Capacitors

0.1 µF (100 nF) ceramic decoupling capacitors (several).

4.7 µF electrolytic or tantalum (where projects list Vcc smoothing). 
GitHub
+1

Resistors

10 kΩ pull-up / pull-down resistors (e.g., for reset / I/O where used).

Misc resistor values shown in some BOMs (5.1 k, 1.5 k, 75 Ω called out in Discipline’s build notes). 
GitHub

Reset / Boot / Tactile

Tactile pushbuttons (RESET, BOOT, etc.). 
GitHub

LEDs / indicators

Through-hole LEDs (single or multiple for status/backlight if the design includes them) + current-limiting resistors. 
GitHub

Headers / connectors

2×N pin header strips for ISP / programming headers (e.g., 6-pin ISP), optional TRRS / JST for split boards, interconnect headers. 
GitHub
+1

IC sockets & support parts

DIP socket or IC socket for AVR (if using DIP MCU) or SOIC adapters as needed. 
GitHub

Misc discrete parts

Resettable polyfuse / fuse (optional, depending on design)

Crystal/resonator load caps (22 pF) — already listed above. 
GitHub

Which repos include BOMs / build guides (so you know where I pulled from)

Discipline — README points to BOM/Build Guide. 
GitHub

Mysterium — repo README / docs include build instructions and BOM pointers. 
GitHub

Plaid — README/build guide mentions BOM. 
GitHub

Gingham — repo exists (design files); explicit standalone BOM not obvious in root README. 
GitHub

Tartan — README references build guide/BOM. 
GitHub

Lumberjack — has a BOM.md in the repo (Bill of Materials). 
GitHub
+1


Name	Layout	Description	GitHub Link
Rosaline	40% staggered	Small 40% keyboard, through-hole only, USB-C	https://github.com/peej/rosaline-keyboard

Lagom	65%	65% keyboard, discrete MCU, THT components only	https://github.com/topics/through-hole

Litl	40%	40% keyboard, easy assembly, through-hole MCU	https://github.com/mohoyt/litl

KBIC65	65%	65% portable keyboard, ProMicro footprint, THT	https://github.com/b-karl/KBIC65

Plaid-Pad	4x4 macropad	Numpad/macropad, supports rotary encoders, THT	https://github.com/Keycapsss/Plaid-Pad

Neopad	4-switch macropad	Compact macropad with two rotary encoders, THT	https://github.com/rookiebwoy/neopad

F12	2x6 macropad	Atmega32A-based macropad, Vial firmware, THT	https://github.com/hadi-syafiq/F12

Dumbpad	4–6 switch macropad	Supports encoders, OLED options, THT	https://github.com/imchipwood/dumbpad

Soupara	20-key macropad	Budget-friendly tactile macropad, mostly THT	https://github.com/salian/soupara

Seagull Macropad	12–16 keys	MX/Choc compatible, encoder, optional battery, THT	https://github.com/klouderone/SeagullMacropad

Hackpad	Custom macropad	Users design macropad with Seeed XIAO RP2040, THT


### PCB Designs
- [ ] Add GH60 PCB repository link - https://github.com/komar007/gh60

---

## Technical Documentation

### Mechanical Keyboard Standards
- [ ] Add Cherry MX switch specifications
- [ ] Add keycap profile documentation (OEM, Cherry, SA, etc.)
- [ ] Add stabilizer specifications (Cherry/Costar)

### CNC Machining Resources
- [ ] Add wood machining feeds/speeds charts
- [ ] Add toolpath strategy guides
- [ ] Add double-sided machining tutorials

### CAD/CAM Tools
- [ ] Add Fusion 360 tutorials
- [ ] Add CadQuery documentation
- [ ] Add FreeCAD resources

---

## Component Specifications

### Through-Hole Components (Typical)
- Diodes: 1N4148 (DO-35 package, ~3mm height)
- Resistors: Through-hole axial (varies by design)
- Controller: Pro Micro, Elite-C, or similar (socketed)
- LED indicators: 3mm or 5mm through-hole LEDs

### Hardware
- **Screws:** M2 × 6mm (PCB to standoffs), M3 × 8mm (case assembly)
- **Standoffs:** 6mm diameter, 5-6mm height
- **Threaded Inserts:** M3 × 5.8mm OD × 4mm depth
- **Magnets:** (if magnetic assembly) specify size

---

## Manufacturing Resources

### 3D Printing (Prototyping)
- [ ] Add recommended print settings for case prototypes
- [ ] Add tolerance adjustment guidelines (printed vs CNC)
- [ ] Add support structure strategies

### CNC Milling
- [ ] Add wood species recommendations
- [ ] Add finishing techniques (sanding, oiling, lacquer)
- [ ] Add fixturing and workholding solutions

---

## Design Validation

### Testing Checklist
- [ ] PCB fit test (opening dimensions)
- [ ] Mounting hole alignment (±0.1mm tolerance)
- [ ] USB port accessibility
- [ ] Switch plate seating
- [ ] Keycap clearance (no interference)
- [ ] Screw boss alignment
- [ ] Acoustic properties

### Validation Scripts
- `examples/validate_design.py` - Standard height validation
- `examples/validate_design_lp.py` - Low-profile validation

---

## Community Resources

### Forums & Communities
- [ ] Add r/MechanicalKeyboards links
- [ ] Add GeekHack threads
- [ ] Add Deskthority resources

### Vendors & Suppliers
- [ ] Add PCB manufacturers
- [ ] Add hardware suppliers (screws, inserts)
- [ ] Add wood suppliers

---

## Notes & Observations

### Through-Hole Specific Considerations
- Component height varies: measure actual PCB with components installed
- Solder joints add 1-2mm below PCB surface
- Consider component placement when designing internal features
- USB connector may be through-hole (requires larger cutout)

### Design Iterations
- Document changes and lessons learned here
- Track tolerance adjustments between prototypes
- Note material-specific behaviors (wood movement, finish effects)

---

## TODO
- [ ] Gather PCB datasheets and schematics
- [ ] Collect reference photos of through-hole builds
- [ ] Document acoustic tuning experiments
- [ ] Add case assembly instructions
- [ ] Create bill of materials (BOM)

