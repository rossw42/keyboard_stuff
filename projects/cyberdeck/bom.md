# Cyberdeck BOM — Micro Journal Rev 2.1 (Pico-less Mod)

Bill of materials for this build. Derived from the [stock Rev 2.1 BOM](https://github.com/unkyulee/micro-journal/blob/main/micro-journal-rev-2.1/build.md), adjusted for the Pico-less modification per [`design.md`](./design.md).

**Assumption:** all stock Rev 2.1 parts are already on hand. Only §2 (connector parts) may require purchase.

---

## 1. Retained Stock Parts (on hand)

| # | Part | Qty | Notes / Reference |
|---|------|-----|-------------------|
| 1 | Wisecoco 7.84" 1280x400 LCD Display | 1 | [Amazon](https://www.amazon.com/wisecoco-Secondary-Stretched-Temperature-Monitoring/dp/B0BXL2Q53Y) / [AliExpress](https://www.aliexpress.com/item/1005004986951553.html) |
| 2 | Raspberry Pi Zero 2W | 1 | Now scans the keyboard matrix directly |
| 3 | 68-key Keyboard PCB | 1 | [Elecrow](https://www.elecrow.com/micro-journal-diy-kit-68-keys-keyboard-pcb.html) — used unmodified |
| 4 | MX-style key switches | 71 | 69 board positions + hot-swap in stock kit (choose to taste) |
| 5 | Keycaps (68-key / 65% compatible set) | 1 set | |
| 6 | EC11 15mm half-handle rotary encoder | 2 | [Amazon](https://www.amazon.com/Position-Degree-Rotary-Encoder-Button/dp/B0GRNSTXFC) |
| 7 | HDMI cable, 25 cm | 1 | Pi → display |
| 8 | Micro SD card, min 8 GB | 1 | micro-journal-linux image |
| 9 | 18650 battery shield w/ 4-slot holder | 1 | [Amazon](https://www.amazon.com/diymore-Battery-Holder-Charging-Holders/dp/B0CBMQ8PZH) |
| 10 | 18650 Li-ion batteries (flat-top) | 2–4 | Optional; ≥2 recommended for stability |
| 11 | Micro USB hub with power input | 1 | **Optional now** — keep only if the USB flash-drive backup workflow is wanted (design.md §2) |
| 12 | Micro USB 2-pin male pigtail cable | 1 | Power leg to the Pi (was 2 in stock — Pico's leg removed) |
| 13 | USB 2-pin male cable | 1 | Power wiring |
| 14 | SPST snap-in rocker switch, 2-pin 19mm | 1 | Main power switch |
| 15 | Rubber O-ring OD18 / ID13.2 / CS2.4 mm | 1 | Display hinge friction |
| 16 | DIN 912 M3 hex screws — 5 mm | 4+ | |
| 17 | DIN 912 M3 hex screws — 10 mm | 4+ | |
| 18 | DIN 912 M3 hex screws — 50 mm | 4+ | |
| 19 | DIN 7046 M2 Phillips screws — 5 mm | 8+ | |
| 20 | M3 heated inserts (OD 4.5, L 3 mm) | 10+ | |
| 21 | M2 heated inserts (OD 3.2, L 3 mm) | 10+ | |
| 22 | TORX T10H screwdriver | 1 | Tool |
| 23 | 30 AWG wire, assorted colors | 1 lot | Knob harnesses + any short jumpers |
| 24 | PLA+ filament | ~1 kg | 3D-printed enclosure (stock case, ~30 h print) |

## 2. Added Parts (the mod — may need purchase)

| # | Part | Qty | Purpose | Product link | Notes |
|---|------|-----|---------|--------------|-------|
| A1 | 2x20 (40-pin) male pin header, 2.54 mm | 1 | Pi Zero 2W GPIO header | [Adafruit #2822 — Break-away 2x20 Dual Male Header](https://www.adafruit.com/product/2822) | Skip if Pi already has a header (e.g., Zero 2 WH). Extra-tall stacking variant: [Adafruit #2223](https://www.adafruit.com/product/2223) |
| A2 | 2x20 (40-pin) IDC ribbon cable, female–female, 10–20 cm | 1 | Removable Pi ↔ keyboard link | [Adafruit #1988 — GPIO Ribbon Cable for Raspberry Pi (40 pins)](https://www.adafruit.com/product/1988) | Standard Raspberry Pi GPIO ribbon; primary connector plan (design.md §5). Also widely available on Amazon/AliExpress as "40 pin GPIO ribbon cable" |
| A3 | 2.54 mm Dupont crimp connector kit (housings 1x1–1x9 + female crimp pins) | 1 kit | Terminate ribbon conductors onto the keyboard PCB's 32-pin header, grouped by function | [Amazon — CHENBO 620pcs 2.54mm Dupont Connector Kit](https://www.amazon.com/dp/B077X8XV2J) | Option A (primary). Any 2.54mm Dupont kit with 1x8/1x9 housings works |
| A4 | *(alternative)* 40-pin GPIO screw-terminal breakout ("T-cobbler" style) | 1 | Screw-terminal serviceability at the keyboard end | [Adafruit #2028 — Assembled Pi T-Cobbler Plus GPIO Breakout](https://www.adafruit.com/product/2028) | Option B — instead of A3, at ~15–20 mm height. Screw-terminal HAT variants: search "Raspberry Pi GPIO screw terminal HAT" on Amazon/AliExpress |
| A5 | Heat-shrink tubing / wire labels | 1 lot | Label row/col/encoder groups | Generic — search "heat shrink tubing kit 2:1 assorted" on Amazon/AliExpress | Strongly recommended before crimping |

## 3. Removed Stock Parts (no longer needed)

| Part | Stock role | Why removed |
|------|-----------|-------------|
| Raspberry Pi Pico (RP2040) | Matrix scan + QMK/Vial firmware + USB HID | Pi Zero 2W scans the matrix directly |
| 1x Micro USB 2-pin pigtail (Pico's leg) | Pico ↔ hub connection | No Pico |
| Micro USB hub *(conditionally)* | Combine power + Pico USB + spare port | Only justified now by the spare USB port; see item 11 above |

## 4. Tools Required (not consumed)

- Soldering iron (through-hole level) — Pi header, knob wires
- Dupont crimping tool (e.g., SN-28B / SN-025) — for Option A terminations
- Multimeter — verify PCB pinout continuity **before final crimping** (design.md §8)
- Flush cutters / wire strippers
- 3D printer (or print service) for the enclosure

---

**Reminder:** verify the keyboard PCB's physical pinout with `matrix_test.py` and a multimeter before final crimping — the upstream build.md wiring table needs on-bench confirmation.