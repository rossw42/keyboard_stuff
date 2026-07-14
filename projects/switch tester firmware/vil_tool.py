#!/usr/bin/env python3
"""
vil_tool.py — Switch Tester inventory <-> Vial saved-layout (.vil) tool.

Workflow:
    1. Export a saved layout once from your board in Vial  ->  template.vil
    2. Maintain your switch inventory in switches.md (Markdown tables)
    3. python vil_tool.py generate            ->  switch_tester_generated.vil
    4. In Vial: File -> Load saved layout     ->  all macros updated at once

Commands:
    generate  Build a .vil from switches.md + template.vil (patches macros only)
    extract   Pull macros out of an exported .vil back into a switches.md
    check     Estimate macro buffer usage vs. available EEPROM space
    report    Print a position -> switch cheat sheet

Inventory model:
    Every switch has an explicit full matrix position ("Pos" column = "row,col")
    and an explicit Type. Macro index = row * matrix_cols + col — matching the
    firmware's test layer, where key (r,c) fires M(r*cols+c). The `## Row N`
    sections are organizational only; any type can live at any position.

The script is board-agnostic: it never fabricates a .vil from scratch, it only
patches the "macro" array of a template exported from the real board (correct
UID, matrix shape and layer count are therefore always preserved).

Stdlib only. Python 3.8+.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Defaults (overridable by CLI flags and the options comment in switches.md)
# ---------------------------------------------------------------------------

DEFAULT_INVENTORY = "switches.md"
DEFAULT_TEMPLATE = "template.vil"
DEFAULT_OUTPUT = "switch_tester_generated.vil"

# Conservative default for ~4KB emulated EEPROM boards (ID75 rp2040/f103)
# after keymap (4 layers x 75 keys x 2B) + vial feature tables + overhead.
DEFAULT_MACRO_BUFFER_BYTES = 3000

TERMINATOR_ACTIONS = {
    "enter": [["tap", "KC_ENTER"]],
    "tab": [["tap", "KC_TAB"]],
    "none": [],
}

OPTIONS_RE = re.compile(r"<!--\s*vil-tool:\s*(.*?)\s*-->", re.DOTALL)
ROW_HEADING_RE = re.compile(r"^##\s*Row\s+(\d+)\s*(?:[—–-]\s*(.+?))?\s*$",
                            re.IGNORECASE)
POS_RE = re.compile(r"^\s*(\d+)\s*[,;/ ]\s*(\d+)\s*$")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

class Switch:
    __slots__ = ("row", "col", "name", "type", "force", "notes", "reserved")

    def __init__(self, row, col, name, type_, force, notes, reserved=False):
        self.row = row
        self.col = col
        self.name = name
        self.type = type_
        self.force = force
        self.notes = notes
        self.reserved = reserved

    @property
    def pos(self):
        return f"{self.row},{self.col}"

    def macro_text(self, include_force=True):
        """The string typed by the key (without terminator)."""
        if self.reserved:
            return None
        text = f"{self.type} - {self.name}" if self.type else self.name
        if include_force and self.force is not None:
            text += f" ({self.force:g}g)"
        return text


# ---------------------------------------------------------------------------
# switches.md parsing
# ---------------------------------------------------------------------------

def parse_options(md_text):
    """Read the '<!-- vil-tool: key=value ... -->' options comment."""
    opts = {"terminator": "enter", "include-force": "true", "auto-sort": "true"}
    m = OPTIONS_RE.search(md_text)
    if m:
        for token in m.group(1).split():
            if "=" in token:
                key, _, value = token.partition("=")
                opts[key.strip().lower()] = value.strip().lower()
    return opts


def _split_table_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def _is_separator_row(cells):
    return all(re.fullmatch(r":?-{2,}:?", c) or c == "" for c in cells)


def parse_inventory(path):
    """
    Parse switches.md.

    Returns (options: dict, sections: list of (heading_row, heading_type,
    [Switch])). Every Switch carries its own explicit (row, col) position.
    """
    md_text = Path(path).read_text(encoding="utf-8")
    options = parse_options(md_text)

    sections = []
    current = None  # [heading_row, heading_type, switches, header_map]
    seen_positions = {}

    for line_no, raw_line in enumerate(md_text.splitlines(), start=1):
        heading = ROW_HEADING_RE.match(raw_line.strip())
        if heading:
            if current:
                sections.append((current[0], current[1], current[2]))
            current = [int(heading.group(1)),
                       (heading.group(2) or "").strip(), [], None]
            continue

        if current is None:
            continue

        line = raw_line.strip()
        if not line.startswith("|"):
            continue

        cells = _split_table_row(raw_line)
        if _is_separator_row(cells):
            continue

        lowered = [c.lower() for c in cells]
        if current[3] is None:
            # Header row — remember column positions.
            if "switch" in lowered:
                header = {}
                for idx, name in enumerate(lowered):
                    if name.startswith("pos"):
                        header["pos"] = idx
                    elif name.startswith("switch"):
                        header["switch"] = idx
                    elif name.startswith("type"):
                        header["type"] = idx
                    elif name.startswith("force"):
                        header["force"] = idx
                    elif name.startswith("note"):
                        header["notes"] = idx
                current[3] = header
            continue

        header = current[3]

        def cell(key):
            idx = header.get(key)
            return cells[idx] if idx is not None and idx < len(cells) else ""

        name = cell("switch")
        if set(name) <= {"."} and name:  # skip "..." placeholder rows
            continue

        # Position — explicit "row,col" required.
        pos_raw = cell("pos")
        pm = POS_RE.match(pos_raw)
        if not pm:
            raise SystemExit(
                f"{path}:{line_no}: Pos column must be 'row,col' "
                f"(got {pos_raw!r}). Example: 2,13")
        row, col = int(pm.group(1)), int(pm.group(2))
        if (row, col) in seen_positions:
            raise SystemExit(
                f"{path}:{line_no}: duplicate position {row},{col} "
                f"(first seen on line {seen_positions[(row, col)]}).")
        seen_positions[(row, col)] = line_no

        if name == "" or name.upper() == "RESERVED":
            current[2].append(Switch(row, col, None, None, None,
                                     cell("notes"), reserved=True))
            continue

        type_ = cell("type") or current[1]
        if not type_:
            raise SystemExit(
                f"{path}:{line_no}: switch {name!r} has no Type and its "
                f"section heading has no default type.")

        force = None
        fm = re.search(r"(\d+(?:\.\d+)?)", cell("force"))
        if fm:
            force = float(fm.group(1))

        current[2].append(Switch(row, col, name, type_, force, cell("notes")))

    if current:
        sections.append((current[0], current[1], current[2]))

    return options, sections


def auto_sort_sections(sections):
    """
    Within each section, re-seat non-reserved switches across that section's
    non-reserved positions, heaviest -> lightest (positions in row-major
    order). Reserved positions stay put.
    """
    result = []
    for heading_row, heading_type, switches in sections:
        slots = sorted((s for s in switches if not s.reserved),
                       key=lambda s: (s.row, s.col))
        positions = [(s.row, s.col) for s in slots]
        ordered = sorted(slots, key=lambda s: -(s.force if s.force is not None
                                                else -1))
        for (row, col), sw in zip(positions, ordered):
            sw.row, sw.col = row, col
        merged = [s for s in switches if s.reserved] + ordered
        merged.sort(key=lambda s: (s.row, s.col))
        result.append((heading_row, heading_type, merged))
    return result


def all_switches(sections):
    return [s for _, _, switches in sections for s in switches]


# ---------------------------------------------------------------------------
# Macro construction & size accounting
# ---------------------------------------------------------------------------

def matrix_cols_from_template(vil):
    """Matrix column count = widest row in the template's layer 0."""
    layout = vil.get("layout")
    if layout and layout[0]:
        return max(len(r) for r in layout[0])
    return None


def build_macros(sections, options, macro_count, cols):
    """
    Build the .vil "macro" array. Macro index = row * cols + col
    (matching the firmware test layer). Unoccupied/reserved = empty macro.
    """
    terminator = TERMINATOR_ACTIONS.get(options.get("terminator", "enter"))
    if terminator is None:
        raise SystemExit(f"Unknown terminator option: {options.get('terminator')!r} "
                         f"(expected one of {sorted(TERMINATOR_ACTIONS)})")
    include_force = options.get("include-force", "true") == "true"

    macros = [[] for _ in range(macro_count)]
    for sw in all_switches(sections):
        index = sw.row * cols + sw.col
        if index >= macro_count:
            raise SystemExit(
                f"Position {sw.pos} maps to macro index {index}, but the "
                f"template only has {macro_count} macro slots. Wrong matrix "
                f"width ({cols} cols) or too-small DYNAMIC_KEYMAP_MACRO_COUNT.")
        text = sw.macro_text(include_force=include_force)
        if text is not None:
            macros[index] = [["text", text]] + [list(a) for a in terminator]
    return macros


def estimate_macro_bytes(macros):
    """
    Estimate on-device EEPROM usage of the macro buffer.

    Encoding (vial-qmk dynamic_keymap): text bytes are stored verbatim;
    a tap action costs 2 bytes (SS_TAP_CODE + keycode); every macro is
    terminated by a single NUL byte.
    """
    total = 0
    for macro in macros:
        for action in macro:
            kind = action[0]
            if kind == "text":
                total += len(action[1].encode("utf-8"))
            elif kind in ("tap", "down", "up"):
                total += 2
            elif kind == "delay":
                total += 4
        total += 1  # NUL terminator per macro
    return total


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def load_vil(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise SystemExit(
            f"Template not found: {path}\n"
            f"Export one from Vial first: File -> Save current layout.")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path} is not valid JSON: {exc}")


def resolve_cols(args, vil, sections):
    if getattr(args, "cols", None):
        return args.cols
    cols = matrix_cols_from_template(vil) if vil else None
    if cols is None:
        cols = max((s.col for s in all_switches(sections)), default=0) + 1
        print(f"NOTE: matrix width not found in template; inferred {cols} "
              f"columns from the inventory (override with --cols).")
    return cols


def cmd_generate(args):
    options, sections = parse_inventory(args.inventory)
    if options.get("auto-sort", "true") == "true":
        sections = auto_sort_sections(sections)

    vil = load_vil(args.template)
    macro_count = len(vil.get("macro", []))
    if macro_count == 0:
        raise SystemExit(
            "Template has no 'macro' array — is this really a Vial saved layout?")
    cols = resolve_cols(args, vil, sections)

    macros = build_macros(sections, options, macro_count, cols)
    used = estimate_macro_bytes(macros)
    switches = all_switches(sections)
    print(f"Positions: {len(switches)} "
          f"(reserved: {sum(1 for s in switches if s.reserved)})")
    print(f"Matrix width: {cols} cols; macro slots in template: {macro_count}")
    print(f"Estimated macro buffer usage: {used} / ~{args.buffer_size} bytes "
          f"({100 * used // args.buffer_size}%)")
    if used > args.buffer_size:
        raise SystemExit("ERROR: estimated usage exceeds the macro buffer — "
                         "shorten switch names or reduce entries.")

    vil["macro"] = macros
    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(vil, fh, indent=2)
        fh.write("\n")
    print(f"Wrote {args.output}")
    print("Load it in Vial: File -> Load saved layout")


def cmd_extract(args):
    vil = load_vil(args.vil)
    macros = vil.get("macro", [])
    cols = args.cols or matrix_cols_from_template(vil)
    if not cols:
        raise SystemExit("Cannot determine matrix width — pass --cols N.")

    text_re = re.compile(r"^(?P<type>[^-]+?)\s*-\s*(?P<name>.+?)"
                         r"(?:\s*\((?P<force>\d+(?:\.\d+)?)g\))?$")

    by_row = {}
    count = 0
    for index, macro in enumerate(macros):
        text = "".join(a[1] for a in macro if a and a[0] == "text").strip()
        if not text:
            continue
        count += 1
        row, col = divmod(index, cols)
        m = text_re.match(text)
        if m:
            entry = (col, m.group("name"), m.group("type").strip(),
                     m.group("force") or "", "")
        else:
            entry = (col, text, "", "", "unparsed")
        by_row.setdefault(row, []).append(entry)

    lines = [
        "# Switch Tester Inventory (extracted)",
        "",
        "<!-- vil-tool: terminator=enter  include-force=true  auto-sort=false -->",
    ]
    for row in sorted(by_row):
        lines += [
            "",
            f"## Row {row} — Mixed",
            "",
            "| Pos | Switch | Type | Force (g) | Notes |",
            "|-----|--------|------|----------:|-------|",
        ]
        for col, name, type_, force, notes in sorted(by_row[row]):
            lines.append(f"| {row},{col} | {name} | {type_} | {force} | {notes} |")

    Path(args.output).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Extracted {count} macro(s) ({cols} cols) -> {args.output}")


def cmd_check(args):
    options, sections = parse_inventory(args.inventory)
    vil = load_vil(args.template) if Path(args.template).exists() else None
    macro_count = len(vil.get("macro", [])) if vil else None
    cols = resolve_cols(args, vil, sections)

    switches = all_switches(sections)
    max_index = max((s.row * cols + s.col for s in switches), default=-1)
    macros = build_macros(sections, options,
                          max(macro_count or 0, max_index + 1), cols)
    used = estimate_macro_bytes(macros)

    print(f"Inventory:        {args.inventory}")
    print(f"Sections:         {len(sections)}")
    print(f"Positions:        {len(switches)} "
          f"(reserved: {sum(1 for s in switches if s.reserved)})")
    print(f"Matrix width:     {cols} cols; highest macro index: {max_index}")
    if macro_count is not None:
        status = "OK" if max_index < macro_count else "TOO MANY"
        print(f"Template slots:   {macro_count}  [{status}]")
    print(f"Estimated usage:  {used} / ~{args.buffer_size} bytes "
          f"({100 * used // args.buffer_size}%)")
    if used > args.buffer_size:
        print("RESULT: FAIL — shorten names or reduce entries.")
        sys.exit(1)
    print("RESULT: OK")


def cmd_report(args):
    options, sections = parse_inventory(args.inventory)
    if options.get("auto-sort", "true") == "true":
        sections = auto_sort_sections(sections)
    include_force = options.get("include-force", "true") == "true"
    cols = args.cols or (max((s.col for s in all_switches(sections)),
                             default=0) + 1)

    for heading_row, heading_type, switches in sections:
        title = f"Row {heading_row}" + (f" — {heading_type}" if heading_type else "")
        print(f"\n{title}")
        print("-" * 64)
        for sw in sorted(switches, key=lambda s: (s.row, s.col)):
            index = sw.row * cols + sw.col
            if sw.reserved:
                print(f"  M{index:<3} pos {sw.pos:<6} [RESERVED]"
                      + (f"   # {sw.notes}" if sw.notes else ""))
            else:
                print(f"  M{index:<3} pos {sw.pos:<6} "
                      f"{sw.macro_text(include_force=include_force)}"
                      + (f"   # {sw.notes}" if sw.notes else ""))
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Switch Tester inventory <-> Vial .vil tool")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("generate", help="build a .vil from switches.md + template")
    p.add_argument("-i", "--inventory", default=DEFAULT_INVENTORY)
    p.add_argument("-t", "--template", default=DEFAULT_TEMPLATE)
    p.add_argument("-o", "--output", default=DEFAULT_OUTPUT)
    p.add_argument("--cols", type=int,
                   help="matrix column count (default: from template layout)")
    p.add_argument("--buffer-size", type=int, default=DEFAULT_MACRO_BUFFER_BYTES,
                   help="assumed EEPROM macro buffer size in bytes")
    p.set_defaults(func=cmd_generate)

    p = sub.add_parser("extract", help="pull macros out of a .vil into markdown")
    p.add_argument("vil", help="exported .vil file")
    p.add_argument("-o", "--output", default="switches_extracted.md")
    p.add_argument("--cols", type=int,
                   help="matrix column count (default: from .vil layout)")
    p.set_defaults(func=cmd_extract)

    p = sub.add_parser("check", help="validate inventory + estimate buffer usage")
    p.add_argument("-i", "--inventory", default=DEFAULT_INVENTORY)
    p.add_argument("-t", "--template", default=DEFAULT_TEMPLATE)
    p.add_argument("--cols", type=int)
    p.add_argument("--buffer-size", type=int, default=DEFAULT_MACRO_BUFFER_BYTES)
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("report", help="print position -> switch cheat sheet")
    p.add_argument("-i", "--inventory", default=DEFAULT_INVENTORY)
    p.add_argument("--cols", type=int)
    p.set_defaults(func=cmd_report)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()