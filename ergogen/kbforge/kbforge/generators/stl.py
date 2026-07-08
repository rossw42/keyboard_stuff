"""
STL rendering via the OpenSCAD CLI.

Renders the standalone `<name>.scad` model (from generators/scad.py) into
STL files, one per case part:

    <name>.plate.stl
    <name>.bottom.stl
    <name>.walls.stl

OpenSCAD is invoked headlessly:

    openscad -o out.stl -D part="plate" model.scad

The OpenSCAD executable is located by (in order):

1. an explicit path passed by the caller (``--openscad`` on the CLI)
2. the ``OPENSCAD_PATH`` environment variable
3. ``openscad`` on the system PATH
4. common install locations (Windows: Program Files, including the
   Nightly build; macOS: the app bundle; Linux: /usr/bin etc.)
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Sequence

#: Parts defined in the standalone SCAD model that make sense as STLs.
DEFAULT_PARTS: Sequence[str] = ("plate", "bottom", "walls")

#: Well-known install locations checked after PATH / env var.
_CANDIDATE_PATHS = [
    # Windows (prefer the nightly build: newer geometry kernel, faster CSG)
    r"C:\Program Files\OpenSCAD (Nightly)\openscad.exe",
    r"C:\Program Files\OpenSCAD\openscad.exe",
    r"C:\Program Files (x86)\OpenSCAD\openscad.exe",
    # macOS
    "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD",
    # Linux
    "/usr/bin/openscad",
    "/usr/local/bin/openscad",
    "/snap/bin/openscad",
]


class OpenSCADNotFound(RuntimeError):
    """Raised when no OpenSCAD executable could be located."""


class STLRenderError(RuntimeError):
    """Raised when OpenSCAD exits with an error while rendering."""


def find_openscad(explicit: Optional[str] = None) -> str:
    """Locate the OpenSCAD executable. Raises OpenSCADNotFound on failure."""
    if explicit:
        if Path(explicit).is_file():
            return explicit
        raise OpenSCADNotFound(f"openscad not found at given path: {explicit}")

    env = os.environ.get("OPENSCAD_PATH")
    if env and Path(env).is_file():
        return env

    on_path = shutil.which("openscad")
    if on_path:
        return on_path

    for candidate in _CANDIDATE_PATHS:
        if Path(candidate).is_file():
            return candidate

    raise OpenSCADNotFound(
        "OpenSCAD executable not found. Install OpenSCAD, add it to PATH, "
        "set the OPENSCAD_PATH environment variable, or pass --openscad."
    )


def render_stls(
    scad_path: Path,
    out_dir: Path,
    base_name: str,
    parts: Sequence[str] = DEFAULT_PARTS,
    openscad: Optional[str] = None,
    quiet: bool = False,
) -> List[Path]:
    """
    Render one STL per part from a standalone kbforge .scad file.

    Returns the list of STL paths written. Raises OpenSCADNotFound or
    STLRenderError on failure.
    """
    exe = find_openscad(openscad)
    out_dir.mkdir(parents=True, exist_ok=True)

    written: List[Path] = []
    for part in parts:
        stl_path = out_dir / f"{base_name}.{part}.stl"
        cmd = [
            exe,
            "-o", str(stl_path),
            "-D", f'part="{part}"',
            str(scad_path),
        ]
        if not quiet:
            print(f"  rendering {stl_path.name} ...", flush=True)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 or not stl_path.is_file():
            stderr = (result.stderr or "").strip()
            raise STLRenderError(
                f"OpenSCAD failed rendering part '{part}' "
                f"(exit {result.returncode}).\n"
                f"Command: {' '.join(cmd)}\n{stderr}"
            )
        written.append(stl_path)
    return written


if __name__ == "__main__":  # tiny manual test helper
    scad = Path(sys.argv[1])
    render_stls(scad, scad.parent, scad.stem)