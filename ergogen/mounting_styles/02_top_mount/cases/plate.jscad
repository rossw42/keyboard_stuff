function switch_plate_extrude_1_6_outline_fn(){
    return new CSG.Path2D([[-10,28.05],[-10,4]]).appendPoint([-16,4]).appendPoint([-16,-4]).appendPoint([-10,-4]).appendPoint([-10,-9]).appendArc([-9,-10],{"radius":1,"clockwise":false,"large":false}).appendPoint([28.05,-10]).appendArc([29.05,-9],{"radius":1,"clockwise":false,"large":false}).appendPoint([29.05,-4]).appendPoint([35.05,-4]).appendPoint([35.05,4]).appendPoint([29.05,4]).appendPoint([29.05,28.05]).appendArc([28.05,29.05],{"radius":1,"clockwise":false,"large":false}).appendPoint([-9,29.05]).appendArc([-10,28.05],{"radius":1,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    CAG.circle({"center":[32.05,0],"radius":1.1})
.union(
    CAG.circle({"center":[-13,0],"radius":1.1})
).union(
    new CSG.Path2D([[12.05,12.05],[26.05,12.05]]).appendPoint([26.05,26.05]).appendPoint([12.05,26.05]).appendPoint([12.05,12.05]).close().innerToCAG()
).union(
    new CSG.Path2D([[12.05,-7],[26.05,-7]]).appendPoint([26.05,7]).appendPoint([12.05,7]).appendPoint([12.05,-7]).close().innerToCAG()
).union(
    new CSG.Path2D([[-7,12.05],[7,12.05]]).appendPoint([7,26.05]).appendPoint([-7,26.05]).appendPoint([-7,12.05]).close().innerToCAG()
).union(
    new CSG.Path2D([[-7,-7],[7,-7]]).appendPoint([7,7]).appendPoint([-7,7]).appendPoint([-7,-7]).close().innerToCAG()
)).extrude({ offset: [0, 0, 1.6] });
}




                function plate_case_fn() {
                    

                // creating part 0 of case plate
                let plate__part_0 = switch_plate_extrude_1_6_outline_fn();

                // make sure that rotations are relative
                let plate__part_0_bounds = plate__part_0.getBounds();
                let plate__part_0_x = plate__part_0_bounds[0].x + (plate__part_0_bounds[1].x - plate__part_0_bounds[0].x) / 2
                let plate__part_0_y = plate__part_0_bounds[0].y + (plate__part_0_bounds[1].y - plate__part_0_bounds[0].y) / 2
                plate__part_0 = translate([-plate__part_0_x, -plate__part_0_y, 0], plate__part_0);
                plate__part_0 = rotate([0,0,0], plate__part_0);
                plate__part_0 = translate([plate__part_0_x, plate__part_0_y, 0], plate__part_0);

                plate__part_0 = translate([0,0,0], plate__part_0);
                let result = plate__part_0;
                
            
                    return result;
                }
            
            
        
            function main() {
                return plate_case_fn();
            }

        