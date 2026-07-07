# Audit: `KLE_SCAD_Ergogen\`

> Agent C audit — compiled 2026-07-07. Static review only; no scripts were run.

## Overview

A **Node.js** CLI tool (deps: `commander`, `@ijprest/kle-serial`, `js-yaml`) with **two pipelines**:

1. `index.js` — KLE JSON → intermediate format → Ergogen YAML (optional SCAD output)
2. `kleToErgogenViaSCAD.js` — KLE → SCAD → JS-evaluated-SCAD → Ergogen (an experiment)

The SCAD/hotswap_pcb_generator side **works**; the Ergogen output side is **broken/incomplete**.

## File/Folder Structure

```
KLE_SCAD_Ergogen/
├── index.js                    # Primary CLI (kle-to-ergogen)
├── kleToErgogenViaSCAD.js      # Alternate CLI (KLE→SCAD→Ergogen pipeline, experimental)
├── package.json / package-lock.json
├── README.md                   # Full docs (partly aspirational — claims features that are disabled)
├── TODO_README.md              # Dated 2026-06-14, maintenance checklist
├── test_40percent.json/.scad/.yaml   # 40% board test artifacts (.yaml output is BROKEN)
├── examples/
│   ├── macropad_2x2.json/.yaml
│   └── numpad.json/.yaml       # stale outputs from older code
├── scad/
│   ├── parameters.scad         # Copied from hotswap_pcb_generator (full PCB/case/plate params)
│   └── stabilizer_spacing.scad # Cherry stabilizer spacing constants per key size
└── src/
    ├── kleParser.js            # KLE JSON → key objects (via @ijprest/kle-serial) — BYPASSED/dead
    ├── kleToIntermediate.js    # KLE → rich intermediate format (stabs, matrix, SCAD-format)
    ├── coordinateTransform.js  # KLE units→mm, centering, Y-flip, matrix grouping — computed then IGNORED
    ├── ergogenGenerator.js     # Intermediate → Ergogen v4 YAML
    ├── scadToErgogen.js        # Parsed SCAD layout → Ergogen YAML
    └── scadEvaluator.js        # Evaluates SCAD-like layout data in JS
```

## Findings

### What works
- **SCAD pipeline:** `test_40percent.scad` is a correct layout, including an automatic `stab_6_25u` spacebar stabilizer entry.
- **Stabilizer handling:** `scad/stabilizer_spacing.scad` + intermediate-format stab detection is the only stabilizer support in the whole collection.
- **Matrix assignment:** `kleToIntermediate.js` produces a rich intermediate format with row/column matrix data.

### What's broken
- **Ergogen output:** `test_40percent.yaml` has 40 empty columns (zero keys) — the current generator produces unusable output.
- **Key-spacing bug:** `examples/*.yaml` were produced by older code with a 19 vs 19.05 mm spacing bug (~1mm cumulative drift).
- **PCBs section:** hardcoded off ("Disabled for now") despite README claiming PCB generation.

### Dead code
- `kleParser.js` is fully bypassed by the current pipeline.
- `coordinateTransform.js` is computed and then ignored — ironically its Y-flip is exactly the fix the broken Ergogen generator needs.
- CLI flags `--split` and `--diode-direction` are no-ops.

## Quality Assessment

- **Status:** Half-working experiment. SCAD/hotswap_pcb_generator integration is genuinely useful and unique; the Ergogen generation is broken and behind `kle_to_ergogen` (Python).
- **Docs:** README overpromises; TODO_README (2026-06-14) is an honest maintenance checklist.

## Recommendations

| Component | Recommendation |
|---|---|
| SCAD pipeline + `scad/` data files | **Merge** — unique hotswap_pcb_generator/OpenSCAD integration |
| Stabilizer detection (`kleToIntermediate.js`) | **Merge** — only stabilizer support in the collection |
| Matrix assignment logic | **Merge** — useful for future QMK conversion |
| `ergogenGenerator.js` | **Remove** — broken; Python `kle_to_ergogen` does this better |
| `kleParser.js`, `coordinateTransform.js` | **Remove** (dead code) — but note the Y-flip logic before discarding |
| `kleToErgogenViaSCAD.js` pipeline | **Remove/defer** — experiment superseded by direct pipeline |
| Broken test/example YAML outputs | **Remove** |
| README.md | **Rewrite** — currently claims disabled features |

## Distinctive vs. Siblings

- Only tool with **stabilizer** handling, **matrix** assignment, and **OpenSCAD/hotswap_pcb_generator** output.
- Its KLE parsing uses the battle-tested `@ijprest/kle-serial` library (the Python sibling hand-rolls parsing).
- Its Ergogen YAML generation is the weakest of the collection — the Python tool should own that role.