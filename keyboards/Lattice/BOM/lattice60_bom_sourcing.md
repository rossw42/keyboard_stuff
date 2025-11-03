# Lattice60 Bill of Materials (BOM) - Sourcing Tracker

**Project:** Lattice60 Custom Keyboard
**Guide Version:** v01
**Last Updated:** 2025-10-20

---

## Electronic Components

| Component | Qty | MPN | Manufacturer | Mouser SKU | Unit Price | Total | Purchased | Est. Arrival |
|-----------|-----|-----|--------------|------------|-----------|-------|-----------|--------------|
| ATmega328p-pu | 1 | ATMEGA328P-PU | Microchip | 556-ATMEGA328P-PU | $2.89 | $2.89 | ☐ | |
| Mini USB Type B socket | 1 | 1734753-1 | TE Connectivity | Avnet 1734753-1 | $0.99 | $0.99 | ☐ | |
| RED LED 3mm | 1 | LTL-4222 | Lite-On | 859-LTL-4222 | $0.19 | $0.19 | ☐ | |
| GREEN LED 3mm | 1 | WP7113GT | Kingbright | 604-WP7113GT | $0.30 | $0.30 | ☐ | |
| 1.5K ohm Resistor 1/4W | 1 | CFR-25JR-52-1K5 | Yageo | 49AK5068 | $0.01 | $0.01 | ☐ | |
| 10K ohm Resistor 1/4W | 1 | CFR-25JR-52-10K | Yageo | 603-CFR-25JR-5210K | $0.10 | $0.10 | ☐ | |
| 1K ohm Resistor 1/4W | 2 | CFR-25JR-52-1K | Yageo | 603-CFR-25JR-521K | $0.10 | $0.20 | ☐ | |
| 68 ohm Resistor 1/4W | 2 | CFR-25JR-52-68R | Yageo | 603-CFR-25JR-52-68R | $0.10 | $0.20 | ☐ | |
| 100mA Resettable fuse | 1 | RXEF010S | Littelfuse | 650-RXEF010S | $0.34 | $0.34 | ☐ | |
| 28pin DIP socket (narrow) | 1 | 1-2199299-2 | TE Connectivity | 571-1-2199299-2 | $0.58 | $0.58 | ☐ | |
| 12MHz crystal HC-49S | 1 | J49SMH-A-G-G-K-12M0 | Jauch | 1908-J49SMH-A-G-G-K-12M0CT-ND | $0.21 | $0.21 | ☐ | |
| 3.6V Zener Diode | 2 | TZX3V6A-TR | Vishay | 78-TZX3V6A | $0.10 | $0.20 | ☐ | |
| 0.1uF Capacitor | 1 | RDER71H104K0M1H03A | Murata | 81-RDER71H104K0M1H3A | $0.46 | $0.46 | ☐ | |
| 22pF Capacitor | 2 | RCE5C2A220J0A2H03B | Murata | 81-RCE5C2A220J0A2H3B | $0.45 | $0.90 | ☐ | |
| 6x6x5mm Push Button Switch | 2 | MJTP1230A | APEM | 642-MJTP1230A | $0.33 | $0.66 | ☐ | |
| 4.7uF Capacitor 16V | 1 | ESK475M016AC3AA | Kemet | 80-ESK475M016AC3AA | $0.19 | $0.19 | ☐ | |
| 1N4148 switching diodes | 66 | 1N4148TR | onsemi | 512-1N4148TR | $0.041 | $2.71 | ☐ | |
| 2.54mm Header 2x3PIN (ISP) | 1 | 68602-406HLF | Amphenol | 649-68602-406HLF | $0.23 | $0.23 | ☐ | |

**Electronic Components Total:** $9.58  
**All components priced:** 18 of 18 components ✅

---

## Component Compatibility Notes

**✓ Components Shared with DISCIPLINE (Exact Match):**
- 3.6V Zener Diodes (same part)
- 22pF Capacitors (same part)
- 0.1uF Capacitor (same part, different qty: Lattice60=1x, DISCIPLINE=2x)
- 1N4148 Diodes (same part, different qty: Lattice60=63x, DISCIPLINE=69x)
- RED LED 3mm (same part)
- 4.7uF Capacitor (same part)
- 2x3 ISP Header (likely same part)

**⚠️ Components Different from DISCIPLINE:**
- **ATmega328p-pu**: Different MCU (DISCIPLINE uses ATmega32A-PU)
- **Mini USB Type B socket**: Different connector (DISCIPLINE uses USB Type-C)
- **12MHz crystal**: Different frequency (DISCIPLINE uses 16MHz)
- **100mA fuse**: Different rating (DISCIPLINE uses 500mA)
- **28-pin DIP socket**: Different size (DISCIPLINE uses 40-pin)
- **Resistors**: Different wattages (Lattice60=1/4W, DISCIPLINE=1/6W) and some different values
- **GREEN LED**: Not present in DISCIPLINE BOM
- **1K ohm resistors**: Not present in DISCIPLINE BOM

## PCBs

| Component | Qty | Purchased | URL/Description | Est. Arrival |
|-----------|-----|-----------|-----------------|--------------|
| Lattice60 top PCB | 1 | ☐ | | |
| Lattice60 backplate PCB | 1 | ☐ | (Optional if using case) | |

## Switches & Stabilizers

| Component | Qty | Purchased | URL/Description | Est. Arrival |
|-----------|-----|-----------|-----------------|--------------|
| Cherry MX or Alps compatible switches | 61 | ☐ | PCB-mount preferred (split spacebar layout) | |
| Durock V2 2u Stabilizers | 5 | Durock V2 | Durock | KBDfans | $2.50 | $12.50 | ☐ | |
| 2u Stabilizer (Backspace) | 1 | ☐ | Optional - for non-split backspace | |
| 2u Stabilizer (Right Shift) | 1 | ☐ | Optional - ANSI Right Shift | |

**Stabilizer Options & Pricing:**

| Stabilizer Type | Qty Needed | Supplier | Price Each | Total | Notes |
|-----------------|------------|----------|------------|-------|-------|
| **Cherry Screw-in 2u** | 5 | KBDfans | $2.00 | $10.00 | Gold-plated, PCB mount |
| **Durock V2 Screw-in 2u** | 5 | KBDfans | $2.50 | $12.50 | Smoother, less rattle |
| **Gateron Screw-in 2u** | 5 | AliExpress | $1.50 | $7.50 | Budget option |
| **GMK Screw-in 2u** | 5 | NovelKeys | $3.00 | $15.00 | Premium option |

## Hardware & Mounting

| Component | Qty | Purchased | URL/Description | Est. Arrival |
|-----------|-----|-----------|-----------------|--------------|
| 4mm M2 spacers | 13 | ☐ | | |
| 3mm M2 screws | 26 | ☐ | (22 if using standoffs) | |
| 10mm M2 standoffs | 4 | ☐ | Optional - for acrylic cover | |
| 6mm M2 screws | 4 | ☐ | Optional - for acrylic cover | |
| M4 Aluminum keyboard feet | 2 | ☐ | Optional | |
| 8x3mm Silicone rubber feet | 2 | ☐ | Optional | |

## Keycaps (Not Included)

| Component | Qty | Purchased | URL/Description | Est. Arrival |
|-----------|-----|-----------|-----------------|--------------|
| Keycap set | 1 | ☐ | Compatible with your layout | |

---

## Quick Order Links

**Components with Confirmed Pricing:**
- [ATmega328P-PU (556-ATMEGA328P-PU)](https://www.mouser.com/ProductDetail/556-ATMEGA328P-PU) - $2.89
- [6x6x5mm Pushbuttons (642-MJTP1230A)](https://www.mouser.com/ProductDetail/642-MJTP1230A) - $0.33 ea (need 2)
- [3.6V Zener Diodes (78-TZX3V6A)](https://www.mouser.com/ProductDetail/78-TZX3V6A) - $0.10 ea (need 2)
- [22pF Capacitors (81-RCE5C2A220J0A2H3B)](https://www.mouser.com/ProductDetail/81-RCE5C2A220J0A2H3B) - $0.45 ea (need 2)
- [0.1uF Capacitor (81-RDER71H104K0M1H3A)](https://www.mouser.com/ProductDetail/81-RDER71H104K0M1H3A) - $0.46
- [1N4148 Diodes (512-1N4148TR)](https://www.mouser.com/ProductDetail/512-1N4148TR) - $0.041 ea (need 63)
- [3mm Red LED (859-LTL-4222)](https://www.mouser.com/ProductDetail/859-LTL-4222) - $0.19

**Complete Build Cost Breakdown:**
- Electronic Components: $9.58
- Durock V2 Stabilizers (5x 2u): $12.50
- **Total Cost:** $22.08

**Components with MPNs (Need to upload CSV to Octopart for pricing):**
- Mini USB Type B: 1734753-1 (TE Connectivity)
- Green LED: WP7113GT (Kingbright)
- 1.5K Resistor: CFR-25JR-52-1K5 (Yageo)
- 10K Resistor: CFR-25JR-52-10K (Yageo)  
- 1K Resistor: CFR-25JR-52-1K (Yageo, 2x)
- 68Ω Resistor: CFR-25JR-52-68R (Yageo, 2x)
- 28-pin DIP socket: 1-2199299-3 (TE Connectivity)
- 4.7uF Capacitor: ESK475M016AC3AA (Kemet)
- 2x3 Header: 68602-406HLF (Amphenol)

**Next Steps:**
Upload `lattice60_octopart_corrected.csv` to Octopart to get pricing for the remaining 9 components, then share the completed CSV to update this markdown file.

---

## Notes

- **Layout Configuration:** Decide on your layout before ordering stabilizers
- **Switch Type:** Ensure switches have PCB-mount bases for best stability
- **Stabilizers:** Count depends on chosen layout (split spacebar, split backspace, etc.)
- **Optional Components:** Items marked with * in original BOM are optional

## Layout Options to Consider

- [x] Split Spacebar (requires 2x 2u stabilizers + 3 extra diodes) - SELECTED
- [ ] Split Backspace (no 2u stabilizer needed)
- [ ] Split Right Shift (no 2u stabilizer needed)
- [ ] Acrylic Top Cover (requires 10mm standoffs + 6mm screws)

## Resources

- **Bootloader:** https://github.com/emdarcher/USBaspLoader/tree/lattice60
- **QMK Firmware:** https://github.com/qmk/qmk_firmware/tree/master/keyboards/lattice60

---

## Progress Tracking

- [ ] All electronic components ordered
- [ ] PCBs ordered
- [ ] Switches & stabilizers ordered
- [ ] Hardware ordered
- [ ] All components received
- [ ] Assembly started
- [ ] Assembly completed
- [ ] Firmware flashed
- [ ] Build tested and working
