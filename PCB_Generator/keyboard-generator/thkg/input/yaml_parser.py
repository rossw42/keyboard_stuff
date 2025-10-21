"""YAML configuration parser"""

import yaml
from pathlib import Path
from typing import Dict, Any
from thkg.config import (
    Configuration, KeyboardType, LayoutStyle, MCUType, USBType,
    Matrix, PCBConfig, PlateConfig, CaseConfig, FirmwareConfig, Switch
)


class YAMLParser:
    """Parse YAML configuration files"""
    
    def parse(self, yaml_path: str) -> Configuration:
        """Parse YAML configuration file
        
        Args:
            yaml_path: Path to YAML configuration file
            
        Returns:
            Configuration object
            
        Raises:
            FileNotFoundError: If YAML file doesn't exist
            yaml.YAMLError: If YAML is malformed
        """
        path = Path(yaml_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {yaml_path}")
        
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        return self._parse_config(data)
    
    def _parse_config(self, data: Dict[str, Any]) -> Configuration:
        """Parse configuration dictionary into Configuration object"""
        config = Configuration()
        
        # Keyboard metadata
        if 'keyboard' in data:
            kb = data['keyboard']
            config.name = kb.get('name', config.name)
            config.description = kb.get('description', config.description)
            config.version = kb.get('version', config.version)
        
        # Layout configuration
        if 'layout' in data:
            layout = data['layout']
            config.layout_preset = layout.get('type')
            config.kle_file = layout.get('kle_file')
            
            # Parse custom switches if provided
            if 'switches' in layout:
                config.switches = [
                    Switch(
                        row=s.get('row', 0),
                        col=s.get('col', 0),
                        x=s.get('x', 0.0),
                        y=s.get('y', 0.0),
                        width=s.get('width', 1.0),
                        height=s.get('height', 1.0),
                        rotation=s.get('rotation', 0.0),
                        stabilizer=s.get('stabilizer'),
                        label=s.get('label', '')
                    )
                    for s in layout['switches']
                ]
        
        # Hardware configuration
        if 'hardware' in data:
            hw = data['hardware']
            if 'mcu' in hw:
                mcu_type = hw['mcu'].get('type', 'atmega328p')
                config.mcu_type = MCUType(mcu_type)
            if 'usb' in hw:
                usb_type = hw['usb'].get('type', 'usb-c-tht')
                config.usb_type = USBType(usb_type)
        
        # Matrix configuration
        if 'matrix' in data:
            m = data['matrix']
            config.matrix = Matrix(
                rows=m.get('rows', 5),
                cols=m.get('cols', 14),
                diode_direction=m.get('diode_direction', 'COL2ROW'),
                row_pins=m.get('row_pins', []),
                col_pins=m.get('col_pins', [])
            )
        
        # PCB configuration
        if 'pcb' in data:
            pcb = data['pcb']
            if 'dimensions' in pcb:
                dims = pcb['dimensions']
                config.pcb = PCBConfig(
                    length=dims.get('length', 285.0),
                    width=dims.get('width', 94.6),
                    thickness=dims.get('thickness', 1.6)
                )
        
        # Plate configuration
        if 'plate' in data:
            plate = data['plate']
            config.plate = PlateConfig(
                enabled=plate.get('enabled', True),
                switch_type=plate.get('switch_type', 'mx'),
                thickness=plate.get('thickness', 1.5),
                material=plate.get('material', 'fr4')
            )
        
        # Case configuration
        if 'case' in data:
            case = data['case']
            config.case = CaseConfig(
                enabled=case.get('enabled', True),
                case_type=case.get('type', 'sandwich'),
                layers=case.get('layers', [])
            )
        
        # Firmware configuration
        if 'firmware' in data:
            fw = data['firmware']
            config.firmware = FirmwareConfig(
                qmk=fw.get('qmk', True),
                via=fw.get('via', True),
                vial=fw.get('vial', False),
                default_keymap=fw.get('default_keymap', 'ansi')
            )
        
        # Output options
        if 'output' in data:
            out = data['output']
            config.output_gerbers = out.get('gerbers', True)
            config.output_kicad = out.get('kicad_files', True)
            config.output_plate_dxf = out.get('plate_dxf', True)
            config.output_case_stl = out.get('case_stl', True)
            config.output_case_dxf = out.get('case_dxf', True)
            config.output_firmware = out.get('firmware', True)
            config.output_bom = out.get('bom', True)
            config.output_build_guide = out.get('build_guide', True)
        
        return config
    
    def save(self, config: Configuration, output_path: str):
        """Save configuration to YAML file
        
        Args:
            config: Configuration object to save
            output_path: Path to save YAML file
        """
        data = {
            'keyboard': {
                'name': config.name,
                'description': config.description,
                'version': config.version
            },
            'layout': {
                'type': config.layout_preset,
                'kle_file': config.kle_file
            },
            'hardware': {
                'mcu': {'type': config.mcu_type.value},
                'usb': {'type': config.usb_type.value}
            },
            'pcb': {
                'dimensions': {
                    'length': config.pcb.length,
                    'width': config.pcb.width,
                    'thickness': config.pcb.thickness
                }
            },
            'plate': {
                'enabled': config.plate.enabled,
                'switch_type': config.plate.switch_type,
                'thickness': config.plate.thickness,
                'material': config.plate.material
            },
            'case': {
                'enabled': config.case.enabled,
                'type': config.case.case_type,
                'layers': config.case.layers
            },
            'firmware': {
                'qmk': config.firmware.qmk,
                'via': config.firmware.via,
                'vial': config.firmware.vial,
                'default_keymap': config.firmware.default_keymap
            },
            'output': {
                'gerbers': config.output_gerbers,
                'kicad_files': config.output_kicad,
                'plate_dxf': config.output_plate_dxf,
                'case_stl': config.output_case_stl,
                'case_dxf': config.output_case_dxf,
                'firmware': config.output_firmware,
                'bom': config.output_bom,
                'build_guide': config.output_build_guide
            }
        }
        
        with open(output_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
