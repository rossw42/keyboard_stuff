"""PCB generator with circuit templates and component library

Based on ai03's PCB Design Guide and industry best practices.
Generates accurate through-hole keyboard PCBs with proper supporting circuits.
"""

from typing import List, Dict
from thkg.config import Configuration, Switch, MCUType
from thkg.pcb.circuits import CircuitTemplates, CircuitTemplate
from thkg.pcb.components import ComponentLibrary


class PCBGenerator:
    """Generate PCB designs with proven circuit templates"""
    
    def __init__(self):
        self.templates = CircuitTemplates()
        self.library = ComponentLibrary()
    
    def generate_pcb(self, config: Configuration, switches: List[Switch]) -> dict:
        """Generate PCB design with proper supporting circuits
        
        Args:
            config: Configuration with MCU type, USB type, matrix
            switches: List of switches with positions
            
        Returns:
            Dictionary with PCB data including circuits and BOM
        """
        # Get circuit templates based on configuration
        circuits = self._get_circuits(config, switches)
        
        # Generate BOM from circuits
        bom = self._generate_bom(circuits, config)
        
        # Calculate PCB dimensions from layout
        dimensions = self._calculate_dimensions(switches, config)
        
        # Get design rules
        rules = config.pcb.layout_rules
        
        return {
            'status': 'ready_for_implementation',
            'message': 'Circuit templates and BOM generated. KiCad integration pending.',
            'circuits': circuits,
            'bom': bom,
            'dimensions': dimensions,
            'layout_rules': {
                'trace_signal': rules.trace_signal_recommended,
                'trace_power': rules.trace_power_recommended,
                'trace_usb': rules.trace_usb_differential,
                'clearance': rules.clearance_recommended,
                'via_drill': rules.via_drill,
                'via_diameter': rules.via_diameter,
            },
            'notes': [
                'USB protection circuit included (ESD, ferrite beads, polyfuse)',
                f'MCU support circuit for {config.mcu_type.value}',
                f'Switch matrix: {config.matrix.rows}x{config.matrix.cols}',
                'All components use through-hole footprints (except USB protection)',
                'Crystal within 10mm of MCU',
                'Decoupling caps next to VCC pins',
            ]
        }
    
    def _get_circuits(self, config: Configuration, switches: List[Switch]) -> Dict[str, CircuitTemplate]:
        """Get circuit templates based on configuration
        
        Args:
            config: Configuration
            switches: List of switches
            
        Returns:
            Dictionary of circuit templates
        """
        circuits = {}
        
        # USB protection circuit
        if config.usb_type.value == "usb-c-tht":
            circuits['usb_protection'] = self.templates.usb_c_protection()
        
        # MCU support circuit
        if config.mcu_type == MCUType.ATMEGA328P:
            circuits['mcu_support'] = self.templates.atmega328p_support()
        elif config.mcu_type == MCUType.ATMEGA32A:
            circuits['mcu_support'] = self.templates.atmega32a_support()
        
        # Switch matrix
        if config.matrix:
            circuits['switch_matrix'] = self.templates.switch_matrix(
                config.matrix.rows,
                config.matrix.cols,
                config.matrix.diode_direction
            )
        
        return circuits
    
    def _generate_bom(self, circuits: Dict[str, CircuitTemplate], config: Configuration) -> List[dict]:
        """Generate Bill of Materials from circuits
        
        Args:
            circuits: Dictionary of circuit templates
            config: Configuration
            
        Returns:
            List of BOM entries with quantities and sourcing
        """
        components = []
        
        # Collect all components from circuits
        for circuit in circuits.values():
            for comp in circuit.components:
                # Map component to library entry
                if comp.value in ["5.1kΩ", "10kΩ", "1.5kΩ"]:
                    category = "Resistor"
                    value = comp.value.replace("kΩ", "k")
                elif comp.value in ["100nF", "22pF"]:
                    category = "Capacitor"
                    value = comp.value
                elif comp.value == "1N4148":
                    category = "Diode"
                    value = "1N4148"
                elif "USBLC6" in comp.value:
                    category = "IC"
                    value = "USBLC6-2SC6"
                elif "ATmega" in comp.value:
                    category = "MCU"
                    value = comp.value.split("-")[0]  # ATmega328P or ATmega32A
                elif "MHz" in comp.value:
                    category = "Crystal"
                    value = comp.value
                elif "600Ω" in comp.value:
                    category = "Ferrite Bead"
                    value = "600R@100MHz"
                elif "500mA" in comp.value:
                    category = "Polyfuse"
                    value = "500mA"
                elif "USB-C" in comp.value:
                    category = "Connector"
                    value = "USB-C-THT"
                elif "ISP" in comp.value:
                    category = "Connector"
                    value = "ISP-Header"
                elif "MX" in comp.value:
                    category = "Switch"
                    value = "MX"
                else:
                    continue
                
                components.append({
                    'category': category,
                    'value': value
                })
        
        # Generate BOM with quantities
        bom = self.library.generate_bom(components)
        
        return bom
    
    def _calculate_dimensions(self, switches: List[Switch], config: Configuration) -> dict:
        """Calculate PCB dimensions from switch layout
        
        Args:
            switches: List of switches with positions
            config: Configuration
            
        Returns:
            Dictionary with PCB dimensions
        """
        if not switches:
            # Use GH60 standard if no switches
            return {
                'length': config.pcb.length,
                'width': config.pcb.width,
                'thickness': config.pcb.thickness,
                'corner_radius': config.pcb.corner_radius,
            }
        
        # Calculate bounding box from switches
        min_x = min(sw.x for sw in switches)
        max_x = max(sw.x + sw.width * 19.05 for sw in switches)  # 19.05mm per unit
        min_y = min(sw.y for sw in switches)
        max_y = max(sw.y + sw.height * 19.05 for sw in switches)
        
        # Add border (5mm on each side)
        border = 5.0
        length = (max_x - min_x) + (2 * border)
        width = (max_y - min_y) + (2 * border)
        
        return {
            'length': round(length, 1),
            'width': round(width, 1),
            'thickness': config.pcb.thickness,
            'corner_radius': config.pcb.corner_radius,
            'border': border,
        }
    
    def get_design_validation(self, config: Configuration) -> List[str]:
        """Validate design against best practices
        
        Args:
            config: Configuration
            
        Returns:
            List of validation messages (warnings/errors)
        """
        messages = []
        
        # Check matrix size vs available pins
        if config.matrix:
            total_pins = config.matrix.rows + config.matrix.cols
            
            if config.mcu_type == MCUType.ATMEGA328P:
                available = 12  # After reserving USB, crystal, ISP
                if total_pins > available:
                    messages.append(
                        f"ERROR: Matrix needs {total_pins} pins, "
                        f"ATmega328P has only {available} available"
                    )
            elif config.mcu_type == MCUType.ATMEGA32A:
                available = 24  # After reserving USB, crystal, ISP
                if total_pins > available:
                    messages.append(
                        f"ERROR: Matrix needs {total_pins} pins, "
                        f"ATmega32A has only {available} available"
                    )
        
        # Check USB type compatibility
        if config.usb_type.value != "usb-c-tht":
            messages.append(
                f"WARNING: USB type '{config.usb_type.value}' not fully supported. "
                "USB-C through-hole recommended."
            )
        
        # Check PCB dimensions
        if config.pcb.length > 300 or config.pcb.width > 150:
            messages.append(
                "WARNING: PCB dimensions exceed typical keyboard size. "
                "Verify dimensions are correct."
            )
        
        return messages
