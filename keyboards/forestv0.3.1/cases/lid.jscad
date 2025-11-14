function _plate_inner_2_extrude_1_6_outline_fn(){
    return new CSG.Path2D([[92.575,-81.875],[108.625,-81.875]]).appendPoint([108.625,-81.9]).appendPoint([117.3152909,-81.9]).appendArc([117.9339035,-81.9644731],{"radius":3,"clockwise":true,"large":false}).appendPoint([204.239667,-100.15195]).appendPoint([210.2446648,-102.8004697]).appendPoint([209.9956722,-103.1469795]).appendPoint([226.6839886,-115.1387514]).appendArc([230.8708629,-114.4531244],{"radius":3,"clockwise":false,"large":false}).appendPoint([241.1120112,-100.2010585]).appendArc([240.4263842,-96.0141843],{"radius":3,"clockwise":false,"large":false}).appendPoint([233.4375,-90.9921615]).appendPoint([233.4375,2.91]).appendArc([230.4375,5.91],{"radius":3,"clockwise":false,"large":false}).appendPoint([186.625,5.91]).appendPoint([186.625,5.911]).appendPoint([170.575,5.911]).appendArc([167.575,8.911],{"radius":3,"clockwise":true,"large":false}).appendPoint([167.575,9.1634]).appendArc([164.575,12.1634],{"radius":3,"clockwise":false,"large":false}).appendPoint([149.725,12.1634]).appendArc([146.725,9.1634],{"radius":3,"clockwise":false,"large":false}).appendPoint([146.725,7.161]).appendArc([143.725,4.161],{"radius":3,"clockwise":true,"large":false}).appendPoint([130.675,4.161]).appendArc([127.675,1.161],{"radius":3,"clockwise":false,"large":false}).appendPoint([127.675,-1.05]).appendArc([124.675,-4.05],{"radius":3,"clockwise":true,"large":false}).appendPoint([111.625,-4.05]).appendArc([108.625,-7.05],{"radius":3,"clockwise":false,"large":false}).appendPoint([108.625,-10.575]).appendArc([105.625,-13.575],{"radius":3,"clockwise":true,"large":false}).appendPoint([92.575,-13.575]).appendArc([89.575,-16.575],{"radius":3,"clockwise":false,"large":false}).appendPoint([89.575,-78.875]).appendArc([92.575,-81.875],{"radius":3,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 1.6] });
}


function _lid_bosses_extrude_1_6_outline_fn(){
    return CAG.circle({"center":[204.775,-71.04],"radius":3.5})
.union(
    CAG.circle({"center":[204.775,-52.04],"radius":3.5})
).union(
    CAG.circle({"center":[147.625,-77.24],"radius":3.5})
).union(
    CAG.circle({"center":[183.725,-36.09],"radius":3.5})
).union(
    CAG.circle({"center":[164.675,-30.14],"radius":3.5})
).union(
    CAG.circle({"center":[111.525,-62],"radius":3.5})
).union(
    CAG.circle({"center":[202.775,-13.99],"radius":3.5})
).union(
    CAG.circle({"center":[144.625,-20.19],"radius":3.5})
).union(
    CAG.circle({"center":[107.525,-33.525],"radius":3.5})
).extrude({ offset: [0, 0, 1.6] });
}


function _screw_holes_extrude_1_8_outline_fn(){
    return CAG.circle({"center":[204.775,-71.04],"radius":0.8})
.union(
    CAG.circle({"center":[204.775,-52.04],"radius":0.8})
).union(
    CAG.circle({"center":[147.625,-77.24],"radius":0.8})
).union(
    CAG.circle({"center":[183.725,-36.09],"radius":0.8})
).union(
    CAG.circle({"center":[164.675,-30.14],"radius":0.8})
).union(
    CAG.circle({"center":[111.525,-62],"radius":0.8})
).union(
    CAG.circle({"center":[202.775,-13.99],"radius":0.8})
).union(
    CAG.circle({"center":[144.625,-20.19],"radius":0.8})
).union(
    CAG.circle({"center":[107.525,-33.525],"radius":0.8})
).extrude({ offset: [0, 0, 1.8] });
}


function _lid_screw_heads_extrude_1_8_outline_fn(){
    return CAG.circle({"center":[204.775,-71.04],"radius":2.4})
.union(
    CAG.circle({"center":[204.775,-52.04],"radius":2.4})
).union(
    CAG.circle({"center":[147.625,-77.24],"radius":2.4})
).union(
    CAG.circle({"center":[183.725,-36.09],"radius":2.4})
).union(
    CAG.circle({"center":[164.675,-30.14],"radius":2.4})
).union(
    CAG.circle({"center":[111.525,-62],"radius":2.4})
).union(
    CAG.circle({"center":[202.775,-13.99],"radius":2.4})
).union(
    CAG.circle({"center":[144.625,-20.19],"radius":2.4})
).union(
    CAG.circle({"center":[107.525,-33.525],"radius":2.4})
).extrude({ offset: [0, 0, 1.8] });
}




                function lid_case_fn() {
                    

                // creating part 0 of case lid
                let lid__part_0 = _plate_inner_2_extrude_1_6_outline_fn();

                // make sure that rotations are relative
                let lid__part_0_bounds = lid__part_0.getBounds();
                let lid__part_0_x = lid__part_0_bounds[0].x + (lid__part_0_bounds[1].x - lid__part_0_bounds[0].x) / 2
                let lid__part_0_y = lid__part_0_bounds[0].y + (lid__part_0_bounds[1].y - lid__part_0_bounds[0].y) / 2
                lid__part_0 = translate([-lid__part_0_x, -lid__part_0_y, 0], lid__part_0);
                lid__part_0 = rotate([0,0,0], lid__part_0);
                lid__part_0 = translate([lid__part_0_x, lid__part_0_y, 0], lid__part_0);

                lid__part_0 = translate([0,0,0], lid__part_0);
                let result = lid__part_0;
                
            

                // creating part 1 of case lid
                let lid__part_1 = _lid_bosses_extrude_1_6_outline_fn();

                // make sure that rotations are relative
                let lid__part_1_bounds = lid__part_1.getBounds();
                let lid__part_1_x = lid__part_1_bounds[0].x + (lid__part_1_bounds[1].x - lid__part_1_bounds[0].x) / 2
                let lid__part_1_y = lid__part_1_bounds[0].y + (lid__part_1_bounds[1].y - lid__part_1_bounds[0].y) / 2
                lid__part_1 = translate([-lid__part_1_x, -lid__part_1_y, 0], lid__part_1);
                lid__part_1 = rotate([0,0,0], lid__part_1);
                lid__part_1 = translate([lid__part_1_x, lid__part_1_y, 0], lid__part_1);

                lid__part_1 = translate([0,0,1.6], lid__part_1);
                result = result.union(lid__part_1);
                
            

                // creating part 2 of case lid
                let lid__part_2 = _screw_holes_extrude_1_8_outline_fn();

                // make sure that rotations are relative
                let lid__part_2_bounds = lid__part_2.getBounds();
                let lid__part_2_x = lid__part_2_bounds[0].x + (lid__part_2_bounds[1].x - lid__part_2_bounds[0].x) / 2
                let lid__part_2_y = lid__part_2_bounds[0].y + (lid__part_2_bounds[1].y - lid__part_2_bounds[0].y) / 2
                lid__part_2 = translate([-lid__part_2_x, -lid__part_2_y, 0], lid__part_2);
                lid__part_2 = rotate([0,0,0], lid__part_2);
                lid__part_2 = translate([lid__part_2_x, lid__part_2_y, 0], lid__part_2);

                lid__part_2 = translate([0,0,1.5], lid__part_2);
                result = result.subtract(lid__part_2);
                
            

                // creating part 3 of case lid
                let lid__part_3 = _lid_screw_heads_extrude_1_8_outline_fn();

                // make sure that rotations are relative
                let lid__part_3_bounds = lid__part_3.getBounds();
                let lid__part_3_x = lid__part_3_bounds[0].x + (lid__part_3_bounds[1].x - lid__part_3_bounds[0].x) / 2
                let lid__part_3_y = lid__part_3_bounds[0].y + (lid__part_3_bounds[1].y - lid__part_3_bounds[0].y) / 2
                lid__part_3 = translate([-lid__part_3_x, -lid__part_3_y, 0], lid__part_3);
                lid__part_3 = rotate([0,0,0], lid__part_3);
                lid__part_3 = translate([lid__part_3_x, lid__part_3_y, 0], lid__part_3);

                lid__part_3 = translate([0,0,-0.1], lid__part_3);
                result = result.subtract(lid__part_3);
                
            
                    return result;
                }
            
            
        
            function main() {
                return lid_case_fn();
            }

        