#!/usr/bin/env python3
"""Verify the two center space switch footprints don't overlap on the choc PCB."""
import math
import re
import sys

pcb_path = sys.argv[1] if len(sys.argv) > 1 else 'ergogen/out_choc/ergogen/pcbs/biaxial_choc.kicad_pcb'
text = open(pcb_path, encoding='utf-8').read()

# All choc switch footprint placements: (at x y rot)
placements = [(float(m.group(1)), float(m.group(2)), float(m.group(3) or 0))
              for m in re.finditer(
                  r'ceoloide:switch_choc[^"]*"[\s\S]{0,600}?\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)',
                  text)]
print(f"choc switch footprints found: {len(placements)}")

# The two center spaces: the pair closest to the overall center X
cx = sum(p[0] for p in placements) / len(placements)
placements.sort(key=lambda p: abs(p[0] - cx))
s1, s2 = sorted(placements[:2])
dist = math.hypot(s2[0] - s1[0], s2[1] - s1[1])
print(f"space L: ({s1[0]}, {s1[1]}) rot {s1[2]}")
print(f"space R: ({s2[0]}, {s2[1]}) rot {s2[2]}")
print(f"center-to-center: {dist:.2f} mm")

# Choc hotswap footprint horizontal extent: socket pads reach ~ +/-8.3mm from
# center (worst case with silkscreen ~ 9mm). Two adjacent need >= ~16.6mm.
REQ = 17.0
print(f"required minimum (choc hotswap width + margin): {REQ} mm")
print("OK: no overlap" if dist >= REQ else "WARNING: potential overlap")