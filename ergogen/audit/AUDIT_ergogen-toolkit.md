# Audit: `ergogen-toolkit\`

> Agent D audit — compiled 2026-07-07. Static review only; no scripts were run.

## Overview

**Not a script collection** — this folder is a working **VS Code extension** ("Ergogen Toolkit" v4.0.0) plus an `autogen script/` subfolder of design-math research documents and YAML configs. There is **no KLE conversion functionality** anywhere in this folder, despite the folder name suggesting overlap with the KLE converters.

## File/Folder Structure

```
ergogen-toolkit/
├── .vscodeignore
├── LICENSE
├── README.md
├── ergogen-lessons-learned.md
├── extension.js                 (1,271 lines — the entire extension, zero runtime deps)
├── package.json                 (VS Code extension manifest, v4.0.0)
├── package-lock.json
└── autogen script/
    ├── README.md
    ├── column_height_math_guide.md
    ├── forest_base_config.yaml
    ├── forestv1.2.yaml
    └── forestv1.3_advanced_math.yaml
```

## Component Notes

### `extension.js` (JavaScript, ~1,271 lines, zero runtime dependencies)
Two VS Code commands:

1. **`ergogen-toolkit.runErgogen`** — spawns the Ergogen CLI (`spawn(ergogenCmd, ["-o", outputDir, yamlFile], {shell:true})`) on the active/last YAML file. Output goes to a directory named after the YAML file's basename. Includes progress notification, cancellation, output-channel streaming, and ENOENT-friendly error messages.
2. **`ergogen-toolkit.openViewer`** — webview **DXF preview** with a hand-rolled DXF parser (LINE/ARC/CIRCLE/LWPOLYLINE → SVG), sidebar file list, and in-panel Run/Refresh buttons.

Quality: working, self-contained, complete for its scope.

### `autogen script/` (no script — research/docs only)
- `column_height_math_guide.md` — three stagger-equalization methods plus a pseudo-code generator algorithm. Genuine design research.
- `forestv1.3_advanced_math.yaml` — fully parametric stagger system; the canonical version.
- `forestv1.2.yaml` — boundary/sine-curve experiments; superseded by v1.3.
- `forest_base_config.yaml` — complete points-less case template; orphaned.
- `README.md` — describes the intended autogen approach.

### Docs
- `README.md` — accurately describes the extension's two commands.
- `ergogen-lessons-learned.md` — practical Ergogen usage lessons; valuable knowledge capture.

## Quality Assessment

- **Status:** The extension is the most finished piece of software in the entire collection.
- The "autogen script" folder is misleadingly named — it is research, not a tool.

## Recommendations

| Component | Recommendation |
|---|---|
| VS Code extension (`extension.js` + manifest) | **Keep** — the workflow centerpiece; already handles the "run Ergogen locally" goal |
| `ergogen-lessons-learned.md` | **Keep** — merge into consolidated toolkit docs |
| `column_height_math_guide.md` | **Keep** — unique design-math research |
| `forestv1.3_advanced_math.yaml` | **Keep** — canonical parametric config example |
| `forestv1.2.yaml` | **Remove/archive** — superseded by v1.3 |
| `forest_base_config.yaml` | **Defer** — orphaned template; decide during consolidation |
| `autogen script/` naming | **Rename** — e.g., `design-math/` (it contains no script) |

## Distinctive vs. Siblings

- Zero overlap with `kle_to_ergogen` and `KLE_SCAD_Ergogen` — no KLE functionality at all.
- The premise in the project rules ("all three appear to deal with converting KLE data") is **incorrect** for this folder; it fills a different niche (local Ergogen runner + DXF viewer inside VS Code).
- Its Run-Ergogen command duplicates the root `run-ergogen*.bat/.ps1` scripts' purpose — one of these approaches should become canonical.