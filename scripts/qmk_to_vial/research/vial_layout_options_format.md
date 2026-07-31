# vial.json Layout Options -- Authoritative Format Specification

Researched read-only from D:\GitHub2\vial-qmk (vial-kb/vial-qmk, commit 8af085df). Survey covers all 659 vial.json files under keyboards/.

## 0. Corpus statistics

- 659 vial.json files total.
- 293 contain a layouts.labels key; 284 are non-empty; 9 are literally empty [].
- Of the 284 non-empty label sets: 86 use only string (checkbox) entries, 70 use only array (multi-choice) entries, 128 mix both.
- 183 boards pair labels with a multi-layout keyboard.json; 76 boards have labels even though keyboard.json defines a single layout macro (typically a LAYOUT_all-style grid); the rest could not be resolved to a keyboard.json with layouts by walking up the tree (data elsewhere).

---

## 1. The labels array format

Located at layouts.labels in vial.json. Two entry kinds:

- A plain STRING entry defines a boolean checkbox option (unchecked = choice 0 = default, checked = choice 1).
- An ARRAY entry defines a multi-choice dropdown: [title, choice0name, choice1name, ...]. The first element is the UI title; remaining elements name choices 0..N-1 in order. Choice 0 is the default.

### Real example 1 -- single checkbox (keyboards/contra/keymaps/vial/vial.json)

```json
"layouts": {
    "labels": [
        "2u Space"
    ],
```

### Real example 2 -- all multi-choice (keyboards/cannonkeys/an_c/keymaps/vial/vial.json)

```json
"layouts": {
    "labels": [
        ["Backspace", "Full", "Split"],
        ["Right Shift", "Full", "Split"],
        ["Bottom Row", "6.25u", "7u"]
    ],
```

### Real example 3 -- mixed, including a 3-way choice (keyboards/42keebs/mysterium/keymaps/vial/vial.json)

```json
"labels": [
    ["Bottom Row", "6.25U", "7U", "Winkeyless"],
    "ISO Enter",
    "Split Left Shift",
    "Split Backspace",
    "Split Right Shift"
],
```

Bit packing (vial-gui layout_editor.py): a checkbox packs to exactly 1 bit; an N-choice dropdown packs to (N-1).bit_length() bits (2 choices = 1 bit, 3-4 choices = 2 bits, 5-8 = 3 bits). Per-option bit strings are concatenated in labels order, first label in the most significant bits, then the whole thing is sent as a big-endian uint32 (VIA layout options value).

---

## 2. Key label suffix format

Each key in layouts.keymap is a KLE legend string. Splitting the raw legend on \\n:

- split index 0 (first legend line): "row,col" -- the matrix position.
- split index 3 (fourth legend line): "g,c" -- the layout-option suffix, where g = 0-based index into the labels array (the option group) and c = 0-based choice index within that group. With default KLE alignment a=4, raw index 3 maps to aligned labels[8] (bottom-right), which is exactly what vial-gui parses in keyboard_comm.py: if key.labels[8]: idx, opt = key.labels[8].split(",").
- Keys with no suffix are common keys, visible in every option combination.

So a full option key looks like:

```json
"3,5\\n\\n\\n0,0"
```

meaning matrix (3,5), option group 0, choice 0.

### Defaults carry an explicit "g,0" suffix

Statistic from this repo: of the 293 vial.json files with a labels key, 280 (280/293) attach an explicit "g,0" suffix to every key of the DEFAULT choice of every option group they actually reference. The default choice is NOT left unsuffixed -- default keys are labelled "g,0" and alternates "g,1", "g,2", etc. This is required by vial-gui: place_widgets() anchors every non-zero choice group onto the bounding box of the choice-0 group of the same index; a group with no choice-0 keys gets a garbage 1e6 anchor.

### The 13 exceptions

- 9 boards declare labels as an empty array [] (no options at all): hhkb/ansi, hhkb/yang, keychron/c3_pro/ansi/red, keyten/aperture, lily58/rev1, monsgeek/m3, rgbkb/mun2, sofle_pico, tominabox1/adalyn.
- 3 boards declare label entries but no key in the keymap carries any option suffix (the options are dead UI): ingenieurrr (5 labels), kprepublic/bm40hsrgb (1 label), preonic/rev3_drop (1 label).
- 1 board is malformed: rainkeebs/twoyo puts the default suffix on the wrong legend line ("6,4\\n0,0" -- split index 1 instead of 3) while alternates are correct ("6,4\\n\\n\\n0,1"); the group therefore has no valid choice-0 anchor.

Two further boards (mechlovin/adelais/rgb_led/rev3 and nachie/littlewritter) declare MORE label entries than option groups actually referenced by keys, but every group they do reference has proper "g,0" defaults, so they are counted compliant.

GENERATOR RULE: always emit an explicit "g,0" suffix on every key of the default choice of every group, and reference every declared label entry at least once.

---

## 3. Alternative key placement conventions

vial-gui re-anchors each selected non-default choice group by rigid translation: the collective bounding-box top-left of the chosen group is snapped onto the bounding-box top-left of the choice-0 group of the same index. Therefore alternates are drawn OUTSIDE the main layout (extra row below, or offset to the right of the row) and only their internal relative geometry matters.

### (a) Bottom-row / spacebar option (checkbox, ortho) -- keyboards/contra/keymaps/vial/vial.json

Labels: ["2u Space"]. Choice 0 (checked semantics: 2u space IS the default here) sits in the bottom row in place; choice 1 (two 1u keys) is an extra KLE row below, x-offset to sit visually under the spacebar:

```json
[
    "3,0", "3,1", "3,2", "3,3", "3,4",
    {"w": 2}, "3,5\\n\\n\\n0,0",
    "3,7", "3,8", "3,9", "3,10", "3,11"
],
[
    {"x": 5}, "3,5\\n\\n\\n0,1", "3,6\\n\\n\\n0,1"
]
```

Pattern: default in place; alternates on a new row directly below (no y gap here), x pushed to the position under the default group so the editing view lines up. The x offset is cosmetic.

### (a2) Bottom-row multi-choice (dropdown) -- keyboards/dm9records/plaid/keymaps/vial/vial.json

Labels: [["Bottom Row", "Grid", "MIT"]]. Grid (choice 0) is in place as two 1u keys; MIT (choice 1) is a single 2u key on an extra row below:

```json
[
    "3,0", "3,1", "3,2", "3,3", "3,4",
    { "c": "#777777" }, "3,5\\n\\n\\n0,0", "3,6\\n\\n\\n0,0",
    { "c": "#cccccc" }, "3,7", "3,8", "3,9", "3,10", "3,11"
],
[{ "x": 5, "c": "#777777", "w": 2 }, "3,5\\n\\n\\n0,1"]
```

### (b) Split backspace -- keyboards/cannonkeys/an_c/keymaps/vial/vial.json

Here the alternate group is placed ABOVE the board; the main layout then starts at y 0.75. Split pair x-aligned over the default 2u backspace at x=13:

```json
[{"x": 13}, "0,13\\n\\n\\n0,1", "0,14\\n\\n\\n0,1"],
[
    {"y": 0.75},
    "0,0", "0,1", "0,2", "0,3", "0,4", "0,5", "0,6", "0,7",
    "0,8", "0,9", "0,10", "0,11", "0,12",
    {"w": 2}, "0,13\\n\\n\\n0,0"
],
```

### (b2) Split backspace to the RIGHT of the row -- keyboards/42keebs/mysterium/keymaps/vial/vial.json

The alternate split pair is appended after the end of the same KLE row with an x gap of 0.5:

```json
[
    ...,
    {"c": "#aaaaaa", "w": 2}, "1,13\\n\\n\\n3,0",
    {"x": 0.25}, "1,15", "1,16", "1,17",
    {"x": 0.5}, "1,13\\n\\n\\n3,1", "1,14\\n\\n\\n3,1"
],
```

### (c) ISO Enter (x2/y2/w2 stepped shape) and split right shift

ISO Enter alternates use the KLE second-rectangle properties w2/h2/x2 to draw the stepped shape, and are placed to the right of the row that contains the default ANSI enter. From keyboards/cannonkeys/bastion60/keymaps/vial/vial.json (a 60% with ISO enter; labels: ["Split Backspace","ISO Enter","Split Left Shift","Split Right Shift",["Bottom Row","6.25U","7U WKL","7U HHKB","Split Space"]]):

```json
[
    {"w": 1.5}, "1,0", "1,1", "1,2", "1,3", "1,4", "1,5", "1,6",
    "1,7", "1,8", "1,9", "1,10", "1,11", "1,12",
    {"c": "#aaaaaa", "w": 1.5}, "1,13\\n\\n\\n1,0",
    {"x": 1.25, "c": "#777777", "w": 1.25, "h": 2, "w2": 1.5, "h2": 1, "x2": -0.25}, "2,13\\n\\n\\n1,1"
],
[
    {"c": "#aaaaaa", "w": 1.75}, "2,0", {"c": "#cccccc"}, "2,1", "2,2", "2,3", "2,4",
    "2,5", "2,6", "2,7", "2,8", "2,9", "2,10", "2,11",
    {"c": "#777777", "w": 2.25}, "2,13\\n\\n\\n1,0",
    {"x": 0.25, "c": "#aaaaaa"}, "1,13\\n\\n\\n1,1"
],
```

Notes: the ISO Enter group (1,1) consists of TWO keys spread over two KLE rows: the stepped enter (h 2, w 1.25 plus second rect w2 1.5, x2 -0.25) hung off the tab row at x gap 1.25, and the extra 1u key (the ANSI backslash position moves) appended after the caps row at x gap 0.25. The ANSI group (1,0) is the in-place 1.5u backslash "1,13" plus the 2.25u enter "2,13". Note the matrix swap: ISO enter reuses matrix coord 2,13 (the ANSI enter coord) and the relocated key reuses 1,13 (the ANSI backslash coord).

Split right shift (an_c, group 1): default 2.75u in place, split pair appended right on the same row with x gap 0.75:

```json
{"w": 2.75}, "3,11\\n\\n\\n1,0",
{"x": 0.75, "w": 1.75}, "3,11\\n\\n\\n1,1", "3,14\\n\\n\\n1,1"
```

### (d) Multi-choice bottom row (3 or more choices) -- keyboards/42keebs/mysterium/keymaps/vial/vial.json

Group 0 = ["Bottom Row", "6.25U", "7U", "Winkeyless"]. Choice 0 is the real bottom row in place; each further choice is its own full KLE row stacked below, the first alternate separated by y 0.25:

```json
[
    {"x": 2.5, "w": 1.25}, "5,0\\n\\n\\n0,0", {"w": 1.25}, "5,1\\n\\n\\n0,0", {"w": 1.25}, "5,2\\n\\n\\n0,0",
    {"c": "#cccccc", "w": 6.25}, "5,6\\n\\n\\n0,0",
    {"c": "#aaaaaa", "w": 1.25}, "5,9\\n\\n\\n0,0", {"w": 1.25}, "5,10\\n\\n\\n0,0",
    {"w": 1.25}, "5,12\\n\\n\\n0,0", {"w": 1.25}, "5,14\\n\\n\\n0,0",
    {"x": 0.25}, "5,15", "5,16", "5,17"
],
[
    {"y": 0.25, "x": 2.5, "w": 1.5}, "5,0\\n\\n\\n0,1", "5,1\\n\\n\\n0,1", {"w": 1.5}, "5,2\\n\\n\\n0,1",
    {"c": "#cccccc", "w": 7}, "5,6\\n\\n\\n0,1",
    {"c": "#aaaaaa", "w": 1.5}, "5,10\\n\\n\\n0,1", "5,12\\n\\n\\n0,1", {"w": 1.5}, "5,14\\n\\n\\n0,1"
],
[
    {"x": 2.5, "w": 1.5}, "5,0\\n\\n\\n0,2",
    {"x": 1, "w": 1.5}, "5,2\\n\\n\\n0,2",
    {"c": "#cccccc", "w": 7}, "5,6\\n\\n\\n0,2",
    {"c": "#aaaaaa", "w": 1.5}, "5,10\\n\\n\\n0,2",
    {"x": 1, "w": 1.5}, "5,14\\n\\n\\n0,2"
]
```

### Placement pattern summary

- Default (choice 0) keys ALWAYS sit in their true position inside the main layout, with explicit g,0 suffixes.
- Alternates for horizontal-slice options (bottom row, spacebar) go on extra KLE rows directly below the board, usually with a y gap of 0.25 (sometimes 0) and an x offset matching the default group x so the picture lines up. Multi-choice groups stack one row per choice, in choice order.
- Alternates for single-key or small-cluster options within a row (split backspace, split right shift, ISO enter, relocated backslash) are appended to the RIGHT end of the same KLE row, after an x gap of 0.25 to 1.25 (0.25, 0.5, 0.75 and 1.25 all observed).
- Some boards instead put small alternates ABOVE the board (an_c split backspace) and push the main layout down with y 0.75.
- The absolute position of an alternate group is cosmetic; vial-gui translates the whole group so its bounding-box top-left matches the choice-0 group bounding-box top-left. Internal relative geometry of each group must be exact.
- A quirk worth knowing: coseyfannitutti/mysterium duplicates common home-row keys (3,1..3,11, same matrix coords, suffix 1,1) inside its ISO Enter group so the ISO group bounding box gets the same top-left as the ANSI group; after re-anchoring the duplicates overlay the common keys exactly. Decal keys with a suffix are the cleaner VIA trick for padding a group bounding box.

---

## 4. Matrix coordinate reuse between choices

Confirmed convention: a key that is ELECTRICALLY THE SAME switch position in a different physical shape reuses the same row,col in every choice; keys that only exist in some choices get their own distinct coords.

- contra: 2u space "3,5\\n\\n\\n0,0" vs split "3,5\\n\\n\\n0,1" + "3,6\\n\\n\\n0,1" -- left split key reuses 3,5; the extra right key is 3,6.
- dm9records/plaid: grid "3,5\\n\\n\\n0,0" + "3,6\\n\\n\\n0,0" vs MIT 2u "3,5\\n\\n\\n0,1" -- the 2u key reuses 3,5; 3,6 simply does not exist in the MIT choice.
- cannonkeys/an_c backspace: 2u "0,13\\n\\n\\n0,0" vs split "0,13\\n\\n\\n0,1" + "0,14\\n\\n\\n0,1".
- cannonkeys/an_c right shift: 2.75u "3,11\\n\\n\\n1,0" vs 1.75u "3,11\\n\\n\\n1,1" + 1u "3,14\\n\\n\\n1,1".
- cannonkeys/an_c bottom row: 6.25u choice uses 4,0 4,1 4,2 4,5 4,9 4,10 4,11 4,14; the 7u choice reuses the same coords but simply omits 4,9 (one fewer key).
- ISO enter: reuses the ANSI enter coord (bastion60 and both mysteriums use 2,13 for both ANSI enter and ISO enter); the 1u key displaced by the ISO shape reuses the ANSI backslash coord (1,13).

Distinct coords are only used when the alternate genuinely adds a switch that the default does not have (split halves, extra 1u keys). This matches how the LAYOUT_all/LAYOUT_xxx C macros share matrix positions in keyboard.json.

---

## 5. Relationship to keyboard.json layout macros (3 boards verified programmatically)

Method: for each board, the set of (row,col) matrix coords was extracted from every keyboard.json layout macro and compared with (i) the union of all vial.json keys and (ii) the per-choice key subsets (common keys plus the keys of a given choice of each group).

### contra (keyboards/contra/keyboard.json)

- Macros: LAYOUT_ortho_4x12 (48 keys), LAYOUT_planck_mit (47 keys).
- Union of all vial keys = 48 coords = exactly LAYOUT_ortho_4x12 (the superset macro).
- Choice 0 of "2u Space" (the 2u spacebar) key set == LAYOUT_planck_mit exactly.
- Choice 1 (two 1u keys) key set == LAYOUT_ortho_4x12 exactly.
- Note: choice 0 here is MIT, i.e. the vial default is not necessarily the first/alphabetical macro.

### dm9records/plaid (keyboards/dm9records/plaid/keyboard.json)

- Macros: LAYOUT_planck_mit (47), LAYOUT_ortho_4x12 (48).
- Union == LAYOUT_ortho_4x12 exactly; choice Grid == LAYOUT_ortho_4x12; choice MIT == LAYOUT_planck_mit. Perfect 1:1 macro-to-choice mapping.

### cannonkeys/an_c (keyboards/cannonkeys/an_c/keyboard.json)

- Macros: LAYOUT_60_ansi (61), LAYOUT_60_ansi_tsangan_split_bs_rshift (62), LAYOUT_all (63).
- Union of all vial keys (63 dedup coords) == LAYOUT_all exactly.
- All-defaults key set (choice 0 everywhere) == LAYOUT_60_ansi exactly.
- Choosing Split Backspace + Split Right Shift + 7u Bottom Row (choice 1 in all three groups) == LAYOUT_60_ansi_tsangan_split_bs_rshift exactly.
- So specific option combinations reproduce specific macros, but the three binary groups generate 8 combinations while only 3 macros exist; vial options are finer-grained than the macro list.

### bonus: coseyfannitutti/mysterium

- Macros: LAYOUT_tkl_ansi (87), LAYOUT_tkl_ansi_7u (86), LAYOUT_tkl_iso (88), LAYOUT_tkl_iso_7u (87).
- Union of vial keys (88) == LAYOUT_tkl_iso (there is no LAYOUT_all; the ISO macro happens to be the superset).
- All-defaults key set == LAYOUT_tkl_ansi exactly.

Takeaway for a generator: the union of all vial option keys should equal the superset macro (LAYOUT_all when it exists, otherwise the largest macro), the all-defaults subset should equal the default macro, and each per-choice subset should correspond to the matching macro region when a matching macro exists. But vial options may legitimately express combinations that have no dedicated macro.

---

## 6. Encoder label format and options on encoders

An encoder key uses the raw KLE legend "i,d" on split index 0 (i = encoder index, d = direction 0/1) and the letter "e" on split index 9 (tenth legend line):

```json
"0,0\\n\\n\\n\\n\\n\\n\\n\\n\\ne"
```

vial-gui detects encoders via aligned labels[4] == "e" (raw index 9 maps to aligned centre slot) and reads idx,direction from labels[0].

Encoders DO carry option suffixes, and commonly: in this repo 155 boards have encoder keys and 305 encoder keys carry an option suffix on split index 3, exactly like normal keys:

```json
"0,0\\n\\n\\n5,1\\n\\n\\n\\n\\n\\ne"
```

(keyboards/42keebs/discipline/keymaps/vial/vial.json -- encoder shown only when checkbox group 5 "Encoder" is enabled). Other examples: 1upkeyboards/pi60 uses "0,14\\n\\n\\n0,2\\n...\\ne" (encoder is choice 2 of the Backspace group), boardsource/lulu, jlw/vault35_universal, 42keebs/basketweave_s all gate encoders behind option groups.

So the full 10-line encoder-with-option legend is: "i,d\\n\\n\\ng,c\\n\\n\\n\\n\\n\\ne".

---

## 7. Multi-layout keyboard.json with NO vial labels

19 of the 202 vial boards whose keyboard.json defines 2 or more layout macros ship a vial.json with no labels at all (about 9 percent) -- they simply drew one fixed layout: annepro2, beekeeb/piantor, boston, bpiphany/frosty_flake, cannonkeys/rekt1800, converter/adb_usb, crkbd, ergodox_ez/base, kbdfans/odinmini, kbdfans/tiger80, keychron/k1_pro/iso/rgb, keychron/q11/ansi_encoder, keychron/q11/iso_encoder, keyhive/lattice60, mechwild/clunker (11 macros!), mt/split75, preonic/rev1, sharkoon/skiller_sgk50_s2, wilba_tech/wt60_d (10 macros).

So layout options are the norm for multi-layout boards (183/202 about 91 percent) but a generator may legitimately fall back to picking one layout when option synthesis is impossible.

---

## 8. Generator checklist

1. labels: string per boolean option, [title, name0, name1, ...] per multi-choice; order defines the option bitfield (first label = most significant bits).
2. Every key: "row,col" on legend line 1; option keys add "g,c" on legend line 4 (raw split index 3).
3. Emit explicit "g,0" on ALL default-choice keys; never leave the default choice unsuffixed; every label entry must be referenced by at least one g,0 key.
4. Reuse matrix coords across choices for electrically identical switches; give genuinely extra switches their own coords; the union of all choices should cover the superset macro key set.
5. Place choice-0 keys in their real positions; place each alternate choice as a compact block below the board (y gap 0.25, one KLE row per choice, x-aligned under the default group) or to the right of its row (x gap 0.25-1.25) -- position is cosmetic, internal geometry is not.
6. ISO enter: single key with w 1.25, h 2, w2 1.5, h2 1, x2 -0.25, reusing the ANSI enter matrix coord; pair it with the relocated 1u key reusing the ANSI backslash coord in the same option group.
7. Encoders: "i,d" plus "e" on legend line 10; add "g,c" on line 4 to gate an encoder behind an option.


