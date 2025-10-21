"""KiCad schematic file parser.

Parses KiCad 6/7 schematic files (.kicad_sch) which use S-expression format.
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
from thkg.templates.models import Component, Connection


class KiCadParser:
    """Parser for KiCad schematic files."""
    
    def __init__(self, schematic_path: Path):
        """Initialize parser with schematic file path."""
        self.path = Path(schematic_path)
        self.content = ""
        self.components: List[Component] = []
        self.connections: List[Connection] = []
        self.nets: Dict[str, List[Tuple[str, str]]] = {}  # net_name -> [(ref, pin), ...]
        
    def parse(self) -> Tuple[List[Component], List[Connection]]:
        """Parse schematic file and return components and connections."""
        self._load_file()
        self._parse_components()
        self._parse_connections()
        return self.components, self.connections
    
    def _load_file(self):
        """Load schematic file content."""
        if not self.path.exists():
            raise FileNotFoundError(f"Schematic file not found: {self.path}")
        
        with open(self.path, 'r', encoding='utf-8') as f:
            self.content = f.read()
    
    def _parse_components(self):
        """Extract all components from schematic."""
        # KiCad format: Each component is a (symbol ...) block with nested properties
        # Structure:
        #   (symbol (lib_id "Library:Part") (at x y rotation) ...
        #     (property "Reference" "R1" ...)
        #     (property "Value" "10k" ...)
        #     (property "Footprint" "..." ...)
        #     (instances
        #       (project "name"
        #         (path "uuid"
        #           (reference "R1") (unit 1)
        #         )
        #       )
        #     )
        #   )
        
        # Find all symbol blocks
        # Use a more robust approach - find symbol blocks and extract data
        symbol_blocks = self._extract_symbol_blocks()
        
        for block in symbol_blocks:
            component = self._parse_symbol_block(block)
            if component:
                self.components.append(component)
        
        # Sort components by reference for consistency
        self.components.sort(key=lambda c: self._sort_key(c.reference))
    
    def _extract_symbol_blocks(self) -> List[str]:
        """Extract all (symbol ...) blocks from the schematic."""
        blocks = []
        depth = 0
        current_block = []
        in_symbol = False
        
        for line in self.content.split('\n'):
            # Check if we're starting a symbol block
            if '(symbol (lib_id' in line:
                in_symbol = True
                depth = line.count('(') - line.count(')')
                current_block = [line]
                continue
            
            if in_symbol:
                current_block.append(line)
                
                # Track parenthesis depth
                depth += line.count('(') - line.count(')')
                
                # If we've closed all parentheses, we've found the end of the block
                if depth == 0:
                    blocks.append('\n'.join(current_block))
                    in_symbol = False
                    current_block = []
        
        return blocks
    
    def _parse_symbol_block(self, block: str) -> Optional[Component]:
        """Parse a single symbol block to extract component data."""
        # Extract lib_id
        lib_id_match = re.search(r'\(lib_id\s+"([^"]+)"\)', block)
        if not lib_id_match:
            return None
        
        lib_id = lib_id_match.group(1)
        library = lib_id.split(':')[0] if ':' in lib_id else ""
        
        # Extract position
        at_match = re.search(r'\(at\s+([\d.-]+)\s+([\d.-]+)(?:\s+([\d.-]+))?\)', block)
        x = float(at_match.group(1)) if at_match else 0.0
        y = float(at_match.group(2)) if at_match else 0.0
        rotation = float(at_match.group(3)) if at_match and at_match.group(3) else 0.0
        
        # Extract properties
        reference = self._extract_property(block, "Reference")
        value = self._extract_property(block, "Value")
        footprint = self._extract_property(block, "Footprint")
        
        if not reference:
            return None
        
        # Create component
        component = Component(
            reference=reference,
            value=value or "",
            footprint=footprint or "",
            library=library,
            symbol=lib_id,
            position=(x, y),
            rotation=rotation,
            properties={}
        )
        
        return component
    
    def _extract_property(self, block: str, property_name: str) -> Optional[str]:
        """Extract a property value from a symbol block."""
        pattern = rf'\(property\s+"{property_name}"\s+"([^"]+)"'
        match = re.search(pattern, block)
        return match.group(1) if match else None
    
    def _sort_key(self, reference: str) -> Tuple:
        """Generate sort key for component reference."""
        # Extract letter prefix and number
        match = re.match(r'([A-Z]+)(\d+)', reference)
        if match:
            prefix = match.group(1)
            number = int(match.group(2))
            return (prefix, number)
        return (reference, 0)
    
    def _parse_connections(self):
        """Extract net connections from schematic."""
        # Find all wire and junction connections
        # This is complex in KiCad - nets are implicit from wire connections
        
        # For now, we'll extract net labels which explicitly name nets
        # Pattern: (label "NET_NAME" (at x y rotation))
        label_pattern = r'\(label\s+"([^"]+)"\s+\(at\s+([\d.-]+)\s+([\d.-]+)'
        
        for match in re.finditer(label_pattern, self.content):
            net_name = match.group(1)
            # x = float(match.group(2))
            # y = float(match.group(3))
            
            # For now, just record that this net exists
            if net_name not in self.nets:
                self.nets[net_name] = []
        
        # Convert nets to Connection objects
        for net_name, pins in self.nets.items():
            if pins:  # Only create connection if we have pins
                connection = Connection(
                    net_name=net_name,
                    pins=pins
                )
                self.connections.append(connection)
    
    def get_component_by_reference(self, reference: str) -> Optional[Component]:
        """Get component by reference designator."""
        for comp in self.components:
            if comp.reference == reference:
                return comp
        return None
    
    def get_components_by_type(self, component_type: str) -> List[Component]:
        """Get all components of a specific type (e.g., 'R', 'C', 'U')."""
        return [c for c in self.components if c.reference.startswith(component_type)]
    
    def get_component_count(self) -> int:
        """Get total number of components."""
        return len(self.components)
    
    def get_net_count(self) -> int:
        """Get total number of nets."""
        return len(self.nets)


def parse_kicad_schematic(schematic_path: Path) -> Tuple[List[Component], List[Connection]]:
    """Parse a KiCad schematic file.
    
    Args:
        schematic_path: Path to .kicad_sch file
        
    Returns:
        Tuple of (components, connections)
    """
    parser = KiCadParser(schematic_path)
    return parser.parse()
