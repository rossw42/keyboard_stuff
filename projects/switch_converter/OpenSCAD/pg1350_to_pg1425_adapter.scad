// ============================================================================
// PG1350 -> PG1425 Switch Adapter (Rectangular Block Design, v3.1)
//
// CONCEPT:
//   A rectangular block, like a tiny "adapter PCB" with a bezel:
//     * TOP SIDE : recessed POCKET that the PG1350 (Kailh Choc) bottom
//                  housing drops INTO. Pocket floor has the TRUE Choc
//                  footprint: center post, 2 plastic locating posts,
//                  and 2 electrical pins.
//     * BOTTOM SIDE: - SQUARE center alignment post fitting the PG1425
//                      PCB's square center hole (primary alignment)
//                    - round pin posts matching the PG1425 PCB hole pattern
//                    - two routing channels for the dual-ended stamped
//                      contacts (Choc pin exits -> PG1425 pad positions)
//
// Z REFERENCE: z = 0 is the BOTTOM face of the block (sits on PG1425 PCB).
//   Posts extend below z = 0 into the PCB holes.
//
// KAILH CHOC PG1350 TRUE BOTTOM LAYOUT (viewed from above, switch north up):
//     center post  phi 3.2  at ( 0.0,  0.0 )
//     locating post phi 1.9 at (-5.5,  0.0 ) and ( 5.5, 0.0 )
//     electrical pin phi~1.0 at ( 0.0,  5.9 ) and ( 5.0, 3.8 )
//     bottom housing 13.8 x 13.8, height 2.2 below the 15x15 flange
// ============================================================================

// ---------------------------------------------------------------------------
// PRINT / TOLERANCE SETTINGS
// ---------------------------------------------------------------------------
$fn = 48;                      // Curve smoothness

pocket_clearance = 0.30;       // mm - added to pocket size (Choc body drop-in fit)
hole_clearance   = 0.20;       // mm - added to hole diameters (switch post/pin fit)
post_clearance   = 0.15;       // mm - subtracted from post sizes (PCB hole fit)
eps              = 0.10;       // mm - overlap fudge for clean booleans

// ---------------------------------------------------------------------------
// PG1350 (Kailh Choc) TRUE DIMENSIONS - TOP-SIDE INTERFACE
// ---------------------------------------------------------------------------
choc_body_xy         = 13.80;  // mm - Choc bottom-housing footprint (square)
choc_body_h          = 2.20;   // mm - bottom housing height below the flange
choc_flange_xy       = 15.00;  // mm - top lip / flange size (datasheet: 15.00)

choc_center_post_d   = 3.20;   // mm - center post diameter,  at (0, 0)
choc_center_post_len = 2.65;   // mm - center post length below housing

choc_side_post_d     = 1.90;   // mm - plastic locating post diameter (x2)
choc_side_post_x     = 5.50;   // mm - locating posts at (+/-5.5, 0)
choc_side_post_len   = 2.65;   // mm - locating post length below housing

choc_pin_d           = 1.20;   // mm - electrical pin hole diameter (PCB drill)
choc_pin_len         = 2.65;   // mm - pin length below housing
choc_pin1_pos        = [ 0.0, 5.9 ];  // mm - pin 1 position (switch center = origin)
choc_pin2_pos        = [ 5.0, 3.8 ];  // mm - pin 2 position

// ---------------------------------------------------------------------------
// PG1425 BOTTOM-SIDE INTERFACE  (block bottom fits the PG1425 PCB footprint)
// ---------------------------------------------------------------------------
// FROM VERIFIED KICAD FOOTPRINT (shikamiya/kicad-footprint-kailh-pg1425-x-switch,
// saved locally as Kailh-PG1425-X-Switch.kicad_mod). Coordinates below are
// relative to the switch center, OpenSCAD convention (Y up):
//   - 2 NON-PLATED alignment holes phi 1.30 at ( 5.5, -5.5) and (-5.5,  5.5)
//     -> the switch's non-metallic alignment pins; we print matching posts
//   - 2 PLATED pin holes drill phi 1.10 at (-3.4,  2.9) [pin1] and (-3.4, -2.0) [pin2]
//   - large center cutout ~5.1 x 4.1 mm at (0, -0.9) (open hole in the PCB)
pg1425_align_hole_d     = 1.30;   // mm - non-plated alignment hole diameter
pg1425_align_positions  = [ [ 5.5, -5.5], [-5.5,  5.5] ];
pg1425_align_pin_h      = 1.40;   // mm - printed alignment pin length (< PCB thickness)

pg1425_pin1_pos         = [-3.4,  2.9];   // mm - plated pin hole 1 (drill 1.10)
pg1425_pin2_pos         = [-3.4, -2.0];   // mm - plated pin hole 2 (drill 1.10)

// Center cutout in the PCB (informational - it is an open hole, the adapter
// bottom face simply spans it; no boss needed since alignment pins locate us)
pg1425_cutout_size      = [ 5.1, 4.1 ];   // mm
pg1425_cutout_pos       = [ 0, -0.9 ];    // mm

// ---------------------------------------------------------------------------
// ADAPTER BODY
// The outer body matches the Choc 15.00 flange exactly, so the switch's
// top lip lands flush on the bezel walls - no wasted width or depth.
// Bezel wall thickness is DERIVED: (15.00 - 13.80 - clearance)/2 ~ 0.45mm.
// ---------------------------------------------------------------------------
body_x = choc_flange_xy;       // mm - outer width  = flange size (15.00)
body_y = choc_flange_xy;       // mm - outer depth  = flange size (15.00)

wall_t = (choc_flange_xy - choc_body_xy - pocket_clearance) / 2;  // ~0.45mm
wall_h           = choc_body_h;// mm - pocket depth: full Choc bottom-housing
                               //      height (2.20), so the flange rests on
                               //      the top of the bezel walls

// Floor thickness = MINIMUM possible: just deeper than the Choc's 2.65mm
// posts/pins so they don't touch the PCB and lift the adapter. Post holes
// go all the way THROUGH (no membrane) - the PCB surface below the post
// positions is solid, so nothing conflicts. Total added height vs a normal
// Choc install = floor_h = 2.80mm.
floor_h = choc_center_post_len + 0.15;   // 2.80mm

body_h = floor_h + wall_h;                             // total block height

corner_radius    = 0.5;        // mm - rounded body corners (0 = square)

// ---------------------------------------------------------------------------
// PLATE-CLIP WINDOWS
// The Choc's retention clips (north + south faces) are designed to snap
// under a 1.2mm plate. Cutting windows through the bezel walls, starting
// plate_t below the wall top, makes the top 1.2mm of wall act exactly like
// a standard Choc plate - the clips snap into the windows and retain the
// switch on the adapter.
// ---------------------------------------------------------------------------
plate_t          = 1.20;       // mm - effective "plate" thickness above window
clip_window_w    = 6.0;        // mm - window width (Choc clips ~5mm, + margin)

// ---------------------------------------------------------------------------
// PIN ROUTING - CAPTIVE WIRE CHANNELS (v3.1)
// Each channel is a polyline trench connecting a Choc pin entry to its
// PG1425 pin-hole position. Unlike v3's full through-slots, the channel
// keeps a thin MEMBRANE of floor material underneath, so a wire laid in
// the channel cannot fall out the bottom. The channel is open at the TOP
// (into the Choc pocket): the wire drops in from above during assembly,
// and once the switch is seated its housing caps the channel - the wire
// is fully captive.
//
// Through-openings remain at exactly two places per channel:
//   * PIN ENTRY  - round through-pocket at the Choc pin position, full
//                  floor depth, so the 2.65mm pin descends fully and the
//                  pin<->wire solder joint is reachable from below
//   * WIRE EXIT  - round through-hole directly above the PG1425 plated
//                  hole, so the wire's end bends down through it into
//                  the PCB hole
//
// Set wire_channel = false to restore the v3 full through-slots.
// ---------------------------------------------------------------------------
slot_w              = 1.4;     // mm - routing channel width
wire_channel        = true;    // true = captive channel; false = v3 through-slot
channel_membrane_t  = 0.50;    // mm - floor membrane left under the channel
wire_exit_hole_d    = 1.40;    // mm - wire exit through-hole (over PG1425 hole)
pin_entry_pocket_d  = 1.60;    // mm - Choc pin entry through-pocket (pin 1.2
                               //      + room for the wire lying beside it)

// Slot polylines: first point = Choc pin entry, last = PG1425 pin hole.
// Slot 2 detours below center to clear the Choc center-post pocket and
// the side-post pocket at (5.5, 0).
slots = [
    [ choc_pin1_pos, pg1425_pin1_pos ],                    // (0,5.9) -> (-3.4, 2.9)
    [ choc_pin2_pos, [2.4, -3.0], pg1425_pin2_pos ],       // (5,3.8) -> (-3.4,-2.0)
];

// ============================================================================
// MODULES
// ============================================================================

// Rounded-corner rectangular block, centered on XY origin, base at z = 0
module rounded_block(x, y, h, r) {
    if (r > 0) {
        linear_extrude(height = h)
            offset(r = r) offset(delta = -r)
                square([x, y], center = true);
    } else {
        translate([0, 0, h/2]) cube([x, y, h], center = true);
    }
}

// Main solid body (bezel walls + floor)
module body() {
    rounded_block(body_x, body_y, body_h, corner_radius);
}

// Top pocket that the Choc bottom housing drops into
module choc_pocket() {
    pocket_xy = choc_body_xy + pocket_clearance;
    translate([0, 0, floor_h])
        rounded_block(pocket_xy, pocket_xy, wall_h + eps, 0.3);
}

// Clip windows cut through the north and south bezel walls. Window spans
// from the pocket floor up to (wall top - plate_t), leaving a 1.2mm
// "plate lip" for the Choc clips to snap under.
module clip_windows() {
    window_h = wall_h - plate_t + eps;   // from floor_h up
    for (sy = [-1, 1])
        translate([0, sy * (body_y/2 - wall_t/2), floor_h + window_h/2 - eps/2])
            cube([clip_window_w, wall_t + 2*eps, window_h], center = true);
}

// Through-hole cut through the full floor (for Choc posts)
module through_hole(pos, d) {
    translate([pos[0], pos[1], -eps])
        cylinder(h = floor_h + 2*eps, d = d + hole_clearance);
}

// PG1350 receiving holes, cut THROUGH the floor - TRUE Choc layout.
// Posts end 0.15mm above the PCB surface (floor is post length + 0.15).
module pg1350_holes() {
    // Center post (phi 3.2) at (0, 0)
    through_hole([0, 0], choc_center_post_d);

    // Two plastic locating posts (phi 1.9 at +/-5.5, 0)
    through_hole([-choc_side_post_x, 0], choc_side_post_d);
    through_hole([ choc_side_post_x, 0], choc_side_post_d);
}

// One routing channel: rounded polyline trench, built as chained hulls
// over consecutive points.
//   wire_channel = true : cut from channel_membrane_t up through the top
//                         (bottom membrane stays -> wire is captive)
//   wire_channel = false: v3 behaviour, cut through the full floor
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

// All pin routing channels
module pin_routing_slots() {
    for (s = slots) routing_slot(s);
}

// Through-openings at the channel ends (only used with wire_channel):
//   - pin entry pockets at the Choc pin positions (full floor depth)
//   - wire exit holes directly over the PG1425 plated holes
module channel_end_openings() {
    // Choc pin entry through-pockets
    for (p = [choc_pin1_pos, choc_pin2_pos])
        translate([p[0], p[1], -eps])
            cylinder(h = floor_h + 2*eps, d = pin_entry_pocket_d);

    // Wire exit through-holes over the PG1425 pin holes
    for (p = [pg1425_pin1_pos, pg1425_pin2_pos])
        translate([p[0], p[1], -eps])
            cylinder(h = floor_h + 2*eps, d = wire_exit_hole_d);
}

// Two printed alignment pins that drop into the PG1425 PCB's non-plated
// phi 1.30 holes. These are the ONLY bottom protrusions.
module pg1425_alignment_pins() {
    for (p = pg1425_align_positions)
        translate([p[0], p[1], -pg1425_align_pin_h])
            cylinder(h = pg1425_align_pin_h + eps,
                     d = pg1425_align_hole_d - post_clearance);
}

// ============================================================================
// ASSEMBLY
// ============================================================================
module adapter() {
    union() {
        difference() {
            body();
            choc_pocket();
            clip_windows();
            pg1350_holes();
            pin_routing_slots();
            if (wire_channel) channel_end_openings();
        }
        pg1425_alignment_pins();
    }
}

adapter();

// ============================================================================
// END OF FILE
// ============================================================================