Suggested downloads (start here)

LaserBoost — GH60 / Pok3r plate DXF downloads (ANSI / HHKB / split shift variants)
Downloadable DXF plates for the commonly used GH60 outline (useful for cases/plates and checking screw locations).
Link / source: LaserBoost “Keyboard Plates — GH60 / Pok3r (download DXF)”. 
laserboost.com

komar007 / GH60 GitHub (original GH60 project) — KiCad / PCB source files
Official GH60 repo (KiCad files, board / gerber / schematic). The KiCad .kicad_pcb contains the board outline and precise pad/standoff/USB port locations — you can open it in KiCad and export the board outline to DXF (or view coordinates directly). 
GitHub

KBDfans — Plate / board files (collection of plate files including OG60 / D60 / Tofu60 / etc.)
KBDfans maintains a downloads section with plate/outline files for many 60% variants (useful if you’re matching a commercial case). Their “Plate Files Document” page lists downloadable plate/outline files. 
KBDfans® Mechanical Keyboards Store
+1

DZ60 / community plates (Reddit / Thingiverse / GrabCAD)
There are community DXF/plate files for DZ60 and related PCBs (plate A/B variants). If your board is DZ60-family, check the DZ60 folders on QMK / GrabCAD / Thingiverse for DXF/STL/plate exports. Examples: QMK DZ60 folder, GrabCAD models and Thingiverse plates. 
git.pngu.org
+2
Thingiverse
+2

How I recommend you proceed (practical, reproducible)

If you want the exact USB cutout position and mounting/standoff coordinates, do this (fastest & most accurate):

A. If you want vendor-supplied DXF (plate/case):

Download the GH60 DXF from LaserBoost (link above) or the plate DXF from KBDfans. Those are already vector DXF files you can open in any CAD/CAM program and measure exact hole positions for mounting bosses and USB cutouts. 
laserboost.com
+1

B. If you want the PCB’s authoritative coordinates (preferred for USB port / screw hole centers):

Download the GH60 repo (komar007) from GitHub and open keyboard.kicad_pcb (or the repo’s gerbers) in KiCad.

In KiCad you can export the board outline as DXF (or simply use the board editor to read exact coordinates of mounting holes and the USB connector footprint). That gives you the true coordinates used for fabrication. 
GitHub

C. If your goal is to check case compatibility:

Overlay the DXF of the PCB outline (or the plate DXF) onto your case CAD drawing — measure the distance between the mounting holes and the USB cutout. LaserBoost and most plate sellers provide DXF that’s ready to overlay. 
laserboost.com

Want me to fetch or extract these for you now?

I can do one of the following right away (pick one) and perform it now:

A — Fetch the LaserBoost GH60 DXF link and attach it here (direct download link to their DXF).

B — Open the komar007 GH60 repo and extract the board outline (export coordinates for every mounting hole + USB cutout) and paste the numeric coordinates here (I’ll read them from the KiCad board file and give you exact X/Y in mm). 
GitHub

C — Grab the DZ60 / BM60 plate DXFs from KBDfans / community sources and give you the exact hole coordinates and USB cutout positions side-by-side (GH60 vs DZ60 vs BM60 comparisons). 
KBDfans® Mechanical Keyboards Store
+1
