#!/usr/bin/env python3
"""Render a BiAxial hull plate DXF to a JPG image.

Usage: python generate_biaxial_jpg.py [dxf_file]
Defaults to the V2 plate DXF.
"""
import math
import sys
import ezdxf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Arc as MplArc

DXF_FILE = sys.argv[1] if len(sys.argv) > 1 else "dxf/biaxial_v2_hull_plate_mx.dxf"
OUT_FILE = DXF_FILE.rsplit('.', 1)[0] + ".jpg"

doc = ezdxf.readfile(DXF_FILE)
msp = doc.modelspace()

fig, ax = plt.subplots(1, 1, figsize=(16, 6), dpi=200)
ax.set_aspect('equal')
ax.set_facecolor('#1a1a1a')
fig.patch.set_facecolor('#1a1a1a')

# Color map by layer
colors = {
    'OUTLINE': '#cccccc',
    'SWITCHES': '#ff4444',
    'MOUNTING': '#44cc44',
}

for e in msp:
    layer = e.dxf.layer
    color = colors.get(layer, '#888888')
    lw = 1.2 if layer == 'OUTLINE' else 0.6

    if e.dxftype() == 'LINE':
        ax.plot([e.dxf.start.x, e.dxf.end.x],
                [e.dxf.start.y, e.dxf.end.y],
                color=color, linewidth=lw)

    elif e.dxftype() == 'ARC':
        cx, cy = e.dxf.center.x, e.dxf.center.y
        r = e.dxf.radius
        sa = e.dxf.start_angle
        ea = e.dxf.end_angle
        if ea <= sa:
            ea += 360
        theta = [sa + (ea - sa) * i / 64 for i in range(65)]
        xs = [cx + r * math.cos(math.radians(t)) for t in theta]
        ys = [cy + r * math.sin(math.radians(t)) for t in theta]
        ax.plot(xs, ys, color=color, linewidth=lw)

    elif e.dxftype() == 'CIRCLE':
        circle = plt.Circle((e.dxf.center.x, e.dxf.center.y),
                            e.dxf.radius, fill=False,
                            color=color, linewidth=lw)
        ax.add_patch(circle)

ax.autoscale()
ax.set_xticks([])
ax.set_yticks([])
ax.set_title('BiAxial Hull Plate (MX)', color='white', fontsize=14, pad=10)

plt.tight_layout()
plt.savefig(OUT_FILE, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print(f"Saved to {OUT_FILE}")
