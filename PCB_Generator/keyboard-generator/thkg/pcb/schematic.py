"""KiCad schematic generation.

Generates KiCad schematic files by combining templates and creating switch matrices.
"""

from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from thkg.templates.models import CircuitTemplate, Component, Connection
from thkg.templates.manager import TemplateManager
from thkg.config import Configuration


class SchematicGenerator:
    """Generate KiCad schematic files."""
    
    def __init__(self, config: Configuration):
        """Initialize schematic generator.
        
        Args:
            config: Keyboard configuration
        """
        self.config = config
        self.template_manager = TemplateManager()
        self.components: List[Component] = []
        self.connections: List[Connection] = []
        
    def generate(self, output_path: Path) -> bool:
        """Generate complete schematic.
        
        Args:
            output_path: Path to output .kicad_sch file
            
        Returns:
            True if successful
        """
        print(f"🎨 Generating schematic: {output_path.name}")
        
        # Load templates
        self._load_templates()
        
        # Generate switch matrix
        self._generate_matrix()
        
        # Combine circuits
        self._combine_circuits()
        
        # Validate schematic
        self._validate_schematic()
        
        # Write schematic file
        self._write_schematic(output_path)
        
        print(f"   ✅ Schematic generated: {len(self.components)} components")
        
        return True
    
    def _validate_schematic(self):
        """Validate generated schematic."""
        from thkg.pcb.validator import SchematicValidator
        
        print("   🔍 Validating schematic...")
        
        validator = SchematicValidator(self.components, self.connections)
        errors, warnings, info = validator.validate()
        
        if errors:
            print(f"      ❌ {len(errors)} errors found")
            for error in errors:
                print(f"         • {error}")
        
        if warnings:
            print(f"      ⚠️  {len(warnings)} warnings")
        
        print(f"      ✅ Validation complete")
    
    def _load_templates(self):
        """Load required templates from cache."""
        print("   📦 Loading templates...")
        
        # Determine MCU type from config
        mcu_type = self.config.hardware.get('mcu', {}).get('type', 'atmega328p')
        
        # Load MCU template
        if mcu_type == 'atmega328p':
            mcu_template = self.template_manager.get_template('lumberjack_mcu')
        elif mcu_type == 'pro_micro':
            mcu_template = self.template_manager.get_template('litl_mcu')
        else:
            mcu_template = self.template_manager.get_template('lumberjack_mcu')  # Default
        
        if mcu_template:
            self.components.extend(mcu_template.components)
            print(f"      ✅ MCU: {mcu_template.name}")
        
        # Load USB template
        usb_template = self.template_manager.get_template('lumberjack_usb')
        if usb_template:
            self.components.extend(usb_template.components)
            print(f"      ✅ USB: {usb_template.name}")
        
        # Load crystal template
        crystal_template = self.template_manager.get_template('lumberjack_crystal')
        if crystal_template:
            self.components.extend(crystal_template.components)
            print(f"      ✅ Crystal: {crystal_template.name}")
        
        # Load reset template
        reset_template = self.template_manager.get_template('lumberjack_reset')
        if reset_template:
            self.components.extend(reset_template.components)
            print(f"      ✅ Reset: {reset_template.name}")
        
        # Load power template
        power_template = self.template_manager.get_template('lumberjack_power')
        if power_template:
            self.components.extend(power_template.components)
            print(f"      ✅ Power: {power_template.name}")
    
    def _generate_matrix(self):
        """Generate switch matrix components."""
        from thkg.pcb.matrix import MatrixGenerator
        
        print("   ⌨️  Generating switch matrix...")
        
        # Get layout from config
        layout = self.config.layout
        num_switches = len(layout.get('switches', []))
        
        if num_switches == 0:
            # Use default 60-key layout
            num_switches = 60
        
        print(f"      Creating matrix for {num_switches} switches")
        
        # Generate matrix
        matrix_gen = MatrixGenerator(num_switches)
        switches, diodes = matrix_gen.generate_components()
        
        # Add to components
        self.components.extend(switches)
        self.components.extend(diodes)
        
        # Generate connections
        matrix_connections = matrix_gen.generate_connections(switches, diodes)
        self.connections.extend(matrix_connections)
        
        # Store matrix info
        self.matrix_rows = matrix_gen.rows
        self.matrix_cols = matrix_gen.cols
        self.pin_assignments = matrix_gen.get_pin_assignments()
        
        print(f"      ✅ Created {len(switches)} switches + {len(diodes)} diodes")
        print(f"      ✅ Matrix: {self.matrix_rows}x{self.matrix_cols}")
        print(f"      ✅ Generated {len(matrix_connections)} connections")
    
    def _combine_circuits(self):
        """Combine all circuits and create connections."""
        print("   🔗 Combining circuits...")
        
        # Connect matrix rows to MCU
        for i, row_pin in enumerate(self.pin_assignments['rows']):
            connection = Connection(
                net_name=f"ROW{i}",
                pins=[
                    ("U1", row_pin),  # MCU pin
                ]
            )
            self.connections.append(connection)
        
        # Connect matrix columns to MCU
        for i, col_pin in enumerate(self.pin_assignments['cols']):
            connection = Connection(
                net_name=f"COL{i}",
                pins=[
                    ("U1", col_pin),  # MCU pin
                ]
            )
            self.connections.append(connection)
        
        # Power connections
        vcc_connection = Connection(
            net_name="VCC",
            pins=[
                ("U1", "VCC"),
                ("J1", "VBUS"),  # USB power
                ("C4", "1"),     # Decoupling cap
                ("C5", "1"),     # Decoupling cap
            ]
        )
        self.connections.append(vcc_connection)
        
        gnd_connection = Connection(
            net_name="GND",
            pins=[
                ("U1", "GND"),
                ("J1", "GND"),
                ("C3", "2"),
                ("C4", "2"),
                ("C5", "2"),
            ]
        )
        self.connections.append(gnd_connection)
        
        print(f"      ✅ Combined {len(self.components)} components")
        print(f"      ✅ Created {len(self.connections)} total connections")
    
    def _write_schematic(self, output_path: Path):
        """Write KiCad schematic file.
        
        Args:
            output_path: Path to output file
        """
        print("   💾 Writing schematic file...")
        
        # Create output directory
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate KiCad S-expression format
        schematic_content = self._generate_kicad_schematic()
        
        # Write to file
        with open(output_path, 'w') as f:
            f.write(schematic_content)
        
        print(f"      ✅ Written to {output_path}")
    
    def _generate_kicad_schematic(self) -> str:
        """Generate KiCad schematic S-expression content.
        
        Returns:
            Schematic file content
        """
        # KiCad schematic header
        content = f"""(kicad_sch (version 20230121) (generator thkg)

  (uuid {self._generate_uuid()})

  (paper "A4")

  (title_block
    (title "{self.config.keyboard.get('name', 'Generated Keyboard')}")
    (date "{datetime.now().strftime('%Y-%m-%d')}")
    (rev "1.0")
    (comment 1 "Generated by THKG")
  )

  (lib_symbols
"""
        
        # Add library symbols (simplified for now)
        content += """    (symbol "Device:R" (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
      (property "Value" "R" (at 0 0 90) (effects (font (size 1.27 1.27))))
    )
"""
        
        content += "  )\n\n"
        
        # Add component instances (simplified)
        for i, comp in enumerate(self.components[:10]):  # First 10 for now
            x = 50 + (i % 5) * 20
            y = 50 + (i // 5) * 20
            
            content += f"""  (symbol (lib_id "{comp.library}:{comp.value}") (at {x} {y} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid {self._generate_uuid()})
    (property "Reference" "{comp.reference}" (at {x} {y-5} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "{comp.value}" (at {x} {y+5} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "{comp.footprint}" (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
  )

"""
        
        content += ")\n"
        
        return content
    
    def _generate_uuid(self) -> str:
        """Generate a UUID for KiCad.
        
        Returns:
            UUID string
        """
        import uuid
        return str(uuid.uuid4())
