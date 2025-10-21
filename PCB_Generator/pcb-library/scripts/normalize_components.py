#!/usr/bin/env python3
"""
Component Normalization System
Standardizes component names, values, and categories
"""

import re
import json
from pathlib import Path
from typing import Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class NormalizedComponent:
    """Normalized component data"""
    category: str
    component: str
    value: str
    footprint: str
    package: str
    
    def __repr__(self):
        return f"{self.category}: {self.component} {self.value} ({self.footprint})"


class ComponentNormalizer:
    """Normalizes component names and values"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict:
        """Load normalization rules from config file"""
        if self.config_path and self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        
        # Default rules
        return {
            "resistor_patterns": [
                r"(?i)^r\d+$",
                r"(?i)^res",
                r"(?i)resistor"
            ],
            "capacitor_patterns": [
                r"(?i)^c\d+$",
                r"(?i)^cap",
                r"(?i)capacitor"
            ],
            "diode_patterns": [
                r"(?i)^d\d+$",
                r"(?i)^diode",
                r"(?i)1n4148"
            ],
            "mcu_patterns": [
                r"(?i)atmega",
                r"(?i)^u\d+$",
                r"(?i)microcontroller",
                r"(?i)pro\s*micro"
            ],
            "crystal_patterns": [
                r"(?i)^y\d+$",
                r"(?i)crystal",
                r"(?i)xtal"
            ],
            "led_patterns": [
                r"(?i)^led",
                r"(?i)^d\d+.*led"
            ],
            "connector_patterns": [
                r"(?i)^j\d+$",
                r"(?i)usb",
                r"(?i)connector",
                r"(?i)header"
            ],
            "switch_patterns": [
                r"(?i)^sw\d+$",
                r"(?i)switch",
                r"(?i)button",
                r"(?i)tactile"
            ]
        }
    
    def normalize(self, component: str, value: str, footprint: str = "") -> NormalizedComponent:
        """Normalize a component"""
        category = self._categorize(component, value, footprint)
        norm_component = self._normalize_component_name(component, category)
        norm_value = self._normalize_value(value, category)
        norm_footprint = self._normalize_footprint(footprint, category)
        package = self._extract_package(footprint, category)
        
        return NormalizedComponent(
            category=category,
            component=norm_component,
            value=norm_value,
            footprint=norm_footprint,
            package=package
        )
    
    def _categorize(self, component: str, value: str, footprint: str) -> str:
        """Determine component category"""
        comp_lower = component.lower()
        val_lower = value.lower()
        foot_lower = footprint.lower()
        
        # Check resistors
        for pattern in self.rules["resistor_patterns"]:
            if re.search(pattern, comp_lower) or re.search(pattern, val_lower):
                if 'k' in val_lower or 'ohm' in val_lower or 'Ω' in value or re.match(r'\d+\.?\d*\s*[kKmM]?[Ωω]?', value):
                    return "Resistors"
        
        # Check capacitors
        for pattern in self.rules["capacitor_patterns"]:
            if re.search(pattern, comp_lower) or re.search(pattern, val_lower):
                if 'f' in val_lower or 'µ' in value or 'u' in val_lower or 'p' in val_lower:
                    return "Capacitors"
        
        # Check diodes
        for pattern in self.rules["diode_patterns"]:
            if re.search(pattern, comp_lower) or re.search(pattern, val_lower):
                return "Diodes"
        
        # Check MCUs
        for pattern in self.rules["mcu_patterns"]:
            if re.search(pattern, comp_lower) or re.search(pattern, val_lower):
                return "Microcontrollers"
        
        # Check crystals
        for pattern in self.rules["crystal_patterns"]:
            if re.search(pattern, comp_lower) or re.search(pattern, val_lower):
                if 'mhz' in val_lower or 'hz' in val_lower:
                    return "Crystals"
        
        # Check LEDs
        for pattern in self.rules["led_patterns"]:
            if re.search(pattern, comp_lower):
                return "LEDs"
        
        # Check connectors
        for pattern in self.rules["connector_patterns"]:
            if re.search(pattern, comp_lower) or re.search(pattern, val_lower) or re.search(pattern, foot_lower):
                return "Connectors"
        
        # Check switches
        for pattern in self.rules["switch_patterns"]:
            if re.search(pattern, comp_lower) or re.search(pattern, val_lower):
                return "Switches"
        
        return "Other"
    
    def _normalize_component_name(self, component: str, category: str) -> str:
        """Normalize component name"""
        if category == "Resistors":
            return "Resistor"
        elif category == "Capacitors":
            return "Capacitor"
        elif category == "Diodes":
            return "Diode"
        elif category == "Microcontrollers":
            return "Microcontroller"
        elif category == "Crystals":
            return "Crystal"
        elif category == "LEDs":
            return "LED"
        elif category == "Connectors":
            return "Connector"
        elif category == "Switches":
            return "Switch"
        else:
            return component.strip()
    
    def _normalize_value(self, value: str, category: str) -> str:
        """Normalize component value"""
        if not value:
            return ""
        
        value = value.strip()
        
        if category == "Resistors":
            return self._normalize_resistor_value(value)
        elif category == "Capacitors":
            return self._normalize_capacitor_value(value)
        elif category == "Diodes":
            return self._normalize_diode_value(value)
        elif category == "Microcontrollers":
            return self._normalize_mcu_value(value)
        elif category == "Crystals":
            return self._normalize_crystal_value(value)
        else:
            return value
    
    def _normalize_resistor_value(self, value: str) -> str:
        """Normalize resistor values (10k → 10kΩ)"""
        # Remove spaces
        value = value.replace(' ', '')
        
        # Handle various formats
        # 10k, 10K, 10000, 10kohm, 10kΩ
        match = re.match(r'(\d+\.?\d*)\s*([kKmM])?([Ωω]|ohm|ohms)?', value, re.IGNORECASE)
        
        if match:
            num = match.group(1)
            multiplier = match.group(2)
            
            if multiplier:
                mult_upper = multiplier.upper()
                if mult_upper == 'K':
                    return f"{num}kΩ"
                elif mult_upper == 'M':
                    return f"{num}MΩ"
            else:
                # Convert to kΩ if >= 1000
                num_val = float(num)
                if num_val >= 1000000:
                    return f"{num_val/1000000:.1f}MΩ".rstrip('0').rstrip('.')
                elif num_val >= 1000:
                    return f"{num_val/1000:.1f}kΩ".rstrip('0').rstrip('.')
                else:
                    return f"{num}Ω"
        
        return value
    
    def _normalize_capacitor_value(self, value: str) -> str:
        """Normalize capacitor values (100nF → 0.1µF)"""
        # Remove spaces
        value = value.replace(' ', '')
        
        # Handle various formats
        # 0.1uF, 100nF, 22pF, 0.1µF
        match = re.match(r'(\d+\.?\d*)\s*([pnuµ])?[fF]?', value, re.IGNORECASE)
        
        if match:
            num = float(match.group(1))
            unit = match.group(2)
            
            if unit:
                unit_lower = unit.lower()
                if unit_lower == 'p':
                    return f"{num}pF"
                elif unit_lower == 'n':
                    # Convert nF to µF if >= 1000
                    if num >= 1000:
                        return f"{num/1000:.1f}µF".rstrip('0').rstrip('.')
                    else:
                        return f"{num}nF"
                elif unit_lower in ['u', 'µ']:
                    return f"{num}µF"
            else:
                # Assume µF for values < 1, pF for values >= 10
                if num < 1:
                    return f"{num}µF"
                elif num >= 10:
                    return f"{num}pF"
        
        return value
    
    def _normalize_diode_value(self, value: str) -> str:
        """Normalize diode values"""
        value_upper = value.upper().replace(' ', '')
        
        # Common diode part numbers
        if '1N4148' in value_upper:
            return "1N4148"
        elif '1N4007' in value_upper:
            return "1N4007"
        elif '1N5817' in value_upper:
            return "1N5817"
        
        return value
    
    def _normalize_mcu_value(self, value: str) -> str:
        """Normalize MCU names"""
        value_upper = value.upper().replace(' ', '').replace('-', '')
        
        # ATmega variants
        if 'ATMEGA32A' in value_upper:
            return "ATmega32A"
        elif 'ATMEGA32U4' in value_upper:
            return "ATmega32U4"
        elif 'ATMEGA328P' in value_upper:
            return "ATmega328P"
        elif 'ATMEGA328' in value_upper:
            return "ATmega328P"
        elif 'PROMICRO' in value_upper:
            return "Pro Micro"
        
        return value
    
    def _normalize_crystal_value(self, value: str) -> str:
        """Normalize crystal values"""
        value_lower = value.lower().replace(' ', '')
        
        # Extract frequency
        match = re.match(r'(\d+\.?\d*)\s*([mkMK])?[hH][zZ]', value_lower)
        if match:
            num = match.group(1)
            unit = match.group(2)
            
            if unit and unit.lower() == 'm':
                return f"{num}MHz"
            elif unit and unit.lower() == 'k':
                return f"{num}kHz"
            else:
                return f"{num}Hz"
        
        return value
    
    def _normalize_footprint(self, footprint: str, category: str) -> str:
        """Normalize footprint names"""
        if not footprint:
            return ""
        
        foot_upper = footprint.upper().replace(' ', '').replace('-', '')
        
        # Common footprint normalizations
        if 'DO35' in foot_upper or 'DO-35' in footprint:
            return "DO-35"
        elif 'DIP28' in foot_upper or 'DIP-28' in footprint:
            return "DIP-28"
        elif 'DIP40' in foot_upper or 'DIP-40' in footprint:
            return "DIP-40"
        elif '0805' in foot_upper:
            return "0805"
        elif '0603' in foot_upper:
            return "0603"
        elif 'AXIAL' in foot_upper:
            return "Axial"
        elif 'RADIAL' in foot_upper:
            return "Radial"
        
        return footprint
    
    def _extract_package(self, footprint: str, category: str) -> str:
        """Extract package type from footprint"""
        if not footprint:
            return "THT"
        
        foot_upper = footprint.upper()
        
        # SMD packages
        if any(smd in foot_upper for smd in ['0805', '0603', '1206', '0402', 'SOT', 'SOIC', 'QFP', 'QFN']):
            return "SMD"
        
        # THT packages
        if any(tht in foot_upper for tht in ['DIP', 'DO-35', 'AXIAL', 'RADIAL', 'THT', 'THROUGH']):
            return "THT"
        
        # Default to THT for through-hole keyboards
        return "THT"


def create_default_config(output_path: Path):
    """Create default normalization configuration file"""
    config = {
        "resistor_patterns": [
            "(?i)^r\\d+$",
            "(?i)^res",
            "(?i)resistor"
        ],
        "capacitor_patterns": [
            "(?i)^c\\d+$",
            "(?i)^cap",
            "(?i)capacitor"
        ],
        "diode_patterns": [
            "(?i)^d\\d+$",
            "(?i)^diode",
            "(?i)1n4148"
        ],
        "mcu_patterns": [
            "(?i)atmega",
            "(?i)^u\\d+$",
            "(?i)microcontroller",
            "(?i)pro\\s*micro"
        ],
        "crystal_patterns": [
            "(?i)^y\\d+$",
            "(?i)crystal",
            "(?i)xtal"
        ],
        "led_patterns": [
            "(?i)^led",
            "(?i)^d\\d+.*led"
        ],
        "connector_patterns": [
            "(?i)^j\\d+$",
            "(?i)usb",
            "(?i)connector",
            "(?i)header"
        ],
        "switch_patterns": [
            "(?i)^sw\\d+$",
            "(?i)switch",
            "(?i)button",
            "(?i)tactile"
        ]
    }
    
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Created default configuration: {output_path}")


def main():
    """Command-line interface for component normalizer"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: normalize_components.py <command> [args]")
        print("Commands:")
        print("  normalize <component> <value> [footprint]  - Normalize a component")
        print("  create-config <output-file>                - Create default config")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "normalize":
        if len(sys.argv) < 4:
            print("Usage: normalize_components.py normalize <component> <value> [footprint]")
            sys.exit(1)
        
        component = sys.argv[2]
        value = sys.argv[3]
        footprint = sys.argv[4] if len(sys.argv) > 4 else ""
        
        normalizer = ComponentNormalizer()
        result = normalizer.normalize(component, value, footprint)
        
        print(f"Original: {component} {value} {footprint}")
        print(f"Normalized: {result}")
    
    elif command == "create-config":
        if len(sys.argv) < 3:
            print("Usage: normalize_components.py create-config <output-file>")
            sys.exit(1)
        
        output_path = Path(sys.argv[2])
        create_default_config(output_path)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
