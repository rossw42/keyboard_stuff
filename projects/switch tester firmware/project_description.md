# Switch Tester Keyboard — Project Description

**Status:** Implemented (firmware + tooling built; awaiting hardware for on-device testing) — see `README.md` for usage
**Target hardware (reference build):** YMDK / Idobao ID75 (5×15 ortho, 75 keys)
**Firmware base:** vial-qmk (`d:\GitHub2\vial-qmk`, branch `vial`)
**Project folder:** `D:\GitHub\keyboard_stuff\projects\switch tester firmware\`

---

## 1. Concept

A fully functional daily-driver keyboard (hotswap, so switches can be swapped freely) that doubles as a **switch tester**. It has:

- **Normal layers** — it types like a regular keyboard.
- **A dedicated Test Layer** — while active, pressing any key types out a description of the physical switch installed in that position, e.g.:

  ```
  Clicky - Kailh Box White (45g)
  Tactile - Boba U4T (62g)
  Linear - Gateron Oil King (55g)
  ```

  Each output ends with Enter so successive presses land on their own lines (Tab variant optional for spreadsheet logging).

The switch descriptions live in Vial **dynamic macros** (EEPROM), so relabeling after a switch swap **never requires reflashing firmware**.

### The key workflow requirement

Editing 75 macro strings one at a time in the Vial GUI (vial.rocks or the desktop app) is painful. Instead:

> **Single source of truth = a plain text file on disk** (`switches.md`, a Markdown table — see §4). A small script converts that file into a Vial **saved layout (`.vil`)**, which is then loaded into Vial in one action: *File → Load saved layout*. Done — all 75 macros updated at once.

No firmware rebuild, no per-macro GUI clicking. Round-trip is also supported: export `.vil` from Vial → script extracts the current macros back into the inventory file.

---

## 2. Why this architecture (decisions already made)

From the previous research session (`chathistory.md`):

| Approach | Verdict |
|---|---|
| Vial Matrix Tester tab | Only shows positions, not switch names. Rejected. |
| `CONSOLE_ENABLE` / hid_listen | Requires host-side tooling to view; outputs row/col not names. Rejected. |
| Compiled `send_string()` per key | Requires **reflash on every switch swap** — defeats the purpose. Rejected. |
| Raw HID + companion app | Most powerful, but requires a resident host app. Overkill (kept as a future option). |
| **Dynamic macros with bumped limits** | ✅ **Chosen.** GUI/file-reconfigurable, no reflash, buffer math works. |

New decision for this session:

| Macro editing method | Verdict |
|---|---|
| Type each macro into Vial GUI | Rejected by user — too tedious for 75 entries. |
| **Edit a file → script generates `.vil` → "Load saved layout" in Vial** | ✅ **Chosen.** One file edit, one load action. |
| Script writes macros directly over Raw HID (Vial protocol, no GUI at all) | Possible stretch goal — see §8. |

---

## 3. The `.vil` file — how the reload trick works

A Vial "saved layout" (`.vil`) is plain JSON containing the complete board state:

```json
{
  "version": 1,
  "uid": <integer — the board's VIAL_KEYBOARD_UID>,
  "layout": [ [ [ "KC_ESC", "KC_1", ... ] ] ],   // [layer][row][col] keycode names
  "encoder_layout": [...],
  "layout_options": -1,
  "macro": [
    [ ["text", "Clicky - Kailh Box White (45g)"], ["tap", "KC_ENTER"] ],
    [ ["text", "Tactile - Boba U4T (62g)"],       ["tap", "KC_ENTER"] ]
  ],
  "vial": { "combo": [...], "tap_dance": [...], "key_override": [...] },
  "settings": { ... }
}
```

Key facts that shape the tooling:

1. **`.vil` files are UID-locked** — Vial only loads a file whose `uid` matches the connected board.
2. Therefore the generator script **never builds a `.vil` from scratch**. Instead it:
   - Takes a **template `.vil` exported once from the real board** (correct UID, layout shape, layer count baked in),
   - Patches only the `macro` array (and optionally the test-layer key assignments) from the switch inventory file,
   - Writes `switch_tester_generated.vil` for loading.
3. Because the script treats the exported `.vil` as an opaque template, **this workflow works on *any* Vial-supported keyboard**, not just the ID75. Board portability comes for free.

---

## 4. Source-of-truth file: `switches.md`

**Decided:** the primary editing surface is a **Markdown table** — easy to read, easy to edit in any editor, renders nicely on GitHub. The script parses it directly (an intermediate JSON is generated internally / on demand for round-trip and debugging, but the human only touches the Markdown).

```markdown
# Switch Tester Inventory — YMDK ID75

<!-- vil-tool: terminator=enter  include-force=true  auto-sort=true -->

## Row 0 — Clicky

| Pos  | Switch           | Type   | Force (g) | Notes        |
|------|------------------|--------|----------:|--------------|
| 0,0  | Cherry MX Green  | Clicky |        80 |              |
| 0,1  | Kailh Box Navy   | Clicky |        75 |              |
| 0,2  | Kailh Box Jade   | Clicky |        70 | thick click  |

## Row 1 — Tactile

| Pos  | Switch           | Type    | Force (g) | Notes        |
|------|------------------|---------|----------:|--------------|
| 1,0  | Zealio V2 78g    | Tactile |        78 |              |
| 1,1  | Gateron Oil King | Linear  |        55 | odd one out  |
```

Parsing rules:

- **`Pos` = full matrix position `row,col`** (top-left = `0,0`). Every entry is fully self-describing: macro index = `row × cols + col`, matching the firmware test layer exactly. Any type can live at any position — the `## Row N — {Type}` sections are purely organizational (the heading type is only a fallback for empty `Type` cells).
- **`Type` is explicit per switch** (Clicky / Tactile / Linear). The typed output *always* states the switch's actual type — one-type-per-row is only an organizing guideline, not a rule.
- Columns: `Pos` (`row,col`, required), `Switch` (name), `Type`, `Force (g)`, `Notes` (free text, **not** included in typed output).
- Options live in one HTML comment at the top (`terminator`, `include-force`, `auto-sort`) so the file is fully self-describing.
- A `RESERVED` or empty `Switch` cell marks positions excluded from macro assignment (e.g. the layer-exit key at `4,14`).
- Duplicate positions are rejected with a line-number error.
- With `auto-sort=true`, each section's switches are re-seated across that section's positions heaviest → lightest (reserved positions stay put); with `auto-sort=false` the `Pos` column is authoritative.

Conventions (initial guidelines, freely breakable via the `Type` column):

- **One switch type per row**: Clicky / Tactile / Linear — starting arrangement only.
- **Within each row, sorted heaviest → lightest actuation force**, left to right.
- Generated macro text: `"{type} - {name} ({force_g}g)"` + Enter (**terminator decided: Enter**).
- The script can **auto-sort** each row by force descending, so the file doesn't even need to be kept in order manually.
- Keys reserved for layer toggling (see §6) get a `RESERVED` switch cell — the script skips them.

An example populated file with 70+ real switches (based on the previous session's list) will ship with the project as a starting point until the real inventory is catalogued.

---

## 5. Tooling: `vil_tool.py`

A single Python script (stdlib only — `json`, `argparse`) with subcommands:

| Command | Function |
|---|---|
| `generate` | `switches.md` + `template.vil` → `switch_tester_generated.vil` (patches the `macro` array only in v1; applies auto-sort in memory — the inventory file itself is never modified; use `report` to see the sorted position map) |
| `extract` | `exported.vil` → `switches.md` (reverse: pull current macros back out, for round-trip / recovery / scaffolding a new board) |
| `check` | Validates buffer usage: total macro bytes vs. available EEPROM macro space; warns before you find out the hard way that strings got truncated |
| `report` | Prints a human-readable position → switch map (and optionally a printable cheat-sheet Markdown table) |

Notes:

- Macro encoding in `.vil` is the Vial GUI's JSON action list (`["text", "..."]`, `["tap", "KC_ENTER"]`) — the GUI handles conversion to the on-wire/EEPROM byte format when loading. The script never has to touch the binary macro format.
- Macro index assignment: `index = row × matrix_cols + col` from each entry's explicit `Pos` (M0 = top-left … M74 = bottom-right on the ID75). This matches how the test layer keys are compiled, so the mapping is exact even with mixed types and gaps. Matrix width is auto-detected from the template's layout (override with `--cols`).
- The Markdown parser is deliberately strict-but-forgiving: it only needs the `## Row` headings and the table pipes; column alignment/whitespace is free-form.
- The script is **board-agnostic**: point it at any board's exported `.vil` and a matching `switches.md` shaped to that board's rows.

### What the script does / does not touch (v1 scope)

The script **only patches macros** in the `.vil`. The Test-layer key assignments (`M0`…`M74` on layer 3) come from the **compiled firmware defaults** in `keymap.c` — they're already correct after the first flash (after an EEPROM reset), so nobody ever has to click 75 key assignments in the GUI. Having the script *also* rewrite layer keycodes in the `.vil` is on the roadmap (§8), not in v1.

> Clarification: "patching the test layer" is **not** live updating — it just means the generated `.vil` file would carry the layer-3 key assignments as well as the macros. Live (no-GUI) updating is the separate Raw-HID "push" stretch goal in §8.

### Update loop (steady state)

```
swap a switch  →  edit one table cell in switches.md
              →  python vil_tool.py generate
              →  Vial (app or vial.rocks): File → Load saved layout
              →  done (seconds, no reflash, no per-macro GUI editing)
```

---

## 6. Firmware (one-time flash)

Custom Vial keymap: `keyboards/ymdk/id75/keymaps/switch_tester/` in `d:\GitHub2\vial-qmk` (copied from the existing `keymaps/vial/` and modified).

### 6.1 ID75 hardware variants (in vial-qmk)

The current-production YMDK/Idobao ID75 ships with one of two PCBs, **both fully supported** in vial-qmk (`keyboards/ymdk/id75/`, shared `keymaps/vial/`):

| Variant | MCU | Bootloader / flashing | Logical EEPROM | Fit? |
|---|---|---|---|---|
| `ymdk/id75/rp2040` | RP2040 | UF2 drag-and-drop (`RPI-RP2` volume) | ~4 KB (8 KB flash backing, wear-leveled) | ✅ |
| `ymdk/id75/f103` | APM32F103 (STM32F103 clone) | UF2 drag-and-drop (`MT.KEY` volume) | ~4 KB (embedded-flash wear-leveled) | ✅ |

**→ Buying a new ID75 does not limit the project** — whichever PCB arrives, the EEPROM budget below holds and flashing is the same drag-and-drop UF2 process (enter bootloader: double-tap the reset button on the PCB back, or hold top-left key while plugging in). Identify the variant on arrival (check the PCB / which volume name appears in bootloader mode) and build the matching target:

```
make ymdk/id75/rp2040:switch_tester   # or
make ymdk/id75/f103:switch_tester
```

The keymap folder is shared between both variants, so only the build target differs.

### 6.2 `config.h` (keymap-level)

```c
#pragma once

#define VIAL_KEYBOARD_UID { /* fresh UID from util/vial_generate_keyboard_uid.py */ }
#define VIAL_UNLOCK_COMBO_ROWS {0, 0}
#define VIAL_UNLOCK_COMBO_COLS {0, 14}   // hold top-left + top-right to unlock

#define DYNAMIC_KEYMAP_MACRO_COUNT 80    // ≥ 75 (default is 16; stock vial keymap uses 32)
#define DYNAMIC_KEYMAP_LAYER_COUNT 4     // base / daily 1 / daily 2 / test (test = highest layer)

// Trim unused Vial dynamic features to reclaim EEPROM for macro text:
#define VIAL_COMBO_ENTRIES 4
#define VIAL_TAP_DANCE_ENTRIES 4
#define VIAL_KEY_OVERRIDE_ENTRIES 4
```

> Note: in current vial-qmk the macro **buffer** is not a fixed `#define` — it automatically gets *all EEPROM remaining* after keymaps/combos/tap-dances/etc. (`nvm_dynamic_keymap.c`). So the way to enlarge it is to shrink everything else (fewer layers, fewer dynamic-feature entries).

### 6.3 EEPROM budget (ID75, either variant, 4 layers)

| Consumer | Bytes (approx.) |
|---|---|
| Keymap: 75 keys × 2 B × 4 layers | 600 |
| Vial dynamic features (trimmed) + QMK settings + base | ~300 |
| **Remaining for macros** (of ~4 KB emulated EEPROM) | **~3.0 KB** |
| Needed: 75 × ~33 B avg (`"Tactile - Wuque Studio Aurora (63g)"` + Enter) | ~2.5 KB |

✅ Fits with ~18% headroom. `vil_tool.py check` enforces this before every load.

### 6.4 `rules.mk`

```make
VIA_ENABLE = yes
VIAL_ENABLE = yes
LTO_ENABLE = yes
VIALRGB_ENABLE = yes   # keep per-key RGB controllable from Vial (RP2040 has flash to spare)
```

### 6.5 Layers & `keymap.c` defaults

Layers 1 and 2 stay free for normal daily-driver use; the Test layer is the **highest layer (3)** so it never interferes with everyday layer stacking.

| Layer | Purpose | Contents |
|---|---|---|
| **0 – Base** | Real keyboard | Standard ortho 5×15 layout (as stock vial keymap) |
| **1 – Daily** | User's working layer | Free for daily-use config (nav, symbols, whatever — set up in Vial) |
| **2 – Daily / Fn** | User's working layer + utility | Free for daily use; also hosts `QK_BOOT`, RGB controls, `EE_CLR`, and `TG(3)` to enter test mode |
| **3 – Test** | Switch tester | Every key = `M0` … `M74` (row-major); one key stays `TG(3)` so you can get back out |

Entering test mode: `TG(3)` on layer 2 (deliberate action — avoids accidentally spraying switch names mid-sentence). One designated key on the Test layer keeps `TG(3)` to exit; that position is excluded from macro assignment.

Optional nicety (RP2040 has room): `layer_state_set_user()` sets the RGB matrix to a distinct color per row type while layer 3 is active (blue = clicky, purple = tactile, red = linear) — instant visual confirmation of test mode and switch category.

### 6.6 `vial.json`

Reuse the stock ID75 `vial.json` (5×15 grid) unchanged.

---

## 7. Portability to other QMK/Vial boards

Design rules that keep this board-agnostic:

1. **The tooling never assumes ID75.** `vil_tool.py` works from an exported `.vil` template of *whatever board is connected* — matrix size, UID, layer count all come from the export.
2. **`switches.md` describes rows generically.** For a different board, rows just have different key counts (the `extract` command can scaffold a correctly-shaped empty inventory from any board's `.vil`).
3. **Firmware requirements on any target board** are only:
   - It runs vial-qmk with `DYNAMIC_KEYMAP_MACRO_COUNT ≥ key count`,
   - Its EEPROM has room for the macro text (script's `check` command verifies),
   - It has a Test layer whose keys are assigned `M0…Mn` (in v1: set in the compiled keymap defaults, or once manually in Vial; roadmap item makes the script patch this too).
4. For boards already running stock Vial firmware with ≥ N macros available, **no reflash is needed at all** — the whole tester can be set up purely by loading a generated `.vil`.

---

## 8. Future ideas / stretch goals (explicitly out of scope for v1)

- **Direct HID push (live updating):** a `vil_tool.py push` command that speaks the Vial/VIA raw-HID protocol and writes the macro buffer directly — removing even the "Load saved layout" click. (Vial's protocol is open; the GUI is Python and can be cribbed from.)
- **Test-layer patching in the `.vil`:** have `generate` also write the `M0…Mn` test-layer key assignments into the file (v1 relies on compiled firmware defaults instead).
- Per-switch extended output (mount, spring type, lube status, price, vendor link — extra Markdown columns).
- Printable tester legend card generated from `switches.md` (`report` command output).
- OLED/companion display showing the last-pressed switch name (hardware change — different board).

---

## 9. Risks & mitigations

| Risk | Mitigation |
|---|---|
| An old-stock ATmega32u4 ID75 arrives (1 KB EEPROM) | Unlikely with current listings; fallback = shorter strings (`"C KailhBoxWht 45g"`) or Raw HID companion approach |
| f103 PCB is a revision incompatible with the in-tree firmware (readme warns some revisions differ) | Verify PCB revision before flashing; keyboard readme: "Check your PCB before flashing" |
| Vial refuses generated `.vil` (format drift between Vial versions) | Always regenerate from a fresh export; `extract`/`generate` are symmetric so drift is caught immediately |
| Macro buffer overflow silently truncates names | `check` command computes bytes vs. available space before every load |
| Accidental test-layer activation types garbage | Test layer (3) only reachable via layer-2 `TG(3)`; distinct RGB color while active |
| EEPROM-stored keymap masks new compiled defaults after reflash | Documented: after changing firmware defaults, reset via `EE_CLR`/Vial "reset EEPROM", then load the generated `.vil` |

---

## 10. Milestones

1. **M0 — Confirm hardware**: board on order; on arrival identify variant (rp2040 vs f103 — check PCB / bootloader volume name), flash stock vial keymap to verify the board works.
2. **M1 — Firmware**: create `keymaps/switch_tester/` (config.h, rules.mk, keymap.c, vial.json), fresh UID, build `make ymdk/id75/<variant>:switch_tester`, flash, verify in Vial (macro count = 80 visible).
3. **M2 — Tooling**: implement `vil_tool.py` (`extract` → `generate` → `check` → `report`), export template `.vil` from the real board.
4. **M3 — Inventory**: fill `switches.md` with the real switch collection (placeholder example list until then), sorted per the row rules.
5. **M4 — End-to-end test**: edit a switch name in the file → generate → load in Vial → press key → correct string types out. Time the loop (target: under 60 seconds).
6. **M5 — Docs**: README with the update loop, flashing instructions, and porting notes for other boards.

---

## 11. Open questions

1. ~~Which ID75 variant is it?~~ **Resolved:** board is being purchased new; both current PCB variants (rp2040 / f103) are supported, have ~4 KB EEPROM, and flash via UF2. Identify the exact variant on arrival to pick the build target — no design impact.
2. **Vial client**: desktop Vial app, vial.rocks in Chrome, or both? (Both support "Load saved layout"; desktop app is recommended for reliability of the load-file workflow.)
3. ~~Inventory file format?~~ **Resolved:** Markdown table (`switches.md`) is the primary editing surface; the script parses it directly (JSON only as an internal/debug intermediate).
4. ~~Output terminator?~~ **Resolved:** Enter (one name per line). Still configurable in the `switches.md` options comment if ever needed.
5. ~~One-type-per-row?~~ **Resolved:** it's a guideline only. The `Type` column override is a **v1 feature**; the output always states each switch's actual type.
6. ~~Script patches test-layer keys?~~ **Resolved:** roadmap (§8). v1 relies on compiled keymap defaults for the `M0…M74` test-layer assignments; the script only patches macros. (Clarified: this is not live updating — live/Raw-HID push is a separate roadmap item.)
7. ~~Which layer for testing?~~ **Resolved:** layer **3** (highest). Layers 1 and 2 remain free for daily-driver use. Entry via `TG(3)` on layer 2 is the working default (changeable in Vial anytime).
8. **Row allocation on 5 rows / 3 types** (soft, guideline only): starting split Clicky ×1, Tactile ×2, Linear ×2 — adjust once the real inventory is catalogued.
