"""KiCad schematic file parser.

Parses KiCad 7.0+ .kicad_sch files (S-expression format) into Python data structures.
"""

from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import logging
import sexpdata

logger = logging.getLogger(__name__)


class KiCadSchematicParser:
    """Parse KiCad .kicad_sch schematic files.
    
    KiCad 7.0+ uses S-expression format, which is human-readable and easy to parse.
    
    Example structure:
        (kicad_sch (version 20230121) (generator eeschema)
          (uuid "...")
          (paper "A4")
          (lib_symbols ...)
          (symbol (lib_id "Device:R") ...)
          (wire (pts (xy 100 100) (xy 150 100)))
        )
    """
    
    def __init__(self, filepath: Path):
        """Initialize parser with schematic file path.
        
        Args:
            filepath: Path to .kicad_sch file
        """
        self.filepath = Path(filepath)
        self.data = None
        self._raw_content = None
    
    def parse(self) -> Dict[str, Any]:
        """Parse schematic file into structured data.
        
        Returns:
            Dictionary containing:
                - version: KiCad file format version
                - uuid: Schematic UUID
                - symbols: List of symbol definitions
                - components: List of placed components
                - wires: List of wire connections
                - labels: List of net labels
                - global_labels: List of global labels
        
        Raises:
            FileNotFoundError: If schematic file doesn't exist
            ValueError: If file format is invalid
        """
        if not self.filepath.exists():
            raise FileNotFoundError(f"Schematic file not found: {self.filepath}")
        
        logger.info(f"Parsing schematic: {self.filepath}")
        
        # Read file content
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self._raw_content = f.read()
        
        # Parse S-expression
        try:
            self.data = sexpdata.loads(self._raw_content)
        except Exception as e:
            raise ValueError(f"Failed to parse S-expression: {e}")
        
        # Verify it's a kicad_sch file
        if not self.data or not isinstance(self.data, list) or \
           not (isinstance(self.data[0], sexpdata.Symbol) and str(self.data[0]) == 'kicad_sch'):
            raise ValueError("Not a valid KiCad schematic file")
        
        result = {
            'version': self._get_version(),
            'uuid': self._get_uuid(),
            'symbols': self._get_symbols(),
            'components': self._get_components(),
            'wires': self._get_wires(),
            'labels': self._get_labels(),
            'global_labels': self._get_global_labels()
        }
        
        logger.info(f"Parsed {len(result['components'])} components, "
                   f"{len(result['wires'])} wires")
        
        return result
    
    def _find_element(self, name: str, parent: Optional[List] = None) -> Optional[List]:
        """Find first element with given name in S-expression.
        
        Args:
            name: Element name to find
            parent: Parent list to search in (defaults to root)
        
        Returns:
            Element list or None if not found
        """
        if parent is None:
            parent = self.data
        
        if not isinstance(parent, list):
            return None
        
        for item in parent:
            if isinstance(item, list) and len(item) > 0:
                if isinstance(item[0], sexpdata.Symbol) and str(item[0]) == name:
                    return item
        return None
    
    def _find_all_elements(self, name: str, parent: Optional[List] = None) -> List[List]:
        """Find all elements with given name in S-expression.
        
        Args:
            name: Element name to find
            parent: Parent list to search in (defaults to root)
        
        Returns:
            List of matching elements
        """
        if parent is None:
            parent = self.data
        
        if not isinstance(parent, list):
            return []
        
        results = []
        for item in parent:
            if isinstance(item, list) and len(item) > 0:
                if isinstance(item[0], sexpdata.Symbol) and str(item[0]) == name:
                    results.append(item)
        return results
    
    def _get_property(self, element: List, prop_name: str) -> Optional[str]:
        """Extract property value from element.
        
        Args:
            element: S-expression element
            prop_name: Property name to find
        
        Returns:
            Property value or None
        """
        if not isinstance(element, list):
            return None
        
        for item in element:
            if isinstance(item, list) and len(item) >= 2:
                if isinstance(item[0], sexpdata.Symbol) and str(item[0]) == 'property':
                    if len(item) >= 3 and item[1] == prop_name:
                        return str(item[2])
        return None
    
    def _get_version(self) -> str:
        """Extract KiCad file format version.
        
        Returns:
            Version string (e.g., "20230121")
        """
        version_elem = self._find_element('version')
        if version_elem and len(version_elem) >= 2:
            return str(version_elem[1])
        return "unknown"
    
    def _get_uuid(self) -> str:
        """Extract schematic UUID.
        
        Returns:
            UUID string
        """
        uuid_elem = self._find_element('uuid')
        if uuid_elem and len(uuid_elem) >= 2:
            return str(uuid_elem[1])
        return ""
    
    def _get_symbols(self) -> List[Dict[str, Any]]:
        """Extract symbol library definitions.
        
        Returns:
            List of symbol definitions with properties
        """
        # TODO: Parse from S-expression
        # Look for: (lib_symbols ...)
        return []
    
    def _get_components(self) -> List[Dict[str, Any]]:
        """Extract placed components (symbol instances).
        
        Returns:
            List of components with:
                - lib_id: Library symbol ID (e.g., "Device:R")
                - reference: Component reference (e.g., "R1")
                - value: Component value (e.g., "10k")
                - position: (x, y) coordinates
                - rotation: Rotation angle
                - properties: Additional properties
        """
        components = []
        symbol_elements = self._find_all_elements('symbol')
        
        for symbol in symbol_elements:
            # Find lib_id
            lib_id = None
            position = (0, 0)
            rotation = 0
            
            for item in symbol:
                if isinstance(item, list) and len(item) >= 2:
                    if isinstance(item[0], sexpdata.Symbol):
                        if str(item[0]) == 'lib_id':
                            lib_id = str(item[1])
                        elif str(item[0]) == 'at':
                            # Position: (at x y rotation)
                            if len(item) >= 3:
                                position = (float(item[1]), float(item[2]))
                            if len(item) >= 4:
                                rotation = float(item[3])
            
            if lib_id:
                component = {
                    'lib_id': lib_id,
                    'reference': self._get_property(symbol, 'Reference') or '',
                    'value': self._get_property(symbol, 'Value') or '',
                    'position': position,
                    'rotation': rotation,
                    'properties': {}
                }
                
                # Extract all properties
                for item in symbol:
                    if isinstance(item, list) and len(item) >= 3:
                        if isinstance(item[0], sexpdata.Symbol) and str(item[0]) == 'property':
                            prop_name = str(item[1])
                            prop_value = str(item[2])
                            component['properties'][prop_name] = prop_value
                
                components.append(component)
        
        return components
    
    def _get_wires(self) -> List[Dict[str, Any]]:
        """Extract wire connections.
        
        Returns:
            List of wires with:
                - points: List of (x, y) coordinates
                - net: Net name (if labeled)
        """
        wires = []
        wire_elements = self._find_all_elements('wire')
        
        for wire in wire_elements:
            points = []
            
            # Find pts element
            for item in wire:
                if isinstance(item, list) and len(item) >= 1:
                    if isinstance(item[0], sexpdata.Symbol) and str(item[0]) == 'pts':
                        # Extract xy points
                        for pt in item[1:]:
                            if isinstance(pt, list) and len(pt) >= 3:
                                if isinstance(pt[0], sexpdata.Symbol) and str(pt[0]) == 'xy':
                                    x = float(pt[1])
                                    y = float(pt[2])
                                    points.append((x, y))
            
            if points:
                wires.append({
                    'points': points,
                    'net': None  # Net name determined by labels
                })
        
        return wires
    
    def _get_labels(self) -> List[Dict[str, Any]]:
        """Extract local net labels.
        
        Returns:
            List of labels with:
                - text: Label text
                - position: (x, y) coordinates
        """
        labels = []
        label_elements = self._find_all_elements('label')
        
        for label in label_elements:
            if len(label) >= 2:
                text = str(label[1])
                position = (0, 0)
                
                # Find position
                for item in label:
                    if isinstance(item, list) and len(item) >= 3:
                        if isinstance(item[0], sexpdata.Symbol) and str(item[0]) == 'at':
                            position = (float(item[1]), float(item[2]))
                
                labels.append({
                    'text': text,
                    'position': position
                })
        
        return labels
    
    def _get_global_labels(self) -> List[Dict[str, Any]]:
        """Extract global net labels.
        
        Returns:
            List of global labels with:
                - text: Label text
                - position: (x, y) coordinates
                - shape: Label shape (input/output/bidirectional)
        """
        global_labels = []
        label_elements = self._find_all_elements('global_label')
        
        for label in label_elements:
            if len(label) >= 2:
                text = str(label[1])
                position = (0, 0)
                shape = 'bidirectional'
                
                # Find position and shape
                for item in label:
                    if isinstance(item, list) and len(item) >= 2:
                        if isinstance(item[0], sexpdata.Symbol):
                            if str(item[0]) == 'at' and len(item) >= 3:
                                position = (float(item[1]), float(item[2]))
                            elif str(item[0]) == 'shape':
                                shape = str(item[1])
                
                global_labels.append({
                    'text': text,
                    'position': position,
                    'shape': shape
                })
        
        return global_labels


def parse_schematic(filepath: Path) -> Dict[str, Any]:
    """Convenience function to parse a schematic file.
    
    Args:
        filepath: Path to .kicad_sch file
    
    Returns:
        Parsed schematic data
    """
    parser = KiCadSchematicParser(filepath)
    return parser.parse()


if __name__ == "__main__":
    # Test with Lumberjack schematic
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    test_file = Path("../pcb-library/design-files/lumberjack/kicad/lumberjack.kicad_sch")
    
    if not test_file.exists():
        print(f"Test file not found: {test_file}")
        print("Trying alternative path...")
        test_file = Path("../../pcb-library/design-files/lumberjack/kicad/lumberjack.kicad_sch")
    
    if not test_file.exists():
        print(f"Test file not found: {test_file}")
        print("Run from keyboard-generator directory")
        sys.exit(1)
    
    print(f"Testing KiCad parser with: {test_file.name}")
    result = parse_schematic(test_file)
    
    print(f"\n✓ Parsed schematic successfully!")
    print(f"  Version: {result['version']}")
    print(f"  UUID: {result['uuid'][:20]}...")
    print(f"  Components: {len(result['components'])}")
    print(f"  Wires: {len(result['wires'])}")
    print(f"  Labels: {len(result['labels'])}")
    print(f"  Global labels: {len(result['global_labels'])}")
    
    # Show first few components
    if result['components']:
        print(f"\nFirst 5 components:")
        for comp in result['components'][:5]:
            print(f"  {comp['reference']:8s} {comp['lib_id']:30s} = {comp['value']}")
    
    print("\n✓ KiCad parser working!")
