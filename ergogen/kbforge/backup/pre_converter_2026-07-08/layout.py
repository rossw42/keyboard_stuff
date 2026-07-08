"""
Canonical layout model for kbforge.

Everything in the pipeline flows through these two classes:

    KLE JSON --parse--> Layout(Key, Key, ...) --generate--> ergogen / scad / docs / json

Coordinate conventions
----------------------
* KLE space:   key units (1u), origin top-left, +y DOWN, rotation clockwise,
               (key.x, key.y) is the key's *top-left corner* before rotation,
               rotation origin is (rotation_x, rotation_y) in units.
* Physical space (mm): computed via `Key.center_mm()` / `Layout.bounds_mm()`,
               +y still DOWN (screen orientation).
* Ergogen space: +y UP, rotation counter-clockwise; generators negate
               y and rotation when emitting Ergogen YAML.

Matrix assignment and stabilizer detection are performed once on the Layout
and shared by every output generator (this logic was previously duplicated
between kle-to-ergogen and kle-to-scad).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .stabilizers import get_stabilizer_info

#: Standard MX key spacing, center-to-center, in millimeters.
DEFAULT_UNIT_MM = 19.05

#: Keys whose Y positions differ by more than this (in key units) are
#: considered to be on different physical rows during matrix assignment.
ROW_TOLERANCE_U = 0.1


@dataclass
class Key:
    """A single key parsed from KLE, in KLE coordinate space (key units)."""

    x: float = 0.0                # top-left corner, key units
    y: float = 0.0
    width: float = 1.0            # key units
    height: float = 1.0
    rotation_angle: float = 0.0   # degrees, clockwise (KLE convention)
    rotation_x: float = 0.0       # rotation origin, key units
    rotation_y: float = 0.0
    labels: List[str] = field(default_factory=list)
    color: str = "#cccccc"
    profile: str = ""
    decal: bool = False           # decal "keys" are graphics, not switches
    ghost: bool = False
    stepped: bool = False
    homing_nub: bool = False
    # Secondary rectangle (ISO enter / big-ass enter). Offsets in units.
    x2: float = 0.0
    y2: float = 0.0
    width2: float = 0.0
    height2: float = 0.0
    # Assigned by Layout.assign_matrix()
    matrix_row: Optional[int] = None
    matrix_col: Optional[int] = None

    # ------------------------------------------------------------------ #
    # Derived geometry
    # ------------------------------------------------------------------ #

    @property
    def primary_label(self) -> str:
        """First non-empty label, or ''."""
        for label in self.labels:
            if label:
                return label
        return ""

    @property
    def is_switch(self) -> bool:
        """True if this key represents a real switch (not a decal/ghost)."""
        return not (self.decal or self.ghost)

    def center_u(self) -> Tuple[float, float]:
        """
        Physical key-center in KLE units, with rotation applied around
        (rotation_x, rotation_y).  +y is DOWN (KLE/screen orientation).
        """
        cx = self.x + self.width / 2.0
        cy = self.y + self.height / 2.0
        if self.rotation_angle:
            theta = math.radians(self.rotation_angle)  # clockwise in y-down space
            cos_t, sin_t = math.cos(theta), math.sin(theta)
            dx, dy = cx - self.rotation_x, cy - self.rotation_y
            cx = self.rotation_x + dx * cos_t - dy * sin_t
            cy = self.rotation_y + dx * sin_t + dy * cos_t
        return cx, cy

    def center_mm(self, unit: float = DEFAULT_UNIT_MM) -> Tuple[float, float]:
        """Physical key-center in millimeters (+y DOWN)."""
        cx, cy = self.center_u()
        return cx * unit, cy * unit

    def corners_u(self) -> List[Tuple[float, float]]:
        """The four (rotated) corners of the key footprint, in KLE units."""
        raw = [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width, self.y + self.height),
            (self.x, self.y + self.height),
        ]
        if not self.rotation_angle:
            return raw
        theta = math.radians(self.rotation_angle)
        cos_t, sin_t = math.cos(theta), math.sin(theta)
        out = []
        for px, py in raw:
            dx, dy = px - self.rotation_x, py - self.rotation_y
            out.append((
                self.rotation_x + dx * cos_t - dy * sin_t,
                self.rotation_y + dx * sin_t + dy * cos_t,
            ))
        return out

    @property
    def stabilizer(self) -> Optional[Dict[str, Any]]:
        """
        Stabilizer record for this key or None.
        Keys >= 2u wide (or tall) need a stabilizer (Cherry spec).
        Returns {'type', 'size', 'vertical', 'left', 'right', 'switch_offset'}.
        """
        if not self.is_switch:
            return None
        return get_stabilizer_info(self.width, self.height)

    def to_dict(self, unit: float = DEFAULT_UNIT_MM) -> Dict[str, Any]:
        """Serializable record used by the JSON generator and docs."""
        cx, cy = self.center_mm(unit)
        record: Dict[str, Any] = {
            "label": self.primary_label,
            "labels": [l for l in self.labels if l],
            "x_u": round(self.x, 4),
            "y_u": round(self.y, 4),
            "width_u": self.width,
            "height_u": self.height,
            "center_mm": [round(cx, 3), round(cy, 3)],
            "rotation_deg": self.rotation_angle,
            "matrix": {"row": self.matrix_row, "col": self.matrix_col},
            "color": self.color,
            "is_switch": self.is_switch,
        }
        if self.rotation_angle:
            record["rotation_origin_u"] = [self.rotation_x, self.rotation_y]
        stab = self.stabilizer
        if stab:
            record["stabilizer"] = stab
        return record


@dataclass
class Layout:
    """A parsed keyboard layout plus derived data shared by all generators."""

    name: str = "keyboard"
    author: str = ""
    notes: str = ""
    keys: List[Key] = field(default_factory=list)
    unit: float = DEFAULT_UNIT_MM
    metadata: Dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------ #
    # Derived collections
    # ------------------------------------------------------------------ #

    @property
    def switches(self) -> List[Key]:
        """Real switch keys (excludes decals/ghosts)."""
        return [k for k in self.keys if k.is_switch]

    @property
    def stabilized(self) -> List[Key]:
        """Switch keys that require a stabilizer."""
        return [k for k in self.switches if k.stabilizer]

    @property
    def has_rotation(self) -> bool:
        return any(k.rotation_angle for k in self.keys)

    # ------------------------------------------------------------------ #
    # Matrix assignment
    # ------------------------------------------------------------------ #

    def assign_matrix(self, tolerance: float = ROW_TOLERANCE_U) -> List[List[Key]]:
        """
        Assign electrical-matrix-style (row, col) indices to switch keys
        based on their *physical* positions rather than their KLE JSON row.
        Handles y-offset rows, split halves, and thumb clusters.

        Algorithm (consolidated from kle-to-scad's assignMatrixPositions and
        kle-to-ergogen's assign_matrix_positions — they were identical ports):
          1. Sort keys by top-left Y then X (KLE units, matching the legacy
             tools; using top-left rather than centers keeps 2u-tall keys
             like numpad + / Enter in the row where they start).
          2. Group into rows whenever Y jumps by more than `tolerance` units.
          3. Within each row, order by X; assign (row_index, col_index).

        Returns the grouped rows (top-to-bottom, left-to-right).
        """
        switches = self.switches
        if not switches:
            return []

        ordered = sorted(switches, key=lambda k: (k.y, k.x))

        rows: List[List[Key]] = []
        current: List[Key] = [ordered[0]]
        last_y = ordered[0].y

        for key in ordered[1:]:
            if abs(key.y - last_y) > tolerance:
                rows.append(current)
                current = [key]
                last_y = key.y
            else:
                current.append(key)
        rows.append(current)

        for row_index, row in enumerate(rows):
            row.sort(key=lambda k: k.x)
            for col_index, key in enumerate(row):
                key.matrix_row = row_index
                key.matrix_col = col_index
        return rows

    @property
    def matrix_size(self) -> Tuple[int, int]:
        """(rows, cols) of the assigned matrix. Assigns if not yet done."""
        if any(k.matrix_row is None for k in self.switches):
            self.assign_matrix()
        if not self.switches:
            return (0, 0)
        rows = max(k.matrix_row for k in self.switches) + 1
        cols = max(k.matrix_col for k in self.switches) + 1
        return rows, cols

    # ------------------------------------------------------------------ #
    # Bounds
    # ------------------------------------------------------------------ #

    def bounds_u(self) -> Dict[str, float]:
        """Rotation-aware bounding box of all keys, in KLE units (+y DOWN)."""
        if not self.keys:
            return {"min_x": 0, "max_x": 0, "min_y": 0, "max_y": 0,
                    "width": 0, "height": 0}
        xs: List[float] = []
        ys: List[float] = []
        for key in self.keys:
            for px, py in key.corners_u():
                xs.append(px)
                ys.append(py)
        return {
            "min_x": min(xs), "max_x": max(xs),
            "min_y": min(ys), "max_y": max(ys),
            "width": max(xs) - min(xs), "height": max(ys) - min(ys),
        }

    def bounds_mm(self) -> Dict[str, float]:
        """Bounding box in millimeters."""
        b = self.bounds_u()
        return {k: v * self.unit for k, v in b.items()}

    # ------------------------------------------------------------------ #
    # Stats (shared by docs generator and CLI summary)
    # ------------------------------------------------------------------ #

    def stats(self) -> Dict[str, Any]:
        rows, cols = self.matrix_size
        b = self.bounds_mm()
        return {
            "name": self.name,
            "total_keys": len(self.keys),
            "switch_count": len(self.switches),
            "decal_count": sum(1 for k in self.keys if k.decal),
            "stabilized_keys": len(self.stabilized),
            "matrix_rows": rows,
            "matrix_cols": cols,
            "has_rotation": self.has_rotation,
            "unique_widths_u": sorted({k.width for k in self.switches}),
            "size_mm": [round(b["width"], 1), round(b["height"], 1)],
            "unit_mm": self.unit,
        }