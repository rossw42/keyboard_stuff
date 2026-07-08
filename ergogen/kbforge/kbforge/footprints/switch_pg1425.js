// kbforge custom Ergogen footprint: Kailh PG1425 "Choc X" switch
//
// Geometry translated from the verified KiCad footprint
// shikamiya/kicad-footprint-kailh-pg1425-x-switch
// (saved locally as projects/switch_converter/Kailh-PG1425-X-Switch.kicad_mod).
// The original module's origin is NOT the switch center; all coordinates
// below have been re-centered on the switch center (the module center sat
// at (-3.4, 2.9) in module-local coordinates, so everything is shifted by
// (+3.4, -2.9)). Coordinates are KiCad footprint-local (y-down).
//
// Features (relative to switch center):
//   * 2 plated pin holes, drill 1.10:
//       pad 1 at (-3.4, -2.9)  -> `from` net (column)
//       pad 2 at (-3.4,  2.0)  -> `to` net (colrow)
//   * 2 non-plated alignment holes, drill 1.30 at (5.5, 5.5) / (-5.5, -5.5)
//   * large non-plated center cutout ~5.1 x 4.1 mm (rounded), centered
//     at (0, 0.9), built from overlapping NPTH oval pads exactly as in
//     the source footprint
//
// This footprint pairs with the PG1350->PG1425 switch-converter adapter
// (projects/switch_converter/OpenSCAD/pg1350_to_pg1425_adapter.scad):
// the adapter's alignment pins drop into the two 1.3mm NPTH holes and
// its routing slots deliver the Choc pins to the two plated holes.
//
// Emitted in KiCad 8 syntax — use with Ergogen `template: kicad8`
// (kbforge's default when footprint_lib is "ceoloide").
//
// Params:
//   side: default F — silkscreen side
//   from: net for pin 1 (kbforge wires the column net here)
//   to:   net for pin 2 (kbforge wires {{colrow}} here)

module.exports = {
  params: {
    designator: 'S',
    side: 'F',
    from: { type: 'net', value: undefined },
    to: { type: 'net', value: undefined }
  },
  body: p => `
  (footprint "kbforge:switch_pg1425"
    (layer "${p.side}.Cu")
    ${p.at}
    (property "Reference" "${p.ref}"
      (at 0 -8.5 ${p.r})
      (layer "${p.side}.SilkS")
      ${p.ref_hide}
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (attr through_hole)
    (fp_line (start -7.4 -7) (end 7.4 -7) (layer "${p.side}.SilkS") (stroke (width 0.15) (type solid)))
    (fp_line (start 7.4 -7) (end 7.4 7) (layer "${p.side}.SilkS") (stroke (width 0.15) (type solid)))
    (fp_line (start 7.4 7) (end -7.4 7) (layer "${p.side}.SilkS") (stroke (width 0.15) (type solid)))
    (fp_line (start -7.4 7) (end -7.4 -7) (layer "${p.side}.SilkS") (stroke (width 0.15) (type solid)))
    (fp_line (start -9.525 -9.525) (end 9.525 -9.525) (layer "F.Fab") (stroke (width 0.15) (type solid)))
    (fp_line (start 9.525 -9.525) (end 9.525 9.525) (layer "F.Fab") (stroke (width 0.15) (type solid)))
    (fp_line (start 9.525 9.525) (end -9.525 9.525) (layer "F.Fab") (stroke (width 0.15) (type solid)))
    (fp_line (start -9.525 9.525) (end -9.525 -9.525) (layer "F.Fab") (stroke (width 0.15) (type solid)))
    (fp_line (start -2.55 2.95) (end 2.55 2.95) (layer "F.Fab") (stroke (width 0.15) (type solid)))
    (fp_line (start 2.55 2.95) (end 2.55 6.55) (layer "F.Fab") (stroke (width 0.15) (type solid)))
    (fp_line (start 2.55 6.55) (end -2.55 6.55) (layer "F.Fab") (stroke (width 0.15) (type solid)))
    (fp_line (start -2.55 6.55) (end -2.55 2.95) (layer "F.Fab") (stroke (width 0.15) (type solid)))
    (fp_line (start -8.255 -8.255) (end 8.255 -8.255) (layer "F.CrtYd") (stroke (width 0.12) (type solid)))
    (fp_line (start 8.255 -8.255) (end 8.255 8.255) (layer "F.CrtYd") (stroke (width 0.12) (type solid)))
    (fp_line (start 8.255 8.255) (end -8.255 8.255) (layer "F.CrtYd") (stroke (width 0.12) (type solid)))
    (fp_line (start -8.255 8.255) (end -8.255 -8.255) (layer "F.CrtYd") (stroke (width 0.12) (type solid)))
    (pad "" np_thru_hole oval (at 0 -1 ${p.r}) (size 5.1 0.3) (drill oval 5.1 0.3) (layers "*.Cu" "*.Mask"))
    (pad "" np_thru_hole oval (at 0 2.8 ${p.r}) (size 5.1 0.3) (drill oval 5.1 0.3) (layers "*.Cu" "*.Mask"))
    (pad "" np_thru_hole oval (at -2.4 0.9 ${p.r}) (size 0.3 4.1) (drill oval 0.3 4.1) (layers "*.Cu" "*.Mask"))
    (pad "" np_thru_hole oval (at 2.4 0.9 ${p.r}) (size 0.3 4.1) (drill oval 0.3 4.1) (layers "*.Cu" "*.Mask"))
    (pad "" np_thru_hole oval (at -1.55 0.9 ${p.r}) (size 2 4.1) (drill oval 2 4.1) (layers "*.Cu" "*.Mask"))
    (pad "" np_thru_hole oval (at 1.55 0.9 ${p.r}) (size 2 4.1) (drill oval 2 4.1) (layers "*.Cu" "*.Mask"))
    (pad "" np_thru_hole oval (at 0 0.9 ${p.r}) (size 5.1 4.1) (drill oval 5.1 4.1) (layers "*.Cu" "*.Mask"))
    (pad "" np_thru_hole circle (at 5.5 5.5 ${p.r}) (size 1.3 1.3) (drill 1.3) (layers "*.Cu" "*.Mask"))
    (pad "" np_thru_hole circle (at -5.5 -5.5 ${p.r}) (size 1.3 1.3) (drill 1.3) (layers "*.Cu" "*.Mask"))
    (pad "1" thru_hole circle (at -3.4 -2.9 ${p.r}) (size 1.6 1.6) (drill 1.1) (layers "*.Cu" "*.Mask") ${p.from.str})
    (pad "2" thru_hole circle (at -3.4 2 ${p.r}) (size 1.4 1.4) (drill 1.1) (layers "*.Cu" "*.Mask") ${p.to.str})
  )
  `
}