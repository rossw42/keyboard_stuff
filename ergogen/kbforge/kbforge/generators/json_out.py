"""
Canonical layout JSON generator.

Serializes the shared Layout model to a stable JSON document. This is the
pipeline's machine-readable intermediate: other tools (QMK scaffolding,
visualizers, converters) can consume it without re-parsing KLE.
"""

from __future__ import annotations

import json
from typing import Any, Dict

from ..layout import Layout


def build_layout_dict(layout: Layout) -> Dict[str, Any]:
    """Build the canonical layout dict."""
    layout.assign_matrix()
    return {
        "format": "kbforge/layout",
        "version": 1,
        "name": layout.name,
        "author": layout.author,
        "notes": layout.notes,
        "unit_mm": layout.unit,
        "stats": layout.stats(),
        "bounds_mm": {k: round(v, 3) for k, v in layout.bounds_mm().items()},
        "keys": [key.to_dict(layout.unit) for key in layout.keys],
    }


def generate_layout_json(layout: Layout, indent: int = 2) -> str:
    """Generate the canonical layout JSON string."""
    return json.dumps(build_layout_dict(layout), indent=indent, ensure_ascii=False) + "\n"