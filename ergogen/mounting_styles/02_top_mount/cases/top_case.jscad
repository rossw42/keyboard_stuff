function top_case_with_holes_extrude_2_outline_fn(){
    return new CSG.Path2D([[-15,31.05],[-15,6]]).appendPoint([-18,6]).appendPoint([-18,-6]).appendPoint([-15,-6]).appendPoint([-15,-12]).appendArc([-12,-15],{"radius":3,"clockwise":false,"large":false}).appendPoint([31.05,-15]).appendArc([34.05,-12],{"radius":3,"clockwise":false,"large":false}).appendPoint([34.05,-6]).appendPoint([37.05,-6]).appendPoint([37.05,6]).appendPoint([34.05,6]).appendPoint([34.05,31.05]).appendArc([31.05,34.05],{"radius":3,"clockwise":false,"large":false}).appendPoint([-12,34.05]).appendArc([-15,31.05],{"radius":3,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    CAG.circle({"center":[32.05,0],"radius":1.1})
.union(
    CAG.circle({"center":[-13,0],"radius":1.1})
)).extrude({ offset: [0, 0, 2] });
}




                function top_case_case_fn() {
                    

                // creating part 0 of case top_case
                let top_case__part_0 = top_case_with_holes_extrude_2_outline_fn();

                // make sure that rotations are relative
                let top_case__part_0_bounds = top_case__part_0.getBounds();
                let top_case__part_0_x = top_case__part_0_bounds[0].x + (top_case__part_0_bounds[1].x - top_case__part_0_bounds[0].x) / 2
                let top_case__part_0_y = top_case__part_0_bounds[0].y + (top_case__part_0_bounds[1].y - top_case__part_0_bounds[0].y) / 2
                top_case__part_0 = translate([-top_case__part_0_x, -top_case__part_0_y, 0], top_case__part_0);
                top_case__part_0 = rotate([0,0,0], top_case__part_0);
                top_case__part_0 = translate([top_case__part_0_x, top_case__part_0_y, 0], top_case__part_0);

                top_case__part_0 = translate([0,0,0], top_case__part_0);
                let result = top_case__part_0;
                
            
                    return result;
                }
            
            
        
            function main() {
                return top_case_case_fn();
            }

        