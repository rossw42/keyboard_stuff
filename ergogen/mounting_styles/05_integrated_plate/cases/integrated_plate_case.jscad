function integrated_top_extrude_3_outline_fn(){
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


function mount_holes_extrude_4_outline_fn(){
    return CAG.circle({"center":[-12,31.05],"radius":1.1})
.union(
    CAG.circle({"center":[31.05,31.05],"radius":1.1})
).union(
    CAG.circle({"center":[31.05,-12],"radius":1.1})
).union(
    CAG.circle({"center":[-12,-12],"radius":1.1})
).extrude({ offset: [0, 0, 4] });
}




                function integrated_plate_case_case_fn() {
                    

                // creating part 0 of case integrated_plate_case
                let integrated_plate_case__part_0 = integrated_top_extrude_3_outline_fn();

                // make sure that rotations are relative
                let integrated_plate_case__part_0_bounds = integrated_plate_case__part_0.getBounds();
                let integrated_plate_case__part_0_x = integrated_plate_case__part_0_bounds[0].x + (integrated_plate_case__part_0_bounds[1].x - integrated_plate_case__part_0_bounds[0].x) / 2
                let integrated_plate_case__part_0_y = integrated_plate_case__part_0_bounds[0].y + (integrated_plate_case__part_0_bounds[1].y - integrated_plate_case__part_0_bounds[0].y) / 2
                integrated_plate_case__part_0 = translate([-integrated_plate_case__part_0_x, -integrated_plate_case__part_0_y, 0], integrated_plate_case__part_0);
                integrated_plate_case__part_0 = rotate([0,0,0], integrated_plate_case__part_0);
                integrated_plate_case__part_0 = translate([integrated_plate_case__part_0_x, integrated_plate_case__part_0_y, 0], integrated_plate_case__part_0);

                integrated_plate_case__part_0 = translate([0,0,0], integrated_plate_case__part_0);
                let result = integrated_plate_case__part_0;
                
            

                // creating part 1 of case integrated_plate_case
                let integrated_plate_case__part_1 = mount_bosses_extrude_3_outline_fn();

                // make sure that rotations are relative
                let integrated_plate_case__part_1_bounds = integrated_plate_case__part_1.getBounds();
                let integrated_plate_case__part_1_x = integrated_plate_case__part_1_bounds[0].x + (integrated_plate_case__part_1_bounds[1].x - integrated_plate_case__part_1_bounds[0].x) / 2
                let integrated_plate_case__part_1_y = integrated_plate_case__part_1_bounds[0].y + (integrated_plate_case__part_1_bounds[1].y - integrated_plate_case__part_1_bounds[0].y) / 2
                integrated_plate_case__part_1 = translate([-integrated_plate_case__part_1_x, -integrated_plate_case__part_1_y, 0], integrated_plate_case__part_1);
                integrated_plate_case__part_1 = rotate([0,0,0], integrated_plate_case__part_1);
                integrated_plate_case__part_1 = translate([integrated_plate_case__part_1_x, integrated_plate_case__part_1_y, 0], integrated_plate_case__part_1);

                integrated_plate_case__part_1 = translate([0,0,0], integrated_plate_case__part_1);
                result = result.union(integrated_plate_case__part_1);
                
            

                // creating part 2 of case integrated_plate_case
                let integrated_plate_case__part_2 = switch_cutouts_extrude_2_outline_fn();

                // make sure that rotations are relative
                let integrated_plate_case__part_2_bounds = integrated_plate_case__part_2.getBounds();
                let integrated_plate_case__part_2_x = integrated_plate_case__part_2_bounds[0].x + (integrated_plate_case__part_2_bounds[1].x - integrated_plate_case__part_2_bounds[0].x) / 2
                let integrated_plate_case__part_2_y = integrated_plate_case__part_2_bounds[0].y + (integrated_plate_case__part_2_bounds[1].y - integrated_plate_case__part_2_bounds[0].y) / 2
                integrated_plate_case__part_2 = translate([-integrated_plate_case__part_2_x, -integrated_plate_case__part_2_y, 0], integrated_plate_case__part_2);
                integrated_plate_case__part_2 = rotate([0,0,0], integrated_plate_case__part_2);
                integrated_plate_case__part_2 = translate([integrated_plate_case__part_2_x, integrated_plate_case__part_2_y, 0], integrated_plate_case__part_2);

                integrated_plate_case__part_2 = translate([0,0,1], integrated_plate_case__part_2);
                result = result.subtract(integrated_plate_case__part_2);
                
            

                // creating part 3 of case integrated_plate_case
                let integrated_plate_case__part_3 = mount_holes_extrude_4_outline_fn();

                // make sure that rotations are relative
                let integrated_plate_case__part_3_bounds = integrated_plate_case__part_3.getBounds();
                let integrated_plate_case__part_3_x = integrated_plate_case__part_3_bounds[0].x + (integrated_plate_case__part_3_bounds[1].x - integrated_plate_case__part_3_bounds[0].x) / 2
                let integrated_plate_case__part_3_y = integrated_plate_case__part_3_bounds[0].y + (integrated_plate_case__part_3_bounds[1].y - integrated_plate_case__part_3_bounds[0].y) / 2
                integrated_plate_case__part_3 = translate([-integrated_plate_case__part_3_x, -integrated_plate_case__part_3_y, 0], integrated_plate_case__part_3);
                integrated_plate_case__part_3 = rotate([0,0,0], integrated_plate_case__part_3);
                integrated_plate_case__part_3 = translate([integrated_plate_case__part_3_x, integrated_plate_case__part_3_y, 0], integrated_plate_case__part_3);

                integrated_plate_case__part_3 = translate([0,0,0], integrated_plate_case__part_3);
                result = result.subtract(integrated_plate_case__part_3);
                
            
                    return result;
                }
            
            
        
            function main() {
                return integrated_plate_case_case_fn();
            }

        