# Ergogen Toolkit — Comprehensive Plan

> Phase 4 output — 2026-07-07. Based on `docs/ERGOGEN_REFERENCE.md`, the four audits in `audit/`, and `audit/CONSOLIDATION_DECISIONS.md`.
> Status: **PLAN ONLY.** No files have been moved or deleted. Execution requires user approval.

---

## 1. Vision

One coherent **Ergogen Toolkit** supporting this workflow:

```
Design in KLE  →  Convert to Ergogen YAML  →  Run Ergogen locally  →
Preview outputs (DXF)  →  Cases (JSCAD→STL) + PCBs (KiCad + ergogen-footprints)  →
[future] QMK firmware scaffold
```

## 2. Proposed Directory Structure

```
ergogen/                              # repo root (D:\GitHub\keyboard_stuff\ergogen)
├── README.md                         # rewritten: what the toolkit is, quick start
├── MASTER_TASK_LIST.md               # orchestration tracking
├── TOOLKIT_PLAN.md                   # this file
├── docs/
│   ├── ERGOGEN_REFERENCE.md          # ✅ done — condensed Ergogen docs
│   ├── coordinate_transformation_plan.md   # from kle_to_ergogen/docs
│   ├── ergogen-lessons-learned.md    # from ergogen-toolkit/
│   ├── ergogen_design_prompt.md      # from mounting_styles/
│   ├── design-math/                  # from ergogen-toolkit/autogen script/
│   │   ├── column_height_math_guide.md
│   │   └── forestv1.3_advanced_math.yaml
│   ├── qmk/                          # salvaged from ergogen_to_qmk_converter/
│   │   ├── ARCHITECTURE.md
│   │   └── QMK_OUTPUT_SPEC.md
│   └── research/
│       ├── ERGOGEN_RESEARCH.md       # refreshed
│       └── ergogen_repos_list.md     # date-stamped snapshot
├── audit/                            # ✅ done — audit trail (kept for provenance)
├── kle-to-ergogen/                   # canonical converter (Python, from kle_to_ergogen/)
│   ├── README.md                     # NEW
│   ├── requirements.txt              # NEW (PyYAML)
│   ├── cli.py
│   ├── data_models/
│   ├── generators/
│   └── examples/                     # example_kle/ renamed
├── kle-to-scad/                      # working SCAD pipeline (Node, extracted from KLE_SCAD_Ergogen/)
│   ├── README.md                     # rewritten, honest scope
│   ├── package.json
│   ├── index.js                      # SCAD path only
│   ├── src/                          # kleToIntermediate.js, scadToErgogen.js as needed
│   └── scad/                         # parameters.scad, stabilizer_spacing.scad
├── vscode-extension/                 # from ergogen-toolkit/ (renamed folder)
│   ├── extension.js
│   ├── package.json
│   └── README.md
├── scripts/
│   ├── run-ergogen.bat               # canonical runner wrapper
│   └── run-ergogen-and-convert.ps1   # ergogen + JSCAD→STL
├── working_samples/                  # tidied: deduped, renamed, artifacts removed, new README
├── mounting_styles/                  # unchanged (deferred stretch goal), README reconciled
└── archive/                          # anything removed-but-not-deleted parks here first
```

## 3. Feature Roadmap

### Milestone 1 — Restructure (no code changes)
1. Create `docs/`, `scripts/`, `archive/` layout above
2. Move/rename folders per Fate Summary Table in `CONSOLIDATION_DECISIONS.md`
3. Park removals (`ergogen_to_qmk_converter/`, dead JS, build artifacts, duplicate `.bat`) in `archive/` — nothing hard-deleted until user sign-off
4. Write new root `README.md` and per-module READMEs
5. Tidy `working_samples/` (dedupe, rename `mantis.yaml`, relocate `testing.yml`, strip artifacts, new README absorbing `COLLECTION_SUMMARY.md`)

### Milestone 2 — Converter hardening (first code work)
1. `kle-to-ergogen`: add README, requirements.txt; verify against `examples/` inputs
2. Port stabilizer detection + matrix assignment from `KLE_SCAD_Ergogen` into the Python converter (use `stabilizer_spacing.scad` constants; document Cherry spec source)
3. Fix/confirm 19.05mm (`u`) spacing consistency (the bug that bit KLE_SCAD_Ergogen)
4. Regression inputs: `examples/macropad-with-3-encoders.json` + a 40% board with spacebar (stabilizer case)

### Milestone 3 — Local pipeline polish
1. Confirm canonical runner (`scripts/run-ergogen.bat` + `.ps1`) works with a locally installed Ergogen (`npm i -g ergogen`)
2. Evaluate folding JSCAD→STL into the VS Code extension
3. Document the full local workflow in root README (install Node, `npm i -g ergogen`, converter usage, extension usage)

### Milestone 4 — PCB stage
1. Wire up `D:\GitHub2\ergogen-footprints` (ceoloide) as the footprint library: document `-o` output structure and footprint reference syntax per `docs/ERGOGEN_REFERENCE.md` §PCBs
2. Add PCB-section generation to `kle-to-ergogen` (currently points-focused): switches + diodes + controller template, using ceoloide footprints
3. Validate a sample KiCad PCB opens cleanly

### Milestone 5 — QMK scaffold (future)
1. Revive the QMK converter design from `docs/qmk/ARCHITECTURE.md` — but implemented fresh, reusing the matrix data the converter now carries
2. Targets: `info.json` + `rules.mk` + `config.h` scaffolding from Ergogen YAML

### Stretch — Mounting styles
- Blocked on Milestones 1–4. Revisit `mounting_styles/` afterward; attempt one style end-to-end (top mount, since a folder exists) before generalizing.

## 4. Risks / Open Questions

- **Naming collision:** the folder `ergogen-toolkit/` (extension) vs. the whole project "Ergogen Toolkit" — plan renames the folder to `vscode-extension/`. Confirm acceptable.
- **Two languages:** Python (converter) + Node (SCAD pipeline, extension, Ergogen itself). Accepted for now; unifying on Node is a possible future refactor.
- **No git history:** the ergogen repo dir has no commits. Recommend an initial commit BEFORE any restructuring so moves are diffable.
- **Ergogen version drift:** local docs are a few months old; verify installed Ergogen version against docs when execution begins.

## 5. Immediate Next Steps (pending user approval)

1. [ ] User reviews audits + this plan
2. [ ] Make initial git commit of current state (safety net)
3. [ ] Execute Milestone 1 restructure
4. [ ] Begin Milestone 2 converter work