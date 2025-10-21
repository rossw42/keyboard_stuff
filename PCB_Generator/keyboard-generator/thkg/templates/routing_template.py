"""Routing template extraction and application.

This module extracts routing patterns from reference PCBs and applies them
to new PCB designs with similar topology.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from thkg.templates.models import Trace, Via, Zone, Net, PCBRouting


@dataclass
class RoutingTemplate:
    """Template for PCB routing patterns."""
    
    name: str
    source_project: str
    source_pcb: str
    
    # Topology information
    row_count: int
    col_count: int
    
    # Routing data
    routing: PCBRouting
    
    # Bounding box (for scaling/positioning)
    bbox_min: Tuple[float, float]  # (x, y)
    bbox_max: Tuple[float, float]  # (x, y)
    
    # Metadata
    description: str = ""
    
    def get_dimensions(self) -> Tuple[float, float]:
        """Get template dimensions (width, height) in mm."""
        width = self.bbox_max[0] - self.bbox_min[0]
        height = self.bbox_max[1] - self.bbox_min[1]
        return (width, height)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'name': self.name,
            'source_project': self.source_project,
            'source_pcb': self.source_pcb,
            'row_count': self.row_count,
            'col_count': self.col_count,
            'bbox_min': self.bbox_min,
            'bbox_max': self.bbox_max,
            'description': self.description,
            'routing': {
                'nets': [asdict(net) for net in self.routing.nets],
                'traces': [asdict(trace) for trace in self.routing.traces],
                'vias': [asdict(via) for via in self.routing.vias],
                'zones': [asdict(zone) for zone in self.routing.zones]
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'RoutingTemplate':
        """Create from dictionary."""
        routing = PCBRouting(
            nets=[Net(**net) for net in data['routing']['nets']],
            traces=[Trace(**trace) for trace in data['routing']['traces']],
            vias=[Via(**via) for via in data['routing']['vias']],
            zones=[Zone(**zone) for zone in data['routing']['zones']]
        )
        
        return cls(
            name=data['name'],
            source_project=data['source_project'],
            source_pcb=data['source_pcb'],
            row_count=data['row_count'],
            col_count=data['col_count'],
            bbox_min=tuple(data['bbox_min']),
            bbox_max=tuple(data['bbox_max']),
            description=data.get('description', ''),
            routing=routing
        )


class RoutingTemplateExtractor:
    """Extract routing templates from reference PCBs."""
    
    def __init__(self, routing_data_dir: Path):
        """Initialize extractor.
        
        Args:
            routing_data_dir: Directory containing extracted routing JSON files
        """
        self.routing_data_dir = Path(routing_data_dir)
        
        if not self.routing_data_dir.exists():
            raise FileNotFoundError(f"Routing data directory not found: {self.routing_data_dir}")
    
    def extract_template(self, project: str, pcb_name: str) -> Optional[RoutingTemplate]:
        """Extract routing template from a PCB.
        
        Args:
            project: Project name (e.g., 'lumberjack')
            pcb_name: PCB name (e.g., 'lumberjack')
            
        Returns:
            RoutingTemplate or None if not found
        """
        # Load routing data
        routing_file = self.routing_data_dir / f"{project}_{pcb_name}_routing.json"
        
        if not routing_file.exists():
            print(f"Routing file not found: {routing_file}")
            return None
        
        with open(routing_file, 'r', encoding='utf-8') as f:
            routing_data = json.load(f)
        
        # Load topology analysis
        analysis_file = self.routing_data_dir / "routing_topology_analysis.json"
        
        if not analysis_file.exists():
            print(f"Analysis file not found: {analysis_file}")
            return None
        
        with open(analysis_file, 'r', encoding='utf-8') as f:
            all_analyses = json.load(f)
        
        # Find analysis for this PCB
        analysis = None
        for a in all_analyses:
            if a['project'] == project and a['pcb_name'] == pcb_name:
                analysis = a
                break
        
        if not analysis:
            print(f"Analysis not found for {project}/{pcb_name}")
            return None
        
        # Create routing object
        routing = PCBRouting(
            nets=[Net(**net) for net in routing_data['nets']],
            traces=[Trace(**trace) for trace in routing_data['traces']],
            vias=[Via(**via) for via in routing_data['vias']],
            zones=[Zone(**zone) for zone in routing_data['zones']]
        )
        
        # Calculate bounding box from traces
        bbox_min, bbox_max = self._calculate_bbox(routing)
        
        # Create template
        template = RoutingTemplate(
            name=f"{project}_{pcb_name}",
            source_project=project,
            source_pcb=pcb_name,
            row_count=analysis['matrix']['row_count'],
            col_count=analysis['matrix']['col_count'],
            routing=routing,
            bbox_min=bbox_min,
            bbox_max=bbox_max,
            description=f"Routing template from {project}/{pcb_name}"
        )
        
        return template
    
    def _calculate_bbox(self, routing: PCBRouting) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Calculate bounding box from routing data.
        
        Args:
            routing: PCBRouting object
            
        Returns:
            Tuple of (min_point, max_point)
        """
        if not routing.traces:
            return ((0, 0), (0, 0))
        
        # Collect all points
        points = []
        for trace in routing.traces:
            points.append(trace.start)
            points.append(trace.end)
        
        for via in routing.vias:
            points.append(via.position)
        
        # Find min/max
        min_x = min(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_x = max(p[0] for p in points)
        max_y = max(p[1] for p in points)
        
        return ((min_x, min_y), (max_x, max_y))
    
    def save_template(self, template: RoutingTemplate, output_dir: Path):
        """Save routing template to JSON file.
        
        Args:
            template: RoutingTemplate to save
            output_dir: Output directory
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"{template.name}_template.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(template.to_dict(), f, indent=2)
        
        print(f"✓ Saved template: {output_file.name}")
    
    def load_template(self, template_file: Path) -> RoutingTemplate:
        """Load routing template from JSON file.
        
        Args:
            template_file: Path to template JSON file
            
        Returns:
            RoutingTemplate
        """
        with open(template_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return RoutingTemplate.from_dict(data)


class RoutingTemplateApplicator:
    """Apply routing templates to new PCB designs."""
    
    def __init__(self, template: RoutingTemplate):
        """Initialize applicator with a template.
        
        Args:
            template: RoutingTemplate to apply
        """
        self.template = template
    
    def apply_to_layout(self, 
                       target_bbox: Tuple[Tuple[float, float], Tuple[float, float]],
                       net_mapping: Dict[str, str]) -> PCBRouting:
        """Apply template routing to a new layout.
        
        Args:
            target_bbox: Target bounding box ((min_x, min_y), (max_x, max_y))
            net_mapping: Mapping from template net names to target net names
                        e.g., {'/ROW0': 'ROW0', '/COL0': 'COL0'}
        
        Returns:
            New PCBRouting with transformed traces/vias
        """
        # Calculate scale factors
        template_width = self.template.bbox_max[0] - self.template.bbox_min[0]
        template_height = self.template.bbox_max[1] - self.template.bbox_min[1]
        
        target_width = target_bbox[1][0] - target_bbox[0][0]
        target_height = target_bbox[1][1] - target_bbox[0][1]
        
        scale_x = target_width / template_width if template_width > 0 else 1.0
        scale_y = target_height / template_height if template_height > 0 else 1.0
        
        # Transform traces
        new_traces = []
        for trace in self.template.routing.traces:
            # Check if this net should be included
            if trace.net_name not in net_mapping:
                continue
            
            # Transform coordinates
            new_start = self._transform_point(trace.start, target_bbox, scale_x, scale_y)
            new_end = self._transform_point(trace.end, target_bbox, scale_x, scale_y)
            
            new_trace = Trace(
                start=new_start,
                end=new_end,
                width=trace.width,
                layer=trace.layer,
                net=trace.net,  # Will be remapped later
                net_name=net_mapping[trace.net_name],
                tstamp=""  # Generate new timestamp
            )
            new_traces.append(new_trace)
        
        # Transform vias
        new_vias = []
        for via in self.template.routing.vias:
            if via.net_name not in net_mapping:
                continue
            
            new_position = self._transform_point(via.position, target_bbox, scale_x, scale_y)
            
            new_via = Via(
                position=new_position,
                size=via.size,
                drill=via.drill,
                layers=via.layers,
                net=via.net,
                net_name=net_mapping[via.net_name],
                tstamp=""
            )
            new_vias.append(new_via)
        
        # Create new routing
        new_routing = PCBRouting(
            nets=[],  # Nets will be created from net_mapping
            traces=new_traces,
            vias=new_vias,
            zones=[]  # Zones are complex, skip for now
        )
        
        return new_routing
    
    def _transform_point(self, 
                        point: Tuple[float, float],
                        target_bbox: Tuple[Tuple[float, float], Tuple[float, float]],
                        scale_x: float,
                        scale_y: float) -> Tuple[float, float]:
        """Transform a point from template space to target space.
        
        Args:
            point: Point in template space
            target_bbox: Target bounding box
            scale_x: X scale factor
            scale_y: Y scale factor
            
        Returns:
            Transformed point
        """
        # Normalize to 0-1 range in template space
        norm_x = (point[0] - self.template.bbox_min[0]) / (self.template.bbox_max[0] - self.template.bbox_min[0])
        norm_y = (point[1] - self.template.bbox_min[1]) / (self.template.bbox_max[1] - self.template.bbox_min[1])
        
        # Scale to target space
        target_x = target_bbox[0][0] + norm_x * (target_bbox[1][0] - target_bbox[0][0])
        target_y = target_bbox[0][1] + norm_y * (target_bbox[1][1] - target_bbox[0][1])
        
        return (target_x, target_y)
