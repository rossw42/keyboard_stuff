# Electrical Connection Deep Dive — PG1350 → PG1425 Adapter

**Goal:** Carry the electrical signal from the PG1350 (Choc V1) switch pins, through the 3D-printed adapter, down into the PG1425 plated through-holes — with **zero added height**, everything **above the board**, at **0° rotation**, using the existing v3 adapter geometry.

**Ground truth:** `OpenSCAD/pg1350_to_pg1425_adapter.scad` (**v3.1**, latest STL: `pg1350_to_pg1425_adapter.stl`; the previous v3 STL is preserved as `pg1350_to_pg1425_adapter_v3_backup.stl`). All dimensions below are taken from that file, not from datasheets or guesses.

![The captive-channel solution](diagrams/in_slot_solution.svg)

## 0. v3.1 change — captive wire channels

The v3 through-slots were open top **and** bottom, so a wire laid in them could fall out. v3.1 converts each slot into a **captive channel**:

- A **0.5 mm floor membrane** (`channel_membrane_t`) now closes the channel bottom — the wire rests on it and cannot drop out.
- The channel remains **open at the top** (into the Choc pocket): the wire is laid in from above during assembly, and once the switch is seated its housing caps the channel — the wire is fully trapped.
- Through-openings survive at exactly two spots per channel:
  - **Pin entry pocket** (φ1.6, `pin_entry_pocket_d`) at each Choc pin position — full floor depth so the 2.65 mm pin descends fully and the pin↔wire solder joint is reachable
  - **Wire exit hole** (φ1.4, `wire_exit_hole_d`) directly over each PG1425 plated hole — the wire's end bends down through it into the PCB
- `wire_channel = false` restores the old v3 through-slots if ever needed.
- Renders verified: `OpenSCAD/adapter_v31_top.png` (channels visible in pocket floor) and `adapter_v31_bottom.png` (bottom face closed except post holes, pin pockets, exit holes, alignment pins).

---

## 1. Hard Constraints (from the v3 adapter)

| Parameter | Value | Consequence for contacts |
|---|---|---|
| Floor thickness | **2.80 mm** (`floor_h`) | Any contact must fit *within* 2.8 mm of vertical space |
| Total block height | 5.00 mm (2.8 floor + 2.2 bezel) | Bezel space is occupied by the Choc body — unusable |
| Choc pin length | 2.65 mm, ends 0.15 mm above PCB | Pin reaches almost to the PCB surface *inside the floor* |
| Routing channels (v3.1) | 1.4 mm wide, 0.5 mm membrane below, open top | Wire is captive: 1.4 × 2.3 mm channel, wire can't fall out |
| Channel 1 path | (0, 5.9) → (-3.4, 2.9) — **4.53 mm** straight | Short bridge |
| Channel 2 path | (5.0, 3.8) → (2.4, -3.0) → (-3.4, -2.0) — **~13.2 mm** with a bend | Long bridge, detours around center/side-post pockets |
| PG1425 pin holes | φ1.10 plated, at (-3.4, 2.9) and (-3.4, -2.0) | Solder target below each slot end |
| Bottom protrusions | ONLY the two φ1.3 alignment pins | Nothing else may hang below z=0 |
| Orientation | **0° — fixed.** | No switch rotation |

### Options ruled out by these constraints

| Option | Why it fails |
|---|---|
| **Mill-Max receptacles** (0300/0667 tailed, 7305/0305 no-tail) | Body alone is ~4.3 mm — 1.5 mm taller than the entire floor. Would lift the switch and add height. Also can't bridge the 4.5/13 mm lateral runs. ❌ |
| **Whole Kailh hotswap socket** (CPG135001S30) | Housing is ~1.8 mm thick and mounts *below* a PCB; our adapter is entirely *above* the PCB, so the socket would need its own pocket + web ≈ +1.8 mm stack height. ❌ |
| **Machined header barrels** | Same height problem as Mill-Max. ❌ |
| **Interposer PCB** | +1.6 mm and against project architecture. ❌ |
| **90° switch rotation** | Rejected (keycap orientation), and the earlier jog math used a wrong footprint center. Dead end — do not revisit. ❌ |

**Conclusion: no off-the-shelf socket/receptacle fits inside a 2.8 mm floor.** The commercial parts are all built for through-PCB mounting and are simply too tall. The contact has to be something *thin and lying in the slot* — which is exactly what the v3 design anticipated ("a bent Choc pin, wire, or stamped contact routes through the slot").

---

## 2. What CAN work inside the slots

The slot is a 1.4 × 2.8 mm channel, open at top and bottom, running from under the Choc pin to directly above the PG1425 hole. The Choc pin descends 2.65 mm into the slot. Three viable fills, from most-buyable to most-manual:

### Option 1 — Harvested Kailh hotswap contacts (buyable metal, right geometry) ⭐

The metal stamping *inside* a Kailh Choc hotswap socket (CPG135001S30, ~$0.25) is the closest thing on Earth to our ideal part:
- **~0.3 mm thick phosphor bronze** — fits the 1.4 mm slot with room to spare
- Contact assembly is **~1.8 mm tall** — fits inside the 2.8 mm floor
- Its mouth is **designed to grip a vertically-inserted Choc pin** — solderless top interface
- Its flat leg extends horizontally ~2–3 mm ⚠ from the pin — heads *along* the slot in the right direction

**How:** crack the plastic housing (it's two thin shells), pull the two stampings, and drop each one into a **shaped pocket** widened from the existing slot (SCAD change: local slot widening at the pin entry to hold the contact mouth captive; the plastic itself becomes the housing). 
- **Slot 1 (4.53 mm):** the contact's own leg covers ~half the run. Bridge the remainder by either (a) extending with a soldered stub of the same strip/wire, or (b) positioning the pocket so the leg end lands over the hole — needs a measurement of the real stamping (⚠ leg length unknown until we hold one).
- **Slot 2 (~13 mm):** the leg can't reach; the contact grips the pin and a bus-wire segment soldered to the leg runs the rest of the slot and drops into the hole.

**Verdict:** best solderless-top option that respects the height budget. Requires one harvesting step and a SCAD pocket revision. Buy 10 sockets (~$2.50) and measure the stampings with calipers first.

### Option 2 — Jig-formed bus wire in the captive channel (simplest, zero height, works with v3.1) ⭐

The channel *is* the forming jig **and** the retainer. Buyable material: **0.6 mm (22–24 AWG) tinned copper bus wire**, by the spool, ~$5.

Per pin (v3.1 assembly):
1. Cut a length ~2 mm longer than the channel path.
2. Lay it into the channel **from above** (channel is open at the top); it follows the path including channel 2's bend and rests on the 0.5 mm membrane — it cannot fall out the bottom.
3. Bend the last ~2.3 mm down through the **wire exit hole** — it drops into the φ1.1 PG1425 hole below.
4. Seat the switch: its housing caps the channel (wire fully captive), and the Choc pin descends into the **pin entry pocket** alongside the wire's start.
5. Solder pin↔wire at the entry pocket (accessible from below through the pocket), then solder the wire tail in the PCB hole from underneath.

**Verdict:** adds exactly 0.0 mm of height, wire is mechanically trapped by membrane + switch body, and every wire is identical because the channel jigs the bends. 2 solder joints per pin. This is the plan of record with the v3.1 STL.

Variant: **nickel strip** (battery-tab strip, 0.1–0.15 mm thick, buyable in rolls) cut into 1.3 mm wide ribbons — flat, springy, solderable, sits even lower in the channel. More cutting work than wire; worth one experiment.

### Option 3 — Direct solder, no bridge (only if hole reach allows)

The Choc pin ends 0.15 mm above the PCB, but it's 4.5 mm sideways from the hole — so this only works if a future adapter revision could shift... it can't (the geometry is fixed by the two footprints). Listed only for completeness: **not viable at 0°.** The bridge (Option 1 or 2) is unavoidable.

---

## 3. Comparison (constraint-respecting options only)

| | 1: Harvested Kailh contact | 2: Bus wire in channel | 2b: Nickel strip in channel |
|---|---|---|---|
| Added height | 0 | 0 | 0 |
| Fits current (v3.1) STL unmodified | ❌ needs pocket revision | ✅ | ✅ |
| Solderless switch insertion (hotswap top) | ✅ | ❌ (pin soldered to wire) | ❌ |
| Switch removable later | ✅ easily | ⚠ desolder 1 joint | ⚠ desolder 1 joint |
| Buyable component | ✅ socket $0.25 (harvest 2 contacts) | ✅ wire spool | ✅ strip roll |
| Manual steps per key | Harvest + seat 2 contacts + 1–2 solder | Form 2 wires (slot-jigged) + 4 solder | Cut 2 strips + 4 solder |
| Unknowns | Stamping dimensions ⚠, pocket design | none — works today | strip width cutting |

---

## 4. Recommendation

1. **Prototype NOW with Option 2 (bus wire in the v3.1 captive channels).** Zero added height, wire mechanically retained, proves the electrical path end-to-end with the current STL. Buy: one spool of 0.6 mm tinned bus wire.
2. **In parallel, buy 10 Kailh Choc hotswap sockets and harvest the contacts.** Measure the stamping (mouth width, height, leg length/direction) with calipers. If the mouth fits a widened slot pocket within the 2.8 mm floor — and it should, at ~1.8 mm tall — revise the SCAD with contact pockets for a solderless-top v4. This *is* the project's "dual-ended stamped contact" architecture, using Kailh's own stamping as the contact.
3. Long-term (if v4 works well and volumes justify it): a custom stamped contact combining the Kailh-style mouth with a full-length slot leg — but only after v4 proves the pocket geometry.

## 5. Next Steps

- [ ] Print the v3.1 STL; verify the 0.5 mm membrane prints cleanly (it bridges a 1.4 mm span — trivial for FDM)
- [ ] Buy: 0.6 mm tinned copper bus wire spool; 10× Kailh Choc hotswap sockets (CPG135001S30)
- [ ] Wire prototype: lay 2 wires into the channels, seat switch, assemble on a PG1425 PCB, continuity + actuation test
- [ ] Harvest 2 contacts from a socket; measure with calipers: overall height, mouth width/depth, leg length, thickness
- [ ] If contact fits: revise SCAD — widen slot locally into a contact pocket at each Choc pin position (keep floor at 2.8 mm)
- [ ] Re-verify slot 2's detour path clears the seated contact + wire extension

---

## Appendix A — Terminology: what is a "solder tail"? (kept for reference)

A Mill-Max style receptacle is machined from one piece of brass: a **mouth** (funnel + internal spring fingers that grip an inserted pin — the hotswap part), a **barrel** (press-fit sleeve), and a **solder tail** (solid ~0.64 mm pin out the bottom that normally goes through a plated PCB hole and is soldered like a resistor leg). See `diagrams/receptacle_anatomy.svg`.

Verified tailed part, for future reference only (REJECTED for this adapter — 4.3 mm body > 2.8 mm floor): **Mill-Max 0300-1-15-15-47-27-10-0**, DigiKey, "Standard Tail", ~$0.79. Note most keyboard-community Mill-Max parts (7305, 0305-2) are "**No Tail**" — flush-bottom.

## Appendix B — PG1425 footprint facts (from `Kailh-PG1425-X-Switch.kicad_mod`, matching the SCAD)

- Footprint is **through-hole**: 2 plated holes, φ1.10 drill, at (-3.4, 2.9) and (-3.4, -2.0) relative to switch center (SCAD/OpenSCAD Y-up convention)
- 2 non-plated φ1.30 alignment holes at (5.5, -5.5) and (-5.5, 5.5) — engaged by the adapter's printed pins
- Central open cutout ~5.1 × 4.1 mm at (0, -0.9)

## Appendix C — Superseded research

Earlier drafts of this document proposed Mill-Max receptacles, whole hotswap sockets under the floor, and a 90° switch rotation. All were **rejected** against the v3 constraints (height budget, above-board-only, fixed 0° orientation, and corrected footprint coordinates). Diagrams `option_a_millmax_section.svg` and `option_b_choc_socket_section.svg` illustrate those rejected concepts and are retained for the record only.