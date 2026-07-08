"""
Run a local Ergogen build and render its cases to STL.

This is the build step of the kbforge workflow: after generating and
reviewing/editing the .ergogen.yaml, pass it back to the CLI
(`python -m kbforge <name>.ergogen.yaml -o <out>`) to produce the
fabrication files *and* printable STLs:

    <out>/.ergogen-build/config.yaml        the generated config, staged
    <out>/.ergogen-build/footprints/...     ceoloide footprints (if needed)
    <out>/ergogen/outlines/*.dxf            plate / board / pcb outlines
    <out>/ergogen/pcbs/*.kicad_pcb          KiCad PCB
    <out>/ergogen/cases/*.jscad             Ergogen case models
    <out>/ergogen/cases/*.stl               STLs rendered from those models

Ergogen itself only emits `.jscad` for cases; the community-standard way
to get an STL is the OpenJSCAD v1 CLI:

    npx --yes @jscad/cli@1 case_bottom.jscad -o case_bottom.stl

which is exactly what this module shells out to for every case file.

Tool discovery:

* Ergogen: an `ergogen` executable on PATH (global npm install) is
  preferred; otherwise `npx --yes ergogen`.
* @jscad/cli: always via `npx --yes @jscad/cli@1` (downloaded/cached by
  npm on first use).
* ceoloide footprints (only when the config references `ceoloide/`):
  ``--footprints`` path > ``ERGOGEN_FOOTPRINTS`` env var > existing copy
  in the build folder > `git clone` from GitHub.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional

FOOTPRINTS_REPO = "https://github.com/ceoloide/ergogen-footprints"
BUILD_DIR_NAME = ".ergogen-build"
OUTPUT_DIR_NAME = "ergogen"


class ErgogenNotFound(RuntimeError):
    """Raised when neither `ergogen` nor `npx` can be located."""


class ErgogenBuildError(RuntimeError):
    """Raised when Ergogen or the jscad->STL conversion fails."""


def _ergogen_cmd() -> List[str]:
    exe = shutil.which("ergogen")
    if exe:
        return [exe]
    npx = shutil.which("npx")
    if npx:
        return [npx, "--yes", "ergogen"]
    raise ErgogenNotFound(
        "Neither `ergogen` nor `npx` found on PATH. Install Node.js and "
        "Ergogen (`npm i -g ergogen`) to build fabrication files."
    )


def _jscad_cmd() -> List[str]:
    npx = shutil.which("npx")
    if npx:
        return [npx, "--yes", "@jscad/cli@1"]
    raise ErgogenNotFound(
        "`npx` not found on PATH; it is required to run @jscad/cli for "
        "the .jscad -> .stl conversion. Install Node.js."
    )


def _run(cmd: List[str], what: str) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise ErgogenBuildError(
            f"{what} failed (exit {result.returncode}).\n"
            f"Command: {' '.join(cmd)}\n{detail}"
        )


def _ensure_footprints(
    build_dir: Path,
    config_text: str,
    footprints: Optional[str] = None,
    quiet: bool = False,
) -> None:
    """Stage footprints/ceoloide next to config.yaml when the config needs it."""
    if "ceoloide/" not in config_text:
        return  # builtin footprints only, nothing to stage

    dest = build_dir / "footprints" / "ceoloide"
    if dest.is_dir() and any(dest.glob("*.js")):
        return  # already staged from a previous build

    source = footprints or os.environ.get("ERGOGEN_FOOTPRINTS")
    if source:
        src = Path(source)
        if not src.is_dir():
            raise ErgogenBuildError(f"footprints folder not found: {source}")
        if not quiet:
            print(f"  copying footprints from {src} ...", flush=True)
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns(".git"),
                        dirs_exist_ok=True)
        return

    if not quiet:
        print(f"  cloning {FOOTPRINTS_REPO} ...", flush=True)
    dest.parent.mkdir(parents=True, exist_ok=True)
    _run(["git", "clone", "--depth", "1", FOOTPRINTS_REPO, str(dest)],
         "git clone of ergogen-footprints")


def render_case_stls(cases_dir: Path, quiet: bool = False) -> List[Path]:
    """Convert every cases/*.jscad to a sibling .stl via @jscad/cli."""
    jscads = sorted(cases_dir.glob("*.jscad")) if cases_dir.is_dir() else []
    if not jscads:
        return []
    cmd_base = _jscad_cmd()
    written: List[Path] = []
    for jscad in jscads:
        stl_path = jscad.with_suffix(".stl")
        if not quiet:
            print(f"  rendering {stl_path.name} ...", flush=True)
        _run(cmd_base + [str(jscad), "-o", str(stl_path)],
             f"jscad -> STL for {jscad.name}")
        if not stl_path.is_file():
            raise ErgogenBuildError(f"expected STL not written: {stl_path}")
        written.append(stl_path)
    return written


def build(
    ergogen_yaml: Path,
    out_dir: Path,
    footprints: Optional[str] = None,
    quiet: bool = False,
) -> List[Path]:
    """
    Run Ergogen on the generated config and convert its cases to STL.

    Returns the list of files written (Ergogen outputs + STLs). Raises
    ErgogenNotFound / ErgogenBuildError on failure.
    """
    ergogen_cmd = _ergogen_cmd()  # fail fast before staging anything

    build_dir = out_dir / BUILD_DIR_NAME
    build_dir.mkdir(parents=True, exist_ok=True)
    config_text = ergogen_yaml.read_text(encoding="utf-8")
    (build_dir / "config.yaml").write_text(config_text, encoding="utf-8")
    _ensure_footprints(build_dir, config_text, footprints, quiet)

    output_dir = out_dir / OUTPUT_DIR_NAME
    if not quiet:
        print(f"  running ergogen -> {output_dir} ...", flush=True)
    _run(ergogen_cmd + [str(build_dir), "-o", str(output_dir)], "ergogen")

    written = [p for p in sorted(output_dir.rglob("*"))
               if p.is_file() and p.suffix in (".dxf", ".svg", ".kicad_pcb", ".jscad")]
    written.extend(render_case_stls(output_dir / "cases", quiet=quiet))
    return written