#!/usr/bin/env python3
"""Keycap clearance check for the choc variant's center space keys.

Models two 1u choc caps SIDE BY SIDE at bottom-row height, symmetric about
the gap midpoint, rotated -6/+6 to match their clusters. Verifies exact
rotated-polygon gaps: space-to-space and space-to-inner-column caps.
Keep positions in sync with biaxial_choc.ergogen.yaml.
"""
import math

# --- config values (keep in sync with biaxial_choc.ergogen.yaml) ---
KX, KY = 19.0, 17.0
MID_X, MID_Y = 210.0, -148.5
CAP_1U_W, CAP_1U_H = 17.5, 16.5      # MBK-class 1u choc cap

# Space keys: symmetric about the gap midpoint at bottom-row height
GAP_MID = (MID_X - 1.7148 * KX + MID_X + 1.6885 * KX) / 2   # 209.75
SP_SEP = 21.5                       # center-to-center between the two spaces
SP_Y = MID_Y - 1.4918 * KY          # bottom-row height


def rot_rect(cx, cy, w, h, ang_deg):
    ang = math.radians(ang_deg)
    c, s = math.cos(ang), math.sin(ang)
    hw, hh = w / 2, h / 2
    return [(cx + dx * c - dy * s, cy + dx * s + dy * c)
            for dx, dy in [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]]


def seg_dist(p1, p2, p3, p4):
    def pt_seg(p, a, b):
        ax, ay = a; bx, by = b; px, py = p
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy
        t = 0 if L2 == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L2))
        return math.hypot(px - (ax + t * dx), py - (ay + t * dy))
    return min(pt_seg(p1, p3, p4), pt_seg(p2, p3, p4),
               pt_seg(p3, p1, p2), pt_seg(p4, p1, p2))


def inside(pt, poly):
    x, y = pt
    n = len(poly)
    cnt = False
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            cnt = not cnt
    return cnt


def poly_gap(a, b):
    if any(inside(p, b) for p in a) or any(inside(p, a) for p in b):
        return -1.0  # overlapping
    return min(seg_dist(a[i], a[(i + 1) % 4], b[j], b[(j + 1) % 4])
               for i in range(4) for j in range(4))


def main():
    slx = GAP_MID - SP_SEP / 2
    srx = GAP_MID + SP_SEP / 2
    cap_l = rot_rect(slx, SP_Y, CAP_1U_W, CAP_1U_H, -6)
    cap_r = rot_rect(srx, SP_Y, CAP_1U_W, CAP_1U_H, +6)

    neighbors = {
        'L-home (G)':   rot_rect(MID_X - 1.6103 * KX, MID_Y - 0.4973 * KY, CAP_1U_W, CAP_1U_H, -6),
        'L-bottom (B)': rot_rect(MID_X - 1.7148 * KX, MID_Y - 1.4918 * KY, CAP_1U_W, CAP_1U_H, -6),
        'R-home (H)':   rot_rect(MID_X + 1.584 * KX, MID_Y - 0.4973 * KY, CAP_1U_W, CAP_1U_H, +6),
        'R-bottom (N)': rot_rect(MID_X + 1.6885 * KX, MID_Y - 1.4918 * KY, CAP_1U_W, CAP_1U_H, +6),
    }

    print(f"Side-by-side 1u spaces ({CAP_1U_W} x {CAP_1U_H} mm caps) at bottom-row height:")
    print(f"  left:  ({slx:.2f}, {SP_Y:.2f}) rot -6")
    print(f"  right: ({srx:.2f}, {SP_Y:.2f}) rot +6   (separation {SP_SEP} mm)")
    g = poly_gap(cap_l, cap_r)
    print(f"  space-to-space cap gap: {'OVERLAP' if g < 0 else f'{g:.2f} mm'}")
    for name, poly in neighbors.items():
        target = cap_l if name.startswith('L') else cap_r
        gg = poly_gap(target, poly)
        print(f"  space vs {name:12s}: {'OVERLAP' if gg < 0 else f'{gg:.2f} mm'}")


if __name__ == '__main__':
    main()