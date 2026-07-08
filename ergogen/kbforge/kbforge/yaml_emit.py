"""
Minimal deterministic YAML emitter.

kbforge emits Ergogen configs without requiring PyYAML: layouts are
plain dict/list/scalar trees, insertion order is preserved, and output is
stable across runs (important for diffing generated configs in git).

Supported values: dict, list, str, int, float, bool, None.
Lists of scalars are emitted in flow style ([a, b]) which matches the
Ergogen convention for shift/size pairs.
"""

from __future__ import annotations

import re
from typing import Any

_PLAIN_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.\- ]*$")
_RESERVED = {"true", "false", "null", "yes", "no", "on", "off", "~"}


def dump(value: Any) -> str:
    """Serialize a dict/list tree to a YAML string."""
    lines: list[str] = []
    _emit(value, lines, indent=0)
    return "\n".join(lines) + "\n"


def _scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        # Trim floating noise; keep up to 3 decimals.
        text = f"{value:.3f}".rstrip("0").rstrip(".")
        return text if text not in ("", "-") else "0"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        if _PLAIN_RE.match(value) and value.strip() == value \
                and value.lower() not in _RESERVED:
            return value
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    raise TypeError(f"Unsupported YAML scalar type: {type(value).__name__}")


def _is_scalar_list(value: Any) -> bool:
    return isinstance(value, list) and all(
        not isinstance(v, (dict, list)) for v in value
    )


def _emit(value: Any, lines: list[str], indent: int, key: str | None = None) -> None:
    pad = "  " * indent
    prefix = f"{pad}{key}:" if key is not None else pad.rstrip()

    if isinstance(value, dict):
        if key is not None:
            if not value:
                lines.append(f"{prefix} {{}}")
                return
            lines.append(prefix)
        for k, v in value.items():
            _emit(v, lines, indent + (1 if key is not None else 0), key=str(k))
    elif isinstance(value, list):
        if _is_scalar_list(value):
            flow = "[" + ", ".join(_scalar(v) for v in value) + "]"
            lines.append(f"{prefix} {flow}" if key is not None else f"{pad}{flow}")
            return
        if key is not None:
            lines.append(prefix)
        for item in value:
            item_pad = "  " * (indent + (1 if key is not None else 0))
            if isinstance(item, dict):
                first = True
                for k, v in item.items():
                    if first:
                        sub: list[str] = []
                        _emit(v, sub, 0, key=str(k))
                        lines.append(f"{item_pad}- {sub[0]}")
                        extra_indent = len(item_pad) + 2
                        for line in sub[1:]:
                            lines.append(" " * extra_indent + line)
                        first = False
                    else:
                        sub = []
                        _emit(v, sub, 0, key=str(k))
                        extra_indent = len(item_pad) + 2
                        for line in sub:
                            lines.append(" " * extra_indent + line)
            elif _is_scalar_list(item):
                flow = "[" + ", ".join(_scalar(v) for v in item) + "]"
                lines.append(f"{item_pad}- {flow}")
            else:
                lines.append(f"{item_pad}- {_scalar(item)}")
    else:
        lines.append(f"{prefix} {_scalar(value)}")