function case_lip_extrude_1_6_outline_fn(){
    return new CSG.Path2D([[90.775,-83.675],[106.825,-83.675]]).appendPoint([106.825,-83.7]).appendPoint([117.1276915,-83.7]).appendArc([117.7463041,-83.7644731],{"radius":3,"clockwise":true,"large":false}).appendPoint([180.325,-96.9518726]).appendPoint([180.325,-97.04]).appendPoint([180.7431943,-97.04]).appendPoint([203.6849316,-101.8745823]).appendPoint([207.4881223,-103.5519893]).appendPoint([207.4835477,-103.5583556]).appendPoint([227.0953648,-117.6508759]).appendArc([231.2822391,-116.9652489],{"radius":3,"clockwise":false,"large":false}).appendPoint([243.6241357,-99.7896824]).appendArc([242.9385087,-95.6028081],{"radius":3,"clockwise":false,"large":false}).appendPoint([235.2375,-90.069072]).appendPoint([235.2375,4.71]).appendArc([232.2375,7.71],{"radius":3,"clockwise":false,"large":false}).appendPoint([188.425,7.71]).appendPoint([188.425,7.711]).appendPoint([172.375,7.711]).appendArc([169.375,10.711],{"radius":3,"clockwise":true,"large":false}).appendPoint([169.375,10.9634]).appendArc([166.375,13.9634],{"radius":3,"clockwise":false,"large":false}).appendPoint([147.925,13.9634]).appendArc([144.925,10.9634],{"radius":3,"clockwise":false,"large":false}).appendPoint([144.925,8.961]).appendArc([141.925,5.961],{"radius":3,"clockwise":true,"large":false}).appendPoint([128.875,5.961]).appendArc([125.875,2.961],{"radius":3,"clockwise":false,"large":false}).appendPoint([125.875,0.75]).appendArc([122.875,-2.25],{"radius":3,"clockwise":true,"large":false}).appendPoint([109.825,-2.25]).appendArc([106.825,-5.25],{"radius":3,"clockwise":false,"large":false}).appendPoint([106.825,-8.775]).appendArc([103.825,-11.775],{"radius":3,"clockwise":true,"large":false}).appendPoint([90.775,-11.775]).appendArc([87.775,-14.775],{"radius":3,"clockwise":false,"large":false}).appendPoint([87.775,-80.675]).appendArc([90.775,-83.675],{"radius":3,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    new CSG.Path2D([[92.575,-81.875],[108.625,-81.875]]).appendPoint([108.625,-81.9]).appendPoint([117.3152909,-81.9]).appendArc([117.9339035,-81.9644731],{"radius":3,"clockwise":true,"large":false}).appendPoint([204.239667,-100.15195]).appendPoint([210.2446648,-102.8004697]).appendPoint([209.9956722,-103.1469795]).appendPoint([226.6839886,-115.1387514]).appendArc([230.8708629,-114.4531244],{"radius":3,"clockwise":false,"large":false}).appendPoint([241.1120112,-100.2010585]).appendArc([240.4263842,-96.0141843],{"radius":3,"clockwise":false,"large":false}).appendPoint([233.4375,-90.9921615]).appendPoint([233.4375,2.91]).appendArc([230.4375,5.91],{"radius":3,"clockwise":false,"large":false}).appendPoint([186.625,5.91]).appendPoint([186.625,5.911]).appendPoint([170.575,5.911]).appendArc([167.575,8.911],{"radius":3,"clockwise":true,"large":false}).appendPoint([167.575,9.1634]).appendArc([164.575,12.1634],{"radius":3,"clockwise":false,"large":false}).appendPoint([149.725,12.1634]).appendArc([146.725,9.1634],{"radius":3,"clockwise":false,"large":false}).appendPoint([146.725,7.161]).appendArc([143.725,4.161],{"radius":3,"clockwise":true,"large":false}).appendPoint([130.675,4.161]).appendArc([127.675,1.161],{"radius":3,"clockwise":false,"large":false}).appendPoint([127.675,-1.05]).appendArc([124.675,-4.05],{"radius":3,"clockwise":true,"large":false}).appendPoint([111.625,-4.05]).appendArc([108.625,-7.05],{"radius":3,"clockwise":false,"large":false}).appendPoint([108.625,-10.575]).appendArc([105.625,-13.575],{"radius":3,"clockwise":true,"large":false}).appendPoint([92.575,-13.575]).appendArc([89.575,-16.575],{"radius":3,"clockwise":false,"large":false}).appendPoint([89.575,-78.875]).appendArc([92.575,-81.875],{"radius":3,"clockwise":false,"large":false}).close().innerToCAG()
).extrude({ offset: [0, 0, 1.6] });
}


function case_wall_extrude_11_outline_fn(){
    return new CSG.Path2D([[90.775,-83.675],[106.825,-83.675]]).appendPoint([106.825,-83.7]).appendPoint([117.1276915,-83.7]).appendArc([117.7463041,-83.7644731],{"radius":3,"clockwise":true,"large":false}).appendPoint([180.325,-96.9518726]).appendPoint([180.325,-97.04]).appendPoint([180.7431943,-97.04]).appendPoint([203.6849316,-101.8745823]).appendPoint([207.4881223,-103.5519893]).appendPoint([207.4835477,-103.5583556]).appendPoint([227.0953648,-117.6508759]).appendArc([231.2822391,-116.9652489],{"radius":3,"clockwise":false,"large":false}).appendPoint([243.6241357,-99.7896824]).appendArc([242.9385087,-95.6028081],{"radius":3,"clockwise":false,"large":false}).appendPoint([235.2375,-90.069072]).appendPoint([235.2375,4.71]).appendArc([232.2375,7.71],{"radius":3,"clockwise":false,"large":false}).appendPoint([188.425,7.71]).appendPoint([188.425,7.711]).appendPoint([172.375,7.711]).appendArc([169.375,10.711],{"radius":3,"clockwise":true,"large":false}).appendPoint([169.375,10.9634]).appendArc([166.375,13.9634],{"radius":3,"clockwise":false,"large":false}).appendPoint([147.925,13.9634]).appendArc([144.925,10.9634],{"radius":3,"clockwise":false,"large":false}).appendPoint([144.925,8.961]).appendArc([141.925,5.961],{"radius":3,"clockwise":true,"large":false}).appendPoint([128.875,5.961]).appendArc([125.875,2.961],{"radius":3,"clockwise":false,"large":false}).appendPoint([125.875,0.75]).appendArc([122.875,-2.25],{"radius":3,"clockwise":true,"large":false}).appendPoint([109.825,-2.25]).appendArc([106.825,-5.25],{"radius":3,"clockwise":false,"large":false}).appendPoint([106.825,-8.775]).appendArc([103.825,-11.775],{"radius":3,"clockwise":true,"large":false}).appendPoint([90.775,-11.775]).appendArc([87.775,-14.775],{"radius":3,"clockwise":false,"large":false}).appendPoint([87.775,-80.675]).appendArc([90.775,-83.675],{"radius":3,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    new CSG.Path2D([[93.475,-80.975],[109.525,-80.975]]).appendPoint([109.525,-81]).appendPoint([117.4090907,-81]).appendArc([118.0277033,-81.0644731],{"radius":3,"clockwise":true,"large":false}).appendPoint([204.5170347,-99.2906338]).appendPoint([211.622936,-102.4247097]).appendPoint([211.2517344,-102.9412914]).appendPoint([226.4783006,-113.8826891]).appendArc([230.6651748,-113.1970621],{"radius":3,"clockwise":false,"large":false}).appendPoint([239.8559489,-100.4067466]).appendArc([239.1703219,-96.2198724],{"radius":3,"clockwise":false,"large":false}).appendPoint([232.5375,-91.4537064]).appendPoint([232.5375,2.01]).appendArc([229.5375,5.01],{"radius":3,"clockwise":false,"large":false}).appendPoint([185.725,5.01]).appendPoint([185.725,5.011]).appendPoint([169.675,5.011]).appendArc([166.675,8.011],{"radius":3,"clockwise":true,"large":false}).appendPoint([166.675,8.2634]).appendArc([163.675,11.2634],{"radius":3,"clockwise":false,"large":false}).appendPoint([150.625,11.2634]).appendArc([147.625,8.2634],{"radius":3,"clockwise":false,"large":false}).appendPoint([147.625,6.261]).appendArc([144.625,3.261],{"radius":3,"clockwise":true,"large":false}).appendPoint([131.575,3.261]).appendArc([128.575,0.261],{"radius":3,"clockwise":false,"large":false}).appendPoint([128.575,-1.95]).appendArc([125.575,-4.95],{"radius":3,"clockwise":true,"large":false}).appendPoint([112.525,-4.95]).appendArc([109.525,-7.95],{"radius":3,"clockwise":false,"large":false}).appendPoint([109.525,-11.475]).appendArc([106.525,-14.475],{"radius":3,"clockwise":true,"large":false}).appendPoint([93.475,-14.475]).appendArc([90.475,-17.475],{"radius":3,"clockwise":false,"large":false}).appendPoint([90.475,-77.975]).appendArc([93.475,-80.975],{"radius":3,"clockwise":false,"large":false}).close().innerToCAG()
).extrude({ offset: [0, 0, 11] });
}


function case_top_extrude_2_outline_fn(){
    return new CSG.Path2D([[90.775,-83.675],[106.825,-83.675]]).appendPoint([106.825,-83.7]).appendPoint([117.1276915,-83.7]).appendArc([117.7463041,-83.7644731],{"radius":3,"clockwise":true,"large":false}).appendPoint([180.325,-96.9518726]).appendPoint([180.325,-97.04]).appendPoint([180.7431943,-97.04]).appendPoint([203.6849316,-101.8745823]).appendPoint([207.4881223,-103.5519893]).appendPoint([207.4835477,-103.5583556]).appendPoint([227.0953648,-117.6508759]).appendArc([231.2822391,-116.9652489],{"radius":3,"clockwise":false,"large":false}).appendPoint([243.6241357,-99.7896824]).appendArc([242.9385087,-95.6028081],{"radius":3,"clockwise":false,"large":false}).appendPoint([235.2375,-90.069072]).appendPoint([235.2375,4.71]).appendArc([232.2375,7.71],{"radius":3,"clockwise":false,"large":false}).appendPoint([188.425,7.71]).appendPoint([188.425,7.711]).appendPoint([172.375,7.711]).appendArc([169.375,10.711],{"radius":3,"clockwise":true,"large":false}).appendPoint([169.375,10.9634]).appendArc([166.375,13.9634],{"radius":3,"clockwise":false,"large":false}).appendPoint([147.925,13.9634]).appendArc([144.925,10.9634],{"radius":3,"clockwise":false,"large":false}).appendPoint([144.925,8.961]).appendArc([141.925,5.961],{"radius":3,"clockwise":true,"large":false}).appendPoint([128.875,5.961]).appendArc([125.875,2.961],{"radius":3,"clockwise":false,"large":false}).appendPoint([125.875,0.75]).appendArc([122.875,-2.25],{"radius":3,"clockwise":true,"large":false}).appendPoint([109.825,-2.25]).appendArc([106.825,-5.25],{"radius":3,"clockwise":false,"large":false}).appendPoint([106.825,-8.775]).appendArc([103.825,-11.775],{"radius":3,"clockwise":true,"large":false}).appendPoint([90.775,-11.775]).appendArc([87.775,-14.775],{"radius":3,"clockwise":false,"large":false}).appendPoint([87.775,-80.675]).appendArc([90.775,-83.675],{"radius":3,"clockwise":false,"large":false}).close().innerToCAG()
.subtract(
    new CSG.Path2D([[199.5318894,-94.3322383],[212.3413247,-99.9818724]]).appendPoint([217.9909588,-87.1724371]).appendPoint([205.1815235,-81.522803]).appendPoint([199.5318894,-94.3322383]).close().innerToCAG()
.union(
    new CSG.Path2D([[188.25,-11.515],[202.25,-11.515]]).appendPoint([202.25,2.485]).appendPoint([188.25,2.485]).appendPoint([188.25,-11.515]).close().innerToCAG()
).union(
    new CSG.Path2D([[188.25,-30.515],[202.25,-30.515]]).appendPoint([202.25,-16.515]).appendPoint([188.25,-16.515]).appendPoint([188.25,-30.515]).close().innerToCAG()
).union(
    new CSG.Path2D([[188.25,-49.515],[202.25,-49.515]]).appendPoint([202.25,-35.515]).appendPoint([188.25,-35.515]).appendPoint([188.25,-49.515]).close().innerToCAG()
).union(
    new CSG.Path2D([[188.25,-68.515],[202.25,-68.515]]).appendPoint([202.25,-54.515]).appendPoint([188.25,-54.515]).appendPoint([188.25,-68.515]).close().innerToCAG()
).union(
    new CSG.Path2D([[169.2,-14.565],[183.2,-14.565]]).appendPoint([183.2,-0.565]).appendPoint([169.2,-0.565]).appendPoint([169.2,-14.565]).close().innerToCAG()
).union(
    new CSG.Path2D([[169.2,-33.565],[183.2,-33.565]]).appendPoint([183.2,-19.565]).appendPoint([169.2,-19.565]).appendPoint([169.2,-33.565]).close().innerToCAG()
).union(
    new CSG.Path2D([[169.2,-52.565],[183.2,-52.565]]).appendPoint([183.2,-38.565]).appendPoint([169.2,-38.565]).appendPoint([169.2,-52.565]).close().innerToCAG()
).union(
    new CSG.Path2D([[169.2,-71.565],[183.2,-71.565]]).appendPoint([183.2,-57.565]).appendPoint([169.2,-57.565]).appendPoint([169.2,-71.565]).close().innerToCAG()
).union(
    new CSG.Path2D([[150.15,-8.615],[164.15,-8.615]]).appendPoint([164.15,5.385]).appendPoint([150.15,5.385]).appendPoint([150.15,-8.615]).close().innerToCAG()
).union(
    new CSG.Path2D([[150.15,-27.615],[164.15,-27.615]]).appendPoint([164.15,-13.615]).appendPoint([150.15,-13.615]).appendPoint([150.15,-27.615]).close().innerToCAG()
).union(
    new CSG.Path2D([[150.15,-46.615],[164.15,-46.615]]).appendPoint([164.15,-32.615]).appendPoint([150.15,-32.615]).appendPoint([150.15,-46.615]).close().innerToCAG()
).union(
    new CSG.Path2D([[150.15,-65.615],[164.15,-65.615]]).appendPoint([164.15,-51.615]).appendPoint([150.15,-51.615]).appendPoint([150.15,-65.615]).close().innerToCAG()
).union(
    new CSG.Path2D([[131.1,-17.665],[145.1,-17.665]]).appendPoint([145.1,-3.665]).appendPoint([131.1,-3.665]).appendPoint([131.1,-17.665]).close().innerToCAG()
).union(
    new CSG.Path2D([[131.1,-36.665],[145.1,-36.665]]).appendPoint([145.1,-22.665]).appendPoint([131.1,-22.665]).appendPoint([131.1,-36.665]).close().innerToCAG()
).union(
    new CSG.Path2D([[131.1,-55.665],[145.1,-55.665]]).appendPoint([145.1,-41.665]).appendPoint([131.1,-41.665]).appendPoint([131.1,-55.665]).close().innerToCAG()
).union(
    new CSG.Path2D([[131.1,-74.665],[145.1,-74.665]]).appendPoint([145.1,-60.665]).appendPoint([131.1,-60.665]).appendPoint([131.1,-74.665]).close().innerToCAG()
).union(
    new CSG.Path2D([[112.05,-21.475],[126.05,-21.475]]).appendPoint([126.05,-7.475]).appendPoint([112.05,-7.475]).appendPoint([112.05,-21.475]).close().innerToCAG()
).union(
    new CSG.Path2D([[112.05,-40.475],[126.05,-40.475]]).appendPoint([126.05,-26.475]).appendPoint([112.05,-26.475]).appendPoint([112.05,-40.475]).close().innerToCAG()
).union(
    new CSG.Path2D([[112.05,-59.475],[126.05,-59.475]]).appendPoint([126.05,-45.475]).appendPoint([112.05,-45.475]).appendPoint([112.05,-59.475]).close().innerToCAG()
).union(
    new CSG.Path2D([[112.05,-78.475],[126.05,-78.475]]).appendPoint([126.05,-64.475]).appendPoint([112.05,-64.475]).appendPoint([112.05,-78.475]).close().innerToCAG()
).union(
    new CSG.Path2D([[93,-31],[107,-31]]).appendPoint([107,-17]).appendPoint([93,-17]).appendPoint([93,-31]).close().innerToCAG()
).union(
    new CSG.Path2D([[93,-50],[107,-50]]).appendPoint([107,-36]).appendPoint([93,-36]).appendPoint([93,-50]).close().innerToCAG()
).union(
    new CSG.Path2D([[93,-69],[107,-69]]).appendPoint([107,-55]).appendPoint([93,-55]).appendPoint([93,-69]).close().innerToCAG()
).union(
    new CSG.Path2D([[180.5595254,-90.6395751],[194.2586512,-93.5264337]]).appendPoint([197.1455098,-79.8273079]).appendPoint([183.446384,-76.9404493]).appendPoint([180.5595254,-90.6395751]).close().innerToCAG()
).union(
    new CSG.Path2D([[216.9683124,-103.9397833],[228.3374818,-112.1093603]]).appendPoint([236.5070588,-100.7401909]).appendPoint([225.1378894,-92.5706139]).appendPoint([216.9683124,-103.9397833]).close().innerToCAG()
)).extrude({ offset: [0, 0, 2] });
}


function _switch_clips_extrude_1_outline_fn(){
    return new CSG.Path2D([[184.7566117,-92.5460029],[189.6491566,-93.5770238]]).appendPoint([192.9484235,-77.9208801]).appendPoint([188.0558786,-76.8898592]).appendPoint([184.7566117,-92.5460029]).close().innerToCAG()
.union(
    new CSG.Path2D([[220.0391471,-107.3778023],[224.0995647,-110.2955083]]).appendPoint([233.4362241,-97.3021719]).appendPoint([229.3758065,-94.3844659]).appendPoint([220.0391471,-107.3778023]).close().innerToCAG()
).union(
    new CSG.Path2D([[203.2456626,-97.0631518],[207.8204609,-99.0808783]]).appendPoint([214.2771856,-84.4415236]).appendPoint([209.7023873,-82.4237971]).appendPoint([203.2456626,-97.0631518]).close().innerToCAG()
).union(
    new CSG.Path2D([[192.75,-12.515],[197.75,-12.515]]).appendPoint([197.75,3.485]).appendPoint([192.75,3.485]).appendPoint([192.75,-12.515]).close().innerToCAG()
).union(
    new CSG.Path2D([[192.75,-31.515],[197.75,-31.515]]).appendPoint([197.75,-15.515]).appendPoint([192.75,-15.515]).appendPoint([192.75,-31.515]).close().innerToCAG()
).union(
    new CSG.Path2D([[192.75,-50.515],[197.75,-50.515]]).appendPoint([197.75,-34.515]).appendPoint([192.75,-34.515]).appendPoint([192.75,-50.515]).close().innerToCAG()
).union(
    new CSG.Path2D([[192.75,-69.515],[197.75,-69.515]]).appendPoint([197.75,-53.515]).appendPoint([192.75,-53.515]).appendPoint([192.75,-69.515]).close().innerToCAG()
).union(
    new CSG.Path2D([[173.7,-15.565],[178.7,-15.565]]).appendPoint([178.7,0.435]).appendPoint([173.7,0.435]).appendPoint([173.7,-15.565]).close().innerToCAG()
).union(
    new CSG.Path2D([[173.7,-34.565],[178.7,-34.565]]).appendPoint([178.7,-18.565]).appendPoint([173.7,-18.565]).appendPoint([173.7,-34.565]).close().innerToCAG()
).union(
    new CSG.Path2D([[173.7,-53.565],[178.7,-53.565]]).appendPoint([178.7,-37.565]).appendPoint([173.7,-37.565]).appendPoint([173.7,-53.565]).close().innerToCAG()
).union(
    new CSG.Path2D([[173.7,-72.565],[178.7,-72.565]]).appendPoint([178.7,-56.565]).appendPoint([173.7,-56.565]).appendPoint([173.7,-72.565]).close().innerToCAG()
).union(
    new CSG.Path2D([[154.65,-9.615],[159.65,-9.615]]).appendPoint([159.65,6.385]).appendPoint([154.65,6.385]).appendPoint([154.65,-9.615]).close().innerToCAG()
).union(
    new CSG.Path2D([[154.65,-28.615],[159.65,-28.615]]).appendPoint([159.65,-12.615]).appendPoint([154.65,-12.615]).appendPoint([154.65,-28.615]).close().innerToCAG()
).union(
    new CSG.Path2D([[154.65,-47.615],[159.65,-47.615]]).appendPoint([159.65,-31.615]).appendPoint([154.65,-31.615]).appendPoint([154.65,-47.615]).close().innerToCAG()
).union(
    new CSG.Path2D([[154.65,-66.615],[159.65,-66.615]]).appendPoint([159.65,-50.615]).appendPoint([154.65,-50.615]).appendPoint([154.65,-66.615]).close().innerToCAG()
).union(
    new CSG.Path2D([[135.6,-18.665],[140.6,-18.665]]).appendPoint([140.6,-2.665]).appendPoint([135.6,-2.665]).appendPoint([135.6,-18.665]).close().innerToCAG()
).union(
    new CSG.Path2D([[135.6,-37.665],[140.6,-37.665]]).appendPoint([140.6,-21.665]).appendPoint([135.6,-21.665]).appendPoint([135.6,-37.665]).close().innerToCAG()
).union(
    new CSG.Path2D([[135.6,-56.665],[140.6,-56.665]]).appendPoint([140.6,-40.665]).appendPoint([135.6,-40.665]).appendPoint([135.6,-56.665]).close().innerToCAG()
).union(
    new CSG.Path2D([[135.6,-75.665],[140.6,-75.665]]).appendPoint([140.6,-59.665]).appendPoint([135.6,-59.665]).appendPoint([135.6,-75.665]).close().innerToCAG()
).union(
    new CSG.Path2D([[116.55,-22.475],[121.55,-22.475]]).appendPoint([121.55,-6.475]).appendPoint([116.55,-6.475]).appendPoint([116.55,-22.475]).close().innerToCAG()
).union(
    new CSG.Path2D([[116.55,-41.475],[121.55,-41.475]]).appendPoint([121.55,-25.475]).appendPoint([116.55,-25.475]).appendPoint([116.55,-41.475]).close().innerToCAG()
).union(
    new CSG.Path2D([[116.55,-60.475],[121.55,-60.475]]).appendPoint([121.55,-44.475]).appendPoint([116.55,-44.475]).appendPoint([116.55,-60.475]).close().innerToCAG()
).union(
    new CSG.Path2D([[116.55,-79.475],[121.55,-79.475]]).appendPoint([121.55,-63.475]).appendPoint([116.55,-63.475]).appendPoint([116.55,-79.475]).close().innerToCAG()
).union(
    new CSG.Path2D([[97.5,-32],[102.5,-32]]).appendPoint([102.5,-16]).appendPoint([97.5,-16]).appendPoint([97.5,-32]).close().innerToCAG()
).union(
    new CSG.Path2D([[97.5,-51],[102.5,-51]]).appendPoint([102.5,-35]).appendPoint([97.5,-35]).appendPoint([97.5,-51]).close().innerToCAG()
).union(
    new CSG.Path2D([[97.5,-70],[102.5,-70]]).appendPoint([102.5,-54]).appendPoint([97.5,-54]).appendPoint([97.5,-70]).close().innerToCAG()
).extrude({ offset: [0, 0, 1] });
}


function _posts_extrude_11_outline_fn(){
    return CAG.circle({"center":[204.775,-71.04],"radius":2.6})
.union(
    CAG.circle({"center":[204.775,-52.04],"radius":2.6})
).union(
    CAG.circle({"center":[147.625,-77.24],"radius":2.6})
).union(
    CAG.circle({"center":[183.725,-36.09],"radius":2.6})
).union(
    CAG.circle({"center":[164.675,-30.14],"radius":2.6})
).union(
    CAG.circle({"center":[111.525,-62],"radius":2.6})
).union(
    CAG.circle({"center":[202.775,-13.99],"radius":2.6})
).union(
    CAG.circle({"center":[144.625,-20.19],"radius":2.6})
).union(
    CAG.circle({"center":[107.525,-33.525],"radius":2.6})
).extrude({ offset: [0, 0, 11] });
}


function _screw_holes_extrude_9_outline_fn(){
    return CAG.circle({"center":[204.775,-71.04],"radius":0.8})
.union(
    CAG.circle({"center":[204.775,-52.04],"radius":0.8})
).union(
    CAG.circle({"center":[147.625,-77.24],"radius":0.8})
).union(
    CAG.circle({"center":[183.725,-36.09],"radius":0.8})
).union(
    CAG.circle({"center":[164.675,-30.14],"radius":0.8})
).union(
    CAG.circle({"center":[111.525,-62],"radius":0.8})
).union(
    CAG.circle({"center":[202.775,-13.99],"radius":0.8})
).union(
    CAG.circle({"center":[144.625,-20.19],"radius":0.8})
).union(
    CAG.circle({"center":[107.525,-33.525],"radius":0.8})
).extrude({ offset: [0, 0, 9] });
}


function _usb_cutout_extrude_4_5_outline_fn(){
    return new CSG.Path2D([[214.63125,4.0961111],[222.63125,4.0961111]]).appendPoint([222.63125,9.4961111]).appendPoint([214.63125,9.4961111]).appendPoint([214.63125,4.0961111]).close().innerToCAG()
.extrude({ offset: [0, 0, 4.5] });
}


function _ttrs_cutout_extrude_20_outline_fn(){
    return CAG.circle({"center":[233.83125,-62.9038889],"radius":4.75})
.extrude({ offset: [0, 0, 20] });
}


function _ttrs_socket_holder_extrude_3_outline_fn(){
    return new CSG.Path2D([[212.03125,-74.1038889],[231.73125,-74.1038889]]).appendPoint([231.73125,-72.4038889]).appendPoint([214.88125,-72.4038889]).appendPoint([214.88125,-53.4038889]).appendPoint([231.73125,-53.4038889]).appendPoint([231.73125,-51.7038889]).appendPoint([212.03125,-51.7038889]).appendPoint([212.03125,-74.1038889]).close().innerToCAG()
.extrude({ offset: [0, 0, 3] });
}


function _mcu_group_extrude_3_outline_fn(){
    return new CSG.Path2D([[205.43125,-50.2538889],[231.83125,-50.2538889]]).appendPoint([231.83125,3.4461111]).appendPoint([230.13125,3.4461111]).appendPoint([230.13125,-46.9038889]).appendPoint([207.13125,-46.9038889]).appendPoint([207.13125,3.4461111]).appendPoint([205.43125,3.4461111]).appendPoint([205.43125,-50.2538889]).close().innerToCAG()
.extrude({ offset: [0, 0, 3] });
}




                function _body_case_fn() {
                    

                // creating part 0 of case _body
                let _body__part_0 = case_lip_extrude_1_6_outline_fn();

                // make sure that rotations are relative
                let _body__part_0_bounds = _body__part_0.getBounds();
                let _body__part_0_x = _body__part_0_bounds[0].x + (_body__part_0_bounds[1].x - _body__part_0_bounds[0].x) / 2
                let _body__part_0_y = _body__part_0_bounds[0].y + (_body__part_0_bounds[1].y - _body__part_0_bounds[0].y) / 2
                _body__part_0 = translate([-_body__part_0_x, -_body__part_0_y, 0], _body__part_0);
                _body__part_0 = rotate([0,0,0], _body__part_0);
                _body__part_0 = translate([_body__part_0_x, _body__part_0_y, 0], _body__part_0);

                _body__part_0 = translate([0,0,0], _body__part_0);
                let result = _body__part_0;
                
            

                // creating part 1 of case _body
                let _body__part_1 = case_wall_extrude_11_outline_fn();

                // make sure that rotations are relative
                let _body__part_1_bounds = _body__part_1.getBounds();
                let _body__part_1_x = _body__part_1_bounds[0].x + (_body__part_1_bounds[1].x - _body__part_1_bounds[0].x) / 2
                let _body__part_1_y = _body__part_1_bounds[0].y + (_body__part_1_bounds[1].y - _body__part_1_bounds[0].y) / 2
                _body__part_1 = translate([-_body__part_1_x, -_body__part_1_y, 0], _body__part_1);
                _body__part_1 = rotate([0,0,0], _body__part_1);
                _body__part_1 = translate([_body__part_1_x, _body__part_1_y, 0], _body__part_1);

                _body__part_1 = translate([0,0,1.6], _body__part_1);
                result = result.union(_body__part_1);
                
            

                // creating part 2 of case _body
                let _body__part_2 = case_top_extrude_2_outline_fn();

                // make sure that rotations are relative
                let _body__part_2_bounds = _body__part_2.getBounds();
                let _body__part_2_x = _body__part_2_bounds[0].x + (_body__part_2_bounds[1].x - _body__part_2_bounds[0].x) / 2
                let _body__part_2_y = _body__part_2_bounds[0].y + (_body__part_2_bounds[1].y - _body__part_2_bounds[0].y) / 2
                _body__part_2 = translate([-_body__part_2_x, -_body__part_2_y, 0], _body__part_2);
                _body__part_2 = rotate([0,0,0], _body__part_2);
                _body__part_2 = translate([_body__part_2_x, _body__part_2_y, 0], _body__part_2);

                _body__part_2 = translate([0,0,11], _body__part_2);
                result = result.union(_body__part_2);
                
            

                // creating part 3 of case _body
                let _body__part_3 = _switch_clips_extrude_1_outline_fn();

                // make sure that rotations are relative
                let _body__part_3_bounds = _body__part_3.getBounds();
                let _body__part_3_x = _body__part_3_bounds[0].x + (_body__part_3_bounds[1].x - _body__part_3_bounds[0].x) / 2
                let _body__part_3_y = _body__part_3_bounds[0].y + (_body__part_3_bounds[1].y - _body__part_3_bounds[0].y) / 2
                _body__part_3 = translate([-_body__part_3_x, -_body__part_3_y, 0], _body__part_3);
                _body__part_3 = rotate([0,0,0], _body__part_3);
                _body__part_3 = translate([_body__part_3_x, _body__part_3_y, 0], _body__part_3);

                _body__part_3 = translate([0,0,7.6], _body__part_3);
                result = result.subtract(_body__part_3);
                
            

                // creating part 4 of case _body
                let _body__part_4 = _posts_extrude_11_outline_fn();

                // make sure that rotations are relative
                let _body__part_4_bounds = _body__part_4.getBounds();
                let _body__part_4_x = _body__part_4_bounds[0].x + (_body__part_4_bounds[1].x - _body__part_4_bounds[0].x) / 2
                let _body__part_4_y = _body__part_4_bounds[0].y + (_body__part_4_bounds[1].y - _body__part_4_bounds[0].y) / 2
                _body__part_4 = translate([-_body__part_4_x, -_body__part_4_y, 0], _body__part_4);
                _body__part_4 = rotate([0,0,0], _body__part_4);
                _body__part_4 = translate([_body__part_4_x, _body__part_4_y, 0], _body__part_4);

                _body__part_4 = translate([0,0,2], _body__part_4);
                result = result.union(_body__part_4);
                
            

                // creating part 5 of case _body
                let _body__part_5 = _screw_holes_extrude_9_outline_fn();

                // make sure that rotations are relative
                let _body__part_5_bounds = _body__part_5.getBounds();
                let _body__part_5_x = _body__part_5_bounds[0].x + (_body__part_5_bounds[1].x - _body__part_5_bounds[0].x) / 2
                let _body__part_5_y = _body__part_5_bounds[0].y + (_body__part_5_bounds[1].y - _body__part_5_bounds[0].y) / 2
                _body__part_5 = translate([-_body__part_5_x, -_body__part_5_y, 0], _body__part_5);
                _body__part_5 = rotate([0,0,0], _body__part_5);
                _body__part_5 = translate([_body__part_5_x, _body__part_5_y, 0], _body__part_5);

                _body__part_5 = translate([0,0,2], _body__part_5);
                result = result.subtract(_body__part_5);
                
            

                // creating part 6 of case _body
                let _body__part_6 = _usb_cutout_extrude_4_5_outline_fn();

                // make sure that rotations are relative
                let _body__part_6_bounds = _body__part_6.getBounds();
                let _body__part_6_x = _body__part_6_bounds[0].x + (_body__part_6_bounds[1].x - _body__part_6_bounds[0].x) / 2
                let _body__part_6_y = _body__part_6_bounds[0].y + (_body__part_6_bounds[1].y - _body__part_6_bounds[0].y) / 2
                _body__part_6 = translate([-_body__part_6_x, -_body__part_6_y, 0], _body__part_6);
                _body__part_6 = rotate([0,0,0], _body__part_6);
                _body__part_6 = translate([_body__part_6_x, _body__part_6_y, 0], _body__part_6);

                _body__part_6 = translate([0,0,7.5], _body__part_6);
                result = result.subtract(_body__part_6);
                
            

                // creating part 7 of case _body
                let _body__part_7 = _ttrs_cutout_extrude_20_outline_fn();

                // make sure that rotations are relative
                let _body__part_7_bounds = _body__part_7.getBounds();
                let _body__part_7_x = _body__part_7_bounds[0].x + (_body__part_7_bounds[1].x - _body__part_7_bounds[0].x) / 2
                let _body__part_7_y = _body__part_7_bounds[0].y + (_body__part_7_bounds[1].y - _body__part_7_bounds[0].y) / 2
                _body__part_7 = translate([-_body__part_7_x, -_body__part_7_y, 0], _body__part_7);
                _body__part_7 = rotate([0,-90,0], _body__part_7);
                _body__part_7 = translate([_body__part_7_x, _body__part_7_y, 0], _body__part_7);

                _body__part_7 = translate([10,0,5.5], _body__part_7);
                result = result.subtract(_body__part_7);
                
            

                // creating part 8 of case _body
                let _body__part_8 = _ttrs_socket_holder_extrude_3_outline_fn();

                // make sure that rotations are relative
                let _body__part_8_bounds = _body__part_8.getBounds();
                let _body__part_8_x = _body__part_8_bounds[0].x + (_body__part_8_bounds[1].x - _body__part_8_bounds[0].x) / 2
                let _body__part_8_y = _body__part_8_bounds[0].y + (_body__part_8_bounds[1].y - _body__part_8_bounds[0].y) / 2
                _body__part_8 = translate([-_body__part_8_x, -_body__part_8_y, 0], _body__part_8);
                _body__part_8 = rotate([0,0,0], _body__part_8);
                _body__part_8 = translate([_body__part_8_x, _body__part_8_y, 0], _body__part_8);

                _body__part_8 = translate([0,0,9], _body__part_8);
                result = result.union(_body__part_8);
                
            

                // creating part 9 of case _body
                let _body__part_9 = _mcu_group_extrude_3_outline_fn();

                // make sure that rotations are relative
                let _body__part_9_bounds = _body__part_9.getBounds();
                let _body__part_9_x = _body__part_9_bounds[0].x + (_body__part_9_bounds[1].x - _body__part_9_bounds[0].x) / 2
                let _body__part_9_y = _body__part_9_bounds[0].y + (_body__part_9_bounds[1].y - _body__part_9_bounds[0].y) / 2
                _body__part_9 = translate([-_body__part_9_x, -_body__part_9_y, 0], _body__part_9);
                _body__part_9 = rotate([0,0,0], _body__part_9);
                _body__part_9 = translate([_body__part_9_x, _body__part_9_y, 0], _body__part_9);

                _body__part_9 = translate([0,0,9], _body__part_9);
                result = result.union(_body__part_9);
                
            
                    return result;
                }
            
            

                function body_case_fn() {
                    

                // creating part 0 of case body
                let body__part_0 = _body_case_fn();

                // make sure that rotations are relative
                let body__part_0_bounds = body__part_0.getBounds();
                let body__part_0_x = body__part_0_bounds[0].x + (body__part_0_bounds[1].x - body__part_0_bounds[0].x) / 2
                let body__part_0_y = body__part_0_bounds[0].y + (body__part_0_bounds[1].y - body__part_0_bounds[0].y) / 2
                body__part_0 = translate([-body__part_0_x, -body__part_0_y, 0], body__part_0);
                body__part_0 = rotate([0,0,0], body__part_0);
                body__part_0 = translate([body__part_0_x, body__part_0_y, 0], body__part_0);

                body__part_0 = translate([0,0,0], body__part_0);
                let result = body__part_0;
                
            
                    return result;
                }
            
            
        
            function main() {
                return body_case_fn();
            }

        