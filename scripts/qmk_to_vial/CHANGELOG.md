# QMK → Vial Converter — Changelog

---

## [Unreleased] — July 2026

### Added

- **Layout options** (`layout_options.py`, new file): when `keyboard.json` defines
  multiple layout macros, the converter now derives real Vial layout options — the
  ISO/ANSI dropdowns and checkboxes in Vial's Layouts pane (`layouts.labels` +
  per-key `"row,col\n\n\ng,c"` KLE tags).  Alternative choices are drawn below the
  board in the KLE; the Vial GUI re-anchors them onto the default keys automatically.

- **End-to-end validation** (`validate_keymap` in `layout_options.py`): the
  serialized KLE is re-parsed, the Vial GUI's bounding-box re-anchoring is
  simulated, and **every layout macro in keyboard.json must be reproduced exactly**
  (matrix ids + absolute geometry) by some combination of option choices.  Any
  failure causes the converter to silently fall back to the previous single-layout
  behavior — no "almost right" output is ever emitted.

- **`--no-layout-options` flag** in `qmk_to_vial_porting.py`: disables layout-option
  derivation and always emits just the first layout (previous behavior).

- **`VIA_EEPROM_LAYOUT_OPTIONS_SIZE`** auto-emitted in `config.h` when the derived
  option bitfield exceeds 8 bits (VIA's default 1-byte storage).

- **`MATRIX_ROWS 6*2` style product-expression support** in `_parse_matrix_define`:
  split boards that express row count as a multiplication (e.g. `viktus/sp111`) now
  parse correctly (bug discovered and fixed during layout-options regression testing).

- **Research docs** (`research/` folder, new):
  - `vial_layout_options_format.md` — authoritative format spec reverse-engineered
    from 293 real vial.json files with `layouts.labels`
  - `vial_gui_option_rendering.md` — actual vial-gui source analysis: how
    `place_widgets()` shows/hides and re-anchors option groups
  - `multi_layout_diff_analysis.md` — how layout macros map to option groups

- **`test_layout_options.py`** (new): layout-options regression suite over every
  `keyboard.json` / `info.json` in the vial-qmk tree. Four checks per board:
  `OPT-EXACT`, `OPT-STRUCT`, `FALLBACK`, `BASELINE`.

### Validation results (layout options)

Tested across the full vial-qmk keyboards tree:

```
keyboards with layouts        : 3,967
  multi-layout boards         : 1,467
    options emitted           : 1,384  (94.4% of multi-layout boards)
    fallback (single layout)  :    83
FAILURES                      :     0
```

### Known limitations (by design)

- Option/choice **label text** is heuristic ("Backspace: 2u/Split", "Bottom Row:
  6.25u Space/7u Space", generic "Option 1/2") — geometry and key membership are
  exact; the text is cosmetic and easy to hand-edit in the generated `vial.json`.
- Default (choice 0) is the plainest-named macro (honoring
  `layout_aliases.LAYOUT`), which may differ from a human author's preference.
- Only combinations asserted by keyboard.json macros are proven; the option lattice
  may allow extra combinations, which is harmless (Vial addresses keys by matrix
  position).

---

## [1.0.0] — July 2026 (initial publish)

### Added

- `keyboard_to_vial_converter.py`: correct KLE-format vial.json generation from
  QMK `keyboard.json` / `info.json`, including:
  - Proper KLE serialization (relative `x`/`y` offsets, rotation clusters ordered
    to avoid the JS falsy-zero reset problem)
  - Faithful KLE parser (`parse_kle`) for roundtrip validation
  - QMK directory-inheritance loader (`load_keyboard_config`): deep-merges parent
    `info.json` / `keyboard.json` files from the keyboards root to the leaf
  - Lenient JSON loader: tolerates `//` comments, trailing commas, missing commas
  - Matrix derivation priority chain: `config.h` `MATRIX_ROWS/COLS` →
    `matrix_pins` (rows doubled for splits, direct-pin supported) → transposed-
    matrix detection → layout coordinate maxima
  - Encoder support: `encoder.rotary` + split right-side encoders → Vial `"e"`
    legend entries
  - Lighting detection: `rgb_matrix` / `rgblight` / `backlight` → correct
    `"lighting"` value

- `qmk_to_vial_porting.py`: full keymaps/vial/ folder generation:
  - `vial.json`, `config.h` (UID + unlock combo), `rules.mk` (VIA/VIAL flags,
    AVR size trims, `ENCODER_MAP_ENABLE`), `keymap.c` (copied from default
    keymap, encoder_map appended when needed), `README.md`
  - Refuses to write into a vial-qmk checkout without `--allow-vial-qmk`

- `README.md`, `TECHNICAL_DETAILS.md`: full usage and internal documentation

### Validation (initial)

- 504 / 504 real vial-qmk keyboard pairs passed (100%)
- 11 / 11 vial-qmk via keymaps byte-exact
- 2,092 QMK via keymaps from git history: 61.6% mechanically derivable, 0 failures
