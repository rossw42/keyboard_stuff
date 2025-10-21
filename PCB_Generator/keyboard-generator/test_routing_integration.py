#!/usr/bin/env python3
"""Test routing integration in PCB generation."""

from pathlib import Path
from thkg.pcb.footprint_library import get_library
from thkg.pcb.routing_integrator import get_integrator


def test_routing_integration():
    """Test routing integration with complete footprints and traces."""
    print("Testing Routing Integration in PCB File")
    print("=" * 80)
    
    # Get libraries
    footprint_lib = get_library()
    routing_int = get_integrator()
    
    # Create a simple PCB file with routing
    print("\n🔨 Generating test PCB file with routing...")
    
    # PCB header
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

"""
    
    # Add nets
    pcb_content += """  (net 0 "")
  (net 1 "GND")
  (net 2 "VCC")
  (net 3 "ROW0")
  (net 4 "ROW1")
  (net 5 "ROW2")
  (net 6 "COL0")
  (net 7 "COL1")
  (net 8 "COL2")

"""
    
    # Add board outline (80mm x 80mm)
    pcb_content += """  (gr_line (start 0 0) (end 80 0) (layer "Edge.Cuts") (stroke (width 0.1) (type solid)) (tstamp 00000000-0000-0000-0000-000000000001))
  (gr_line (start 80 0) (end 80 80) (layer "Edge.Cuts") (stroke (width 0.1) (type solid)) (tstamp 00000000-0000-0000-0000-000000000002))
  (gr_line (start 80 80) (end 0 80) (layer "Edge.Cuts") (stroke (width 0.1) (type solid)) (tstamp 00000000-0000-0000-0000-000000000003))
  (gr_line (start 0 80) (end 0 0) (layer "Edge.Cuts") (stroke (width 0.1) (type solid)) (tstamp 00000000-0000-0000-0000-000000000004))

"""
    
    # Add footprints
    print("   📦 Adding footprints...")
    switch_count = 0
    diode_count = 0
    
    for row in range(3):
        for col in range(3):
            x = 20 + (col * 19.05)
            y = 20 + (row * 19.05)
            ref = f"SW{row * 3 + col + 1}"
            
            footprint = footprint_lib.get_footprint(
                "lumberjack:MX",
                ref,
                (x, y),
                rotation=0,
                net_map={"1": 6 + col, "2": 3 + row}
            )
            
            if footprint:
                pcb_content += footprint + "\n\n"
                switch_count += 1
    
    for row in range(3):
        for col in range(3):
            x = 20 + (col * 19.05)
            y = 30 + (row * 19.05)
            ref = f"D{row * 3 + col + 1}"
            
            footprint = footprint_lib.get_footprint(
                "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal",
                ref,
                (x, y),
                rotation=90,
                net_map={"1": 3 + row, "2": 6 + col}
            )
            
            if footprint:
                pcb_content += footprint + "\n\n"
                diode_count += 1
    
    print(f"      ✅ Added {switch_count} switches and {diode_count} diodes")
    
    # Add routing
    print("\n   🔀 Adding routing...")
    
    # Build net map
    net_map = {
        'GND': 1,
        'VCC': 2,
        'ROW0': 3,
        'ROW1': 4,
        'ROW2': 5,
        'COL0': 6,
        'COL1': 7,
        'COL2': 8,
    }
    
    # Generate routing
    pcb_bbox = ((0, 0), (80, 80))
    routing = routing_int.generate_routing_for_matrix(3, 3, pcb_bbox, net_map)
    
    if routing:
        routing_content = routing_int.routing_to_kicad(routing)
        pcb_content += routing_content + "\n\n"
        
        # Add ground plane
        ground_plane = routing_int.add_ground_plane(pcb_bbox, 1, "B.Cu")
        pcb_content += ground_plane + "\n\n"
        
        print(f"      ✅ Added {len(routing.traces)} traces and {len(routing.vias)} vias")
    else:
        print("      ⚠️  No routing generated")
    
    # Close PCB file
    pcb_content += ")\n"
    
    # Write to file
    output_dir = Path("output/test-routing")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "test-3x3-with-routing.kicad_pcb"
    
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
    
    # Count elements
    footprint_count = pcb_content.count('(footprint ')
    segment_count = pcb_content.count('(segment ')
    via_count = pcb_content.count('(via ')
    zone_count = pcb_content.count('(zone ')
    fp_line_count = pcb_content.count('(fp_line ')
    pad_count = pcb_content.count('(pad ')
    
    print(f"\n📊 Component Details:")
    print(f"   • Footprints: {footprint_count}")
    print(f"   • fp_line elements: {fp_line_count}")
    print(f"   • Pads: {pad_count}")
    
    print(f"\n📊 Routing Details:")
    print(f"   • Segments (traces): {segment_count}")
    print(f"   • Vias: {via_count}")
    print(f"   • Zones (ground planes): {zone_count}")
    
    # Compare to targets
    print(f"\n📈 Comparison:")
    print(f"   • Without routing: ~1,353 lines")
    print(f"   • With routing: {lines:,} lines")
    if lines > 1353:
        improvement = lines / 1353
        print(f"   • Improvement: {improvement:.1f}x larger")
    
    print(f"\n📈 Progress to Target:")
    print(f"   • Target (dumbpad): ~46,803 lines")
    print(f"   • Target (lumberjack): ~77,560 lines")
    print(f"   • Our PCB: {lines:,} lines")
    progress = (lines / 46803) * 100
    print(f"   • Progress: {progress:.1f}% of dumbpad target")
    
    if lines > 5000:
        print(f"   ✅ Excellent! Significant progress")
    elif lines > 2000:
        print(f"   ✅ Good! Much better with routing")
    else:
        print(f"   ⚠️  Still needs more routing data")
    
    print("\n" + "=" * 80)
    print("✅ Routing integration test complete!")
    print(f"📁 Output: {output_file}")


if __name__ == "__main__":
    test_routing_integration()
