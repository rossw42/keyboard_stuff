"""PCB routing using extracted templates."""

from pathlib import Path
from typing import List, Dict, Tuple
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from thkg.templates.routing_template import RoutingTemplateExtractor, RoutingTemplateApplicator


class Router:
    """Route PCB traces using extracted templates."""
    
    def __init__(self, components: List, connections: List):
        """Initialize router.
        
        Args:
            components: List of components
            connections: List of connections
        """
        self.components = components
        self.connections = connections
        self.traces = []
        self.vias = []
        self.template = None
        
    def route_all(self):
        """Route all connections using template."""
        print("   🔀 Loading routing template...")
        
        # Determine layout size from components
        if not self.components:
            print("      ⚠ No components to route")
            return
        
        # Calculate bounding box
        positions = [c.position for c in self.components if c.position]
        if not positions:
            print("      ⚠ No component positions")
            return
        
        min_x = min(p[0] for p in positions)
        min_y = min(p[1] for p in positions)
        max_x = max(p[0] for p in positions)
        max_y = max(p[1] for p in positions)
        
        layout_width = max_x - min_x
        layout_height = max_y - min_y
        
        print(f"      Layout size: {layout_width:.1f}mm × {layout_height:.1f}mm")
        
        # Select appropriate template based on size
        template_name = self._select_template(layout_width, layout_height)
        
        if not template_name:
            print("      ⚠ No suitable template found, generating basic routing")
            self._generate_basic_routing()
            return
        
        print(f"      Using template: {template_name}")
        
        # Load template
        try:
            routing_data_dir = Path(__file__).parent.parent.parent / "routing_data"
            templates_dir = Path(__file__).parent.parent.parent / "routing_templates"
            
            if not templates_dir.exists():
                print(f"      ⚠ Templates directory not found: {templates_dir}")
                self._generate_basic_routing()
                return
            
            template_file = templates_dir / f"{template_name}_template.json"
            
            if not template_file.exists():
                print(f"      ⚠ Template file not found: {template_file}")
                self._generate_basic_routing()
                return
            
            extractor = RoutingTemplateExtractor(routing_data_dir)
            self.template = extractor.load_template(template_file)
            
            print(f"      ✓ Template loaded: {len(self.template.routing.traces)} traces")
            
            # Apply template
            self._apply_template(min_x, min_y, max_x, max_y)
            
        except Exception as e:
            print(f"      ⚠ Error loading template: {e}")
            self._generate_basic_routing()
    
    def _select_template(self, width: float, height: float) -> str:
        """Select best template based on layout size.
        
        Args:
            width: Layout width in mm
            height: Layout height in mm
            
        Returns:
            Template name or None
        """
        # Template sizes (from our extracted data)
        templates = {
            'dumbpad_dumbpad': (91.1, 74.9),      # Macropad
            'litl_litl': (237.4, 86.2),            # Compact
            'lumberjack_lumberjack': (273.9, 86.2) # Full
        }
        
        # Calculate area
        layout_area = width * height
        
        # Find closest template by area
        best_template = None
        best_diff = float('inf')
        
        for name, (t_width, t_height) in templates.items():
            t_area = t_width * t_height
            diff = abs(t_area - layout_area)
            
            if diff < best_diff:
                best_diff = diff
                best_template = name
        
        return best_template
    
    def _apply_template(self, min_x: float, min_y: float, max_x: float, max_y: float):
        """Apply routing template to layout.
        
        Args:
            min_x, min_y, max_x, max_y: Bounding box
        """
        print("      Applying template routing...")
        
        # Create net mapping (simplified - map common nets)
        net_mapping = {}
        
        # Map power nets
        for net in self.template.routing.nets:
            if net.name in ['GND', 'VCC', '+5V', '+3V3']:
                net_mapping[net.name] = net.name
            elif '/ROW' in net.name or 'ROW' in net.name:
                # Map row nets
                net_mapping[net.name] = net.name.replace('/', '')
            elif '/COL' in net.name or 'COL' in net.name:
                # Map column nets
                net_mapping[net.name] = net.name.replace('/', '')
        
        if not net_mapping:
            print("      ⚠ No nets to map")
            return
        
        # Apply template
        applicator = RoutingTemplateApplicator(self.template)
        target_bbox = ((min_x, min_y), (max_x, max_y))
        
        new_routing = applicator.apply_to_layout(target_bbox, net_mapping)
        
        # Convert to trace format for PCB generator
        for trace in new_routing.traces:
            self.traces.append({
                'start': trace.start,
                'end': trace.end,
                'width': trace.width,
                'layer': trace.layer,
                'net': trace.net,
                'net_name': trace.net_name
            })
        
        for via in new_routing.vias:
            self.vias.append({
                'position': via.position,
                'size': via.size,
                'drill': via.drill,
                'layers': via.layers,
                'net': via.net,
                'net_name': via.net_name
            })
        
        print(f"      ✓ Generated {len(self.traces)} traces, {len(self.vias)} vias")
    
    def _generate_basic_routing(self):
        """Generate basic routing without template (fallback)."""
        print("      Generating basic routing...")
        
        # Generate simple point-to-point traces for each connection
        for conn in self.connections:
            if len(conn.pins) < 2:
                continue
            
            # Get component positions
            comp1_ref, pin1 = conn.pins[0]
            comp2_ref, pin2 = conn.pins[1]
            
            comp1 = next((c for c in self.components if c.reference == comp1_ref), None)
            comp2 = next((c for c in self.components if c.reference == comp2_ref), None)
            
            if not comp1 or not comp2 or not comp1.position or not comp2.position:
                continue
            
            # Create trace
            self.traces.append({
                'start': comp1.position,
                'end': comp2.position,
                'width': 0.25,
                'layer': 'F.Cu',
                'net': 0,
                'net_name': conn.net_name
            })
        
        print(f"      ✓ Generated {len(self.traces)} basic traces")
    
    def get_trace_count(self) -> int:
        """Get number of traces generated.
        
        Returns:
            Trace count
        """
        return len(self.traces)
