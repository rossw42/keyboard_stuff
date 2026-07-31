# QMK → Vial Porting Script

Point it at a QMK keyboard directory, get back a complete, buildable
`keymaps/vial/` folder — `vial.json`, `config.h`, `rules.mk`, `keymap.c`,
and a README. I hated hand-writing KLE JSON for hours. I lost track of matrix columns and positions so many times.
This just works, because it was tested against every single keyboard in the vial-qmk repo until it did.

I have recently converted the following boards with this script:

```
keyhive/opus
eggsworks/tamagov2
eggsworks/egg58
wilba_tech/wt60_d
peej/lumberjack
splitkb/kyria_rev1
```

For how it works internally, see [TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md).
For the frankly excessive research behind it, see
[Methodology & Research](#methodology--research) below.

---

## Usage

```bash
# Write to a separate output directory (keeps your source tree clean)
python qmk_to_vial_porting.py "path\to\my_keyboard" "path\to\output"

# Write directly into the keyboard directory (creates keymaps/vial/ in place)
# use --allow-vial-qmk to override
python qmk_to_vial_porting.py "path\to\my_keyboard" --allow-vial-qmk

# Disable layout-option derivation (always emit just the first layout)
python qmk_to_vial_porting.py "path\to\my_keyboard" "out" --no-layout-options
```

Example:

```bash
python qmk_to_vial_porting.py "D:\GitHub2\vial-qmk\keyboards\eggsworks\tamago" "output"
```

Output:

```
output\eggsworks_tamago\keymaps\vial\
├── vial.json     # Vial layout definition (real KLE format, encoders and all)
├── config.h      # Vial UID + unlock combo
├── rules.mk      # VIA/VIAL build flags
├── keymap.c      # copied from the keyboard's default keymap
└── README.md     # build instructions (yes, the output has its own README)
```

That's it. Five files, zero guesswork.

---

## Using the Output

1. Copy the generated `keymaps\vial\` folder into the keyboard's directory
   in your vial-qmk tree. (Back up any existing `keymaps\vial\` first —
   future you will thank present you.)
2. Build and flash:

```bash
make <keyboard>:vial          # e.g. make eggsworks/tamago:vial
make <keyboard>:vial:flash
```

3. Open the board in [Vial](https://get.vial.today/) and remap to your
   heart's content. No recompiling. That's the whole point.

---

## Layout Options (multiple layouts)

When a `keyboard.json` defines **multiple layout macros** (e.g.
`LAYOUT_60_ansi`, `LAYOUT_60_iso`, `LAYOUT_60_ansi_split_bs_rshift`), the
converter now derives real **Vial layout options** — the dropdowns/checkboxes
in the Vial GUI's Layouts pane (`layouts.labels` + per-key `"row,col\n\n\ng,c"`
tags in the KLE keymap). Alternative choices are drawn below the board, exactly
like hand-made vial.json files; the Vial GUI re-anchors them onto the default
keys automatically.

**Accuracy guarantee:** options are only emitted when the generated file passes
a built-in validator that simulates the Vial GUI's rendering (bounding-box
re-anchoring of the selected choice) and proves that **every layout macro in
keyboard.json is reproduced exactly** — matrix ids and absolute
x/y/w/h/rotation — by some combination of option choices. If that proof fails
for any macro, the converter silently falls back to the previous single-layout
behavior. There is no "almost right" output.

Verified across the full vial-qmk keyboards tree (`test_layout_options.py`):
3,967 boards, 1,467 multi-layout, **1,384 got provably-exact options,
83 fell back, 0 failures**. When derived options need more than VIA's default
1 byte of EEPROM (bitfield > 8 bits), the generated `config.h` includes
`VIA_EEPROM_LAYOUT_OPTIONS_SIZE` automatically.

Caveats (by design):

- Option/choice **names** are heuristic ("Backspace: 2u/Split", "Bottom Row:
  6.25u Space/7u Space", or generic "Option 1/2") — geometry and key
  membership are exact, the *text* is cosmetic and easy to hand-edit in the
  generated vial.json.
- The default (choice 0) is the plainest-named macro (honoring
  `layout_aliases.LAYOUT`), which may differ from what a human author would
  pick — also cosmetic.
- Only combinations asserted by keyboard.json macros are proven; like
  hand-made files, the option lattice may allow extra combinations, which is
  harmless (Vial addresses keys by matrix position).

Research backing this feature lives in [research/](research/):
`vial_layout_options_format.md`, `vial_gui_option_rendering.md`,
`multi_layout_diff_analysis.md`.

---

## Notes

- Handles keyboards using `keyboard.json` **or** `info.json`, including
  multi-level configs (parent/child directories), split keyboards, and
  rotary encoders.
- Also survives QMK JSON files containing `//` comments, trailing commas,
  and the occasional *missing* comma. (Yes, those exist in the wild. Yes,
  we were surprised too.)
- If the keyboard has no `keymaps/default/keymap.c`, a stub `keymap.c` is
  generated — edit it before building, or enjoy a keyboard that types
  nothing very reliably.
- `config.h` `MATRIX_ROWS/COLS` parsing understands product expressions
  like `6*2` (split boards such as viktus/sp111).
- Validated against **504 real keyboards** from the vial-qmk repository
  (100% pass), plus 11/11 byte-exact via keymaps and 2,092 historical QMK
  via keymaps, plus the 3,967-board layout-options regression
  (`test_layout_options.py`, 0 failures). Details in
  [TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md).

---

## Methodology & Research

This converter was not written from a spec, because **no spec exists** for
how `keyboard.json` maps to `vial.json` or to a VIA/Vial keymap. Every rule
in it was **reverse-engineered from real firmware repositories and verified
against ground truth with a 100%-match standard**. In other words: we
didn't guess, we cross-examined 2,600 keyboards until they confessed.

### Campaign 1 — vial.json format (504 keyboard pairs)

**Question:** How does Vial's `vial.json` derive from QMK's `keyboard.json`?

**Method:**

1. Scanned the entire vial-qmk repo and built a CSV of every
   `keyboard.json` ↔ `keymaps/vial/vial.json` pair (504 pairs,
   `vial_keyboard_pairs.csv`).
2. Diffed generated output against every real file, categorized every
   mismatch, fixed the converter, and repeated until all pairs passed.

**Key discoveries** (each one found by a failing comparison, not by
documentation — again, there is no documentation):

- `layouts.keymap` is a genuine **KLE (keyboard-layout-editor) serialized
  document** — rows of relative offsets, not absolute coordinates. Earlier
  attempts that emitted absolute x/y rendered a beautiful, perfectly valid
  layout of exactly zero keys in Vial.
- KLE parsers inherit a JavaScript quirk: `r`/`rx`/`ry` values of **0 are
  falsy and ignored**, so rotation state must never be "reset to zero" —
  rotation clusters must be emitted in an order that only increases.
  (JavaScript strikes again, even in a Python project.)
- Encoders are keys whose legend line 9 is `"e"` and whose label is
  `encoderIndex,direction` — not a matrix coordinate.
- The electrical matrix comes from a **priority chain**: `config.h`
  `MATRIX_ROWS/COLS` (authoritative for custom matrices) → `matrix_pins`
  (rows doubled for splits, direct-pin supported) → layout maximums, with
  transposed-matrix detection (e.g. planck rev6's 4×12 pins wired as 8×6).
- QMK definitions are **layered**: leaf `keyboard.json` inherits from parent
  `info.json` files, so the loader deep-merges the whole directory chain.

**Result:** validated against all 504 real keyboards (100% pass).

### Campaign 2 — keymaps/via/keymap.c in vial-qmk (11 files, 100% byte-exact)

**Question:** Given a `keyboard.json`, how do you get to the board's
`keymaps/via/keymap.c`?

**Method:** the pairs CSV was extended with a `via_keymap.c` column; every
via keymap was diffed against its board's `default` keymap and against
**git history** (blob-hash matching against every historical revision of
the default keymap).

**Core rule discovered:**

> `keymaps/via/keymap.c` = a copy of `keymaps/default/keymap.c`.
> VIA needs no C changes — it's enabled purely in `rules.mk`; the keymap is
> just the factory default, which VIA overrides at runtime from EEPROM.

Every divergence was explained and captured as a byte-exact patch:
frozen historical snapshots (proven via git — the via blob equals an old
default blob from before the `RESET`→`QK_BOOT` rename), whitespace drift,
and tiny author edits.

**11/11 boards generated 100% byte-identical.**

### Campaign 3 — keymaps/via/keymap.c in QMK proper (2,092 files via git archaeology)

**Question:** Does the vial-qmk rule hold at real scale?

**Obstacle:** current QMK master contains **zero** via keymaps — PR #24322
deleted all of them in Aug 2024. Solution: all 2,092 files were recovered
from git history at ref `45dc2499dc~1` using read-only git plumbing
(`ls-tree` + `cat-file --batch`), letting ~3,500 file blobs be compared in
seconds without a checkout. Git remembers everything. Git *forgives*
nothing.

**Findings at scale (2,092 boards, `qmk_via_keymap_pairs.csv`):**


| Rule                                               | Boards    | %         |
| -------------------------------------------------- | --------- | --------- |
| via = copy of default (token-level)                | 774       | 37.0%     |
| via = default + transparent padding layers         | 507       | 24.2%     |
| truncation / era-keycode drift                     | 8         | 0.4%      |
| **Mechanically derivable (100% functional match)** | **1,289** | **61.6%** |
| genuine human-authored edits                       | 739       | 35.3%     |

- **The 4-layer convention is proven, not assumed:** of boards that add
  layers, 90% land on exactly **4** — VIA's `DYNAMIC_KEYMAP_LAYER_COUNT`
  default. Padding layers are all-transparent and mirror the base layer's
  formatting.
- **Byte-exact matching was achieved for every board where a deterministic
  rule exists** (600 boards / 28.7%); beyond that, ~2,000 different authors'
  whitespace makes byte-identity information-theoretically impossible, so
  the remaining matches are verified at the token level
  (compilation-equivalent keymaps).
- The vial-qmk "frozen snapshot" rule does *not* generalize (1/1,504) —
  confirming vial-qmk's via folders are pre-removal leftovers, while QMK's
  were independently authored.

**Result:** the converter's keymap policy — *copy default, pad with
transparent layers to 4* — reproduces what real keyboard authors actually
did for 61.6% of 2,092 boards, and is the correct scaffold for the rest.

### Campaign 4 — Layout options from multi-layout keyboard.json (3,967 boards)

**Question:** Can Vial's GUI layout options (ISO/ANSI, split backspace,
bottom-row variants...) be derived from a keyboard.json with multiple layout
macros — accurately enough to ship?

**Method:**

1. Reverse-engineered the option encoding from 293 real vial.json files with
   `layouts.labels` (`research/vial_layout_options_format.md`): defaults carry
   explicit `g,0` tags (280/293), alternates reuse matrix coords when
   electrically identical, and are drawn beside/below the board.
2. Read the actual vial-gui source (`research/vial_gui_option_rendering.md`)
   to learn the rendering contract: the GUI shows only the selected choice per
   group and **rigidly translates it so its collective bounding-box top-left
   snaps onto choice 0's** — meaning alternates can live anywhere in the KLE,
   but every group needs an in-place choice-0 and consistent group anchors.
3. Proved on hand-made files (`research/multi_layout_diff_analysis.md`) that
   option membership is a geometric diff between layout macros (same matrix id
   + same geometry = common key; leftovers cluster into option regions), while
   names/ordering are editorial.
4. Implemented diff → cluster → merge → anchor-stabilize → emit
   (`layout_options.py`), then closed the loop with a validator that
   re-parses the final KLE, **simulates the GUI re-anchoring, and requires
   every keyboard.json macro to be reproduced exactly** by some choice
   combination. No proof, no options — the converter falls back to the old
   single-layout output.

**Result:** `test_layout_options.py` over every keyboard.json in vial-qmk:
3,967 boards, 1,384 with provably-exact options, 83 clean fallbacks,
**0 failures**. The single failure found along the way was a pre-existing
matrix-size bug (`MATRIX_ROWS 6*2` parsed as 6) — fixed.

### The methodology in one sentence

> Build a ground-truth corpus of real file pairs, generate candidates,
> **accept only 100% matches**, explain every failure, encode the
> explanation as a rule, and repeat until the failures are provably
> human-authored content rather than missing rules.

All research was performed strictly read-only against the source
repositories. No keyboards were harmed in the making of this converter.

---

*Last Updated: July 2026 (layout options added)*
