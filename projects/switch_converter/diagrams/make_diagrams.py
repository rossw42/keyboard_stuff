"""
Generate SVG diagrams for the PG1350 -> PG1425 adapter electrical-connection options.

Outputs (same folder):
  - option_a_millmax_section.svg   : cross-section of Option A (Mill-Max tailed receptacle)
  - option_b_choc_socket_section.svg : cross-section of Option B (Kailh Choc hotswap socket + pin stubs)
  - top_view_pin_alignment.svg     : top view showing 90-deg CCW pin/pad alignment

All geometry is drawn in millimeters and scaled; sections are SCHEMATIC composites
(both pins unfolded into one plane) but distances/thicknesses are to scale.
"""

import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- colors
C_PCB = "#2f7d43"
C_PCB_DARK = "#1d5a2e"
C_HOLE = "#f2ede2"
C_COPPER = "#c87533"
C_ADAPTER = "#9aa2ab"
C_ADAPTER_DK = "#6d757e"
C_SWITCH = "#d9b380"
C_SWITCH_DK = "#b28a54"
C_STEM = "#c1553a"
C_GOLD = "#c9a227"
C_GOLD_DK = "#8f7318"
C_BRONZE = "#b0762c"
C_SOLDER = "#b9bcc4"
C_PIN = "#8a8f98"
C_TEXT = "#222"
C_NOTE = "#666"
C_DIM = "#c0392b"
C_SOCKET = "#4a4f57"


class Canvas:
    """mm -> px canvas. x maps left/right around cx; z maps UP from base."""

    def __init__(self, w, h, cx, base, scale=20.0):
        self.w, self.h, self.cx, self.base, self.s = w, h, cx, base, scale
        self.el = []

    def X(self, x):
        return self.cx + x * self.s

    def Z(self, z):
        return self.base - z * self.s

    # ---- primitives -------------------------------------------------
    def rect(self, x0, z0, x1, z1, fill, stroke="none", sw=1, dash=None, rx=0):
        X0, X1 = sorted([self.X(x0), self.X(x1)])
        Z0, Z1 = sorted([self.Z(z0), self.Z(z1)])
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(
            f'<rect x="{X0:.1f}" y="{Z0:.1f}" width="{X1-X0:.1f}" height="{Z1-Z0:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d} rx="{rx}"/>'
        )

    def poly(self, pts, fill="none", stroke="#333", sw=2, close=False, dash=None):
        p = " ".join(f"{self.X(x):.1f},{self.Z(z):.1f}" for x, z in pts)
        tag = "polygon" if close else "polyline"
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(
            f'<{tag} points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d} '
            f'stroke-linejoin="round" stroke-linecap="round"/>'
        )

    def circle(self, x, z, r_mm, fill, stroke="none", sw=1):
        self.el.append(
            f'<circle cx="{self.X(x):.1f}" cy="{self.Z(z):.1f}" r="{r_mm*self.s:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )

    def ellipse(self, x, z, rx_mm, rz_mm, fill, stroke="none", sw=1):
        self.el.append(
            f'<ellipse cx="{self.X(x):.1f}" cy="{self.Z(z):.1f}" rx="{rx_mm*self.s:.1f}" '
            f'ry="{rz_mm*self.s:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )

    # ---- text / annotation ------------------------------------------
    def text_px(self, px, py, s, size=13, anchor="start", fill=C_TEXT, bold=False, italic=False):
        w = ' font-weight="bold"' if bold else ""
        i = ' font-style="italic"' if italic else ""
        self.el.append(
            f'<text x="{px:.0f}" y="{py:.0f}" font-family="Segoe UI, Arial, sans-serif" '
            f'font-size="{size}" text-anchor="{anchor}" fill="{fill}"{w}{i}>{s}</text>'
        )

    def label(self, px, py, lines, tx, tz, anchor="start", size=13, fill=C_TEXT):
        """Multi-line label at px,py with a leader line to mm point (tx,tz)."""
        if isinstance(lines, str):
            lines = [lines]
        for k, ln in enumerate(lines):
            self.text_px(px, py + k * (size + 3), ln, size=size, anchor=anchor, fill=fill)
        # leader from near text toward target
        sx = px + (-6 if anchor == "start" else 6)
        sy = py + (len(lines) - 1) * (size + 3) * 0.5 - 4
        self.el.append(
            f'<line x1="{sx:.0f}" y1="{sy:.0f}" x2="{self.X(tx):.1f}" y2="{self.Z(tz):.1f}" '
            f'stroke="#555" stroke-width="1" stroke-dasharray="3,3"/>'
        )
        self.el.append(
            f'<circle cx="{self.X(tx):.1f}" cy="{self.Z(tz):.1f}" r="2.6" fill="#555"/>'
        )

    def dim_h(self, x0, x1, z, txt, above=True):
        y = self.Z(z)
        X0, X1 = self.X(x0), self.X(x1)
        self.el.append(
            f'<line x1="{X0:.1f}" y1="{y:.1f}" x2="{X1:.1f}" y2="{y:.1f}" stroke="{C_DIM}" '
            f'stroke-width="1.4" marker-start="url(#dim)" marker-end="url(#dim)"/>'
        )
        ty = y - 6 if above else y + 15
        self.text_px((X0 + X1) / 2, ty, txt, size=12, anchor="middle", fill=C_DIM, bold=True)

    def dim_v(self, x, z0, z1, txt):
        Xp = self.X(x)
        Y0, Y1 = self.Z(z0), self.Z(z1)
        self.el.append(
            f'<line x1="{Xp:.1f}" y1="{Y0:.1f}" x2="{Xp:.1f}" y2="{Y1:.1f}" stroke="{C_DIM}" '
            f'stroke-width="1.4" marker-start="url(#dim)" marker-end="url(#dim)"/>'
        )
        self.text_px(Xp + 7, (Y0 + Y1) / 2 + 4, txt, size=12, fill=C_DIM, bold=True)

    def arrow(self, x0, z0, x1, z1, color=C_DIM, sw=2):
        self.el.append(
            f'<line x1="{self.X(x0):.1f}" y1="{self.Z(z0):.1f}" x2="{self.X(x1):.1f}" '
            f'y2="{self.Z(z1):.1f}" stroke="{color}" stroke-width="{sw}" marker-end="url(#arr)"/>'
        )

    # ---- save --------------------------------------------------------
    def save(self, name):
        defs = (
            '<defs>'
            '<marker id="arr" markerWidth="9" markerHeight="9" refX="7" refY="3.5" orient="auto">'
            f'<path d="M0,0 L8,3.5 L0,7 z" fill="{C_DIM}"/></marker>'
            '<marker id="dim" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">'
            f'<path d="M1,4 L7,1 L7,7 z" fill="{C_DIM}"/></marker>'
            "</defs>"
        )
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}">'
            f'<rect width="{self.w}" height="{self.h}" fill="#fbfaf7"/>'
            + defs
            + "".join(self.el)
            + "</svg>"
        )
        path = os.path.join(OUT_DIR, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print("wrote", path)


# ======================================================================
# Shared side-view pieces
# ======================================================================
def draw_pcb(c, holes, z_top=0.0, x0=-11, x1=11):
    """PCB slab with plated through-holes (list of x centers)."""
    c.rect(x0, z_top - 1.6, x1, z_top, C_PCB, stroke=C_PCB_DARK, sw=1.5)
    for hx in holes:
        c.rect(hx - 0.55, z_top - 1.6, hx + 0.55, z_top, C_HOLE)          # drill
        c.rect(hx - 0.85, z_top - 0.18, hx + 0.85, z_top, C_COPPER)       # annular top
        c.rect(hx - 0.85, z_top - 1.6, hx + 0.85, z_top - 1.42, C_COPPER)  # annular bottom
        # plated barrel walls
        c.rect(hx - 0.65, z_top - 1.6, hx - 0.55, z_top, C_COPPER)
        c.rect(hx + 0.55, z_top - 1.6, hx + 0.65, z_top, C_COPPER)


def draw_choc_switch(c, z_seat, pins, pin_bottom, post_bottom=None):
    """Choc V1 above the adapter pocket floor at z_seat. pins = list of x."""
    zs = z_seat
    c.rect(-6.9, zs, 6.9, zs + 2.2, C_SWITCH, stroke=C_SWITCH_DK, sw=1.5)   # bottom housing
    c.rect(-7.5, zs + 2.2, 7.5, zs + 3.0, C_SWITCH, stroke=C_SWITCH_DK, sw=1.5)  # flange
    c.rect(-6.4, zs + 3.0, 6.4, zs + 4.6, "#e6c797", stroke=C_SWITCH_DK, sw=1.5)  # upper housing
    c.rect(-2.9, zs + 4.6, 2.9, zs + 7.4, C_STEM, stroke="#8e3a26", sw=1.5, rx=3)  # stem (schematic)
    if post_bottom is not None:
        c.rect(-1.6, post_bottom, 1.6, zs, C_SWITCH, stroke=C_SWITCH_DK, sw=1)  # center post
    for px_ in pins:
        c.rect(px_ - 0.3, pin_bottom, px_ + 0.3, zs, C_PIN, stroke="#5c6067", sw=1)


def solder_fillet(c, hx, z_bot):
    c.poly(
        [(hx - 0.95, z_bot), (hx + 0.95, z_bot), (hx + 0.33, z_bot - 0.75),
         (hx - 0.33, z_bot - 0.75)],
        fill=C_SOLDER, stroke="#8d919a", sw=1, close=True,
    )


# ======================================================================
# Diagram 1 — Option A: Mill-Max tailed receptacle
# ======================================================================
def option_a():
    c = Canvas(960, 690, cx=440, base=450)
    PIN_L, HOLE_L = -5.5, -2.8   # 2.7 mm jog (schematic positions, true distance)
    PIN_R, HOLE_R = 2.5, 3.8     # 1.3 mm jog
    POST_X = 6.3                 # printed alignment post

    # PCB (with extra NPTH for the alignment post)
    draw_pcb(c, [HOLE_L, HOLE_R])
    c.rect(POST_X - 0.65, -1.6, POST_X + 0.65, 0, C_HOLE)  # locating hole (NPTH)

    # adapter: floor 0..2.8, bezel walls 2.8..5.0
    c.rect(-7.5, 0, 7.5, 2.8, C_ADAPTER, stroke=C_ADAPTER_DK, sw=1.5)
    c.rect(-7.5, 2.8, -6.75, 5.0, C_ADAPTER, stroke=C_ADAPTER_DK, sw=1.5)
    c.rect(6.75, 2.8, 7.5, 5.0, C_ADAPTER, stroke=C_ADAPTER_DK, sw=1.5)
    # center-post recess in floor
    c.rect(-1.75, 0.15, 1.75, 2.8, "#e8e6e1")
    # alignment post (printed, part of adapter)
    c.rect(POST_X - 0.6, -1.5, POST_X + 0.6, 0, C_ADAPTER, stroke=C_ADAPTER_DK, sw=1)

    # receptacles pressed into floor (barrel 0..2.8)
    for px_ in (PIN_L, PIN_R):
        c.rect(px_ - 0.83, 0, px_ + 0.83, 2.8, C_GOLD, stroke=C_GOLD_DK, sw=1.5)
        c.rect(px_ - 0.5, 2.15, px_ + 0.5, 2.8, "#3d3d3d")  # mouth opening
        # spring fingers hint
        c.poly([(px_ - 0.45, 2.75), (px_ - 0.15, 2.0)], stroke=C_GOLD_DK, sw=2)
        c.poly([(px_ + 0.45, 2.75), (px_ + 0.15, 2.0)], stroke=C_GOLD_DK, sw=2)

    # switch on top (pins reach into receptacle mouths)
    draw_choc_switch(c, z_seat=2.8, pins=[PIN_L, PIN_R], pin_bottom=1.1, post_bottom=0.25)

    # solder tails: exit barrel bottom, jog sideways, drop through PTH
    for px_, hx in ((PIN_L, HOLE_L), (PIN_R, HOLE_R)):
        c.poly([(px_, 0.1), (px_, -0.15), (hx, -0.7), (hx, -2.35)],
               stroke=C_GOLD, sw=13, dash=None)
        c.poly([(px_, 0.1), (px_, -0.15), (hx, -0.7), (hx, -2.35)],
               stroke=C_GOLD_DK, sw=1)
        solder_fillet(c, hx, -1.6)

    # ---- dimensions
    c.dim_v(8.6, 0, 2.8, "floor 2.8")
    c.dim_v(11.6, -1.6, 0, "PCB 1.6")
    c.dim_h(PIN_L, HOLE_L, -3.3, "2.7 mm jog", above=False)
    c.dim_h(PIN_R, HOLE_R, -3.3, "1.3 mm jog", above=False)

    # ---- labels
    c.text_px(480, 36, "Option A — Mill-Max tailed receptacle (0300-1-15-15-47-27-10-0)", 21, "middle", bold=True)
    c.text_px(480, 58, "Cross-section, schematic — both pins unfolded into one plane; thicknesses to scale",
              13, "middle", fill=C_NOTE, italic=True)

    c.label(660, 150, ["Choc V1 switch (PG1350)"], 5.8, 9.0)
    c.label(660, 235, ["Choc pin plugs into mouth", "= hotswap, NO solder"], PIN_R, 2.4)
    c.label(660, 305, ["Mill-Max 0300-1 receptacle,", "press-fit in printed floor,", "mouth facing up"], PIN_R + 0.6, 1.0)
    c.label(700, 400, ["Printed alignment post", "drops into φ1.3 locating hole"], POST_X, -0.7)
    c.label(690, 480, ["PG1425 plated through-hole", "(1.1 mm drill)"], HOLE_R + 0.5, -1.0)
    c.label(660, 545, ["Solder joint on PCB underside", "(only solder step per pin)"], HOLE_R, -2.2)

    c.label(220, 165, ["3D-printed adapter shell", "15 × 15 mm"], -7.1, 4.0, anchor="end")
    c.label(220, 250, ["Bezel wall — Choc clips in", "like a normal switch plate"], -6.9, 3.4, anchor="end")
    c.label(220, 330, ["Receptacle SOLDER TAIL:", "solid brass pin out the bottom", "of the barrel (~0.5-0.8 mm dia)"], PIN_L - 0.2, -0.1, anchor="end")
    c.label(220, 430, ["Tail bent sideways to reach", "the PG1425 hole, then straight", "down through it"], (PIN_L + HOLE_L) / 2, -0.55, anchor="end")

    c.text_px(480, 660, "Assembly per key: press 2 receptacles into print → snap Choc in → set adapter on PCB → bend 2 tails → 2 solder joints underneath",
              13, "middle", fill=C_NOTE)
    c.save("option_a_millmax_section.svg")


# ======================================================================
# Diagram 2 — Option B: Kailh Choc hotswap socket + pin stubs
# ======================================================================
def option_b():
    c = Canvas(960, 720, cx=440, base=480)
    PIN_L, PIN_R = -4.5, 1.5       # socket mouth / Choc pin positions (schematic)
    STUB_L, STUB_R = -7.0, 4.0     # where the pin stubs / PTH sit (schematic)
    FLOOR = 3.4                    # thicker floor: 1.8 socket pocket + 1.6 web

    draw_pcb(c, [STUB_L, STUB_R])

    # adapter: floor 0..3.4 with socket pocket 0..1.8, walls 3.4..5.6
    c.rect(-7.5, 0, 7.5, FLOOR, C_ADAPTER, stroke=C_ADAPTER_DK, sw=1.5)
    c.rect(-7.5, FLOOR, -6.75, FLOOR + 2.2, C_ADAPTER, stroke=C_ADAPTER_DK, sw=1.5)
    c.rect(6.75, FLOOR, 7.5, FLOOR + 2.2, C_ADAPTER, stroke=C_ADAPTER_DK, sw=1.5)

    # socket pocket (cutout in floor underside) + socket housing
    c.rect(-6.2, 0, 3.2, 1.8, "#e8e6e1")                                   # pocket
    c.rect(-6.0, 0, 3.0, 1.8, C_SOCKET, stroke="#2e3238", sw=1.5, rx=3)    # socket body
    # socket mouths + bronze contacts
    for px_ in (PIN_L, PIN_R):
        c.rect(px_ - 0.75, 0.7, px_ + 0.75, 1.8, "#2a2d33")
        c.poly([(px_ - 0.6, 1.75), (px_ - 0.18, 0.9)], stroke=C_BRONZE, sw=3)
        c.poly([(px_ + 0.6, 1.75), (px_ + 0.18, 0.9)], stroke=C_BRONZE, sw=3)
        # floor web pass-through hole for the Choc pin
        c.rect(px_ - 0.65, 1.8, px_ + 0.65, FLOOR, "#e8e6e1")

    # SMD pads exiting the housing ends (bronze tabs)
    c.rect(-7.3, 0.0, -6.0, 0.28, C_BRONZE, stroke="#7d5420", sw=1)
    c.rect(3.0, 0.0, 4.3, 0.28, C_BRONZE, stroke="#7d5420", sw=1)

    # pin stubs soldered onto the pads, dropping through the PTHs
    for sx in (STUB_L, STUB_R):
        c.rect(sx - 0.4, -2.3, sx + 0.4, 0.8, C_PIN, stroke="#5c6067", sw=1)   # 0.8 mm stub
        c.ellipse(sx, 0.42, 0.85, 0.5, C_SOLDER, stroke="#8d919a", sw=1)       # joint to pad
        solder_fillet(c, sx, -1.6)

    # switch on top (pins pass through web into socket mouths)
    draw_choc_switch(c, z_seat=FLOOR, pins=[PIN_L, PIN_R], pin_bottom=1.0, post_bottom=2.0)

    # ---- dimensions
    c.dim_v(8.6, 1.8, FLOOR, "web 1.6")
    c.dim_v(8.6, 0, 1.8, "socket 1.8")
    c.dim_v(11.6, -1.6, 0, "PCB 1.6")
    c.dim_v(-8.6, 0, FLOOR, "floor 3.4")

    # ---- labels
    c.text_px(480, 36, "Option B — Kailh Choc hotswap socket + soldered pin stubs", 21, "middle", bold=True)
    c.text_px(480, 58, "Cross-section, schematic — socket clipped into a pocket under the adapter floor",
              13, "middle", fill=C_NOTE, italic=True)

    c.label(660, 150, ["Choc V1 switch (PG1350)"], 5.8, FLOOR + 5.6)
    c.label(660, 240, ["Choc pin passes through the", "1.6 mm web — exactly like a", "hotswap PCB"], PIN_R, 2.6)
    c.label(660, 330, ["Socket mouth grips the pin", "(designed for Choc pins)"], PIN_R + 0.4, 1.2)
    c.label(700, 410, ["SMD pad (pre-tinned tab)"], 3.6, 0.15)
    c.label(700, 530, ["~4 mm stub of 0.8 mm solid wire", "SOLDERED to the pad, pointing", "straight down into the PTH"], STUB_R + 0.35, -0.4)
    c.label(660, 630, ["Solder joint on PCB underside"], STUB_R, -2.2)

    c.label(220, 165, ["3D-printed adapter shell", "(floor +0.6 mm thicker than", "Option A → taller stack)"], -7.1, 4.4, anchor="end")
    c.label(220, 280, ["Kailh Choc hotswap socket", "CPG135001S30, clipped into", "printed pocket (self-fixturing)"], -4.0, 0.9, anchor="end")
    c.label(220, 400, ["Do NOT bend the SMD pads —", "stamped bronze cracks; solder", "a stub to them instead"], -6.6, 0.15, anchor="end")
    c.label(220, 500, ["Stub prepared on the bench in a", "printed jig, before assembly"], STUB_L - 0.3, -1.0, anchor="end")

    c.text_px(480, 692, "Assembly per key: solder 2 stubs to socket pads (bench, jigged) → clip socket into pocket → snap Choc in → set on PCB → 2 solder joints underneath",
              12.5, "middle", fill=C_NOTE)
    c.save("option_b_choc_socket_section.svg")


# ======================================================================
# Diagram 0 — Anatomy of a Mill-Max tailed receptacle (what is a "tail"?)
# ======================================================================
def receptacle_anatomy():
    # big scale: 1 mm = 44 px. Datum z=0 at the shoulder underside.
    c = Canvas(960, 720, cx=330, base=330, scale=44.0)

    BR = 0.775        # barrel outer radius (~1.55 mm dia)
    SHR = 1.0         # shoulder radius (~2.0 mm dia)
    BARREL_H = 3.7    # barrel length below shoulder
    SH_H = 0.6        # shoulder height
    TAIL_R = 0.32     # tail radius (~0.64 mm dia)
    TAIL_H = 3.2      # tail length

    # ---------- solder TAIL (highlighted) ----------
    c.rect(-TAIL_R, -BARREL_H - TAIL_H, TAIL_R, -BARREL_H, C_GOLD, stroke=C_GOLD_DK, sw=2)
    c.poly([(-TAIL_R, -BARREL_H - TAIL_H), (TAIL_R, -BARREL_H - TAIL_H), (0, -BARREL_H - TAIL_H - 0.35)],
           fill=C_GOLD, stroke=C_GOLD_DK, sw=1.5, close=True)  # pointed tip
    # highlight ring around tail
    c.rect(-TAIL_R - 0.22, -BARREL_H - TAIL_H - 0.5, TAIL_R + 0.22, -BARREL_H + 0.1,
           "none", stroke=C_DIM, sw=2.5, dash="6,4", rx=8)

    # ---------- barrel (cutaway) ----------
    c.rect(-BR, -BARREL_H, BR, 0, C_GOLD, stroke=C_GOLD_DK, sw=2)
    # cutaway interior
    c.rect(-BR + 0.25, -BARREL_H + 0.35, BR - 0.25, 0, "#f5efdd")
    # internal spring-finger contact clip (the thing that grips the pin)
    c.poly([(-0.5, -0.25), (-0.16, -1.5), (-0.5, -2.6)], stroke="#a05a2c", sw=5)
    c.poly([(0.5, -0.25), (0.16, -1.5), (0.5, -2.6)], stroke="#a05a2c", sw=5)

    # ---------- shoulder ----------
    c.rect(-SHR, 0, SHR, SH_H, C_GOLD, stroke=C_GOLD_DK, sw=2)
    # funnel mouth opening
    c.poly([(-0.62, SH_H), (-0.3, SH_H - 0.45), (0.3, SH_H - 0.45), (0.62, SH_H)],
           fill="#3d3d3d", stroke="none", close=True)

    # ---------- Choc pin entering from above ----------
    c.rect(-0.14, 0.9, 0.14, 3.2, C_PIN, stroke="#5c6067", sw=1.5)
    c.text_px(c.X(0), c.Z(3.5), "switch pin", 13, "middle", fill=C_NOTE)
    c.arrow(0.9, 2.6, 0.35, 1.2)
    c.text_px(c.X(1.0), c.Z(2.7), "plugs in from the top (hotswap)", 12.5)

    # ---------- section: how it sits in the adapter floor (right side inset) ----------
    # (drawn as ghost plastic around barrel)
    c.rect(-2.6, -2.8, -BR - 0.04, 0, C_ADAPTER, stroke=C_ADAPTER_DK, sw=1)
    c.rect(BR + 0.04, -2.8, 2.6, 0, C_ADAPTER, stroke=C_ADAPTER_DK, sw=1)
    c.text_px(c.X(-2.55), c.Z(-1.3), "printed", 11.5, "start", fill="#3c434b")
    c.text_px(c.X(-2.55), c.Z(-1.6), "floor", 11.5, "start", fill="#3c434b")

    # ---------- dimensions ----------
    c.dim_v(3.0, -BARREL_H, SH_H, '~4.3 mm body')
    c.dim_v(3.0, -BARREL_H - TAIL_H, -BARREL_H, "~3 mm TAIL")
    c.dim_h(-TAIL_R, TAIL_R, -BARREL_H - TAIL_H - 0.9, "φ0.64 mm", above=False)

    # ---------- labels ----------
    c.text_px(480, 36, "What is the solder tail? — Mill-Max receptacle anatomy", 21, "middle", bold=True)
    c.text_px(480, 60, "Part: Mill-Max 0300-1-15-15-47-27-10-0  (DigiKey ED90337-ND style listing, ~$0.79 ea) — accepts 0.64–0.94 mm pins", 13, "middle", fill=C_NOTE, italic=True)

    c.label(70, 200, ["MOUTH: funnel opening", "in the shoulder"], -0.5, 0.45, anchor="start")
    c.label(70, 280, ["CONTACT CLIP: 4 spring", "fingers inside grip the", "switch pin — this is the", "hotswap part"], -0.35, -1.4, anchor="start")
    c.label(70, 400, ["BARREL: machined brass", "sleeve — press-fits into a", "hole in the printed floor"], -BR, -3.2, anchor="start")
    c.label(70, 505, ["TAIL: solid brass pin,", "one piece with the barrel.", "On a normal PCB it goes", "through a plated hole and", "is soldered like a resistor", "leg. In our adapter: bend it", "1.3–2.7 mm sideways into", "the PG1425 hole."], 0.05, -5.3, anchor="start")

    c.label(660, 230, ["SHOULDER: stops the barrel", "at the floor surface"], SHR - 0.1, 0.3, anchor="start")

    # one-piece note
    c.text_px(660, 430, "The tail is NOT a separate part —", 13, fill=C_TEXT, bold=True)
    c.text_px(660, 448, "barrel + tail are machined from one", 13)
    c.text_px(660, 466, "piece of brass, then gold plated.", 13)
    c.text_px(660, 500, 'Beware: parts sold as "No Tail"', 13, fill=C_DIM, bold=True)
    c.text_px(660, 518, "(e.g. 0305-2, 7305) end flush at the", 13, fill=C_DIM)
    c.text_px(660, 536, "barrel bottom — no metal to reach", 13, fill=C_DIM)
    c.text_px(660, 554, "the PG1425 hole. Filter DigiKey by", 13, fill=C_DIM)
    c.text_px(660, 572, 'Tail Type = "Standard Tail".', 13, fill=C_DIM)

    c.text_px(480, 700, "Dimensions approximate — confirm on the Mill-Max 0300 datasheet before ordering", 12, "middle", fill=C_NOTE, italic=True)
    c.save("receptacle_anatomy.svg")


# ======================================================================
# Diagram 3 — Top view: pin/pad alignment with 90° CCW rotation
# ======================================================================
def top_view():
    # here "z" axis = footprint Y (Y-up handled by Canvas Z flip)
    c = Canvas(960, 700, cx=310, base=360, scale=22.0)

    # PCB + adapter outline
    c.rect(-13, -13, 13, 13, C_PCB, stroke=C_PCB_DARK, sw=2, rx=6)
    c.rect(-7.5, -7.5, 7.5, 7.5, "none", stroke="#fbfaf7", sw=2, dash="7,5")

    # central NPTH cutout (5.1 x 4.1)
    c.ellipse(0, 0, 2.55, 2.05, "#14401c", stroke="#0c2a12", sw=1.5)
    # locating holes
    for lx, ly in ((5.5, -4.6), (-5.5, 6.4)):
        c.circle(lx, ly, 0.65, "#14401c", stroke="#cfd8cf", sw=1.5)

    # PG1425 plated holes
    c.circle(-3.4, 3.8, 0.80, C_COPPER, stroke="#8a4e1f", sw=1.5)
    c.circle(-3.4, 3.8, 0.55, C_HOLE)
    c.circle(-3.4, -1.1, 0.70, C_COPPER, stroke="#8a4e1f", sw=1.5)
    c.circle(-3.4, -1.1, 0.55, C_HOLE)

    # ghost: Choc pins at 0 deg (reference)
    for gx, gy in ((0, 5.9), (5.0, 3.8)):
        c.rect(gx - 0.5, gy - 0.5, gx + 0.5, gy + 0.5, "none", stroke="#e8e0c8", sw=1.6, dash="3,3")

    # Choc pins after 90 deg CCW rotation
    for px_, py_ in ((-3.8, 5.0), (-5.9, 0.0)):
        c.rect(px_ - 0.5, py_ - 0.5, px_ + 0.5, py_ + 0.5, "#ffd23f", stroke="#8f7318", sw=1.6)

    # jog arrows
    c.arrow(-3.8, 5.0, -3.45, 3.95, color="#ff5544", sw=2.5)
    c.arrow(-5.9, 0.0, -3.55, -1.0, color="#ff5544", sw=2.5)

    # in-figure labels
    c.text_px(c.X(-3.0), c.Z(4.9), "1.26 mm", 13, "start", fill="#ffdcd6", bold=True)
    c.text_px(c.X(-6.0), c.Z(-2.3), "2.73 mm", 13, "start", fill="#ffdcd6", bold=True)
    c.text_px(c.X(0), c.Z(-0.05) + 4, "central cutout", 11, "middle", fill="#9fbfa4")
    c.text_px(c.X(0), c.Z(-8.4), "adapter footprint 15 × 15 (dashed)", 12, "middle", fill="#e8f0e8")

    # title
    c.text_px(480, 36, "Top view — why rotating the Choc 90° CCW almost solves it", 21, "middle", bold=True)
    c.text_px(480, 58, "PG1425 PCB seen from above; Choc pin landing spots vs. PG1425 plated holes (to scale)",
              13, "middle", fill=C_NOTE, italic=True)

    # legend
    lx, ly = 660, 130
    c.text_px(lx, ly, "Legend", 15, bold=True)
    items = [
        (C_COPPER, "circle", "PG1425 plated hole (1.1 mm drill)"),
        ("#14401c", "circle", "φ1.3 locating hole (alignment post)"),
        ("#ffd23f", "rect", "Choc pin, switch rotated 90° CCW"),
        ("none", "rect-dash", "Choc pin at 0° (reference)"),
        ("#ff5544", "arrow", "Required jog — bendable distance"),
    ]
    for k, (col, shape, txt) in enumerate(items):
        y = ly + 28 + k * 30
        if shape == "circle":
            c.el.append(f'<circle cx="{lx+9}" cy="{y-4}" r="8" fill="{col}" stroke="#666"/>')
        elif shape == "rect":
            c.el.append(f'<rect x="{lx+1}" y="{y-12}" width="16" height="16" fill="{col}" stroke="#8f7318"/>')
        elif shape == "rect-dash":
            c.el.append(f'<rect x="{lx+1}" y="{y-12}" width="16" height="16" fill="none" stroke="#b8a86a" stroke-dasharray="3,3" stroke-width="1.6"/>')
        elif shape == "arrow":
            c.el.append(f'<line x1="{lx}" y1="{y-4}" x2="{lx+18}" y2="{y-4}" stroke="{col}" stroke-width="2.5" marker-end="url(#arr)"/>')
        c.text_px(lx + 26, y, txt, 12.5)

    c.text_px(lx, ly + 200, "Trade-off: keycap sits rotated 90°.", 12.5, fill=C_NOTE)
    c.text_px(lx, ly + 218, "Fine for blank caps; sideways", 12.5, fill=C_NOTE)
    c.text_px(lx, ly + 236, "legends otherwise. Keep 0° as a", 12.5, fill=C_NOTE)
    c.text_px(lx, ly + 254, "parametric variant (needs the", 12.5, fill=C_NOTE)
    c.text_px(lx, ly + 272, "bus-wire bridge, Option D).", 12.5, fill=C_NOTE)

    c.save("top_view_pin_alignment.svg")


# ======================================================================
# Diagram 4 — In-slot solution (matches v3 adapter SCAD, 0° rotation)
# ======================================================================
def in_slot_solution():
    """Two panels: (top) real slot routing seen from above, from the SCAD;
    (bottom) cross-section along slot 1 with a bus wire / harvested contact."""
    c = Canvas(960, 760, cx=250, base=300, scale=17.0)

    # ---------------- TOP PANEL: top view of v3 floor with slots ----------
    # body 15x15
    c.rect(-7.5, -7.5, 7.5, 7.5, C_ADAPTER, stroke=C_ADAPTER_DK, sw=2, rx=1)
    # Choc post holes (through floor)
    c.circle(0, 0, 1.7, "#e8e6e1", stroke="#777", sw=1)        # center post 3.2+cl
    c.circle(-5.5, 0, 1.05, "#e8e6e1", stroke="#777", sw=1)    # side posts
    c.circle(5.5, 0, 1.05, "#e8e6e1", stroke="#777", sw=1)
    # slots (1.4 wide) as thick lines — true SCAD paths
    slot1 = [(0, 5.9), (-3.4, 2.9)]
    slot2 = [(5.0, 3.8), (2.4, -3.0), (-3.4, -2.0)]
    for pts in (slot1, slot2):
        c.poly(pts, stroke="#e8e6e1", sw=1.4 * 17.0)
        c.poly(pts, stroke="#777", sw=1)
    # bus wires lying in slots
    for pts in (slot1, slot2):
        c.poly(pts, stroke="#c87533", sw=8)
    # PG1425 plated holes under slot ends
    for hx, hy in ((-3.4, 2.9), (-3.4, -2.0)):
        c.circle(hx, hy, 0.8, C_COPPER, stroke="#8a4e1f", sw=1.5)
        c.circle(hx, hy, 0.55, C_HOLE)
    # Choc pin positions
    for px_, py_ in ((0, 5.9), (5.0, 3.8)):
        c.circle(px_, py_, 0.6, C_PIN, stroke="#444", sw=1.5)
    # alignment pins (bottom side)
    for ax, ay in ((5.5, -5.5), (-5.5, 5.5)):
        c.circle(ax, ay, 0.6, "none", stroke="#3c434b", sw=1.8)

    c.text_px(480, 34, "The captive-channel solution — v3.1 adapter", 21, "middle", bold=True)
    c.text_px(480, 56, "Top: floor viewed from above with the two wire channels (true SCAD paths). Bottom: section along channel 1.",
              13, "middle", fill=C_NOTE, italic=True)

    c.label(560, 110, ["Choc pin drops in here — through-", "pocket (φ1.6) at (0,5.9) & (5,3.8)"], 5.0, 3.8)
    c.label(560, 175, ["0.6 mm bus wire laid into the channel", "from ABOVE — channel is the jig"], 3.7, 0.6)
    c.label(560, 240, ["Channel 2 detours around the", "center/side-post pockets"], 2.4, -3.0)
    c.label(560, 300, ["Wire exit through-hole (φ1.4) —", "wire bends down into PG1425 hole"], -3.4, -2.0)
    c.label(560, 360, ["Printed alignment pins (bottom)", "index the whole thing on the PCB"], 5.5, -5.5)
    c.label(120, 110, ["Channels: 1.4 mm wide, open at the", "TOP only — a 0.5 mm floor membrane", "closes the bottom so the wire", "cannot fall out"], -1.7, 4.4, anchor="start")

    # ---------------- BOTTOM PANEL: section along slot 1 ------------------
    c2_base = 640           # px baseline for section panel
    s2 = 34.0               # px/mm for section
    cx2 = 300

    def SX(x):  # section x: distance along slot (mm)
        return cx2 + x * s2

    def SZ(z):  # section z: height above PCB top (mm)
        return c2_base - z * s2

    def srect(x0, z0, x1, z1, fill, stroke="none", sw=1):
        X0, X1 = sorted([SX(x0), SX(x1)])
        Z0, Z1 = sorted([SZ(z0), SZ(z1)])
        c.el.append(f'<rect x="{X0:.1f}" y="{Z0:.1f}" width="{X1-X0:.1f}" height="{Z1-Z0:.1f}" '
                    f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    # PCB (1.6) with plated hole at x=4.53 (channel 1 length)
    HL = 4.53
    MEM = 0.5   # membrane thickness
    srect(-3, -1.6, 9, 0, C_PCB, stroke=C_PCB_DARK, sw=1.5)
    srect(HL - 0.55, -1.6, HL + 0.55, 0, C_HOLE)
    srect(HL - 0.85, -0.18, HL + 0.85, 0, C_COPPER)
    srect(HL - 0.85, -1.6, HL + 0.85, -1.42, C_COPPER)
    # floor 2.8: side walls full height; membrane closes channel bottom
    srect(-3, 0, -0.8, 2.8, C_ADAPTER, stroke=C_ADAPTER_DK, sw=1.5)       # left wall
    srect(HL + 0.7, 0, 9, 2.8, C_ADAPTER, stroke=C_ADAPTER_DK, sw=1.5)    # right wall
    # membrane under channel: from pin pocket edge to exit hole edge
    srect(0.8, 0, HL - 0.7, MEM, C_ADAPTER, stroke=C_ADAPTER_DK, sw=1.5)
    # (pin-entry pocket x=-0.8..0.8 open full depth; exit hole HL-0.7..HL+0.7 open)
    # switch body above (schematic)
    srect(-3, 2.8, 9, 4.6, C_SWITCH, stroke=C_SWITCH_DK, sw=1.5)
    # Choc pin descending in the entry pocket at x=0 (2.65 long from floor top)
    srect(-0.15, 0.15, 0.15, 2.8, C_PIN, stroke="#5c6067", sw=1.5)
    # bus wire: lies ON the membrane, runs to exit hole, bends down through it
    c.el.append(f'<polyline points="{SX(0):.0f},{SZ(MEM + 0.3):.0f} {SX(HL):.0f},{SZ(MEM + 0.3):.0f} '
                f'{SX(HL):.0f},{SZ(-1.5):.0f}" fill="none" stroke="#c87533" stroke-width="9" '
                f'stroke-linejoin="round" stroke-linecap="round"/>')
    # solder joints: pin<->wire (via entry pocket), wire<->PCB underside
    c.el.append(f'<circle cx="{SX(0):.0f}" cy="{SZ(MEM + 0.35):.0f}" r="9" fill="{C_SOLDER}" stroke="#8d919a"/>')
    c.el.append(f'<polygon points="{SX(HL)-16:.0f},{SZ(-1.6):.0f} {SX(HL)+16:.0f},{SZ(-1.6):.0f} '
                f'{SX(HL)+5:.0f},{SZ(-1.6)+13:.0f} {SX(HL)-5:.0f},{SZ(-1.6)+13:.0f}" '
                f'fill="{C_SOLDER}" stroke="#8d919a"/>')

    c.text_px(480, 495, "Section along channel 1 — 0.5 mm membrane traps the wire; switch body caps the top", 14, "middle", bold=True)
    c.text_px(SX(0), SZ(3.2) - 40, "Choc pin in entry pocket (full depth)", 12, "middle", fill=C_NOTE)
    c.el.append(f'<line x1="{SX(0):.0f}" y1="{SZ(3.2)-36:.0f}" x2="{SX(0):.0f}" y2="{SZ(2.2):.0f}" stroke="#555" stroke-width="1" stroke-dasharray="3,3"/>')
    c.text_px(SX(2.2), SZ(MEM + 0.3) - 14, "wire on membrane", 12, "middle", fill="#8a4e1f", bold=True)
    c.text_px(SX(2.4), SZ(MEM) + 16, "0.5 mm membrane (closed bottom)", 11.5, "middle", fill="#3c434b", bold=True)
    c.text_px(SX(0) - 30, SZ(0.35) + 28, "solder pin↔wire (via entry pocket)", 11.5, "end")
    c.text_px(SX(HL) + 30, SZ(-1.6) + 24, "solder wire↔PCB (underside, via exit hole)", 11.5)
    c.text_px(SX(-2.2), SZ(1.4) + 4, "floor 2.8", 12, "middle", fill=C_DIM, bold=True)
    c.text_px(SX(7.2), SZ(-0.8) + 4, "PCB 1.6", 12, "middle", fill=C_DIM, bold=True)

    c.text_px(480, 745, "Assembly: lay wire into channel from above → seat switch (caps channel, pin lands beside wire) → solder at entry pocket + exit hole",
              12, "middle", fill=C_NOTE, italic=True)
    c.save("in_slot_solution.svg")


if __name__ == "__main__":
    receptacle_anatomy()
    option_a()
    option_b()
    top_view()
    in_slot_solution()
