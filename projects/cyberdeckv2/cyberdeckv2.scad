// =============================================================================
// cyberdeckv2.scad — Cyberdeck v2: stock Micro Journal Rev 8 case, lid
// modified to fit the 7.84" Wisecoco 400x1280 bar panel.
//
// Approach: use unkyulee's Rev 8 STLs as-is (base, enclosures, hood, wire
// cap) and apply boolean modifications ONLY to the three Display Panel
// pieces (the lid's front frame):
//   1. fill the stock ~5" display aperture (middle piece),
//   2. cut a new wide aperture for the 7.84" active area,
//   3. cut a pocket on the back side for the panel outline (flush mount).
// The same global cutters are applied to Left/Middle/Right, so the printed
// pieces keep their original zig-zag joints and screw geometry elsewhere.
//
// Rev 8 assembly coordinates (from the STLs): x centered, y toward hinge
// (hinge/wire-cap zone at y 42..74), display frame z 23(face)..27, display
// enclosure (back shell) z 23..35.
//
// part = "panel_left" | "panel_middle" | "panel_right"   (modified pieces)
//      | "lid_assembly"       (modified frame + enclosure + wire cap + ghost panel)
//      | "lid_frame_only"     (three modified panel pieces + ghost panel)
//      | "aperture_check"     (2D-ish sanity: cutters + stock frame)
// =============================================================================

part = "lid_assembly";
show_ghost = true;         // show 7.84" panel mockup in assemblies

$fn = 32;
EPS = 0.01;

STL = "stl/";

// ---------------------------------------------------------------------------
// 7.84" Wisecoco panel (VERIFY on the bench before final print)
// ---------------------------------------------------------------------------
pan_w = 213.6;             // panel outline width
pan_h = 71.9;              // panel outline height
pan_t = 2.9;               // panel thickness
act_w = 205.4;             // active area width
act_h = 64.2;              // active area height

ap_clear  = 1.0;           // aperture margin around active area (per side... total below)
pk_clear  = 0.3;           // pocket clearance around panel outline (per side)

// ---------------------------------------------------------------------------
// Placement in Rev 8 lid coordinates
// ---------------------------------------------------------------------------
// Frame face region: x -161.2..161.2, y -56.7..42.0 (98.7 tall).
// Stock screw holes to preserve sit near y = -43.5 and y = +31.2.
// Center the panel at y = -6 so the pocket clears both rows (~1 mm).
disp_cx = 0;
disp_cy = -6;

// Frame z: face at z=23, back at z=27 (4 mm thick).
frame_z0 = 23; frame_z1 = 27;
face_t   = 1.0;            // material left in front of the panel (bezel lip)

// Derived cutter boxes
ap_w = act_w + 2*ap_clear;         // 207.4
ap_h = act_h + 2*ap_clear;         // 66.2
pk_w = pan_w + 2*pk_clear;         // 214.2
pk_h = pan_h + 2*pk_clear;         // 72.5

// Stock aperture region to fill (probed from the STL, +0.6 overlap)
fill_x0 = -49.2; fill_x1 = 56.6;
fill_y0 = -46.5; fill_y1 = 31.9;

echo(str("CHECK [", (ap_w <= 300 && pk_w <= 315) ? "PASS" : "FAIL",
     "] aperture/pocket fit frame width  ", ap_w, " / ", pk_w, " <= 322"));
echo(str("CHECK [", (disp_cy - pk_h/2 >= -50 && disp_cy + pk_h/2 <= 36)
     ? "PASS" : "FAIL", "] pocket inside frame field  y[",
     disp_cy - pk_h/2, ",", disp_cy + pk_h/2, "] within [-50,36]"));
echo(str("CHECK [", (disp_cy - pk_h/2 > -43.5 + 0.8) ? "PASS" : "FAIL",
     "] pocket clears bottom screw row  ", disp_cy - pk_h/2, " > -42.7"));
echo(str("CHECK [", (disp_cy + pk_h/2 < 31.2 - 0.8) ? "PASS" : "FAIL",
     "] pocket clears top screw row  ", disp_cy + pk_h/2, " < 30.4"));

// ---------------------------------------------------------------------------
// Cutters / fillers
// ---------------------------------------------------------------------------
module new_aperture() {   // through-cut for the visible active area
    translate([disp_cx - ap_w/2, disp_cy - ap_h/2, frame_z0 - 1])
        cube([ap_w, ap_h, (frame_z1 - frame_z0) + 2]);
}

module panel_pocket() {   // back-side recess the panel drops into
    translate([disp_cx - pk_w/2, disp_cy - pk_h/2, frame_z0 + face_t])
        cube([pk_w, pk_h, (frame_z1 - frame_z0) - face_t + 1]);
}

module old_aperture_fill() {   // solid slab over the stock 5" opening
    translate([fill_x0, fill_y0, frame_z0])
        cube([fill_x1 - fill_x0, fill_y1 - fill_y0, frame_z1 - frame_z0]);
}

// ---------------------------------------------------------------------------
// Modified Display Panel pieces
// ---------------------------------------------------------------------------
module panel_middle_mod() {
    difference() {
        union() {
            import(str(STL, "Display Panel Middle.stl"));
            old_aperture_fill();
        }
        new_aperture();
        panel_pocket();
    }
}

module panel_left_mod() {
    difference() {
        import(str(STL, "Display Panel Left.stl"));
        new_aperture();
        panel_pocket();
    }
}

module panel_right_mod() {
    difference() {
        import(str(STL, "Display Panel Right.stl"));
        new_aperture();
        panel_pocket();
    }
}

// ---------------------------------------------------------------------------
// Ghost mockup of the 7.84" panel seated in the pocket
// ---------------------------------------------------------------------------
module ghost_panel() {
    color("Black", 0.85)
        translate([disp_cx - pan_w/2, disp_cy - pan_h/2, frame_z0 + face_t])
            cube([pan_w, pan_h, pan_t]);
}

// ---------------------------------------------------------------------------
// Assemblies (stock Rev 8 parts imported unmodified)
// ---------------------------------------------------------------------------
module lid_frame_only() {
    panel_left_mod();
    panel_middle_mod();
    panel_right_mod();
    if (show_ghost) ghost_panel();
}

module lid_assembly() {
    lid_frame_only();
    color("Khaki") {
        import(str(STL, "Display Enclosure Left.stl"));
        import(str(STL, "Display Enclosure Middle.stl"));
        import(str(STL, "Display Enclosure Right.stl"));
        import(str(STL, "Display Wire Cap.stl"));
    }
}

// Whole device, closed, as the parts sit in the shared Rev 8 assembly
// coordinate system. `open_angle` swings the lid about the hinge axis
// (measured from the Display Enclosure roll: y ~ 66, z ~ 29).
open_angle = 0;
hinge_axis = [0, 66, 29];

module lid_at(a) {
    translate(hinge_axis) rotate([a, 0, 0]) translate(-hinge_axis) children();
}

module full_assembly() {
    // base
    color("Gold") {
        import(str(STL, "Enclosure Left.stl"));
        import(str(STL, "Enclosure Middle.stl"));
        import(str(STL, "Enclosure Right.stl"));
        import(str(STL, "Enclosure Lid.stl"));
    }
    color("Goldenrod") {
        import(str(STL, "Hood Bottom.stl"));
        import(str(STL, "Hood Left.stl"));
        import(str(STL, "Hood Right.stl"));
        import(str(STL, "Hood Top.stl"));
    }
    color("DimGray") {
        import(str(STL, "keyboard plate space.stl"));
        import(str(STL, "keyboard plate arrow.stl"));
    }
    // lid (rotatable)
    lid_at(open_angle) {
        color("Khaki") {
            import(str(STL, "Display Enclosure Left.stl"));
            import(str(STL, "Display Enclosure Middle.stl"));
            import(str(STL, "Display Enclosure Right.stl"));
        }
        panel_left_mod();
        panel_middle_mod();
        panel_right_mod();
        if (show_ghost) ghost_panel();
    }
    color("Khaki") import(str(STL, "Display Wire Cap.stl"));
}

// ---------------------------------------------------------------------------
// Part selection
// ---------------------------------------------------------------------------
if (part == "panel_left")        panel_left_mod();
else if (part == "panel_middle") panel_middle_mod();
else if (part == "panel_right")  panel_right_mod();
else if (part == "lid_frame_only") lid_frame_only();
else if (part == "lid_assembly") lid_assembly();
else if (part == "full_assembly") full_assembly();
else if (part == "aperture_check") {
    %import(str(STL, "Display Panel Middle.stl"));
    %import(str(STL, "Display Panel Left.stl"));
    %import(str(STL, "Display Panel Right.stl"));
    color("Red", 0.5) new_aperture();
    color("Blue", 0.3) panel_pocket();
}
else echo(str("unknown part: ", part));