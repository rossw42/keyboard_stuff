function bottom_outline_extrude_2_outline_fn(){
    return new CSG.Path2D([[-15,37.05],[-15,-18]]).appendArc([-13,-20],{"radius":2,"clockwise":false,"large":false}).appendPoint([70.15,-20]).appendArc([72.15,-18],{"radius":2,"clockwise":false,"large":false}).appendPoint([72.15,37.05]).appendArc([70.15,39.05],{"radius":2,"clockwise":false,"large":false}).appendPoint([-13,39.05]).appendArc([-15,37.05],{"radius":2,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 2] });
}


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


function case_walls_extrude_12_outline_fn(){
    return new CSG.Path2D([[-18,37.05],[-18,-18]]).appendArc([-13,-23],{"radius":5,"clockwise":false,"large":false}).appendPoint([70.15,-23]).appendArc([75.15,-18],{"radius":5,"clockwise":false,"large":false}).appendPoint([75.15,37.05]).appendArc([70.15,42.05],{"radius":5,"clockwise":false,"large":false}).appendPoint([-13,42.05]).appendArc([-18,37.05],{"radius":5,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 12] });
}


function case_outline_extrude_12_outline_fn(){
    return new CSG.Path2D([[-15,37.05],[-15,-18]]).appendArc([-13,-20],{"radius":2,"clockwise":false,"large":false}).appendPoint([70.15,-20]).appendArc([72.15,-18],{"radius":2,"clockwise":false,"large":false}).appendPoint([72.15,37.05]).appendArc([70.15,39.05],{"radius":2,"clockwise":false,"large":false}).appendPoint([-13,39.05]).appendArc([-15,37.05],{"radius":2,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 12] });
}


function switch_wells_extrude_5_outline_fn(){
    return new CSG.Path2D([[30.1,11.05],[46.1,11.05]]).appendPoint([46.1,27.05]).appendPoint([30.1,27.05]).appendPoint([30.1,11.05]).close().innerToCAG()
.union(
    new CSG.Path2D([[30.1,-8],[46.1,-8]]).appendPoint([46.1,8]).appendPoint([30.1,8]).appendPoint([30.1,-8]).close().innerToCAG()
).union(
    new CSG.Path2D([[11.05,11.05],[27.05,11.05]]).appendPoint([27.05,27.05]).appendPoint([11.05,27.05]).appendPoint([11.05,11.05]).close().innerToCAG()
).union(
    new CSG.Path2D([[11.05,-8],[27.05,-8]]).appendPoint([27.05,8]).appendPoint([11.05,8]).appendPoint([11.05,-8]).close().innerToCAG()
).union(
    new CSG.Path2D([[-8,11.05],[8,11.05]]).appendPoint([8,27.05]).appendPoint([-8,27.05]).appendPoint([-8,11.05]).close().innerToCAG()
).union(
    new CSG.Path2D([[-8,-8],[8,-8]]).appendPoint([8,8]).appendPoint([-8,8]).appendPoint([-8,-8]).close().innerToCAG()
).union(
    new CSG.Path2D([[49.15,11.05],[65.15,11.05]]).appendPoint([65.15,27.05]).appendPoint([49.15,27.05]).appendPoint([49.15,11.05]).close().innerToCAG()
).union(
    new CSG.Path2D([[49.15,-8],[65.15,-8]]).appendPoint([65.15,8]).appendPoint([49.15,8]).appendPoint([49.15,-8]).close().innerToCAG()
).extrude({ offset: [0, 0, 5] });
}


function switch_cutouts_extrude_13_outline_fn(){
    return new CSG.Path2D([[31.1,12.05],[45.1,12.05]]).appendPoint([45.1,26.05]).appendPoint([31.1,26.05]).appendPoint([31.1,12.05]).close().innerToCAG()
.union(
    new CSG.Path2D([[31.1,-7],[45.1,-7]]).appendPoint([45.1,7]).appendPoint([31.1,7]).appendPoint([31.1,-7]).close().innerToCAG()
).union(
    new CSG.Path2D([[12.05,12.05],[26.05,12.05]]).appendPoint([26.05,26.05]).appendPoint([12.05,26.05]).appendPoint([12.05,12.05]).close().innerToCAG()
).union(
    new CSG.Path2D([[12.05,-7],[26.05,-7]]).appendPoint([26.05,7]).appendPoint([12.05,7]).appendPoint([12.05,-7]).close().innerToCAG()
).union(
    new CSG.Path2D([[-7,12.05],[7,12.05]]).appendPoint([7,26.05]).appendPoint([-7,26.05]).appendPoint([-7,12.05]).close().innerToCAG()
).union(
    new CSG.Path2D([[-7,-7],[7,-7]]).appendPoint([7,7]).appendPoint([-7,7]).appendPoint([-7,-7]).close().innerToCAG()
).union(
    new CSG.Path2D([[50.15,12.05],[64.15,12.05]]).appendPoint([64.15,26.05]).appendPoint([50.15,26.05]).appendPoint([50.15,12.05]).close().innerToCAG()
).union(
    new CSG.Path2D([[50.15,-7],[64.15,-7]]).appendPoint([64.15,7]).appendPoint([50.15,7]).appendPoint([50.15,-7]).close().innerToCAG()
).extrude({ offset: [0, 0, 13] });
}


function mounting_holes_extrude_13_outline_fn(){
    return CAG.circle({"center":[133.2,-35],"radius":1.1})
.union(
    CAG.circle({"center":[57.05,-35],"radius":1.1})
).union(
    CAG.circle({"center":[95.2,15],"radius":1.1})
).union(
    CAG.circle({"center":[19.05,15],"radius":1.1})
).extrude({ offset: [0, 0, 13] });
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
            
            

                function case_top_integrated_case_fn() {
                    

                // creating part 0 of case case_top_integrated
                let case_top_integrated__part_0 = _top_outer_case_fn();

                // make sure that rotations are relative
                let case_top_integrated__part_0_bounds = case_top_integrated__part_0.getBounds();
                let case_top_integrated__part_0_x = case_top_integrated__part_0_bounds[0].x + (case_top_integrated__part_0_bounds[1].x - case_top_integrated__part_0_bounds[0].x) / 2
                let case_top_integrated__part_0_y = case_top_integrated__part_0_bounds[0].y + (case_top_integrated__part_0_bounds[1].y - case_top_integrated__part_0_bounds[0].y) / 2
                case_top_integrated__part_0 = translate([-case_top_integrated__part_0_x, -case_top_integrated__part_0_y, 0], case_top_integrated__part_0);
                case_top_integrated__part_0 = rotate([0,0,0], case_top_integrated__part_0);
                case_top_integrated__part_0 = translate([case_top_integrated__part_0_x, case_top_integrated__part_0_y, 0], case_top_integrated__part_0);

                case_top_integrated__part_0 = translate([0,0,0], case_top_integrated__part_0);
                let result = case_top_integrated__part_0;
                
            

                // creating part 1 of case case_top_integrated
                let case_top_integrated__part_1 = _top_inner_case_fn();

                // make sure that rotations are relative
                let case_top_integrated__part_1_bounds = case_top_integrated__part_1.getBounds();
                let case_top_integrated__part_1_x = case_top_integrated__part_1_bounds[0].x + (case_top_integrated__part_1_bounds[1].x - case_top_integrated__part_1_bounds[0].x) / 2
                let case_top_integrated__part_1_y = case_top_integrated__part_1_bounds[0].y + (case_top_integrated__part_1_bounds[1].y - case_top_integrated__part_1_bounds[0].y) / 2
                case_top_integrated__part_1 = translate([-case_top_integrated__part_1_x, -case_top_integrated__part_1_y, 0], case_top_integrated__part_1);
                case_top_integrated__part_1 = rotate([0,0,0], case_top_integrated__part_1);
                case_top_integrated__part_1 = translate([case_top_integrated__part_1_x, case_top_integrated__part_1_y, 0], case_top_integrated__part_1);

                case_top_integrated__part_1 = translate([0,0,0], case_top_integrated__part_1);
                result = result.subtract(case_top_integrated__part_1);
                
            

                // creating part 2 of case case_top_integrated
                let case_top_integrated__part_2 = _switch_wells_case_fn();

                // make sure that rotations are relative
                let case_top_integrated__part_2_bounds = case_top_integrated__part_2.getBounds();
                let case_top_integrated__part_2_x = case_top_integrated__part_2_bounds[0].x + (case_top_integrated__part_2_bounds[1].x - case_top_integrated__part_2_bounds[0].x) / 2
                let case_top_integrated__part_2_y = case_top_integrated__part_2_bounds[0].y + (case_top_integrated__part_2_bounds[1].y - case_top_integrated__part_2_bounds[0].y) / 2
                case_top_integrated__part_2 = translate([-case_top_integrated__part_2_x, -case_top_integrated__part_2_y, 0], case_top_integrated__part_2);
                case_top_integrated__part_2 = rotate([0,0,0], case_top_integrated__part_2);
                case_top_integrated__part_2 = translate([case_top_integrated__part_2_x, case_top_integrated__part_2_y, 0], case_top_integrated__part_2);

                case_top_integrated__part_2 = translate([0,0,0], case_top_integrated__part_2);
                result = result.subtract(case_top_integrated__part_2);
                
            

                // creating part 3 of case case_top_integrated
                let case_top_integrated__part_3 = _switch_cutouts_case_fn();

                // make sure that rotations are relative
                let case_top_integrated__part_3_bounds = case_top_integrated__part_3.getBounds();
                let case_top_integrated__part_3_x = case_top_integrated__part_3_bounds[0].x + (case_top_integrated__part_3_bounds[1].x - case_top_integrated__part_3_bounds[0].x) / 2
                let case_top_integrated__part_3_y = case_top_integrated__part_3_bounds[0].y + (case_top_integrated__part_3_bounds[1].y - case_top_integrated__part_3_bounds[0].y) / 2
                case_top_integrated__part_3 = translate([-case_top_integrated__part_3_x, -case_top_integrated__part_3_y, 0], case_top_integrated__part_3);
                case_top_integrated__part_3 = rotate([0,0,0], case_top_integrated__part_3);
                case_top_integrated__part_3 = translate([case_top_integrated__part_3_x, case_top_integrated__part_3_y, 0], case_top_integrated__part_3);

                case_top_integrated__part_3 = translate([0,0,0], case_top_integrated__part_3);
                result = result.subtract(case_top_integrated__part_3);
                
            

                // creating part 4 of case case_top_integrated
                let case_top_integrated__part_4 = _mounting_holes_case_fn();

                // make sure that rotations are relative
                let case_top_integrated__part_4_bounds = case_top_integrated__part_4.getBounds();
                let case_top_integrated__part_4_x = case_top_integrated__part_4_bounds[0].x + (case_top_integrated__part_4_bounds[1].x - case_top_integrated__part_4_bounds[0].x) / 2
                let case_top_integrated__part_4_y = case_top_integrated__part_4_bounds[0].y + (case_top_integrated__part_4_bounds[1].y - case_top_integrated__part_4_bounds[0].y) / 2
                case_top_integrated__part_4 = translate([-case_top_integrated__part_4_x, -case_top_integrated__part_4_y, 0], case_top_integrated__part_4);
                case_top_integrated__part_4 = rotate([0,0,0], case_top_integrated__part_4);
                case_top_integrated__part_4 = translate([case_top_integrated__part_4_x, case_top_integrated__part_4_y, 0], case_top_integrated__part_4);

                case_top_integrated__part_4 = translate([0,0,0], case_top_integrated__part_4);
                result = result.subtract(case_top_integrated__part_4);
                
            
                    return result;
                }
            
            

                function _top_outer_case_fn() {
                    

                // creating part 0 of case _top_outer
                let _top_outer__part_0 = case_walls_extrude_12_outline_fn();

                // make sure that rotations are relative
                let _top_outer__part_0_bounds = _top_outer__part_0.getBounds();
                let _top_outer__part_0_x = _top_outer__part_0_bounds[0].x + (_top_outer__part_0_bounds[1].x - _top_outer__part_0_bounds[0].x) / 2
                let _top_outer__part_0_y = _top_outer__part_0_bounds[0].y + (_top_outer__part_0_bounds[1].y - _top_outer__part_0_bounds[0].y) / 2
                _top_outer__part_0 = translate([-_top_outer__part_0_x, -_top_outer__part_0_y, 0], _top_outer__part_0);
                _top_outer__part_0 = rotate([0,0,0], _top_outer__part_0);
                _top_outer__part_0 = translate([_top_outer__part_0_x, _top_outer__part_0_y, 0], _top_outer__part_0);

                _top_outer__part_0 = translate([0,0,0], _top_outer__part_0);
                let result = _top_outer__part_0;
                
            
                    return result;
                }
            
            

                function _top_inner_case_fn() {
                    

                // creating part 0 of case _top_inner
                let _top_inner__part_0 = case_outline_extrude_12_outline_fn();

                // make sure that rotations are relative
                let _top_inner__part_0_bounds = _top_inner__part_0.getBounds();
                let _top_inner__part_0_x = _top_inner__part_0_bounds[0].x + (_top_inner__part_0_bounds[1].x - _top_inner__part_0_bounds[0].x) / 2
                let _top_inner__part_0_y = _top_inner__part_0_bounds[0].y + (_top_inner__part_0_bounds[1].y - _top_inner__part_0_bounds[0].y) / 2
                _top_inner__part_0 = translate([-_top_inner__part_0_x, -_top_inner__part_0_y, 0], _top_inner__part_0);
                _top_inner__part_0 = rotate([0,0,0], _top_inner__part_0);
                _top_inner__part_0 = translate([_top_inner__part_0_x, _top_inner__part_0_y, 0], _top_inner__part_0);

                _top_inner__part_0 = translate([0,0,0], _top_inner__part_0);
                let result = _top_inner__part_0;
                
            
                    return result;
                }
            
            

                function _switch_wells_case_fn() {
                    

                // creating part 0 of case _switch_wells
                let _switch_wells__part_0 = switch_wells_extrude_5_outline_fn();

                // make sure that rotations are relative
                let _switch_wells__part_0_bounds = _switch_wells__part_0.getBounds();
                let _switch_wells__part_0_x = _switch_wells__part_0_bounds[0].x + (_switch_wells__part_0_bounds[1].x - _switch_wells__part_0_bounds[0].x) / 2
                let _switch_wells__part_0_y = _switch_wells__part_0_bounds[0].y + (_switch_wells__part_0_bounds[1].y - _switch_wells__part_0_bounds[0].y) / 2
                _switch_wells__part_0 = translate([-_switch_wells__part_0_x, -_switch_wells__part_0_y, 0], _switch_wells__part_0);
                _switch_wells__part_0 = rotate([0,0,0], _switch_wells__part_0);
                _switch_wells__part_0 = translate([_switch_wells__part_0_x, _switch_wells__part_0_y, 0], _switch_wells__part_0);

                _switch_wells__part_0 = translate([0,0,0], _switch_wells__part_0);
                let result = _switch_wells__part_0;
                
            
                    return result;
                }
            
            

                function _switch_cutouts_case_fn() {
                    

                // creating part 0 of case _switch_cutouts
                let _switch_cutouts__part_0 = switch_cutouts_extrude_13_outline_fn();

                // make sure that rotations are relative
                let _switch_cutouts__part_0_bounds = _switch_cutouts__part_0.getBounds();
                let _switch_cutouts__part_0_x = _switch_cutouts__part_0_bounds[0].x + (_switch_cutouts__part_0_bounds[1].x - _switch_cutouts__part_0_bounds[0].x) / 2
                let _switch_cutouts__part_0_y = _switch_cutouts__part_0_bounds[0].y + (_switch_cutouts__part_0_bounds[1].y - _switch_cutouts__part_0_bounds[0].y) / 2
                _switch_cutouts__part_0 = translate([-_switch_cutouts__part_0_x, -_switch_cutouts__part_0_y, 0], _switch_cutouts__part_0);
                _switch_cutouts__part_0 = rotate([0,0,0], _switch_cutouts__part_0);
                _switch_cutouts__part_0 = translate([_switch_cutouts__part_0_x, _switch_cutouts__part_0_y, 0], _switch_cutouts__part_0);

                _switch_cutouts__part_0 = translate([0,0,0], _switch_cutouts__part_0);
                let result = _switch_cutouts__part_0;
                
            
                    return result;
                }
            
            

                function _mounting_holes_case_fn() {
                    

                // creating part 0 of case _mounting_holes
                let _mounting_holes__part_0 = mounting_holes_extrude_13_outline_fn();

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
                let assembly__part_0 = case_base_case_fn();

                // make sure that rotations are relative
                let assembly__part_0_bounds = assembly__part_0.getBounds();
                let assembly__part_0_x = assembly__part_0_bounds[0].x + (assembly__part_0_bounds[1].x - assembly__part_0_bounds[0].x) / 2
                let assembly__part_0_y = assembly__part_0_bounds[0].y + (assembly__part_0_bounds[1].y - assembly__part_0_bounds[0].y) / 2
                assembly__part_0 = translate([-assembly__part_0_x, -assembly__part_0_y, 0], assembly__part_0);
                assembly__part_0 = rotate([0,0,0], assembly__part_0);
                assembly__part_0 = translate([assembly__part_0_x, assembly__part_0_y, 0], assembly__part_0);

                assembly__part_0 = translate([0,0,0], assembly__part_0);
                let result = assembly__part_0;
                
            

                // creating part 1 of case assembly
                let assembly__part_1 = case_bottom_case_fn();

                // make sure that rotations are relative
                let assembly__part_1_bounds = assembly__part_1.getBounds();
                let assembly__part_1_x = assembly__part_1_bounds[0].x + (assembly__part_1_bounds[1].x - assembly__part_1_bounds[0].x) / 2
                let assembly__part_1_y = assembly__part_1_bounds[0].y + (assembly__part_1_bounds[1].y - assembly__part_1_bounds[0].y) / 2
                assembly__part_1 = translate([-assembly__part_1_x, -assembly__part_1_y, 0], assembly__part_1);
                assembly__part_1 = rotate([0,0,0], assembly__part_1);
                assembly__part_1 = translate([assembly__part_1_x, assembly__part_1_y, 0], assembly__part_1);

                assembly__part_1 = translate([0,0,2], assembly__part_1);
                result = result.union(assembly__part_1);
                
            

                // creating part 2 of case assembly
                let assembly__part_2 = case_top_integrated_case_fn();

                // make sure that rotations are relative
                let assembly__part_2_bounds = assembly__part_2.getBounds();
                let assembly__part_2_x = assembly__part_2_bounds[0].x + (assembly__part_2_bounds[1].x - assembly__part_2_bounds[0].x) / 2
                let assembly__part_2_y = assembly__part_2_bounds[0].y + (assembly__part_2_bounds[1].y - assembly__part_2_bounds[0].y) / 2
                assembly__part_2 = translate([-assembly__part_2_x, -assembly__part_2_y, 0], assembly__part_2);
                assembly__part_2 = rotate([0,0,0], assembly__part_2);
                assembly__part_2 = translate([assembly__part_2_x, assembly__part_2_y, 0], assembly__part_2);

                assembly__part_2 = translate([0,0,6], assembly__part_2);
                result = result.union(assembly__part_2);
                
            
                    return result;
                }
            
            
        
            function main() {
                return assembly_case_fn();
            }

        