function case_outline_extrude_10_outline_fn(){
    return new CSG.Path2D([[47.625,23.575],[87.3,23.575]]).appendArc([90.3,20.575],{"radius":3,"clockwise":true,"large":false}).appendPoint([90.3,19.625]).appendArc([95.3,14.625],{"radius":5,"clockwise":false,"large":false}).appendPoint([123.3,14.625]).appendArc([128.3,19.625],{"radius":5,"clockwise":false,"large":false}).appendPoint([128.3,26.3446693]).appendArc([128.825,28.575],{"radius":5,"clockwise":false,"large":false}).appendPoint([128.825,77.2582725]).appendArc([129.1125,77.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([135.4759859,77.25]).appendArc([138.4474912,73.8375],{"radius":3,"clockwise":true,"large":false}).appendArc([138.4,73.15],{"radius":5,"clockwise":false,"large":false}).appendPoint([138.4,55.15]).appendArc([138.7230661,53.3818684],{"radius":5,"clockwise":false,"large":false}).appendArc([133.9,48.385],{"radius":5,"clockwise":false,"large":false}).appendPoint([133.9,30.385]).appendArc([138.9,25.385],{"radius":5,"clockwise":false,"large":false}).appendPoint([165.9,25.385]).appendArc([170.9,30.385],{"radius":5,"clockwise":false,"large":false}).appendPoint([170.9,48.385]).appendArc([166.0769339,53.3818685],{"radius":5,"clockwise":false,"large":false}).appendArc([166.4,55.15],{"radius":5,"clockwise":false,"large":false}).appendPoint([166.4,73.15]).appendArc([166.3525088,73.8375],{"radius":5,"clockwise":false,"large":false}).appendArc([169.3240141,77.25],{"radius":3,"clockwise":true,"large":false}).appendPoint([175.6875,77.25]).appendArc([180.6875,82.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([180.6875,100.25]).appendArc([175.6875,105.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([173.2885069,105.25]).appendArc([173.4,106.3],{"radius":5,"clockwise":false,"large":false}).appendPoint([173.4,122.3]).appendArc([168.4,127.3],{"radius":5,"clockwise":false,"large":false}).appendPoint([136.4,127.3]).appendArc([131.4,122.3],{"radius":5,"clockwise":false,"large":false}).appendPoint([131.4,106.3]).appendArc([131.5114931,105.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([129.1125,105.25]).appendArc([128.825,105.2417275],{"radius":5,"clockwise":false,"large":false}).appendPoint([128.825,123.825]).appendArc([128.3,126.0553307],{"radius":5,"clockwise":false,"large":false}).appendPoint([128.3,132.775]).appendArc([123.3,137.775],{"radius":5,"clockwise":false,"large":false}).appendPoint([95.3,137.775]).appendArc([90.3,132.775],{"radius":5,"clockwise":false,"large":false}).appendPoint([90.3,131.825]).appendArc([87.3,128.825],{"radius":3,"clockwise":true,"large":false}).appendPoint([47.625,128.825]).appendArc([42.625,123.825],{"radius":5,"clockwise":false,"large":false}).appendPoint([42.625,28.575]).appendArc([47.625,23.575],{"radius":5,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    new CSG.Path2D([[152.6875,100.25],[152.6875,82.25]]).appendArc([154.8256824,78.15],{"radius":5,"clockwise":false,"large":false}).appendPoint([149.9743176,78.15]).appendArc([152.1125,82.25],{"radius":5,"clockwise":false,"large":false}).appendPoint([152.1125,100.25]).appendArc([152.0010069,101.3],{"radius":5,"clockwise":false,"large":false}).appendPoint([152.7989931,101.3]).appendArc([152.6875,100.25],{"radius":5,"clockwise":false,"large":false}).close().innerToCAG()
.union(
    new CSG.Path2D([[103.3,33.575],[115.3,33.575]]).appendArc([118.3,36.575],{"radius":3,"clockwise":false,"large":false}).appendPoint([118.3,115.825]).appendArc([115.3,118.825],{"radius":3,"clockwise":false,"large":false}).appendPoint([103.3,118.825]).appendArc([100.3,115.825],{"radius":3,"clockwise":false,"large":false}).appendPoint([100.3,36.575]).appendArc([103.3,33.575],{"radius":3,"clockwise":false,"large":false}).close().innerToCAG()
)).extrude({ offset: [0, 0, 10] });
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

        