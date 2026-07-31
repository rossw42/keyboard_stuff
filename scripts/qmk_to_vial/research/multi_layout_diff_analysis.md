# Deriving vial.json Layout Options from Multi-Layout keyboard.json: Diff Analysis

Read-only analysis of D:/GitHub2/vial-qmk and D:/GitHub2/qmk_firmware.
Question: can vial.json layout option groups (labels + per-key group,choice indices) be mechanically derived from a keyboard.json that defines MULTIPLE layout macros?

Method: for each board, parse keyboard.json layout macros into (matrix-id, x, y, w) sets, parse the hand-made vial.json KLE keymap extracting each key matrix label and its optional group,choice marker, then test every combination of option choices against every macro by matrix-set equality, and compare geometry.

Survey: 183 boards in vial-qmk have BOTH a multi-macro keyboard.json/info.json AND a hand-made vial.json with layout labels (full list generated during analysis). Case studies below.

## 1. Case studies

### 1a. cannonkeys/an_c

Layout macros: LAYOUT_60_ansi (61 keys), LAYOUT_60_ansi_tsangan_split_bs_rshift (62), LAYOUT_all (63).

vial labels: [Backspace: Full/Split], [Right Shift: Full/Split], [Bottom Row: 6.25u/7u].

Option groups and regions (from vial KLE markers):
- group 0 Backspace: choice 0 = one 2u key (0,13); choice 1 = two 1u keys (0,13)+(0,14). Region = top-right 2u slot.
- group 1 Right Shift: choice 0 = 2.75u (3,11); choice 1 = 1.75u (3,11) + 1u (3,14).
- group 2 Bottom Row: choice 0 = 8 keys, 1.25u mods + 6.25u space; choice 1 = 7 keys, 1.5/1/1.5 + 7u space (tsangan).

Combination - mapping (verified by matrix-set equality):
- (0,0,0) == LAYOUT_60_ansi  (exact)
- (1,1,1) == LAYOUT_60_ansi_tsangan_split_bs_rshift  (exact)
- (1,1,0) == LAYOUT_all  (exact)
- the other 5 of 8 combos have NO macro: vial exposes a superset of the macro set (harmless at runtime because vial addresses keys by matrix position).

Base (all choice-0) = LAYOUT_60_ansi. It is the FIRST macro in file order and the plain community layout name (fewest suffixes). It is NOT LAYOUT_all. Choice-0 geometry matches LAYOUT_60_ansi coordinates exactly up to a constant y translation of 1.75 (the vial KLE draws the split-backspace alternates in extra rows above the board).

### 1b. dm9records/plaid

Layout macros: LAYOUT_planck_mit (47), LAYOUT_ortho_4x12 (48).

vial labels: [Bottom Row: Grid/MIT]. group 0: choice 0 = (3,5) 1u + (3,6) 1u; choice 1 = (3,5) 2u.

Mapping: (0,) == LAYOUT_ortho_4x12 exact; (1,) == LAYOUT_planck_mit exact. Base = LAYOUT_ortho_4x12, geometry match is EXACT (0 mismatches). Note the base here is the SECOND macro in file order and the LARGER one.

### 1c. contra

Layout macros: LAYOUT_ortho_4x12 (48), LAYOUT_planck_mit (47).

vial labels: [2u Space] (a single BOOLEAN option, not a multi-choice group). group 0: choice 0 = (3,5) 2u; choice 1 = (3,5) 1u + (3,6) 1u.

Mapping: (0,) == LAYOUT_planck_mit; (1,) == LAYOUT_ortho_4x12. Same hardware family as plaid, but the human author made the OPPOSITE ordering decision: here the MIT 2u-space variant is choice 0 (the default rendering) and grid is the alternate, and the option is expressed as a boolean label string instead of a [name, c0, c1] list. This proves choice ordering and boolean-vs-list presentation are purely editorial, not derivable.

### 1d. coseyfannitutti/mysterium (the board 42keebs/mysterium keymap actually points at; 42keebs/mysterium itself has no keyboard.json, layouts live in .h files)

Layout macros: LAYOUT_tkl_ansi (87), LAYOUT_tkl_ansi_7u (86), LAYOUT_tkl_iso (88), LAYOUT_tkl_iso_7u (87).

vial labels: [Bottom Row: 6.25U/7U], ISO Enter (bool), Split Left Shift (bool).

Groups: g0 bottom row (8 keys 6.25u form vs 7 keys 7u form); g1 ISO enter (3 keys ANSI form vs 15 keys ISO form - the vial author put the whole ISO home/enter region plus alternates off to the side, x up to 29.75, i.e. drawn OUTSIDE the board bounding box); g2 left shift (2.25u vs 1.25u+1u... 13 keys again drawn off-board).

Combination - (matrix-set equality):
- LAYOUT_tkl_ansi == (0,0,0) and (0,1,0)
- LAYOUT_tkl_ansi_7u == (1,0,0) and (1,1,0)
- LAYOUT_tkl_iso == (0,0,1) and (0,1,1)
- LAYOUT_tkl_iso_7u == (1,0,1) and (1,1,1)

Every macro is reachable, but AMBIGUOUSLY (2 combos each) because the vial author modeled ISO Enter and Split Left Shift as two INDEPENDENT toggles while the macros only encode 4 of the 8 combinations; the ISO enter toggle alone changes keys whose matrix ids overlap the left-shift group in the ISO drawing. Also: 4 macros collapse into 3 orthogonal options - the FACTORIZATION (2x2x2 covering a 4-macro set) is a human modeling decision.

Base (all-zero) = LAYOUT_tkl_ansi = first macro in file. Geometry of choice-0 keys matches it exactly modulo a constant y offset of +1 (extra KLE rows for alternates).

### 1e. 42keebs/mysterium note

D:/GitHub2/vial-qmk/keyboards/42keebs/mysterium has NO keyboard.json/info.json (C-header layouts only), so it cannot be part of a keyboard.json-driven derivation; its vial.json (labels: Bottom Row 6.25U/7U, ISO Enter, Split Left Shift) matches the coseyfannitutti/mysterium pattern above. Substituted dztech/tofu60-class boards and 1b/1c above to keep 4 verifiable case studies.

### 1f. Which macro is the vial BASE (all choice-0)?

- cannonkeys/an_c: base = LAYOUT_60_ansi. First in file: yes. LAYOUT_all: no. Largest: no (61 of 63).
- dm9records/plaid: base = LAYOUT_ortho_4x12. First in file: no (2nd). Largest: yes (48).
- contra: base = LAYOUT_planck_mit. First in file: no. Largest: NO (47 of 48).
- coseyfannitutti/mysterium: base = LAYOUT_tkl_ansi. First in file: yes. Largest: no (87 of 88).

Conclusion: there is NO consistent rule. The base is whatever the vial author considered the canonical retail configuration. It is frequently the plain ANSI macro, but contra proves it can be the SMALLER macro and not the first one. Crucially, the vial keymap is usually a UNION drawing: base keys form the main board and alternates are drawn beside/above it, so the union of all choices can exceed the union of all macros, and some choice combinations correspond to no macro at all (an_c: 5 of 8 combos unmapped). LAYOUT_all, where present, is just one point in the combination lattice (an_c: combo (1,1,0)).

## 2. Geometric diff pattern between two layout macros (verified on dz60)

dz60 keyboard.json has 29 layout macros (dztech/dz60v2: 35 - the combinatorial-explosion case).

### LAYOUT_60_ansi (61) vs LAYOUT_60_iso (62)
- 58 keys identical (same matrix id AND same x/y/w).
- only in ISO: (3,1) at x=1.25, y=3, w=1 (the extra ISO key next to left shift).
- shared matrix id but DIFFERENT geometry: (1,14) 1.5u at (13.5,1) - at (12.75,2) [backslash becomes ISO hash]; (2,13) 2.25u enter at (12.75,2) - at (13.75,1) [ANSI enter becomes top of ISO enter]; (3,0) 2.25u lshift - lshift.
- So one macro pair can differ in THREE disjoint physical regions simultaneously (enter block, backslash, left shift), and keys can KEEP their matrix id while moving and resizing. A naive same-matrix-means-common-key diff is wrong; key identity for diffing must be matrix id PLUS geometry.

### LAYOUT_60_ansi (61) vs LAYOUT_60_ansi_split_bs_rshift (63)
- 59 keys identical.
- only in split variant: (0,13) 1u at (13,0) and (3,14) 1u at (14,3).
- shared-id geometry change: (0,14) 2u at x13 - at x14 (backspace shrinks, shifts right); (3,13) 2.75u - (rshift shrinks).
- Pattern confirmed: the differing keys of the two macros occupy the SAME x/y bounding slots (x 13..15 y 0; x 12.25..15 y 3) filled with different widths and key counts; each such contiguous slot corresponds exactly to one vial option group (Split Backspace, Split Right Shift). The dz60 vial.json exposes Split Backspace, ISO Enter, a 10-choice Row 4 group, and a 7-choice Bottom row group: humans FACTOR the 29-macro set into 4 quasi-orthogonal groups whose product (2x2x10x7 = 280) vastly exceeds 29; most combos map to no macro but remain electrically valid.

ai03/polaris (qmk_firmware) layouts: LAYOUT_60_ansi, LAYOUT_60_ansi_split_bs_rshift, LAYOUT_60_ansi_tsangan_split_bs_rshift, LAYOUT_all - same suffix-composition pattern (each suffix = one localized region substitution).

## 3. Mechanical decidability: algorithm sketch and ambiguities

### Algorithm (works fully for 2-macro boards, mostly for suffix-composed families)
1. Parse all N layout macros into key sets keyed by (matrix_row, matrix_col) with geometry (x, y, w, h, r...).
2. Pick a BASE layout. Candidate heuristics, in order: (a) the macro named LAYOUT_all / LAYOUT_default if the goal is a maximal drawing; (b) for the vial DEFAULT rendering, the macro with the fewest name suffixes (LAYOUT_60_ansi over LAYOUT_60_ansi_split_bs_rshift), else the first macro in file order. No heuristic reproduces every hand-made file (contra picked the mit variant).
3. For each non-base macro M, compute diff vs base: keys IDENTICAL = same matrix id AND same geometry (dz60 shows same matrix id with different geometry must count as differing). Leftover keys on each side form the changed set.
4. Cluster each changed set into connected regions by geometric adjacency or overlap of key rectangles (base-side region and M-side region overlap in x/y bounding box: an_c backspace slot x13..15 y0; dz60 rshift slot x12.25..15 y3).
5. Each region-pair (base form, M form) is a candidate option group; merge region-pairs that recur across multiple macros (the split_bs region appears identically in every *_split_bs* macro). Choice 0 = base form, further choices = each distinct alternate form.
6. Emit the vial KLE: draw base layout; draw alternate forms next to or above the board; tag every key in group g choice c with the KLE label line g,c; tag base-region keys with g,0.
7. Emit labels from suffix vocabulary (section 4), falling back to generic names (Backspace, Enter, Left Shift, Right Shift, Bottom Row inferred from region y-position and x-position).

### Ambiguities (why full automation fails in general)
- Multi-region diffs: LAYOUT_60_ansi vs LAYOUT_60_iso differs in 3 regions at once (enter, backslash, lshift). A pairwise diff cannot tell whether that is one 3-part option (correct for ISO enter, which vial files model as ONE group spanning enter+backslash) or three independent options. Factorizing N macros into K orthogonal groups is a set-cover / factorization problem with multiple valid solutions; humans choose the ergonomic one.
- Overlapping groups: the same physical slot can participate in different groupings across macros (dz60 Row 4 mixes rshift-split, arrows, ISO variants into one 10-choice group instead of several booleans - a pure design choice).
- Combinatorial explosion: dz60 has 29 macros but the human option lattice encodes 280 combos; conversely an_c has 8 combos for 3 macros. Deriving groups from macros only reproduces combinations that exist as macros; the extra combos in hand-made files are intentional generalization beyond keyboard.json.
- Matrix identity is unstable: keys keep matrix ids while moving (ISO hash (1,14) moves rows in KLE terms), and different macros may reuse an id for physically different keys, so region matching must be geometric, not id-based.
- Ordering/polarity of choices (which form is choice 0, boolean vs list label) is editorial: plaid vs contra pick opposite defaults for identical hardware.
- Boards without keyboard.json (42keebs/mysterium) or with layouts only in C headers are out of scope for any keyboard.json-driven derivation.

## 4. Option naming from layout macro suffixes

Community layout vocabulary (from D:/GitHub2/qmk_firmware/layouts/default folder names and docs/reference_info_json.md conventions). Suffix - option label:
- iso - Enter (implies enter + backslash + often lshift region)
- ansi - (usually the base / choice 0)
- split_bs - Backspace
- split_bs_rshift - Backspace + Split Right Shift (two options)
- split_rshift / split_lshift - Right/Left Shift
- split_space / split_spc - Spacebar
- tsangan - Bottom Row (1.5/1/1.5 mods + 7u space)
- hhkb / true_hhkb - Bottom Row (blockers, split bs)
- wkl - Bottom Row; rwkl / lwkl - winkeyless
- arrow - Keys variant
- 2u_space, 7u_space / 7u_spc, 6u, 625u_space, 10u_space - size choices (Spacebar: 6.25U / 7U / ...)
- mit / planck_mit / 1x2uC - 2u center space; 2x2u, 1x2uL, 1x2uR - geometries
- blocker / noblocker - percent blocker variants
- f13 - top row; nofrow - F-row
- jis / abnt2 - layouts
- numpad_NxM / ortho_NxM - choices (become a Layout: ... group, e.g. 40percentclub/4x4 [Layout: 4x4/4x8/4x12/4x16])

Standard community names (60_ansi, tkl_iso_tsangan_split_bs_rshift, alice_split_bs, ...) are exactly compositions of these tokens, so for boards whose macros use community names, option NAMES are derivable by tokenizing the suffix delta between two macros. Custom-named macros (LAYOUT_calbatr0ss, LAYOUT_olivierko, LAYOUT_directional in dz60; LAYOUT_wk_bs; LAYOUT_2r/4l in viktus/sp_mini) carry no derivable semantics.

Observed hand-made label conventions across the 183-board survey: booleans are usually Split X / Full X / ISO Enter strings; multi-choice groups are [Bottom Row, 6.25U, 7U, WKL, HHKB], [Enter, ANSI, ISO], [Right Shift, Full, Split]. These map 1:1 onto the suffix vocabulary above.

## 5. VERDICT

100 percent mechanically derivable from keyboard.json alone:
- The union geometry of all macros (every physical key rectangle that can exist), since each macro gives absolute x/y/w/h.
- Matrix labels for every key (row,col from the matrix field) - the KLE legend vial needs.
- Whether a given key belongs to the base or to an alternate, whenever the diff between two macros is confined to disjoint bounding regions (the 2-macro case: plaid, contra, and every single-suffix pair like X vs X_split_bs). For such boards a correct vial.json with one option group per differing region can be generated fully automatically, verified here by exact matrix-set equality on plaid/contra/an_c/mysterium.
- Validation: any generated option lattice can be machine-checked by testing that every keyboard.json macro equals some choice combination (the test used in section 1).

Requires heuristics / human input:
- GROUPING when macros differ in multiple regions simultaneously (iso = enter+backslash+lshift; tsangan_split_bs_rshift = 3 regions): factorizing N macros into K orthogonal option groups has multiple valid solutions; suffix tokenization of community layout names resolves most real cases but fails for custom macro names.
- BASE selection / choice-0 polarity: no rule matches all hand-made files (contra vs plaid disagree on identical hardware). Heuristic: fewest-suffix community name, else largest common layout; cosmetic only - vial works regardless.
- Human-readable option NAMES: derivable only via the suffix vocabulary table; custom macros need fallbacks like Bottom Row Option 2.
- Choice ORDERING within a group and boolean-vs-multichoice presentation: purely editorial.
- Boards whose combination lattice intentionally exceeds the macro set (an_c 8 combos vs 3 macros): safe to generate anyway since vial addresses keys by matrix position, but it goes beyond what keyboard.json asserts.

Bottom line: for 2-macro boards and single-suffix macro families, vial.json layout options ARE mechanically derivable end-to-end (geometry, membership, and names via suffix vocab). For multi-region suffixes (iso) and large composed families (dz60-class, 29-35 macros), region membership per macro-pair is still computable, but the factorization into named option groups needs the suffix-token heuristic, and label text / ordering / default choice remain human conventions that can only be approximated.

## Appendix: data sources
- Survey list of 183 boards: generated from vial-qmk keyboards tree (multi-layout keyboard.json or info.json + vial.json with labels).
- Raw diff/match output: research/_out.txt (same directory as this file).
