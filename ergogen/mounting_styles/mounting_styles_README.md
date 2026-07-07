# Keyboard Mounting Styles (Research — Deferred Stretch Goal)

Research toward generating Ergogen cases for different keyboard mounting styles. **Status: deferred** — per [`../TOOLKIT_PLAN.md`](../TOOLKIT_PLAN.md), this is a stretch goal blocked on Milestones 1–4. It is unclear whether Ergogen's case system can express all of these styles; treat everything here as exploratory.

## What actually exists in this folder

```
mounting_styles/
├── mounting_styles_README.md   # this file
├── reference_images/           # 7 reference images + cheat sheet (see its README)
├── sandwich_mount/             # EMPTY — placeholder, no config yet
└── top_mount/                  # EMPTY — placeholder, no config yet
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

## Next steps (when unblocked)

1. Attempt **top mount** first end-to-end (folder already exists)
2. Use the patterns in [`../working_samples/`](../working_samples/) and the methodology in [`../docs/ergogen_design_prompt.md`](../docs/ergogen_design_prompt.md)
3. Validate one style fully before generalizing to the others