# PCB Footprints Guide — ceoloide/ergogen-footprints with Local Ergogen v4.1

> Milestone 4 documentation. Sources: `D:\GitHub2\ergogen-footprints` (repo + README), `docs/ERGOGEN_REFERENCE.md` §PCBs, and `working_samples/split/samoklava/config.yaml` (a real config with a `pcbs:` section).

## 1. What is ergogen-footprints?

[ceoloide/ergogen-footprints](https://github.com/ceoloide/ergogen-footprints) is a library of custom PCB footprints for Ergogen, written as Ergogen footprint modules (`.js` files). It covers everything needed for a keyboard PCB: switches (MX, Choc v1/v2, Gateron low-profile), diodes, microcontrollers (nice!nano, SuperMini nRF52840), displays, encoders, TRRS jacks, battery connectors, power/reset switches, and routing utilities.

**Local clone:** `D:\GitHub2\ergogen-footprints`

**Requirements:** Ergogen ≥ **4.1.0** (installed: 4.1.0 ✓) and `template: kicad8` in the pcb config for current footprint versions.

## 2. Making footprints available to a local Ergogen run

Per the repo README, the mechanism is a **`footprints` folder next to your config**:

```
my-keyboard/
├── config.yaml
└── footprints/            <- copy the .js files you need here
    ├── switch_mx.js
    ├── diode_tht_sod123.js
    └── mcu_nice_nano.js
```

Then run Ergogen **against the folder, not the file**:

```
ergogen my-keyboard -o my-keyboard/output
```

Footprints are referenced in YAML by filename without extension, prefixed with `ceoloide/` if you keep the folder structure `footprints/ceoloide/switch_mx.js` (or bare `switch_mx` if placed at `footprints/` root — match the `what:` name to the file's relative path under `footprints/`).

## 3. `pcbs:` YAML syntax with real footprint names

```yaml
pcbs:
  my_board:
    template: kicad8
    outlines:
      edge:
        outline: board_outline    # an outline defined in your outlines: section
        layer: Edge.Cuts
    footprints:
      switches:
        what: switch_mx
        where: true               # every point tagged as a key
        params:
          from: "{{colrow}}"      # per-key net, e.g. r0c1
          to: "{{col_net}}"       # column net
          hotswap: true
          reversible: false
      diodes:
        what: diode_tht_sod123
        where: true
        adjust:
          shift: [0, -5]          # tuck diode below the switch
        params:
          from: "{{colrow}}"
          to: "{{row_net}}"
      controller:
        what: mcu_nice_nano
        where:
          ref: matrix_r0c0        # anchor relative to a point
          shift: [30, 0]
        params:
          P0: row_0
          P1: row_1
          P2: col_0
          P3: col_1
          # ... P4–P21, RAW, GND, RST, VCC available
```

Key concepts (see `ERGOGEN_REFERENCE.md` §PCBs for full detail):
- `what:` — footprint name (file name without `.js`)
- `where:` — filter/anchor selecting which points get the footprint (`true` = all, tag filters, or an anchor)
- `params:` — footprint-specific parameters; net params (like `from`/`to`, `P0`–`P21`) wire the electrical connections
- `{{colrow}}`-style templating substitutes per-point metadata into net names

## 4. Most useful footprints in the repo

| Footprint | Purpose |
|---|---|
| `switch_mx` | Cherry MX switch, hotswap/solder, reversible option |
| `switch_choc_v1_v2` | Kailh Choc v1/v2 low-profile switch |
| `switch_gateron_ks27_ks33` | Gateron low-profile KS-27/KS-33 |
| `diode_tht_sod123` | Diode, dual THT/SOD-123 SMD pads |
| `mcu_nice_nano` | nice!nano / Pro Micro–compatible controller (P0–P21, RAW, GND, RST, VCC) |
| `mcu_supermini_nrf52840` | SuperMini nRF52840 controller |
| `rotary_encoder_ec11_ec12` | EC11/EC12 rotary encoder |
| `trrs_pj320a` | TRRS jack (split keyboards) |
| `display_nice_view` / `display_ssd1306` | nice!view / OLED displays |
| `mounting_hole_npth` / `mounting_hole_plated` | Case mounting holes |
| `reset_switch_smd_side` / `power_switch_smd_side` | Side-actuated reset/power switches |
| `battery_connector_jst_ph_2` | JST-PH battery connector (wireless builds) |
| `utility_router` | Draw traces/routes declaratively from YAML |
| `utility_text` / `utility_ergogen_logo` | Silkscreen text / logo |
| `utility_filled_zone` / `utility_keepout_zone` | Copper fill / keepout zones |
| `utility_point_debugger` | Debug marker showing each point's location |

## 5. Output structure & verifying in KiCad

Running `ergogen <config-folder> -o output` produces:

```
output/
├── points/       # points debug data (yaml)
├── outlines/     # DXF/SVG outlines
├── cases/        # JSCAD 3D cases
└── pcbs/
    └── my_board.kicad_pcb    # one file per entry under pcbs:
```

Open `pcbs/my_board.kicad_pcb` directly in **KiCad 8** (double-click or `File → Open` in the PCB Editor — no project file needed). Verify:
1. The board outline appears on Edge.Cuts
2. Switch footprints sit at each key point
3. Nets are assigned (run DRC; ratsnest lines show unrouted connections — routing is normally done manually or with `utility_router` / an autorouter)

## 6. Next step for the toolkit

Per `TOOLKIT_PLAN.md` Milestone 4: teach `kle-to-ergogen` to emit a `pcbs:` section (switch + diode per point, controller template) using these footprints, so a KLE sketch converts to an openable KiCad PCB in one pipeline run.