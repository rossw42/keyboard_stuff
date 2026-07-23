#!/usr/bin/env python3
"""
Generate le-oeuf.converter.scad from the le-oeuf KiCad PCB.

Parses d:/GitHub2/eggsworks/le-oeuf/le-oeuf/le-oeuf.kicad_pcb for:
  * every `le-oeuf:Kailh-PG1425-X-Switch` footprint -> adapter position/rotation
  * the Edge.Cuts board outline -> plate outline polygon (arcs sampled)

Emits an OpenSCAD file in the same "converter" format proven on the kbforge
numpad example: parts = adapter | panel | plate, with the PG1350->PG1425
adapter (v3.1) geometry inlined.

Coordinate conversion: KiCad is y-down; OpenSCAD is y-up.  Points map
(x, y) -> (x, -y); footprint rotation transfers as-is (the mirror flips
chirality twice: once for the axis, once for the local footprint frame).

Usage:  python generate_converter_scad.py
"""

import math
import re
from pathlib import Path

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
PCB_PATH = Path(r"D:\GitHub2\eggsworks\le-oeuf\le-oeuf\le-oeuf.kicad_pcb")
OUT_PATH = Path(__file__).parent / "le-oeuf.converter.scad"
SWITCH_FOOTPRINT = "le-oeuf:Kailh-PG1425-X-Switch"
MCU_FOOTPRINT    = "le-oeuf:Xiao_nRF52840_AC_Reflow"  # controller footprint ref
# Physical PCB dimensions of the controller (width × length, mm).
# Adjust here when swapping to a different controller board.
MCU_CONTROLLER_W = 17.5   # Seeed Xiao BLE (nRF52840) width,  mm
MCU_CONTROLLER_L = 21.0   # Seeed Xiao BLE (nRF52840) length, mm
MCU_CLEARANCE    =  1.25  # extra clearance added on every side, mm
SPRUE_MAX_DIST = 25.0   # mm - connect adapters closer than this with sprues
ARC_SEG_LEN = 1.0       # mm - arc sampling resolution for Edge.Cuts
CHAIN_TOL = 0.05        # mm - endpoint matching tolerance when chaining edge


# --------------------------------------------------------------------------
# Minimal s-expression block extraction (paren counting)
# --------------------------------------------------------------------------
def extract_blocks(text: str, token: str):
    """Return every balanced-paren block starting with `token`."""
    blocks = []
    i = 0
    n = len(text)
    while True:
        j = text.find(token, i)
        if j < 0:
            break
        depth = 0
        k = j
        while k < n:
            c = text[k]
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        blocks.append(text[j:k + 1])
        i = k + 1
    return blocks


NUM = r"(-?\d+(?:\.\d+)?)"


def parse_mcu(text: str):
    """Return (x, y) center of the MCU footprint in KiCad coords, or None."""
    for block in extract_blocks(text, f'(footprint "{MCU_FOOTPRINT}"'):
        m_at = re.search(rf"\(at\s+{NUM}\s+{NUM}(?:\s+{NUM})?\)", block)
        if m_at:
            return float(m_at.group(1)), float(m_at.group(2))
    return None


def parse_switches(text: str):
    """[(ref, x, y, rot)] for every switch footprint."""
    out = []
    for block in extract_blocks(text, f'(footprint "{SWITCH_FOOTPRINT}"'):
        m_at = re.search(rf"\(at\s+{NUM}\s+{NUM}(?:\s+{NUM})?\)", block)
        m_ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
        if not m_at:
            continue
        x, y = float(m_at.group(1)), float(m_at.group(2))
        rot = float(m_at.group(3)) if m_at.group(3) else 0.0
        ref = m_ref.group(1) if m_ref else "?"
        out.append((ref, x, y, rot))
    out.sort(key=lambda t: int(re.sub(r"\D", "", t[0]) or 0))
    return out


# --------------------------------------------------------------------------
# Edge.Cuts outline extraction
# --------------------------------------------------------------------------
def _xy(block, name):
    m = re.search(rf"\({name}\s+{NUM}\s+{NUM}\)", block)
    return (float(m.group(1)), float(m.group(2))) if m else None


def sample_arc(s, m, e, seg_len=ARC_SEG_LEN):
    """Sample a KiCad 3-point arc (start, mid, end) into a point list."""
    ax, ay = s
    bx, by = m
    cx, cy = e
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-9:                       # collinear -> straight line
        return [s, e]
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay)
          + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx)
          + (cx**2 + cy**2) * (bx - ax)) / d
    r = math.hypot(ax - ux, ay - uy)
    a0 = math.atan2(ay - uy, ax - ux)
    a1 = math.atan2(by - uy, bx - ux)
    a2 = math.atan2(cy - uy, cx - ux)

    def ccw_span(f, t):
        sp = t - f
        while sp <= 0:
            sp += 2 * math.pi
        return sp
    # pick sweep direction so the arc passes through the mid point
    if ccw_span(a0, a1) <= ccw_span(a0, a2):
        sweep = ccw_span(a0, a2)            # CCW
    else:
        sweep = -ccw_span(a2, a0)           # CW
    steps = max(2, int(abs(sweep) * r / seg_len))
    return [(ux + r * math.cos(a0 + sweep * i / steps),
             uy + r * math.sin(a0 + sweep * i / steps))
            for i in range(steps + 1)]


def parse_edge_cuts(text: str):
    """Return ordered outline polygon [(x, y)] in KiCad coords, or None."""
    segs = []  # each: (start, end, full point list)
    for block in extract_blocks(text, "(gr_line"):
        if '"Edge.Cuts"' not in block:
            continue
        s, e = _xy(block, "start"), _xy(block, "end")
        if s and e:
            segs.append((s, e, [s, e]))
    for block in extract_blocks(text, "(gr_arc"):
        if '"Edge.Cuts"' not in block:
            continue
        s, m, e = _xy(block, "start"), _xy(block, "mid"), _xy(block, "end")
        if s and m and e:
            segs.append((s, e, sample_arc(s, m, e)))
    for block in extract_blocks(text, "(gr_rect"):
        if '"Edge.Cuts"' not in block:
            continue
        s, e = _xy(block, "start"), _xy(block, "end")
        if s and e:
            pts = [s, (e[0], s[1]), e, (s[0], e[1]), s]
            return pts
    # drop degenerate zero-length segments (e.g. arcs with start == end)
    segs = [s for s in segs
            if math.hypot(s[0][0] - s[1][0], s[0][1] - s[1][1]) > CHAIN_TOL]
    if not segs:
        return None

    def close(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1]) < CHAIN_TOL

    chain = list(segs[0][2])
    used = {0}
    while len(used) < len(segs):
        tail = chain[-1]
        found = False
        for i, (s, e, pts) in enumerate(segs):
            if i in used:
                continue
            if close(s, tail):
                chain.extend(pts[1:])
                used.add(i)
                found = True
                break
            if close(e, tail):
                chain.extend(list(reversed(pts))[1:])
                used.add(i)
                found = True
                break
        if not found:
            print(f"warning: edge chain broke after {len(used)}/{len(segs)} "
                  "segments - outline may be incomplete")
            break
    if close(chain[0], chain[-1]):
        chain.pop()
    else:
        print("warning: outline is not closed "
              f"(gap {math.hypot(chain[0][0]-chain[-1][0], chain[0][1]-chain[-1][1]):.3f}mm)")
    return chain


# --------------------------------------------------------------------------
# SCAD emission
# --------------------------------------------------------------------------
ADAPTER_AND_PARTS = r"""
// ==========================================================================
// PG1350 -> PG1425 ADAPTER (inlined from pg1350_to_pg1425_adapter.scad v3.1)
// z = 0 is the adapter's bottom face (sits on the PG1425 PCB);
// alignment pins extend below z = 0.
// ==========================================================================

pocket_clearance = 0.30;
hole_clearance   = 0.20;
post_clearance   = 0.15;
eps              = 0.10;

choc_body_xy         = 13.80;
choc_body_h          = 2.20;
choc_flange_xy       = 15.00;
choc_center_post_d   = 3.20;
choc_center_post_len = 2.65;
choc_side_post_d     = 1.90;
choc_side_post_x     = 5.50;
choc_pin1_pos        = [ 0.0, 5.9 ];
choc_pin2_pos        = [ 5.0, 3.8 ];

pg1425_align_hole_d    = 1.30;
pg1425_align_positions = [ [ 5.5, -5.5], [-5.5,  5.5] ];
pg1425_align_pin_h     = 1.40;
pg1425_pin1_pos        = [-3.4,  2.9];
pg1425_pin2_pos        = [-3.4, -2.0];

body_x  = choc_flange_xy;
body_y  = choc_flange_xy;
wall_t  = (choc_flange_xy - choc_body_xy - pocket_clearance) / 2;
wall_h  = choc_body_h;
floor_h = choc_center_post_len + 0.15;
body_h  = floor_h + wall_h;
adapter_corner_radius = 0.5;

plate_t       = 1.20;
clip_window_w = 6.0;
slot_w        = 1.4;

// v3.1 captive wire channels
wire_channel       = true;   // true = captive channel; false = v3 through-slot
channel_membrane_t = 0.50;   // floor membrane under the channel
wire_exit_hole_d   = 1.40;   // through-hole over each PG1425 plated hole
pin_entry_pocket_d = 1.60;   // through-pocket at each Choc pin position

adapter_slots = [
    [ choc_pin1_pos, pg1425_pin1_pos ],
    [ choc_pin2_pos, [2.4, -3.0], pg1425_pin2_pos ],
];

module rounded_block(x, y, h, r) {
    if (r > 0) {
        linear_extrude(height = h)
            offset(r = r) offset(delta = -r)
                square([x, y], center = true);
    } else {
        translate([0, 0, h/2]) cube([x, y, h], center = true);
    }
}

module adapter_body() {
    rounded_block(body_x, body_y, body_h, adapter_corner_radius);
}

module choc_pocket() {
    pocket_xy = choc_body_xy + pocket_clearance;
    translate([0, 0, floor_h])
        rounded_block(pocket_xy, pocket_xy, wall_h + eps, 0.3);
}

module clip_windows() {
    window_h = wall_h - plate_t + eps;
    for (sy = [-1, 1])
        translate([0, sy * (body_y/2 - wall_t/2), floor_h + window_h/2 - eps/2])
            cube([clip_window_w, wall_t + 2*eps, window_h], center = true);
}

module through_hole(pos, d) {
    translate([pos[0], pos[1], -eps])
        cylinder(h = floor_h + 2*eps, d = d + hole_clearance);
}

module pg1350_holes() {
    through_hole([0, 0], choc_center_post_d);
    through_hole([-choc_side_post_x, 0], choc_side_post_d);
    through_hole([ choc_side_post_x, 0], choc_side_post_d);
}

module routing_slot(pts) {
    z0 = wire_channel ? channel_membrane_t : -eps;
    h  = wire_channel ? (floor_h - channel_membrane_t + eps) : (floor_h + 2*eps);
    translate([0, 0, z0])
        linear_extrude(height = h)
            for (i = [0 : len(pts) - 2])
                hull() {
                    translate(pts[i])     circle(d = slot_w);
                    translate(pts[i + 1]) circle(d = slot_w);
                }
}

module pin_routing_slots() {
    for (s = adapter_slots) routing_slot(s);
}

// v3.1: through-openings at the channel ends
module channel_end_openings() {
    for (p = [choc_pin1_pos, choc_pin2_pos])
        translate([p[0], p[1], -eps])
            cylinder(h = floor_h + 2*eps, d = pin_entry_pocket_d);
    for (p = [pg1425_pin1_pos, pg1425_pin2_pos])
        translate([p[0], p[1], -eps])
            cylinder(h = floor_h + 2*eps, d = wire_exit_hole_d);
}

module pg1425_alignment_pins() {
    for (p = pg1425_align_positions)
        translate([p[0], p[1], -pg1425_align_pin_h])
            cylinder(h = pg1425_align_pin_h + eps,
                     d = pg1425_align_hole_d - post_clearance);
}

module adapter(with_pins = true) {
    union() {
        difference() {
            adapter_body();
            choc_pocket();
            clip_windows();
            pg1350_holes();
            pin_routing_slots();
            if (wire_channel) channel_end_openings();
        }
        if (with_pins) pg1425_alignment_pins();
    }
}

// ==========================================================================
// PANEL (Variant A): adapters at true board positions + snap-off sprues
// ==========================================================================

module placed_adapters(with_pins = true) {
    for (c = converters)
        translate([c[0], c[1], 0])
            rotate([0, 0, c[2]])
                adapter(with_pins);
}

module sprue_bars() {
    // Thin bars spanning the gaps between neighboring adapter bodies,
    // overlapping ~0.5mm into each solid floor for adhesion. Snap or cut
    // them off after printing.
    linear_extrude(height = sprue_h)
        for (s = sprues) {
            dx = s[2] - s[0];
            dy = s[3] - s[1];
            d  = norm([dx, dy]);
            ux = dx / d;
            uy = dy / d;
            hull() {
                translate([s[0] + ux*sprue_inset, s[1] + uy*sprue_inset])
                    circle(d = sprue_w);
                translate([s[2] - ux*sprue_inset, s[3] - uy*sprue_inset])
                    circle(d = sprue_w);
            }
        }
}

module panel() {
    placed_adapters(with_pins = true);
    sprue_bars();
}

// ==========================================================================
// INTEGRATED PLATE (Variant B): full-thickness slab fused with the adapters
//
// The slab spans z = 0 .. body_h - the SAME thickness as the switch
// converters - so the plate is flush with the adapter tops AND rests on the
// PCB like the adapters do. At converter positions the slab opens to the
// full 15x15 adapter footprint and the adapter body (with its pocket, clip
// windows, holes and wire channels) is fused in. Clip-relief cuts behind
// each bezel clip window keep the Choc retention clips functional.
//
// The plate outline is the actual le-oeuf Edge.Cuts PCB outline (arcs
// sampled), grown/shrunk by plate_edge_offset.
//
// NOTE: the slab underside now sits ON the PCB (z = 0). Any top-side PCB
// component under the slab footprint (diodes, MCU, slide switch, battery)
// will collide - use mcu_cutout to relieve it.
// ==========================================================================

module plate_outline_2d() {
    offset(delta = plate_edge_offset)
        polygon(board_edge);
}

module plate_cutouts_2d() {
    // full adapter footprint (rounded to match adapter_corner_radius) so
    // the fused adapter supplies all geometry within it, corner-gap free
    for (c = converters)
        translate([c[0], c[1]])
            rotate([0, 0, c[2]])
                offset(r = adapter_corner_radius)
                    offset(delta = -adapter_corner_radius)
                        square([body_x, body_y], center = true);
    if (mcu_cutout)
        translate(mcu_cutout_center)
            square(mcu_cutout_size, center = true);
}

// Outline chamfer implementation: builds a stack of thin extruded layers
// whose OUTER boundary is offset() by a fraction of plate_chamfer, so the
// outer edge bevels smoothly while concave features in board_edge (like the
// center waist) remain correct - offset() handles concavity properly, unlike
// hull(). plate_cutouts_2d() is subtracted from every layer so switch
// pockets / MCU window stay full-height straight cuts through the chamfer.
//
// invert = false: outline shrinks as z increases within the zone (top chamfer)
// invert = true : outline shrinks as z decreases within the zone (bottom chamfer)
module chamfer_layer_stack(zone_h, steps, max_delta, base_z, invert) {
    layer_h = zone_h / steps;
    for (i = [0 : steps - 1]) {
        frac = invert ? (steps - i - 0.5) / steps : (i + 0.5) / steps;
        d = -max_delta * frac;
        translate([0, 0, base_z + i * layer_h])
            linear_extrude(height = layer_h + eps)
                difference() {
                    offset(delta = d) plate_outline_2d();
                    plate_cutouts_2d();
                }
    }
}

// Full plate outline solid, z = 0 .. body_h, with the outer edge optionally
// chamfered on the top and/or bottom face (see plate_chamfer* variables).
module chamfered_outline_solid() {
    chamfer_active = (plate_chamfer > 0) && (plate_chamfer_top || plate_chamfer_bottom);
    if (!chamfer_active) {
        linear_extrude(body_h)
            difference() {
                plate_outline_2d();
                plate_cutouts_2d();
            }
    } else {
        top_h    = plate_chamfer_top    ? plate_chamfer : 0;
        bottom_h = plate_chamfer_bottom ? plate_chamfer : 0;
        mid_h    = body_h - top_h - bottom_h;
        union() {
            if (bottom_h > 0)
                chamfer_layer_stack(bottom_h, plate_chamfer_steps, plate_chamfer,
                                     0, invert = true);
            if (mid_h > 0)
                translate([0, 0, bottom_h])
                    linear_extrude(mid_h)
                        difference() {
                            plate_outline_2d();
                            plate_cutouts_2d();
                        }
            if (top_h > 0)
                chamfer_layer_stack(top_h, plate_chamfer_steps, plate_chamfer,
                                     body_h - top_h, invert = false);
        }
    }
}

// Relief voids cut into the slab directly behind each adapter clip window,
// so the Choc clips can still flex outward and snap into the windows.
module plate_clip_reliefs() {
    window_h = wall_h - plate_t + eps;
    for (c = converters)
        translate([c[0], c[1], 0])
            rotate([0, 0, c[2]])
                for (sy = [-1, 1])
                    translate([0,
                               sy * (body_y/2 + clip_relief_depth/2 - eps),
                               floor_h + window_h/2 - eps/2])
                        cube([clip_window_w,
                              clip_relief_depth + 2*eps,
                              window_h], center = true);
}

// Center relief: removes material from BELOW across the middle bridge
// (X span center_relief_x, full Y extent), leaving center_top_t on top.
// The adapters are unioned back afterwards, so key positions - if any
// fell inside the span - would remain full thickness.
module center_relief_cut() {
    span = center_relief_x[1] - center_relief_x[0];
    translate([center_relief_x[0], layout_min[1] - 200, -eps])
        cube([span, (layout_max[1] - layout_min[1]) + 400,
              body_h - center_top_t + eps]);
}

// Center window: trapezoid through-cutout in the upper bridge section,
// between the top of the board and the top of the key clusters.
// The shape widens toward the top (following the board outline) and
// narrows toward the key rows.  Defined as a clean 4-point trapezoid
// then inset by center_window_margin on every side.
//
// Outer trapezoid corners (before margin, y-up):
//   top-left:     ~[120, -48]  (near board top edge)
//   top-right:    ~[158, -48]
//   bottom-right: ~[154, -64]  (just above top key row)
//   bottom-left:  ~[124, -64]
//
// Tune center_window_top_y / center_window_bot_y to shift the window up/down,
// and center_window_top_w / center_window_bot_w to adjust the taper.
center_window_top_y  = -48.0;   // y of the wide top edge (board top ≈ -44)
center_window_bot_y  = -64.0;   // y of the narrow bottom edge (key rows start ≈ -56)
center_window_top_cx = 139.0;   // X center of the window
center_window_top_w  =  38.0;   // width of top edge (before margin)
center_window_bot_w  =  30.0;   // width of bottom edge (before margin)

module center_window_cut() {
    hw_top = center_window_top_w / 2;
    hw_bot = center_window_bot_w / 2;
    cx     = center_window_top_cx;
    trap = [
        [cx - hw_top, center_window_top_y],
        [cx + hw_top, center_window_top_y],
        [cx + hw_bot, center_window_bot_y],
        [cx - hw_bot, center_window_bot_y]
    ];
    linear_extrude(height = body_h + 2*eps)
        offset(delta = -center_window_margin)
            polygon(trap);
}

module integrated_plate() {
    union() {
        difference() {
            chamfered_outline_solid();
            plate_clip_reliefs();
            if (center_relief) center_relief_cut();
        }
        placed_adapters(with_pins = plate_pins);
    }
}

module integrated_plate_windowed() {
    if (center_window) {
        difference() {
            integrated_plate();
            translate([0, 0, -eps])
                center_window_cut();
        }
    } else {
        integrated_plate();
    }
}

// ==========================================================================

if (part == "adapter")     adapter();
else if (part == "plate")  integrated_plate_windowed();
else                       panel();
"""


def fmt_pts(pts, per_line=4, indent="  "):
    items = [f"[{x:.3f}, {y:.3f}]" for x, y in pts]
    lines = []
    for i in range(0, len(items), per_line):
        lines.append(indent + ", ".join(items[i:i + per_line]))
    return ",\n".join(lines)


def main():
    text = PCB_PATH.read_text(encoding="utf-8", errors="replace")

    switches = parse_switches(text)
    if not switches:
        raise SystemExit("no switch footprints found!")
    print(f"found {len(switches)} '{SWITCH_FOOTPRINT}' footprints")

    # KiCad y-down -> OpenSCAD y-up
    converters = [(x, -y, rot) for (_ref, x, y, rot) in switches]

    edge = parse_edge_cuts(text)
    if edge:
        board_edge = [(x, -y) for (x, y) in edge]
        print(f"board edge: {len(board_edge)} points")
    else:
        # fallback: bounding box of adapters + 3mm margin
        xs = [c[0] for c in converters]
        ys = [c[1] for c in converters]
        m = 7.5 + 3.0
        board_edge = [(min(xs) - m, min(ys) - m), (max(xs) + m, min(ys) - m),
                      (max(xs) + m, max(ys) + m), (min(xs) - m, max(ys) + m)]
        print("warning: no Edge.Cuts found, using bounding-box outline")

    # center relief span: gap between left/right key clusters, keeping clear
    # of the rotated 15x15 adapter footprints (half-extent at 7deg + margin)
    mid_x = (min(c[0] for c in converters) + max(c[0] for c in converters)) / 2
    half_ext = 7.5 * (math.cos(math.radians(7)) + math.sin(math.radians(7)))
    margin = 0.5
    left_max = max(c[0] for c in converters if c[0] < mid_x) + half_ext + margin
    right_min = min(c[0] for c in converters if c[0] >= mid_x) - half_ext - margin
    print(f"center relief X span: {left_max:.2f} .. {right_min:.2f} "
          f"({right_min - left_max:.2f}mm wide)")

    # sprues: connect neighboring adapters
    sprues = []
    for i in range(len(converters)):
        for j in range(i + 1, len(converters)):
            d = math.hypot(converters[i][0] - converters[j][0],
                           converters[i][1] - converters[j][1])
            if d <= SPRUE_MAX_DIST:
                sprues.append((converters[i][0], converters[i][1],
                               converters[j][0], converters[j][1]))
    print(f"sprues: {len(sprues)} pairs (max dist {SPRUE_MAX_DIST}mm)")

    # MCU position (KiCad y-down -> OpenSCAD y-up)
    mcu_pos = parse_mcu(text)
    if mcu_pos:
        mcu_cx, mcu_cy = mcu_pos[0], -mcu_pos[1]
        print(f"MCU '{MCU_FOOTPRINT}' center: ({mcu_cx:.3f}, {mcu_cy:.3f}) y-up")
    else:
        mcu_cx = (min(c[0] for c in converters) + max(c[0] for c in converters)) / 2
        mcu_cy = max(c[1] for c in converters) + 2
        print(f"warning: MCU footprint '{MCU_FOOTPRINT}' not found; "
              f"using fallback center ({mcu_cx:.3f}, {mcu_cy:.3f})")

    xs = [c[0] for c in converters]
    ys = [c[1] for c in converters]

    conv_lines = "\n".join(
        f"  [{x:.6f}, {y:.6f}, {r:.1f}],   // {ref}"
        for (ref, _, _, _), (x, y, r) in zip(switches, converters)
    )
    sprue_lines = ",\n".join(
        f"  [{a:.3f}, {b:.3f}, {c:.3f}, {d:.3f}]" for (a, b, c, d) in sprues
    )

    header = f"""\
// le-oeuf - switch-converter panel / integrated plate
// Generated by generate_converter_scad.py from
//   {PCB_PATH}
// Converter positions: {len(switches)} of {len(switches)} switches
// (all keys use the Kailh-PG1425-X-Switch footprint).
//
// Adapter geometry inlined from
// projects/switch_converter/OpenSCAD/pg1350_to_pg1425_adapter.scad (v3.1):
// a 15x15x5mm carrier that seats a Kailh Choc PG1350 switch onto a Kailh
// PG1425 "Choc X" PCB footprint. The top 1.2mm of its bezel walls act as
// the switch plate (clip windows included).
//
// Parts:
//   "adapter" - one adapter at the origin
//   "panel"   - all adapters at board positions, joined by snap-off sprues
//   "plate"   - integrated converter plate (adapters fused into one plate
//               whose outline is the actual le-oeuf PCB Edge.Cuts)

/* [Part Selection] */
part = "plate"; // [adapter, panel, plate]

/* [Panel] */
sprue_w = 2.0;
sprue_h = 0.8;
sprue_inset = 7.0;   // sprue endpoints this far from adapter centers

/* [Plate] */
plate_pins        = false; // per-key alignment pins under the plate.
                           // false (default) = flat bottom, prints flat on
                           // the bed with ZERO supports; the plate outline
                           // matching the PCB edge provides alignment.
                           // true = pins included; print on a >=1.4mm raft
                           // or with supports.
plate_edge_offset = 0.0;   // grow (+) / shrink (-) the PCB outline, mm
clip_relief_depth = 1.2;   // slab relief behind each clip window, mm

// Outline chamfer: bevels the plate's OUTER edge (the board_edge boundary)
// so it isn't a sharp 90° edge. Implemented with a stack of thin offset()
// layers rather than hull()-lofting, because hull() takes the convex hull
// of the outline and would erase the board's concave notches (e.g. the
// center waist); offset() shrinks/grows a polygon correctly even where
// it's concave. Only the OUTER boundary is chamfered - interior cutouts
// (switch pockets, MCU window, center window, etc.) stay straight-walled.
plate_chamfer        = 1.0;   // mm — bevel size on the outer edge (0 = disable, square edge)
plate_chamfer_top    = true;  // chamfer the top-facing outer edge
plate_chamfer_bottom = false; // leave false: the bottom must stay flat/full-size
                               // so the outline keeps resting flush on the PCB
                               // edge (alignment + zero-support printing)
plate_chamfer_steps  = 8;     // stepped layers approximating the slope (higher = smoother/slower)

// Center window: a trapezoid through-cutout in the bridge between the two
// key clusters.  The trapezoid matches the shape of the bridge (narrow at
// the top, wider at the bottom — like a keystone), inset uniformly by
// center_window_margin mm on all sides.  Set center_window = false to disable.
center_window        = true;
center_window_margin = 4.0;  // mm of slab remaining around every edge

// Center relief: thins the middle bridge (between the two key clusters)
// from BELOW, leaving center_top_t of material on top, so components
// mounted on the PCB under that section have clearance. The X span is
// auto-computed from the key clusters (adapter footprints stay full
// thickness); the top surface stays flush.
center_relief   = true;
center_top_t    = 1.5;     // remaining plate thickness over the relief, mm
center_relief_x = [{left_max:.3f}, {right_min:.3f}];  // X span of the relief

// MCU cutout: {MCU_FOOTPRINT} (PCB center extracted from KiCad footprint).
// Physical board: {MCU_CONTROLLER_W} × {MCU_CONTROLLER_L} mm; clearance: {MCU_CLEARANCE} mm per side.
// Adjust mcu_controller_w / mcu_controller_l to match a different controller.
mcu_controller_w  = {MCU_CONTROLLER_W};   // controller PCB width,  mm
mcu_controller_l  = {MCU_CONTROLLER_L};   // controller PCB length, mm
mcu_clearance     =  {MCU_CLEARANCE};  // extra clearance added on every side, mm
mcu_cutout        = true;   // full through-cutout for the MCU
mcu_cutout_center = [{mcu_cx:.3f}, {mcu_cy:.3f}]; // PCB footprint center (y-up)
mcu_cutout_size   = [mcu_controller_w + 2*mcu_clearance,
                     mcu_controller_l + 2*mcu_clearance];

/* [Hidden] */
$fn = 48;

// Converter positions: [x_center, y_center, rotation_deg]  (y-up)
converters = [
{conv_lines}
];

// Sprue pairs: [x1, y1, x2, y2]
sprues = [
{sprue_lines}
];

// le-oeuf PCB Edge.Cuts outline, y-up ({len(board_edge)} pts)
board_edge = [
{fmt_pts(board_edge)}
];

// Layout extents (adapter centers, mm, y-up space)
layout_min = [{min(xs):.3f}, {min(ys):.3f}];
layout_max = [{max(xs):.3f}, {max(ys):.3f}];
"""

    OUT_PATH.write_text(header + ADAPTER_AND_PARTS, encoding="utf-8")
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    main()