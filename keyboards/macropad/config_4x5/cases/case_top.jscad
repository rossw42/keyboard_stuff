function switchplate_extrude_1_6_outline_fn(){
    return new CSG.Path2D([[161.925,121.8],[161.925,123.325]]).appendArc([161.425,123.825],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([143.375,123.825]).appendArc([142.875,123.325],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([142.875,121.8]).appendPoint([161.925,121.8]).close().innerToCAG()
.union(
    new CSG.Path2D([[143.375,104.775],[161.425,104.775]]).appendArc([161.925,105.275],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([161.925,106.8]).appendPoint([142.875,106.8]).appendPoint([142.875,105.275]).appendArc([143.375,104.775],{"radius":0.5,"clockwise":false,"large":false}).close().innerToCAG()
).union(
    new CSG.Path2D([[86.225,133.35],[104.275,133.35]]).appendArc([104.775,133.85],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([104.775,151.9]).appendArc([104.275,152.4],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([86.225,152.4]).appendArc([85.725,151.9],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([85.725,133.85]).appendArc([86.225,133.35],{"radius":0.5,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    new CSG.Path2D([[88.25,135.875],[102.25,135.875]]).appendPoint([102.25,149.875]).appendPoint([88.25,149.875]).appendPoint([88.25,135.875]).close().innerToCAG()
)).union(
    new CSG.Path2D([[129.0875,81.725],[147.1375,81.725]]).appendArc([147.6375,82.225],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([147.6375,100.275]).appendArc([147.1375,100.775],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([129.0875,100.775]).appendArc([128.5875,100.275],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([128.5875,82.225]).appendArc([129.0875,81.725],{"radius":0.5,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    new CSG.Path2D([[131.1125,84.25],[145.1125,84.25]]).appendPoint([145.1125,98.25]).appendPoint([131.1125,98.25]).appendPoint([131.1125,84.25]).close().innerToCAG()
)).union(
    new CSG.Path2D([[157.6625,81.725],[175.7125,81.725]]).appendArc([176.2125,82.225],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([176.2125,100.275]).appendArc([175.7125,100.775],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([157.6625,100.775]).appendArc([157.1625,100.275],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([157.1625,82.225]).appendArc([157.6625,81.725],{"radius":0.5,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    new CSG.Path2D([[159.6875,84.25],[173.6875,84.25]]).appendPoint([173.6875,98.25]).appendPoint([159.6875,98.25]).appendPoint([159.6875,84.25]).close().innerToCAG()
)).union(
    new CSG.Path2D([[143.375,29.86],[161.425,29.86]]).appendArc([161.925,30.36],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([161.925,48.41]).appendArc([161.425,48.91],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([143.375,48.91]).appendArc([142.875,48.41],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([142.875,30.36]).appendArc([143.375,29.86],{"radius":0.5,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    new CSG.Path2D([[145.4,32.385],[159.4,32.385]]).appendPoint([159.4,46.385]).appendPoint([145.4,46.385]).appendPoint([145.4,32.385]).close().innerToCAG()
)).union(
    new CSG.Path2D([[143.375,54.625],[161.425,54.625]]).appendArc([161.925,55.125],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([161.925,73.175]).appendArc([161.425,73.675],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([143.375,73.675]).appendArc([142.875,73.175],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([142.875,55.125]).appendArc([143.375,54.625],{"radius":0.5,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    new CSG.Path2D([[145.4,57.15],[159.4,57.15]]).appendPoint([159.4,71.15]).appendPoint([145.4,71.15]).appendPoint([145.4,57.15]).close().innerToCAG()
)).union(
    new CSG.Path2D([[24.3125,28.575],[123.325,28.575]]).appendArc([123.825,29.075],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([123.825,123.325]).appendArc([123.325,123.825],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([24.3125,123.825]).appendArc([23.8125,123.325],{"radius":0.5,"clockwise":false,"large":false}).appendPoint([23.8125,29.075]).appendArc([24.3125,28.575],{"radius":0.5,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    new CSG.Path2D([[26.3375,107.3],[40.3375,107.3]]).appendPoint([40.3375,121.3]).appendPoint([26.3375,121.3]).appendPoint([26.3375,107.3]).close().innerToCAG()
.union(
    new CSG.Path2D([[26.3375,88.25],[40.3375,88.25]]).appendPoint([40.3375,102.25]).appendPoint([26.3375,102.25]).appendPoint([26.3375,88.25]).close().innerToCAG()
).union(
    new CSG.Path2D([[26.3375,69.2],[40.3375,69.2]]).appendPoint([40.3375,83.2]).appendPoint([26.3375,83.2]).appendPoint([26.3375,69.2]).close().innerToCAG()
).union(
    new CSG.Path2D([[26.3375,50.15],[40.3375,50.15]]).appendPoint([40.3375,64.15]).appendPoint([26.3375,64.15]).appendPoint([26.3375,50.15]).close().innerToCAG()
).union(
    new CSG.Path2D([[26.3375,31.1],[40.3375,31.1]]).appendPoint([40.3375,45.1]).appendPoint([26.3375,45.1]).appendPoint([26.3375,31.1]).close().innerToCAG()
).union(
    new CSG.Path2D([[107.3,107.3],[121.3,107.3]]).appendPoint([121.3,121.3]).appendPoint([107.3,121.3]).appendPoint([107.3,107.3]).close().innerToCAG()
).union(
    new CSG.Path2D([[107.3,88.25],[121.3,88.25]]).appendPoint([121.3,102.25]).appendPoint([107.3,102.25]).appendPoint([107.3,88.25]).close().innerToCAG()
).union(
    new CSG.Path2D([[107.3,69.2],[121.3,69.2]]).appendPoint([121.3,83.2]).appendPoint([107.3,83.2]).appendPoint([107.3,69.2]).close().innerToCAG()
).union(
    new CSG.Path2D([[107.3,50.15],[121.3,50.15]]).appendPoint([121.3,64.15]).appendPoint([107.3,64.15]).appendPoint([107.3,50.15]).close().innerToCAG()
).union(
    new CSG.Path2D([[107.3,31.1],[121.3,31.1]]).appendPoint([121.3,45.1]).appendPoint([107.3,45.1]).appendPoint([107.3,31.1]).close().innerToCAG()
).union(
    new CSG.Path2D([[88.25,107.3],[102.25,107.3]]).appendPoint([102.25,121.3]).appendPoint([88.25,121.3]).appendPoint([88.25,107.3]).close().innerToCAG()
).union(
    new CSG.Path2D([[88.25,88.25],[102.25,88.25]]).appendPoint([102.25,102.25]).appendPoint([88.25,102.25]).appendPoint([88.25,88.25]).close().innerToCAG()
).union(
    new CSG.Path2D([[88.25,69.2],[102.25,69.2]]).appendPoint([102.25,83.2]).appendPoint([88.25,83.2]).appendPoint([88.25,69.2]).close().innerToCAG()
).union(
    new CSG.Path2D([[88.25,50.15],[102.25,50.15]]).appendPoint([102.25,64.15]).appendPoint([88.25,64.15]).appendPoint([88.25,50.15]).close().innerToCAG()
).union(
    new CSG.Path2D([[88.25,31.1],[102.25,31.1]]).appendPoint([102.25,45.1]).appendPoint([88.25,45.1]).appendPoint([88.25,31.1]).close().innerToCAG()
).union(
    new CSG.Path2D([[69.2,107.3],[83.2,107.3]]).appendPoint([83.2,121.3]).appendPoint([69.2,121.3]).appendPoint([69.2,107.3]).close().innerToCAG()
).union(
    new CSG.Path2D([[69.2,88.25],[83.2,88.25]]).appendPoint([83.2,102.25]).appendPoint([69.2,102.25]).appendPoint([69.2,88.25]).close().innerToCAG()
).union(
    new CSG.Path2D([[69.2,69.2],[83.2,69.2]]).appendPoint([83.2,83.2]).appendPoint([69.2,83.2]).appendPoint([69.2,69.2]).close().innerToCAG()
).union(
    new CSG.Path2D([[69.2,50.15],[83.2,50.15]]).appendPoint([83.2,64.15]).appendPoint([69.2,64.15]).appendPoint([69.2,50.15]).close().innerToCAG()
).union(
    new CSG.Path2D([[69.2,31.1],[83.2,31.1]]).appendPoint([83.2,45.1]).appendPoint([69.2,45.1]).appendPoint([69.2,31.1]).close().innerToCAG()
).union(
    new CSG.Path2D([[50.15,107.3],[64.15,107.3]]).appendPoint([64.15,121.3]).appendPoint([50.15,121.3]).appendPoint([50.15,107.3]).close().innerToCAG()
).union(
    new CSG.Path2D([[50.15,88.25],[64.15,88.25]]).appendPoint([64.15,102.25]).appendPoint([50.15,102.25]).appendPoint([50.15,88.25]).close().innerToCAG()
).union(
    new CSG.Path2D([[50.15,69.2],[64.15,69.2]]).appendPoint([64.15,83.2]).appendPoint([50.15,83.2]).appendPoint([50.15,69.2]).close().innerToCAG()
).union(
    new CSG.Path2D([[50.15,50.15],[64.15,50.15]]).appendPoint([64.15,64.15]).appendPoint([50.15,64.15]).appendPoint([50.15,50.15]).close().innerToCAG()
).union(
    new CSG.Path2D([[50.15,31.1],[64.15,31.1]]).appendPoint([64.15,45.1]).appendPoint([50.15,45.1]).appendPoint([50.15,31.1]).close().innerToCAG()
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

        