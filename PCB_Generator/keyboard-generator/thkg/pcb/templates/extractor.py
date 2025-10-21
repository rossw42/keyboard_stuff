"""Circuit template extractor.

Extracts reusable circuit blocks from KiCad schematics.
"""

from typing import Dict, List, Any, Optional, Set
from pathlib import Path
import logging

# Handle imports for both module and standalone execution
try:
    from ..kicad_parser import parse_schematic
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
    from thkg.pcb.kicad_parser import parse_schematic

logger = logging.getLogger(__name__)


class CircuitBlock:
    """Represents a reusable circuit block."""
    
    def __init__(self, name: str, block_type: str):
        """Initialize circuit block.
        
        Args:
            name: Block name (e.g., "ATmega328P_Support")
            block_type: Block type (mcu, usb, reset, crystal, etc.)
        """
        self.name = name
        self.block_type = block_type
        self.components: List[Dict[str, Any]] = []
        self.connections: List[Dict[str, Any]] = []
        self.input_pins: List[str] = []
        self.output_pins: List[str] = []
        self.power_pins: Dict[str, List[str]] = {'VCC': [], 'GND': []}
    
    def add_component(self, component: Dict[str, Any]):
        """Add component to block."""
        self.components.append(component)
    
    def add_connection(self, connection: Dict[str, Any]):
        """Add connection to block."""
        self.connections.append(connection)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'name': self.name,
            'type': self.block_type,
            'components': self.components,
            'connections': self.connections,
            'input_pins': self.input_pins,
            'output_pins': self.output_pins,
            'power_pins': self.power_pins
        }


class TemplateExtractor:
    """Extract circuit templates from KiCad schematics."""
    
    def __init__(self, schematic_path: Path):
        """Initialize extractor.
        
        Args:
            schematic_path: Path to .kicad_sch file
        """
        self.schematic_path = schematic_path
        self.schematic_data = None
        self.blocks: List[CircuitBlock] = []
    
    def extract(self) -> List[CircuitBlock]:
        """Extract all circuit blocks from schematic.
        
        Returns:
            List of identified circuit blocks
        """
        logger.info(f"Extracting templates from: {self.schematic_path.name}")
        
        # Parse schematic
        self.schematic_data = parse_schematic(self.schematic_path)
        
        # Identify circuit blocks
        self._identify_mcu_block()
        self._identify_usb_block()
        self._identify_crystal_block()
        self._identify_reset_block()
        
        logger.info(f"Extracted {len(self.blocks)} circuit blocks")
        
        return self.blocks
    
    def _identify_mcu_block(self):
        """Identify MCU and supporting components."""
        # Find MCU component (including Pro Micro modules)
        mcu_components = []
        
        for c in self.schematic_data['components']:
            lib_id_lower = c['lib_id'].lower()
            value_lower = c['value'].lower()
            
            if ('atmega' in lib_id_lower or 
                'mcu' in lib_id_lower or
                'promicro' in lib_id_lower or
                'pro_micro' in lib_id_lower or
                'promicro' in value_lower or
                (c['reference'] in ['U1', 'U2'] and 'atmega' in value_lower)):
                mcu_components.append(c)
        
        if not mcu_components:
            logger.debug("No MCU found")
            return
        
        mcu = mcu_components[0]
        logger.info(f"Found MCU: {mcu['reference']} ({mcu['lib_id']})")
        
        # Create MCU block
        block = CircuitBlock(f"{mcu['value']}_Support", "mcu")
        block.add_component(mcu)
        
        # Find nearby decoupling capacitors (within 50mm)
        mcu_pos = mcu['position']
        for comp in self.schematic_data['components']:
            if 'C' in comp['lib_id'] and comp['reference'].startswith('C'):
                # Check if near MCU
                comp_pos = comp['position']
                distance = ((comp_pos[0] - mcu_pos[0])**2 + 
                           (comp_pos[1] - mcu_pos[1])**2)**0.5
                
                if distance < 50:  # Within 50mm
                    block.add_component(comp)
                    logger.debug(f"  Added decoupling cap: {comp['reference']}")
        
        self.blocks.append(block)
    
    def _identify_usb_block(self):
        """Identify USB connector and protection circuit."""
        # Find USB connector
        usb_components = [
            c for c in self.schematic_data['components']
            if 'usb' in c['lib_id'].lower()
        ]
        
        if not usb_components:
            logger.debug("No USB connector found")
            return
        
        usb = usb_components[0]
        logger.info(f"Found USB: {usb['reference']} ({usb['lib_id']})")
        
        # Create USB block
        block = CircuitBlock(f"USB_{usb['value']}", "usb")
        block.add_component(usb)
        
        # Find protection components (ESD, ferrite beads, polyfuse)
        usb_pos = usb['position']
        for comp in self.schematic_data['components']:
            lib_id_lower = comp['lib_id'].lower()
            
            # ESD protection
            if 'esd' in lib_id_lower or 'usblc' in lib_id_lower:
                block.add_component(comp)
                logger.debug(f"  Added ESD protection: {comp['reference']}")
            
            # Ferrite beads
            elif 'ferrite' in lib_id_lower or 'fb' in comp['reference'].lower():
                comp_pos = comp['position']
                distance = ((comp_pos[0] - usb_pos[0])**2 + 
                           (comp_pos[1] - usb_pos[1])**2)**0.5
                if distance < 50:
                    block.add_component(comp)
                    logger.debug(f"  Added ferrite bead: {comp['reference']}")
            
            # Polyfuse
            elif 'fuse' in lib_id_lower or comp['reference'].startswith('F'):
                comp_pos = comp['position']
                distance = ((comp_pos[0] - usb_pos[0])**2 + 
                           (comp_pos[1] - usb_pos[1])**2)**0.5
                if distance < 50:
                    block.add_component(comp)
                    logger.debug(f"  Added polyfuse: {comp['reference']}")
            
            # CC resistors (5.1k for USB-C)
            elif comp['reference'].startswith('R') and '5.1' in comp['value']:
                comp_pos = comp['position']
                distance = ((comp_pos[0] - usb_pos[0])**2 + 
                           (comp_pos[1] - usb_pos[1])**2)**0.5
                if distance < 50:
                    block.add_component(comp)
                    logger.debug(f"  Added CC resistor: {comp['reference']}")
        
        self.blocks.append(block)
    
    def _identify_crystal_block(self):
        """Identify crystal oscillator and load capacitors."""
        # Find crystal
        crystal_components = [
            c for c in self.schematic_data['components']
            if 'crystal' in c['lib_id'].lower() or c['reference'].startswith('Y')
        ]
        
        if not crystal_components:
            logger.debug("No crystal found")
            return
        
        crystal = crystal_components[0]
        logger.info(f"Found crystal: {crystal['reference']} ({crystal['value']})")
        
        # Create crystal block
        block = CircuitBlock(f"Crystal_{crystal['value']}", "crystal")
        block.add_component(crystal)
        
        # Find load capacitors (typically 22pF, near crystal)
        crystal_pos = crystal['position']
        for comp in self.schematic_data['components']:
            if comp['reference'].startswith('C'):
                comp_pos = comp['position']
                distance = ((comp_pos[0] - crystal_pos[0])**2 + 
                           (comp_pos[1] - crystal_pos[1])**2)**0.5
                
                # Load caps are very close to crystal
                if distance < 30:
                    block.add_component(comp)
                    logger.debug(f"  Added load cap: {comp['reference']} = {comp['value']}")
        
        self.blocks.append(block)
    
    def _identify_reset_block(self):
        """Identify reset circuit (pull-up resistor, button)."""
        # Find reset button
        reset_components = [
            c for c in self.schematic_data['components']
            if 'sw' in c['lib_id'].lower() and 
               ('reset' in c['reference'].lower() or 'rst' in c['reference'].lower())
        ]
        
        if not reset_components:
            logger.debug("No reset button found")
            return
        
        reset_sw = reset_components[0]
        logger.info(f"Found reset button: {reset_sw['reference']}")
        
        # Create reset block
        block = CircuitBlock("Reset_Circuit", "reset")
        block.add_component(reset_sw)
        
        # Find pull-up resistor (typically 10k)
        reset_pos = reset_sw['position']
        for comp in self.schematic_data['components']:
            if comp['reference'].startswith('R'):
                comp_pos = comp['position']
                distance = ((comp_pos[0] - reset_pos[0])**2 + 
                           (comp_pos[1] - reset_pos[1])**2)**0.5
                
                if distance < 30 and '10k' in comp['value'].lower():
                    block.add_component(comp)
                    logger.debug(f"  Added pull-up: {comp['reference']} = {comp['value']}")
        
        self.blocks.append(block)


def extract_templates(schematic_path: Path) -> List[CircuitBlock]:
    """Convenience function to extract templates.
    
    Args:
        schematic_path: Path to .kicad_sch file
    
    Returns:
        List of extracted circuit blocks
    """
    extractor = TemplateExtractor(schematic_path)
    return extractor.extract()


if __name__ == "__main__":
    # Test with Lumberjack schematic
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    test_file = Path("../pcb-library/design-files/lumberjack/kicad/lumberjack.kicad_sch")
    
    if not test_file.exists():
        print(f"Test file not found: {test_file}")
        sys.exit(1)
    
    print(f"Extracting templates from: {test_file.name}\n")
    blocks = extract_templates(test_file)
    
    print(f"\n✓ Extracted {len(blocks)} circuit blocks:\n")
    for block in blocks:
        print(f"  {block.name} ({block.block_type})")
        print(f"    Components: {len(block.components)}")
        for comp in block.components:
            print(f"      - {comp['reference']:8s} {comp['lib_id']:30s} = {comp['value']}")
        print()
    
    print("✓ Template extraction working!")
