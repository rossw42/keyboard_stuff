# PCB Design Improvements

**Date:** October 20, 2025  
**Status:** Complete ✅

---

## Overview

The keyboard generator has been enhanced with comprehensive PCB design knowledge from industry-standard guides (ai03's PCB Design Guide and ebastler's ZMK Design Guide). These improvements ensure accurate, manufacturable through-hole PCB designs following best practices.

---

## What Changed

### 1. Pin Assignments (`thkg/layout/pins.py`)

**Before:**
- Simple pin lists without proper reservations
- Crystal pins (XTAL1/XTAL2) not reserved
- ISP pins (MISO/MOSI/SCK) not reserved
- Generic USB pin reservations

**After:**
- ✅ Crystal oscillator pins properly reserved (PB6/PB7)
- ✅ ISP programming pins reserved (PB3/PB4/PB5)
- ✅ USB pins correctly reserved (D+/D- on proper pins)
- ✅ Detailed pin capability metadata (PWM, ADC)
- ✅ Pin reservation explanations for documentation

**ATmega328P Reserved Pins:**
- D0, D1: UART (USB communication)
- D2, D3: INT0/INT1 (reserved for future use)
- B3, B4, B5: MOSI, MISO, SCK (ISP programming)
- B6, B7: XTAL1, XTAL2 (16MHz crystal)

**Available Pins:** 13 pins for matrix (after reservations)

---

### 2. Component Specifications (`thkg/config.py`)

**New Configuration Classes:**

#### `USBProtectionConfig`
Standard USB-C protection circuit components:
- ESD protection: USBLC6-2SC6 (SOT-23-6)
- Ferrite beads: 600Ω@100MHz (0805)
- Polyfuse: 500mA (1206)
- CC resistors: 5.1kΩ (0805)
- Decoupling caps: 100nF (0805)

#### `CrystalConfig`
16MHz crystal oscillator circuit:
- Frequency: 16MHz
- Load capacitors: 22pF (through-hole ceramic)
- Footprint: HC-49S

#### `DecouplingConfig`
MCU decoupling capacitors:
- Value: 100nF
- Quantity: 4 (one per VCC pin)
- Footprint: Through-hole ceramic disc

#### `DiodeConfig`
Matrix diodes:
- Part: 1N4148 (standard switching diode)
- Footprint: DO-35 through-hole
- Specs: 1V forward voltage, 200mA

#### `PCBLayoutRules`
Manufacturing design rules:
- Signal traces: 0.4mm (recommended)
- Power traces: 0.8mm (recommended)
- USB differential: 0.4mm (90Ω impedance)
- Clearance: 0.3mm (recommended)
- Vias: 0.6mm diameter, 0.3mm drill
- Component spacing rules

---

### 3. Circuit Templates (`thkg/pcb/circuits.py`)

**New Module:** Proven circuit patterns for keyboard PCBs

#### USB-C Protection Circuit
Complete protection circuit with:
- CC configuration resistors (5.1kΩ to GND)
- ESD protection IC (USBLC6-2SC6)
- Ferrite beads for noise filtering
- Polyfuse for overcurrent protection
- Decoupling capacitors
- Detailed connection map
- Placement notes

#### ATmega328P Support Circuit
Complete MCU support with:
- 16MHz crystal oscillator
- 22pF load capacitors
- 4× 100nF decoupling capacitors
- 10kΩ RESET pull-up resistor
- ISP programming header
- Connection map
- Layout guidelines

#### ATmega32A Support Circuit
Similar to ATmega328P with:
- USB D+/D- connections on PD2/PD3
- Optional USB D+ pull-up resistor
- Different pinout for DIP-40 package

#### Switch Matrix Template
Generates matrix circuits with:
- Configurable rows × columns
- COL2ROW or ROW2COL diode direction
- 1N4148 diodes for each switch
- Complete connection map
- Routing guidelines

---

### 4. Component Library (`thkg/pcb/components.py`)

**New Module:** Standardized components with real part numbers

#### Component Categories

**Resistors (Through-Hole):**
- 5.1kΩ: Yageo CFR-25JB-52-5K1 (USB-C CC)
- 10kΩ: Yageo CFR-25JB-52-10K (RESET pull-up)
- 1.5kΩ: Yageo CFR-25JB-52-1K5 (USB D+ pull-up)

**Capacitors (Through-Hole):**
- 100nF: Kemet C315C104M5U5TA (decoupling)
- 22pF: Kemet C315C220J2G5TA (crystal load)

**Diodes:**
- 1N4148: Vishay 1N4148-TAP (matrix diodes)

**ICs (SMD):**
- USBLC6-2SC6: STMicroelectronics (ESD protection)

**MCUs (Through-Hole DIP):**
- ATmega328P-PU: Microchip ATMEGA328P-PU (DIP-28)
- ATmega32A-PU: Microchip ATMEGA32A-PU (DIP-40)

**Crystals:**
- 16MHz: ECS ECS-160-20-4X (HC-49S)

**Ferrite Beads (SMD):**
- 600Ω@100MHz: Murata BLM21PG601SN1D (0805)

**Polyfuses (SMD):**
- 500mA: Bourns MF-MSMF050-2 (1206)

**Connectors:**
- USB-C: HRO TYPE-C-31-M-12 (through-hole)
- ISP Header: 2×3 pin header, 2.54mm pitch

**Switches:**
- Cherry MX compatible (PCB mount, 5-pin)

#### Features
- Complete part numbers for ordering
- Manufacturer information
- Footprint references (KiCad compatible)
- Vendor SKUs (Mouser, Digikey, LCSC)
- Datasheets links
- BOM generation with quantities

---

### 5. Enhanced PCB Generator (`thkg/pcb/generator.py`)

**New Capabilities:**

#### Circuit Integration
- Automatically selects circuit templates based on config
- Combines USB protection + MCU support + switch matrix
- Generates complete circuit with all connections

#### BOM Generation
- Extracts components from all circuits
- Consolidates quantities (e.g., 4× 100nF caps)
- Includes real part numbers and vendors
- Ready for ordering

#### Dimension Calculation
- Calculates PCB size from switch layout
- Adds proper border (5mm default)
- Falls back to GH60 standard if needed

#### Design Validation
- Checks matrix size vs available pins
- Validates USB type compatibility
- Warns about unusual dimensions
- Prevents common mistakes

#### Layout Rules Export
- Provides trace width specifications
- Clearance requirements
- Via sizing
- Component spacing rules

---

## Test Results

All tests passing ✅

```
============================================================
✓ ALL TESTS PASSED!
============================================================

The keyboard generator now includes:
  ✓ Accurate pin assignments with proper reservations
  ✓ Industry-standard circuit templates
  ✓ Component library with real part numbers
  ✓ Automatic BOM generation
  ✓ PCB layout rules from best practices

Ready for Phase 2 KiCad integration!
```

### Test Coverage

1. **Pin Assignments**
   - ATmega328P: 13 available pins (9 reserved)
   - ATmega32A: 23 available pins (9 reserved)
   - 3×3 matrix assignment: Success

2. **Circuit Templates**
   - USB-C protection: 9 components, 18 connections
   - ATmega328P support: 10 components, 22 connections
   - 3×3 switch matrix: 18 components, 27 connections

3. **Component Library**
   - All components have real part numbers
   - BOM generation consolidates quantities
   - Vendor information included

4. **PCB Generator**
   - Generates 3 circuits for 3×3 macropad
   - BOM: 12 unique parts
   - Layout rules: All specified
   - Validation: No issues

---

## Usage Example

```python
from thkg.config import Configuration, MCUType, USBType, Matrix
from thkg.pcb.generator import PCBGenerator

# Create configuration
config = Configuration(
    name="MyMacropad",
    mcu_type=MCUType.ATMEGA328P,
    usb_type=USBType.USB_C_THT,
)

# Set up matrix
config.matrix = Matrix(rows=3, cols=3, diode_direction="COL2ROW")

# Generate PCB
generator = PCBGenerator()
result = generator.generate_pcb(config, [])

# Access circuits
circuits = result['circuits']
# - usb_protection: USB-C Protection circuit
# - mcu_support: ATmega328P Support circuit
# - switch_matrix: 3×3 Switch Matrix

# Access BOM
bom = result['bom']
# List of components with quantities and part numbers

# Access layout rules
rules = result['layout_rules']
# Trace widths, clearances, via sizing

# Validate design
messages = generator.get_design_validation(config)
```

---

## Benefits

### For Users
- ✅ Accurate PCB designs that follow industry standards
- ✅ Complete BOM with real part numbers for ordering
- ✅ No pin conflicts (crystal, ISP, USB properly reserved)
- ✅ Manufacturing-ready specifications

### For Phase 2 Implementation
- ✅ Circuit templates ready for KiCad integration
- ✅ Component library with footprint references
- ✅ Layout rules for auto-routing
- ✅ Validation to prevent common mistakes

### For Quality
- ✅ Based on proven designs (ai03's guide)
- ✅ Industry-standard component values
- ✅ Proper USB protection (ESD, overcurrent)
- ✅ Correct crystal oscillator circuit
- ✅ Adequate decoupling capacitors

---

## Design Principles Applied

### From ai03's PCB Design Guide

1. **USB Protection**
   - ESD protection IC (USBLC6-2SC6)
   - Ferrite beads for noise filtering
   - Polyfuse for overcurrent protection
   - CC resistors for USB-C configuration

2. **MCU Support**
   - Crystal within 10mm of MCU
   - 22pF load capacitors for 16MHz crystal
   - 100nF decoupling caps next to VCC pins
   - 10kΩ RESET pull-up resistor
   - ISP header for programming

3. **PCB Layout**
   - 2-layer design (standard)
   - Signal traces: 0.4mm
   - Power traces: 0.8mm
   - USB differential: 90Ω impedance
   - Clearance: 0.3mm minimum

4. **Matrix Design**
   - 1N4148 diodes (standard)
   - COL2ROW or ROW2COL configurable
   - Proper diode orientation

---

## Files Modified

### Updated Files
1. `thkg/layout/pins.py` - Fixed pin reservations
2. `thkg/config.py` - Added component specifications
3. `thkg/pcb/generator.py` - Enhanced with templates and BOM

### New Files
1. `thkg/pcb/circuits.py` - Circuit templates
2. `thkg/pcb/components.py` - Component library
3. `test_pcb_improvements.py` - Test suite
4. `PCB_IMPROVEMENTS.md` - This document

---

## Next Steps for Phase 2

With these improvements in place, Phase 2 (KiCad integration) can now:

1. **Use Circuit Templates**
   - Import templates into KiCad schematic
   - Place components according to templates
   - Connect nets as specified

2. **Use Component Library**
   - Map components to KiCad footprints
   - Generate accurate BOM
   - Include vendor information

3. **Apply Layout Rules**
   - Configure DRC with our specifications
   - Set trace widths automatically
   - Apply clearance rules

4. **Validate Designs**
   - Check pin assignments before generation
   - Verify component compatibility
   - Warn about potential issues

---

## Conclusion

The keyboard generator now has comprehensive PCB design knowledge integrated. All improvements are based on industry-standard practices from ai03's PCB Design Guide and include:

- ✅ Accurate pin assignments with proper reservations
- ✅ Proven circuit templates (USB, MCU, matrix)
- ✅ Component library with real part numbers
- ✅ Automatic BOM generation
- ✅ PCB layout rules from best practices
- ✅ Design validation

**The generator is now ready for Phase 2 KiCad integration with a solid foundation for producing accurate, manufacturable through-hole keyboard PCBs.**

---

**Last Updated:** October 20, 2025  
**Status:** Complete and tested ✅
