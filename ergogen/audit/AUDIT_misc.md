# Audit: Miscellaneous Contents of `D:\GitHub\keyboard_stuff\ergogen`

> Agent E audit — compiled 2026-07-07. Static review only; no scripts were run.
> Covers everything EXCEPT `kle_to_ergogen\`, `KLE_SCAD_Ergogen\`, `ergogen-toolkit\` (see their dedicated audits).
> Note: the repo working tree has git initialized but **no commits**, so no history was available.

---

## 1) `ergogen_to_qmk_converter\` — 100% vaporware (docs only, zero code)

Structure (complete):
- `__init__.py` — docstring + version 0.1.0 only; all imports commented out ("will be implemented")
- `parsers/__init__.py`, `generators/__init__.py`, `data_models/__init__.py` — docstrings only, every class import commented out
- `README.md` (225 lines) — planned architecture: parse Ergogen YAML → QMKHardwareModel → generate `config.h` / `keyboard.h` / `rules.mk` / `info.json`. Phase 1–4 checklists all unchecked except "project structure setup"
- `PROJECT_SUMMARY.md` — dated Jan 5, 2025, "Ready for Development"; explicitly lists every actual script (ergogen_parser.py, cli.py, generators, data models, tests) as ⏳ TODO. Includes a "Tomorrow's Kickoff Plan" that was never executed
- `docs/ARCHITECTURE.md` (364 lines) — thorough design doc
- `docs/QMK_OUTPUT_SPEC.md` — output format specification

**Every implementation file claimed in the docs does not exist.**

**Recommendation:** **Remove** the folder after salvaging `docs/ARCHITECTURE.md` and `docs/QMK_OUTPUT_SPEC.md` into the consolidated toolkit's docs (the QMK conversion idea remains a legitimate future feature).

---

## 2) `working_samples\` — the crown jewel (keep + tidy)

~20 real community configs in categorized subfolders, demonstrating proven Ergogen patterns: **Absolem, Samoklava, Corney Island, ChonkV, Cephalopoda, Kaly, Tern**, and more.

Issues found:
- 4+ duplicate configs at root level vs. their categorized copies
- `mantis.yaml` is misnamed — actually an AI-generated numpad, not the Mantis keyboard
- `testing.yml` is KLE-converter output misfiled as a community sample
- Generated DXF/JSCAD build artifacts checked in alongside sources

**Recommendation:** **Keep + consolidate** — deduplicate, fix misnamed files, remove build artifacts, keep as the reference library.

---

## 3) `mounting_styles\` — partial research (defer)

Actual contents:
```
mounting_styles/
├── ergogen_design_prompt.md        # Comprehensive AI-prompt/design-methodology doc — genuinely useful
├── mounting_styles_README.md       # Describes six mounting-style YAML configs
├── reference_images/               # 7 images + README (mounting-style cheat sheet + per-style photos)
├── sandwich_mount/                 # (per-style folder)
└── top_mount/                      # (per-style folder)
```

The README describes six mounting-style YAML configurations (tray, top, bottom, sandwich, gasket, integrated), but only two per-style folders exist — the research is incomplete relative to its own README.

Notable: `ergogen_design_prompt.md` is a distilled "how to write working Ergogen configs" methodology (start minimal, incremental additions, use working samples as templates) — useful beyond the mounting-style project.

**Recommendation:** **Defer** — matches the project rules' "aspirational/stretch goal" designation. Keep `ergogen_design_prompt.md` visible in the consolidated docs; reconcile README vs. actual contents.

---

## 4) Root runner scripts

### `run-ergogen.bat`
Thin wrapper: validates an argument, then calls `run-ergogen-and-convert.ps1` via `powershell -ExecutionPolicy Bypass`. Despite the name, it runs the full convert pipeline.

### `run-ergogen-and-convert.ps1`
Takes a YAML file, creates an output dir named after the YAML basename (next to the YAML), runs `ergogen <file> -o <dir>`, then converts JSCAD case files to STL. Assumes `ergogen` is on PATH.

### `run-ergogen-and-convert.bat`
Standalone batch equivalent: runs `ergogen`, then converts each `cases\*.jscad` to STL via `npx @jscad/cli@1 <file> -of stla`, verifies STL creation by file existence, prints a summary of generated cases/pcbs/outlines. Assumes `ergogen` and `npx` (Node.js) on PATH.

Overlap: `run-ergogen.bat` + `.ps1` duplicate what the `.bat` does; all three also overlap with the VS Code extension's Run Ergogen command — except the extension does **not** do JSCAD→STL conversion, which is unique to these scripts.

**Recommendation:** **Merge** — keep one canonical runner (the `.ps1`, wrapped by `run-ergogen.bat`), fold the JSCAD→STL step into the consolidated toolkit (or eventually the extension); remove the redundant standalone `.bat`.

---

## 5) Root docs

| File | Content | Assessment |
|---|---|---|
| `ERGOGEN_RESEARCH.md` | Research notes (Oct 22, 2025): official resources, learning path, FlatFootFox tutorial series, community links | Mostly still accurate; links-based content ages well. **Keep**, refresh during consolidation |
| `ergogen_repos_list.md` | 123 Ergogen GitHub repos sorted by stars (Oct 22, 2025 API pull) | Snapshot data; star counts stale but ranking still indicative. **Keep** as reference, mark with date |
| `COLLECTION_SUMMARY.md` | Describes the working_samples collection effort; references docs that no longer exist at root (`WORKING_SAMPLES_COLLECTION_GUIDE.md`, `RESEARCH_SUMMARY.md`, `DOWNLOAD_PROGRESS.md`) | Partially outdated — references missing files. **Merge** relevant content into a refreshed samples README, then remove |
| `README.md` | Humorous but honest overview of every folder; correctly identifies ergogen-toolkit (VS Code ext) as "the star," admits kle_to_ergogen is flaky and ergogen_to_qmk_converter is ambitious/unfinished | Broadly accurate. **Rewrite** after consolidation to reflect new structure |

---

## Summary Recommendations

| Item | Verdict |
|---|---|
| `ergogen_to_qmk_converter\` | Remove (salvage ARCHITECTURE.md + QMK_OUTPUT_SPEC.md) |
| `working_samples\` | Keep + deduplicate/tidy |
| `mounting_styles\` | Defer (stretch goal); keep `ergogen_design_prompt.md` prominent |
| `run-ergogen.bat` + `.ps1` | Keep as canonical runner |
| `run-ergogen-and-convert.bat` | Remove (redundant); preserve JSCAD→STL logic |
| `ERGOGEN_RESEARCH.md` | Keep, refresh |
| `ergogen_repos_list.md` | Keep, date-stamp |
| `COLLECTION_SUMMARY.md` | Merge into samples README, then remove |
| `README.md` | Rewrite post-consolidation |