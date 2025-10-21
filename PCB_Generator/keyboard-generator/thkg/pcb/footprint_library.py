"""Footprint library for loading complete footprints from extracted library."""

from pathlib import Path
from typing import Dict, List, Optional
import json
import re
import uuid


class FootprintLibrary:
    """Load and manage complete footprints from extracted library."""
    
    def __init__(self, library_path: Optional[Path] = None):
        """Initialize footprint library.
        
        Args:
            library_path: Path to footprint library directory
        """
        if library_path is None:
            # Default to extracted footprints
            library_path = Path(__file__).parent.parent.parent / "kicad_knowledge_base" / "footprints"
        
        self.library_path = library_path
        self.index: Dict[str, List[Dict]] = {}
        self.cache: Dict[str, str] = {}
        
        # Load index
        self._load_index()
    
    def _load_index(self):
        """Load footprint index."""
        index_path = self.library_path / "footprint_index.json"
        
        if not index_path.exists():
            print(f"⚠️  Warning: Footprint index not found at {index_path}")
            return
        
        with open(index_path, 'r') as f:
            self.index = json.load(f)
        
        print(f"✅ Loaded footprint library with {self._count_footprints()} footprints")
    
    def _count_footprints(self) -> int:
        """Count total footprints in index."""
        return sum(len(fps) for fps in self.index.values())
    
    def find_footprint(self, library_name: str, reference_hint: Optional[str] = None) -> Optional[str]:
        """Find footprint by library name.
        
        Args:
            library_name: Library name (e.g., "lumberjack:MX", "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal")
            reference_hint: Optional reference hint to help find specific footprint
            
        Returns:
            Footprint file path or None if not found
        """
        # Try exact library match first
        for source, footprints in self.index.items():
            for fp in footprints:
                if fp['library'] == library_name:
                    return fp['file']
        
        # Try partial match on library name
        library_base = library_name.split(':')[-1] if ':' in library_name else library_name
        
        for source, footprints in self.index.items():
            for fp in footprints:
                fp_base = fp['library'].split(':')[-1] if ':' in fp['library'] else fp['library']
                if library_base.lower() in fp_base.lower():
                    return fp['file']
        
        return None
    
    def find_by_type(self, component_type: str) -> Optional[str]:
        """Find footprint by component type.
        
        Args:
            component_type: Component type (e.g., "switch", "diode", "resistor")
            
        Returns:
            Footprint file path or None if not found
        """
        type_map = {
            'switch': ['MX', 'SW_Cherry', 'Kailh'],
            'diode': ['D_DO-35', 'DO-1N4148'],
            'resistor': ['R_Axial'],
            'capacitor': ['C_Disc', 'CP_Radial'],
            'mcu': ['DIP-28', 'ATMEGA', 'PRO_MICRO'],
            'usb': ['USB_C', 'USB'],
            'crystal': ['Crystal'],
            'led': ['LED'],
            'mounting_hole': ['MountingHole'],
        }
        
        keywords = type_map.get(component_type.lower(), [])
        
        for source, footprints in self.index.items():
            for fp in footprints:
                for keyword in keywords:
                    if keyword.lower() in fp['library'].lower():
                        return fp['file']
        
        return None
    
    def load_footprint(self, file_path: str) -> Optional[str]:
        """Load footprint content from file.
        
        Args:
            file_path: Relative path to footprint file (from index)
            
        Returns:
            Footprint content or None if not found
        """
        # Check cache
        if file_path in self.cache:
            return self.cache[file_path]
        
        # The file_path from index already includes the subdirectory
        # e.g., "footprints/lumberjack/MX2.kicad_fp"
        # But library_path already points to .../footprints/
        # So we need to remove the "footprints/" prefix if present
        if file_path.startswith("footprints/"):
            file_path = file_path[len("footprints/"):]
        
        # Load from file
        full_path = self.library_path / file_path
        
        if not full_path.exists():
            print(f"⚠️  Warning: Footprint file not found: {full_path}")
            return None
        
        with open(full_path, 'r') as f:
            content = f.read()
        
        # Cache it
        self.cache[file_path] = content
        
        return content
    
    def get_footprint(self, library_name: str, reference: str, 
                     position: tuple, rotation: float = 0,
                     net_map: Optional[Dict[str, int]] = None) -> Optional[str]:
        """Get complete footprint with updated position and nets.
        
        Args:
            library_name: Library name
            reference: Component reference (e.g., "SW1", "D1")
            position: (x, y) position in mm
            rotation: Rotation in degrees
            net_map: Mapping of pad numbers to net numbers
            
        Returns:
            Complete footprint definition or None if not found
        """
        # Find footprint file
        file_path = self.find_footprint(library_name, reference)
        
        if not file_path:
            print(f"⚠️  Warning: Footprint not found for {library_name}")
            return None
        
        # Load footprint content
        content = self.load_footprint(file_path)
        
        if not content:
            return None
        
        # Update footprint
        updated = self._update_footprint(content, reference, position, rotation, net_map)
        
        return updated
    
    def _update_footprint(self, content: str, reference: str, 
                         position: tuple, rotation: float,
                         net_map: Optional[Dict[str, int]]) -> str:
        """Update footprint with new position, reference, and nets.
        
        Args:
            content: Original footprint content
            reference: New reference
            position: New (x, y) position
            rotation: New rotation
            net_map: Net mapping for pads
            
        Returns:
            Updated footprint content
        """
        x, y = position
        
        # Update position
        content = re.sub(
            r'\(at\s+[\d.-]+\s+[\d.-]+(?:\s+[\d.-]+)?\)',
            f'(at {x} {y} {rotation})',
            content,
            count=1  # Only update the first (at ...) which is the footprint position
        )
        
        # Update reference (both property and fp_text formats)
        content = re.sub(
            r'\(property\s+"Reference"\s+"[^"]*"',
            f'(property "Reference" "{reference}"',
            content
        )
        content = re.sub(
            r'\(fp_text\s+reference\s+"[^"]*"',
            f'(fp_text reference "{reference}"',
            content
        )
        
        # Update all UUIDs to be unique
        def replace_uuid(match):
            return f'(tstamp {uuid.uuid4()})'
        
        content = re.sub(r'\(tstamp\s+[a-f0-9-]+\)', replace_uuid, content)
        
        # Update net assignments in pads
        if net_map:
            # Split content into lines and process each pad
            lines = content.split('\n')
            result_lines = []
            current_pad_num = None
            
            for line in lines:
                # Check if this line starts a pad definition
                pad_match = re.search(r'\(pad\s+"([^"]+)"', line)
                if pad_match:
                    current_pad_num = pad_match.group(1)
                
                # If we're in a pad and this line has a net assignment, update it
                if current_pad_num and '(net ' in line:
                    if current_pad_num in net_map:
                        net_num = net_map[current_pad_num]
                        # Replace the net number
                        line = re.sub(r'\(net\s+\d+', f'(net {net_num}', line)
                    # Reset after processing net line
                    if ')' in line and 'tstamp' in line:
                        current_pad_num = None
                
                result_lines.append(line)
            
            content = '\n'.join(result_lines)
        
        return content


# Global library instance
_library = None


def get_library() -> FootprintLibrary:
    """Get global footprint library instance."""
    global _library
    if _library is None:
        _library = FootprintLibrary()
    return _library
