"""Circuit block identification from parsed components.

This module identifies functional circuit blocks (MCU, USB, reset, crystal, etc.)
from a list of components.
"""

from typing import List, Dict, Optional, Set
from thkg.templates.models import Component, CircuitTemplate


class CircuitBlockIdentifier:
    """Identify functional circuit blocks from components."""
    
    def __init__(self, components: List[Component]):
        """Initialize identifier with component list.
        
        Args:
            components: List of components from schematic
        """
        self.components = components
        self.blocks: Dict[str, List[Component]] = {}
        
    def identify_all_blocks(self) -> Dict[str, List[Component]]:
        """Identify all circuit blocks.
        
        Returns:
            Dictionary mapping block type to component list
        """
        self.blocks = {
            'mcu': self.identify_mcu_block(),
            'usb': self.identify_usb_block(),
            'reset': self.identify_reset_block(),
            'crystal': self.identify_crystal_block(),
            'power': self.identify_power_block(),
            'matrix': self.identify_matrix_block(),
            'leds': self.identify_led_block(),
        }
        
        return self.blocks
    
    def identify_mcu_block(self) -> List[Component]:
        """Identify MCU and related components.
        
        Returns:
            List of MCU-related components
        """
        mcu_components = []
        
        # Find MCU
        for comp in self.components:
            # Check for ATmega or other MCUs
            if any(mcu in comp.value.upper() for mcu in ['ATMEGA', 'ATMEGA328', 'ATMEGA32']):
                mcu_components.append(comp)
                break
            # Check for Pro Micro footprint
            if 'PRO_MICRO' in comp.footprint.upper() or 'PROMICRO' in comp.footprint.upper():
                mcu_components.append(comp)
                break
        
        # Find IC socket (if present)
        for comp in self.components:
            if comp.reference.startswith('IC') and 'SOCKET' in comp.value.upper():
                mcu_components.append(comp)
        
        return mcu_components
    
    def identify_usb_block(self) -> List[Component]:
        """Identify USB connector and related components.
        
        Returns:
            List of USB-related components
        """
        usb_components = []
        
        # Find USB connector
        for comp in self.components:
            if 'USB' in comp.symbol.upper() or 'USB' in comp.value.upper():
                usb_components.append(comp)
                
                # Find nearby resistors (USB pull-up/down resistors)
                # Typically 5.1k for USB-C CC pins, 75Ω for data lines
                usb_resistors = self._find_nearby_resistors(comp, ['5.1K', '75', '1.5K'])
                usb_components.extend(usb_resistors)
                
                # Find zener diodes (USB protection)
                zeners = [c for c in self.components 
                         if c.reference.startswith('D') and '3.6V' in c.value.upper()]
                usb_components.extend(zeners[:2])  # Usually 2 zener diodes
                
                break
        
        return usb_components
    
    def identify_reset_block(self) -> List[Component]:
        """Identify reset circuit components.
        
        Returns:
            List of reset-related components
        """
        reset_components = []
        
        # Find reset switch
        for comp in self.components:
            if comp.reference.startswith('SW') and 'RESET' in comp.value.upper():
                reset_components.append(comp)
            elif comp.reference.startswith('SW') and 'TACTILE' in comp.footprint.upper():
                # Tactile switches are often reset/boot switches
                reset_components.append(comp)
        
        # Find pull-up resistor (typically 10k)
        for comp in self.components:
            if comp.reference.startswith('R') and '10K' in comp.value.upper():
                reset_components.append(comp)
                break
        
        return reset_components
    
    def identify_crystal_block(self) -> List[Component]:
        """Identify crystal oscillator and load capacitors.
        
        Returns:
            List of crystal-related components
        """
        crystal_components = []
        
        # Find crystal
        for comp in self.components:
            if comp.reference.startswith('Y'):
                crystal_components.append(comp)
                
                # Find load capacitors (typically 22pF)
                load_caps = [c for c in self.components 
                            if c.reference.startswith('C') and '22P' in c.value.upper()]
                crystal_components.extend(load_caps[:2])  # Usually 2 capacitors
                
                break
        
        return crystal_components
    
    def identify_power_block(self) -> List[Component]:
        """Identify power-related components.
        
        Returns:
            List of power-related components
        """
        power_components = []
        
        # Find polyfuse
        for comp in self.components:
            if comp.reference.startswith('F'):
                power_components.append(comp)
        
        # Find decoupling capacitors (0.1µF, 100nF)
        decoupling_caps = [c for c in self.components 
                          if c.reference.startswith('C') and 
                          ('100N' in c.value.upper() or '0.1U' in c.value.upper())]
        power_components.extend(decoupling_caps)
        
        # Find bulk capacitor (4.7µF)
        bulk_caps = [c for c in self.components 
                    if c.reference.startswith('C') and '4.7U' in c.value.upper()]
        power_components.extend(bulk_caps)
        
        return power_components
    
    def identify_matrix_block(self) -> List[Component]:
        """Identify keyboard matrix components (switches and diodes).
        
        Returns:
            List of matrix components
        """
        matrix_components = []
        
        # Find switches (MX, SW)
        switches = [c for c in self.components 
                   if c.reference.startswith('MX') or 
                   (c.reference.startswith('SW') and 'PUSH' in c.value.upper())]
        matrix_components.extend(switches)
        
        # Find diodes (1N4148)
        diodes = [c for c in self.components 
                 if c.reference.startswith('D') and '4148' in c.value]
        matrix_components.extend(diodes)
        
        return matrix_components
    
    def identify_led_block(self) -> List[Component]:
        """Identify LED indicators and resistors.
        
        Returns:
            List of LED-related components
        """
        led_components = []
        
        # Find LEDs
        leds = [c for c in self.components 
               if c.reference.startswith('LED') or 
               ('LED' in c.symbol.upper() and c.reference.startswith('D'))]
        led_components.extend(leds)
        
        # Find current-limiting resistors (typically 1.5k)
        led_resistors = [c for c in self.components 
                        if c.reference.startswith('R') and '1.5K' in c.value.upper()]
        led_components.extend(led_resistors)
        
        return led_components
    
    def _find_nearby_resistors(self, component: Component, values: List[str]) -> List[Component]:
        """Find resistors with specific values.
        
        Args:
            component: Reference component
            values: List of resistor values to find (e.g., ['5.1K', '75'])
            
        Returns:
            List of matching resistors
        """
        resistors = []
        for comp in self.components:
            if comp.reference.startswith('R'):
                for value in values:
                    if value.upper() in comp.value.upper():
                        resistors.append(comp)
                        break
        return resistors
    
    def get_block_summary(self) -> Dict[str, int]:
        """Get summary of identified blocks.
        
        Returns:
            Dictionary mapping block type to component count
        """
        if not self.blocks:
            self.identify_all_blocks()
        
        return {block_type: len(components) 
                for block_type, components in self.blocks.items()}
    
    def create_template(self, block_type: str, name: str, 
                       source_project: str, version: str = "1.0") -> Optional[CircuitTemplate]:
        """Create a circuit template from an identified block.
        
        Args:
            block_type: Type of block ('mcu', 'usb', etc.)
            name: Template name
            source_project: Source project name
            version: Template version
            
        Returns:
            CircuitTemplate or None if block not found
        """
        if block_type not in self.blocks:
            return None
        
        components = self.blocks[block_type]
        if not components:
            return None
        
        template = CircuitTemplate(
            name=name,
            type=block_type,
            source_project=source_project,
            version=version,
            components=components,
            connections=[],  # TODO: Extract connections
            description=f"{block_type.upper()} circuit from {source_project}"
        )
        
        return template


def identify_circuit_blocks(components: List[Component]) -> Dict[str, List[Component]]:
    """Identify all circuit blocks from component list.
    
    Args:
        components: List of components from schematic
        
    Returns:
        Dictionary mapping block type to component list
    """
    identifier = CircuitBlockIdentifier(components)
    return identifier.identify_all_blocks()
