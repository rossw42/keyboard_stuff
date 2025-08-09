function switchplate_extrude_1_6_outline_fn(){
    return new CSG.Path2D([[143.4,56.15],[161.4,56.15]]).appendPoint([161.4,74.15]).appendPoint([143.4,74.15]).appendPoint([143.4,56.15]).close().innerToCAG()
.subtract(
    CAG.circle({"center":[152.4,65.15],"radius":3.5})
).union(
    new CSG.Path2D([[129.1125,83.25],[147.1125,83.25]]).appendPoint([147.1125,101.25]).appendPoint([129.1125,101.25]).appendPoint([129.1125,83.25]).close().innerToCAG()
.subtract(
    CAG.circle({"center":[138.1125,92.25],"radius":3.5})
)).union(
    new CSG.Path2D([[157.6875,83.25],[175.6875,83.25]]).appendPoint([175.6875,101.25]).appendPoint([157.6875,101.25]).appendPoint([157.6875,83.25]).close().innerToCAG()
.subtract(
    CAG.circle({"center":[166.6875,92.25],"radius":3.5})
)).union(
    new CSG.Path2D([[138.9,29.48],[165.9,29.48]]).appendPoint([165.9,47.48]).appendPoint([138.9,47.48]).appendPoint([138.9,29.48]).close().innerToCAG()
.subtract(
    new CSG.Path2D([[145.4,31.48],[159.4,31.48]]).appendPoint([159.4,45.48]).appendPoint([145.4,45.48]).appendPoint([145.4,31.48]).close().innerToCAG()
)).union(
    new CSG.Path2D([[136.4,107.3],[168.4,107.3]]).appendPoint([168.4,123.3]).appendPoint([136.4,123.3]).appendPoint([136.4,107.3]).close().innerToCAG()
.subtract(
    new CSG.Path2D([[138.4,107.8],[166.4,107.8]]).appendPoint([166.4,122.8]).appendPoint([138.4,122.8]).appendPoint([138.4,107.8]).close().innerToCAG()
)).union(
    new CSG.Path2D([[123.3,19.625],[123.3,132.775]]).appendPoint([95.3,132.775]).appendPoint([95.3,121.3]).appendPoint([102.25,121.3]).appendPoint([102.25,107.3]).appendPoint([95.3,107.3]).appendPoint([95.3,102.25]).appendPoint([102.25,102.25]).appendPoint([102.25,88.25]).appendPoint([95.3,88.25]).appendPoint([95.3,83.2]).appendPoint([102.25,83.2]).appendPoint([102.25,69.2]).appendPoint([95.3,69.2]).appendPoint([95.3,64.15]).appendPoint([102.25,64.15]).appendPoint([102.25,50.15]).appendPoint([95.3,50.15]).appendPoint([95.3,45.1]).appendPoint([102.25,45.1]).appendPoint([102.25,31.1]).appendPoint([95.3,31.1]).appendPoint([95.3,19.625]).appendPoint([123.3,19.625]).close().innerToCAG()
.subtract(
    new CSG.Path2D([[107.3,107.3],[121.3,107.3]]).appendPoint([121.3,121.3]).appendPoint([107.3,121.3]).appendPoint([107.3,107.3]).close().innerToCAG()
.union(
    new CSG.Path2D([[107.3,88.25],[121.3,88.25]]).appendPoint([121.3,102.25]).appendPoint([107.3,102.25]).appendPoint([107.3,88.25]).close().innerToCAG()
).union(
    new CSG.Path2D([[107.3,69.2],[121.3,69.2]]).appendPoint([121.3,83.2]).appendPoint([107.3,83.2]).appendPoint([107.3,69.2]).close().innerToCAG()
).union(
    new CSG.Path2D([[107.3,50.15],[121.3,50.15]]).appendPoint([121.3,64.15]).appendPoint([107.3,64.15]).appendPoint([107.3,50.15]).close().innerToCAG()
).union(
    new CSG.Path2D([[107.3,31.1],[121.3,31.1]]).appendPoint([121.3,45.1]).appendPoint([107.3,45.1]).appendPoint([107.3,31.1]).close().innerToCAG()
))).extrude({ offset: [0, 0, 1.6] });
}




                function case_top_case_fn() {
                    

                // creating part 0 of case case_top
                let case_top__part_0 = switchplate_extrude_1_6_outline_fn();

                // make sure that rotations are relative
                let case_top__part_0_bounds = case_top__part_0.getBounds();
                let case_top__part_0_x = case_top__part_0_bounds[0].x + (case_top__part_0_bounds[1].x - case_top__part_0_bounds[0].x) / 2
                let case_top__part_0_y = case_top__part_0_bounds[0].y + (case_top__part_0_bounds[1].y - case_top__part_0_bounds[0].y) / 2
                case_top__part_0 = translate([-case_top__part_0_x, -case_top__part_0_y, 0], case_top__part_0);
                case_top__part_0 = rotate([0,0,0], case_top__part_0);
                case_top__part_0 = translate([case_top__part_0_x, case_top__part_0_y, 0], case_top__part_0);

                case_top__part_0 = translate([0,0,0], case_top__part_0);
                let result = case_top__part_0;
                
            
                    return result;
                }
            
            
        
            function main() {
                return case_top_case_fn();
            }

        