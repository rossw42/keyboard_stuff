# Ergogen Toolkit — Master Task List

> Orchestration tracking for the consolidated Ergogen Toolkit.
> Rules of engagement: `D:\Keyboard Workspace\.clinerules\ergogen.md`
> Plan: `TOOLKIT_PLAN.md`

---

## Agent Roster & Status

| Agent | Assignment | Status | Output |
|---|---|---|---|
| A | Ergogen docs research | ✅ done | `docs/ERGOGEN_REFERENCE.md` |
| B | Audit kle_to_ergogen | ✅ done | `audit/AUDIT_kle_to_ergogen.md` |
| C | Audit KLE_SCAD_Ergogen | ✅ done | `audit/AUDIT_KLE_SCAD_Ergogen.md` |
| D | Audit ergogen-toolkit | ✅ done | `audit/AUDIT_ergogen-toolkit.md` |
| E | Audit misc (QMK conv, samples, runners, docs) | ✅ done | `audit/AUDIT_misc.md` |
| F | Root README draft | ✅ done | `README.md` (rewritten) |
| G | kle-to-ergogen README + requirements | ✅ done | `kle-to-ergogen/README.md`, `requirements.txt` |
| H | kle-to-scad verify + README | ✅ done | found startup crash → `index.js` rewritten; `kle-to-scad/README.md` |
| I | working_samples curation | ✅ done | `working_samples/README.md` |
| J | Archive + mounting_styles docs | ✅ done | `archive/README.md`, corrected `mounting_styles_README.md` |
| K | PCB footprints guide | ✅ done | `docs/PCB_FOOTPRINTS_GUIDE.md` |

---

## Phase 1: Learn Ergogen ✅ COMPLETE
- [x] `docs/ERGOGEN_REFERENCE.md` (504 lines) — condensed reference for the full config format

## Phase 2: Audit ✅ COMPLETE
- [x] Four audit reports in `audit/`
- Key finding: the assumed 3-way KLE overlap was wrong — `ergogen-toolkit` (VS Code extension) has no KLE code

## Phase 3: Consolidation decisions ✅ COMPLETE
- [x] `audit/CONSOLIDATION_DECISIONS.md` — feature matrix + keep/merge/remove/defer per component

## Phase 4: Toolkit plan ✅ COMPLETE
- [x] `TOOLKIT_PLAN.md` — structure, milestones, risks

## Phase 5: Execution

### Milestone 1 — Restructure ✅ COMPLETE
- [x] Git safety commit before restructuring (`92cec8a`)
- [x] New layout created: `docs/` (+design-math, qmk, research), `scripts/`, `archive/`
- [x] Renames: `kle_to_ergogen`→`kle-to-ergogen`, `KLE_SCAD_Ergogen`→`kle-to-scad`, `ergogen-toolkit`→`vscode-extension`
- [x] Archived (not deleted): QMK vaporware, dead JS, broken YAML outputs, build artifacts, duplicate `.bat`, npm strays, `forestv1.2.yaml`, `COLLECTION_SUMMARY.md`
- [x] `working_samples/` tidied: duplicates archived, `mantis.yaml`→`ai_generated_numpad.yaml`, loose files → `uncategorized/`, new README
- [x] New READMEs: root, kle-to-ergogen, kle-to-scad, working_samples, archive, mounting_styles (corrected — old one described 6 configs that don't exist)

### Milestone 2 — Converter hardening ✅ CORE COMPLETE
- [x] `requirements.txt` added; PyYAML verified as only dep
- [x] Fixed package imports broken by folder rename (cli.py, generators, parsers)
- [x] **Bug fixed:** KLE metadata object (first array element) crashed the parser
- [x] **Bug fixed:** generator emitted points directly under `points:` — Ergogen 4.1.0 requires `points.zones`; absolute layouts now emit one zone per point with `anchor.shift`
- [x] Internal validator updated to zones-based structure
- [x] Regression input 1: `macropad-with-3-encoders.json` → 27 points ✅
- [x] Regression input 2: `test_40percent.json` (spacebar/stabilizer board) → 40 points ✅
- [ ] DEFERRED: port stabilizer detection + matrix assignment from kle-to-scad into the Python converter (next code work)

### Milestone 3 — Local pipeline ✅ VERIFIED
- [x] Ergogen 4.1.0 confirmed installed and working locally
- [x] `scripts/run-ergogen.bat` + `.ps1` verified end-to-end: KLE → converter → Ergogen → DXF/SVG outputs for both regression boards
- [x] Full workflow documented in root README
- [ ] DEFERRED: fold JSCAD→STL into the VS Code extension

### Milestone 3b — kle-to-scad repair ✅ COMPLETE
- [x] Agent H found index.js crashed on startup (requires → archived files)
- [x] `index.js` rewritten as honest SCAD-only CLI (no-op flags removed)
- [x] `package.json` renamed/rescoped to `kle-to-scad`
- [x] Smoke test: `test_40percent.json` → 40 keys, 4×12 matrix, 1 stabilizer ✅

### Milestone 4 — PCB stage 🔄 DOCS DONE, CODE PENDING
- [x] `docs/PCB_FOOTPRINTS_GUIDE.md` — ceoloide footprints usage, pcbs YAML syntax, KiCad verification
- [ ] Add `pcbs:` section generation to kle-to-ergogen (switch + diode + controller)
- [ ] Validate a generated `.kicad_pcb` opens cleanly in KiCad

### Milestone 5 — QMK scaffold ⏳ FUTURE
- [ ] Fresh implementation based on `docs/qmk/ARCHITECTURE.md`

### Stretch — Mounting styles ⏳ DEFERRED
- [ ] Attempt top mount end-to-end after Milestone 4 code work

---

## Bugs Found & Fixed This Session

| # | Bug | Fix |
|---|---|---|
| 1 | `kle-to-scad/index.js` crashed on startup (3 requires → archived files) | Rewritten as SCAD-only CLI |
| 2 | Python imports broke after folder rename (`kle_to_ergogen.` prefix) | Local-package imports + path fix |
| 3 | KLE metadata object crashed parser ("Row 0 must be an array") | Metadata detection + name extraction |
| 4 | Generated YAML rejected by Ergogen ("Unexpected key r0c0 within points") | Points now emitted under `points.zones` with `anchor.shift` |
| 5 | Validator false-positives (looked for x/y, generator emits shift) | Zones-aware validation |

## Status Log

| Date | Update |
|------|--------|
| 2026-07-07 | Phases 1–4 complete (5 agents); plan approved by user |
| 2026-07-07 | Safety commit `92cec8a`; Milestone 1 restructure executed |
| 2026-07-07 | Agents F–J: READMEs drafted; H found kle-to-scad crash |
| 2026-07-07 | Converters repaired + smoke-tested; 5 bugs fixed |
| 2026-07-07 | End-to-end pipeline verified with Ergogen 4.1.0 (both regression boards) |
| 2026-07-07 | Agent K: PCB footprints guide written — Milestones 1–3 complete, M4 docs done |