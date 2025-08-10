function case_outline_extrude_1_outline_fn(){
    return new CSG.Path2D([[-12,29.05],[-12,-10]]).appendArc([-10,-12],{"radius":2,"clockwise":false,"large":false}).appendPoint([29.05,-12]).appendArc([31.05,-10],{"radius":2,"clockwise":false,"large":false}).appendPoint([31.05,29.05]).appendArc([29.05,31.05],{"radius":2,"clockwise":false,"large":false}).appendPoint([-10,31.05]).appendArc([-12,29.05],{"radius":2,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 1] });
}


function case_outline_extrude_8_outline_fn(){
    return new CSG.Path2D([[-12,29.05],[-12,-10]]).appendArc([-10,-12],{"radius":2,"clockwise":false,"large":false}).appendPoint([29.05,-12]).appendArc([31.05,-10],{"radius":2,"clockwise":false,"large":false}).appendPoint([31.05,29.05]).appendArc([29.05,31.05],{"radius":2,"clockwise":false,"large":false}).appendPoint([-10,31.05]).appendArc([-12,29.05],{"radius":2,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 8] });
}


function board_extrude_8_outline_fn(){
    return new CSG.Path2D([[-10,27.05],[-10,-8]]).appendArc([-8,-10],{"radius":2,"clockwise":false,"large":false}).appendPoint([27.05,-10]).appendArc([29.05,-8],{"radius":2,"clockwise":false,"large":false}).appendPoint([29.05,27.05]).appendArc([27.05,29.05],{"radius":2,"clockwise":false,"large":false}).appendPoint([-8,29.05]).appendArc([-10,27.05],{"radius":2,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 8] });
}


function standoff_posts_extrude_4_outline_fn(){
    return CAG.circle({"center":[31.05,31.05],"radius":2.5})
.union(
    CAG.circle({"center":[-12,-12],"radius":2.5})
).union(
    CAG.circle({"center":[9.525,9.525],"radius":2.5})
).extrude({ offset: [0, 0, 4] });
}


function screw_holes_extrude_8_outline_fn(){
    return CAG.circle({"center":[31.05,31.05],"radius":1.1})
.union(
    CAG.circle({"center":[-12,-12],"radius":1.1})
).union(
    CAG.circle({"center":[9.525,9.525],"radius":1.1})
).extrude({ offset: [0, 0, 8] });
}




                function tray_case_case_fn() {
                    

                // creating part 0 of case tray_case
                let tray_case__part_0 = case_outline_extrude_1_outline_fn();

                // make sure that rotations are relative
                let tray_case__part_0_bounds = tray_case__part_0.getBounds();
                let tray_case__part_0_x = tray_case__part_0_bounds[0].x + (tray_case__part_0_bounds[1].x - tray_case__part_0_bounds[0].x) / 2
                let tray_case__part_0_y = tray_case__part_0_bounds[0].y + (tray_case__part_0_bounds[1].y - tray_case__part_0_bounds[0].y) / 2
                tray_case__part_0 = translate([-tray_case__part_0_x, -tray_case__part_0_y, 0], tray_case__part_0);
                tray_case__part_0 = rotate([0,0,0], tray_case__part_0);
                tray_case__part_0 = translate([tray_case__part_0_x, tray_case__part_0_y, 0], tray_case__part_0);

                tray_case__part_0 = translate([0,0,0], tray_case__part_0);
                let result = tray_case__part_0;
                
            

                // creating part 1 of case tray_case
                let tray_case__part_1 = case_outline_extrude_8_outline_fn();

                // make sure that rotations are relative
                let tray_case__part_1_bounds = tray_case__part_1.getBounds();
                let tray_case__part_1_x = tray_case__part_1_bounds[0].x + (tray_case__part_1_bounds[1].x - tray_case__part_1_bounds[0].x) / 2
                let tray_case__part_1_y = tray_case__part_1_bounds[0].y + (tray_case__part_1_bounds[1].y - tray_case__part_1_bounds[0].y) / 2
                tray_case__part_1 = translate([-tray_case__part_1_x, -tray_case__part_1_y, 0], tray_case__part_1);
                tray_case__part_1 = rotate([0,0,0], tray_case__part_1);
                tray_case__part_1 = translate([tray_case__part_1_x, tray_case__part_1_y, 0], tray_case__part_1);

                tray_case__part_1 = translate([0,0,0], tray_case__part_1);
                result = result.union(tray_case__part_1);
                
            

                // creating part 2 of case tray_case
                let tray_case__part_2 = board_extrude_8_outline_fn();

                // make sure that rotations are relative
                let tray_case__part_2_bounds = tray_case__part_2.getBounds();
                let tray_case__part_2_x = tray_case__part_2_bounds[0].x + (tray_case__part_2_bounds[1].x - tray_case__part_2_bounds[0].x) / 2
                let tray_case__part_2_y = tray_case__part_2_bounds[0].y + (tray_case__part_2_bounds[1].y - tray_case__part_2_bounds[0].y) / 2
                tray_case__part_2 = translate([-tray_case__part_2_x, -tray_case__part_2_y, 0], tray_case__part_2);
                tray_case__part_2 = rotate([0,0,0], tray_case__part_2);
                tray_case__part_2 = translate([tray_case__part_2_x, tray_case__part_2_y, 0], tray_case__part_2);

                tray_case__part_2 = translate([0,0,0], tray_case__part_2);
                result = result.subtract(tray_case__part_2);
                
            

                // creating part 3 of case tray_case
                let tray_case__part_3 = standoff_posts_extrude_4_outline_fn();

                // make sure that rotations are relative
                let tray_case__part_3_bounds = tray_case__part_3.getBounds();
                let tray_case__part_3_x = tray_case__part_3_bounds[0].x + (tray_case__part_3_bounds[1].x - tray_case__part_3_bounds[0].x) / 2
                let tray_case__part_3_y = tray_case__part_3_bounds[0].y + (tray_case__part_3_bounds[1].y - tray_case__part_3_bounds[0].y) / 2
                tray_case__part_3 = translate([-tray_case__part_3_x, -tray_case__part_3_y, 0], tray_case__part_3);
                tray_case__part_3 = rotate([0,0,0], tray_case__part_3);
                tray_case__part_3 = translate([tray_case__part_3_x, tray_case__part_3_y, 0], tray_case__part_3);

                tray_case__part_3 = translate([0,0,0], tray_case__part_3);
                result = result.union(tray_case__part_3);
                
            

                // creating part 4 of case tray_case
                let tray_case__part_4 = screw_holes_extrude_8_outline_fn();

                // make sure that rotations are relative
                let tray_case__part_4_bounds = tray_case__part_4.getBounds();
                let tray_case__part_4_x = tray_case__part_4_bounds[0].x + (tray_case__part_4_bounds[1].x - tray_case__part_4_bounds[0].x) / 2
                let tray_case__part_4_y = tray_case__part_4_bounds[0].y + (tray_case__part_4_bounds[1].y - tray_case__part_4_bounds[0].y) / 2
                tray_case__part_4 = translate([-tray_case__part_4_x, -tray_case__part_4_y, 0], tray_case__part_4);
                tray_case__part_4 = rotate([0,0,0], tray_case__part_4);
                tray_case__part_4 = translate([tray_case__part_4_x, tray_case__part_4_y, 0], tray_case__part_4);

                tray_case__part_4 = translate([0,0,0], tray_case__part_4);
                result = result.subtract(tray_case__part_4);
                
            
                    return result;
                }
            
            
        
            function main() {
                return tray_case_case_fn();
            }

        