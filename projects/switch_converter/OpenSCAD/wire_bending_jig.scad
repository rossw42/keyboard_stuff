// ============================================================================
// PG1350 -> PG1425 Wire-Forming Jig
// Companion tool for pg1350_to_pg1425_adapter.scad (v3.1 captive wire channels)
//
// PURPOSE:
//   Bends 0.5-0.6mm solid tinned-copper bus wire (or diode legs, same diameter)
//   into the EXACT shape needed for each of the adapter's two captive wire
//   channels (see ../electrical_connection_research.md, "Option 2 - Jig-formed
//   bus wire").
//   36 keys x 2 wires = 72 wires needed for a full le-oeuf board, so a
//   repeatable forming jig is worth the print.
//
// GEOMETRY SOURCE OF TRUTH:
//   The point coordinates below are copied VERBATIM from the `slots` array
//   in pg1350_to_pg1425_adapter.scad. If that file's slot geometry ever
//   changes, update the numbers here to match (they are intentionally
//   duplicated rather than shared, since this file must stay a standalone
//   print-and-use tool).
//
// HOW IT WORKS -- BENDING LANES:
//   Each channel becomes one "lane" on the jig:
//     - A short peg is printed at the START point (where the Choc pin sits)
//       and at any interior BEND point (channel 2 only). Wrap the wire
//       around these pegs, pulling it taut, and the pin spacing/angle of
//       the real channel is reproduced automatically.
//     - A through-hole (full plate thickness) sits at the END point (where
//       the wire drops into the PG1425 PCB hole). Press the taut wire tail
//       straight down into this hole: it (a) locates the bend at exactly
//       the right XY position, (b) forms a clean 90 degree bend, and
//       (c) gives a consistent ~3mm tail in one motion.
//     - A shallow engraved groove traces the path between points as a
///      visual guide only (not required to hold the wire - the pegs and
//       end hole do that).
//
// HOW IT WORKS -- HORIZONTAL CUT-LENGTH GAUGES:
//   Two low rails lie FLAT on the plate (one per channel), each with an
//   open-top U-groove running along it. Everything happens from above -
//   you never flip the jig.
//     - The groove is closed off by a solid STOP WALL at its left end.
//     - The rail's right end is a clean vertical CUT FACE, positioned at
//       exactly `cut_length` from the stop wall.
//     - Immediately past the cut face is a rectangular CUTTER-RELIEF SLOT
//       cut all the way through the plate, so flush-cutter jaws can close
//       completely against the cut face without hitting the plate.
//
//   To cut a wire: drop it into the groove, slide it left until it butts
//   against the stop wall, then snip flush against the vertical cut face.
//   The result is exactly `cut_length` every time - path length plus a
//   3mm solder tail at each end.
//
//   CH1 cut length: 4.5mm path + 3mm + 3mm tails = 10.5mm
//   CH2 cut length: 13.2mm path + 3mm + 3mm tails = 19.2mm
//
// USAGE:
//   PRE-CUT WIRES (horizontal gauge rails, no flipping):
//   1a. Lay a wire into the CH1 (or CH2) groove.
//   1b. Slide it left until it stops against the wall.
//   1c. Snip flush against the vertical face at the far end of the rail.
//       The relief slot below lets the cutters close all the way.
//
//   FORM WIRES (bending lanes with pegs):
//   2. Lane CH1 (straight): hook wire at the START peg, pull taut along the
//      groove, press the tail into the END hole.
//   3. Lane CH2 (bent): hook at START peg, wrap around the MID peg, pull
//      taut along the second groove segment, press the tail into the END
//      hole.
//   4. Lift the formed wire off the pegs. Solder pin-end to the Choc pin,
//      tail-end into the PG1425 plated hole.
//
// PRINT NOTES:
//   - Print flat, pegs pointing up, NO SUPPORTS NEEDED. The gauge rails are
//     low solid bars with open-top grooves (cut down from above) and the
//     relief slots are straight vertical through-cuts - all self-supporting.
//   - 0.2mm layers, PETG or PLA. The forming pegs (1.3mm dia x 5mm tall)
//     are the finest feature.
//   - If a forming peg snaps after heavy use, reprint with `peg_d` bumped to
//     1.6-1.8mm, or drill out the stub and press in a short length of 1.3mm
//     steel wire/pin stock for a near-indestructible version.
// ============================================================================

$fn = 32;

// ---------------------------------------------------------------------------
// CHANNEL GEOMETRY -- copied verbatim from pg1350_to_pg1425_adapter.scad
// (switch-center-relative coordinates, OpenSCAD Y-up convention)
// ---------------------------------------------------------------------------
choc_pin1_pos    = [ 0.0,  5.9];   // channel 1 start (Choc pin 1)
choc_pin2_pos    = [ 5.0,  3.8];   // channel 2 start (Choc pin 2)
pg1425_pin1_pos  = [-3.4,  2.9];   // channel 1 end   (PG1425 hole 1)
pg1425_pin2_pos  = [-3.4, -2.0];   // channel 2 end   (PG1425 hole 2)
slot2_bend_pos   = [ 2.4, -3.0];   // channel 2 interior bend point

// Same structure as the adapter's `slots` array:
//   slots[0] = channel 1 : straight,  4.53mm
//   slots[1] = channel 2 : 7.28mm + 5.89mm, ~101 deg interior bend
slots = [
    [ choc_pin1_pos, pg1425_pin1_pos ],
    [ choc_pin2_pos, slot2_bend_pos, pg1425_pin2_pos ],
];

slot_lengths_mm  = [ "4.5",  "13.2" ];  // string labels for plate text
slot_lengths_num = [  4.5,    13.2  ];  // numeric, for cut-length math

// ---------------------------------------------------------------------------
// WIRE / JIG FIT PARAMETERS
// ---------------------------------------------------------------------------
wire_d      = 0.60;   // mm - target wire diameter (24AWG solid tinned copper / diode leg)
peg_d       = 1.30;   // mm - printed forming-peg diameter (wraps the wire)
peg_h       = 5.0;    // mm - peg height above the plate top surface
hole_clear  = 0.35;   // mm - clearance added to wire_d for the end-forming hole
groove_w    = 1.6;    // mm - shallow guide-groove width (visual aid only)
groove_d    = 0.35;   // mm - shallow guide-groove depth

plate_t     = 3.0;    // mm - plate thickness = the formed tail length
plate_w     = 74;     // mm
plate_h     = 44;     // mm
plate_r     = 4;      // mm - corner rounding

// Where each slot's FIRST point (the start peg) lands on the plate.
lane_origins = [ [20, 32], [52, 34] ];

// ---------------------------------------------------------------------------
// HORIZONTAL CUT-GAUGE PARAMETERS
// ---------------------------------------------------------------------------
solder_tail = 3.0;    // mm - solder-tail allowance added at EACH end of the wire
                      // (total wire = path_length + 2 * solder_tail)

// Computed cut lengths (path + both tails):
cut_len = [ for (l = slot_lengths_num) l + 2 * solder_tail ];
//   cut_len[0] = 4.5  + 6 = 10.5 mm  (CH1)
//   cut_len[1] = 13.2 + 6 = 19.2 mm  (CH2)

gauge_rail_h   = 3.5;              // mm - rail height above the plate top
gauge_rail_w   = 6.0;              // mm - rail width (across the groove, Y)
gauge_groove_w = wire_d + 0.60;    // mm - ~1.2mm: wire drops in easily, stays put

// Groove is cut the FULL rail height, so its floor is the plate top surface.
// This is important: the wire then lies in the same plane as the plate top,
// which is also the top of the cutter-relief through-slot. The overhanging
// wire tail therefore has the ENTIRE plate thickness of open air beneath it,
// letting flush-cutter jaws close fully against the cut face.
gauge_groove_d = gauge_rail_h;

gauge_stop_t   = 2.5;              // mm - solid stop-wall thickness at the groove start
gauge_relief_l = 8.0;              // mm - cutter-relief slot length past the cut face
gauge_relief_w = 7.0;              // mm - cutter-relief slot width (Y) - wider than the
                                   //      rail so jaws clear the rail sides too

// Gauge rail placement: [ x of the STOP FACE (groove start), y center of rail ]
// Both run left-to-right; wire butts left, cut happens at the right end.
gauge_origin = [ [8, 23], [8, 13] ];   // CH1 upper rail, CH2 lower rail

// ---------------------------------------------------------------------------
// MODULES
// ---------------------------------------------------------------------------

// Rounded-corner flat plate, bottom face at z = 0, corner at XY origin.
module rounded_plate(w, h, t, r) {
    linear_extrude(height = t)
        offset(r = r) offset(delta = -r)
            square([w, h], center = false);
}

// Translate a slot's point list so its first point sits at `origin`
// (keeps every relative vector - and therefore every length/angle -
// identical to the real adapter channel).
function lane_points(slot, origin) =
    [ for (p = slot) [ p[0] - slot[0][0] + origin[0],
                       p[1] - slot[0][1] + origin[1] ] ];

// Shallow engraved line tracing the wire path (visual alignment aid only).
module guide_groove(pts) {
    for (i = [0 : len(pts) - 2])
        hull() {
            translate([pts[i][0],   pts[i][1],   plate_t - groove_d + 0.02])
                cylinder(h = groove_d, d = groove_w);
            translate([pts[i+1][0], pts[i+1][1], plate_t - groove_d + 0.02])
                cylinder(h = groove_d, d = groove_w);
        }
}

// Forming pegs at every point EXCEPT the last (start + any mid bend points).
module forming_pegs(pts) {
    for (i = [0 : len(pts) - 2])
        translate([pts[i][0], pts[i][1], plate_t])
            cylinder(h = peg_h, d = peg_d);
}

// Through-hole at the LAST point - press the tail straight down into this.
module end_hole(pts) {
    p = pts[len(pts) - 1];
    translate([p[0], p[1], -0.5])
        cylinder(h = plate_t + 1, d = wire_d + hole_clear);
}

// Small ruler (0-20mm) for reference.
module ruler(x0, y0) {
    for (i = [0 : 20]) {
        major = (i % 5 == 0);
        translate([x0 + i, y0, plate_t - 0.30])
            cube([0.3, major ? 2.4 : 1.2, 0.35], center = false);
    }
    for (i = [0, 5, 10, 15, 20])
        translate([x0 + i - 1.0, y0 + 3.0, plate_t - 0.35])
            linear_extrude(height = 0.4)
                text(str(i), size = 2.0, font = "Liberation Sans");
}

// Lane labels + reference channel length, engraved.
module lane_label(origin, tag, len_str) {
    translate([origin[0] - 5, origin[1] + 5, plate_t - 0.35])
        linear_extrude(height = 0.4)
            text(tag, size = 3.0, font = "Liberation Sans:style=Bold");
    translate([origin[0] - 5, origin[1] + 1.8, plate_t - 0.35])
        linear_extrude(height = 0.4)
            text(str(len_str, "mm"), size = 2.0, font = "Liberation Sans");
}

// ---------------------------------------------------------------------------
// HORIZONTAL CUT GAUGE
//   Rail body: solid bar lying flat on the plate. Spans from the back of the
//   stop wall (x0 - stop_t) to the CUT FACE at (x0 + cut_length).
//   Wire seats in an open-top groove that starts at the stop wall face (x0).
// ---------------------------------------------------------------------------
module cut_gauge_rail(org, cut_length) {
    x0 = org[0];
    yc = org[1];
    translate([x0 - gauge_stop_t, yc - gauge_rail_w / 2, plate_t])
        cube([gauge_stop_t + cut_length, gauge_rail_w, gauge_rail_h]);
}

// Open-top U-groove: begins at the stop-wall face (x0) and runs to the cut
// face. Cut the full rail height, so the wire seats on the plate top surface.
module cut_gauge_groove(org, cut_length) {
    x0 = org[0];
    yc = org[1];
    translate([x0, yc - gauge_groove_w / 2, plate_t])
        cube([cut_length + 0.01, gauge_groove_w, gauge_groove_d + 1]);
}

// Cutter-relief slot: rectangular through-cut in the plate starting exactly
// at the cut face, so flush-cutter jaws close fully against that face.
module cut_gauge_relief(org, cut_length) {
    x0 = org[0];
    yc = org[1];
    translate([x0 + cut_length, yc - gauge_relief_w / 2, -0.5])
        cube([gauge_relief_l, gauge_relief_w, plate_t + 1]);
}

// Engraved witness tick on the plate top, marking the cut plane.
module cut_gauge_cutline(org, cut_length) {
    x0 = org[0];
    yc = org[1];
    translate([x0 + cut_length - 0.2, yc + gauge_rail_w / 2 + 0.6,
               plate_t - 0.40])
        cube([0.4, 2.5, 0.5]);
}

// Engraved label on the plate, right of the relief slot: "CH1  10.5mm"
module cut_gauge_label(org, cut_length, tag) {
    x0 = org[0];
    yc = org[1];
    translate([x0 + cut_length + gauge_relief_l + 2.5, yc - 1.2,
               plate_t - 0.35])
        linear_extrude(height = 0.4)
            text(str(tag, "  ", cut_length, "mm"), size = 2.4,
                 font = "Liberation Sans:style=Bold");
}

// ---------------------------------------------------------------------------
// ASSEMBLY
// ---------------------------------------------------------------------------
module jig() {
    pts0 = lane_points(slots[0], lane_origins[0]);
    pts1 = lane_points(slots[1], lane_origins[1]);

    difference() {
        union() {
            rounded_plate(plate_w, plate_h, plate_t, plate_r);
            forming_pegs(pts0);
            forming_pegs(pts1);
            // Horizontal cut-gauge rails (solid bodies)
            cut_gauge_rail(gauge_origin[0], cut_len[0]);
            cut_gauge_rail(gauge_origin[1], cut_len[1]);
        }
        // --- Bending-lane features ---
        guide_groove(pts0);
        guide_groove(pts1);
        end_hole(pts0);
        end_hole(pts1);
        lane_label(lane_origins[0], "CH1", slot_lengths_mm[0]);
        lane_label(lane_origins[1], "CH2", slot_lengths_mm[1]);

        // --- Reference ruler ---
        ruler(6, 4);

        // --- Cut-gauge features ---
        cut_gauge_groove (gauge_origin[0], cut_len[0]);
        cut_gauge_groove (gauge_origin[1], cut_len[1]);
        cut_gauge_relief (gauge_origin[0], cut_len[0]);
        cut_gauge_relief (gauge_origin[1], cut_len[1]);
        cut_gauge_cutline(gauge_origin[0], cut_len[0]);
        cut_gauge_cutline(gauge_origin[1], cut_len[1]);
        cut_gauge_label  (gauge_origin[0], cut_len[0], "CH1");
        cut_gauge_label  (gauge_origin[1], cut_len[1], "CH2");

        // --- Thumb hang-hole, top-right corner ---
        translate([plate_w - 8, plate_h - 8, -0.5])
            cylinder(h = plate_t + 1, d = 4);
    }
}

jig();

// ============================================================================
// END OF FILE
// ============================================================================
