function case_outline_extrude_10_outline_fn(){
    return new CSG.Path2D([[128.3,19.625],[128.3,78.3164573]]).appendArc([129.1125,78.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([135.4759859,78.25]).appendArc([138.4474912,74.8375],{"radius":3,"clockwise":true,"large":false}).appendArc([138.4,74.15],{"radius":5,"clockwise":false,"large":false}).appendPoint([138.4,56.15]).appendArc([140.0042527,52.48],{"radius":5,"clockwise":false,"large":false}).appendPoint([138.9,52.48]).appendArc([133.9,47.48],{"radius":5,"clockwise":false,"large":false}).appendPoint([133.9,29.48]).appendArc([138.9,24.48],{"radius":5,"clockwise":false,"large":false}).appendPoint([165.9,24.48]).appendArc([170.9,29.48],{"radius":5,"clockwise":false,"large":false}).appendPoint([170.9,47.48]).appendArc([165.9,52.48],{"radius":5,"clockwise":false,"large":false}).appendPoint([164.7957473,52.48]).appendArc([166.4,56.15],{"radius":5,"clockwise":false,"large":false}).appendPoint([166.4,74.15]).appendArc([166.3525088,74.8375],{"radius":5,"clockwise":false,"large":false}).appendArc([169.3240141,78.25],{"radius":3,"clockwise":true,"large":false}).appendPoint([175.6875,78.25]).appendArc([180.6875,83.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([180.6875,101.25]).appendArc([175.6875,106.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([173.2885069,106.25]).appendArc([173.4,107.3],{"radius":5,"clockwise":false,"large":false}).appendPoint([173.4,123.3]).appendArc([168.4,128.3],{"radius":5,"clockwise":false,"large":false}).appendPoint([136.4,128.3]).appendArc([131.4,123.3],{"radius":5,"clockwise":false,"large":false}).appendPoint([131.4,107.3]).appendArc([131.5114931,106.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([129.1125,106.25]).appendArc([128.3,106.1835427],{"radius":5,"clockwise":false,"large":false}).appendPoint([128.3,132.775]).appendArc([123.3,137.775],{"radius":5,"clockwise":false,"large":false}).appendPoint([95.3,137.775]).appendArc([90.3,132.775],{"radius":5,"clockwise":false,"large":false}).appendPoint([90.3,19.625]).appendArc([95.3,14.625],{"radius":5,"clockwise":false,"large":false}).appendPoint([123.3,14.625]).appendArc([128.3,19.625],{"radius":5,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    new CSG.Path2D([[152.6875,101.25],[152.6875,83.25]]).appendArc([154.8256824,79.15],{"radius":5,"clockwise":false,"large":false}).appendPoint([149.9743176,79.15]).appendArc([152.1125,83.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([152.1125,101.25]).appendArc([152.0010069,102.3],{"radius":5,"clockwise":false,"large":false}).appendPoint([152.7989931,102.3]).appendArc([152.6875,101.25],{"radius":5,"clockwise":false,"large":false}).close().innerToCAG()
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

        