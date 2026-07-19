# PCB Auto-Routing Workflow — Orchestrator Step 1
## Project: biaxial_choc (Ergogen v4.1.0 output)

**Target file:** `ergogen/out_choc/ergogen/pcbs/biaxial_choc.kicad_pcb`
**CAD:** KiCad (file format `20240108` / KiCad 8)
**Stackup:** 2-layer (F.Cu / B.Cu), 1.6 mm FR-4, 1 oz copper assumed

---

## 1. Board Inventory (from file analysis)

| Item | Qty | Footprint | Layer |
|---|---|---|---|
| Key switches | 42 | `ceoloide:switch_choc_v1_v2` | B.Cu (reversible-style placement) |
| Matrix diodes | 42 | `ceoloide:diode_tht_sod123` | THT (both layers) |
| Controller | 1 | `ceoloide:mcu_nice_nano` (Pro Micro pinout) | F.Cu @ (210, 129.5) |
| Reset switch | 1 | `ceoloide:reset_switch_smd_side` | SMD |
| Mounting holes | 7 | `ceoloide:mounting_hole_npth` | NPTH |

**Routing state:** 0 segments, 0 vias, 0 zones — board is fully unrouted. Edge.Cuts outline is present (201 graphic items).

---

## 2. ⚠️ CRITICAL NETLIST DEFECT — MUST FIX BEFORE ROUTING

**Net 2 `"default_default"` has 85 pads.** This net absorbs every switch pad-2 (42) and every diode anode pad (42+1). In a diode matrix, each switch→diode link must be a **unique per-key net**.

- **Root cause (confirmed in `ergogen/biaxial_choc.ergogen.yaml`):** The config correctly uses `to: "{{colrow}}"` (switch) and `from: "{{colrow}}"` (diode) — **but** every key is declared as its own standalone zone (`key_r0c0`, `key_r1c0`, …) with no named `columns:`/`rows:` inside the zone. Ergogen therefore assigns the default column name `default` and default row name `default` to every key, so `{{colrow}}` resolves to the same string `default_default` for all 42 keys.
- **Fix:** Replace `{{colrow}}` with `{{name}}` in both footprints (each key already carries a unique `name`, e.g. `key_r0c0`):
  ```yaml
  switches:
    params:
      from: "{{column_net}}"
      to: "{{name}}"        # was: "{{colrow}}"
  diodes:
    params:
      from: "{{name}}"      # was: "{{colrow}}"
      to: "{{row_net}}"
  ```
  Then re-run Ergogen to regenerate the PCB with 42 unique switch→diode nets.
- **Consequence if routed as-is:** All diode anodes short together → the matrix scans as a single ghost-key blob. **Routing is blocked until this is corrected and the PCB regenerated.**

---

## 3. Net Categorization

### A. Power Rails (highest routing priority)
| Net | Pads | Role | Current class |
|---|---|---|---|
| `GND` | 6 | System ground | Power |
| `RAW` | 2 | 5 V USB / battery input to nice!nano | Power |
| `VCC` | 2 | 3.3 V regulated output from nice!nano | Power |

### B. Control / Reset
| Net | Pads | Role |
|---|---|---|
| `RST` | 4 | Reset switch → MCU RST (momentary to GND) |

### C. High-Speed Signals
**None on this board.** USB D+/D− and the BLE antenna are contained on the nice!nano module itself. Nets `D1`/`D2` are single-pad module breakouts (no route required). This dramatically simplifies the DRC profile.

### D. Low-Speed Matrix Signals (bulk of routing work)
| Group | Nets | Pads each | Notes |
|---|---|---|---|
| Rows | `row0`–`row4` | 12 / 12 / 12 / 4 / 12 | Scan rate < 10 kHz; timing non-critical |
| Columns | `col0`–`col9` | 6–7 | Same class |
| Per-key diode links | `key_r0c0`–`key_r4c9` after §2 fix | 2 each | Shortest possible: switch pad 2 → diode anode (5 mm below switch) |
| Spare GPIO | `P19`, `P20`, `P21`, `P101`, `P102`, `P107` | 2 | Reserved breakouts — route only if used |

### E. No-Route (floating single-pad nets)
`MCU1_1`–`MCU1_24`, `D1`, `D2` — module pin stubs; exclude from ratsnest completion checks.

---

## 4. High-Level Layout Strategy

Placement is fixed by Ergogen (switch matrix geometry is the product). Strategy is therefore **routing-layer discipline**:

1. **Layer assignment convention (standard for 2-layer keyboards):**
   - **B.Cu (switch side): COLUMN traces** — switch pad 1s live here; columns run vertically through the key grid.
   - **F.Cu (MCU side): ROW traces** — rows run horizontally; THT diodes give free layer transitions at each key.
2. **Zone plan:** GND copper pour on **both** F.Cu and B.Cu, stitched with vias on a ~10 mm grid and around the MCU. This replaces discrete GND routing (only 6 GND pads) and improves BLE module ground reference.
3. **Power routing order (strict):**
   1. `GND` pour + stitching vias
   2. `RAW` — thick trace, MCU pad → any battery/USB consumer
   3. `VCC` — thick trace (feeds nothing off-module here unless spare GPIO used)
   4. `RST` — reset switch to MCU, keep < 30 mm, away from row/col bundles
4. **Matrix fan-in:** Route all 5 rows + 10 cols toward the MCU at (210, 129.5). Bundle them into two harnesses (left keys / right keys of the fan) and enter the MCU region on alternating layers to avoid a via farm under the module.
5. **Diode links:** After the netlist fix, each `SxDx` net is a < 8 mm point-to-point trace on B.Cu — route these **first** among signals since they're fully constrained.
6. **Keep-outs:** No copper pour or traces under the nice!nano antenna end (top ~8 mm of the module footprint); respect the 3.4 mm / 1.9 mm / 3.0 mm NPTH switch holes and 7 mounting holes with full clearance.

---

## 5. DRC Profile (KiCad Net Classes)

| Net Class | Members | Track Width | Clearance | Via (dia/drill) | Rationale |
|---|---|---|---|---|---|
| `Power` | RAW, VCC | **0.5 mm** | 0.2 mm | 0.8 / 0.4 mm | ≤ 500 mA @ 1 oz → 0.5 mm gives large margin, low IR drop |
| `GND` | GND | Pour + **0.5 mm** min trace | 0.2 mm | 0.8 / 0.4 mm | Pour-primary; trace only for stitching tails |
| `Signal` (default) | rows, cols, SxDx, RST, spare GPIO | **0.25 mm** | 0.2 mm | 0.6 / 0.3 mm | Standard low-cost fab capability (JLC/PCBWay 6/6 mil safe) |

**Global rules:**
- Minimum clearance (all): **0.2 mm** — comfortably above 0.127 mm fab minimum
- Minimum via drill: **0.3 mm**; minimum annular ring: **0.15 mm**
- Copper-to-Edge.Cuts: **0.3 mm**; copper-to-NPTH: **0.3 mm**
- Bends: **45° only** — no 90° corners (per verification policy)
- Zone settings: 0.3 mm clearance, 0.25 mm min width, thermal relief on THT diode pads (spoke 0.4 mm)

---

## 6. Handoff to Routing Specialist

**Blocked pending:** §2 netlist fix + Ergogen regeneration.

Once unblocked, execute in this order:
1. Lock MCU1, RST1, MH1–7 (already fixed by Ergogen — do not move)
2. Pour GND zones (both layers) per §4.2
3. Route Power class (RAW, VCC, RST) per §4.3
4. Route all 42 per-key diode links on B.Cu
5. Route columns on B.Cu, rows on F.Cu, fan into MCU per §4.4
6. Deliver: routed `.kicad_pcb` + via count + total trace length report → Design Verifier