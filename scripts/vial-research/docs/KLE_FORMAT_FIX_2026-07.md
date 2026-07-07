# vial.json Converter Rewrite — Correct KLE Format (July 2026)

## Why the old converter produced no keys in Vial

The previous `keyboard_to_vial_converter.py` emitted one pseudo-row per key
with **absolute** x values:

```json
"keymap": [
  [{"x": 0.0, "y": 0.0}, "0,0"],
  [{"x": 1.0, "y": 0.0}, "0,1"],
  ...
]
```

The old tests "passed" because they compared the generated output against
itself/structural heuristics — not against how Vial actually parses the
keymap. The real `layouts.keymap` is a **KLE (keyboard-layout-editor)
serialized document**:

- The keymap is a list of **rows**; each row is a flat list mixing property
  dicts and label strings.
- Property dicts apply to the **next key only**: `x`/`y` are **relative
  gaps**, `w`/`h` are size, `r`/`rx`/`ry` rotation, `d` decal, `c` color.
- Each new row advances y by 1 and resets x to the rotation anchor.
- Labels are `"row,col"` matrix coordinates. Layout-option keys carry a
  legend-line-3 suffix: `"row,col\n\n\ngroup,choice"`.

Feeding absolute coordinates as "relative gaps" and putting every key in
its own row scattered keys off-screen / stacked them — Vial rendered
nothing usable.

## Verified format facts (from 504 real vial.json files)

1. **Encoder entries** — legend line 9 (10th `\n` field) is `"e"`. The
   leading pair is `encoderIndex,direction` (0=CCW, 1=CW), **not** a matrix
   coordinate: `"0,0\n\n\n\n\n\n\n\n\ne"`, `"0,1\n\n\n\n\n\n\n\n\ne"`.
   Encoder + layout option combine: `"0,0\n\n\n0,1\n\n\n\n\n\ne"`.
   Real files with encoder hardware but no encoder entries simply predate
   Vial encoder support.
2. **Matrix size** — priority order that matches all reference files:
   1. `config.h` `MATRIX_ROWS`/`MATRIX_COLS` (leaf dir, then parents) —
      authoritative for custom matrices (doio/kb04 1x8, cocot46plus 10x6,
      ferris 8x10).
   2. `matrix_pins` pin counts (or `direct` matrix dims), **rows doubled
      when a `split` section exists**.
   3. Transposed-matrix detection: if layouts address more rows than the
      pin matrix while total size matches (planck rev6: 4x12 pins wired
      as 8x6), use layout maxima.
   4. Layout coordinate maxima as final fallback.
3. **QMK config inheritance** — leaf `keyboard.json` files inherit
   `matrix_pins`, `encoder`, `split`, `usb`, etc. from parent-directory
   `info.json`/`keyboard.json` (keychron/q11, ergodox_ez, ploopyco...).
   The converter deep-merges the directory chain.
4. **Lenient JSON** — 4 keyboard.json files in vial-qmk contain `//`
   comments, trailing commas, or missing commas. The loader repairs these.
5. **Hand-authored content not derivable from keyboard.json**: key colors
   `c`, decals `d`, stepped-key props `w2/h2/x2/y2`, layout-option labels
   & placement, custom display names — byte-identical output is impossible
   by design; functional equivalence is the correct target.

## New architecture

- `keyboard_to_vial_converter.py`
  - `load_keyboard_config()` — inheritance-aware, lenient loader
  - `layout_to_keys()` — keyboard.json layout → absolute keys
  - `encoder_keys()` — Vial encoder entries from `encoder.rotary`
    (+ split right half)
  - `serialize_kle()` — absolute keys → valid KLE rows (relative offsets,
    rotation clusters ordered to avoid the JS falsy-zero reset problem)
  - `parse_kle()` — faithful kle-serial parser used for validation
  - `derive_matrix()`, `derive_lighting()` per the rules above
- `test_all_pairs.py` — semantic regression across all 504 CSV pairs:
  1. CONVERT, 2. ROUNDTRIP (generated KLE re-parses to the exact source
  geometry), 3. ENCODERS (physical count), 4. LABELS (every real matrix
  label derivable from keyboard.json), 5. MATRIX (exact rows/cols match).

## Result

```
RESULTS: 504 / 504 passed (100.0%)   [47 passed with documented notes]
```

18 keyboards carry documented, verified discrepancies in the *reference*
files (stale matrix numbering vs. current keyboard.json, keys wired on the
PCB but absent from every layout, bottom-up row numbering, missing layouts
section). These are listed with reasons in `KNOWN_DISCREPANCIES` inside
`test_all_pairs.py`; the affected single check is skipped and reported as
a note, all other checks still apply.

## Coordinator

`scripts/qmk_to_vial/qmk_to_vial_porting.py` was rewritten to import the
tested converter (its own duplicated broken logic removed). It generates
`vial.json`, `config.h` (UID + unlock combo = first/last key of layout),
`rules.mk` (VIA/VIAL, AVR size trims, `ENCODER_MAP_ENABLE` when encoders
present), `keymap.c` (copied from the default keymap), `README.md`. It
**refuses to write inside a vial-qmk checkout** unless `--allow-vial-qmk`
is passed.