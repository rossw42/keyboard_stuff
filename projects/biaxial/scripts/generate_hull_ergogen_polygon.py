#!/usr/bin/env python3
"""Patch ergogen/biaxial.ergogen.yaml with the EXACT Omnibus Hull outline.

Ergogen cannot import DXF outlines, so this script converts the hull outline
(same geometry as Omnibus_Hull.dxf / generate_biaxial_dxf.py: body + four
compound-arc mounting tab corners) into an ergogen `polygon` part by sampling
each arc into short segments, then rewrites the `_hull_body:` outline block
inside ergogen/biaxial.ergogen.yaml in place.

Coordinates are emitted relative to the hull body center, anchored at
(mid_x, mid_y) in the ergogen config; subsequent polygon points are relative
deltas (ergogen anchors each polygon point off the previous one).

Run from the biaxial project root:  python scripts/generate_hull_ergogen_polygon.py
"""
import math
import re

CONFIG = "ergogen/biaxial.ergogen.yaml"
ARC_SEGMENTS = 8          # segments per arc
TOL = 0.02                # chaining tolerance, mm

# Hull body center (from Omnibus_Hull.dxf bounds)
CX = (-233.3625 + 9.525) / 2   # -111.91875
CY = (-9.525 + 66.675) / 2     # 28.575

# --- Outline segments (exact values from Omnibus_Hull.dxf) ---
LINES = [
    ((11.85, 66.675), (-235.6875, 66.675)),      # top edge
    ((-235.6875, 61.325), (-234.8625, 61.325)),  # left top shoulder
    ((-233.3625, 59.825), (-233.3625, -2.675)),  # left inner tab edge
    ((-234.8625, -4.175), (-235.6875, -4.175)),  # left bottom shoulder
    ((-235.6875, -9.525), (11.85, -9.525)),      # bottom edge
    ((11.85, -4.175), (11.025, -4.175)),         # right bottom shoulder
    ((9.525, -2.675), (9.525, 59.825)),          # right inner tab edge
    ((11.025, 61.325), (11.85, 61.325)),         # right top shoulder
]
ARCS = [
    # left-top tab (5-arc compound)
    ((-235.6875, 64.0), 2.675, 90, 127.8792),
    ((-237.0229, 65.7167), 0.5, 127.8792, 258.8119),
    ((-237.3625, 64.0), 1.25, -78.8119, 78.8119),
    ((-237.0229, 62.2833), 0.5, 101.1881, 232.1208),
    ((-235.6875, 64.0), 2.675, 232.1208, 270),
    # left inner corners
    ((-234.8625, 59.825), 1.5, 0, 90),
    ((-234.8625, -2.675), 1.5, -90, 0),
    # left-bottom tab
    ((-235.6875, -6.85), 2.675, 90, 127.8792),
    ((-237.0229, -5.1333), 0.5, 127.8792, 258.8119),
    ((-237.3625, -6.85), 1.25, -78.8119, 78.8119),
    ((-237.0229, -8.5667), 0.5, 101.1881, 232.1208),
    ((-235.6875, -6.85), 2.675, 232.1208, 270),
    # right-bottom tab
    ((11.85, -6.85), 2.675, 270, 307.8792),
    ((13.1854, -8.5667), 0.5, -52.1208, 78.8119),
    ((13.525, -6.85), 1.25, 101.1881, 258.8119),
    ((13.1854, -5.1333), 0.5, -78.8119, 52.1208),
    ((11.85, -6.85), 2.675, 52.1208, 90),
    # right inner corners
    ((11.025, -2.675), 1.5, 180, 270),
    ((11.025, 59.825), 1.5, 90, 180),
    # right-top tab
    ((11.85, 64.0), 2.675, 270, 307.8792),
    ((13.1854, 62.2833), 0.5, -52.1208, 78.8119),
    ((13.525, 64.0), 1.25, 101.1881, 258.8119),
    ((13.1854, 65.7167), 0.5, -78.8119, 52.1208),
    ((11.85, 64.0), 2.675, 52.1208, 90),
]


def arc_points(center, r, sa, ea, n=ARC_SEGMENTS):
    cx, cy = center
    if ea <= sa:
        ea += 360
    return [(cx + r * math.cos(math.radians(sa + (ea - sa) * i / n)),
             cy + r * math.sin(math.radians(sa + (ea - sa) * i / n)))
            for i in range(n + 1)]


def build_path():
    segs = [[p1, p2] for p1, p2 in LINES]
    segs += [arc_points(c, r, sa, ea) for c, r, sa, ea in ARCS]

    def close(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1]) < TOL

    path = segs.pop(0)  # top edge, right -> left
    while segs:
        end = path[-1]
        for i, s in enumerate(segs):
            if close(s[0], end):
                path += s[1:]
                segs.pop(i)
                break
            if close(s[-1], end):
                path += list(reversed(s))[1:]
                segs.pop(i)
                break
        else:
            raise RuntimeError(f"Could not chain outline at {end}; {len(segs)} segments left")
    if not close(path[0], path[-1]):
        raise RuntimeError("Outline did not close")
    path.pop()  # drop duplicate closing point
    # dedupe consecutive near-identical points
    out = [path[0]]
    for p in path[1:]:
        if math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) > 0.005:
            out.append(p)
    return out


def emit_yaml_block(path):
    """_hull_body outline block: polygon anchored at hull center."""
    rel = [(round(x - CX, 4), round(y - CY, 4)) for x, y in path]
    lines = [
        "  # Omnibus Hull plate outline (EXACT geometry from Omnibus_Hull.dxf:",
        "  # 242.8875 x 76.2 mm body + four compound-arc mounting tab corners),",
        "  # arcs sampled at %d segments. Regenerate with" % ARC_SEGMENTS,
        "  # scripts/generate_hull_ergogen_polygon.py",
        "  _hull_body:",
        "    - what: polygon",
        "      points:",
    ]
    # First point: absolute from (0,0) -> hull center + offset
    def expr(base, v):
        return f"{base} - {abs(v)}" if v < 0 else f"{base} + {v}"
    x0, y0 = rel[0]
    lines.append(f'        - shift: ["{expr("mid_x", x0)}", "{expr("mid_y", y0)}"]')
    px, py = rel[0]
    for x, y in rel[1:]:
        dx, dy = round(x - px, 4), round(y - py, 4)
        lines.append(f"        - shift: [{dx}, {dy}]")
        px, py = x, y
    return "\n".join(lines) + "\n"


def patch_config(block):
    with open(CONFIG, "r", encoding="utf-8") as f:
        text = f.read()
    # Replace from the _hull_body comment/definition up to the next top-level
    # outline key at 2-space indent (_mounting_holes).
    pattern = re.compile(
        r"^  # Omnibus Hull plate.*?(?=^  _mounting_holes:)", re.S | re.M)
    if not pattern.search(text):
        raise RuntimeError("Could not locate _hull_body block in config")
    text = pattern.sub(block, text, count=1)
    with open(CONFIG, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    path = build_path()
    # sanity: bounding box should span the tabs
    xs = [p[0] for p in path]
    ys = [p[1] for p in path]
    print(f"Hull outline: {len(path)} points, "
          f"bbox {min(xs):.2f}..{max(xs):.2f} x {min(ys):.2f}..{max(ys):.2f} "
          f"({max(xs)-min(xs):.2f} x {max(ys)-min(ys):.2f} mm)")
    block = emit_yaml_block(path)
    patch_config(block)
    print(f"Patched {CONFIG} with exact hull polygon")


if __name__ == "__main__":
    main()