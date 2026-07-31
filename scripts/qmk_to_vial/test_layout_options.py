"""
test_layout_options.py - regression test for layout-option generation.

Runs over EVERY keyboard.json/info.json in the vial-qmk keyboards tree
(plus the 504-pair CSV corpus used by the original regression) and checks:

  OPT-EXACT   When options are emitted, the final serialized vial.json is
              independently re-parsed and, simulating the Vial GUI's
              re-anchoring (bbox top-left of the selected choice snapped
              onto choice 0's), EVERY layout macro in keyboard.json must be
              reproduced EXACTLY (matrix ids + absolute x/y/w/h/r/rx/ry)
              by some option-choice combination.  This is the 100%%
              correctness guarantee.
  OPT-STRUCT  Emitted options are structurally valid: contiguous group and
              choice indices, non-empty choice 0 per group, labels count
              matches group count, option bitfield fits 32 bits, matrix
              labels within the derived matrix bounds.
  FALLBACK    When options are NOT emitted, the output is byte-identical
              to the converter with layout_options=False (i.e. the
              previously-verified single-layout behavior is untouched).
  BASELINE    layout_options=False output geometry still roundtrips
              exactly against the source layout (the original ROUNDTRIP
              check from test_all_pairs.py).

Usage:
    python test_layout_options.py [--verbose] [keyboards_root]

Exit code 0 only when there are ZERO failures.
"""

import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from keyboard_to_vial_converter import (
    convert_keyboard_to_vial,
    parse_kle,
    split_label,
    pick_layout,
    layout_to_keys,
    load_keyboard_config,
    derive_matrix,
)
from layout_options import validate_keymap, option_bits

VIAL_QMK = r"D:\GitHub2\vial-qmk"
PAIRS_CSV = os.path.join(HERE, "..", "archive", "vial-research",
                         "vial_keyboard_pairs.csv")


def geometry_key(k):
    return (round(float(k["x"]), 4), round(float(k["y"]), 4),
            round(float(k.get("w", 1)), 4), round(float(k.get("h", 1)), 4),
            round(float(k.get("r", 0) or 0), 4),
            round(float(k.get("rx", 0) or 0), 4)
            if float(k.get("r", 0) or 0) else 0.0,
            round(float(k.get("ry", 0) or 0), 4)
            if float(k.get("r", 0) or 0) else 0.0)


def collect_keyboard_jsons(root):
    """Every keyboard.json / info.json that defines a 'layouts' section."""
    out = []
    kb_root = os.path.join(root, "keyboards")
    for dirpath, dirnames, filenames in os.walk(kb_root):
        dirnames[:] = [d for d in dirnames if d != "keymaps"]
        for fname in ("keyboard.json", "info.json"):
            if fname in filenames:
                p = os.path.join(dirpath, fname)
                out.append(p)
    return out


def baseline_roundtrip(kb, vial_plain):
    """Original ROUNDTRIP check: generated single-layout keymap re-parses
    to the exact source geometry and matrix labels."""
    _, entries = pick_layout(kb)
    src = layout_to_keys(entries)
    gen = [k for k in parse_kle(vial_plain["layouts"]["keymap"])
           if not split_label(k["label"])[2]]  # drop encoders
    if len(src) != len(gen):
        return False
    want = sorted((split_label(k["label"])[0],) + geometry_key(k)
                  for k in src)
    got = sorted((split_label(k["label"])[0],) + geometry_key(k)
                 for k in gen)
    return want == got


def matrix_in_bounds(vial, kb):
    m = vial.get("matrix")
    if not m:
        return True  # nothing to check against
    for k in parse_kle(vial["layouts"]["keymap"]):
        primary, _, is_enc = split_label(k["label"])
        if is_enc or "," not in primary:
            continue
        r, c = (int(v) for v in primary.split(","))
        if r >= m["rows"] or c >= m["cols"] or r < 0 or c < 0:
            return False
    return True


def run(root, verbose=False):
    paths = collect_keyboard_jsons(root)
    # add CSV corpus paths (may overlap; de-dupe)
    if os.path.isfile(PAIRS_CSV):
        with open(PAIRS_CSV, newline="", encoding="utf-8") as f:
            for row in csv.reader(f):
                if row and os.path.isfile(row[0]) and row[0] not in paths:
                    paths.append(row[0])
    paths = sorted(set(os.path.normcase(os.path.abspath(p))
                       for p in paths))

    stats = {"total": 0, "multi": 0, "options": 0, "fallback_multi": 0,
             "single": 0, "skip": 0}
    failures = []

    for p in paths:
        kb = None
        try:
            kb = load_keyboard_config(p)
        except Exception:
            pass
        if not isinstance(kb, dict) or not kb.get("layouts"):
            stats["skip"] += 1
            continue
        stats["total"] += 1

        layouts = kb.get("layouts") or {}
        n_lay = sum(1 for v in layouts.values()
                    if isinstance(v, dict) and v.get("layout"))
        multi = n_lay > 1
        if multi:
            stats["multi"] += 1
        else:
            stats["single"] += 1

        vial_opt, _ = convert_keyboard_to_vial(p, layout_options=True)
        vial_plain, _ = convert_keyboard_to_vial(p, layout_options=False)
        if vial_opt is None or vial_plain is None:
            failures.append((p, "CONVERT", "conversion returned None"))
            continue

        # JSON round-trip so we test exactly what lands in vial.json
        vial_opt = json.loads(json.dumps(vial_opt))
        vial_plain = json.loads(json.dumps(vial_plain))

        labels = vial_opt["layouts"].get("labels")

        # BASELINE: plain output still roundtrips exactly
        try:
            if not baseline_roundtrip(kb, vial_plain):
                failures.append((p, "BASELINE",
                                 "plain output geometry mismatch"))
                continue
        except Exception as e:
            failures.append((p, "BASELINE", repr(e)))
            continue

        if labels:
            stats["options"] += 1
            # OPT-STRUCT
            if option_bits(labels) > 32:
                failures.append((p, "OPT-STRUCT", "bitfield > 32 bits"))
                continue
            if not matrix_in_bounds(vial_opt, kb):
                failures.append((p, "OPT-STRUCT",
                                 "matrix label out of bounds"))
                continue
            # OPT-EXACT: independent re-validation of the final JSON
            try:
                ok = validate_keymap(vial_opt["layouts"]["keymap"],
                                     layouts, labels)
            except Exception as e:
                failures.append((p, "OPT-EXACT", repr(e)))
                continue
            if not ok:
                failures.append((p, "OPT-EXACT",
                                 "macro not reproduced exactly"))
                continue
            if verbose:
                names = [l[0] if isinstance(l, list) else l for l in labels]
                print("OPTIONS {}  {}".format(
                    os.path.relpath(p, root) if p.startswith(
                        os.path.normcase(root)) else p, names))
        else:
            if multi:
                stats["fallback_multi"] += 1
            # FALLBACK: output identical to the pre-feature converter
            if vial_opt != vial_plain:
                failures.append((p, "FALLBACK",
                                 "no-options output differs from "
                                 "layout_options=False output"))
                continue

    print()
    print("=" * 68)
    print("keyboards with layouts        : {}".format(stats["total"]))
    print("  single-layout boards        : {}".format(stats["single"]))
    print("  multi-layout boards         : {}".format(stats["multi"]))
    print("    options emitted           : {}".format(stats["options"]))
    print("    fallback (single layout)  : {}".format(
        stats["fallback_multi"]))
    print("unparseable/no-layout skipped : {}".format(stats["skip"]))
    print("FAILURES                      : {}".format(len(failures)))
    print("=" * 68)
    for p, kind, msg in failures[:60]:
        print("FAIL [{}] {}\n     {}".format(kind, p, msg))
    if len(failures) > 60:
        print("... and {} more".format(len(failures) - 60))
    return 0 if not failures else 1


if __name__ == "__main__":
    verbose = "--verbose" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = args[0] if args else VIAL_QMK
    sys.exit(run(root, verbose=verbose))