# PCB Design Checklist

Quick reference checklist for keyboard PCB design. Use this to ensure you haven't missed critical steps.

---

## Pre-Design Phase

### Requirements
- [ ] Determine keyboard layout (60%, 65%, TKL, etc.)
- [ ] Choose MCU (ATmega328P, ATmega32A, Pro Micro, nRF52840)
- [ ] Decide wired vs wireless
- [ ] Plan features (LEDs, encoders, OLED, etc.)
- [ ] Check pin count requirements

### Tools & Libraries
- [ ] KiCad installed (7.0+ recommended)
- [ ] marbastlib library installed
- [ ] Git repository created
- [ ] .gitignore configured for KiCad

---

## Schematic Design

### USB Circuit
- [ ] USB connector added (USB-C recommended)
- [ ] CC resistors: 2× 5.1kΩ (USB-C only)
- [ ] ESD protection: USBLC6-2SC6 or similar
- [ ] Polyfuse: 500mA
- [ ] Ferrite beads: 2× 600Ω@100MHz
- [ ] Decoupling caps: 2× 100nF

### MCU Circuit
- [ ] MCU symbol added
- [ ] Decoupling caps on all VCC pins (100nF each)
- [ ] RESET pull-up: 10kΩ
- [ ] Crystal: 16MHz (for USB timing)
- [ ] Crystal load caps: 2× 22pF
- [ ] ISP/SWD programming header
- [ ] All pins assigned or marked NC

### Power Circuit
- [ ] Power input from USB
- [ ] Voltage regulator if needed (3.3V for nRF52840)
- [ ] Input cap: 10µF
- [ ] Output cap: 10µF
- [ ] Power LED (optional)

### Wireless Only
- [ ] Battery management IC (TP4056 or BQ24075)
- [ ] Charge current programming resistor
- [ ] Battery connector (JST-PH 2.0)
- [ ] Power switch (optional)
- [ ] Voltage divider for battery sensing
- [ ] Charging indicator LED

### Switch Matrix
- [ ] All switches added
- [ ] One diode per switch (1N4148)
- [ ] Diode orientation correct (COL2ROW or ROW2COL)
- [ ] Matrix dimensions optimized (minimize rows+cols)
- [ ] All rows connected to MCU pins
- [ ] All columns connected to MCU pins
- [ ] No pin conflicts

### Optional Features
- [ ] Rotary encoder circuit
- [ ] OLED display circuit
- [ ] WS2812 LED circuit
- [ ] LED power switch (wireless)
- [ ] Status LEDs
- [ ] Speaker/buzzer

### Schematic Review
- [ ] Run ERC (Electrical Rules Check)
- [ ] All pins connected
- [ ] No floating inputs
- [ ] Power symbols correct
- [ ] Net names clear and consistent
- [ ] Component values verified
- [ ] Footprints assigned to all components

---

## PCB Layout

### Setup
- [ ] Board outline defined
- [ ] Mounting holes placed (M2, 2mm diameter)
- [ ] PCB dimensions match spec (e.g., 285×94.6mm for 60%)
- [ ] Corner radius set (2mm typical)
- [ ] Design rules configured
  - [ ] Trace width: 0.25mm min, 0.4mm recommended
  - [ ] Clearance: 0.2mm min, 0.3mm recommended
  - [ ] Via size: 0.8mm drill, 1.4mm pad

### Component Placement
- [ ] USB connector at board edge
- [ ] MCU centrally located
- [ ] Crystal within 10mm of MCU
- [ ] Decoupling caps next to MCU pins
- [ ] Switches in precise grid (19.05mm spacing)
- [ ] Diodes near switches
- [ ] Programming header accessible
- [ ] LEDs positioned (if used)
- [ ] Battery connector accessible (wireless)
- [ ] All components on top layer
- [ ] Tall components away from switches
- [ ] Case clearance considered (12mm+ above PCB)

### Routing - Critical Signals
- [ ] USB D+/D- differential pair
  - [ ] Equal length (±5mm)
  - [ ] 90Ω impedance
  - [ ] No vias if possible
  - [ ] Away from noisy signals
- [ ] Crystal traces
  - [ ] Short and direct
  - [ ] No vias
  - [ ] Ground plane underneath
  - [ ] Guard ring (optional)

### Routing - Matrix
- [ ] Rows routed (typically horizontal)
- [ ] Columns routed (typically vertical)
- [ ] Trace width adequate (0.4mm+)
- [ ] No acute angles
- [ ] Vias minimized

### Routing - Power
- [ ] VCC traces wide (0.8mm+)
- [ ] GND plane on bottom layer
- [ ] GND vias distributed (every 10-20mm)
- [ ] Star topology from regulator
- [ ] Decoupling caps close to ICs

### Wireless Specific
- [ ] Antenna at board edge
- [ ] No ground plane under antenna
- [ ] No traces under antenna
- [ ] 5mm clearance from metal
- [ ] Module away from USB (noise)

### Silkscreen
- [ ] Component references visible
- [ ] Polarity marks on diodes
- [ ] Pin 1 marks on ICs
- [ ] USB connector labeled
- [ ] Programming header labeled
- [ ] Version number
- [ ] Designer name/logo (optional)
- [ ] No silkscreen on pads

### Design Rule Check
- [ ] Run DRC
- [ ] All errors fixed
- [ ] Warnings reviewed
- [ ] Clearances verified
- [ ] Trace widths checked
- [ ] Via sizes correct

### Final Review
- [ ] Visual inspection of all traces
- [ ] Component footprints verified
- [ ] Pin assignments match schematic
- [ ] Mounting holes correct size
- [ ] Board dimensions correct
- [ ] USB connector accessible
- [ ] Programming header accessible
- [ ] All layers reviewed

---

## Pre-Manufacturing

### Gerber Generation
- [ ] Gerbers exported
  - [ ] F.Cu (top copper)
  - [ ] B.Cu (bottom copper)
  - [ ] F.Mask (top solder mask)
  - [ ] B.Mask (bottom solder mask)
  - [ ] F.Silkscreen
  - [ ] B.Silkscreen
  - [ ] Edge.Cuts
  - [ ] PTH drill file
  - [ ] NPTH drill file (if used)
- [ ] Gerbers reviewed in viewer
- [ ] Drill file checked

### Documentation
- [ ] Schematic PDF exported
- [ ] PCB layout PDF exported
- [ ] BOM generated
- [ ] Assembly drawing created
- [ ] README updated
- [ ] License file included

### Version Control
- [ ] All files committed to git
- [ ] Tagged with version number
- [ ] Pushed to remote repository

---

## Post-Manufacturing

### Visual Inspection
- [ ] No shorts between traces
- [ ] No broken traces
- [ ] Solder mask correct
- [ ] Silkscreen readable
- [ ] Mounting holes correct size
- [ ] Board dimensions correct

### Component Assembly
- [ ] Components oriented correctly
- [ ] Polarity checked (diodes, ICs, caps)
- [ ] Solder joints inspected
- [ ] No bridges between pins
- [ ] No cold solder joints

### Electrical Testing
- [ ] Continuity test on power rails
- [ ] No shorts between VCC and GND
- [ ] USB connector pinout verified
- [ ] Crystal oscillating (oscilloscope)
- [ ] Voltage at MCU correct (5V or 3.3V)

### Firmware Testing
- [ ] Bootloader flashed (if needed)
- [ ] Test firmware uploaded
- [ ] USB enumeration successful
- [ ] All keys register
- [ ] No ghosting
- [ ] LEDs work (if used)

### Wireless Testing (if applicable)
- [ ] Battery charges correctly
- [ ] Charging LED indicates status
- [ ] Battery voltage sensing works
- [ ] Bluetooth pairing successful
- [ ] All keys work wirelessly
- [ ] Sleep/wake functions
- [ ] Battery life acceptable

---

## Common Mistakes to Avoid

### Schematic
- ❌ Forgetting CC resistors on USB-C
- ❌ Wrong crystal load capacitor values
- ❌ Missing decoupling capacitors
- ❌ Diodes in wrong orientation
- ❌ Pin assignment conflicts

### Layout
- ❌ USB traces not differential pair
- ❌ Crystal traces too long
- ❌ Ground plane splits
- ❌ Insufficient clearance
- ❌ Components under switches

### Manufacturing
- ❌ Wrong Gerber export settings
- ❌ Missing drill files
- ❌ Incorrect board dimensions
- ❌ Silkscreen on pads

### Assembly
- ❌ Reversed diodes
- ❌ Reversed ICs
- ❌ Wrong component values
- ❌ Solder bridges

---

## Resources

- **Full Guide:** [PCB_DESIGN_GUIDE.md](PCB_DESIGN_GUIDE.md)
- **Wireless Guide:** [WIRELESS_PCB_DESIGN.md](WIRELESS_PCB_DESIGN.md)
- **ai03 Guide:** https://wiki.ai03.com/books/pcb-design
- **ZMK Guide:** https://github.com/ebastler/zmk-designguide

---

**Print this checklist and check off items as you complete them!**

**Last Updated:** October 20, 2025
