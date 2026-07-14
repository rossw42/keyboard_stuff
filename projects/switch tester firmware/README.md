# Switch Tester Keyboard (YMDK ID75 + Vial)

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

## Status

**Ready — waiting on hardware.** Firmware and tooling are complete and tested;
the rp2040 firmware is already built. When the ID75 arrives:

1. Identify the PCB variant: enter the bootloader (double-tap the reset button
   on the PCB back) and check the drive name — `RPI-RP2` = rp2040 (already
   built), `MT.KEY` = f103 (build it with the command below).
2. Copy the `.uf2` to the bootloader drive.
3. Press `EE_CLR` (layer 2, bottom-left) once so the compiled defaults load.
4. In Vial: **File → Save current layout** → save as `template.vil` here.
5. Update `switches.md` with the real inventory, then
   `python vil_tool.py generate` and load the result in Vial.

---

## Files in this project

| File | Purpose |
|---|---|
| `switches.md` | **Source of truth** — your switch inventory as Markdown tables (edit this) |
| `vil_tool.py` | Converts `switches.md` → a loadable Vial layout (`.vil`); also `extract`, `check`, `report` |
| `sample_template.vil` | Example template (matches the firmware defaults) for offline testing — replace with a real `template.vil` exported from your board |
| `project_description.md` | Full project design document |
| `chathistory.md` | Original planning-session transcript |

Firmware keymap lives in the vial-qmk repo:
`d:\GitHub2\vial-qmk\keyboards\ymdk\id75\keymaps\switch_tester\`
(`config.h`, `rules.mk`, `keymap.c`, `vial.json`, `readme.md`)

Pre-built firmware (rp2040 variant):
`d:\GitHub2\vial-qmk\ymdk_id75_rp2040_switch_tester.uf2`

---

## One-time setup

### 1. Build the firmware

Build from the **vial-qmk** repo (not official qmk_firmware). Pick the target
matching your ID75's PCB — check which volume name appears in bootloader mode:
`RPI-RP2` → rp2040, `MT.KEY` → f103.

```bash
cd d:\GitHub2\vial-qmk
qmk compile -kb ymdk/id75/rp2040 -km switch_tester   # RP2040 PCB
qmk compile -kb ymdk/id75/f103   -km switch_tester   # APM32F103 PCB
```

Or via Docker (works from plain PowerShell, no QMK toolchain needed):

```powershell
docker run --rm -v "d:/GitHub2/vial-qmk:/qmk_firmware" -w /qmk_firmware `
  qmkfm/qmk_cli make ymdk/id75/rp2040:switch_tester
```

Artifact: `ymdk_id75_rp2040_switch_tester.uf2` (repo root / `.build\`).
The rp2040 build is already done; only rebuild if the keymap changes, or run
the f103 target if that's the PCB that arrives.

### 2. Flash

1. Enter the bootloader: **double-tap the reset button** on the back of the
   PCB (or hold the top-left key while plugging in — this also clears EEPROM).
2. A USB drive appears (`RPI-RP2` or `MT.KEY`).
3. Copy the `.uf2` onto it. The board reboots on its own. (The drive vanishing
   right after the copy is normal — that means it worked.)

> After the **first** flash of this keymap (or after changing keymap defaults),
> reset the EEPROM so the compiled defaults take effect: press the `EE_CLR`
> key on the Fn layer (layer 2, bottom-left), or use Vial's "Reset EEPROM",
> or re-plug while holding the top-left key.

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
| 3 | **Test** — every key fires macro `M(row·15+col)`; **bottom-right = `TG(3)`** to exit |

While layer 3 is active the RGB matrix turns solid cyan as a "test mode"
indicator.

Macro index ↔ key position is row-major: `M0` = top-left … `M73`, with
`M74` unused (bottom-right is the exit key).

### Reactive same-type RGB highlighting

The ID75 has one addressable RGB LED per key (RGB_MATRIX, not just
underglow), so the Test layer does more than type text: **pressing any
switch lights up every other key of the same type** and turns everything
else off — Clicky = blue, Tactile = purple, Linear = red. The board stays
dark until the first press after entering the Test layer.

This works with **zero changes to `switches.md` or `vil_tool.py`** — the
generated macro text already always starts with the literal type word
(`"Clicky - ..."`, `"Tactile - ..."`, `"Linear - ..."`), and the firmware
reads that first character straight out of the Vial dynamic-macro EEPROM
buffer at runtime (`dynamic_keymap_macro_get_buffer()`), rebuilding its
75-entry type map every time the Test layer is (re-)entered — so it always
matches whatever `.vil` you last loaded. See `keymap.c` in the vial-qmk
keymap folder for the implementation. Changing the *highlight logic itself*
(colors, behavior) does require a firmware rebuild, but the day-to-day
switch-swap workflow below is completely unaffected.


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
| 4,14 | RESERVED         |        |           | exit key |
```

- **`Pos` is the full matrix position `row,col`** (top-left = `0,0`). Every
  entry is fully self-describing — macro index = `row × 15 + col` — so any
  switch type can live at any position. The `## Row N — Type` sections are
  purely organizational.
- `Type` should be filled explicitly per switch; an empty cell falls back to
  the section heading's type. The typed output always states the actual type.
- `RESERVED` marks skipped positions (keep `4,14` for the `TG(3)` exit key).
- Duplicate positions are rejected with a line-number error.
- Options comment: `terminator` = `enter` | `tab` | `none`;
  `include-force` = include `(NNg)` in output; `auto-sort` = re-seat each
  section's switches across its positions heaviest → lightest (set `false`
  to make the `Pos` column authoritative).
- `...` placeholder rows are ignored.

### vil_tool.py commands

```bash
python vil_tool.py generate                 # switches.md + template.vil -> switch_tester_generated.vil
python vil_tool.py check                    # validate + estimate EEPROM macro buffer usage
python vil_tool.py report                   # print M-index -> position -> switch cheat sheet
python vil_tool.py extract exported.vil     # pull macros back out of a .vil into markdown
```

Useful flags: `-i/--inventory`, `-t/--template`, `-o/--output`,
`--cols` (matrix width; auto-detected from the template's layout),
`--buffer-size` (default 3000 bytes — the conservative estimate of macro
EEPROM space on the ID75 with this firmware).

---

## Using this on a different keyboard

The tool is board-agnostic — nothing in it is ID75-specific:

1. Flash the board with vial-qmk firmware whose
   `DYNAMIC_KEYMAP_MACRO_COUNT` ≥ `rows × cols` (see this keymap's `config.h`
   for the pattern), with a test layer where key `(r,c)` fires `M(r·cols+c)`.
2. Export `template.vil` from that board in Vial (the tool reads the matrix
   width from it automatically).
3. Reshape `switches.md` with that board's `row,col` positions.
4. `generate` → load. Same loop.

If the board's stock Vial firmware already exposes enough macro slots, you
don't even need a custom flash — set the test layer keys once in the Vial GUI
and just use the tool for macros.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Vial refuses to load the generated `.vil` | Regenerate from a **fresh export** of the connected board (UID/shape must match) |
| Keys type the wrong/old defaults after reflash | EEPROM still holds the old keymap — `EE_CLR` (Fn layer) then reload the `.vil` |
| `check` reports FAIL | Shorten switch names, drop `include-force`, or trim entries |
| Test layer types nothing on some keys | Those macros are empty — inventory has fewer entries than keys, or a `RESERVED` marker is misplaced |
| Bootloader drive never appears | Double-tap the reset button faster; or hold top-left key while plugging in |