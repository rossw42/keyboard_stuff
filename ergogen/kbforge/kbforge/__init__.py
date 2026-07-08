"""
kbforge — Unified KLE-driven keyboard generation workflow.

Start from a simple Keyboard Layout Editor (KLE) JSON file and produce:
  * Ergogen YAML     (points + outlines + plate + PCB + cases)
  * OpenSCAD         (standalone plate/case model, no dependencies)
  * OpenSCAD layout  (hotswap_pcb_generator-compatible data file)
  * Documentation    (Markdown: stats, matrix, BOM, build pipeline)
  * Layout JSON      (canonical intermediate model, for tooling/QMK later)

Consolidates the former `kle-to-ergogen` (Python) and `kle-to-scad` (Node)
tools into one parse-once, generate-many pipeline.
"""

__version__ = "1.0.0"

from .layout import Layout, Key
from .kle_parser import parse_kle_file, parse_kle_data, KLEParseError

__all__ = [
    "Layout",
    "Key",
    "parse_kle_file",
    "parse_kle_data",
    "KLEParseError",
    "__version__",
]