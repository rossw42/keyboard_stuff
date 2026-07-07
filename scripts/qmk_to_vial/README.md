# QMK to VIAL Porting Scripts

Convert any QMK keyboard directory to a VIAL-enabled keymap. The conversion
logic was rebuilt in July 2026 after discovering the previous output format
was invalid (keys did not render in the Vial app) — the new converter passes
a **504/504 keyboard regression test** against real vial.json files from the
vial-qmk repository.

---

## Scripts

| Script | Purpose |
|--------|---------|
| `qmk_to_vial_porting.py` | Full porting coordinator — generates all VIAL files (vial.json, config.h, rules.mk, keymap.c, README.md) |
| `keyboard_to_vial_converter.py` | Core conversion library — keyboard.json → correct KLE-format vial.json (synced from `../vial-research/`) |
| `keyboard_to_vial_converter_precise.py` | **DEPRECATED** — old converter producing invalid absolute-coordinate output; kept for reference only |

The regression test suite lives in
`../vial-research/test_all_pairs.py` and validates against
`../vial-research/vial_keyboard_pairs.csv` (504 pairs).

---

## Usage

```bash
# Write to an output directory (recommended)
python qmk_to_vial_porting.py "D:\GitHub2\vial-qmk\keyboards\eggsworks\tamago" "output"

# Write into the keyboard directory itself (keymaps/vial/)
python qmk_to_vial_porting.py "path\to\my_keyboard"

# The script REFUSES to write inside a vial-qmk checkout unless you
# explicitly override:
python qmk_to_vial_porting.py "...\vial-qmk\keyboards\foo" --allow-vial-qmk
```

Standalone vial.json only:

```bash
python keyboard_to_vial_converter.py "path\to\keyboard.json"
```

---

## What Gets Generated

```
<output>/<keyboard_name>/keymaps/vial/
├── vial.json     # KLE-format layout, matrix size, lighting, encoders
├── config.h      # VIAL_KEYBOARD_UID + unlock combo (first + last key)
├── rules.mk      # VIA/VIAL enablement, AVR size trims, ENCODER_MAP_ENABLE
├── keymap.c      # copied from keymaps/default/keymap.c (or stub)
└── README.md     # build/flash instructions
```

Build after copying into your vial-qmk tree:

```bash
make <keyboard>/<variant>:vial        # e.g. make eggsworks/tamago:vial
make <keyboard>/<variant>:vial:flash
```

---

## The vial.json Format (correct, verified)

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
      ...
      ["4,0", "4,1", "4,2", "4,3", {"w": 2}, "4,4",
       {"x": 3, "w": 2}, "9,4", "9,3", "9,2", "9,1", "9,0"]
    ]
  }
}
```

> **Why the old converter failed:** it emitted one pseudo-row per key with
> ABSOLUTE x/y values. Since KLE treats `x`/`y` as relative gaps, keys were
> scattered off-canvas and Vial rendered nothing.

---

## Conversion Rules (derived from all 504 real pairs)

### Matrix size (`"matrix": {rows, cols}`)
Priority order:
1. `config.h` `MATRIX_ROWS`/`MATRIX_COLS` (leaf dir, then parent dirs) —
   authoritative for custom matrices (doio/kb04 1x8, cocot46plus 10x6)
2. `matrix_pins` pin counts (or `direct` matrix dims), **rows doubled when
   a `split` section exists**
3. Transposed-matrix detection: layouts addressing more rows than the pin
   matrix while total size matches (planck rev6: 4x12 pins wired as 8x6)
4. Layout coordinate maxima as final fallback

### Lighting
- `rgb_matrix` present → `"vialrgb"`
- `rgblight` + `backlight` → `"qmk_backlight_rgblight"`
- `rgblight` only → `"qmk_rgblight"`
- `backlight` only → `"qmk_backlight"`
- otherwise → `"none"`

### QMK config inheritance
Leaf `keyboard.json` files inherit `matrix_pins`, `encoder`, `split`,
`usb`, etc. from parent-directory `info.json`/`keyboard.json` files
(keychron/q11, ergodox_ez, ploopyco...). The converter deep-merges the
whole directory chain, leaf wins.

### Encoders
`encoder.rotary` entries (plus `split.encoder.right.rotary`, or a mirrored
copy for splits without explicit right-side config) become paired
CCW/CW entries appended on a row below the layout.

### Lenient JSON
Several keyboard.json files in the wild contain `//` comments, trailing
commas, or missing commas — the loader repairs all of these.

### Not derivable from keyboard.json (by design)
Key colors `c`, decals `d`, stepped-key props `w2/h2/x2/y2`, layout-option
labels/placement, custom display names. Byte-identical output vs.
hand-authored files is impossible; **functional equivalence** (geometry +
matrix labels + encoders + matrix size) is what the test suite verifies.

---

## Testing

Run the full regression suite (reads vial-qmk read-only, writes nothing
there):

```bash
python ..\vial-research\test_all_pairs.py            # summary
python ..\vial-research\test_all_pairs.py --verbose  # per-keyboard notes
```

Current result:

```
RESULTS: 504 / 504 passed (100.0%)   [47 passed with documented notes]
```

18 reference vial.json files carry verified hand-authored discrepancies
(stale matrix numbering, PCB keys absent from every keyboard.json layout,
bottom-up row numbering, etc.) — documented per keyboard in
`KNOWN_DISCREPANCIES` inside `test_all_pairs.py`.

See `..\vial-research\docs\KLE_FORMAT_FIX_2026-07.md` for the full
write-up of the format research and the rewrite.

---

## Safety

- The coordinator **refuses to write inside any path containing
  `vial-qmk`** unless `--allow-vial-qmk` is passed.
- Always back up an existing `keymaps/vial/` folder before overwriting.

---

*Last Updated: July 2026 — converter rewritten to correct KLE format;
504/504 regression pass.*