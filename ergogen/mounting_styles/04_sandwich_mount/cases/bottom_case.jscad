function case_outline_extrude_6_outline_fn(){
    return new CSG.Path2D([[-15,31.05],[-15,-12]]).appendArc([-12,-15],{"radius":3,"clockwise":false,"large":false}).appendPoint([31,-15]).appendArc([34,-12],{"radius":3,"clockwise":false,"large":false}).appendPoint([34,31.05]).appendArc([31,34.05],{"radius":3,"clockwise":false,"large":false}).appendPoint([-12,34.05]).appendArc([-15,31.05],{"radius":3,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 6] });
}


function screw_bosses_extrude_6_outline_fn(){
    return CAG.circle({"center":[-12,31.05],"radius":4})
.union(
    CAG.circle({"center":[31,31.05],"radius":4})
).union(
    CAG.circle({"center":[31,-12],"radius":4})
).union(
    CAG.circle({"center":[-12,-12],"radius":4})
).extrude({ offset: [0, 0, 6] });
}


function through_holes_extrude_7_6_outline_fn(){
    return CAG.circle({"center":[-12,31.05],"radius":1.1})
.union(
    CAG.circle({"center":[31,31.05],"radius":1.1})
).union(
    CAG.circle({"center":[31,-12],"radius":1.1})
).union(
    CAG.circle({"center":[-12,-12],"radius":1.1})
).extrude({ offset: [0, 0, 7.6] });
}


function countersink_holes_extrude_0_6_outline_fn(){
    return CAG.circle({"center":[-12,31.05],"radius":3})
.union(
    CAG.circle({"center":[31,31.05],"radius":3})
).union(
    CAG.circle({"center":[31,-12],"radius":3})
).union(
    CAG.circle({"center":[-12,-12],"radius":3})
).extrude({ offset: [0, 0, 0.6] });
}




                function bottom_case_case_fn() {
                    

                // creating part 0 of case bottom_case
                let bottom_case__part_0 = case_outline_extrude_6_outline_fn();

                // make sure that rotations are relative
                let bottom_case__part_0_bounds = bottom_case__part_0.getBounds();
                let bottom_case__part_0_x = bottom_case__part_0_bounds[0].x + (bottom_case__part_0_bounds[1].x - bottom_case__part_0_bounds[0].x) / 2
                let bottom_case__part_0_y = bottom_case__part_0_bounds[0].y + (bottom_case__part_0_bounds[1].y - bottom_case__part_0_bounds[0].y) / 2
                bottom_case__part_0 = translate([-bottom_case__part_0_x, -bottom_case__part_0_y, 0], bottom_case__part_0);
                bottom_case__part_0 = rotate([0,0,0], bottom_case__part_0);
                bottom_case__part_0 = translate([bottom_case__part_0_x, bottom_case__part_0_y, 0], bottom_case__part_0);

                bottom_case__part_0 = translate([0,0,0], bottom_case__part_0);
                let result = bottom_case__part_0;
                
            

                // creating part 1 of case bottom_case
                let bottom_case__part_1 = screw_bosses_extrude_6_outline_fn();

                // make sure that rotations are relative
                let bottom_case__part_1_bounds = bottom_case__part_1.getBounds();
                let bottom_case__part_1_x = bottom_case__part_1_bounds[0].x + (bottom_case__part_1_bounds[1].x - bottom_case__part_1_bounds[0].x) / 2
                let bottom_case__part_1_y = bottom_case__part_1_bounds[0].y + (bottom_case__part_1_bounds[1].y - bottom_case__part_1_bounds[0].y) / 2
                bottom_case__part_1 = translate([-bottom_case__part_1_x, -bottom_case__part_1_y, 0], bottom_case__part_1);
                bottom_case__part_1 = rotate([0,0,0], bottom_case__part_1);
                bottom_case__part_1 = translate([bottom_case__part_1_x, bottom_case__part_1_y, 0], bottom_case__part_1);

                bottom_case__part_1 = translate([0,0,0], bottom_case__part_1);
                result = result.union(bottom_case__part_1);
                
            

                // creating part 2 of case bottom_case
                let bottom_case__part_2 = through_holes_extrude_7_6_outline_fn();

                // make sure that rotations are relative
                let bottom_case__part_2_bounds = bottom_case__part_2.getBounds();
                let bottom_case__part_2_x = bottom_case__part_2_bounds[0].x + (bottom_case__part_2_bounds[1].x - bottom_case__part_2_bounds[0].x) / 2
                let bottom_case__part_2_y = bottom_case__part_2_bounds[0].y + (bottom_case__part_2_bounds[1].y - bottom_case__part_2_bounds[0].y) / 2
                bottom_case__part_2 = translate([-bottom_case__part_2_x, -bottom_case__part_2_y, 0], bottom_case__part_2);
                bottom_case__part_2 = rotate([0,0,0], bottom_case__part_2);
                bottom_case__part_2 = translate([bottom_case__part_2_x, bottom_case__part_2_y, 0], bottom_case__part_2);

                bottom_case__part_2 = translate([0,0,0], bottom_case__part_2);
                result = result.subtract(bottom_case__part_2);
                
            

                // creating part 3 of case bottom_case
                let bottom_case__part_3 = countersink_holes_extrude_0_6_outline_fn();

                // make sure that rotations are relative
                let bottom_case__part_3_bounds = bottom_case__part_3.getBounds();
                let bottom_case__part_3_x = bottom_case__part_3_bounds[0].x + (bottom_case__part_3_bounds[1].x - bottom_case__part_3_bounds[0].x) / 2
                let bottom_case__part_3_y = bottom_case__part_3_bounds[0].y + (bottom_case__part_3_bounds[1].y - bottom_case__part_3_bounds[0].y) / 2
                bottom_case__part_3 = translate([-bottom_case__part_3_x, -bottom_case__part_3_y, 0], bottom_case__part_3);
                bottom_case__part_3 = rotate([0,0,0], bottom_case__part_3);
                bottom_case__part_3 = translate([bottom_case__part_3_x, bottom_case__part_3_y, 0], bottom_case__part_3);

                bottom_case__part_3 = translate([0,0,0], bottom_case__part_3);
                result = result.subtract(bottom_case__part_3);
                
            
                    return result;
                }
            
            
        
            function main() {
                return bottom_case_case_fn();
            }

        