function bottom_outline_extrude_2_outline_fn(){
    return new CSG.Path2D([[-15,37.05],[-15,-18]]).appendArc([-13,-20],{"radius":2,"clockwise":false,"large":false}).appendPoint([70.15,-20]).appendArc([72.15,-18],{"radius":2,"clockwise":false,"large":false}).appendPoint([72.15,37.05]).appendArc([70.15,39.05],{"radius":2,"clockwise":false,"large":false}).appendPoint([-13,39.05]).appendArc([-15,37.05],{"radius":2,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 2] });
}




                function case_base_case_fn() {
                    

                // creating part 0 of case case_base
                let case_base__part_0 = bottom_outline_extrude_2_outline_fn();

                // make sure that rotations are relative
                let case_base__part_0_bounds = case_base__part_0.getBounds();
                let case_base__part_0_x = case_base__part_0_bounds[0].x + (case_base__part_0_bounds[1].x - case_base__part_0_bounds[0].x) / 2
                let case_base__part_0_y = case_base__part_0_bounds[0].y + (case_base__part_0_bounds[1].y - case_base__part_0_bounds[0].y) / 2
                case_base__part_0 = translate([-case_base__part_0_x, -case_base__part_0_y, 0], case_base__part_0);
                case_base__part_0 = rotate([0,0,0], case_base__part_0);
                case_base__part_0 = translate([case_base__part_0_x, case_base__part_0_y, 0], case_base__part_0);

                case_base__part_0 = translate([0,0,0], case_base__part_0);
                let result = case_base__part_0;
                
            
                    return result;
                }
            
            
        
            function main() {
                return case_base_case_fn();
            }

        