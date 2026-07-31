# QMK to VIAL — Technical Details

Technical reference for the conversion pipeline. For usage instructions,
see [README.md](README.md).

---

## Background

The conversion logic was rebuilt in July 2026 after discovering the
previous output format was invalid (keys did not render in the Vial app).
The new converter passes a **504/504 keyboard regression test** against
real vial.json files from the vial-qmk repository.

### Why the old converter failed

It emitted one pseudo-row per key with ABSOLUTE x/y values:

```json
"keymap": [
  [{"x": 0.0, "y": 0.0}, "0,0"],
  [{"x": 1.0, "y": 0.0}, "0,1"]
]
```

Since KLE treats `x`/`y` as relative gaps and each row auto-advances y,
keys were scattered off-canvas and Vial rendered nothing. The old tests
"passed" because they compared structure heuristics, not actual KLE
parsing behavior.

---

## The vial.json Format (verified against 504 real files)

`layouts.keymap` is a **KLE (keyboard-layout-editor) serialized document**:

- A list of **rows**; each row mixes property dicts and label strings.
- Property dicts apply to the **next key only**. `x`/`y` are **relative
  gaps** (not absolute coordinates), `w`/`h` are size, `r`/`rx`/`ry`
  rotation, `d` decal, `c` color.
- Each new row advances y by 1 and resets x to the rotation anchor.
- Key labels are `"row,col"` matrix coordinates. Layout-option keys carry
  a legend-line-3 suffix: `"row,col\n\n\ngroup,choice"`.
- **Encoder entries** have legend line 9 = `"e"` and their leading pair is
  `encoderIndex,direction` (0=CCW, 1=CW):
  `"0,0\n\n\n\n\n\n\n\n\ne"`, `"0,1\n\n\n\n\n\n\n\n\ne"`.
  Encoder + layout option combine: `"0,0\n\n\n0,1\n\n\n\n\n\ne"`.

Example output (eggsworks/tamago, split ortho):

```json
{
  "name": "eggsworks/tamago",
  "vendorId": "0x4557",
  "productId": "0x7490",
  "lighting": "none",
  "matrix": {"rows": 10, "cols": 6},
  "layouts": {
    "keymap": [
      ["0,0", "0,1", "0,2", "0,3", "0,4", "0,5",
       {"x": 3}, "5,5", "5,4", "5,3", "5,2", "5,1", "5,0"],
      ["1,0", "1,1", "1,2", "1,3", "1,4", "1,5",
       {"x": 3}, "6,5", "6,4", "6,3", "6,2", "6,1", "6,0"],
      ["4,0", "4,1", "4,2", "4,3", {"w": 2}, "4,4",
       {"x": 3, "w": 2}, "9,4", "9,3", "9,2", "9,1", "9,0"]
    ]
  }
}
```

---

## Conversion Rules (derived from all 504 real pairs)

### Matrix size (`"matrix": {rows, cols}`)

Priority order:

1. `config.h` `MATRIX_ROWS`/`MATRIX_COLS` (leaf dir, then parent dirs) —
   authoritative for custom matrices (doio/kb04 1x8, cocot46plus 10x6,
   ferris 8x10)
2. `matrix_pins` pin counts (or `direct` matrix dims), **rows doubled when
   a `split` section exists**
3. Transposed-matrix detection: layouts addressing more rows than the pin
   matrix while total size matches (planck rev6: 4x12 pins wired as 8x6)
4. Layout coordinate maxima as final fallback

### Lighting

| keyboard.json | vial.json lighting |
|---|---|
| `rgb_matrix` present | `"vialrgb"` |
| `rgblight` + `backlight` | `"qmk_backlight_rgblight"` |
| `rgblight` only | `"qmk_rgblight"` |
| `backlight` only | `"qmk_backlight"` |
| none of the above | `"none"` |

### QMK config inheritance

Leaf `keyboard.json` files inherit `matrix_pins`, `encoder`, `split`,
`usb`, etc. from parent-directory `info.json`/`keyboard.json` files
(keychron/q11, ergodox_ez, ploopyco...). The converter walks the directory
chain from the keyboards root to the leaf and deep-merges every
info.json/keyboard.json found; the leaf file wins.

### Encoders

`encoder.rotary` entries (plus `split.encoder.right.rotary`, or a mirrored
copy for splits without an explicit right-side config) become paired
CCW/CW entries appended on a row below the layout. Vial identifies them
purely by the `"e"` legend and `index,direction` label — their position in
the keymap is cosmetic.

Note: real vial.json files that define encoder hardware but contain no
encoder entries simply predate Vial encoder support; adding them is an
improvement, not a mismatch.

### Lenient JSON

Several keyboard.json files in the wild contain `//` comments, trailing
commas, or missing commas between members — the loader repairs all of
these before parsing.

### Layout options (multi-layout keyboard.json)

When keyboard.json defines multiple layout macros, `layout_options.py`
derives real Vial layout options:

1. **Parse** every macro into keys identified by matrix id **plus** exact
   geometry (dz60 proves keys keep their matrix id while moving/resizing
   between ANSI and ISO, so identity must be geometric).
2. **Base selection**: `layout_aliases.LAYOUT` target, else plain `LAYOUT`,
   else the fewest-token non-`_all` name, else file order. Multiple
   candidates are tried until one yields a valid derivation.
3. **Diff** each other macro against the base; leftover keys on both sides
   are **clustered** into regions by bounding-box overlap (rotation-aware).
4. **Merge** regions across macros (shared base keys or overlapping bboxes)
   into option groups; distinct key-sets a region takes per macro become
   the group's choices (choice 0 = base form).
5. **Anchor stabilization**: the Vial GUI renders the selected choice by
   rigidly translating it so its collective bbox top-left snaps onto
   choice 0's bbox top-left (verified in vial-gui `keyboard_widget.py`,
   see `research/vial_gui_option_rendering.md`). When choices have
   different native anchors (e.g. a choice that simply deletes a key),
   nearby always-common keys are duplicated into every choice of the group
   to equalize the anchor — the same trick hand-made files use for ISO
   enter.
6. **Emit**: choice-0 keys in place tagged `"row,col\n\n\ng,0"` (matching
   the 280/293 real-file convention), alternative choices as blocks below
   the board, `layouts.labels` with heuristic names.
7. **Validate** (`validate_keymap`): the serialized KLE is re-parsed with
   the faithful KLE parser, the GUI re-anchoring is simulated, and **every
   layout macro must be reproduced exactly** (matrix ids + absolute
   geometry, multiset comparison) by some choice combination; group/choice
   indices must be contiguous, every group needs a non-empty choice 0, and
   the option bitfield must fit VIA's uint32. Any failure → the converter
   silently falls back to the single-layout keymap, so options are
   **correct by construction**.

The option bitfield packs checkbox = 1 bit, N-choice dropdown =
`(N-1).bit_length()` bits, first label in the most-significant bits;
`qmk_to_vial_porting.py` emits `VIA_EEPROM_LAYOUT_OPTIONS_SIZE` in config.h
when the total exceeds 8 bits. `--no-layout-options` disables the feature.

### Not derivable from keyboard.json (by design)

Key colors `c`, decals `d`, stepped-key props `w2/h2/x2/y2`, layout-option
label *text* / choice ordering / default polarity (editorial — contra and
plaid picked opposite defaults for identical hardware), custom display
names. Byte-identical output vs. hand-authored files is impossible;
**functional equivalence** (geometry + matrix labels + encoders + matrix
size + provably-exact option combinations) is what the test suites verify.

---

## Architecture

`keyboard_to_vial_converter.py` (synced from `../vial-research/`):

| Function | Role |
|---|---|
| `load_keyboard_config()` | inheritance-aware, lenient JSON loader |
| `layout_to_keys()` | keyboard.json layout → absolute-positioned keys |
| `encoder_keys()` | Vial encoder entries from `encoder.rotary` |
| `serialize_kle()` | absolute keys → valid KLE rows (relative offsets; rotation clusters ordered to avoid the JS falsy-zero reset problem) |
| `parse_kle()` | faithful kle-serial parser used for validation |
| `derive_matrix()` / `derive_lighting()` | rules described above (config.h parsing handles `6*2`-style expressions) |
| `build_layout_options()` | derive + validate layout options (wraps `layout_options.py`) |
| `convert_keyboard_to_vial()` | top-level entry point (`layout_options=True` by default) |

`layout_options.py`:

| Function | Role |
|---|---|
| `build_options()` | multi-macro diff → clustered option groups → labels + tagged absolute keys |
| `validate_keymap()` | GUI-rendering simulation; proves every macro is an exact choice combination |
| `option_bits()` | VIA bitfield width for `VIA_EEPROM_LAYOUT_OPTIONS_SIZE` |

`qmk_to_vial_porting.py` (coordinator) imports the converter and adds
file generation: config.h (UID + unlock combo = first/last key of the
layout), rules.mk (VIA/VIAL, AVR size trims, `ENCODER_MAP_ENABLE` when
encoders are present), keymap.c (copied from the default keymap), and a
README. It refuses to write inside any path containing `vial-qmk` unless
`--allow-vial-qmk` is passed.

---

## Testing

Run the full regression suite (reads vial-qmk read-only, writes nothing
there):

```bash
python ..\vial-research\test_all_pairs.py            # summary
python ..\vial-research\test_all_pairs.py --verbose  # per-keyboard notes
```

Five checks per pair:

1. **CONVERT** — conversion succeeds
2. **ROUNDTRIP** — generated KLE re-parses to the exact source geometry
   (x, y, w, h, r, rx, ry) and matrix labels
3. **ENCODERS** — physical encoder count matches the real file
4. **LABELS** — every matrix label in the real keymap is derivable from
   keyboard.json
5. **MATRIX** — exact rows/cols match

Current result:

```
RESULTS: 504 / 504 passed (100.0%)   [47 passed with documented notes]
```

18 reference vial.json files carry verified hand-authored discrepancies
(stale matrix numbering, PCB keys absent from every keyboard.json layout,
bottom-up row numbering, missing layouts section, etc.) — documented per
keyboard in `KNOWN_DISCREPANCIES` inside `test_all_pairs.py`; only the
affected check is skipped, all others still apply.

Layout-options regression (runs over EVERY keyboard.json/info.json in the
vial-qmk tree, not just the 504 pairs):

```bash
python test_layout_options.py            # summary
python test_layout_options.py --verbose  # per-board option listing
```

Four checks per board: **OPT-EXACT** (emitted options reproduce every
macro exactly under simulated GUI rendering), **OPT-STRUCT** (contiguous
indices, non-empty choice 0, ≤32-bit bitfield, matrix labels in bounds),
**FALLBACK** (boards without options produce output identical to
`layout_options=False`), **BASELINE** (single-layout output still
roundtrips exactly). Current result:

```
keyboards with layouts        : 3967
  multi-layout boards         : 1467
    options emitted           : 1384
    fallback (single layout)  : 83
FAILURES                      : 0
```

See `..\vial-research\docs\KLE_FORMAT_FIX_2026-07.md` and the
`research/` folder here (`vial_layout_options_format.md`,
`vial_gui_option_rendering.md`, `multi_layout_diff_analysis.md`) for the
full research write-ups.

---

*Last Updated: July 2026 (layout options added)*
