# Switch Tester Keyboard (Custom RP2040 Lumberjack-style + Vial)

A fully working keyboard that doubles as a **switch tester**: toggle to the
Test layer and every key types out the name of the switch installed in that
position, e.g.

```
Clicky - Kailh Box White (45g)
Tactile - Boba U4T (62g)
Linear - Gateron Oil King (55g)
```

Switch names live in **Vial dynamic macros (EEPROM)** and are bulk-managed
from a Markdown file — **no reflashing, no per-macro GUI editing** when you
swap switches.

See [`project_description.md`](project_description.md) for the full design
rationale, and [`chathistory.md`](chathistory.md) for the original planning
session.

---

## Hardware

**Custom RP2040 Lumberjack-style board** (5×12 ortholinear, 60 keys,
per-key RGB, unreleased). Same physical layout and case fit as the Peej
Lumberjack, but with an RP2040 controller and per-key addressable LEDs.

- **Flash method**: UF2 drag-and-drop (double-tap reset → `RPI-RP2` drive
  appears → copy `.uf2`)
- **EEPROM**: ~4 KB emulated (RP2040 flash-backed) — ample for 60 macros
- **No existing QMK definition**: a new `keyboard.json` is needed (GPIO/LED
  wiring required from hardware designer before this step)

---

## Status

**Firmware + tooling complete (for 5×12 layout); awaiting GPIO/LED wiring
to write `keyboard.json` and build firmware.** Once hardware details are
in hand:

1. Create `keyboards/<vendor>/<boardname>/keyboard.json` (matrix pins,
   RP2040, RGB matrix config) in vial-qmk.
2. Create `keymaps/switch_tester/` (already designed — see §6 of
   `project_description.md`), generate a fresh UID, build and flash.
3. Press `EE_CLR` (layer 2) once so compiled defaults load.
4. In Vial: **File → Save current layout** → save as `template.vil` here.
5. Update `switches.md` with the real inventory, then
   `python vil_tool.py generate` and load the result in Vial.

---

## Files in this project

| File | Purpose |
|---|---|
| `switches.md` | **Source of truth** — your switch inventory as Markdown tables (edit this) |
| `vil_tool.py` | Converts `switches.md` → a loadable Vial layout (`.vil`); also `extract`, `check`, `report` |
| `sample_template.vil` | Example template for offline testing — replace with a real `template.vil` exported from your board |
| `project_description.md` | Full project design document |
| `chathistory.md` | Original planning-session transcript |

Firmware keymap (to be created in vial-qmk):
`d:\GitHub2\vial-qmk\keyboards\<vendor>\<boardname>\keymaps\switch_tester\`
(`config.h`, `rules.mk`, `keymap.c`, `vial.json`)

Reference: existing Peej Lumberjack vial keymap at
`d:\GitHub2\vial-qmk\keyboards\peej\lumberjack\keymaps\vial\`

---

## One-time setup

### 1. Build the firmware

> **Prerequisite**: `keyboard.json` for the custom board must be created first
> (GPIO/LED wiring needed). See §6.1 of `project_description.md`.

Build from the **vial-qmk** repo (not official qmk_firmware):

```bash
cd d:\GitHub2\vial-qmk
qmk compile -kb <vendor>/<boardname> -km switch_tester
```

### 2. Flash

1. Enter the bootloader: **double-tap the reset button** on the PCB.
2. A USB drive appears (`RPI-RP2`).
3. Copy the `.uf2` onto it. The board reboots on its own. (The drive
   vanishing right after the copy is normal — that means it worked.)

> After the **first** flash of this keymap (or after changing keymap
> defaults), reset the EEPROM so the compiled defaults take effect: press
> the `EE_CLR` key on the Fn layer (layer 2), or use Vial's "Reset EEPROM".

### 3. Export the template

Open Vial (desktop app or [vial.rocks](https://vial.rocks)), connect the
board, then **File → Save current layout** → save as `template.vil` in this
folder. This captures your board's UID and layout shape; the tool patches
macros into it. Redo this export if you ever change layers/keys in Vial that
you want preserved.

---

## Layer map (compiled defaults)

| Layer | What it is |
|---|---|
| 0 | Base — normal typing (`MO(1)` and `MO(2)` on the bottom row) |
| 1 | Daily — empty/transparent, yours to configure in Vial |
| 2 | Fn — `QK_BOOT`, RGB controls, `EE_CLR`, and **`TG(3)` (top-right)** to enter test mode |
| 3 | **Test** — every key fires macro `M(row·12+col)`; **bottom-right = `TG(3)`** to exit |

While layer 3 is active the RGB matrix turns solid cyan as a "test mode"
indicator.

Macro index ↔ key position is row-major: `M0` = top-left … `M58`, with
`M59` unused (bottom-right = `4,11` is the exit key `TG(3)`).

### Reactive same-type RGB highlighting

The board has one addressable RGB LED per key (RGB_MATRIX, 60 keys total),
so the Test layer does more than type text: **pressing any switch lights up
every other key of the same type** and turns everything else off —
Clicky = blue, Tactile = purple, Linear = red. The board stays dark until
the first press after entering the Test layer.

This works with **zero changes to `switches.md` or `vil_tool.py`** — the
generated macro text already always starts with the literal type word
(`"Clicky - ..."`, `"Tactile - ..."`, `"Linear - ..."`), and the firmware
reads that first character straight out of the Vial dynamic-macro EEPROM
buffer at runtime (`dynamic_keymap_macro_get_buffer()`), rebuilding its
60-entry type map every time the Test layer is (re-)entered. See `keymap.c`
in the vial-qmk keymap folder for the implementation.

---

## The update loop (every switch swap)

```
1. Edit the switch's entry in switches.md (its row,col position)
2. python vil_tool.py generate
3. Vial: File -> Load saved layout -> switch_tester_generated.vil
Done. (~30 seconds, no reflash)
```

### `switches.md` format

```markdown
<!-- vil-tool: terminator=enter  include-force=true  auto-sort=true -->

## Row 0 — Clicky

| Pos  | Switch           | Type   | Force (g) | Notes |
|------|------------------|--------|----------:|-------|
| 0,0  | Cherry MX Green  | Clicky |        80 |       |
| 0,1  | Gateron Oil King | Linear |        55 | mixed in a clicky row — fine |
| 4,11 | RESERVED         |        |           | exit key |
```

- **`Pos` is the full matrix position `row,col`** (top-left = `0,0`,
  bottom-right = `4,11`). Macro index = `row × 12 + col`.
- `Type` should be filled explicitly per switch; an empty cell falls back
  to the section heading's type. The typed output always states actual type.
- `RESERVED` marks skipped positions (keep `4,11` for the `TG(3)` exit key).
- Duplicate positions are rejected with a line-number error.
- Options comment: `terminator` = `enter` | `tab` | `none`;
  `include-force` = include `(NNg)` in output; `auto-sort` = re-seat each
  section's switches across its positions heaviest → lightest (set `false`
  to make the `Pos` column authoritative).

### vil_tool.py commands

```bash
python vil_tool.py generate                 # switches.md + template.vil -> switch_tester_generated.vil
python vil_tool.py check                    # validate + estimate EEPROM macro buffer usage
python vil_tool.py report                   # print M-index -> position -> switch cheat sheet
python vil_tool.py extract exported.vil     # pull macros back out of a .vil into markdown
```

Useful flags: `-i/--inventory`, `-t/--template`, `-o/--output`,
`--cols` (matrix width; auto-detected from the template's layout),
`--buffer-size` (default 3000 bytes — conservative estimate of macro
EEPROM space on this firmware).

---

## Using this on a different keyboard

The tool is board-agnostic — nothing in it is specific to this board:

1. Flash the board with vial-qmk firmware whose
   `DYNAMIC_KEYMAP_MACRO_COUNT` ≥ `rows × cols` (see this keymap's
   `config.h` for the pattern), with a test layer where key `(r,c)`
   fires `M(r·cols+c)`.
2. Export `template.vil` from that board in Vial (the tool reads the
   matrix width from it automatically).
3. Reshape `switches.md` with that board's `row,col` positions.
4. `generate` → load. Same loop.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Vial refuses to load the generated `.vil` | Regenerate from a **fresh export** of the connected board (UID/shape must match) |
| Keys type the wrong/old defaults after reflash | EEPROM still holds the old keymap — `EE_CLR` (Fn layer) then reload the `.vil` |
| `check` reports FAIL | Shorten switch names, drop `include-force`, or trim entries |
| Test layer types nothing on some keys | Those macros are empty — inventory has fewer entries than keys, or a `RESERVED` marker is misplaced |
| Bootloader drive never appears | Double-tap the reset button faster |
