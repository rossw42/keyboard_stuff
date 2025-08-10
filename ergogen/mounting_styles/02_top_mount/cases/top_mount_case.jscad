function case_outline_extrude_1_outline_fn(){
    return new CSG.Path2D([[-15,31.05],[-15,-12]]).appendArc([-12,-15],{"radius":3,"clockwise":false,"large":false}).appendPoint([31.05,-15]).appendArc([34.05,-12],{"radius":3,"clockwise":false,"large":false}).appendPoint([34.05,31.05]).appendArc([31.05,34.05],{"radius":3,"clockwise":false,"large":false}).appendPoint([-12,34.05]).appendArc([-15,31.05],{"radius":3,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 1] });
}


function case_outline_extrude_10_outline_fn(){
    return new CSG.Path2D([[-15,31.05],[-15,-12]]).appendArc([-12,-15],{"radius":3,"clockwise":false,"large":false}).appendPoint([31.05,-15]).appendArc([34.05,-12],{"radius":3,"clockwise":false,"large":false}).appendPoint([34.05,31.05]).appendArc([31.05,34.05],{"radius":3,"clockwise":false,"large":false}).appendPoint([-12,34.05]).appendArc([-15,31.05],{"radius":3,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 10] });
}


function board_extrude_10_outline_fn(){
    return new CSG.Path2D([[-10,27.05],[-10,-8]]).appendArc([-8,-10],{"radius":2,"clockwise":false,"large":false}).appendPoint([27.05,-10]).appendArc([29.05,-8],{"radius":2,"clockwise":false,"large":false}).appendPoint([29.05,27.05]).appendArc([27.05,29.05],{"radius":2,"clockwise":false,"large":false}).appendPoint([-8,29.05]).appendArc([-10,27.05],{"radius":2,"clockwise":false,"large":false}).close().innerToCAG()
.extrude({ offset: [0, 0, 10] });
}


function top_case_with_holes_extrude_2_outline_fn(){
    return new CSG.Path2D([[-15,31.05],[-15,6]]).appendPoint([-18,6]).appendPoint([-18,-6]).appendPoint([-15,-6]).appendPoint([-15,-12]).appendArc([-12,-15],{"radius":3,"clockwise":false,"large":false}).appendPoint([31.05,-15]).appendArc([34.05,-12],{"radius":3,"clockwise":false,"large":false}).appendPoint([34.05,-6]).appendPoint([37.05,-6]).appendPoint([37.05,6]).appendPoint([34.05,6]).appendPoint([34.05,31.05]).appendArc([31.05,34.05],{"radius":3,"clockwise":false,"large":false}).appendPoint([-12,34.05]).appendArc([-15,31.05],{"radius":3,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    CAG.circle({"center":[32.05,0],"radius":1.1})
.union(
    CAG.circle({"center":[-13,0],"radius":1.1})
)).extrude({ offset: [0, 0, 2] });
}




                function bottom_case_fn() {
                    

                // creating part 0 of case bottom
                let bottom__part_0 = case_outline_extrude_1_outline_fn();

                // make sure that rotations are relative
                let bottom__part_0_bounds = bottom__part_0.getBounds();
                let bottom__part_0_x = bottom__part_0_bounds[0].x + (bottom__part_0_bounds[1].x - bottom__part_0_bounds[0].x) / 2
                let bottom__part_0_y = bottom__part_0_bounds[0].y + (bottom__part_0_bounds[1].y - bottom__part_0_bounds[0].y) / 2
                bottom__part_0 = translate([-bottom__part_0_x, -bottom__part_0_y, 0], bottom__part_0);
                bottom__part_0 = rotate([0,0,0], bottom__part_0);
                bottom__part_0 = translate([bottom__part_0_x, bottom__part_0_y, 0], bottom__part_0);

                bottom__part_0 = translate([0,0,0], bottom__part_0);
                let result = bottom__part_0;
                
            
                    return result;
                }
            
            

                function wall_case_fn() {
                    

                // creating part 0 of case wall
                let wall__part_0 = _outerWall_case_fn();

                // make sure that rotations are relative
                let wall__part_0_bounds = wall__part_0.getBounds();
                let wall__part_0_x = wall__part_0_bounds[0].x + (wall__part_0_bounds[1].x - wall__part_0_bounds[0].x) / 2
                let wall__part_0_y = wall__part_0_bounds[0].y + (wall__part_0_bounds[1].y - wall__part_0_bounds[0].y) / 2
                wall__part_0 = translate([-wall__part_0_x, -wall__part_0_y, 0], wall__part_0);
                wall__part_0 = rotate([0,0,0], wall__part_0);
                wall__part_0 = translate([wall__part_0_x, wall__part_0_y, 0], wall__part_0);

                wall__part_0 = translate([0,0,0], wall__part_0);
                let result = wall__part_0;
                
            

                // creating part 1 of case wall
                let wall__part_1 = _innerWall_case_fn();

                // make sure that rotations are relative
                let wall__part_1_bounds = wall__part_1.getBounds();
                let wall__part_1_x = wall__part_1_bounds[0].x + (wall__part_1_bounds[1].x - wall__part_1_bounds[0].x) / 2
                let wall__part_1_y = wall__part_1_bounds[0].y + (wall__part_1_bounds[1].y - wall__part_1_bounds[0].y) / 2
                wall__part_1 = translate([-wall__part_1_x, -wall__part_1_y, 0], wall__part_1);
                wall__part_1 = rotate([0,0,0], wall__part_1);
                wall__part_1 = translate([wall__part_1_x, wall__part_1_y, 0], wall__part_1);

                wall__part_1 = translate([0,0,0], wall__part_1);
                result = result.subtract(wall__part_1);
                
            
                    return result;
                }
            
            

                function _outerWall_case_fn() {
                    

                // creating part 0 of case _outerWall
                let _outerWall__part_0 = case_outline_extrude_10_outline_fn();

                // make sure that rotations are relative
                let _outerWall__part_0_bounds = _outerWall__part_0.getBounds();
                let _outerWall__part_0_x = _outerWall__part_0_bounds[0].x + (_outerWall__part_0_bounds[1].x - _outerWall__part_0_bounds[0].x) / 2
                let _outerWall__part_0_y = _outerWall__part_0_bounds[0].y + (_outerWall__part_0_bounds[1].y - _outerWall__part_0_bounds[0].y) / 2
                _outerWall__part_0 = translate([-_outerWall__part_0_x, -_outerWall__part_0_y, 0], _outerWall__part_0);
                _outerWall__part_0 = rotate([0,0,0], _outerWall__part_0);
                _outerWall__part_0 = translate([_outerWall__part_0_x, _outerWall__part_0_y, 0], _outerWall__part_0);

                _outerWall__part_0 = translate([0,0,0], _outerWall__part_0);
                let result = _outerWall__part_0;
                
            
                    return result;
                }
            
            

                function _innerWall_case_fn() {
                    

                // creating part 0 of case _innerWall
                let _innerWall__part_0 = board_extrude_10_outline_fn();

                // make sure that rotations are relative
                let _innerWall__part_0_bounds = _innerWall__part_0.getBounds();
                let _innerWall__part_0_x = _innerWall__part_0_bounds[0].x + (_innerWall__part_0_bounds[1].x - _innerWall__part_0_bounds[0].x) / 2
                let _innerWall__part_0_y = _innerWall__part_0_bounds[0].y + (_innerWall__part_0_bounds[1].y - _innerWall__part_0_bounds[0].y) / 2
                _innerWall__part_0 = translate([-_innerWall__part_0_x, -_innerWall__part_0_y, 0], _innerWall__part_0);
                _innerWall__part_0 = rotate([0,0,0], _innerWall__part_0);
                _innerWall__part_0 = translate([_innerWall__part_0_x, _innerWall__part_0_y, 0], _innerWall__part_0);

                _innerWall__part_0 = translate([0,0,0], _innerWall__part_0);
                let result = _innerWall__part_0;
                
            
                    return result;
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
            
            

                function top_mount_case_case_fn() {
                    

                // creating part 0 of case top_mount_case
                let top_mount_case__part_0 = bottom_case_fn();

                // make sure that rotations are relative
                let top_mount_case__part_0_bounds = top_mount_case__part_0.getBounds();
                let top_mount_case__part_0_x = top_mount_case__part_0_bounds[0].x + (top_mount_case__part_0_bounds[1].x - top_mount_case__part_0_bounds[0].x) / 2
                let top_mount_case__part_0_y = top_mount_case__part_0_bounds[0].y + (top_mount_case__part_0_bounds[1].y - top_mount_case__part_0_bounds[0].y) / 2
                top_mount_case__part_0 = translate([-top_mount_case__part_0_x, -top_mount_case__part_0_y, 0], top_mount_case__part_0);
                top_mount_case__part_0 = rotate([0,0,0], top_mount_case__part_0);
                top_mount_case__part_0 = translate([top_mount_case__part_0_x, top_mount_case__part_0_y, 0], top_mount_case__part_0);

                top_mount_case__part_0 = translate([0,0,0], top_mount_case__part_0);
                let result = top_mount_case__part_0;
                
            

                // creating part 1 of case top_mount_case
                let top_mount_case__part_1 = wall_case_fn();

                // make sure that rotations are relative
                let top_mount_case__part_1_bounds = top_mount_case__part_1.getBounds();
                let top_mount_case__part_1_x = top_mount_case__part_1_bounds[0].x + (top_mount_case__part_1_bounds[1].x - top_mount_case__part_1_bounds[0].x) / 2
                let top_mount_case__part_1_y = top_mount_case__part_1_bounds[0].y + (top_mount_case__part_1_bounds[1].y - top_mount_case__part_1_bounds[0].y) / 2
                top_mount_case__part_1 = translate([-top_mount_case__part_1_x, -top_mount_case__part_1_y, 0], top_mount_case__part_1);
                top_mount_case__part_1 = rotate([0,0,0], top_mount_case__part_1);
                top_mount_case__part_1 = translate([top_mount_case__part_1_x, top_mount_case__part_1_y, 0], top_mount_case__part_1);

                top_mount_case__part_1 = translate([0,0,0], top_mount_case__part_1);
                result = result.union(top_mount_case__part_1);
                
            

                // creating part 2 of case top_mount_case
                let top_mount_case__part_2 = top_case_case_fn();

                // make sure that rotations are relative
                let top_mount_case__part_2_bounds = top_mount_case__part_2.getBounds();
                let top_mount_case__part_2_x = top_mount_case__part_2_bounds[0].x + (top_mount_case__part_2_bounds[1].x - top_mount_case__part_2_bounds[0].x) / 2
                let top_mount_case__part_2_y = top_mount_case__part_2_bounds[0].y + (top_mount_case__part_2_bounds[1].y - top_mount_case__part_2_bounds[0].y) / 2
                top_mount_case__part_2 = translate([-top_mount_case__part_2_x, -top_mount_case__part_2_y, 0], top_mount_case__part_2);
                top_mount_case__part_2 = rotate([0,0,0], top_mount_case__part_2);
                top_mount_case__part_2 = translate([top_mount_case__part_2_x, top_mount_case__part_2_y, 0], top_mount_case__part_2);

                top_mount_case__part_2 = translate([0,0,10], top_mount_case__part_2);
                result = result.union(top_mount_case__part_2);
                
            
                    return result;
                }
            
            
        
            function main() {
                return top_mount_case_case_fn();
            }

        