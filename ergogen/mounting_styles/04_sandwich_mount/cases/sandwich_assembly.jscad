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


function switch_plate_extrude_1_6_outline_fn(){
    return new CSG.Path2D([[-10,28.05],[-10,-9]]).appendArc([-9,-10],{"radius":1,"clockwise":false,"large":false}).appendPoint([28,-10]).appendArc([29,-9],{"radius":1,"clockwise":false,"large":false}).appendPoint([29,28.05]).appendArc([28,29.05],{"radius":1,"clockwise":false,"large":false}).appendPoint([-9,29.05]).appendArc([-10,28.05],{"radius":1,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    new CSG.Path2D([[12,12.05],[26,12.05]]).appendPoint([26,26.05]).appendPoint([12,26.05]).appendPoint([12,12.05]).close().innerToCAG()
.union(
    new CSG.Path2D([[12,-7],[26,-7]]).appendPoint([26,7]).appendPoint([12,7]).appendPoint([12,-7]).close().innerToCAG()
).union(
    new CSG.Path2D([[-7,12.05],[7,12.05]]).appendPoint([7,26.05]).appendPoint([-7,26.05]).appendPoint([-7,12.05]).close().innerToCAG()
).union(
    new CSG.Path2D([[-7,-7],[7,-7]]).appendPoint([7,7]).appendPoint([-7,7]).appendPoint([-7,-7]).close().innerToCAG()
)).extrude({ offset: [0, 0, 1.6] });
}


function through_holes_extrude_15_outline_fn(){
    return CAG.circle({"center":[-12,31.05],"radius":1.1})
.union(
    CAG.circle({"center":[31,31.05],"radius":1.1})
).union(
    CAG.circle({"center":[31,-12],"radius":1.1})
).union(
    CAG.circle({"center":[-12,-12],"radius":1.1})
).extrude({ offset: [0, 0, 15] });
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




                function sandwich_assembly_case_fn() {
                    

                // creating part 0 of case sandwich_assembly
                let sandwich_assembly__part_0 = case_outline_extrude_6_outline_fn();

                // make sure that rotations are relative
                let sandwich_assembly__part_0_bounds = sandwich_assembly__part_0.getBounds();
                let sandwich_assembly__part_0_x = sandwich_assembly__part_0_bounds[0].x + (sandwich_assembly__part_0_bounds[1].x - sandwich_assembly__part_0_bounds[0].x) / 2
                let sandwich_assembly__part_0_y = sandwich_assembly__part_0_bounds[0].y + (sandwich_assembly__part_0_bounds[1].y - sandwich_assembly__part_0_bounds[0].y) / 2
                sandwich_assembly__part_0 = translate([-sandwich_assembly__part_0_x, -sandwich_assembly__part_0_y, 0], sandwich_assembly__part_0);
                sandwich_assembly__part_0 = rotate([0,0,0], sandwich_assembly__part_0);
                sandwich_assembly__part_0 = translate([sandwich_assembly__part_0_x, sandwich_assembly__part_0_y, 0], sandwich_assembly__part_0);

                sandwich_assembly__part_0 = translate([0,0,0], sandwich_assembly__part_0);
                let result = sandwich_assembly__part_0;
                
            

                // creating part 1 of case sandwich_assembly
                let sandwich_assembly__part_1 = screw_bosses_extrude_6_outline_fn();

                // make sure that rotations are relative
                let sandwich_assembly__part_1_bounds = sandwich_assembly__part_1.getBounds();
                let sandwich_assembly__part_1_x = sandwich_assembly__part_1_bounds[0].x + (sandwich_assembly__part_1_bounds[1].x - sandwich_assembly__part_1_bounds[0].x) / 2
                let sandwich_assembly__part_1_y = sandwich_assembly__part_1_bounds[0].y + (sandwich_assembly__part_1_bounds[1].y - sandwich_assembly__part_1_bounds[0].y) / 2
                sandwich_assembly__part_1 = translate([-sandwich_assembly__part_1_x, -sandwich_assembly__part_1_y, 0], sandwich_assembly__part_1);
                sandwich_assembly__part_1 = rotate([0,0,0], sandwich_assembly__part_1);
                sandwich_assembly__part_1 = translate([sandwich_assembly__part_1_x, sandwich_assembly__part_1_y, 0], sandwich_assembly__part_1);

                sandwich_assembly__part_1 = translate([0,0,0], sandwich_assembly__part_1);
                result = result.union(sandwich_assembly__part_1);
                
            

                // creating part 2 of case sandwich_assembly
                let sandwich_assembly__part_2 = switch_plate_extrude_1_6_outline_fn();

                // make sure that rotations are relative
                let sandwich_assembly__part_2_bounds = sandwich_assembly__part_2.getBounds();
                let sandwich_assembly__part_2_x = sandwich_assembly__part_2_bounds[0].x + (sandwich_assembly__part_2_bounds[1].x - sandwich_assembly__part_2_bounds[0].x) / 2
                let sandwich_assembly__part_2_y = sandwich_assembly__part_2_bounds[0].y + (sandwich_assembly__part_2_bounds[1].y - sandwich_assembly__part_2_bounds[0].y) / 2
                sandwich_assembly__part_2 = translate([-sandwich_assembly__part_2_x, -sandwich_assembly__part_2_y, 0], sandwich_assembly__part_2);
                sandwich_assembly__part_2 = rotate([0,0,0], sandwich_assembly__part_2);
                sandwich_assembly__part_2 = translate([sandwich_assembly__part_2_x, sandwich_assembly__part_2_y, 0], sandwich_assembly__part_2);

                sandwich_assembly__part_2 = translate([0,0,6], sandwich_assembly__part_2);
                result = result.union(sandwich_assembly__part_2);
                
            

                // creating part 3 of case sandwich_assembly
                let sandwich_assembly__part_3 = case_outline_extrude_6_outline_fn();

                // make sure that rotations are relative
                let sandwich_assembly__part_3_bounds = sandwich_assembly__part_3.getBounds();
                let sandwich_assembly__part_3_x = sandwich_assembly__part_3_bounds[0].x + (sandwich_assembly__part_3_bounds[1].x - sandwich_assembly__part_3_bounds[0].x) / 2
                let sandwich_assembly__part_3_y = sandwich_assembly__part_3_bounds[0].y + (sandwich_assembly__part_3_bounds[1].y - sandwich_assembly__part_3_bounds[0].y) / 2
                sandwich_assembly__part_3 = translate([-sandwich_assembly__part_3_x, -sandwich_assembly__part_3_y, 0], sandwich_assembly__part_3);
                sandwich_assembly__part_3 = rotate([0,0,0], sandwich_assembly__part_3);
                sandwich_assembly__part_3 = translate([sandwich_assembly__part_3_x, sandwich_assembly__part_3_y, 0], sandwich_assembly__part_3);

                sandwich_assembly__part_3 = translate([0,0,7.6], sandwich_assembly__part_3);
                result = result.union(sandwich_assembly__part_3);
                
            

                // creating part 4 of case sandwich_assembly
                let sandwich_assembly__part_4 = screw_bosses_extrude_6_outline_fn();

                // make sure that rotations are relative
                let sandwich_assembly__part_4_bounds = sandwich_assembly__part_4.getBounds();
                let sandwich_assembly__part_4_x = sandwich_assembly__part_4_bounds[0].x + (sandwich_assembly__part_4_bounds[1].x - sandwich_assembly__part_4_bounds[0].x) / 2
                let sandwich_assembly__part_4_y = sandwich_assembly__part_4_bounds[0].y + (sandwich_assembly__part_4_bounds[1].y - sandwich_assembly__part_4_bounds[0].y) / 2
                sandwich_assembly__part_4 = translate([-sandwich_assembly__part_4_x, -sandwich_assembly__part_4_y, 0], sandwich_assembly__part_4);
                sandwich_assembly__part_4 = rotate([0,0,0], sandwich_assembly__part_4);
                sandwich_assembly__part_4 = translate([sandwich_assembly__part_4_x, sandwich_assembly__part_4_y, 0], sandwich_assembly__part_4);

                sandwich_assembly__part_4 = translate([0,0,7.6], sandwich_assembly__part_4);
                result = result.union(sandwich_assembly__part_4);
                
            

                // creating part 5 of case sandwich_assembly
                let sandwich_assembly__part_5 = through_holes_extrude_15_outline_fn();

                // make sure that rotations are relative
                let sandwich_assembly__part_5_bounds = sandwich_assembly__part_5.getBounds();
                let sandwich_assembly__part_5_x = sandwich_assembly__part_5_bounds[0].x + (sandwich_assembly__part_5_bounds[1].x - sandwich_assembly__part_5_bounds[0].x) / 2
                let sandwich_assembly__part_5_y = sandwich_assembly__part_5_bounds[0].y + (sandwich_assembly__part_5_bounds[1].y - sandwich_assembly__part_5_bounds[0].y) / 2
                sandwich_assembly__part_5 = translate([-sandwich_assembly__part_5_x, -sandwich_assembly__part_5_y, 0], sandwich_assembly__part_5);
                sandwich_assembly__part_5 = rotate([0,0,0], sandwich_assembly__part_5);
                sandwich_assembly__part_5 = translate([sandwich_assembly__part_5_x, sandwich_assembly__part_5_y, 0], sandwich_assembly__part_5);

                sandwich_assembly__part_5 = translate([0,0,0], sandwich_assembly__part_5);
                result = result.subtract(sandwich_assembly__part_5);
                
            

                // creating part 6 of case sandwich_assembly
                let sandwich_assembly__part_6 = countersink_holes_extrude_0_6_outline_fn();

                // make sure that rotations are relative
                let sandwich_assembly__part_6_bounds = sandwich_assembly__part_6.getBounds();
                let sandwich_assembly__part_6_x = sandwich_assembly__part_6_bounds[0].x + (sandwich_assembly__part_6_bounds[1].x - sandwich_assembly__part_6_bounds[0].x) / 2
                let sandwich_assembly__part_6_y = sandwich_assembly__part_6_bounds[0].y + (sandwich_assembly__part_6_bounds[1].y - sandwich_assembly__part_6_bounds[0].y) / 2
                sandwich_assembly__part_6 = translate([-sandwich_assembly__part_6_x, -sandwich_assembly__part_6_y, 0], sandwich_assembly__part_6);
                sandwich_assembly__part_6 = rotate([0,0,0], sandwich_assembly__part_6);
                sandwich_assembly__part_6 = translate([sandwich_assembly__part_6_x, sandwich_assembly__part_6_y, 0], sandwich_assembly__part_6);

                sandwich_assembly__part_6 = translate([0,0,0], sandwich_assembly__part_6);
                result = result.subtract(sandwich_assembly__part_6);
                
            

                // creating part 7 of case sandwich_assembly
                let sandwich_assembly__part_7 = countersink_holes_extrude_0_6_outline_fn();

                // make sure that rotations are relative
                let sandwich_assembly__part_7_bounds = sandwich_assembly__part_7.getBounds();
                let sandwich_assembly__part_7_x = sandwich_assembly__part_7_bounds[0].x + (sandwich_assembly__part_7_bounds[1].x - sandwich_assembly__part_7_bounds[0].x) / 2
                let sandwich_assembly__part_7_y = sandwich_assembly__part_7_bounds[0].y + (sandwich_assembly__part_7_bounds[1].y - sandwich_assembly__part_7_bounds[0].y) / 2
                sandwich_assembly__part_7 = translate([-sandwich_assembly__part_7_x, -sandwich_assembly__part_7_y, 0], sandwich_assembly__part_7);
                sandwich_assembly__part_7 = rotate([0,0,0], sandwich_assembly__part_7);
                sandwich_assembly__part_7 = translate([sandwich_assembly__part_7_x, sandwich_assembly__part_7_y, 0], sandwich_assembly__part_7);

                sandwich_assembly__part_7 = translate([0,0,13.4], sandwich_assembly__part_7);
                result = result.subtract(sandwich_assembly__part_7);
                
            
                    return result;
                }
            
            
        
            function main() {
                return sandwich_assembly_case_fn();
            }

        