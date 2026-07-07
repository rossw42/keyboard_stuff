// ============================================================================
// PG1350 to PG1425 Switch Adapter - Main Shell Design (FIXED)
// OpenSCAD model for 3D printing
// 
// DESIGN: Plate-mounted bezel with dual-ended stamped contacts (Option B)
// See CONSOLIDATED_SWITCH_SPECS.md and project_overview.md for design details
//
// AUTHOR: Fixed geometry to properly connect all parts
// ============================================================================

// ============================================================================
// TOP-LEVEL CONFIGURABLE PARAMETERS
// ============================================================================

// Material & Print Settings
$fn = 64;                           // Smoothness of curves (higher = smoother, slower render)
wall_thickness = 1.2;               // mm - Wall thickness for printed shell
base_thickness = 2.0;               // mm - Base plate thickness
top_cover_thickness = 2.5;          // mm - Top cover thickness
filament_width = 0.6;               // mm - Typical FDM filament width

// Assembly & Tolerance Settings
print_tolerance = 0.1;              // mm - Add to internal dimensions for printing
assembly_clearance = 0.2;           // mm - Clearance for moving parts/assembly
contact_material_thickness = 0.5;   // mm - Thickness of stamped contact material
mounting_clearance = 0.3;           // mm - Extra clearance for mounting holes

// ============================================================================
// PG1350 SWITCH DIMENSIONS (from Kaihua Electronics CP6135001D02-1)
// ============================================================================

// External dimensions (top shell)
choc_external_width = 15.0;         // mm - Top shell width/height
choc_external_height = 15.0;        // mm - Bottom shell width/height

// Internal opening (where switch stem enters)
choc_internal_opening = 13.8;       // mm - Critical dimension for PG1350 compatibility

// Stem diameter (critical for mechanical stability)
choc_stem_diameter = 3.2;           // mm - Must match PG1350 stem exactly

// Mounting heights
choc_top_mount_height = 5.0;        // mm - Top mounting height from PCB
choc_bottom_mount_height = 5.8;     // mm - Bottom mounting height from PCB

// PCB interface (PG1350 side)
choc_pcb_width = 5.90;              // mm - Overall PCB width
choc_pcb_length = 11.00;            // mm - Overall PCB length  
choc_pin_spacing_x = 3.80;          // mm - Pin center-to-center (X)
choc_pin_spacing_y = 5.00;          // mm - Pin center-to-center (Y)

// PCB mounting holes
choc_top_hole_diameter = 1.90;      // mm - Top mounting holes (2 holes)
choc_bottom_hole_diameter = 1.20;   // mm - Bottom mounting holes (2 holes)

// Side profile features
choc_side_height = 14.50;           // mm - Total side height
choc_top_flange_width = 2.65;       // mm - Top flange width
choc_bottom_flange_width = 3.00;    // mm - Bottom flange width

// ============================================================================
// PG1425 SWITCH DIMENSIONS (from Kaihua Electronics CP6142501D02)
// ============================================================================

// External dimensions
pg1425_external_width = 14.0;       // mm - Top shell width/height
pg1425_external_height = 14.0;      // mm - Bottom shell width/height

// Internal opening (where switch stem enters)
pg1425_internal_opening = 10.2;     // mm - Critical dimension for PG1425 compatibility

// Stem diameter (critical for mechanical stability)
pg1425_stem_diameter = 0.9;         // mm - Must match PG1425 stem exactly

// Mounting heights
pg1425_top_mount_height = 5.0;      // mm - Top mounting height from PCB
pg1425_bottom_mount_height = 5.0;   // mm - Bottom mounting height from PCB

// PCB interface (PG1425 side)
pg1425_pcb_width = 5.50;            // mm - Overall PCB width
pg1425_pcb_length = 5.50;           // mm - Overall PCB length
pg1425_pin_spacing = 2.90;          // mm - Pin center-to-center

// PCB mounting holes
pg1425_top_hole_diameter = 1.30;    // mm - Top mounting holes (2 holes)
pg1425_bottom_hole_diameter = 1.10; // mm - Bottom mounting holes (2 holes)

// Land pattern (copper clad side)
pg1425_top_land_width = 5.10;       // mm - Top land width
pg1425_bottom_land_width = 5.50;    // mm - Bottom land width

// LED position (full color variant)
pg1425_led_x_offset = 4.10;         // mm from left pin center
pg1425_led_y_offset = 1.15;         // mm from bottom pin center

// ============================================================================
// ADAPTER GEOMETRY CALCULATIONS
// ============================================================================

// Size difference between PG1350 and PG1425 external dimensions
size_diff_width = choc_external_width - pg1425_external_width;  // 1.0mm
size_diff_height = choc_external_height - pg1425_external_height; // 1.0mm

// Gap to bridge (PG1350 internal opening minus PG1425 PCB footprint)
gap_to_bridge_x = choc_internal_opening - pg1425_pcb_width;    // 8.3mm total
gap_to_bridge_y = choc_internal_opening - pg1425_pcb_length;   // 8.3mm total

// Per-side gap for bridge design (centered)
bridge_half_x = gap_to_bridge_x / 2;     // ~4.15mm per side
bridge_half_y = gap_to_bridge_y / 2;     // ~4.15mm per side

// PCB interface gap
pcb_gap_width = choc_pcb_width - pg1425_pcb_width;    // 0.40mm total (0.20mm per side)

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

// Module to create a cylindrical hole with optional counterbore
module mounting_hole(x, y, diameter, depth, counterbore_diameter = null, 
                      counterbore_depth = null) {
    // Main through-hole
    cylinder(h = depth + 0.2, r = diameter/2, center = [x, y], $fn = 32);
    
    // Optional counterbore
    if (counterbore_diameter != null) {
        translate([x, y, -counterbore_depth]) 
            cylinder(h = depth + counterbore_depth + 0.2, r = counterbore_diameter/2, center = [x, y], $fn = 32);
    }
}

// Module to create a cylindrical protrusion/post
module post(x, y, diameter, height) {
    cylinder(h = height, r = diameter/2, center = [x, y], $fn = 32);
}

// ============================================================================
// MAIN RENDER BLOCK - Constructive Solid Geometry Approach (FIXED)
// ============================================================================

difference() {
    // Start with a solid outer bounding box (the complete adapter shell)
    translate([wall_thickness/2 - print_tolerance/2, wall_thickness/2 - print_tolerance/2, 
                -(base_thickness + top_cover_thickness)/2])
        cube([choc_external_width + pg1425_pcb_width + 2*wall_thickness - (print_tolerance-assembly_clearance)*2, 
               choc_external_height + pg1425_pcb_length + 2*wall_thickness - (print_tolerance-assembly_clearance)*2, 
               base_thickness + top_cover_thickness], center = [0, 0, 0]);
    
    // Carve out PG1350 side cavity with proper wall thickness
    translate([wall_thickness/2 + assembly_clearance, wall_thickness/2 + assembly_clearance, -base_thickness/2])
        cube([choc_internal_opening + assembly_clearance*2, 
               choc_internal_opening + assembly_clearance*2, base_thickness], center = [choc_external_width/2, choc_external_height/2, 0]);
    
    // Carve out PG1425 side cavity with proper wall thickness - FIXED POSITIONING
    translate([wall_thickness/2 + assembly_clearance, wall_thickness/2 + assembly_clearance, -base_thickness/2])
        cube([pg1425_internal_opening + assembly_clearance*2, 
               pg1425_internal_opening + assembly_clearance*2, base_thickness], center = [choc_external_width/2 + bridge_half_x, choc_external_height/2 + bridge_half_y, 0]);
    
    // Carve out PG1350 PCB mounting holes (top) - subtract from solid
    translate([-choc_pcb_width/2 - choc_top_hole_diameter/2 - mounting_clearance + wall_thickness/2, 
                -choc_pin_spacing_y/2 - choc_top_hole_diameter/2 - mounting_clearance + wall_thickness/2, base_thickness])
        cylinder(h = base_thickness + 0.2, r = (choc_top_hole_diameter + mounting_clearance)/2);
    
    translate([choc_pcb_width/2 + choc_top_hole_diameter/2 + mounting_clearance - wall_thickness/2, 
                -choc_pin_spacing_y/2 - choc_top_hole_diameter/2 - mounting_clearance + wall_thickness/2, base_thickness])
        cylinder(h = base_thickness + 0.2, r = (choc_top_hole_diameter + mounting_clearance)/2);
    
    // Carve out PG1350 PCB mounting holes (bottom)  
    translate([-choc_pcb_width/2 - choc_bottom_hole_diameter/2 - mounting_clearance + wall_thickness/2, 
                choc_pin_spacing_y/2 + choc_bottom_hole_diameter/2 - mounting_clearance + wall_thickness/2, base_thickness])
        cylinder(h = base_thickness + 0.2, r = (choc_bottom_hole_diameter + mounting_clearance)/2);
    
    translate([choc_pcb_width/2 + choc_bottom_hole_diameter/2 + mounting_clearance - wall_thickness/2, 
                choc_pin_spacing_y/2 + choc_bottom_hole_diameter/2 - mounting_clearance + wall_thickness/2, base_thickness])
        cylinder(h = base_thickness + 0.2, r = (choc_bottom_hole_diameter + mounting_clearance)/2);
    
    // Carve out PG1425 PCB mounting holes (top)
    translate([-pg1425_pcb_width/2 - pg1425_top_hole_diameter/2 - mounting_clearance + wall_thickness/2, 
                -pg1425_pin_spacing/2 - pg1425_top_hole_diameter/2 - mounting_clearance + wall_thickness/2, base_thickness])
        cylinder(h = base_thickness + 0.2, r = (pg1425_top_hole_diameter + mounting_clearance)/2);
    
    translate([pg1425_pcb_width/2 + pg1425_top_hole_diameter/2 + mounting_clearance - wall_thickness/2, 
                -pg1425_pin_spacing/2 - pg1425_top_hole_diameter/2 - mounting_clearance + wall_thickness/2, base_thickness])
        cylinder(h = base_thickness + 0.2, r = (pg1425_top_hole_diameter + mounting_clearance)/2);
    
    // Carve out PG1425 PCB mounting holes (bottom)  
    translate([-pg1425_pcb_width/2 - pg1425_bottom_hole_diameter/2 - mounting_clearance + wall_thickness/2, 
                pg1425_pin_spacing/2 + pg1425_bottom_hole_diameter/2 - mounting_clearance + wall_thickness/2, base_thickness])
        cylinder(h = base_thickness + 0.2, r = (pg1425_bottom_hole_diameter + mounting_clearance)/2);
    
    translate([pg1425_pcb_width/2 + pg1425_bottom_hole_diameter/2 + mounting_clearance - wall_thickness/2, 
                pg1425_pin_spacing/2 + pg1425_bottom_hole_diameter/2 - mounting_clearance + wall_thickness/2, base_thickness])
        cylinder(h = base_thickness + 0.2, r = (pg1425_bottom_hole_diameter + mounting_clearance)/2);
    
    // ADD BRIDGE WALLS BETWEEN PG1350 AND PG1425 SIDES - THIS CONNECTS THE GEOMETRY
    union() {
        // Left bridge wall (connecting the two cavities)
        translate([choc_external_width/2 - bridge_half_x - wall_thickness/2, 
                    choc_external_height/2 + assembly_clearance, 
                    -(base_thickness + top_cover_thickness)/2])
            cube([wall_thickness - assembly_clearance*2, 
                   pg1425_internal_opening + assembly_clearance*2, 
                   base_thickness + top_cover_thickness], center = [0, 0, 0]);
        
        // Right bridge wall (connecting the two cavities)
        translate([choc_external_width/2 + bridge_half_x + wall_thickness/2 - pg1425_internal_opening - assembly_clearance*2, 
                    choc_external_height/2 + assembly_clearance, 
                    -(base_thickness + top_cover_thickness)/2])
            cube([wall_thickness - assembly_clearance*2, 
                   pg1425_internal_opening + assembly_clearance*2, 
                   base_thickness + top_cover_thickness], center = [0, 0, 0]);
        
        // Front bridge wall (connecting the two cavities)
        translate([choc_external_width/2 + assembly_clearance, 
                    choc_external_height/2 - bridge_half_y - wall_thickness/2, 
                    -(base_thickness + top_cover_thickness)/2])
            cube([pg1425_internal_opening + assembly_clearance*2, 
                   wall_thickness - assembly_clearance*2, 
                   base_thickness + top_cover_thickness], center = [0, 0, 0]);
        
        // Rear bridge wall (connecting the two cavities)
        translate([choc_external_width/2 + assembly_clearance, 
                    choc_external_height/2 + bridge_half_y + wall_thickness/2 - pg1425_internal_opening - assembly_clearance*2, 
                    -(base_thickness + top_cover_thickness)/2])
            cube([pg1425_internal_opening + assembly_clearance*2, 
                   wall_thickness - assembly_clearance*2, 
                   base_thickness + top_cover_thickness], center = [0, 0, 0]);
    }
}

// ============================================================================
// END OF FILE
// ============================================================================