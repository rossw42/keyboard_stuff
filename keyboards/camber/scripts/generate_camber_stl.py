#!/usr/bin/env python3
"""
Extrude micro_alice_hull_plate.dxf to a 3mm STL.
Builds the plate outline directly from known coordinates,
then subtracts switch cutouts parsed from the DXF.
"""
import math
import ezdxf
import cadquery as cq
from shapely.geometry import Polygon, LinearRing
from shapely.ops import unary_union, polygonize

THICKNESS = 1.5
DXF_FILE  = "dxf/camber_hull_plate_mx.dxf"
STL_FILE  = "stl/camber_hull_plate_mx.stl"


def arc_pts(cx, cy, r, start_deg, end_deg, n=24):
    if end_deg <= start_deg:
        end_deg += 360
    return [(cx + r*math.cos(math.radians(start_deg + (end_deg-start_deg)*i/n)),
             cy + r*math.sin(math.radians(start_deg + (end_deg-start_deg)*i/n)))
            for i in range(n+1)]


def build_outline():
    """
    Trace the Hull plate outline as an ordered polygon.
    Uses the exact compound-arc tab geometry from Omnibus_Hull.dxf.
    Each tab corner: 2.675mm outer → 0.5mm transition → 1.25mm inner → 0.5mm → 2.675mm outer
    """
    R1 = 2.675; R2 = 0.5; R3 = 1.25; R_inner = 1.5

    pts = []
    # Top edge right to left
    pts.append((11.85, 66.675))
    pts.append((-235.6875, 66.675))

    # Left top tab corner (5-arc compound, center at -235.6875, 64.0)
    pts.extend(arc_pts(-235.6875, 64.0, R1, 90, 127.8792))
    pts.extend(arc_pts(-237.0229, 65.7167, R2, 127.8792, 258.8119))
    pts.extend(arc_pts(-237.3625, 64.0, R3, -78.8119, 78.8119))
    pts.extend(arc_pts(-237.0229, 62.2833, R2, 101.1881, 232.1208))
    pts.extend(arc_pts(-235.6875, 64.0, R1, 232.1208, 270))

    # Left shoulder + inner tab
    pts.append((-235.6875, 61.325))
    pts.append((-234.8625, 61.325))
    pts.extend(arc_pts(-234.8625, 59.825, R_inner, 0, 90))
    pts.append((-233.3625, 59.825))
    pts.append((-233.3625, -2.675))
    pts.extend(arc_pts(-234.8625, -2.675, R_inner, -90, 0))
    pts.append((-234.8625, -4.175))
    pts.append((-235.6875, -4.175))

    # Left bottom tab corner (5-arc compound, center at -235.6875, -6.85)
    pts.extend(arc_pts(-235.6875, -6.85, R1, 90, 127.8792))
    pts.extend(arc_pts(-237.0229, -5.1333, R2, 127.8792, 258.8119))
    pts.extend(arc_pts(-237.3625, -6.85, R3, -78.8119, 78.8119))
    pts.extend(arc_pts(-237.0229, -8.5667, R2, 101.1881, 232.1208))
    pts.extend(arc_pts(-235.6875, -6.85, R1, 232.1208, 270))

    # Bottom edge left to right
    pts.append((-235.6875, -9.525))
    pts.append((11.85, -9.525))

    # Right bottom tab corner (5-arc compound, center at 11.85, -6.85)
    pts.extend(arc_pts(11.85, -6.85, R1, 270, 307.8792))
    pts.extend(arc_pts(13.1854, -8.5667, R2, -52.1208, 78.8119))
    pts.extend(arc_pts(13.525, -6.85, R3, 101.1881, 258.8119))
    pts.extend(arc_pts(13.1854, -5.1333, R2, -78.8119, 52.1208))
    pts.extend(arc_pts(11.85, -6.85, R1, 52.1208, 90))

    # Right shoulder + inner tab
    pts.append((11.85, -4.175))
    pts.append((11.025, -4.175))
    pts.extend(arc_pts(11.025, -2.675, R_inner, 180, 270))
    pts.append((9.525, -2.675))
    pts.append((9.525, 59.825))
    pts.extend(arc_pts(11.025, 59.825, R_inner, 90, 180))
    pts.append((11.025, 61.325))
    pts.append((11.85, 61.325))

    # Right top tab corner (5-arc compound, center at 11.85, 64.0)
    pts.extend(arc_pts(11.85, 64.0, R1, 270, 307.8792))
    pts.extend(arc_pts(13.1854, 62.2833, R2, -52.1208, 78.8119))
    pts.extend(arc_pts(13.525, 64.0, R3, 101.1881, 258.8119))
    pts.extend(arc_pts(13.1854, 65.7167, R2, -78.8119, 52.1208))
    pts.extend(arc_pts(11.85, 64.0, R1, 52.1208, 90))

    return Polygon(pts)


def build_cutouts(msp):
    """Reconstruct switch cutouts from SWITCHES layer using polygonize."""
    from shapely.geometry import LineString
    geoms = []
    for e in msp.query('LINE[layer=="SWITCHES"]'):
        geoms.append(LineString([
            (e.dxf.start.x, e.dxf.start.y),
            (e.dxf.end.x,   e.dxf.end.y)
        ]))
    merged = unary_union(geoms)
    polys  = list(polygonize(merged))
    print(f"  Found {len(polys)} switch cutouts")
    return polys


def shapely_poly_to_cq_wire(poly, wp):
    """Add a shapely polygon exterior as a closed wire to a CadQuery workplane."""
    pts = list(poly.exterior.coords[:-1])  # drop repeated last point
    return wp.polyline(pts).close()


def main():
    doc = ezdxf.readfile(DXF_FILE)
    msp = doc.modelspace()

    print("Building outline...")
    outline = build_outline()
    print(f"  Outline area: {outline.area:.1f} mm²")

    print("Building switch cutouts...")
    cutouts = build_cutouts(msp)

    print("Subtracting cutouts...")
    plate = outline.buffer(0)  # fix any self-intersections from arc discretization
    for cut in cutouts:
        plate = plate.difference(cut)
    print(f"  Plate area after cutouts: {plate.area:.1f} mm²")

    print("Extruding with CadQuery...")
    # Use the cleaned shapely plate polygon (outline minus cutouts)
    # Simplify slightly to remove near-duplicate points from arc discretization
    clean_outline = outline.buffer(0).simplify(0.001, preserve_topology=True)
    outline_pts = list(clean_outline.exterior.coords[:-1])

    solid = (cq.Workplane("XY")
               .polyline(outline_pts)
               .close()
               .extrude(THICKNESS))

    # Cut each switch hole
    for cut in cutouts:
        cut_pts = list(cut.exterior.coords[:-1])
        solid = (solid
                 .faces(">Z")
                 .workplane()
                 .polyline(cut_pts)
                 .close()
                 .cutThruAll())

    print(f"Exporting to {STL_FILE}...")
    cq.exporters.export(solid, STL_FILE)
    print(f"✅ Done — {STL_FILE}")


if __name__ == "__main__":
    main()
