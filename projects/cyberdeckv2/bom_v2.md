# Cyberdeck v2 BOM — Rev 8 Case + 7.84" Screen (Pico-less)

Bill of materials for the **Cyberdeck v2** build: unkyulee's Rev 8 case
(lid modified for the 7.84" panel) + the Pico-less Pi Zero 2W electronics.

Sources: the original project [`bom.md`](bom.md) (Rev 2.1 parts on
hand), the [upstream Rev 8 build.md](https://github.com/unkyulee/micro-journal/blob/main/micro-journal-rev-8/build.md)
hardware list, and this project's `design_v2.md` / `design.md`.

**Assumption:** all Rev 2.1 parts are on hand (screen, Pi, keyboard PCB,
switches, battery shield...). Newly purchased items are marked **BUY?** —
mostly Rev 8-specific case hardware.

---

## 1. Printed Parts — `stl/` (17 files, print all)

| # | Part | Qty | Notes |
|---|------|-----|-------|
| P1 | `panel_left.stl`, `panel_middle.stl`, `panel_right.stl` | 3 | **Modified** lid front frame — holds the 7.84" panel. ⚠ Re-export after bench-measuring the panel (`design_v2.md` §6) |
| P2 | `Display Enclosure Left/Middle/Right.stl` | 3 | Stock Rev 8 — lid back shell + hinge roll |
| P3 | `Display Wire Cap.stl` | 1 | Stock Rev 8 — hinge cable cover |
| P4 | `Enclosure Left/Middle/Right.stl` | 3 | Stock Rev 8 — keyboard base |
| P5 | `Enclosure Lid.stl` | 1 | Stock Rev 8 — battery door |
| P6 | `Hood Top/Bottom/Left/Right.stl` | 4 | Stock Rev 8 — rear electronics hood |
| P7 | `keyboard plate space.stl`, `keyboard plate arrow.stl` | 2 | Stock Rev 8 — switch plates (same as Rev 2.1) |
| — | Filament | ~1 kg | PLA+ ok; PETG/ABS recommended for hinge parts |

Stock `Display Back Cover.stl` and `Display Port.stl` are **not printed**
(5"-display hardware, replaced by the panel pocket).

## 2. Display (on hand from Rev 2.1)

| # | Part | Qty | Notes / Reference |
|---|------|-----|-------------------|
| D1 | Wisecoco 7.84" 1280×400 IPS bar panel + MIPI→HDMI driver board | 1 | [Amazon](https://www.amazon.com/wisecoco-Secondary-Stretched-Temperature-Monitoring/dp/B0BXL2Q53Y) / [AliExpress](https://www.aliexpress.com/item/1005004986951553.html) |
| D2 | **BUY?** Slim/ribbon HDMI cable, 20–30 cm, ≤ 6 mm bend stack | 1 | Ends per the driver board (typically mini-HDMI → the Pi's mini-HDMI). The stock 25 cm cable works only if it tolerates the hinge bend — a flat/ribbon FPV-style HDMI is safer through the Wire Cap channel |
| D3 | Thin foam tape (1–2 mm) | 1 roll | Panel shim in the frame pocket |

## 3. Compute & Power (on hand from Rev 2.1)

| # | Part | Qty | Notes |
|---|------|-----|-------|
| C1 | Raspberry Pi Zero 2W (+ 2×20 male header if headerless) | 1 | Scans the keyboard matrix directly ([header: Adafruit #2822](https://www.adafruit.com/product/2822)) |
| C2 | Micro SD card, ≥ 8 GB | 1 | micro-journal-linux + this project's `src/` overlay |
| C3 | 18650 battery shield w/ holder | 1 | [Amazon](https://www.amazon.com/diymore-Battery-Holder-Charging-Holders/dp/B0CBMQ8PZH) — mounts low in the rear bay for balance |
| C4 | 18650 Li-ion cells (flat-top) | 2–4 | ≥ 2 recommended |
| C5 | SPST snap-in rocker switch, 2-pin 19 mm | 1 | Main power — fits the Rev 8 hood opening ([AliExpress ref](https://it.aliexpress.com/item/1005008528747478.html)) |
| C6 | Micro USB 2-pin male pigtail | 1 | Shield → Pi power leg |

## 4. Keyboard (on hand from Rev 2.1)

| # | Part | Qty | Notes |
|---|------|-----|-------|
| K1 | 68-key keyboard PCB | 1 | [Elecrow](https://www.elecrow.com/micro-journal-diy-kit-68-keys-keyboard-pcb.html) — unmodified |
| K2 | MX-style switches | 71 | |
| K3 | Keycaps (65%-compatible set) | 1 set | |
| K4 | EC11 15 mm rotary encoders | 2 | [Amazon](https://www.amazon.com/Position-Degree-Rotary-Encoder-Button/dp/B0GRNSTXFC) |
| K5 | **BUY?** Costar stabilizer 6.25u | 1 | Spacebar — required by the Rev 8 plates (upstream Rev 8 BOM) |

## 5. Pi ↔ Keyboard Connector (the Pico-less mod — from bom.md §2)

| # | Part | Qty | Notes |
|---|------|-----|-------|
| W1 | 2×20 40-pin IDC ribbon cable, F–F, 10–20 cm | 1 | [Adafruit #1988](https://www.adafruit.com/product/1988) — primary plan (design.md §5) |
| W2 | 2.54 mm Dupont crimp kit (housings + female pins) | 1 kit | [Amazon CHENBO 620 pcs](https://www.amazon.com/dp/B077X8XV2J) — terminate 22 conductors at the PCB header |
| W3 | *(alt.)* 40-pin GPIO screw-terminal breakout | 1 | [Adafruit #2028 T-Cobbler Plus](https://www.adafruit.com/product/2028) — Option B instead of W2 |
| W4 | 30 AWG wire, assorted | 1 lot | Knob harnesses, power jumpers |
| W5 | Heat-shrink / wire labels | 1 lot | Label row/col/encoder groups before crimping |

## 6. Case Hardware (upstream Rev 8 list — **BUY?** the 70 mm screws)

| # | Part | Qty | Notes |
|---|------|-----|-------|
| H1 | M3 heat-set inserts, OD 4.5 × L 3 mm | 10+ | On hand from Rev 2.1 |
| H2 | M2 heat-set inserts, OD 3.2 × L 3 mm | 10+ | On hand from Rev 2.1 |
| H3 | DIN 912 M3 hex screws, 5 mm | 8+ | On hand |
| H4 | DIN 912 M3 hex screws, 10 mm | 4+ | On hand |
| H5 | **BUY?** DIN 912 M3 hex screws, **70 mm** | 4+ | Rev 8 span ties / hinge pins — Rev 2.1 kit had 50 mm, Rev 8 needs 70 mm |
| H6 | DIN 7046 M2 machine screws, 5 mm | 8+ | Frame → shell (on hand) |
| H7 | **BUY?** B-7000 glue | 1 tube | Zig-zag joint bonding ([AliExpress ref](https://www.aliexpress.com/item/1005005379063116.html)) |

## 7. Not Needed for v2 (from the Rev 2.1 kit)

| Part | Why |
|------|-----|
| Raspberry Pi Pico (RP2040) | Pico-less — Pi scans the matrix |
| Micro USB hub | Optional; only for the USB flash-backup workflow |
| Rubber O-ring OD18 (Rev 2.1 hinge friction) | Rev 8 hinge uses the screw-tension barrel instead |
| Rev 2.1 case prints / 45 mm side knobs | Replaced by the Rev 8 case; encoders keep their stock knobs per Rev 8 layout |
| ESP32 S3, reflective LCD, FPC adapter, LiPo charger (upstream Rev 8 BOM) | Rev 8's stock electronics — replaced by our Pi + Wisecoco set |

## 8. Tools (not consumed)

- Soldering iron (heat-set inserts + through-hole)
- TORX T10H / hex drivers (DIN 912 screws)
- Dupont crimper (SN-28B style), flush cutters, strippers
- Multimeter — verify PCB pinout **before final crimping**
- 3D printer (220×220 bed minimum) or print service

---

**Likely purchase list (everything else is on hand):** M3×70 screws (H5),
B-7000 (H7), Costar 6.25u stab (K5), possibly a slim HDMI cable (D2) and
the connector parts (W1/W2) if not already bought for the Rev 2.1 mod.