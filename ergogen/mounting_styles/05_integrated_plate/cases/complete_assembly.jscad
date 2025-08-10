function case_bottom_extrude_3_outline_fn(){
    return new CSG.Path2D([[-15,31.05],[-15,-12]]).appendArc([-12,-15],{"radius":3,"clockwise":false,"large":false}).appendPoint([31.05,-15]).appendArc([34.05,-12],{"radius":3,"clockwise":false,"large":false}).appendPoint([34.05,31.05]).appendArc([31.05,34.05],{"radius":3,"clockwise":false,"large":false}).appendPoint([-12,34.05]).appendArc([-15,31.05],{"radius":3,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 3] });
}


function mount_bosses_extrude_3_outline_fn(){
    return CAG.circle({"center":[-12,31.05],"radius":4})
.union(
    CAG.circle({"center":[31.05,31.05],"radius":4})
).union(
    CAG.circle({"center":[31.05,-12],"radius":4})
).union(
    CAG.circle({"center":[-12,-12],"radius":4})
).extrude({ offset: [0, 0, 3] });
}


function integrated_top_extrude_3_outline_fn(){
    return new CSG.Path2D([[-15,31.05],[-15,-12]]).appendArc([-12,-15],{"radius":3,"clockwise":false,"large":false}).appendPoint([31.05,-15]).appendArc([34.05,-12],{"radius":3,"clockwise":false,"large":false}).appendPoint([34.05,31.05]).appendArc([31.05,34.05],{"radius":3,"clockwise":false,"large":false}).appendPoint([-12,34.05]).appendArc([-15,31.05],{"radius":3,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 3] });
}


function switch_cutouts_extrude_2_outline_fn(){
    return new CSG.Path2D([[12.05,12.05],[26.05,12.05]]).appendPoint([26.05,26.05]).appendPoint([12.05,26.05]).appendPoint([12.05,12.05]).close().innerToCAG()
.union(
    new CSG.Path2D([[12.05,-7],[26.05,-7]]).appendPoint([26.05,7]).appendPoint([12.05,7]).appendPoint([12.05,-7]).close().innerToCAG()
).union(
    new CSG.Path2D([[-7,12.05],[7,12.05]]).appendPoint([7,26.05]).appendPoint([-7,26.05]).appendPoint([-7,12.05]).close().innerToCAG()
).union(
    new CSG.Path2D([[-7,-7],[7,-7]]).appendPoint([7,7]).appendPoint([-7,7]).appendPoint([-7,-7]).close().innerToCAG()
).extrude({ offset: [0, 0, 2] });
}


function mount_holes_extrude_8_outline_fn(){
    return CAG.circle({"center":[-12,31.05],"radius":1.1})
.union(
    CAG.circle({"center":[31.05,31.05],"radius":1.1})
).union(
    CAG.circle({"center":[31.05,-12],"radius":1.1})
).union(
    CAG.circle({"center":[-12,-12],"radius":1.1})
).extrude({ offset: [0, 0, 8] });
}


function threaded_inserts_extrude_2_outline_fn(){
    return CAG.circle({"center":[-12,31.05],"radius":2})
.union(
    CAG.circle({"center":[31.05,31.05],"radius":2})
).union(
    CAG.circle({"center":[31.05,-12],"radius":2})
).union(
    CAG.circle({"center":[-12,-12],"radius":2})
).extrude({ offset: [0, 0, 2] });
}




                function complete_assembly_case_fn() {
                    

                // creating part 0 of case complete_assembly
                let complete_assembly__part_0 = case_bottom_extrude_3_outline_fn();

                // make sure that rotations are relative
                let complete_assembly__part_0_bounds = complete_assembly__part_0.getBounds();
                let complete_assembly__part_0_x = complete_assembly__part_0_bounds[0].x + (complete_assembly__part_0_bounds[1].x - complete_assembly__part_0_bounds[0].x) / 2
                let complete_assembly__part_0_y = complete_assembly__part_0_bounds[0].y + (complete_assembly__part_0_bounds[1].y - complete_assembly__part_0_bounds[0].y) / 2
                complete_assembly__part_0 = translate([-complete_assembly__part_0_x, -complete_assembly__part_0_y, 0], complete_assembly__part_0);
                complete_assembly__part_0 = rotate([0,0,0], complete_assembly__part_0);
                complete_assembly__part_0 = translate([complete_assembly__part_0_x, complete_assembly__part_0_y, 0], complete_assembly__part_0);

                complete_assembly__part_0 = translate([0,0,0], complete_assembly__part_0);
                let result = complete_assembly__part_0;
                
            

                // creating part 1 of case complete_assembly
                let complete_assembly__part_1 = mount_bosses_extrude_3_outline_fn();

                // make sure that rotations are relative
                let complete_assembly__part_1_bounds = complete_assembly__part_1.getBounds();
                let complete_assembly__part_1_x = complete_assembly__part_1_bounds[0].x + (complete_assembly__part_1_bounds[1].x - complete_assembly__part_1_bounds[0].x) / 2
                let complete_assembly__part_1_y = complete_assembly__part_1_bounds[0].y + (complete_assembly__part_1_bounds[1].y - complete_assembly__part_1_bounds[0].y) / 2
                complete_assembly__part_1 = translate([-complete_assembly__part_1_x, -complete_assembly__part_1_y, 0], complete_assembly__part_1);
                complete_assembly__part_1 = rotate([0,0,0], complete_assembly__part_1);
                complete_assembly__part_1 = translate([complete_assembly__part_1_x, complete_assembly__part_1_y, 0], complete_assembly__part_1);

                complete_assembly__part_1 = translate([0,0,0], complete_assembly__part_1);
                result = result.union(complete_assembly__part_1);
                
            

                // creating part 2 of case complete_assembly
                let complete_assembly__part_2 = integrated_top_extrude_3_outline_fn();

                // make sure that rotations are relative
                let complete_assembly__part_2_bounds = complete_assembly__part_2.getBounds();
                let complete_assembly__part_2_x = complete_assembly__part_2_bounds[0].x + (complete_assembly__part_2_bounds[1].x - complete_assembly__part_2_bounds[0].x) / 2
                let complete_assembly__part_2_y = complete_assembly__part_2_bounds[0].y + (complete_assembly__part_2_bounds[1].y - complete_assembly__part_2_bounds[0].y) / 2
                complete_assembly__part_2 = translate([-complete_assembly__part_2_x, -complete_assembly__part_2_y, 0], complete_assembly__part_2);
                complete_assembly__part_2 = rotate([0,0,0], complete_assembly__part_2);
                complete_assembly__part_2 = translate([complete_assembly__part_2_x, complete_assembly__part_2_y, 0], complete_assembly__part_2);

                complete_assembly__part_2 = translate([0,0,3], complete_assembly__part_2);
                result = result.union(complete_assembly__part_2);
                
            

                // creating part 3 of case complete_assembly
                let complete_assembly__part_3 = mount_bosses_extrude_3_outline_fn();

                // make sure that rotations are relative
                let complete_assembly__part_3_bounds = complete_assembly__part_3.getBounds();
                let complete_assembly__part_3_x = complete_assembly__part_3_bounds[0].x + (complete_assembly__part_3_bounds[1].x - complete_assembly__part_3_bounds[0].x) / 2
                let complete_assembly__part_3_y = complete_assembly__part_3_bounds[0].y + (complete_assembly__part_3_bounds[1].y - complete_assembly__part_3_bounds[0].y) / 2
                complete_assembly__part_3 = translate([-complete_assembly__part_3_x, -complete_assembly__part_3_y, 0], complete_assembly__part_3);
                complete_assembly__part_3 = rotate([0,0,0], complete_assembly__part_3);
                complete_assembly__part_3 = translate([complete_assembly__part_3_x, complete_assembly__part_3_y, 0], complete_assembly__part_3);

                complete_assembly__part_3 = translate([0,0,3], complete_assembly__part_3);
                result = result.union(complete_assembly__part_3);
                
            

                // creating part 4 of case complete_assembly
                let complete_assembly__part_4 = switch_cutouts_extrude_2_outline_fn();

                // make sure that rotations are relative
                let complete_assembly__part_4_bounds = complete_assembly__part_4.getBounds();
                let complete_assembly__part_4_x = complete_assembly__part_4_bounds[0].x + (complete_assembly__part_4_bounds[1].x - complete_assembly__part_4_bounds[0].x) / 2
                let complete_assembly__part_4_y = complete_assembly__part_4_bounds[0].y + (complete_assembly__part_4_bounds[1].y - complete_assembly__part_4_bounds[0].y) / 2
                complete_assembly__part_4 = translate([-complete_assembly__part_4_x, -complete_assembly__part_4_y, 0], complete_assembly__part_4);
                complete_assembly__part_4 = rotate([0,0,0], complete_assembly__part_4);
                complete_assembly__part_4 = translate([complete_assembly__part_4_x, complete_assembly__part_4_y, 0], complete_assembly__part_4);

                complete_assembly__part_4 = translate([0,0,4], complete_assembly__part_4);
                result = result.subtract(complete_assembly__part_4);
                
            

                // creating part 5 of case complete_assembly
                let complete_assembly__part_5 = mount_holes_extrude_8_outline_fn();

                // make sure that rotations are relative
                let complete_assembly__part_5_bounds = complete_assembly__part_5.getBounds();
                let complete_assembly__part_5_x = complete_assembly__part_5_bounds[0].x + (complete_assembly__part_5_bounds[1].x - complete_assembly__part_5_bounds[0].x) / 2
                let complete_assembly__part_5_y = complete_assembly__part_5_bounds[0].y + (complete_assembly__part_5_bounds[1].y - complete_assembly__part_5_bounds[0].y) / 2
                complete_assembly__part_5 = translate([-complete_assembly__part_5_x, -complete_assembly__part_5_y, 0], complete_assembly__part_5);
                complete_assembly__part_5 = rotate([0,0,0], complete_assembly__part_5);
                complete_assembly__part_5 = translate([complete_assembly__part_5_x, complete_assembly__part_5_y, 0], complete_assembly__part_5);

                complete_assembly__part_5 = translate([0,0,0], complete_assembly__part_5);
                result = result.subtract(complete_assembly__part_5);
                
            

                // creating part 6 of case complete_assembly
                let complete_assembly__part_6 = threaded_inserts_extrude_2_outline_fn();

                // make sure that rotations are relative
                let complete_assembly__part_6_bounds = complete_assembly__part_6.getBounds();
                let complete_assembly__part_6_x = complete_assembly__part_6_bounds[0].x + (complete_assembly__part_6_bounds[1].x - complete_assembly__part_6_bounds[0].x) / 2
                let complete_assembly__part_6_y = complete_assembly__part_6_bounds[0].y + (complete_assembly__part_6_bounds[1].y - complete_assembly__part_6_bounds[0].y) / 2
                complete_assembly__part_6 = translate([-complete_assembly__part_6_x, -complete_assembly__part_6_y, 0], complete_assembly__part_6);
                complete_assembly__part_6 = rotate([0,0,0], complete_assembly__part_6);
                complete_assembly__part_6 = translate([complete_assembly__part_6_x, complete_assembly__part_6_y, 0], complete_assembly__part_6);

                complete_assembly__part_6 = translate([0,0,0], complete_assembly__part_6);
                result = result.subtract(complete_assembly__part_6);
                
            
                    return result;
                }
            
            
        
            function main() {
                return complete_assembly_case_fn();
            }

        