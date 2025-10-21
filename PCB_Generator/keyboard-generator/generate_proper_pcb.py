#!/usr/bin/env python3
"""Generate proper KiCad PCB files with complete footprints."""

from pathlib import Path
import uuid


def generate_mx_switch_footprint(ref, x, y, rotation=0):
    """Generate Cherry MX switch footprint with pads."""
    return f"""  (footprint "Button_Switch_Keyboard:SW_Cherry_MX_PCB_1.00u" (layer "F.Cu")
    (tstamp {uuid.uuid4()})
    (at {x} {y} {rotation})
    (descr "Cherry MX keyswitch PCB Mount Keycap 1.00u")
    (property "Reference" "{ref}" (at 0 -8 {rotation}) (layer "F.SilkS")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
    (property "Value" "SW_Push" (at 0 8 {rotation}) (layer "F.Fab")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
    (fp_line (start -7 -7) (end -7 7) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp {uuid.uuid4()}))
    (fp_line (start -7 7) (end 7 7) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp {uuid.uuid4()}))
    (fp_line (start 7 -7) (end -7 -7) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp {uuid.uuid4()}))
    (fp_line (start 7 7) (end 7 -7) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp {uuid.uuid4()}))
    (pad "1" thru_hole circle (at -3.81 -2.54 {rotation}) (size 2.2 2.2) (drill 1.5) (layers "*.Cu" "*.Mask") (tstamp {uuid.uuid4()}))
    (pad "2" thru_hole circle (at 2.54 -5.08 {rotation}) (size 2.2 2.2) (drill 1.5) (layers "*.Cu" "*.Mask") (tstamp {uuid.uuid4()}))
  )
"""


def generate_diode_footprint(ref, x, y, rotation=0):
    """Generate 1N4148 diode footprint."""
    return f"""  (footprint "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal" (layer "F.Cu")
    (tstamp {uuid.uuid4()})
    (at {x} {y} {rotation})
    (descr "Diode, DO-35_SOD27 series, Axial, Horizontal, pin pitch=7.62mm")
    (property "Reference" "{ref}" (at 3.81 -2 {rotation}) (layer "F.SilkS")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
    (property "Value" "1N4148" (at 3.81 2 {rotation}) (layer "F.Fab")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
    (fp_line (start 1.04 0) (end 1.69 0) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp {uuid.uuid4()}))
    (fp_line (start 5.93 0) (end 6.58 0) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp {uuid.uuid4()}))
    (pad "1" thru_hole rect (at 0 0 {rotation}) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (tstamp {uuid.uuid4()}))
    (pad "2" thru_hole oval (at 7.62 0 {rotation}) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (tstamp {uuid.uuid4()}))
  )
"""


def generate_atmega328p_footprint(ref, x, y, rotation=0):
    """Generate ATmega328P DIP-28 footprint."""
    pads = ""
    for i in range(1, 15):
        y_pos = (i-1) * 2.54
        pads += f'    (pad "{i}" thru_hole oval (at 0 {y_pos} {rotation}) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (tstamp {uuid.uuid4()}))\n'
    for i in range(15, 29):
        y_pos = (28-i) * 2.54
        pads += f'    (pad "{i}" thru_hole oval (at 7.62 {y_pos} {rotation}) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (tstamp {uuid.uuid4()}))\n'
    
    return f"""  (footprint "Package_DIP:DIP-28_W7.62mm" (layer "F.Cu")
    (tstamp {uuid.uuid4()})
    (at {x} {y} {rotation})
    (descr "28-lead though-hole mounted DIP package, row spacing 7.62 mm (300 mils)")
    (property "Reference" "{ref}" (at 3.81 -2 {rotation}) (layer "F.SilkS")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
    (property "Value" "ATmega328P-PU" (at 3.81 35 {rotation}) (layer "F.Fab")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
{pads}  )
"""


def generate_usb_c_footprint(ref, x, y, rotation=0):
    """Generate USB-C connector footprint."""
    return f"""  (footprint "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12" (layer "F.Cu")
    (tstamp {uuid.uuid4()})
    (at {x} {y} {rotation})
    (descr "USB Type-C receptacle for USB 2.0")
    (property "Reference" "{ref}" (at 0 -5 {rotation}) (layer "F.SilkS")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
    (property "Value" "USB_C" (at 0 5 {rotation}) (layer "F.Fab")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
    (pad "A1" smd rect (at -3.25 0 {rotation}) (size 0.6 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "A4" smd rect (at -2.45 0 {rotation}) (size 0.6 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "A5" smd rect (at -1.25 0 {rotation}) (size 0.3 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "A6" smd rect (at -0.25 0 {rotation}) (size 0.3 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "A7" smd rect (at 0.25 0 {rotation}) (size 0.3 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "A8" smd rect (at 1.25 0 {rotation}) (size 0.3 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "A9" smd rect (at 2.45 0 {rotation}) (size 0.6 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "A12" smd rect (at 3.25 0 {rotation}) (size 0.6 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "B1" smd rect (at 3.25 0 {rotation}) (size 0.6 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "B4" smd rect (at 2.45 0 {rotation}) (size 0.6 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "B5" smd rect (at 1.25 0 {rotation}) (size 0.3 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "B6" smd rect (at 0.25 0 {rotation}) (size 0.3 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "B7" smd rect (at -0.25 0 {rotation}) (size 0.3 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "B8" smd rect (at -1.25 0 {rotation}) (size 0.3 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "B9" smd rect (at -2.45 0 {rotation}) (size 0.6 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "B12" smd rect (at -3.25 0 {rotation}) (size 0.6 1.8) (layers "F.Cu" "F.Paste" "F.Mask") (tstamp {uuid.uuid4()}))
    (pad "S1" thru_hole oval (at -4.32 0 {rotation}) (size 1 2.1) (drill oval 0.6 1.7) (layers "*.Cu" "*.Mask") (tstamp {uuid.uuid4()}))
    (pad "S1" thru_hole oval (at 4.32 0 {rotation}) (size 1 2.1) (drill oval 0.6 1.7) (layers "*.Cu" "*.Mask") (tstamp {uuid.uuid4()}))
  )
"""


def generate_resistor_footprint(ref, value, x, y, rotation=0):
    """Generate resistor footprint."""
    return f"""  (footprint "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" (layer "F.Cu")
    (tstamp {uuid.uuid4()})
    (at {x} {y} {rotation})
    (descr "Resistor, Axial_DIN0204 series")
    (property "Reference" "{ref}" (at 3.81 -2 {rotation}) (layer "F.SilkS")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
    (property "Value" "{value}" (at 3.81 2 {rotation}) (layer "F.Fab")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
    (pad "1" thru_hole circle (at 0 0 {rotation}) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (tstamp {uuid.uuid4()}))
    (pad "2" thru_hole oval (at 7.62 0 {rotation}) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (tstamp {uuid.uuid4()}))
  )
"""


def generate_capacitor_footprint(ref, value, x, y, rotation=0):
    """Generate capacitor footprint."""
    return f"""  (footprint "Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm" (layer "F.Cu")
    (tstamp {uuid.uuid4()})
    (at {x} {y} {rotation})
    (descr "C, Disc series, Radial")
    (property "Reference" "{ref}" (at 1.25 -2 {rotation}) (layer "F.SilkS")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
    (property "Value" "{value}" (at 1.25 2 {rotation}) (layer "F.Fab")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
    (pad "1" thru_hole circle (at 0 0 {rotation}) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (tstamp {uuid.uuid4()}))
    (pad "2" thru_hole circle (at 2.5 0 {rotation}) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (tstamp {uuid.uuid4()}))
  )
"""


def generate_crystal_footprint(ref, x, y, rotation=0):
    """Generate crystal footprint."""
    return f"""  (footprint "Crystal:Crystal_HC49-U_Vertical" (layer "F.Cu")
    (tstamp {uuid.uuid4()})
    (at {x} {y} {rotation})
    (descr "Crystal HC-49/U, Vertical")
    (property "Reference" "{ref}" (at 0 -6 {rotation}) (layer "F.SilkS")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
    (property "Value" "16MHz" (at 0 6 {rotation}) (layer "F.Fab")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
    (pad "1" thru_hole circle (at -2.45 0 {rotation}) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (tstamp {uuid.uuid4()}))
    (pad "2" thru_hole circle (at 2.45 0 {rotation}) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (tstamp {uuid.uuid4()}))
  )
"""


def generate_3x3_macropad():
    """Generate 3x3 macropad PCB."""
    print("\n" + "="*80)
    print("Generating 3x3 Macropad PCB with Complete Footprints")
    print("="*80 + "\n")
    
    output_dir = Path('output/3x3-proper')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pcb_content = f"""(kicad_pcb (version 20221018) (generator thkg)

  (general
    (thickness 1.6)
  )

  (paper "A4")
  
  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (32 "B.Adhes" user "B.Adhesive")
    (33 "F.Adhes" user "F.Adhesive")
    (34 "B.Paste" user)
    (35 "F.Paste" user)
    (36 "B.SilkS" user "B.Silkscreen")
    (37 "F.SilkS" user "F.Silkscreen")
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (40 "Dwgs.User" user "User.Drawings")
    (41 "Cmts.User" user "User.Comments")
    (42 "Eco1.User" user "User.Eco1")
    (43 "Eco2.User" user "User.Eco2")
    (44 "Edge.Cuts" user)
    (45 "Margin" user)
    (46 "B.CrtYd" user "B.Courtyard")
    (47 "F.CrtYd" user "F.Courtyard")
    (48 "B.Fab" user)
    (49 "F.Fab" user)
  )

  (setup
    (pad_to_mask_clearance 0)
    (pcbplotparams
      (layerselection 0x00010fc_ffffffff)
      (plot_on_all_layers_selection 0x0000000_00000000)
      (disableapertmacros false)
      (usegerberextensions false)
      (usegerberattributes true)
      (usegerberadvancedattributes true)
      (creategerberjobfile true)
      (svgprecision 4)
      (plotframeref false)
      (viasonmask false)
      (mode 1)
      (useauxorigin false)
      (hpglpennumber 1)
      (hpglpenspeed 20)
      (hpglpendiameter 15.000000)
      (psnegative false)
      (psa4output false)
      (plotreference true)
      (plotvalue true)
      (plotinvisibletext false)
      (sketchpadsonfab false)
      (subtractmaskfromsilk false)
      (outputformat 1)
      (mirror false)
      (drillshape 1)
      (scaleselection 1)
      (outputdirectory "")
    )
  )

  (net 0 "")
  (net 1 "GND")
  (net 2 "VCC")
  (net 3 "COL0")
  (net 4 "COL1")
  (net 5 "COL2")
  (net 6 "ROW0")
  (net 7 "ROW1")
  (net 8 "ROW2")

  (gr_line (start 0 0) (end 285 0) (stroke (width 0.1) (type solid)) (layer "Edge.Cuts") (tstamp {uuid.uuid4()}))
  (gr_line (start 285 0) (end 285 94.6) (stroke (width 0.1) (type solid)) (layer "Edge.Cuts") (tstamp {uuid.uuid4()}))
  (gr_line (start 285 94.6) (end 0 94.6) (stroke (width 0.1) (type solid)) (layer "Edge.Cuts") (tstamp {uuid.uuid4()}))
  (gr_line (start 0 94.6) (end 0 0) (stroke (width 0.1) (type solid)) (layer "Edge.Cuts") (tstamp {uuid.uuid4()}))

"""
    
    # Add switches in 3x3 grid (19.05mm spacing)
    switch_spacing = 19.05
    start_x = 50
    start_y = 30
    
    for row in range(3):
        for col in range(3):
            x = start_x + col * switch_spacing
            y = start_y + row * switch_spacing
            ref = f"SW{row}{col}"
            pcb_content += generate_mx_switch_footprint(ref, x, y)
            
            # Add diode below each switch
            diode_ref = f"D{row}{col}"
            diode_y = y + 8  # 8mm below switch
            pcb_content += generate_diode_footprint(diode_ref, x, diode_y, 90)
    
    # Add MCU (center-bottom)
    pcb_content += generate_atmega328p_footprint("U1", 142.5, 70)
    
    # Add USB-C (top center)
    pcb_content += generate_usb_c_footprint("J1", 142.5, 10, 90)
    
    # Add resistors (near MCU)
    pcb_content += generate_resistor_footprint("R1", "1.5k", 120, 65, 90)
    pcb_content += generate_resistor_footprint("R2", "75R", 125, 65, 90)
    pcb_content += generate_resistor_footprint("R3", "75R", 130, 65, 90)
    pcb_content += generate_resistor_footprint("R4", "5.1k", 135, 65, 90)
    pcb_content += generate_resistor_footprint("R5", "5.1k", 140, 65, 90)
    
    # Add capacitors
    pcb_content += generate_capacitor_footprint("C1", "22pF", 155, 70)
    pcb_content += generate_capacitor_footprint("C2", "22pF", 155, 75)
    pcb_content += generate_capacitor_footprint("C3", "100nF", 155, 80)
    pcb_content += generate_capacitor_footprint("C4", "100nF", 155, 85)
    
    # Add crystal
    pcb_content += generate_crystal_footprint("Y1", 160, 77.5)
    
    # Add mounting holes (GH60 standard)
    mounting_holes = [
        (19.0, 9.5), (266.0, 9.5),
        (28.5, 47.3), (256.5, 47.3),
        (57.0, 85.0), (228.0, 85.0),
    ]
    
    for i, (x, y) in enumerate(mounting_holes, 1):
        pcb_content += f"""  (footprint "MountingHole:MountingHole_2.2mm_M2" (layer "F.Cu")
    (tstamp {uuid.uuid4()})
    (at {x} {y})
    (descr "Mounting Hole 2.2mm, no annular")
    (property "Reference" "H{i}" (at 0 -3 0) (layer "F.SilkS")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
    (property "Value" "MountingHole" (at 0 3 0) (layer "F.Fab")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp {uuid.uuid4()})
    )
    (pad "" np_thru_hole circle (at 0 0) (size 2.2 2.2) (drill 2.2) (layers "*.Cu" "*.Mask") (tstamp {uuid.uuid4()}))
  )

"""
    
    pcb_content += ")\n"
    
    # Write file
    pcb_file = output_dir / "3x3-Macropad.kicad_pcb"
    with open(pcb_file, 'w') as f:
        f.write(pcb_content)
    
    print(f"✅ Generated: {pcb_file}")
    print(f"   • 9 switches with footprints")
    print(f"   • 9 diodes")
    print(f"   • ATmega328P MCU")
    print(f"   • USB-C connector")
    print(f"   • 5 resistors")
    print(f"   • 4 capacitors")
    print(f"   • 1 crystal")
    print(f"   • 6 mounting holes")
    print(f"   • Complete pad definitions")
    
    return pcb_file


if __name__ == '__main__':
    print("\n🔧 Proper KiCad PCB Generator")
    print("="*80)
    print("Generating PCB files with complete footprint definitions")
    print("="*80)
    
    pcb_file = generate_3x3_macropad()
    
    print("\n" + "="*80)
    print("✅ PCB generated successfully!")
    print("="*80)
    print(f"\nYou can now open this file in KiCad or an online viewer:")
    print(f"  {pcb_file}")
    print("\nThis file includes:")
    print("  • Complete footprint definitions with pads")
    print("  • Proper pad sizes and drill holes")
    print("  • Silkscreen and fab layers")
    print("  • GH60-compatible board outline")
    print("  • Standard mounting holes")
    print()
