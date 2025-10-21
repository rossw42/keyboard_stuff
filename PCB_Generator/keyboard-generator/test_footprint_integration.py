#!/usr/bin/env python3
"""Test footprint integration in PCB file generation."""

from pathlib import Path
from thkg.pcb.footprint_library import get_library


def test_footprint_integration():
    """Test generating a PCB file with complete footprints."""
    print("Testing Footprint Integration in PCB File")
    print("=" * 80)
    
    # Get library
    library = get_library()
    
    # Create a simple PCB file with a few components
    print("\n🔨 Generating test PCB file...")
    
    pcb_content = """(kicad_pcb (version 20221018) (generator thkg)

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
  (net 4 "ROW0")

"""
    
    # Add board outline (80mm x 80mm for 3x3 macropad)
    pcb_content += """  (gr_line (start 0 0) (end 80 0) (layer "Edge.Cuts") (stroke (width 0.1) (type solid)) (tstamp 00000000-0000-0000-0000-000000000001))
  (gr_line (start 80 0) (end 80 80) (layer "Edge.Cuts") (stroke (width 0.1) (type solid)) (tstamp 00000000-0000-0000-0000-000000000002))
  (gr_line (start 80 80) (end 0 80) (layer "Edge.Cuts") (stroke (width 0.1) (type solid)) (tstamp 00000000-0000-0000-0000-000000000003))
  (gr_line (start 0 80) (end 0 0) (layer "Edge.Cuts") (stroke (width 0.1) (type solid)) (tstamp 00000000-0000-0000-0000-000000000004))

"""
    
    # Add complete footprints from library
    print("   📦 Adding footprints from library...")
    
    # Add 3x3 grid of switches
    switch_count = 0
    for row in range(3):
        for col in range(3):
            x = 20 + (col * 19.05)  # 19.05mm spacing
            y = 20 + (row * 19.05)
            ref = f"SW{row * 3 + col + 1}"
            
            footprint = library.get_footprint(
                "lumberjack:MX",
                ref,
                (x, y),
                rotation=0,
                net_map={"1": 3 + col, "2": 6 + row}
            )
            
            if footprint:
                pcb_content += footprint + "\n\n"
                switch_count += 1
                print(f"      ✅ Added {ref} at ({x:.1f}, {y:.1f})")
            else:
                print(f"      ❌ Failed to add {ref}")
    
    # Add 3x3 grid of diodes
    diode_count = 0
    for row in range(3):
        for col in range(3):
            x = 20 + (col * 19.05)
            y = 30 + (row * 19.05)  # 10mm below switch
            ref = f"D{row * 3 + col + 1}"
            
            footprint = library.get_footprint(
                "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal",
                ref,
                (x, y),
                rotation=90,
                net_map={"1": 6 + row, "2": 3 + col}
            )
            
            if footprint:
                pcb_content += footprint + "\n\n"
                diode_count += 1
                print(f"      ✅ Added {ref} at ({x:.1f}, {y:.1f})")
            else:
                print(f"      ❌ Failed to add {ref}")
    
    # Close PCB file
    pcb_content += ")\n"
    
    # Write to file
    output_dir = Path("output/test-footprint")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "test-3x3-macropad.kicad_pcb"
    
    print(f"\n💾 Writing PCB file...")
    with open(output_file, 'w') as f:
        f.write(pcb_content)
    
    # Analyze output
    lines = pcb_content.count('\n')
    size = len(pcb_content)
    
    print(f"\n📊 PCB File Statistics:")
    print(f"   • File: {output_file}")
    print(f"   • Size: {size:,} bytes")
    print(f"   • Lines: {lines:,}")
    print(f"   • Switches: {switch_count}")
    print(f"   • Diodes: {diode_count}")
    
    # Count footprint elements
    fp_line_count = pcb_content.count('(fp_line ')
    fp_text_count = pcb_content.count('(fp_text ')
    fp_circle_count = pcb_content.count('(fp_circle ')
    pad_count = pcb_content.count('(pad ')
    
    print(f"\n📊 Footprint Details:")
    print(f"   • fp_line elements: {fp_line_count}")
    print(f"   • fp_text elements: {fp_text_count}")
    print(f"   • fp_circle elements: {fp_circle_count}")
    print(f"   • Pads: {pad_count}")
    
    # Compare to targets
    print(f"\n📈 Comparison:")
    print(f"   • Previous generated PCBs: ~500 lines")
    print(f"   • This PCB: {lines:,} lines")
    print(f"   • Improvement: {lines / 500:.1f}x larger")
    
    if lines > 2000:
        print(f"   ✅ Excellent! Much more complete than before")
    elif lines > 1000:
        print(f"   ✅ Good! Significant improvement")
    else:
        print(f"   ⚠️  Still needs more content")
    
    print("\n" + "=" * 80)
    print("✅ Footprint integration test complete!")
    print(f"📁 Output: {output_file}")


if __name__ == "__main__":
    test_footprint_integration()
