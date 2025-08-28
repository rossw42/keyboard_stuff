// Lily58 Wooden Keyboard Case - Left Half
// Tray Mount Design for CNC/3D Printing
// Generate STL: Open in OpenSCAD and press F6, then Export as STL

// === PARAMETERS ===
// Adjust these values for your specific needs
case_length = 155;        // External length (mm)
case_width = 120;         // External width (mm) 
case_height = 18;         // Total case height (mm)
wall_thickness = 5;       // Wall thickness (mm)
bottom_thickness = 8;     // Bottom thickness (mm)
cavity_depth = 12;        // Internal cavity depth (mm)

// Mounting hole parameters
standoff_hole_dia = 3.2;  // M3 clearance holes
countersink_dia = 6;      // Countersink diameter for screw heads
countersink_depth = 3;    // Countersink depth

// Cutout dimensions
trrs_hole_dia = 7;        // TRRS jack hole
promicro_width = 20;      // Pro Micro cutout width
promicro_height = 35;     // Pro Micro cutout height
usb_width = 9;            // USB-C cutout width
usb_height = 3.5;         // USB-C cutout height

// === MOUNTING HOLE POSITIONS ===
// Adjust these coordinates to match your PCB's mounting holes
mounting_holes = [
    [30, 25],     // Hole 1
    [75, 20],     // Hole 2
    [120, 25],    // Hole 3
    [40, 70],     // Hole 4
    [100, 80],    // Hole 5
    [135, 70]     // Hole 6
];

// === MAIN CASE MODULE ===
module lily58_case() {
    difference() {
        // Main case body (rounded rectangle)
        hull() {
            translate([5, 5, 0]) 
                cylinder(r=5, h=case_height, $fn=20);
            translate([case_length-5, 5, 0]) 
                cylinder(r=5, h=case_height, $fn=20);
            translate([5, case_width-5, 0]) 
                cylinder(r=5, h=case_height, $fn=20);
            translate([case_length-5, case_width-5, 0]) 
                cylinder(r=5, h=case_height, $fn=20);
        }
        
        // Internal cavity
        translate([wall_thickness, wall_thickness, bottom_thickness])
            cube([
                case_length - (2 * wall_thickness), 
                case_width - (2 * wall_thickness), 
                cavity_depth + 1
            ]);
        
        // Mounting holes with countersinks
        for (hole = mounting_holes) {
            translate([hole[0], hole[1], 0]) {
                // Through hole
                cylinder(d=standoff_hole_dia, h=case_height+2, $fn=16);
                // Countersink from bottom
                translate([0, 0, -1])
                    cylinder(d=countersink_dia, h=countersink_depth+1, $fn=16);
            }
        }
        
        // TRRS jack cutout (side edge)
        translate([-1, 30, case_height/2])
            rotate([0, 90, 0])
                cylinder(d=trrs_hole_dia, h=wall_thickness+2, $fn=16);
        
        // Pro Micro access cutout
        translate([case_length - 40, case_width - 45, -1])
            cube([promicro_width, promicro_height, bottom_thickness+2]);
        
        // USB-C cutout (back edge)
        translate([case_length - 30, case_width+1, case_height/2])
            rotate([90, 0, 0])
                hull() {
                    cylinder(d=usb_height, h=wall_thickness+2, $fn=16);
                    translate([usb_width-usb_height, 0, 0])
                        cylinder(d=usb_height, h=wall_thickness+2, $fn=16);
                }
    }
}

// === GENERATE THE CASE ===
lily58_case();

// === OPTIONAL: Show PCB outline for reference ===
// Uncomment the next line to see PCB position
// translate([wall_thickness, wall_thickness, bottom_thickness + 2]) 
//     cube([case_length - (2 * wall_thickness), case_width - (2 * wall_thickness), 1.6]);

// === NOTES FOR CUSTOMIZATION ===
/*
TO CUSTOMIZE FOR YOUR SPECIFIC LILY58:
1. Measure your PCB mounting holes
2. Update the mounting_holes array with exact coordinates
3. Adjust cutout positions for your specific PCB layout
4. Test print a small section first to verify fit

TO GENERATE STL:
1. Install OpenSCAD (free from openscad.org)
2. Open this file in OpenSCAD
3. Press F6 to render
4. File → Export → Export as STL

FOR CNC MACHINING:
- Use case_height = 18 for solid wood block
- Machine from top down, leaving bottom thickness intact
- Consider adding registration features for flip operations

FOR 3D PRINTING:
- Print upside down (open cavity facing up)
- Add support for overhangs if needed
- Consider splitting into top/bottom halves for large printers
*/
