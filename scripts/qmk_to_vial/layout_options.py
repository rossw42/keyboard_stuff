"""
layout_options.py - derive Vial layout options ("labels" + per-key
group,choice tags) from a QMK keyboard.json that defines multiple layout
macros.

Background (see research/ docs in this folder):

* vial.json layout options are encoded per key as KLE legend line 3:
  "row,col\n\n\ngroup,choice".  layouts.labels[] names each group: a plain
  string = boolean checkbox, a list ["Title", "Choice0", "Choice1", ...] =
  dropdown.  Default-choice keys carry an explicit "g,0" tag (280/293 real
  vial.json files do this - research/vial_layout_options_format.md).
* The Vial GUI shows, per group, only the keys of the selected choice and
  rigidly translates that choice so its collective bounding-box top-left
  lands on the choice-0 group's bounding-box top-left
  (vial-gui keyboard_widget.py::place_widgets - see
  research/vial_gui_option_rendering.md).  Alternative-choice keys can
  therefore be drawn anywhere (convention: below the board), PROVIDED every
  choice of a group has the same native bounding-box top-left.  When it
  does not naturally, we duplicate nearby always-common keys into every
  choice - the same trick hand-made files (coseyfannitutti/mysterium ISO
  enter) use.

Algorithm (research/multi_layout_diff_analysis.md):
 1. Parse every layout macro into keys identified by (row, col, geometry).
 2. Pick a base layout (plain/community-named macro preferred).
 3. Diff every other macro against the base; cluster differing keys into
    connected regions by rectangle overlap.
 4. Merge overlapping regions across macros into option groups; each
    group's choices are the distinct forms the region takes per macro
    (choice 0 = base form).
 5. Stabilize each group's anchor (equal native bbox top-left across
    choices) by pulling in always-common neighbour keys.
 6. Emit: base board in place (choice-0 keys tagged "g,0"), alternative
    choices as blocks below the board, plus the labels list.
 7. Validate end-to-end (validate_keymap): parse the serialized KLE back,
    simulate the GUI re-anchoring, and require EVERY keyboard.json macro to
    be reproduced EXACTLY (matrix ids + absolute geometry) by some choice
    combination.  Callers fall back to single-layout output on any failure,
    so an emitted option set is correct by construction.
"""

import math
from collections import Counter, OrderedDict

EPS = 1e-4


# ---------------------------------------------------------------------------
# key parsing / geometry
# ---------------------------------------------------------------------------

def _f(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def parse_layout_keys(entries):
    """keyboard.json layout entries -> list of normalized key dicts.

    Entries without a valid matrix position are skipped (same rule as the
    single-layout converter).  rx/ry are normalized to 0 when r == 0."""
    keys = []
    for e in entries or []:
        if not isinstance(e, dict):
            continue
        m = e.get("matrix")
        if not (isinstance(m, list) and len(m) == 2):
            continue
        try:
            row, col = int(m[0]), int(m[1])
        except (TypeError, ValueError):
            continue
        r = _f(e.get("r", 0))
        keys.append({
            "row": row, "col": col,
            "x": _f(e.get("x", 0)), "y": _f(e.get("y", 0)),
            "w": _f(e.get("w", 1), 1.0), "h": _f(e.get("h", 1), 1.0),
            "r": r,
            "rx": _f(e.get("rx", 0)) if r else 0.0,
            "ry": _f(e.get("ry", 0)) if r else 0.0,
        })
    return keys


def key_ident(k):
    """Full identity of a key: matrix position + exact geometry."""
    return (k["row"], k["col"],
            round(k["x"], 4), round(k["y"], 4),
            round(k["w"], 4), round(k["h"], 4),
            round(k["r"], 4), round(k["rx"], 4), round(k["ry"], 4))


def key_bbox(k):
    """Axis-aligned bounding box of the (possibly rotated) key rectangle.

    Matches the Vial GUI, which anchors option groups on the bounding rect
    of the rotated key polygons."""
    if not k["r"]:
        return (k["x"], k["y"], k["x"] + k["w"], k["y"] + k["h"])
    ang = math.radians(k["r"])
    ca, sa = math.cos(ang), math.sin(ang)
    rx, ry = k["rx"], k["ry"]
    pts = []
    for px, py in ((k["x"], k["y"]),
                   (k["x"] + k["w"], k["y"]),
                   (k["x"], k["y"] + k["h"]),
                   (k["x"] + k["w"], k["y"] + k["h"])):
        dx, dy = px - rx, py - ry
        pts.append((rx + dx * ca - dy * sa, ry + dx * sa + dy * ca))
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))


def _union_bbox(keys):
    bbs = [key_bbox(k) for k in keys]
    return (min(b[0] for b in bbs), min(b[1] for b in bbs),
            max(b[2] for b in bbs), max(b[3] for b in bbs))


def _tl(keys):
    """Group anchor as the GUI computes it: independent min-x / min-y over
    the keys' bounding boxes."""
    bbs = [key_bbox(k) for k in keys]
    return (min(b[0] for b in bbs), min(b[1] for b in bbs))


def _overlap(a, b, eps=0.01):
    """True when rectangles a and b overlap with positive area (touching
    edges do NOT count, so adjacent keys don't chain into one region)."""
    return (a[0] + eps < b[2] and b[0] + eps < a[2]
            and a[1] + eps < b[3] and b[1] + eps < a[3])


# ---------------------------------------------------------------------------
# clustering / grouping
# ---------------------------------------------------------------------------

def _cluster(tagged):
    """Union-find clustering of (tag, key) items by bbox overlap."""
    n = len(tagged)
    if n == 0:
        return []
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    bbs = [key_bbox(k) for _, k in tagged]
    for i in range(n):
        for j in range(i + 1, n):
            if _overlap(bbs[i], bbs[j]):
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[ri] = rj
    out = OrderedDict()
    for i in range(n):
        out.setdefault(find(i), []).append(tagged[i])
    return list(out.values())


def _base_candidates(names, preferred=None):
    """Order layout names by suitability as the base (default) layout:
    explicit preference (layout_aliases LAYOUT target), then plain LAYOUT,
    then non-'_all' names with the fewest tokens, then file order."""
    def score(item):
        i, n = item
        nl = n.lower()
        return (0 if (preferred and n == preferred) else 1,
                0 if nl == "layout" else 1,
                1 if nl.endswith("_all") else 0,
                len(nl.split("_")),
                i)
    return [n for _, n in sorted(enumerate(names), key=lambda t: score(t))]


# ---------------------------------------------------------------------------
# anchor stabilization
# ---------------------------------------------------------------------------

def _stabilize(choices, pool, used):
    """Return extra always-common keys to duplicate into every choice so
    that all choices share the same native bbox top-left (the GUI anchor),
    or None when impossible.

    Because extras appear in EVERY choice, each added key affects all
    anchors identically: TL_c = (min(choice_minx, extras_minx),
    min(choice_miny, extras_miny)).  Adding a key at or left of / above the
    global minimum therefore equalizes that axis for all choices."""
    extras = OrderedDict()
    for _ in range(400):
        aug = [list(ch) + list(extras.values()) for ch in choices]
        has_empty = any(not a for a in aug)
        if not has_empty:
            tls = [_tl(a) for a in aug]
            tx = min(t[0] for t in tls)
            ty = min(t[1] for t in tls)
            bad_x = any(t[0] - tx > EPS for t in tls)
            bad_y = any(t[1] - ty > EPS for t in tls)
            if not bad_x and not bad_y:
                return list(extras.values())
        else:
            allk = [k for a in aug for k in a]
            if not allk:
                return None
            ub = _union_bbox(allk)
            tx, ty = ub[0], ub[1]
            bad_x = bad_y = False  # just need any nearby key

        best = None
        for ident, k in pool.items():
            if ident in used or ident in extras:
                continue
            bb = key_bbox(k)
            if not has_empty:
                if bad_x and bb[0] > tx + EPS:
                    continue
                if (not bad_x) and bad_y and bb[1] > ty + EPS:
                    continue
            d = (tx - bb[0]) ** 2 + (ty - bb[1]) ** 2
            if best is None or d < best[0]:
                best = (d, ident, k)
        if best is None:
            return None
        extras[best[1]] = best[2]
    return None


# ---------------------------------------------------------------------------
# naming (cosmetic only - correctness is guaranteed by validate_keymap)
# ---------------------------------------------------------------------------

def _fmt_num(v):
    f = float(v)
    if abs(f - round(f)) < 1e-9:
        return str(int(round(f)))
    return ("%.4f" % f).rstrip("0").rstrip(".")


def _region_name(region_keys, board_bb, used_names):
    if not region_keys:
        base = "Layout"
    else:
        bb = _union_bbox(region_keys)
        bw = max(board_bb[2] - board_bb[0], 1e-6)
        bh = max(board_bb[3] - board_bb[1], 1e-6)
        rel_x = ((bb[0] + bb[2]) / 2.0 - board_bb[0]) / bw
        rel_y = ((bb[1] + bb[3]) / 2.0 - board_bb[1]) / bh
        width = bb[2] - bb[0]
        if width >= 0.5 * bw:
            base = "Bottom Row" if rel_y > 0.6 else "Layout"
        elif rel_y >= 0.75:
            if rel_x < 0.35:
                base = "Bottom Left"
            elif rel_x > 0.65:
                base = "Bottom Right"
            else:
                base = "Space"
        elif rel_y <= 0.25:
            if rel_x > 0.6:
                base = "Backspace"
            elif rel_x < 0.4:
                base = "Top Left"
            else:
                base = "Top Row"
        else:
            if rel_x > 0.65:
                base = "Enter" if rel_y < 0.6 else "Right Shift"
            elif rel_x < 0.35:
                base = "Left Shift" if rel_y >= 0.5 else "Left Side"
            else:
                base = "Layout"
    name = base
    i = 2
    while name in used_names:
        name = "{} {}".format(base, i)
        i += 1
    used_names.add(name)
    return name


def _choice_desc(keys, idx):
    if not keys:
        return "None"
    ws = sorted((float(k["w"]) for k in keys), reverse=True)
    if len(keys) == 1:
        return _fmt_num(ws[0]) + "u"
    if ws[0] >= 3:
        return "{}u Space".format(_fmt_num(ws[0]))
    if all(abs(w - 1.0) < 1e-6 for w in ws):
        return "Split" if len(keys) <= 3 else "{} keys".format(len(keys))
    return "Option {}".format(idx + 1)


def _choice_descs(choices):
    descs = [_choice_desc(ch, i) for i, ch in enumerate(choices)]
    if len(set(descs)) != len(descs):
        descs = ["Option {}".format(i + 1) for i in range(len(choices))]
    return descs


def option_bits(labels):
    """Total bits the option bitfield uses (VIA/Vial packing: checkbox = 1
    bit, N-choice dropdown = (N-1).bit_length() bits)."""
    bits = 0
    for entry in labels or []:
        if isinstance(entry, list):
            n = max(len(entry) - 1, 2)
            bits += max(1, (n - 1).bit_length())
        else:
            bits += 1
    return bits


# ---------------------------------------------------------------------------
# derivation
# ---------------------------------------------------------------------------

def build_options(layouts_dict, preferred_base=None):
    """Derive layout options from a keyboard.json 'layouts' dict.

    Returns {"labels": [...], "keys": [key dicts with 'label' strings for
    serialize_kle()], "base": base_layout_name} or None when options cannot
    be derived (caller should fall back to single-layout output).

    The result still MUST be validated with validate_keymap() after KLE
    serialization; build_options alone does not guarantee correctness."""
    parsed = OrderedDict()
    for name, spec in (layouts_dict or {}).items():
        entries = spec.get("layout") if isinstance(spec, dict) else None
        ks = parse_layout_keys(entries)
        if ks:
            parsed[name] = ks
    if len(parsed) < 2:
        return None

    for base_name in _base_candidates(list(parsed.keys()), preferred_base):
        try:
            res = _derive(parsed, base_name)
        except Exception:
            res = None
        if res is not None:
            return res
    return None


def _derive(parsed, base_name):
    layout_idents = {}
    for n, ks in parsed.items():
        d = OrderedDict()
        for k in ks:
            i = key_ident(k)
            if i in d:
                return None  # duplicate key within one layout - bail out
            d[i] = k
        layout_idents[n] = d
    base_ids = layout_idents[base_name]

    # ---- per-layout diff vs base, clustered into regions ----
    clusters = []
    for n in parsed:
        if n == base_name:
            continue
        ids = layout_idents[n]
        removed = [base_ids[i] for i in base_ids if i not in ids]
        added = [ids[i] for i in ids if i not in base_ids]
        if not removed and not added:
            continue
        tagged = [("b", k) for k in removed] + [(n, k) for k in added]
        for cl in _cluster(tagged):
            clusters.append({
                "layout": n,
                "base": OrderedDict((key_ident(k), k)
                                    for t, k in cl if t == "b"),
                "added": OrderedDict((key_ident(k), k)
                                     for t, k in cl if t != "b"),
            })
    if not clusters:
        return None  # every layout is identical to the base

    # ---- merge clusters across layouts into option groups ----
    n_cl = len(clusters)
    parent = list(range(n_cl))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    cl_bbs = []
    for c in clusters:
        cl_bbs.append(_union_bbox(list(c["base"].values())
                                  + list(c["added"].values())))
    for i in range(n_cl):
        for j in range(i + 1, n_cl):
            if find(i) == find(j):
                continue
            share_base = bool(set(clusters[i]["base"])
                              & set(clusters[j]["base"]))
            if share_base or _overlap(cl_bbs[i], cl_bbs[j]):
                parent[find(i)] = find(j)

    merged = OrderedDict()
    for i, c in enumerate(clusters):
        g = merged.setdefault(find(i), {"base": OrderedDict(),
                                        "forms": OrderedDict()})
        for ident, k in c["base"].items():
            g["base"][ident] = k
        fa = g["forms"].setdefault(c["layout"], OrderedDict())
        for ident, k in c["added"].items():
            fa[ident] = k
    groups = list(merged.values())
    # deterministic group order: by region position (y, x)
    groups.sort(key=lambda g: _tl(list(g["base"].values())
                                  or [k for f in g["forms"].values()
                                      for k in f.values()]))

    # ---- build choices per group ----
    assigned = set()
    for g in groups:
        assigned.update(g["base"].keys())
    pool = OrderedDict((i, k) for i, k in base_ids.items()
                       if i not in assigned)
    used = set()

    out_groups = []
    for g in groups:
        base_form = sorted(g["base"].values(),
                           key=lambda k: (k["y"], k["x"]))
        choices = [list(base_form)]
        sigs = {frozenset(g["base"].keys()): 0}
        for n in parsed:  # original layouts-dict order
            if n not in g["forms"]:
                continue
            form = OrderedDict()
            for ident, k in g["base"].items():
                if ident in layout_idents[n]:
                    form[ident] = k
            for ident, k in g["forms"][n].items():
                form[ident] = k
            sig = frozenset(form.keys())
            if sig not in sigs:
                sigs[sig] = len(choices)
                choices.append(sorted(form.values(),
                                      key=lambda k: (k["y"], k["x"])))
        if len(choices) < 2:
            continue
        extras = _stabilize(choices, pool, used)
        if extras is None:
            return None
        for k in extras:
            used.add(key_ident(k))
        out_groups.append({"choices": choices, "extras": extras,
                           "region": base_form
                           or [k for ch in choices for k in ch]})
    if not out_groups:
        return None

    # ---- labels ----
    board_bb = _union_bbox(list(base_ids.values()))
    used_names = set()
    labels = []
    for g in out_groups:
        name = _region_name(g["region"], board_bb, used_names)
        labels.append([name] + _choice_descs(g["choices"]))
    if option_bits(labels) > 32:
        return None  # VIA layout options are a uint32 bitfield

    # ---- emit absolute keys ----
    def mk(k, tag):
        label = "{},{}".format(k["row"], k["col"])
        if tag is not None:
            label += "\n\n\n{},{}".format(tag[0], tag[1])
        return {"label": label,
                "x": k["x"], "y": k["y"], "w": k["w"], "h": k["h"],
                "r": k["r"], "rx": k["rx"], "ry": k["ry"]}

    keys_out = []
    extra_ids = used
    for ident, k in base_ids.items():
        if ident in assigned or ident in extra_ids:
            continue
        keys_out.append(mk(k, None))
    for gi, g in enumerate(out_groups):
        for k in g["choices"][0] + g["extras"]:
            keys_out.append(mk(k, (gi, 0)))
    if not keys_out:
        return None

    # alternative choices drawn as blocks below the board (cosmetic - the
    # GUI re-anchors them onto the choice-0 bbox top-left)
    main_bb = _union_bbox(
        [{"x": k["x"], "y": k["y"], "w": k["w"], "h": k["h"],
          "r": k["r"], "rx": k["rx"], "ry": k["ry"]} for k in keys_out])
    cur_y = main_bb[3] + 0.5
    for gi, g in enumerate(out_groups):
        for ci in range(1, len(g["choices"])):
            block = g["choices"][ci] + g["extras"]
            bb = _union_bbox(block)
            dx, dy = -bb[0], cur_y - bb[1]
            for k in block:
                kk = dict(k)
                kk["x"] = k["x"] + dx
                kk["y"] = k["y"] + dy
                if k["r"]:
                    kk["rx"] = k["rx"] + dx
                    kk["ry"] = k["ry"] + dy
                keys_out.append(mk(kk, (gi, ci)))
            cur_y += (bb[3] - bb[1]) + 0.25

    return {"labels": labels, "keys": keys_out, "base": base_name}


# ---------------------------------------------------------------------------
# validation: simulate the Vial GUI and require every macro to be exact
# ---------------------------------------------------------------------------

def _render_ident(rec, dx, dy):
    r = rec["r"]
    return (rec["row"], rec["col"],
            round(rec["x"] + dx, 4), round(rec["y"] + dy, 4),
            round(rec["w"], 4), round(rec["h"], 4),
            round(r, 4),
            round(rec["rx"] + dx, 4) if r else 0.0,
            round(rec["ry"] + dy, 4) if r else 0.0)


def _combo_match(remaining, group_ids, idx, groups, rendered):
    if idx == len(group_ids):
        return sum(remaining.values()) == 0
    gi = group_ids[idx]
    for ci in sorted(groups[gi]):
        form = rendered[(gi, ci)]
        if sum((form - remaining).values()) == 0:  # form is a sub-multiset
            if _combo_match(remaining - form, group_ids, idx + 1,
                            groups, rendered):
                return True
    return False


def validate_keymap(keymap, layouts_dict, labels=None):
    """Verify a serialized KLE keymap with layout options against the
    source keyboard.json layouts.

    Simulates the Vial GUI exactly: per (group, choice), keys are rigidly
    translated so the choice bbox top-left lands on the choice-0 bbox
    top-left.  Every layout macro in layouts_dict must then equal
    common-keys + one rendered choice per group, with EXACT matrix ids and
    absolute geometry.  Also checks structural rules (contiguous group and
    choice indices, non-empty choice 0)."""
    from keyboard_to_vial_converter import parse_kle, split_label

    keys = parse_kle(keymap)
    common = []
    groups = {}
    for k in keys:
        primary, option, is_enc = split_label(k["label"])
        if is_enc:
            continue
        if "," not in primary:
            return False
        try:
            row, col = (int(v) for v in primary.split(","))
        except ValueError:
            return False
        r = float(k.get("r", 0) or 0)
        rec = {"row": row, "col": col,
               "x": float(k["x"]), "y": float(k["y"]),
               "w": float(k.get("w", 1)), "h": float(k.get("h", 1)),
               "r": r,
               "rx": float(k.get("rx", 0) or 0) if r else 0.0,
               "ry": float(k.get("ry", 0) or 0) if r else 0.0}
        if option:
            try:
                gi, ci = (int(v) for v in option.split(","))
            except ValueError:
                return False
            groups.setdefault(gi, {}).setdefault(ci, []).append(rec)
        else:
            common.append(rec)

    # structural checks
    gis = sorted(groups)
    if gis != list(range(len(gis))):
        return False
    if labels is not None and len(labels) != len(gis):
        return False
    for gi in gis:
        cis = sorted(groups[gi])
        if cis != list(range(len(cis))) or len(cis) < 2:
            return False
        if not groups[gi][0]:
            return False
        if labels is not None:
            entry = labels[gi]
            n_choices = (len(entry) - 1) if isinstance(entry, list) else 2
            if len(cis) > max(n_choices, 2):
                return False

    # rendered form of every (group, choice) after GUI re-anchoring
    rendered = {}
    for gi in gis:
        tl0 = _tl(groups[gi][0])
        for ci, ks in groups[gi].items():
            if not ks:
                rendered[(gi, ci)] = Counter()
                continue
            tlc = _tl(ks)
            dx, dy = tl0[0] - tlc[0], tl0[1] - tlc[1]
            rendered[(gi, ci)] = Counter(
                _render_ident(rec, dx, dy) for rec in ks)
    common_cnt = Counter(_render_ident(rec, 0.0, 0.0) for rec in common)

    # every layout macro must be reproducible by some choice combination
    found_any = False
    for spec in (layouts_dict or {}).values():
        entries = spec.get("layout") if isinstance(spec, dict) else None
        lk = parse_layout_keys(entries)
        if not lk:
            continue
        found_any = True
        target = Counter(key_ident(k) for k in lk)
        if sum((common_cnt - target).values()):
            return False  # common keys must appear in every macro
        if not _combo_match(target - common_cnt, gis, 0, groups, rendered):
            return False
    return found_any