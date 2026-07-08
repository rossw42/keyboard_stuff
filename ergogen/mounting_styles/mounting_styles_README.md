# Keyboard Mounting Styles (Research — Deferred Stretch Goal)

Research toward generating Ergogen cases for different keyboard mounting styles. **Status: deferred** — per [`../TOOLKIT_PLAN.md`](../TOOLKIT_PLAN.md), this is a stretch goal blocked on Milestones 1–4. It is unclear whether Ergogen's case system can express all of these styles; treat everything here as exploratory.

## What actually exists in this folder

```
mounting_styles/
├── mounting_styles_README.md     # this file
├── MOUNTING_STYLES_ANALYSIS.md   # feasibility analysis + proposed representations
├── option_a_templates/           # per-style Ergogen config fragments (UNTESTED sketches)
├── option_b_descriptors/         # proposed toolkit descriptor format (schema + examples)
├── reference_images/             # 7 reference images + cheat sheet (see its README)

```

> An earlier version of this README described six complete YAML configurations (tray, top, bottom, sandwich, gasket, integrated). **Those files do not exist** — the descriptions below are retained as design research/context only.

The companion design-methodology document formerly in this folder now lives at [`../docs/ergogen_design_prompt.md`](../docs/ergogen_design_prompt.md).

## The six mounting styles (researched, not yet implemented)

| Style | Concept | Key structural requirements |
|---|---|---|
| **Tray mount** | PCB sits in a case tray | Perimeter mounting holes in PCB, M3 standoffs in case bottom |
| **Top mount** | Plate attaches to case from above | Plate tabs, countersunk screws from top, separate plate from PCB |
| **Bottom mount** | Plate attaches to case from below | Plate tabs, screws from case bottom |
| **Sandwich mount** | Plate clamped between top and bottom case halves | Through-bolts around perimeter through plate |
| **Gasket mount** | Plate suspended on gaskets between halves | Gasket tabs on plate, gasket channels in both case halves |
| **Integrated plate** | Plate is part of the top case | Single top-case-with-plate piece |

See `reference_images/` for photos of each style and a comparison cheat sheet.

## Feasibility analysis & proposed templates

See [`MOUNTING_STYLES_ANALYSIS.md`](MOUNTING_STYLES_ANALYSIS.md) — verdict: all six styles are expressible as Ergogen Z-stacked extrusions + booleans. It proposes a shared parameter block, per-style "layer recipe" template fragments, and a higher-level descriptor format for the consolidated toolkit.

Both options are written out for later consideration (design sketches, **untested**):

- [`option_a_templates/`](option_a_templates/README.md) — `_shared.yaml` + all six style fragments in pure Ergogen `units:`/`outlines:`/`cases:` form
- [`option_b_descriptors/`](option_b_descriptors/README.md) — descriptor schema + sandwich/top-mount example descriptors for a future toolkit generator

## Next steps (when unblocked)

1. Attempt **top mount** first end-to-end (folder already exists)
2. Use the patterns in [`../working_samples/`](../working_samples/) and the methodology in [`../docs/ergogen_design_prompt.md`](../docs/ergogen_design_prompt.md)
3. Validate one style fully before generalizing to the others