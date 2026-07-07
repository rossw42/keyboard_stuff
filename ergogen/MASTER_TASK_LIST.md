# Ergogen Toolkit — Master Task List

> Orchestration plan for building the consolidated Ergogen Toolkit.
> Rules of engagement: `D:\Keyboard Workspace\.clinerules\ergogen.md`
> Current phase: **learning, documenting, consolidating — no script execution.**

---

## Phase 1: Learn Ergogen (docs research) ✅ COMPLETE

- [x] **Agent A — Docs Researcher**
  - Read all of `D:\Keyboard Workspace\ergogen-docs-md`
  - Output: `docs/ERGOGEN_REFERENCE.md` (504 lines — condensed reference covering pipeline, preprocessing, units, points, outlines, cases, PCBs, CLI usage, metadata)

## Phase 2: Audit existing scripts (parallel agents) ✅ COMPLETE

- [x] **Agent B — Audit `kle_to_ergogen\`** → `audit/AUDIT_kle_to_ergogen.md`
  - Finding: working Python KLE→Ergogen converter; best Ergogen output; unique naming strategies + provenance comments
- [x] **Agent C — Audit `KLE_SCAD_Ergogen\`** → `audit/AUDIT_KLE_SCAD_Ergogen.md`
  - Finding: Node CLI; SCAD pipeline works (unique stabilizer/matrix support); Ergogen output BROKEN; much dead code
- [x] **Agent D — Audit `ergogen-toolkit\`** → `audit/AUDIT_ergogen-toolkit.md`
  - Finding: NOT a KLE tool — a working VS Code extension (Run Ergogen + DXF viewer); most finished software here
- [x] **Agent E — Audit everything else** → `audit/AUDIT_misc.md`
  - Finding: `ergogen_to_qmk_converter` is vaporware (docs only); `working_samples` is the crown jewel (needs tidying); mounting_styles incomplete; runner scripts overlap; some root docs stale

## Phase 3: Overlap analysis & consolidation decisions ✅ COMPLETE

- [x] Feature matrix comparing the KLE-related tools
- [x] Best-implementation picks per feature
- [x] Keep / merge / remove / defer decision for every script/folder
- [x] Output: `audit/CONSOLIDATION_DECISIONS.md`
- **Key finding:** the assumed 3-way KLE overlap was wrong — `ergogen-toolkit` has no KLE functionality; real overlap is only between the Python and Node converters, each with a distinct working half.

## Phase 4: Toolkit plan ✅ COMPLETE

- [x] Comprehensive plan written: `TOOLKIT_PLAN.md`
  - Proposed directory structure, 5 milestones + stretch goal, risks, next steps
- [x] Outdated research files assessed (dispositions recorded in decisions doc; rewrites happen in Milestone 1)

---

## Phase 5: Execution (⏸ AWAITING USER APPROVAL)

- [ ] User reviews audits + `TOOLKIT_PLAN.md`
- [ ] Initial git commit of current state (repo has no commits — safety net before restructuring)
- [ ] Milestone 1 — Restructure (moves/renames/archive per `CONSOLIDATION_DECISIONS.md`; nothing hard-deleted)
- [ ] Milestone 2 — Converter hardening (stabilizer + matrix port into Python converter)
- [ ] Milestone 3 — Local pipeline polish (canonical runner, workflow docs)
- [ ] Milestone 4 — PCB stage (ergogen-footprints integration)
- [ ] Milestone 5 — QMK scaffold (future)
- [ ] Stretch — Mounting styles

---

## Deliverables Index

| File | Purpose |
|---|---|
| `docs/ERGOGEN_REFERENCE.md` | Condensed Ergogen documentation reference |
| `audit/AUDIT_kle_to_ergogen.md` | Audit of Python KLE→Ergogen converter |
| `audit/AUDIT_KLE_SCAD_Ergogen.md` | Audit of Node KLE/SCAD tool |
| `audit/AUDIT_ergogen-toolkit.md` | Audit of VS Code extension |
| `audit/AUDIT_misc.md` | Audit of QMK converter, samples, mounting styles, runners, root docs |
| `audit/CONSOLIDATION_DECISIONS.md` | Feature matrix + keep/merge/remove/defer decisions |
| `TOOLKIT_PLAN.md` | Comprehensive toolkit build plan |

## Status Log

| Date | Update |
|------|--------|
| 2026-07-07 | Master task list created; Phase 1–2 agents dispatched |
| 2026-07-07 | All 5 agents completed; audit reports written |
| 2026-07-07 | Phase 3 consolidation decisions written |
| 2026-07-07 | Phase 4 TOOLKIT_PLAN.md written — Phases 1–4 COMPLETE, awaiting user approval for execution |