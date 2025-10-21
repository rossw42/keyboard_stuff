"""KiCad PCB file parser for extracting routing information.

Parses KiCad 6/7 PCB files (.kicad_pcb) which use S-expression format.
Extracts traces, vias, zones, and net connectivity.
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from thkg.templates.models import Trace, Via, Zone, Net, PCBRouting


class KiCadPCBParser:
    """Parser for KiCad PCB files."""
    
    def __init__(self, pcb_path: Path):
        """Initialize parser with PCB file path."""
        self.path = Path(pcb_path)
        self.content = ""
        self.routing = PCBRouting()
        
    def parse(self) -> PCBRouting:
        """Parse PCB file and return routing information."""
        self._load_file()
        self._parse_nets()
        self._parse_traces()
        self._parse_vias()
        self._parse_zones()
        self._enrich_with_net_names()
        return self.routing
    
    def _load_file(self):
        """Load PCB file content."""
        if not self.path.exists():
            raise FileNotFoundError(f"PCB file not found: {self.path}")
        
        with open(self.path, 'r', encoding='utf-8') as f:
            self.content = f.read()
    
    def _parse_nets(self):
        """Extract net definitions."""
        # Pattern: (net 0 "")
        # Pattern: (net 1 "GND")
        net_pattern = r'\(net\s+(\d+)\s+"([^"]*)"\)'
        
        for match in re.finditer(net_pattern, self.content):
            net_num = int(match.group(1))
            net_name = match.group(2)
            
            net = Net(number=net_num, name=net_name)
            self.routing.nets.append(net)
    
    def _parse_traces(self):
        """Extract trace segments."""
        # Pattern: (segment (start x y) (end x y) (width w) (layer "L") (net n) (tstamp uuid))
        # Example: (segment (start 108.016611 86.788089) (end 117.6711 77.1336) (width 0.25) (layer "F.Cu") (net 3) (tstamp 4420647a...))
        
        segment_pattern = r'\(segment\s+\(start\s+([\d.-]+)\s+([\d.-]+)\)\s+\(end\s+([\d.-]+)\s+([\d.-]+)\)\s+\(width\s+([\d.-]+)\)\s+\(layer\s+"([^"]+)"\)\s+\(net\s+(\d+)\)(?:\s+\(tstamp\s+([a-f0-9-]+)\))?\)'
        
        for match in re.finditer(segment_pattern, self.content):
            start_x = float(match.group(1))
            start_y = float(match.group(2))
            end_x = float(match.group(3))
            end_y = float(match.group(4))
            width = float(match.group(5))
            layer = match.group(6)
            net = int(match.group(7))
            tstamp = match.group(8) if match.group(8) else ""
            
            trace = Trace(
                start=(start_x, start_y),
                end=(end_x, end_y),
                width=width,
                layer=layer,
                net=net,
                tstamp=tstamp
            )
            self.routing.traces.append(trace)
    
    def _parse_vias(self):
        """Extract vias."""
        # Pattern: (via (at x y) (size s) (drill d) (layers "L1" "L2") (net n) (tstamp uuid))
        # Example: (via (at 113.03 87.63) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 6) (tstamp 650e6db4...))
        
        via_pattern = r'\(via\s+\(at\s+([\d.-]+)\s+([\d.-]+)\)\s+\(size\s+([\d.-]+)\)\s+\(drill\s+([\d.-]+)\)\s+\(layers\s+"([^"]+)"\s+"([^"]+)"\)\s+\(net\s+(\d+)\)(?:\s+\(tstamp\s+([a-f0-9-]+)\))?\)'
        
        for match in re.finditer(via_pattern, self.content):
            x = float(match.group(1))
            y = float(match.group(2))
            size = float(match.group(3))
            drill = float(match.group(4))
            layer1 = match.group(5)
            layer2 = match.group(6)
            net = int(match.group(7))
            tstamp = match.group(8) if match.group(8) else ""
            
            via = Via(
                position=(x, y),
                size=size,
                drill=drill,
                layers=(layer1, layer2),
                net=net,
                tstamp=tstamp
            )
            self.routing.vias.append(via)
    
    def _parse_zones(self):
        """Extract copper zones (ground planes, etc.)."""
        # Zones are complex multi-line structures
        # Pattern: (zone (net n) (net_name "NAME") (layer "L") ... (filled_polygon ...))
        
        # Find all zone blocks
        zone_blocks = self._extract_zone_blocks()
        
        for block in zone_blocks:
            zone = self._parse_zone_block(block)
            if zone:
                self.routing.zones.append(zone)
    
    def _extract_zone_blocks(self) -> List[str]:
        """Extract all (zone ...) blocks from the PCB."""
        blocks = []
        depth = 0
        current_block = []
        in_zone = False
        
        for line in self.content.split('\n'):
            # Check if we're starting a zone block
            if re.match(r'\s*\(zone\s+', line):
                in_zone = True
                depth = line.count('(') - line.count(')')
                current_block = [line]
                continue
            
            if in_zone:
                current_block.append(line)
                
                # Track parenthesis depth
                depth += line.count('(') - line.count(')')
                
                # If we've closed all parentheses, we've found the end of the block
                if depth == 0:
                    blocks.append('\n'.join(current_block))
                    in_zone = False
                    current_block = []
        
        return blocks
    
    def _parse_zone_block(self, block: str) -> Optional[Zone]:
        """Parse a single zone block."""
        # Extract net number
        net_match = re.search(r'\(net\s+(\d+)\)', block)
        if not net_match:
            return None
        net = int(net_match.group(1))
        
        # Extract net name
        net_name_match = re.search(r'\(net_name\s+"([^"]+)"\)', block)
        net_name = net_name_match.group(1) if net_name_match else ""
        
        # Extract layer
        layer_match = re.search(r'\(layer\s+"([^"]+)"\)', block)
        layer = layer_match.group(1) if layer_match else ""
        
        # Extract priority
        priority_match = re.search(r'\(priority\s+(\d+)\)', block)
        priority = int(priority_match.group(1)) if priority_match else 0
        
        # Extract tstamp
        tstamp_match = re.search(r'\(tstamp\s+([a-f0-9-]+)\)', block)
        tstamp = tstamp_match.group(1) if tstamp_match else ""
        
        # Extract filled polygons (simplified - just note they exist)
        # Full polygon parsing would be complex, so we'll just mark that the zone exists
        filled_polygons = []
        if '(filled_polygon' in block:
            # Zone has filled polygons
            filled_polygons = [[]]  # Placeholder
        
        zone = Zone(
            net=net,
            net_name=net_name,
            layer=layer,
            priority=priority,
            filled_polygons=filled_polygons,
            tstamp=tstamp
        )
        
        return zone
    
    def _enrich_with_net_names(self):
        """Add net names to traces and vias."""
        # Create net lookup
        net_lookup = {net.number: net.name for net in self.routing.nets}
        
        # Enrich traces
        for trace in self.routing.traces:
            trace.net_name = net_lookup.get(trace.net, "")
        
        # Enrich vias
        for via in self.routing.vias:
            via.net_name = net_lookup.get(via.net, "")
        
        # Zones already have net_name from parsing


def parse_kicad_pcb(pcb_path: Path) -> PCBRouting:
    """Parse a KiCad PCB file and extract routing information.
    
    Args:
        pcb_path: Path to .kicad_pcb file
        
    Returns:
        PCBRouting object with nets, traces, vias, and zones
    """
    parser = KiCadPCBParser(pcb_path)
    return parser.parse()
