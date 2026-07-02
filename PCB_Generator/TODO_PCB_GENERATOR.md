# TODO — PCB_Generator

Date: 2026-06-14

This file lists recommended next steps and short-term tasks to bring `PCB_Generator` to full operational status (Phase 2 onward).

## Short-term tasks (high priority)

- [ ] Run smoke tests for `keyboard-generator`, `case-generator`, and `pcb-library`.
  - Commands:
    ```bash
    cd "d:/GitHub/keyboard_stuff/PCB_Generator/keyboard-generator"
    pip install -r requirements.txt || pip install -e .
    pytest tests/
    ```
- [ ] Verify Python versions and pin dependencies (`requirements.txt` / `setup.py`).
- [ ] Add CI (GitHub Actions) to run `pytest` and `flake8` on push.
- [ ] Start Phase 2: implement PCB generation in `keyboard-generator/pcb/`.
  - Deliverables: generate `.kicad_pcb` and `.kicad_sch` from config
  - Verify output imports cleanly into KiCad 7.x

## Medium-term tasks

- [ ] Add unit tests for `keyboard-generator` modules: `layout`, `pcb`, `plate`.
- [ ] Improve documentation: add `QUICKSTART.md` examples for PCB generation.
- [ ] Automate BOM generation and integration with `pcb-library/boms/master-bom.csv`.
- [ ] Add packaging: `pip` package metadata, `pyproject.toml`.

## Lower-priority / Optional

- [ ] Add a Dockerfile for reproducible builds (Python 3.10+).
- [ ] Add CI job to produce release artifacts (DXF, Gerbers, STL) and attach to GitHub Releases.
- [ ] Add a simple web UI for interactive generation (Flask or static HTML + JS).

## Notes & Risks

- KiCad compatibility: aim for KiCad 7.x export to avoid conversion issues.
- CAD dependencies: `cadquery` and `ezdxf` versions may be heavy; use CI caching.
- Licensing: ensure each `pcb-library` design license is explicit in `design-files/`.

---

If you want, I can:
- Run the smoke tests now for `keyboard-generator`.
- Add a GitHub Actions CI skeleton in `.github/workflows/`.
- Begin implementing PCB export code in `keyboard-generator/pcb/`.

Which would you like me to do next?