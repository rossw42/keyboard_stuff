"""Complete PCB generation (schematic + layout)."""

from pathlib import Path
from typing import Optional
from thkg.config import Configuration
from thkg.pcb.schematic import SchematicGenerator
from thkg.pcb.layout import LayoutGenerator
from thkg.pcb.router import Router
from thkg.pcb.footprint_library import get_library
from thkg.pcb.routing_integrator import get_integrator


class PCBGenerator:
    """Generate complete PCB (schematic + layout)."""
    
    def __init__(self, config: Configuration):
        """Initialize PCB generator.
        
        Args:
            config: Keyboard configuration
        """
        self.config = config
        self.schematic_gen = SchematicGenerator(config)
        self.layout_gen: Optional[LayoutGenerator] = None
        self.router: Optional[Router] = None
    
    def generate(self, output_dir: Path) -> bool:
        """Generate complete PCB.
        
        Args:
            output_dir: Output directory
            
        Returns:
            True if successful
        """
        print(f"\n{'='*80}")
        print(f"Generating Complete PCB: {self.config.name}")
        print(f"{'='*80}\n")
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate schematic
        schematic_path = output_dir / f"{self.config.name}.kicad_sch"
        print("📄 Step 1: Generating Schematic")
        self.schematic_gen.generate(schematic_path)
        
        # Generate layout
        print("\n📐 Step 2: Generating PCB Layout")
        self.layout_gen = LayoutGenerator(
            self.schematic_gen.components,
            self.schematic_gen.connections
        )
        self.layout_gen.generate_layout()
        
        # Route traces
        print("\n🔀 Step 3: Routing Traces")
        self.router = Router(
            self.schematic_gen.components,
            self.schematic_gen.connections
        )
        self.router.route_all()
        
        # Write PCB file
        print("\n💾 Step 4: Writing PCB File")
        pcb_path = output_dir / f"{self.config.name}.kicad_pcb"
        self._write_pcb_file(pcb_path)
        
        # Summary
        print(f"\n{'='*80}")
        print("✅ PCB Generation Complete!")
        print(f"{'='*80}")
        print(f"\n📁 Output Directory: {output_dir}")
        print(f"   • Schematic: {schematic_path.name}")
        print(f"   • PCB: {pcb_path.name}")
        print(f"\n📊 Statistics:")
        print(f"   • Components: {len(self.schematic_gen.components)}")
        print(f"   • Connections: {len(self.schematic_gen.connections)}")
        print(f"   • Traces: {self.router.get_trace_count()}")
        print(f"\n{'='*80}\n")
        
        return True
    
    def _write_pcb_file(self, output_path: Path):
        """Write KiCad PCB file.
        
        Args:
            output_path: Path to output file
        """
        print("   💾 Writing PCB file...")
        
        # Generate KiCad PCB format
        pcb_content = self._generate_kicad_pcb()
        
        # Write to file
        with open(output_path, 'w') as f:
            f.write(pcb_content)
        
        print(f"      ✅ Written to {output_path}")
    
    def _generate_kicad_pcb(self) -> str:
        """Generate KiCad PCB file content with complete footprints.
        
        Returns:
            PCB file content
        """
        from datetime import datetime
        import uuid
        
        content = f"""(kicad_pcb (version 20221018) (generator thkg)

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
      (dashed_line_dash_ratio 12.000000)
      (dashed_line_gap_ratio 3.000000)
      (svgprecision 4)
      (plotframeref false)
      (viasonmask false)
      (mode 1)
      (useauxorigin false)
      (hpglpennumber 1)
      (hpglpenspeed 20)
      (hpglpendiameter 15.000000)
      (dxfpolygonmode true)
      (dxfimperialunits true)
      (dxfusepcbnewfont true)
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
        
        # Add board outline (GH60 standard: 285mm x 94.6mm)
        content += "  (gr_line (start 0 0) (end 285 0) (layer \"Edge.Cuts\") (width 0.1))\n"
        content += "  (gr_line (start 285 0) (end 285 94.6) (layer \"Edge.Cuts\") (width 0.1))\n"
        content += "  (gr_line (start 285 94.6) (end 0 94.6) (layer \"Edge.Cuts\") (width 0.1))\n"
        content += "  (gr_line (start 0 94.6) (end 0 0) (layer \"Edge.Cuts\") (width 0.1))\n\n"
        
        # Add mounting holes (GH60 standard positions)
        mounting_holes = [
            (19.0, 9.5),    # TL
            (266.0, 9.5),   # TR
            (28.5, 47.3),   # ML
            (256.5, 47.3),  # MR
            (57.0, 85.0),   # BL
            (228.0, 85.0),  # BR
        ]
        
        for i, (x, y) in enumerate(mounting_holes, 1):
            content += f"""  (footprint "MountingHole:MountingHole_2.2mm_M2" (layer "F.Cu")
    (at {x} {y})
    (property "Reference" "H{i}" (at 0 -3 0) (layer "F.SilkS"))
    (property "Value" "MountingHole" (at 0 3 0) (layer "F.Fab"))
    (pad "" np_thru_hole circle (at 0 0) (size 2.2 2.2) (drill 2.2) (layers "*.Cu" "*.Mask"))
  )

"""
        
        # Add footprints with complete pad definitions
        if self.layout_gen and self.schematic_gen.components:
            for comp in self.schematic_gen.components:
                if comp.position:
                    x, y = comp.position
                    footprint_def = self._get_footprint_definition(comp)
                    content += footprint_def + "\n"
        
        # Add routing (traces, vias, zones)
        routing_content = self._generate_routing()
        if routing_content:
            content += "\n" + routing_content + "\n"
        
        content += ")\n"
        
        return content
    
    def _generate_routing(self) -> str:
        """Generate routing (traces, vias, zones) using templates.
        
        Returns:
            KiCad routing content or empty string
        """
        # Get routing integrator
        integrator = get_integrator()
        
        # Determine matrix size from config
        if not self.config.matrix:
            return ""
        
        rows = self.config.matrix.rows
        cols = self.config.matrix.cols
        
        # Calculate PCB bounding box
        # For now, use standard dimensions or calculate from switches
        if hasattr(self.config.pcb, 'length') and hasattr(self.config.pcb, 'width'):
            pcb_bbox = ((0, 0), (self.config.pcb.length, self.config.pcb.width))
        else:
            # Default to reasonable size
            pcb_bbox = ((0, 0), (285.0, 94.6))  # GH60 standard
        
        # Build net map
        net_map = {
            'GND': 1,
            'VCC': 2,
        }
        
        # Add row nets
        for i in range(rows):
            net_map[f'ROW{i}'] = 3 + i
        
        # Add column nets
        for i in range(cols):
            net_map[f'COL{i}'] = 3 + rows + i
        
        # Generate routing
        routing = integrator.generate_routing_for_matrix(rows, cols, pcb_bbox, net_map)
        
        if not routing:
            return ""
        
        # Convert to KiCad format
        content = integrator.routing_to_kicad(routing)
        
        # Add ground plane
        ground_plane = integrator.add_ground_plane(pcb_bbox, 1, "B.Cu")
        content += "\n\n" + ground_plane
        
        return content
    
    def _get_footprint_definition(self, comp) -> str:
        """Get complete footprint definition from library.
        
        Args:
            comp: Component object
            
        Returns:
            Footprint definition string
        """
        x, y = comp.position
        ref = comp.reference
        value = comp.value
        footprint = comp.footprint
        rotation = comp.rotation if hasattr(comp, 'rotation') else 0
        
        # Get footprint library
        library = get_library()
        
        # Determine component type and library name
        library_name = None
        
        # MX Switch footprint (Cherry MX compatible)
        if 'MX' in ref or 'SW' in ref:
            library_name = "lumberjack:MX"
        
        # Diode footprint (1N4148)
        elif 'D' in ref and 'LED' not in ref:
            library_name = "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal"
        
        # Resistor footprint
        elif 'R' in ref:
            library_name = "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal"
        
        # Capacitor footprint
        elif 'C' in ref:
            library_name = "Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm"
        
        # ATmega328P DIP-28
        elif 'U' in ref and 'ATMEGA' in value.upper():
            library_name = "Package_DIP:DIP-28_W7.62mm"
        
        # Crystal
        elif 'Y' in ref or 'XTAL' in value.upper():
            library_name = "Crystal:Crystal_HC49-4H_Vertical"
        
        # LED
        elif 'LED' in ref:
            library_name = "LED_THT:LED_D3.0mm"
        
        # Try to get footprint from library
        if library_name:
            # Build net map if available
            net_map = None
            if hasattr(comp, 'nets') and comp.nets:
                net_map = comp.nets
            
            footprint_def = library.get_footprint(
                library_name, 
                ref, 
                (x, y), 
                rotation,
                net_map
            )
            
            if footprint_def:
                return footprint_def
        
        # Fallback to minimal footprint
        print(f"⚠️  Warning: Using minimal footprint for {ref} ({library_name or footprint})")
        return f"""  (footprint "{footprint}" (layer "F.Cu")
    (at {x} {y} {rotation})
    (property "Reference" "{ref}" (at 0 -3 0) (layer "F.SilkS"))
    (property "Value" "{value}" (at 0 3 0) (layer "F.Fab"))
  )"""
