include <parameters.scad>
include <stabilizer_spacing.scad>

use <utils.scad>

/* [Layout Values] */
/* Layout Format (each key):
    [
        [                                       // Location Data
            [x_location, y_location],
            key_size,
            [rotation, rotation_x, rotation_y],
        ],
        [                                       // Borders
            top_border,
            bottom_border,
            left_border,
            right_border
        ],
        extra_data                              // Extra data (depending on component type)
        [                                       // Trim (optional booleans)
            top_border,
            bottom_border,
            left_border,
            right_border
        ],
    ]
*/

// Keyswitch Layout
//     (extra_data = rotate_column)
base_switch_layout = [
  [[[3,0],1,[0,0,0]],[1,1,1,1],false],
  [[[10.5,0],1,[0,0,0]],[1,1,1,1],false],
  [[[2,0.06000000000000005],1,[0,0,0]],[1,1,1,1],false],
  [[[4,0.06000000000000005],1,[0,0,0]],[1,1,1,1],false],
  [[[9.5,0.06000000000000005],1,[0,0,0]],[1,1,1,1],false],
  [[[11.5,0.06000000000000005],1,[0,0,0]],[1,1,1,1],false],
  [[[5,0.20000000000000007],1,[0,0,0]],[1,1,1,1],false],
  [[[8.5,0.20000000000000007],1,[0,0,0]],[1,1,1,1],false],
  [[[1,0.2500000000000002],1,[0,0,0]],[1,1,1,1],false],
  [[[12.5,0.2500000000000002],1,[0,0,0]],[1,1,1,1],false],
  [[[0,0.3100000000000003],1,[0,0,0]],[1,1,1,1],false],
  [[[13.5,0.3100000000000003],1,[0,0,0]],[1,1,1,1],false],
  [[[3,1.0000000000000002],1,[0,0,0]],[1,1,1,1],false],
  [[[10.5,1.0000000000000002],1,[0,0,0]],[1,1,1,1],false],
  [[[2,1.06],1,[0,0,0]],[1,1,1,1],false],
  [[[4,1.06],1,[0,0,0]],[1,1,1,1],false],
  [[[9.5,1.06],1,[0,0,0]],[1,1,1,1],false],
  [[[11.5,1.06],1,[0,0,0]],[1,1,1,1],false],
  [[[5,1.2000000000000002],1,[0,0,0]],[1,1,1,1],false],
  [[[8.5,1.2000000000000002],1,[0,0,0]],[1,1,1,1],false],
  [[[1,1.2500000000000002],1,[0,0,0]],[1,1,1,1],false],
  [[[12.5,1.2500000000000002],1,[0,0,0]],[1,1,1,1],false],
  [[[0,1.31],1,[0,0,0]],[1,1,1,1],false],
  [[[13.5,1.31],1,[0,0,0]],[1,1,1,1],false],
  [[[3,2],1,[0,0,0]],[1,1,1,1],false],
  [[[10.5,2],1,[0,0,0]],[1,1,1,1],false],
  [[[2,2.06],1,[0,0,0]],[1,1,1,1],false],
  [[[4,2.06],1,[0,0,0]],[1,1,1,1],false],
  [[[9.5,2.06],1,[0,0,0]],[1,1,1,1],false],
  [[[11.5,2.06],1,[0,0,0]],[1,1,1,1],false],
  [[[5,2.2],1,[0,0,0]],[1,1,1,1],false],
  [[[8.5,2.2],1,[0,0,0]],[1,1,1,1],false],
  [[[1,2.25],1,[0,0,0]],[1,1,1,1],false],
  [[[12.5,2.25],1,[0,0,0]],[1,1,1,1],false],
  [[[0,2.31],1,[0,0,0]],[1,1,1,1],false],
  [[[13.5,2.31],1,[0,0,0]],[1,1,1,1],false],
  [[[6,2.7],1,[0,0,0]],[1,1,1,1],false],
  [[[7.5,2.7],1,[0,0,0]],[1,1,1,1],false],
  [[[3,3],1,[0,0,0]],[1,1,1,1],false],
  [[[10.5,3],1,[0,0,0]],[1,1,1,1],false],
  [[[2,3.06],1,[0,0,0]],[1,1,1,1],false],
  [[[4,3.06],1,[0,0,0]],[1,1,1,1],false],
  [[[9.5,3.06],1,[0,0,0]],[1,1,1,1],false],
  [[[11.5,3.06],1,[0,0,0]],[1,1,1,1],false],
  [[[5,3.2000000000000006],1,[0,0,0]],[1,1,1,1],false],
  [[[8.5,3.2000000000000006],1,[0,0,0]],[1,1,1,1],false],
  [[[1,3.250000000000001],1,[0,0,0]],[1,1,1,1],false],
  [[[12.5,3.250000000000001],1,[0,0,0]],[1,1,1,1],false],
  [[[0,3.310000000000001],1,[0,0,0]],[1,1,1,1],false],
  [[[13.5,3.310000000000001],1,[0,0,0]],[1,1,1,1],false],
  [[[2.5,4.130000000000001],1,[0,0,0]],[1,1,1,1],false],
  [[[3.5,4.130000000000001],1,[0,0,0]],[1,1,1,1],false],
  [[[10,4.130000000000001],1,[0,0,0]],[1,1,1,1],false],
  [[[11,4.130000000000001],1,[0,0,0]],[1,1,1,1],false],
  [[[4.5,4.200000000000001],1,[0,0,0]],[1,1,1,1],false],
  [[[9,4.200000000000001],1,[0,0,0]],[1,1,1,1],false],
  [[[7.2,4.1499999999999995],1.75,[-58,8,4.8]],[1,1,1+0.375*unit*mm,1+0.375*unit*mm],false],
  [[[5.55,4.1499999999999995],1.75,[58,6.5,4.8]],[1,1,1+0.375*unit*mm,1+0.375*unit*mm],false],
];

// MCU Position(s)
base_mcu_layout = [];

// TRRS Position(s)
base_trrs_layout = [];

// Stabilizer layout
//     (extra_data = [key_size, left_offset, right_offset, switch_offset=0])
//     (see stabilizer_spacing.scad for presets)
base_stab_layout = [
];

// Via layout
//     (extra_data = [via_width, via_length])
base_via_layout = [];

// Plate Layout (if different than PCB)
//     (extra_data = component_type)
base_plate_layout = [];

// Standoff layout
//     (extra_data = [standoff_integration_override, standoff_attachment_override])
base_standoff_layout = [];

module additional_plate_cutouts() {
    square(0); // Dummy geometry to fix preview bug
} 

module additional_case_cavities() {
    square(0); // Dummy geometry to fix preview bug
}

// Whether to only use base_plate_layout to generate the plate footprint
use_plate_layout_only = false;

// Whether to flip the layout (useful for split boards)
invert_layout_flag = false;

// Whether the layout is staggered-row or staggered-column
layout_type = "column";  // [column, row]

// Tenting
// Angle around y-axis (i.e. typing angle)
tent_angle_y = 0;
// Angle around x-axis
tent_angle_x = 0;
// Point around which keyboard is tented
tent_point = [0, 0, 0];

