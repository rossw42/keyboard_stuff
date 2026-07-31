"""
keyboard.json -> vial.json Converter (Correct KLE Format Implementation)

The vial.json "layouts.keymap" field is a standard KLE (keyboard-layout-editor)
serialized document:

  - keymap is a list of ROWS
  - each row is a flat list mixing property dicts and label strings
  - property dicts apply to the NEXT key: {"x": gap, "y": gap, "w": width,
    "h": height, "r"/"rx"/"ry": rotation, "d": decal, ...}
  - "x"/"y" are RELATIVE offsets (gaps), NOT absolute coordinates
  - each new row automatically advances y by 1 and resets x to the rotation
    anchor (rx, default 0)
  - key labels are "row,col" matrix coordinates; layout-option keys carry a
    suffix on legend line 3: "row,col\n\n\ngroup,choice"
  - ENCODER entries have legend line 9 equal to "e" and their leading pair is
    "encoderIndex,direction" (0=CCW, 1=CW), NOT a matrix coordinate:
    "0,0\n\n\n\n\n\n\n\n\ne" / "0,1\n\n\n\n\n\n\n\n\ne"

The previous converter produced one pseudo-row per key with ABSOLUTE x values,
which is not valid KLE and rendered no usable keys in Vial.

This module converts a QMK keyboard.json layout (entries like
{"matrix": [r, c], "x": X, "y": Y, "w": W, "h": H}) into a proper KLE keymap
by grouping keys into visual rows (by y, per rotation cluster), sorting by x,
and emitting relative offsets.  Encoders defined in keyboard.json are emitted
as Vial encoder entries.  The electrical matrix size is derived from
matrix_pins (doubled rows for split keyboards, direct-pin matrices supported)
with a config.h MATRIX_ROWS/MATRIX_COLS fallback for custom matrices.

It also provides a faithful KLE parser (kle-serial semantics, including the
JS falsy-zero quirk for r/rx/ry) so generated and real keymaps can be compared
by their absolute key geometry and matrix labels.
"""

import json
import os
import re
from collections import OrderedDict


# ---------------------------------------------------------------------------
# lenient JSON loading (QMK repos contain files with // comments, trailing
# commas, and even missing commas between members)
# ---------------------------------------------------------------------------

def _strip_line_comments(text):
    """Remove // comments outside of strings."""
    out = []
    in_str = False
    escape = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_str:
            out.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
            i += 1
            continue
        if ch == '"':
            in_str = True
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _repair_json(text):
    text = _strip_line_comments(text)
    # remove trailing commas:  , }  or  , ]
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    # insert missing commas between a closing brace/bracket/string/number
    # and a following string key on the next line
    text = re.sub(r'([}\]"])(\s*\n\s*)"', r'\1,\2"', text)
    # the above may re-introduce a comma before a closing brace on rare
    # patterns; clean trailing commas again
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    return text


def load_json(path):
    """Load JSON, tolerating //-comments, trailing and missing commas."""
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    try:
        return json.loads(raw)
    except ValueError:
        return json.loads(_repair_json(raw))


def _deep_merge(base, override):
    """Recursively merge override into base (dicts merged, others replaced)."""
    out = dict(base)
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_keyboard_config(kb_path):
    """Load a keyboard.json with QMK-style directory inheritance.

    QMK keyboard definitions are layered: a leaf keyboard.json (e.g.
    keyboards/keychron/q11/ansi_encoder/keyboard.json) inherits fields such
    as matrix_pins, encoder, split and usb from parent-directory info.json /
    keyboard.json files (e.g. keyboards/keychron/q11/info.json).  This walks
    from the 'keyboards' root down to the leaf, deep-merging every
    info.json / keyboard.json found along the way (leaf wins).
    """
    kb_path = os.path.abspath(kb_path)
    leaf_dir = os.path.dirname(kb_path)

    # collect directory chain up to (and excluding) the 'keyboards' root
    chain = []
    d = leaf_dir
    while True:
        chain.append(d)
        parent = os.path.dirname(d)
        if not parent or parent == d:
            break
        if os.path.basename(d).lower() == "keyboards":
            chain.pop()  # don't include the keyboards dir itself
            break
        d = parent
    chain.reverse()  # topmost parent first

    merged = {}
    for directory in chain:
        for fname in ("info.json", "keyboard.json"):
            p = os.path.join(directory, fname)
            if os.path.normcase(p) == os.path.normcase(kb_path):
                continue  # merge the requested leaf file last
            if os.path.isfile(p):
                try:
                    data = load_json(p)
                    if isinstance(data, dict):
                        merged = _deep_merge(merged, data)
                except Exception:
                    pass
    try:
        leaf = load_json(kb_path)
    except Exception:
        leaf = None
    if isinstance(leaf, dict):
        merged = _deep_merge(merged, leaf)
    return merged if merged else None


def num(v):
    """Return int when integral, else float (cleaner JSON output)."""
    f = float(v)
    if f == int(f):
        return int(f)
    return round(f, 6)


# ---------------------------------------------------------------------------
# KLE parsing (kle-serial semantics)
# ---------------------------------------------------------------------------

def parse_kle(keymap):
    """Parse a KLE keymap (list of rows) into absolute-positioned keys.

    Returns a list of dicts:
      {label, x, y, w, h, r, rx, ry, decal}
    Follows kle-serial semantics, including the JS falsy check quirk:
    r/rx/ry values of 0 do NOT trigger state changes.
    """
    keys = []
    x = 0.0
    y = 0.0
    r = 0.0
    rot_x = 0.0
    rot_y = 0.0
    cluster_x = 0.0
    cluster_y = 0.0

    for row in keymap:
        if not isinstance(row, list):
            # Some KLE documents start with a metadata dict; skip it.
            continue
        w = 1.0
        h = 1.0
        decal = False
        for item in row:
            if isinstance(item, dict):
                if item.get("r"):
                    r = float(item["r"])
                if item.get("rx"):
                    rot_x = cluster_x = float(item["rx"])
                    x = cluster_x
                    y = cluster_y
                if item.get("ry"):
                    rot_y = cluster_y = float(item["ry"])
                    x = cluster_x
                    y = cluster_y
                x += float(item.get("x", 0) or 0)
                y += float(item.get("y", 0) or 0)
                if item.get("w"):
                    w = float(item["w"])
                if item.get("h"):
                    h = float(item["h"])
                if item.get("d"):
                    decal = True
            else:
                keys.append({
                    "label": str(item),
                    "x": x, "y": y, "w": w, "h": h,
                    "r": r, "rx": rot_x, "ry": rot_y,
                    "decal": decal,
                })
                x += w
                w = 1.0
                h = 1.0
                decal = False
        # end of row
        y += 1.0
        x = rot_x
    return keys


def split_label(label):
    """Split a KLE label into (primary, option, is_encoder).

    primary    = matrix coordinate text on legend line 0 (e.g. "3,6"), or
                 "encIdx,dir" for encoder entries
    option     = layout-option text on legend line 3 (e.g. "1,0") or None
    is_encoder = True when legend line 9 is "e"
    """
    parts = label.split("\n")
    primary = parts[0] if parts else ""
    option = parts[3] if len(parts) > 3 and parts[3] else None
    is_encoder = len(parts) > 9 and parts[9] == "e"
    return primary, option, is_encoder


ENCODER_SUFFIX = "\n\n\n\n\n\n\n\n\ne"


def encoder_label(index, direction):
    """Vial encoder keymap label: 'index,direction' + line-9 'e' marker."""
    return "{},{}{}".format(index, direction, ENCODER_SUFFIX)


# ---------------------------------------------------------------------------
# KLE serialization (from absolute keys to rows with relative offsets)
# ---------------------------------------------------------------------------

def serialize_kle(keys):
    """Serialize absolute-positioned keys into KLE rows.

    keys: list of dicts {label, x, y, w, h, r, rx, ry}
    Rotation clusters are emitted after non-rotated keys, ordered so that
    r/rx/ry never need to be reset back to zero (KLE parsers ignore
    zero-valued r/rx/ry due to JS falsy checks).
    """
    if not keys:
        return []

    # group keys by rotation state
    groups = OrderedDict()
    for k in keys:
        gk = (float(k.get("r", 0)), float(k.get("rx", 0)), float(k.get("ry", 0)))
        groups.setdefault(gk, []).append(k)

    # order: non-rotated group first, then ascending (rx, ry, r) so we never
    # transition a nonzero value back to zero
    def group_order(gk):
        r, rx, ry = gk
        is_rotated = 1 if (r or rx or ry) else 0
        return (is_rotated, rx, ry, r)

    ordered_groups = sorted(groups.items(), key=lambda kv: group_order(kv[0]))

    out_rows = []

    # simulated parser state
    sim_x = 0.0
    sim_y = 0.0
    sim_r = 0.0
    sim_rx = 0.0
    sim_ry = 0.0
    cl_x = 0.0
    cl_y = 0.0
    first_row = True

    for (r, rx, ry), gkeys in ordered_groups:
        # split group into visual rows by y, sort keys by x
        rows = OrderedDict()
        for k in sorted(gkeys, key=lambda k: (float(k["y"]), float(k["x"]))):
            rows.setdefault(float(k["y"]), []).append(k)

        for yv, rkeys in rows.items():
            if not first_row:
                sim_y += 1.0
                sim_x = sim_rx
            first_row = False

            props = OrderedDict()
            if r != sim_r and r != 0:
                props["r"] = num(r)
                sim_r = r
            if rx != sim_rx and rx != 0:
                props["rx"] = num(rx)
                sim_rx = rx
                cl_x = rx
                sim_x = cl_x
                sim_y = cl_y
            if ry != sim_ry and ry != 0:
                props["ry"] = num(ry)
                sim_ry = ry
                cl_y = ry
                sim_x = cl_x
                sim_y = cl_y
            if yv != sim_y:
                props["y"] = num(yv - sim_y)
                sim_y = yv

            row = []
            for i, k in enumerate(rkeys):
                p = props if i == 0 else OrderedDict()
                kx = float(k["x"])
                kw = float(k.get("w", 1))
                kh = float(k.get("h", 1))
                if kx != sim_x:
                    p["x"] = num(kx - sim_x)
                    sim_x = kx
                if kw != 1:
                    p["w"] = num(kw)
                if kh != 1:
                    p["h"] = num(kh)
                if p:
                    row.append(dict(p))
                row.append(k["label"])
                sim_x = kx + kw
            out_rows.append(row)

    return out_rows


# ---------------------------------------------------------------------------
# keyboard.json extraction
# ---------------------------------------------------------------------------

def derive_lighting(kb):
    feats = kb.get("features", {}) or {}
    has_rgb_matrix = bool(kb.get("rgb_matrix")) or bool(feats.get("rgb_matrix"))
    has_rgblight = bool(kb.get("rgblight")) or bool(feats.get("rgblight"))
    has_backlight = bool(kb.get("backlight")) or bool(feats.get("backlight"))
    if has_rgb_matrix:
        return "vialrgb"
    if has_backlight and has_rgblight:
        return "qmk_backlight_rgblight"
    if has_rgblight:
        return "qmk_rgblight"
    if has_backlight:
        return "qmk_backlight"
    return "none"


def is_split(kb):
    """Split keyboard detection: any 'split' config section that is not
    explicitly disabled means the electrical matrix rows are doubled."""
    split = kb.get("split")
    if not isinstance(split, dict) or not split:
        return False
    if split.get("enabled") is False:
        return False
    return True


def _parse_matrix_define(text, name):
    """Extract '#define NAME <value>' where value may be a plain integer
    or a simple product expression like '6*2' or '(6 * 2)' (used by split
    boards, e.g. viktus/sp111 'MATRIX_ROWS 6*2')."""
    m = re.search(r"#\s*define\s+{}\s+\(?\s*(\d+(?:\s*\*\s*\d+)*)\s*\)?"
                  .format(name), text)
    if not m:
        return None
    val = 1
    for part in m.group(1).split("*"):
        val *= int(part.strip())
    return val


def _config_h_matrix(kb_path):
    """Read MATRIX_ROWS / MATRIX_COLS from config.h, searching from the
    keyboard.json directory up to the keyboards/ root.  Boards with custom
    or non-standard matrices (e.g. doio/kb04 1x8 with only 5 col pins,
    aki27/cocot46plus 10x6) define the authoritative size there."""
    if not kb_path:
        return None, None
    directory = os.path.dirname(os.path.abspath(kb_path))
    rows = cols = None
    d = directory
    while True:
        cfg = os.path.join(d, "config.h")
        if os.path.isfile(cfg):
            try:
                with open(cfg, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read()
                if rows is None:
                    rows = _parse_matrix_define(text, "MATRIX_ROWS")
                if cols is None:
                    cols = _parse_matrix_define(text, "MATRIX_COLS")
            except OSError:
                pass
        if rows is not None and cols is not None:
            break
        parent = os.path.dirname(d)
        if not parent or parent == d or os.path.basename(d).lower() == "keyboards":
            break
        d = parent
    return rows, cols


def derive_matrix(kb, kb_path=None):
    """Derive the electrical matrix {rows, cols}.

    Priority:
      1. config.h MATRIX_ROWS/MATRIX_COLS (leaf dir, then parents) -
         authoritative for custom / non-standard matrices
      2. matrix_pins (rows/cols pin counts or direct-pin matrix),
         with rows doubled for split keyboards
      3. layout coordinate maximums (also used to detect transposed
         matrices, e.g. planck rev6: 4x12 pins wired as an 8x6 matrix)
    """
    # 1. config.h wins when it defines the size explicitly
    ch_rows, ch_cols = _config_h_matrix(kb_path)

    rows = None
    cols = None
    mp = kb.get("matrix_pins") or {}
    if mp.get("direct"):
        rows = len(mp["direct"])
        if rows and isinstance(mp["direct"][0], list):
            cols = max(len(rw) for rw in mp["direct"])
        if is_split(kb):
            rows *= 2
    else:
        if mp.get("rows"):
            rows = len(mp["rows"])
            if is_split(kb):
                rows *= 2
        if mp.get("cols"):
            cols = len(mp["cols"])

    if ch_rows is not None:
        rows = ch_rows
    if ch_cols is not None:
        cols = ch_cols

    # layout coordinate maximums
    max_r = -1
    max_c = -1
    for lay in (kb.get("layouts") or {}).values():
        for k in lay.get("layout", []):
            m = k.get("matrix")
            if isinstance(m, list) and len(m) == 2:
                try:
                    max_r = max(max_r, int(m[0]))
                    max_c = max(max_c, int(m[1]))
                except (TypeError, ValueError):
                    pass

    # transposed-matrix detection: layouts address more rows than the pin
    # matrix provides while the total electrical size is unchanged
    # (e.g. planck rev6: 4 row pins x 12 col pins wired as 8x6)
    if (ch_rows is None and ch_cols is None
            and rows is not None and cols is not None
            and max_r >= 0 and max_c >= 0
            and max_r + 1 > rows
            and (max_r + 1) * (max_c + 1) == rows * cols):
        rows = max_r + 1
        cols = max_c + 1

    # final fallback: layout maximums
    if rows is None and max_r >= 0:
        rows = max_r + 1
    if cols is None and max_c >= 0:
        cols = max_c + 1

    if rows and cols:
        return {"rows": rows, "cols": cols}
    return None


def encoder_count(kb):
    """Total number of rotary encoders (left + right half for splits).

    Vial numbers them 0..N-1; each contributes a CCW (dir 0) and CW (dir 1)
    keymap entry."""
    n = 0
    enc = kb.get("encoder") or {}
    rotary = enc.get("rotary") or []
    n += len(rotary)
    if is_split(kb):
        split_enc = (kb.get("split", {}).get("encoder") or {})
        right = (split_enc.get("right") or {}).get("rotary")
        if right is not None:
            n += len(right)
        elif rotary:
            # QMK mirrors the left-half encoder config on the right half
            # when no explicit right-side config is given
            n += len(rotary)
    return n


def layout_to_keys(layout_entries):
    """Convert keyboard.json layout entries into absolute key dicts for
    serialize_kle(). Entries without a matrix position are skipped."""
    keys = []
    for entry in layout_entries:
        if not isinstance(entry, dict):
            continue
        m = entry.get("matrix")
        if not (isinstance(m, list) and len(m) == 2):
            continue
        try:
            label = "{},{}".format(int(m[0]), int(m[1]))
        except (TypeError, ValueError):
            continue
        keys.append({
            "label": label,
            "x": float(entry.get("x", 0) or 0),
            "y": float(entry.get("y", 0) or 0),
            "w": float(entry.get("w", 1) or 1),
            "h": float(entry.get("h", 1) or 1),
            "r": float(entry.get("r", 0) or 0),
            "rx": float(entry.get("rx", 0) or 0),
            "ry": float(entry.get("ry", 0) or 0),
        })
    return keys


def encoder_keys(kb, existing_keys):
    """Build absolute key dicts for Vial encoder entries.

    They are placed on a fresh row below the physical layout; position is
    cosmetic - Vial identifies them purely by the 'e' legend and
    'index,direction' label."""
    n = encoder_count(kb)
    if n <= 0:
        return []
    base_y = 0.0
    if existing_keys:
        base_y = max(k["y"] + k.get("h", 1) for k in existing_keys)
    keys = []
    x = 0.0
    for i in range(n):
        for d in (0, 1):
            keys.append({
                "label": encoder_label(i, d),
                "x": x, "y": base_y, "w": 1.0, "h": 1.0,
                "r": 0.0, "rx": 0.0, "ry": 0.0,
            })
            x += 1.0
        x += 0.5  # gap between encoders
    return keys


def pick_layout(kb, layout_name=None):
    """Return (layout_name, layout_entries) from keyboard.json."""
    layouts = kb.get("layouts") or {}
    if not isinstance(layouts, dict) or not layouts:
        return None, []
    if layout_name and layout_name in layouts:
        return layout_name, layouts[layout_name].get("layout", [])
    # honor layout_aliases pointing LAYOUT at a specific layout
    aliases = kb.get("layout_aliases") or {}
    if not layout_name and "LAYOUT" in aliases and aliases["LAYOUT"] in layouts:
        name = aliases["LAYOUT"]
        return name, layouts[name].get("layout", [])
    # otherwise first layout in file order
    name = next(iter(layouts))
    return name, layouts[name].get("layout", [])


def build_layout_options(kb):
    """Derive Vial layout options from a multi-layout keyboard.json.

    Returns {"labels": [...], "keymap_keys": [...], "base": name} when a
    provably-correct option set can be derived and validated, else None.
    Correctness gate: the serialized KLE is re-parsed and every layout
    macro in keyboard.json must be reproduced EXACTLY (matrix ids +
    absolute geometry) by some option-choice combination under the Vial
    GUI's bounding-box re-anchoring semantics (see layout_options.py and
    the research/ docs).  Anything short of that returns None so callers
    fall back to the single-layout keymap."""
    from layout_options import build_options, validate_keymap

    layouts = kb.get("layouts") or {}
    if not isinstance(layouts, dict) or len(layouts) < 2:
        return None
    aliases = kb.get("layout_aliases") or {}
    preferred = aliases.get("LAYOUT") if aliases.get("LAYOUT") in layouts \
        else None
    try:
        opts = build_options(layouts, preferred_base=preferred)
    except Exception:
        return None
    if not opts:
        return None
    keymap = serialize_kle(opts["keys"])
    try:
        if not validate_keymap(keymap, layouts, opts["labels"]):
            return None
    except Exception:
        return None
    return {"labels": opts["labels"], "keys": opts["keys"],
            "base": opts["base"]}


# ---------------------------------------------------------------------------
# top-level conversion
# ---------------------------------------------------------------------------

def convert_keyboard_to_vial(kb_path, layout_name=None,
                             layout_options=True):
    """Convert a keyboard.json file into a vial.json dict.

    Applies QMK directory inheritance (parent info.json / keyboard.json
    files are merged in).  Returns (vial_dict, kb_data) or (None, None).
    """
    try:
        kb = load_keyboard_config(kb_path)
    except Exception as e:
        print("ERROR loading {}: {}: {}".format(kb_path, type(e).__name__, str(e)[:120]))
        return None, None
    if not isinstance(kb, dict):
        return None, None

    vial = convert_keyboard_data_to_vial(kb, layout_name=layout_name,
                                         kb_path=kb_path,
                                         layout_options=layout_options)
    return vial, kb


def convert_keyboard_data_to_vial(kb, layout_name=None, kb_path=None,
                                  layout_options=True):
    """Convert already-loaded keyboard.json data into a vial.json dict.

    When layout_options is True (default) and keyboard.json defines
    multiple layout macros, a Vial layout-option set (layouts.labels +
    per-key "g,c" tags) is derived and emitted - but ONLY when it passes
    the strict validate_keymap() gate proving every macro is reproduced
    exactly.  Otherwise the output is the single-layout keymap exactly as
    before."""
    usb = kb.get("usb", {}) or {}
    name = kb.get("keyboard_name") or ""

    vial = OrderedDict()
    vial["name"] = name
    vial["vendorId"] = str(usb.get("vid", "0xFEED"))
    vial["productId"] = str(usb.get("pid", "0x0000"))
    vial["lighting"] = derive_lighting(kb)

    matrix = derive_matrix(kb, kb_path)
    if matrix:
        vial["matrix"] = matrix

    opts = None
    if layout_options and not layout_name:
        opts = build_layout_options(kb)

    if opts:
        keys = opts["keys"] + encoder_keys(kb, opts["keys"])
        vial["layouts"] = {
            "labels": opts["labels"],
            "keymap": serialize_kle(keys),
        }
    else:
        _, layout_entries = pick_layout(kb, layout_name)
        keys = layout_to_keys(layout_entries)
        keys = keys + encoder_keys(kb, keys)
        vial["layouts"] = {"keymap": serialize_kle(keys)}
    return vial


# ---------------------------------------------------------------------------
# keymaps/via/keymap.c generation (research finding: via = copy of the
# default keymap, plus documented per-board divergence patches; see
# via_keymap_generator.py for the full knowledge base and evidence)
# ---------------------------------------------------------------------------

def generate_via_keymap_c(kb_path, output_root):
    """Generate keymaps/via/keymap.c for a board into a separate output
    folder (never into the source repo).

    Returns (generated_path, is_match, detail) where is_match reports the
    byte-for-byte comparison against the real keymaps/via/keymap.c when one
    exists (None when the board has no real via keymap to compare against).
    """
    from via_keymap_generator import (generate_via_keymap,
                                      verify_via_keymap,
                                      find_real_via_keymap)
    gen_path = generate_via_keymap(kb_path, output_root)
    if find_real_via_keymap(kb_path):
        ok, _, detail = verify_via_keymap(kb_path, gen_path)
        return gen_path, ok, detail
    return gen_path, None, "no real via keymap to compare against"


if __name__ == "__main__":
    import sys
    test_kb = r"D:\GitHub2\vial-qmk\keyboards\alps64\keyboard.json"
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        test_kb = args[0]

    vial, kb = convert_keyboard_to_vial(test_kb)
    if vial:
        print(json.dumps(vial, indent=2))
    else:
        print("Conversion failed for {}".format(test_kb))

    # optional: also generate keymaps/via/keymap.c alongside the vial.json
    if "--via-keymap" in sys.argv:
        out_root = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "out_via")
        try:
            gen_path, ok, detail = generate_via_keymap_c(test_kb, out_root)
            print("\nvia keymap.c generated: {}".format(gen_path))
            print("verification: {} - {}".format(
                "PASS" if ok else ("N/A" if ok is None else "FAIL"), detail))
        except Exception as e:
            print("\nvia keymap.c generation failed: {}: {}".format(
                type(e).__name__, e))
