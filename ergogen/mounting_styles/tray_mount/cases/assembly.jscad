function expanded_board_extrude_5_6_outline_fn(){
    return new CSG.Path2D([[-13,27.05],[-13,-8]]).appendArc([-8,-13],{"radius":5,"clockwise":false,"large":false}).appendPoint([65.15,-13]).appendArc([70.15,-8],{"radius":5,"clockwise":false,"large":false}).appendPoint([70.15,27.05]).appendArc([65.15,32.05],{"radius":5,"clockwise":false,"large":false}).appendPoint([-8,32.05]).appendArc([-13,27.05],{"radius":5,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 5.6] });
}


function board_extrude_5_6_outline_fn(){
    return new CSG.Path2D([[-10,27.05],[-10,-8]]).appendArc([-8,-10],{"radius":2,"clockwise":false,"large":false}).appendPoint([65.15,-10]).appendArc([67.15,-8],{"radius":2,"clockwise":false,"large":false}).appendPoint([67.15,27.05]).appendArc([65.15,29.05],{"radius":2,"clockwise":false,"large":false}).appendPoint([-8,29.05]).appendArc([-10,27.05],{"radius":2,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 5.6] });
}


function mounting_posts_extrude_4_outline_fn(){
    return CAG.circle({"center":[85.625,-19.05],"radius":2.5})
.union(
    CAG.circle({"center":[95.2,15],"radius":2.5})
).union(
    CAG.circle({"center":[19.05,15],"radius":2.5})
).extrude({ offset: [0, 0, 4] });
}


function mounting_holes_extrude_5_outline_fn(){
    return CAG.circle({"center":[85.625,-19.05],"radius":1.1})
.union(
    CAG.circle({"center":[95.2,15],"radius":1.1})
).union(
    CAG.circle({"center":[19.05,15],"radius":1.1})
).extrude({ offset: [0, 0, 5] });
}




                function case_bottom_case_fn() {
                    

                // creating part 0 of case case_bottom
                let case_bottom__part_0 = _outer_wall_case_fn();

                // make sure that rotations are relative
                let case_bottom__part_0_bounds = case_bottom__part_0.getBounds();
                let case_bottom__part_0_x = case_bottom__part_0_bounds[0].x + (case_bottom__part_0_bounds[1].x - case_bottom__part_0_bounds[0].x) / 2
                let case_bottom__part_0_y = case_bottom__part_0_bounds[0].y + (case_bottom__part_0_bounds[1].y - case_bottom__part_0_bounds[0].y) / 2
                case_bottom__part_0 = translate([-case_bottom__part_0_x, -case_bottom__part_0_y, 0], case_bottom__part_0);
                case_bottom__part_0 = rotate([0,0,0], case_bottom__part_0);
                case_bottom__part_0 = translate([case_bottom__part_0_x, case_bottom__part_0_y, 0], case_bottom__part_0);

                case_bottom__part_0 = translate([0,0,0], case_bottom__part_0);
                let result = case_bottom__part_0;
                
            

                // creating part 1 of case case_bottom
                let case_bottom__part_1 = _inner_cavity_case_fn();

                // make sure that rotations are relative
                let case_bottom__part_1_bounds = case_bottom__part_1.getBounds();
                let case_bottom__part_1_x = case_bottom__part_1_bounds[0].x + (case_bottom__part_1_bounds[1].x - case_bottom__part_1_bounds[0].x) / 2
                let case_bottom__part_1_y = case_bottom__part_1_bounds[0].y + (case_bottom__part_1_bounds[1].y - case_bottom__part_1_bounds[0].y) / 2
                case_bottom__part_1 = translate([-case_bottom__part_1_x, -case_bottom__part_1_y, 0], case_bottom__part_1);
                case_bottom__part_1 = rotate([0,0,0], case_bottom__part_1);
                case_bottom__part_1 = translate([case_bottom__part_1_x, case_bottom__part_1_y, 0], case_bottom__part_1);

                case_bottom__part_1 = translate([0,0,0], case_bottom__part_1);
                result = result.subtract(case_bottom__part_1);
                
            

                // creating part 2 of case case_bottom
                let case_bottom__part_2 = _mounting_posts_case_fn();

                // make sure that rotations are relative
                let case_bottom__part_2_bounds = case_bottom__part_2.getBounds();
                let case_bottom__part_2_x = case_bottom__part_2_bounds[0].x + (case_bottom__part_2_bounds[1].x - case_bottom__part_2_bounds[0].x) / 2
                let case_bottom__part_2_y = case_bottom__part_2_bounds[0].y + (case_bottom__part_2_bounds[1].y - case_bottom__part_2_bounds[0].y) / 2
                case_bottom__part_2 = translate([-case_bottom__part_2_x, -case_bottom__part_2_y, 0], case_bottom__part_2);
                case_bottom__part_2 = rotate([0,0,0], case_bottom__part_2);
                case_bottom__part_2 = translate([case_bottom__part_2_x, case_bottom__part_2_y, 0], case_bottom__part_2);

                case_bottom__part_2 = translate([0,0,0], case_bottom__part_2);
                result = result.union(case_bottom__part_2);
                
            

                // creating part 3 of case case_bottom
                let case_bottom__part_3 = _mounting_holes_case_fn();

                // make sure that rotations are relative
                let case_bottom__part_3_bounds = case_bottom__part_3.getBounds();
                let case_bottom__part_3_x = case_bottom__part_3_bounds[0].x + (case_bottom__part_3_bounds[1].x - case_bottom__part_3_bounds[0].x) / 2
                let case_bottom__part_3_y = case_bottom__part_3_bounds[0].y + (case_bottom__part_3_bounds[1].y - case_bottom__part_3_bounds[0].y) / 2
                case_bottom__part_3 = translate([-case_bottom__part_3_x, -case_bottom__part_3_y, 0], case_bottom__part_3);
                case_bottom__part_3 = rotate([0,0,0], case_bottom__part_3);
                case_bottom__part_3 = translate([case_bottom__part_3_x, case_bottom__part_3_y, 0], case_bottom__part_3);

                case_bottom__part_3 = translate([0,0,0], case_bottom__part_3);
                result = result.subtract(case_bottom__part_3);
                
            
                    return result;
                }
            
            

                function _outer_wall_case_fn() {
                    

                // creating part 0 of case _outer_wall
                let _outer_wall__part_0 = expanded_board_extrude_5_6_outline_fn();

                // make sure that rotations are relative
                let _outer_wall__part_0_bounds = _outer_wall__part_0.getBounds();
                let _outer_wall__part_0_x = _outer_wall__part_0_bounds[0].x + (_outer_wall__part_0_bounds[1].x - _outer_wall__part_0_bounds[0].x) / 2
                let _outer_wall__part_0_y = _outer_wall__part_0_bounds[0].y + (_outer_wall__part_0_bounds[1].y - _outer_wall__part_0_bounds[0].y) / 2
                _outer_wall__part_0 = translate([-_outer_wall__part_0_x, -_outer_wall__part_0_y, 0], _outer_wall__part_0);
                _outer_wall__part_0 = rotate([0,0,0], _outer_wall__part_0);
                _outer_wall__part_0 = translate([_outer_wall__part_0_x, _outer_wall__part_0_y, 0], _outer_wall__part_0);

                _outer_wall__part_0 = translate([0,0,0], _outer_wall__part_0);
                let result = _outer_wall__part_0;
                
            
                    return result;
                }
            
            

                function _inner_cavity_case_fn() {
                    

                // creating part 0 of case _inner_cavity
                let _inner_cavity__part_0 = board_extrude_5_6_outline_fn();

                // make sure that rotations are relative
                let _inner_cavity__part_0_bounds = _inner_cavity__part_0.getBounds();
                let _inner_cavity__part_0_x = _inner_cavity__part_0_bounds[0].x + (_inner_cavity__part_0_bounds[1].x - _inner_cavity__part_0_bounds[0].x) / 2
                let _inner_cavity__part_0_y = _inner_cavity__part_0_bounds[0].y + (_inner_cavity__part_0_bounds[1].y - _inner_cavity__part_0_bounds[0].y) / 2
                _inner_cavity__part_0 = translate([-_inner_cavity__part_0_x, -_inner_cavity__part_0_y, 0], _inner_cavity__part_0);
                _inner_cavity__part_0 = rotate([0,0,0], _inner_cavity__part_0);
                _inner_cavity__part_0 = translate([_inner_cavity__part_0_x, _inner_cavity__part_0_y, 0], _inner_cavity__part_0);

                _inner_cavity__part_0 = translate([0,0,0], _inner_cavity__part_0);
                let result = _inner_cavity__part_0;
                
            
                    return result;
                }
            
            

                function _mounting_posts_case_fn() {
                    

                // creating part 0 of case _mounting_posts
                let _mounting_posts__part_0 = mounting_posts_extrude_4_outline_fn();

                // make sure that rotations are relative
                let _mounting_posts__part_0_bounds = _mounting_posts__part_0.getBounds();
                let _mounting_posts__part_0_x = _mounting_posts__part_0_bounds[0].x + (_mounting_posts__part_0_bounds[1].x - _mounting_posts__part_0_bounds[0].x) / 2
                let _mounting_posts__part_0_y = _mounting_posts__part_0_bounds[0].y + (_mounting_posts__part_0_bounds[1].y - _mounting_posts__part_0_bounds[0].y) / 2
                _mounting_posts__part_0 = translate([-_mounting_posts__part_0_x, -_mounting_posts__part_0_y, 0], _mounting_posts__part_0);
                _mounting_posts__part_0 = rotate([0,0,0], _mounting_posts__part_0);
                _mounting_posts__part_0 = translate([_mounting_posts__part_0_x, _mounting_posts__part_0_y, 0], _mounting_posts__part_0);

                _mounting_posts__part_0 = translate([0,0,0], _mounting_posts__part_0);
                let result = _mounting_posts__part_0;
                
            
                    return result;
                }
            
            

                function _mounting_holes_case_fn() {
                    

                // creating part 0 of case _mounting_holes
                let _mounting_holes__part_0 = mounting_holes_extrude_5_outline_fn();

                // make sure that rotations are relative
                let _mounting_holes__part_0_bounds = _mounting_holes__part_0.getBounds();
                let _mounting_holes__part_0_x = _mounting_holes__part_0_bounds[0].x + (_mounting_holes__part_0_bounds[1].x - _mounting_holes__part_0_bounds[0].x) / 2
                let _mounting_holes__part_0_y = _mounting_holes__part_0_bounds[0].y + (_mounting_holes__part_0_bounds[1].y - _mounting_holes__part_0_bounds[0].y) / 2
                _mounting_holes__part_0 = translate([-_mounting_holes__part_0_x, -_mounting_holes__part_0_y, 0], _mounting_holes__part_0);
                _mounting_holes__part_0 = rotate([0,0,0], _mounting_holes__part_0);
                _mounting_holes__part_0 = translate([_mounting_holes__part_0_x, _mounting_holes__part_0_y, 0], _mounting_holes__part_0);

                _mounting_holes__part_0 = translate([0,0,0], _mounting_holes__part_0);
                let result = _mounting_holes__part_0;
                
            
                    return result;
                }
            
            

                function assembly_case_fn() {
                    

                // creating part 0 of case assembly
                let assembly__part_0 = case_bottom_case_fn();

                // make sure that rotations are relative
                let assembly__part_0_bounds = assembly__part_0.getBounds();
                let assembly__part_0_x = assembly__part_0_bounds[0].x + (assembly__part_0_bounds[1].x - assembly__part_0_bounds[0].x) / 2
                let assembly__part_0_y = assembly__part_0_bounds[0].y + (assembly__part_0_bounds[1].y - assembly__part_0_bounds[0].y) / 2
                assembly__part_0 = translate([-assembly__part_0_x, -assembly__part_0_y, 0], assembly__part_0);
                assembly__part_0 = rotate([0,0,0], assembly__part_0);
                assembly__part_0 = translate([assembly__part_0_x, assembly__part_0_y, 0], assembly__part_0);

                assembly__part_0 = translate([0,0,0], assembly__part_0);
                let result = assembly__part_0;
                
            
                    return result;
                }
            
            
        
            function main() {
                return assembly_case_fn();
            }

        