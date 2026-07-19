#!/usr/bin/env python3
"""Check ALL switch footprint pairs on a generated PCB for pad overlap /
insufficient clearance. Parses the kicad_pcb s-expression, extracts each
switch footprint's placement and pad geometry, and reports the tightest
pairs (pad-edge to pad-edge distance).

Usage: python scripts/check_choc_overlaps.py [pcb_path] [clearance_mm]
"""
import math
import re
import sys

PCB = sys.argv[1] if len(sys.argv) > 1 else 'ergogen/out_choc/ergogen/pcbs/biaxial_choc.kicad_pcb'
CLEARANCE = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5  # min pad-edge gap


def tokenize(text):
    return re.findall(r'\(|\)|"[^"]*"|[^\s()"]+', text)


def parse(tokens, i=0):
    """Parse s-expression tokens into nested lists."""
    assert tokens[i] == '('
    i += 1
    out = []
    while tokens[i] != ')':
        if tokens[i] == '(':
            node, i = parse(tokens, i)
            out.append(node)
        else:
            out.append(tokens[i])
            i += 1
    return out, i + 1


def find_all(node, name):
    for child in node:
        if isinstance(child, list) and child and child[0] == name:
            yield child


def first(node, name):
    for c in find_all(node, name):
        return c
    return None


def main():
    text = open(PCB, encoding='utf-8').read()
    tokens = tokenize(text)
    tree, _ = parse(tokens, 0)

    switches = []  # (ref, x, y, rot, [(px, py, pr)])  pr = pad bounding radius
    for fp in find_all(tree, 'footprint'):
        name = fp[1].strip('"')
        if 'switch' not in name:
            continue
        at = first(fp, 'at')
        fx, fy = float(at[1]), float(at[2])
        frot = float(at[3]) if len(at) > 3 else 0.0
        ref = ''
        for prop in find_all(fp, 'property'):
            if prop[1].strip('"') == 'Reference':
                ref = prop[2].strip('"')
        c, s = math.cos(math.radians(frot)), math.sin(math.radians(frot))
        pads = []
        for pad in find_all(fp, 'pad'):
            pat = first(pad, 'at')
            psize = first(pad, 'size')
            if not pat or not psize:
                continue
            dx, dy = float(pat[1]), float(pat[2])
            w, h = float(psize[1]), float(psize[2])
            # KiCad: pad offsets rotate with the footprint (y-down; rotation
            # sign consistent within the file, fine for distance checks)
            ax = fx + dx * c + dy * s
            ay = fy - dx * s + dy * c
            pads.append((ax, ay, math.hypot(w, h) / 2))
        switches.append((ref or name, fx, fy, frot, pads))

    print(f"switch footprints: {len(switches)}")
    results = []
    for i in range(len(switches)):
        for j in range(i + 1, len(switches)):
            r1, x1, y1, _, p1 = switches[i]
            r2, x2, y2, _, p2 = switches[j]
            if math.hypot(x2 - x1, y2 - y1) > 40:
                continue  # not neighbors
            gap = min(math.hypot(bx - ax, by - ay) - (ar + br)
                      for ax, ay, ar in p1 for bx, by, br in p2)
            results.append((gap, r1, r2, math.hypot(x2 - x1, y2 - y1)))
    results.sort()
    bad = [r for r in results if r[0] < CLEARANCE]
    print(f"\nTightest 12 pairs (pad-edge gap, refs, center dist):")
    for gap, r1, r2, d in results[:12]:
        flag = "  << TOO CLOSE" if gap < CLEARANCE else ""
        print(f"  {gap:7.2f} mm  {r1:>4} - {r2:<4}  centers {d:.2f} mm{flag}")
    if bad:
        print(f"\nWARNING: {len(bad)} pair(s) under {CLEARANCE} mm pad clearance")
        sys.exit(1)
    print(f"\nOK: all pairs have >= {CLEARANCE} mm pad clearance")


if __name__ == '__main__':
    main()