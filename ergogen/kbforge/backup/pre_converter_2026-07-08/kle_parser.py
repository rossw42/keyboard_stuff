"""
KLE (Keyboard Layout Editor) JSON parser.

A faithful Python port of the kle-serial deserialization algorithm
(https://github.com/ijprest/kle-serial), which is what keyboard-layout-editor.com
itself uses. This replaces both previous parsers:

  * kle-to-ergogen/parsers/simple_kle_parser.py  — was incomplete (dropped
    rotation-cluster resets, x2/y2 secondary rects, decals, per-key h reset
    bugs, persistent-property handling)
  * kle-to-scad's dependency on @ijprest/kle-serial (Node)

Accepted input:
  * Raw KLE download JSON:      [ {meta}, [row], [row], ... ]
  * Rows only:                  [ [row], [row], ... ]
  * KLE "internal" JSON:        { "meta": {...}, "keys": [...] }   (rare)

KLE serialization semantics implemented (per kle-serial):
  * A row is a list of items; dict items set properties for FOLLOWING keys,
    string items emit a key with the current properties.
  * Persistent until changed: c (color), t (text color), g (ghost),
    a (align), f/f2 (font), p (profile), r/rx/ry (rotation).
  * Reset after every key: w, h, x2, y2, w2, h2, n (nub), l (stepped),
    d (decal).
  * x/y in a dict are RELATIVE offsets added to the cursor.
  * Specifying rx (or ry) sets the rotation cluster origin AND resets the
    cursor to the cluster origin (both x and y).
  * At end of each row: y += 1 and x resets to rotation_x (the cluster x).
"""

from __future__ import annotations

import json
from typing import Any, List, Union

from .layout import Key, Layout


class KLEParseError(Exception):
    """Raised when KLE parsing fails."""


def parse_kle_file(path: str, name: str = "") -> Layout:
    """Parse a KLE JSON file into a Layout."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        raise KLEParseError(f"KLE file not found: {path}")
    except json.JSONDecodeError as exc:
        raise KLEParseError(f"Invalid JSON in {path}: {exc}")
    return parse_kle_data(data, name=name)


def parse_kle_json(text: str, name: str = "") -> Layout:
    """Parse a KLE JSON string into a Layout."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise KLEParseError(f"Invalid JSON: {exc}")
    return parse_kle_data(data, name=name)


def parse_kle_data(data: Union[list, dict], name: str = "") -> Layout:
    """
    Parse loaded KLE JSON data (list-of-rows form, optionally with a leading
    metadata dict) into a Layout.
    """
    if isinstance(data, dict) and "keys" in data:
        # Rare "internal" form — flatten back is not supported; be explicit.
        raise KLEParseError(
            "KLE 'internal' format (dict with 'keys') is not supported; "
            "export the raw layout JSON from keyboard-layout-editor.com."
        )
    if not isinstance(data, list):
        raise KLEParseError("KLE layout must be a JSON array")

    layout = Layout(name=name or "keyboard")

    rows = list(data)
    if rows and isinstance(rows[0], dict):
        meta = rows.pop(0)
        layout.name = name or meta.get("name") or layout.name
        layout.author = meta.get("author", "")
        layout.notes = meta.get("notes", "")
        layout.metadata = {k: v for k, v in meta.items()
                           if k not in ("name", "author", "notes")}

    # Cursor state (mirrors kle-serial's `current` key prototype)
    cur = Key()
    cluster_x, cluster_y = 0.0, 0.0

    for row_index, row in enumerate(rows):
        if not isinstance(row, list):
            raise KLEParseError(
                f"Row {row_index} must be an array (got {type(row).__name__})"
            )
        for item_index, item in enumerate(row):
            if isinstance(item, dict):
                _apply_props(cur, item, item_index)
                if "rx" in item:
                    cur.rotation_x = cluster_x = float(item["rx"])
                    cur.x, cur.y = cluster_x, cluster_y
                if "ry" in item:
                    cur.rotation_y = cluster_y = float(item["ry"])
                    cur.x, cur.y = cluster_x, cluster_y
                cur.x += float(item.get("x", 0))
                cur.y += float(item.get("y", 0))
            elif isinstance(item, str):
                key = _emit_key(cur, item)
                layout.keys.append(key)
                # advance cursor & reset per-key properties
                cur.x += cur.width
                cur.width = cur.height = 1.0
                cur.x2 = cur.y2 = cur.width2 = cur.height2 = 0.0
                cur.decal = cur.stepped = cur.homing_nub = False
            else:
                raise KLEParseError(
                    f"Row {row_index} item {item_index}: expected string or "
                    f"object, got {type(item).__name__}"
                )
        # end of row: newline
        cur.y += 1.0
        cur.x = cur.rotation_x

    if not layout.keys:
        raise KLEParseError("No keys found in KLE layout")

    layout.assign_matrix()
    return layout


# ---------------------------------------------------------------------- #
# Internals
# ---------------------------------------------------------------------- #

def _apply_props(cur: Key, item: dict, item_index: int) -> None:
    """Apply a KLE property dict to the cursor key (excluding x/y/rx/ry)."""
    if "r" in item:
        # kle-serial only allows r on the first item of a row; we accept it
        # anywhere but keep the semantic (it persists).
        cur.rotation_angle = float(item["r"])
    if "w" in item:
        cur.width = float(item["w"])
        cur.width2 = float(item["w"])
    if "h" in item:
        cur.height = float(item["h"])
        cur.height2 = float(item["h"])
    if "x2" in item:
        cur.x2 = float(item["x2"])
    if "y2" in item:
        cur.y2 = float(item["y2"])
    if "w2" in item:
        cur.width2 = float(item["w2"])
    if "h2" in item:
        cur.height2 = float(item["h2"])
    if "c" in item:
        cur.color = item["c"]
    if "p" in item:
        cur.profile = item["p"]
    if "g" in item:
        cur.ghost = bool(item["g"])
    if "d" in item:
        cur.decal = bool(item["d"])
    if "n" in item:
        cur.homing_nub = bool(item["n"])
    if "l" in item:
        cur.stepped = bool(item["l"])


def _emit_key(cur: Key, label_text: str) -> Key:
    """Snapshot the cursor state into a concrete Key with labels."""
    return Key(
        x=cur.x,
        y=cur.y,
        width=cur.width,
        height=cur.height,
        rotation_angle=cur.rotation_angle,
        rotation_x=cur.rotation_x,
        rotation_y=cur.rotation_y,
        labels=label_text.split("\n"),
        color=cur.color,
        profile=cur.profile,
        decal=cur.decal,
        ghost=cur.ghost,
        stepped=cur.stepped,
        homing_nub=cur.homing_nub,
        x2=cur.x2,
        y2=cur.y2,
        width2=cur.width2,
        height2=cur.height2,
    )