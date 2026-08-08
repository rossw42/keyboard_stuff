# Wire-Bending Jig — for the PG1350→PG1425 Adapter's Captive Wire Channels

Small handheld jig that lets you form the ~72 bridge wires (36 keys × 2 wires,
for a full le-oeuf board) into a repeatable, exact shape instead of eyeballing
each bend with pliers. Print it, keep it on the bench, and every wire comes
out identical.

**Files:**
- `wire_bending_jig.scad` — OpenSCAD source (parametric)
- `wire_bending_jig.stl` — ready-to-print export
- `wire_bending_jig_preview.png` — render for reference

---

## What size wire to use

**Recommendation: 0.5–0.6 mm diameter solid, BARE (uninsulated), tinned
copper wire — 24 AWG bus/jumper wire, or diode legs (same spec).**

**Bare wire is correct and required here — do NOT use insulated hookup
wire.** Each wire runs alone in its own dedicated, walled-off plastic
channel (capped by the switch housing once assembled), so there's no
crossing point where a bare conductor could short against anything —
the channel itself provides all the isolation insulation would give you.
Insulation would also add 0.3mm+ of jacket diameter on top of the 0.5mm
conductor, which risks blowing the fit in the 1.4mm channel / Ø1.6mm pin
pocket, and you'd still have to strip both ends for the solder joints
anyway. Bare tinned bus wire needs zero prep: cut to length and go.


| Option | Diameter | Verdict |
|---|---|---|
| **24 AWG solid tinned copper bus wire** | **0.51 mm** | ✅ **Best choice** — fits the 1.4 mm channel with clearance, stiff enough to hold a formed bend, thick enough to solder reliably. |
| **Diode legs (1N4148 or similar)** | **~0.52–0.55 mm** | ✅ **Excellent substitute** — virtually the same diameter and material as 24 AWG bus wire. Solid tinned copper, holds bends perfectly, solders identically. Cut-off waste legs from your matrix diodes are perfect; zero cost, zero prep. |
| 22 AWG solid | 0.64 mm | Works too, slightly stiffer/harder to form tight bends around the 1.3mm peg; more force needed. Fine if 24 AWG isn't available. |
| 26–28 AWG (typical stranded hookup wire) | 0.40 mm or stranded | ❌ Avoid — stranded wire won't hold a crisp bend (springs back / kinks). |
| Kynar/Wire-Wrap wire (30 AWG) | 0.25 mm | ❌ Too thin — floppy, won't stay in the channel shape, marginal current capacity. |

**Why solid wire specifically:**
- **Must be solid core, not stranded.** Stranded wire un-twists and springs open after bending — it won't hold the jig's shape once you lift it off the pegs. Solid wire takes a "set" and keeps the bend.
- **Tinned copper** solders cleanly without extra flux/prep and resists oxidation while sitting formed on the bench before assembly.
- Channel width is 1.4 mm and the pin-entry pocket is Ø1.6 mm — 0.51–0.55 mm wire leaves comfortable clearance in both, with room for the solder fillet at the pin joint.

Buy: **one spool of 24 AWG (0.5–0.6 mm) solid tinned copper wire** — or just
use the cut-off legs from your matrix diodes.

---

## Cut-length gauges

The jig has two **horizontal cut-gauge rails** (one per channel) lying flat on
the plate, left side. Each rail is a low bar with an open-top groove running
along it. **Everything is done from above — you never flip the jig.**

Each rail has three parts:

- A solid **stop wall** closing off the left end of the groove.
- An open-top **groove** the wire drops into. Its floor is the plate top
  surface, so the wire lies flat.
- A clean vertical **cut face** at the right end, exactly `cut_length` from
  the stop wall — with a **cutter-relief slot** cut clear through the plate
  immediately past it, so flush-cutter jaws close fully against the face
  without fouling on the plate.

**To pre-cut wires to the exact finished length:**

1. Pick the rail for the channel you're cutting (**CH1** or **CH2**, engraved
   on the plate to the right of each rail with its target length).
2. **Drop the wire into the groove** from above.
3. **Slide it left** until it butts against the stop wall.
4. **Snip flush against the vertical cut face** at the right end of the rail.
   The overhanging tail sits over the open relief slot, so the cutters get
   full clearance.

The stop-wall-to-cut-face distance equals the finished wire length — wire path
plus a 3 mm solder tail at each end:

| Rail | Path length | + tails | = Cut length |
|---|---|---|---|
| **CH1** | 4.5 mm | + 3 + 3 mm | **10.5 mm** |
| **CH2** | 13.2 mm | + 3 + 3 mm | **19.2 mm** |

Every wire you cut this way is identical. You can batch-cut a full tray of
72 wires (36 × CH1 + 36 × CH2) before bending a single one.

**To adjust the solder-tail allowance:** change `solder_tail` in the SCAD
(default 3.0 mm). Both rail lengths recalculate automatically.

---

## How the jig works

The plate has two "lanes," one per wire per key:

- **Lane CH1** — the short, straight channel (Choc pin 1 → PG1425 hole 1,
  ~4.5 mm). One forming peg at the start, a through-hole at the end.
- **Lane CH2** — the long, bent channel (Choc pin 2 → PG1425 hole 2, ~13.2 mm,
  with one interior bend). Two forming pegs (start + bend point), a
  through-hole at the end.

The peg spacing/angle and the hole position are copied **exactly** from the
adapter's own `slots` array in `pg1350_to_pg1425_adapter.scad`, so a wire
formed on the jig drops straight into the real channel with zero fiddling.

A printed ruler (0–20mm) and lane length labels are included for reference.

## How to use it

### Step 1 — Pre-cut wires (horizontal cut-gauge rails)

1. Drop a wire into the **CH1** groove, slide it left to the stop wall, snip
   flush at the cut face. Repeat 36 times (one per key).
2. Same for the **CH2** rail. 36 more cuts.

### Step 2 — Form wires (bending lanes)

3. **Form Lane CH1 (straight wire, 1 bend):**
   - Hook the wire around the single peg.
   - Pull the wire taut along the shallow guide groove toward the end hole.
   - Push the free end straight down through the through-hole — this forms
     a clean 90° downward bend at exactly the right spot and gives a
     consistent ~3mm tail (the hole depth = plate thickness).
4. **Form Lane CH2 (bent wire, 2 bends):**
   - Hook the wire around the **start** peg.
   - Wrap it around the **second (bend)** peg, following the first groove
     segment.
   - Pull taut along the second groove segment toward the end hole.
   - Push the free end down through the through-hole, same as CH1.
5. **Lift the formed wire straight up off the pegs.** It keeps its shape.
6. **Repeat** — every wire comes out identical.
7. **Install per the adapter's assembly steps** (see
   `../electrical_connection_research.md`, Option 2): lay the wire into the
   real channel, solder pin↔wire at the entry pocket, solder the tail into
   the PG1425 plated hole, then seat the switch (its housing caps the
   channel and traps the wire).

## Print settings

- Print flat, pegs facing up, **no supports needed**. The gauge rails are low
  solid bars with open-top grooves (cut from above) and the relief slots are
  straight vertical through-cuts — all fully self-supporting.
- 0.2mm layer height, PLA or PETG.
- The 1.3mm-diameter forming pegs are the finest feature.
- If a peg snaps after heavy repeated use:
  - Reprint with `peg_d` increased to 1.6–1.8mm in the SCAD (slightly wider
    formed bend radius, still fine), or
  - Drill out the broken peg stub and press in a short offcut of steel wire
    or a dowel pin for a near-indestructible version.

## Customizing

All key parameters are at the top of `wire_bending_jig.scad`:

| Parameter | Purpose |
|---|---|
| `wire_d` | Target wire diameter — bump if you switch wire gauge |
| `peg_d` | Forming peg diameter |
| `hole_clear` | Extra clearance on the end through-hole (forming lanes) |
| `plate_t` | Plate thickness = length of the formed tail |
| `solder_tail` | Solder-tail allowance at each end (default 3 mm) — drives cut-gauge rail lengths |
| `gauge_rail_h` / `gauge_rail_w` | Cut-gauge rail height / width |
| `gauge_groove_w` | Cut-gauge groove width (wire seat) |
| `gauge_relief_l` / `gauge_relief_w` | Cutter-relief slot size — enlarge if your flush cutters are bulky |

If the adapter's `slots` geometry in `pg1350_to_pg1425_adapter.scad` is ever
revised, copy the updated point coordinates into the `slots` array at the
top of `wire_bending_jig.scad` to keep the two files in sync.
