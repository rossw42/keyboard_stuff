"""Routing integration for PCB generation.

Integrates routing templates into generated PCBs.
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional
import uuid
from thkg.templates.routing_template import RoutingTemplate, RoutingTemplateApplicator
from thkg.templates.models import PCBRouting, Trace, Via, Zone


class RoutingIntegrator:
    """Integrate routing templates into PCB generation."""
    
    def __init__(self, template_dir: Optional[Path] = None):
        """Initialize routing integrator.
        
        Args:
            template_dir: Directory containing routing templates
        """
        if template_dir is None:
            template_dir = Path(__file__).parent.parent.parent / "routing_templates"
        
        self.template_dir = Path(template_dir)
        self.templates: Dict[str, RoutingTemplate] = {}
        
        # Load available templates
        self._load_templates()
    
    def _load_templates(self):
        """Load all available routing templates."""
        if not self.template_dir.exists():
            print(f"⚠️  Warning: Template directory not found: {self.template_dir}")
            return
        
        template_files = list(self.template_dir.glob("*_template.json"))
        
        for template_file in template_files:
            try:
                import json
                with open(template_file, 'r') as f:
                    data = json.load(f)
                
                template = RoutingTemplate.from_dict(data)
                self.templates[template.name] = template
                
            except Exception as e:
                print(f"⚠️  Warning: Failed to load template {template_file.name}: {e}")
        
        if self.templates:
            print(f"✅ Loaded {len(self.templates)} routing templates")
    
    def select_template(self, rows: int, cols: int) -> Optional[RoutingTemplate]:
        """Select best routing template for given matrix size.
        
        Args:
            rows: Number of rows in matrix
            cols: Number of columns in matrix
            
        Returns:
            Best matching template or None
        """
        if not self.templates:
            return None
        
        # Find templates with similar dimensions
        candidates = []
        for name, template in self.templates.items():
            # Calculate similarity score
            row_diff = abs(template.row_count - rows)
            col_diff = abs(template.col_count - cols)
            score = row_diff + col_diff
            
            candidates.append((score, template))
        
        # Sort by score (lower is better)
        candidates.sort(key=lambda x: x[0])
        
        if candidates:
            best_template = candidates[0][1]
            print(f"   📐 Selected template: {best_template.name}")
            print(f"      • Template size: {best_template.row_count}x{best_template.col_count}")
            print(f"      • Target size: {rows}x{cols}")
            print(f"      • Traces: {len(best_template.routing.traces)}")
            print(f"      • Vias: {len(best_template.routing.vias)}")
            return best_template
        
        return None
    
    def apply_routing(self,
                     template: RoutingTemplate,
                     target_bbox: Tuple[Tuple[float, float], Tuple[float, float]],
                     net_map: Dict[str, int]) -> PCBRouting:
        """Apply routing template to target layout.
        
        Args:
            template: Routing template to apply
            target_bbox: Target bounding box ((min_x, min_y), (max_x, max_y))
            net_map: Mapping from net names to net numbers
                    e.g., {'GND': 1, 'VCC': 2, 'ROW0': 3}
        
        Returns:
            PCBRouting with transformed traces and vias
        """
        # Create net name mapping (template names to target names)
        net_name_mapping = {}
        for template_net in template.routing.nets:
            # Try to match net names
            template_name = template_net.name
            
            # Remove leading slash if present
            clean_name = template_name.lstrip('/')
            
            # Check if we have this net in our map
            if clean_name in net_map:
                net_name_mapping[template_name] = clean_name
            elif template_name in net_map:
                net_name_mapping[template_name] = template_name
        
        # Apply template
        applicator = RoutingTemplateApplicator(template)
        routing = applicator.apply_to_layout(target_bbox, net_name_mapping)
        
        # Update net numbers
        for trace in routing.traces:
            if trace.net_name in net_map:
                trace.net = net_map[trace.net_name]
            # Generate new UUID
            trace.tstamp = str(uuid.uuid4())
        
        for via in routing.vias:
            if via.net_name in net_map:
                via.net = net_map[via.net_name]
            via.tstamp = str(uuid.uuid4())
        
        return routing
    
    def generate_routing_for_matrix(self,
                                    rows: int,
                                    cols: int,
                                    pcb_bbox: Tuple[Tuple[float, float], Tuple[float, float]],
                                    net_map: Dict[str, int]) -> Optional[PCBRouting]:
        """Generate routing for a keyboard matrix.
        
        Args:
            rows: Number of rows
            cols: Number of columns
            pcb_bbox: PCB bounding box
            net_map: Net name to number mapping
            
        Returns:
            PCBRouting or None if no template available
        """
        # Select template
        template = self.select_template(rows, cols)
        
        if not template:
            print("   ⚠️  No suitable routing template found")
            return None
        
        # Apply routing
        routing = self.apply_routing(template, pcb_bbox, net_map)
        
        print(f"   ✅ Applied routing:")
        print(f"      • Traces: {len(routing.traces)}")
        print(f"      • Vias: {len(routing.vias)}")
        
        return routing
    
    def routing_to_kicad(self, routing: PCBRouting) -> str:
        """Convert routing to KiCad PCB format.
        
        Args:
            routing: PCBRouting object
            
        Returns:
            KiCad PCB format string
        """
        lines = []
        
        # Add traces (segments)
        for trace in routing.traces:
            line = (
                f'  (segment (start {trace.start[0]:.4f} {trace.start[1]:.4f}) '
                f'(end {trace.end[0]:.4f} {trace.end[1]:.4f}) '
                f'(width {trace.width}) '
                f'(layer "{trace.layer}") '
                f'(net {trace.net}) '
                f'(tstamp {trace.tstamp}))'
            )
            lines.append(line)
        
        # Add vias
        for via in routing.vias:
            layers_str = ' '.join(f'"{layer}"' for layer in via.layers)
            line = (
                f'  (via (at {via.position[0]:.4f} {via.position[1]:.4f}) '
                f'(size {via.size}) '
                f'(drill {via.drill}) '
                f'(layers {layers_str}) '
                f'(net {via.net}) '
                f'(tstamp {via.tstamp}))'
            )
            lines.append(line)
        
        return '\n'.join(lines)
    
    def add_ground_plane(self,
                        pcb_bbox: Tuple[Tuple[float, float], Tuple[float, float]],
                        net_number: int,
                        layer: str = "B.Cu") -> str:
        """Add a ground plane zone to PCB.
        
        Args:
            pcb_bbox: PCB bounding box
            net_number: Net number for ground (usually 1)
            layer: Layer for ground plane (default B.Cu)
            
        Returns:
            KiCad zone definition
        """
        min_x, min_y = pcb_bbox[0]
        max_x, max_y = pcb_bbox[1]
        
        # Add small margin
        margin = 1.0
        min_x += margin
        min_y += margin
        max_x -= margin
        max_y -= margin
        
        zone = f'''  (zone (net {net_number}) (net_name "GND") (layer "{layer}") (tstamp {uuid.uuid4()}) (hatch edge 0.5)
    (connect_pads (clearance 0.5))
    (min_thickness 0.25) (filled_areas_thickness no)
    (fill yes (thermal_gap 0.5) (thermal_bridge_width 0.5))
    (polygon
      (pts
        (xy {min_x} {min_y})
        (xy {max_x} {min_y})
        (xy {max_x} {max_y})
        (xy {min_x} {max_y})
      )
    )
  )'''
        
        return zone


# Global integrator instance
_integrator = None


def get_integrator() -> RoutingIntegrator:
    """Get global routing integrator instance."""
    global _integrator
    if _integrator is None:
        _integrator = RoutingIntegrator()
    return _integrator
