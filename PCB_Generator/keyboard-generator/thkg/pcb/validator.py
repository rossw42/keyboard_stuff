"""Schematic validation."""

from typing import List, Dict, Tuple
from thkg.templates.models import Component, Connection


class SchematicValidator:
    """Validate generated schematics."""
    
    def __init__(self, components: List[Component], connections: List[Connection]):
        """Initialize validator.
        
        Args:
            components: List of components
            connections: List of connections
        """
        self.components = components
        self.connections = connections
        self.errors = []
        self.warnings = []
        self.info = []
    
    def validate(self) -> Tuple[List[str], List[str], List[str]]:
        """Run all validations.
        
        Returns:
            Tuple of (errors, warnings, info)
        """
        self._validate_power()
        self._validate_matrix()
        self._validate_mcu()
        self._validate_usb()
        
        return self.errors, self.warnings, self.info
    
    def _validate_power(self):
        """Validate power connections."""
        # Check for VCC net
        vcc_nets = [c for c in self.connections if 'VCC' in c.net_name.upper()]
        if not vcc_nets:
            self.errors.append("No VCC power net found")
        else:
            self.info.append(f"VCC net found with {len(vcc_nets[0].pins)} connections")
        
        # Check for GND net
        gnd_nets = [c for c in self.connections if 'GND' in c.net_name.upper()]
        if not gnd_nets:
            self.errors.append("No GND net found")
        else:
            self.info.append(f"GND net found with {len(gnd_nets[0].pins)} connections")
        
        # Check for decoupling capacitors
        caps = [c for c in self.components if c.reference.startswith('C') and '100N' in c.value.upper()]
        if len(caps) < 2:
            self.warnings.append(f"Only {len(caps)} decoupling capacitors found (recommend 2+)")
        else:
            self.info.append(f"Found {len(caps)} decoupling capacitors")
    
    def _validate_matrix(self):
        """Validate switch matrix."""
        # Check for switches
        switches = [c for c in self.components if c.reference.startswith('SW')]
        if not switches:
            self.errors.append("No switches found")
        else:
            self.info.append(f"Found {len(switches)} switches")
        
        # Check for diodes
        diodes = [c for c in self.components if c.reference.startswith('D') and '4148' in c.value]
        if not diodes:
            self.errors.append("No diodes found")
        elif len(diodes) != len(switches):
            self.warnings.append(f"Diode count ({len(diodes)}) doesn't match switch count ({len(switches)})")
        else:
            self.info.append(f"Found {len(diodes)} diodes (matches switches)")
        
        # Check for row/column nets
        row_nets = [c for c in self.connections if c.net_name.startswith('ROW')]
        col_nets = [c for c in self.connections if c.net_name.startswith('COL')]
        
        if not row_nets:
            self.errors.append("No row nets found")
        else:
            self.info.append(f"Found {len(row_nets)} row nets")
        
        if not col_nets:
            self.errors.append("No column nets found")
        else:
            self.info.append(f"Found {len(col_nets)} column nets")
    
    def _validate_mcu(self):
        """Validate MCU connections."""
        # Check for MCU
        mcu = [c for c in self.components if 'ATMEGA' in c.value.upper() or 'MICRO' in c.value.upper()]
        if not mcu:
            self.errors.append("No MCU found")
        else:
            self.info.append(f"Found MCU: {mcu[0].value}")
        
        # Check for crystal
        crystal = [c for c in self.components if c.reference.startswith('Y')]
        if not crystal:
            self.warnings.append("No crystal found (may be using internal oscillator)")
        else:
            self.info.append(f"Found crystal: {crystal[0].value}")
    
    def _validate_usb(self):
        """Validate USB connections."""
        # Check for USB connector
        usb = [c for c in self.components if 'USB' in c.symbol.upper()]
        if not usb:
            self.warnings.append("No USB connector found")
        else:
            self.info.append(f"Found USB connector: {usb[0].value}")
        
        # Check for USB resistors
        usb_resistors = [c for c in self.components if c.reference.startswith('R') and 
                        ('75' in c.value or '5.1K' in c.value.upper())]
        if len(usb_resistors) < 2:
            self.warnings.append(f"Only {len(usb_resistors)} USB resistors found (recommend 2+)")
    
    def print_report(self):
        """Print validation report."""
        print()
        print("=" * 80)
        print("Schematic Validation Report")
        print("=" * 80)
        print()
        
        if self.errors:
            print(f"❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"   • {error}")
            print()
        
        if self.warnings:
            print(f"⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")
            print()
        
        if self.info:
            print(f"ℹ️  INFO ({len(self.info)}):")
            for info in self.info:
                print(f"   • {info}")
            print()
        
        # Summary
        if not self.errors:
            print("✅ Validation PASSED")
        else:
            print(f"❌ Validation FAILED with {len(self.errors)} errors")
        
        print("=" * 80)
