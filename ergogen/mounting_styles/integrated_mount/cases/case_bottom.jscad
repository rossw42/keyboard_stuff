function case_walls_extrude_4_outline_fn(){
    return new CSG.Path2D([[-18,37.05],[-18,-18]]).appendArc([-13,-23],{"radius":5,"clockwise":false,"large":false}).appendPoint([70.15,-23]).appendArc([75.15,-18],{"radius":5,"clockwise":false,"large":false}).appendPoint([75.15,37.05]).appendArc([70.15,42.05],{"radius":5,"clockwise":false,"large":false}).appendPoint([-13,42.05]).appendArc([-18,37.05],{"radius":5,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 4] });
}


function case_outline_extrude_4_outline_fn(){
    return new CSG.Path2D([[-15,37.05],[-15,-18]]).appendArc([-13,-20],{"radius":2,"clockwise":false,"large":false}).appendPoint([70.15,-20]).appendArc([72.15,-18],{"radius":2,"clockwise":false,"large":false}).appendPoint([72.15,37.05]).appendArc([70.15,39.05],{"radius":2,"clockwise":false,"large":false}).appendPoint([-13,39.05]).appendArc([-15,37.05],{"radius":2,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 4] });
}


function mounting_posts_extrude_8_outline_fn(){
    return CAG.circle({"center":[133.2,-35],"radius":2.5})
.union(
    CAG.circle({"center":[57.05,-35],"radius":2.5})
).union(
    CAG.circle({"center":[95.2,15],"radius":2.5})
).union(
    CAG.circle({"center":[19.05,15],"radius":2.5})
).extrude({ offset: [0, 0, 8] });
}


function mounting_holes_extrude_12_outline_fn(){
    return CAG.circle({"center":[133.2,-35],"radius":1.1})
.union(
    CAG.circle({"center":[57.05,-35],"radius":1.1})
).union(
    CAG.circle({"center":[95.2,15],"radius":1.1})
).union(
    CAG.circle({"center":[19.05,15],"radius":1.1})
).extrude({ offset: [0, 0, 12] });
}




                function _bottom_outer_case_fn() {
                    

                // creating part 0 of case _bottom_outer
                let _bottom_outer__part_0 = case_walls_extrude_4_outline_fn();

                // make sure that rotations are relative
                let _bottom_outer__part_0_bounds = _bottom_outer__part_0.getBounds();
                let _bottom_outer__part_0_x = _bottom_outer__part_0_bounds[0].x + (_bottom_outer__part_0_bounds[1].x - _bottom_outer__part_0_bounds[0].x) / 2
                let _bottom_outer__part_0_y = _bottom_outer__part_0_bounds[0].y + (_bottom_outer__part_0_bounds[1].y - _bottom_outer__part_0_bounds[0].y) / 2
                _bottom_outer__part_0 = translate([-_bottom_outer__part_0_x, -_bottom_outer__part_0_y, 0], _bottom_outer__part_0);
                _bottom_outer__part_0 = rotate([0,0,0], _bottom_outer__part_0);
                _bottom_outer__part_0 = translate([_bottom_outer__part_0_x, _bottom_outer__part_0_y, 0], _bottom_outer__part_0);

                _bottom_outer__part_0 = translate([0,0,0], _bottom_outer__part_0);
                let result = _bottom_outer__part_0;
                
            
                    return result;
                }
            
            

                function _bottom_inner_case_fn() {
                    

                // creating part 0 of case _bottom_inner
                let _bottom_inner__part_0 = case_outline_extrude_4_outline_fn();

                // make sure that rotations are relative
                let _bottom_inner__part_0_bounds = _bottom_inner__part_0.getBounds();
                let _bottom_inner__part_0_x = _bottom_inner__part_0_bounds[0].x + (_bottom_inner__part_0_bounds[1].x - _bottom_inner__part_0_bounds[0].x) / 2
                let _bottom_inner__part_0_y = _bottom_inner__part_0_bounds[0].y + (_bottom_inner__part_0_bounds[1].y - _bottom_inner__part_0_bounds[0].y) / 2
                _bottom_inner__part_0 = translate([-_bottom_inner__part_0_x, -_bottom_inner__part_0_y, 0], _bottom_inner__part_0);
                _bottom_inner__part_0 = rotate([0,0,0], _bottom_inner__part_0);
                _bottom_inner__part_0 = translate([_bottom_inner__part_0_x, _bottom_inner__part_0_y, 0], _bottom_inner__part_0);

                _bottom_inner__part_0 = translate([0,0,0], _bottom_inner__part_0);
                let result = _bottom_inner__part_0;
                
            
                    return result;
                }
            
            

                function _bottom_mounting_posts_case_fn() {
                    

                // creating part 0 of case _bottom_mounting_posts
                let _bottom_mounting_posts__part_0 = mounting_posts_extrude_8_outline_fn();

                // make sure that rotations are relative
                let _bottom_mounting_posts__part_0_bounds = _bottom_mounting_posts__part_0.getBounds();
                let _bottom_mounting_posts__part_0_x = _bottom_mounting_posts__part_0_bounds[0].x + (_bottom_mounting_posts__part_0_bounds[1].x - _bottom_mounting_posts__part_0_bounds[0].x) / 2
                let _bottom_mounting_posts__part_0_y = _bottom_mounting_posts__part_0_bounds[0].y + (_bottom_mounting_posts__part_0_bounds[1].y - _bottom_mounting_posts__part_0_bounds[0].y) / 2
                _bottom_mounting_posts__part_0 = translate([-_bottom_mounting_posts__part_0_x, -_bottom_mounting_posts__part_0_y, 0], _bottom_mounting_posts__part_0);
                _bottom_mounting_posts__part_0 = rotate([0,0,0], _bottom_mounting_posts__part_0);
                _bottom_mounting_posts__part_0 = translate([_bottom_mounting_posts__part_0_x, _bottom_mounting_posts__part_0_y, 0], _bottom_mounting_posts__part_0);

                _bottom_mounting_posts__part_0 = translate([0,0,0], _bottom_mounting_posts__part_0);
                let result = _bottom_mounting_posts__part_0;
                
            
                    return result;
                }
            
            

                function _bottom_mounting_holes_case_fn() {
                    

                // creating part 0 of case _bottom_mounting_holes
                let _bottom_mounting_holes__part_0 = mounting_holes_extrude_12_outline_fn();

                // make sure that rotations are relative
                let _bottom_mounting_holes__part_0_bounds = _bottom_mounting_holes__part_0.getBounds();
                let _bottom_mounting_holes__part_0_x = _bottom_mounting_holes__part_0_bounds[0].x + (_bottom_mounting_holes__part_0_bounds[1].x - _bottom_mounting_holes__part_0_bounds[0].x) / 2
                let _bottom_mounting_holes__part_0_y = _bottom_mounting_holes__part_0_bounds[0].y + (_bottom_mounting_holes__part_0_bounds[1].y - _bottom_mounting_holes__part_0_bounds[0].y) / 2
                _bottom_mounting_holes__part_0 = translate([-_bottom_mounting_holes__part_0_x, -_bottom_mounting_holes__part_0_y, 0], _bottom_mounting_holes__part_0);
                _bottom_mounting_holes__part_0 = rotate([0,0,0], _bottom_mounting_holes__part_0);
                _bottom_mounting_holes__part_0 = translate([_bottom_mounting_holes__part_0_x, _bottom_mounting_holes__part_0_y, 0], _bottom_mounting_holes__part_0);

                _bottom_mounting_holes__part_0 = translate([0,0,0], _bottom_mounting_holes__part_0);
                let result = _bottom_mounting_holes__part_0;
                
            
                    return result;
                }
            
            

                function case_bottom_case_fn() {
                    

                // creating part 0 of case case_bottom
                let case_bottom__part_0 = _bottom_outer_case_fn();

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
                let case_bottom__part_1 = _bottom_inner_case_fn();

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
                let case_bottom__part_2 = _bottom_mounting_posts_case_fn();

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
                let case_bottom__part_3 = _bottom_mounting_holes_case_fn();

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
            
            
        
            function main() {
                return case_bottom_case_fn();
            }

        