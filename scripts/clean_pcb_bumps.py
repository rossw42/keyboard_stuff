#!/usr/bin/env python3
"""
Clean up mouse bites / breakaway tabs from split PCB STEP files
"""

import sys
import os
import cadquery as cq
from cadquery import exporters

def clean_pcb_bumps(input_file, output_file=None):
    """Remove small bumps/tabs from PCB edges"""
    
    print(f"Cleaning bumps from: {os.path.basename(input_file)}")
    
    # Import PCB
    pcb = cq.importers.importStep(input_file)
    bb = pcb.val().BoundingBox()
    
    print(f"  PCB bounds: X({bb.xmin:.2f}, {bb.xmax:.2f}), Y({bb.ymin:.2f}, {bb.ymax:.2f})")
    
    # Get the PCB outline
    try:
        pcb_shape = pcb.val()
        wp = cq.Workplane("XY").add(pcb_shape)
        faces = wp.faces().vals()
        
        # Find the largest face (top or bottom)
        largest_face = max(faces, key=lambda f: f.Area())
        outer_wire = largest_face.outerWire()
        
        # Create a slightly offset outline (inward by 0.5mm to remove bumps)
        cleaned_wires = outer_wire.offset2D(-0.5)
        
        if cleaned_wires:
            # Offset back out to original size
            final_wires = cleaned_wires[0].offset2D(0.5)
            
            if final_wires:
                # Create new PCB from cleaned outline
                pcb_thickness = bb.zmax - bb.zmin
                cleaned_pcb = (cq.Workplane("XY")
                              .add(final_wires[0])
                              .toPending()
                              .extrude(pcb_thickness)
                              .translate((0, 0, bb.zmin)))
                
                print(f"  ✓ Cleaned PCB outline (removed bumps)")
                
                # Export
                if output_file is None:
                    base = os.path.splitext(input_file)[0]
                    output_file = f"{base}_cleaned.step"
                
                exporters.export(cleaned_pcb, output_file)
                print(f"  ✓ Saved: {os.path.basename(output_file)}")
                
                return cleaned_pcb
        
        print(f"  ⚠ Could not clean outline, returning original")
        return pcb
        
    except Exception as e:
        print(f"  ⚠ Cleaning failed: {e}")
        print(f"  Returning original PCB")
        return pcb

def main():
    if len(sys.argv) < 2:
        print("Usage: python clean_pcb_bumps.py <input.step> [output.step]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    
    clean_pcb_bumps(input_file, output_file)

if __name__ == "__main__":
    main()
