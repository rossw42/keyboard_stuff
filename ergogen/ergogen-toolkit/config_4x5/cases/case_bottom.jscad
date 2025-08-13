function case_outline_extrude_10_outline_fn(){
    return new CSG.Path2D([[169.3240141,77.25],[175.6875,77.25]]).appendArc([180.6875,82.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([180.6875,100.25]).appendArc([175.6875,105.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([173.2885069,105.25]).appendArc([173.4,106.3],{"radius":5,"clockwise":false,"large":false}).appendPoint([173.4,122.3]).appendArc([168.4,127.3],{"radius":5,"clockwise":false,"large":false}).appendPoint([136.4,127.3]).appendArc([131.4,122.3],{"radius":5,"clockwise":false,"large":false}).appendPoint([131.4,106.3]).appendArc([131.5114931,105.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([129.1125,105.25]).appendArc([124.1125,100.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([124.1125,82.25]).appendArc([129.1125,77.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([135.4759859,77.25]).appendArc([138.4474912,73.8375],{"radius":3,"clockwise":true,"large":false}).appendArc([138.4,73.15],{"radius":5,"clockwise":false,"large":false}).appendPoint([138.4,55.15]).appendArc([138.7230661,53.3818684],{"radius":5,"clockwise":false,"large":false}).appendArc([133.9,48.385],{"radius":5,"clockwise":false,"large":false}).appendPoint([133.9,30.385]).appendArc([138.9,25.385],{"radius":5,"clockwise":false,"large":false}).appendPoint([165.9,25.385]).appendArc([170.9,30.385],{"radius":5,"clockwise":false,"large":false}).appendPoint([170.9,48.385]).appendArc([166.0769339,53.3818685],{"radius":5,"clockwise":false,"large":false}).appendArc([166.4,55.15],{"radius":5,"clockwise":false,"large":false}).appendPoint([166.4,73.15]).appendArc([166.3525088,73.8375],{"radius":5,"clockwise":false,"large":false}).appendArc([169.3240141,77.25],{"radius":3,"clockwise":true,"large":false}).close().innerToCAG()
.subtract(
    new CSG.Path2D([[152.6875,100.25],[152.6875,82.25]]).appendArc([154.8256824,78.15],{"radius":5,"clockwise":false,"large":false}).appendPoint([149.9743176,78.15]).appendArc([152.1125,82.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([152.1125,100.25]).appendArc([152.0010069,101.3],{"radius":5,"clockwise":false,"large":false}).appendPoint([152.7989931,101.3]).appendArc([152.6875,100.25],{"radius":5,"clockwise":false,"large":false}).close().innerToCAG()
).extrude({ offset: [0, 0, 10] });
}




                function case_bottom_case_fn() {
                    

                // creating part 0 of case case_bottom
                let case_bottom__part_0 = case_outline_extrude_10_outline_fn();

                // make sure that rotations are relative
                let case_bottom__part_0_bounds = case_bottom__part_0.getBounds();
                let case_bottom__part_0_x = case_bottom__part_0_bounds[0].x + (case_bottom__part_0_bounds[1].x - case_bottom__part_0_bounds[0].x) / 2
                let case_bottom__part_0_y = case_bottom__part_0_bounds[0].y + (case_bottom__part_0_bounds[1].y - case_bottom__part_0_bounds[0].y) / 2
                case_bottom__part_0 = translate([-case_bottom__part_0_x, -case_bottom__part_0_y, 0], case_bottom__part_0);
                case_bottom__part_0 = rotate([0,0,0], case_bottom__part_0);
                case_bottom__part_0 = translate([case_bottom__part_0_x, case_bottom__part_0_y, 0], case_bottom__part_0);

                case_bottom__part_0 = translate([0,0,0], case_bottom__part_0);
                let result = case_bottom__part_0;
                
            
                    return result;
                }
            
            
        
            function main() {
                return case_bottom_case_fn();
            }

        