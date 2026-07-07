# Consolidation Decisions

> Phase 3 output — synthesized from the four audit reports (`AUDIT_kle_to_ergogen.md`, `AUDIT_KLE_SCAD_Ergogen.md`, `AUDIT_ergogen-toolkit.md`, `AUDIT_misc.md`). 2026-07-07.

---

## Key Finding: the original overlap assumption was wrong

The project rules assumed `kle_to_ergogen`, `KLE_SCAD_Ergogen`, and `ergogen-toolkit` all overlap on KLE conversion. The audits show:

- **`kle_to_ergogen`** (Python) — KLE → Ergogen YAML. Working. Best Ergogen output.
- **`KLE_SCAD_Ergogen`** (Node) — KLE → Ergogen (BROKEN) + KLE → OpenSCAD (WORKING). Unique stabilizer/matrix/SCAD features.
- **`ergogen-toolkit`** (VS Code extension) — **no KLE functionality at all.** Local Ergogen runner + DXF viewer. Most finished software in the collection.

So the real overlap is only between the first two — and even there, each side has a distinct working half.

## Feature Matrix (KLE-related tools)

| Feature | kle_to_ergogen (Py) | KLE_SCAD_Ergogen (Node) | Winner |
|---|---|---|---|
| KLE JSON parsing | hand-rolled | `@ijprest/kle-serial` (battle-tested lib) | Node lib concept; Py implementation acceptable |
| Ergogen YAML generation | **Working**, provenance comments | Broken (empty columns, 19 vs 19.05 bug) | **Python** |
| Key naming strategies (matrix/sequential/label) | **Yes** (unique) | No | **Python** |
| CLI design | Polished (`--validate-only`, `--stats`, `--section-only`) | commander, with no-op flags | **Python** |
| Stabilizer detection/spacing | No | **Yes** (unique) | **Node** |
| Matrix (row/col) assignment | Partial | **Rich intermediate format** | **Node** |
| OpenSCAD / hotswap_pcb_generator output | No | **Yes, working** (unique) | **Node** |
| Coordinate transform docs | **Best doc in collection** | Y-flip code (dead, but correct idea) | **Python doc** |

## Decisions per Component

### KLE → Ergogen conversion → **base on `kle_to_ergogen` (Python)**
- D1. The Python converter becomes the canonical KLE → Ergogen converter.
- D2. Port from `KLE_SCAD_Ergogen`: stabilizer detection (`kleToIntermediate.js` + `stabilizer_spacing.scad` data) and matrix-assignment logic (also feeds future QMK conversion).
- D3. Add a README + `requirements.txt`; remove orphaned `package.json`/lock and checked-in `output/` artifacts.

### KLE → OpenSCAD pipeline → **keep as a separate module**
- D4. Preserve the working SCAD pipeline (`index.js` SCAD path + `scad/` data files) as a distinct toolkit module (`kle-to-scad`). Do not attempt to rewrite in Python for now.
- D5. Delete the broken/dead parts: `ergogenGenerator.js`, `kleParser.js`, `coordinateTransform.js` (note its Y-flip logic first), `kleToErgogenViaSCAD.js`, broken test/example YAML.

### VS Code extension → **keep as-is, it's the workflow hub**
- D6. `ergogen-toolkit/` extension is kept unchanged (rename consideration: it currently squats on the name the whole consolidated project wants).
- D7. Move `autogen script/` contents out of the extension folder into toolkit docs (rename to `design-math`); archive superseded `forestv1.2.yaml`.

### Ergogen runners → **one canonical runner**
- D8. Keep `run-ergogen.bat` → `run-ergogen-and-convert.ps1` as the canonical CLI runner (includes JSCAD→STL).
- D9. Remove `run-ergogen-and-convert.bat` (redundant duplicate).
- D10. Future: fold JSCAD→STL into the VS Code extension (deferred).

### QMK converter → **remove folder, salvage design docs**
- D11. `ergogen_to_qmk_converter/` is vaporware (zero code). Salvage `docs/ARCHITECTURE.md` + `docs/QMK_OUTPUT_SPEC.md` into toolkit docs as the design basis for a future QMK feature; remove the rest.

### Working samples → **keep, tidy**
- D12. Deduplicate root-level copies, rename mislabeled `mantis.yaml`, move `testing.yml` out, remove checked-in build artifacts, write a samples README (absorbing the useful parts of `COLLECTION_SUMMARY.md`).

### Mounting styles → **defer (stretch goal)**
- D13. Leave as research; promote `ergogen_design_prompt.md` into main toolkit docs; reconcile its README with actual contents (only 2 of 6 described styles exist).

### Root docs
- D14. Keep `ERGOGEN_RESEARCH.md` (refresh) and `ergogen_repos_list.md` (date-stamp as snapshot).
- D15. Remove `COLLECTION_SUMMARY.md` after merging into samples README.
- D16. Rewrite root `README.md` post-consolidation.

## Fate Summary Table

| Item | Fate |
|---|---|
| `kle_to_ergogen/` (core code) | **Keep** — canonical KLE→Ergogen converter |
| `kle_to_ergogen/` npm files + `output/` | **Remove** |
| `KLE_SCAD_Ergogen/` SCAD pipeline + `scad/` | **Merge** → `kle-to-scad` module |
| `KLE_SCAD_Ergogen/` stabilizer + matrix logic | **Merge** → into Python converter |
| `KLE_SCAD_Ergogen/` Ergogen generator + dead code | **Remove** |
| `ergogen-toolkit/` VS Code extension | **Keep** |
| `ergogen-toolkit/autogen script/` | **Move** → docs/design-math (archive v1.2 yaml) |
| `ergogen_to_qmk_converter/` | **Remove** (salvage 2 design docs) |
| `working_samples/` | **Keep** + tidy |
| `mounting_styles/` | **Defer** (promote design prompt doc) |
| `run-ergogen.bat` + `.ps1` | **Keep** (canonical runner) |
| `run-ergogen-and-convert.bat` | **Remove** |
| `ERGOGEN_RESEARCH.md`, `ergogen_repos_list.md` | **Keep** (refresh/date-stamp) |
| `COLLECTION_SUMMARY.md` | **Remove** after merge |
| Root `README.md` | **Rewrite** |

> Per project rules, no files are deleted in this phase — these are documented decisions to be executed in the consolidation/migration phase after user approval.