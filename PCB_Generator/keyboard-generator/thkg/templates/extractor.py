"""Template extraction from KiCad schematics."""

from pathlib import Path
from typing import List, Optional
from thkg.templates.models import CircuitTemplate, Component, Connection
from thkg.templates.kicad_parser import parse_kicad_schematic


class TemplateExtractor:
    """Extract circuit templates from KiCad schematic files."""
    
    def __init__(self, library_path: Optional[Path] = None):
        """Initialize extractor.
        
        Args:
            library_path: Path to PCB library (default: ../pcb-library)
        """
        if library_path is None:
            # Default to pcb-library relative to this file
            library_path = Path(__file__).parent.parent.parent.parent / "pcb-library"
        
        self.library_path = Path(library_path)
        
        if not self.library_path.exists():
            raise FileNotFoundError(f"PCB library not found: {self.library_path}")
    
    def extract_from_project(self, project_name: str) -> List[CircuitTemplate]:
        """Extract all templates from a project.
        
        Args:
            project_name: Name of project (e.g., 'lumberjack', 'discipline')
            
        Returns:
            List of extracted templates
        """
        from thkg.templates.identifier import CircuitBlockIdentifier
        
        project_path = self.library_path / "design-files" / project_name / "kicad"
        
        if not project_path.exists():
            raise FileNotFoundError(f"Project not found: {project_path}")
        
        # Find schematic file (KiCad 6/7 or KiCad 5)
        schematic_files = list(project_path.glob("*.kicad_sch"))
        if not schematic_files:
            schematic_files = list(project_path.glob("*.sch"))
        
        if not schematic_files:
            raise FileNotFoundError(f"No schematic files found in {project_path}")
        
        # Use first schematic file
        schematic_path = schematic_files[0]
        
        # Check if it's KiCad 5 format
        if schematic_path.suffix == '.sch':
            # KiCad 5 format - not yet supported
            print(f"Warning: {project_name} uses KiCad 5 format (.sch) - skipping")
            return []
        
        # Parse schematic
        components, connections = parse_kicad_schematic(schematic_path)
        
        if not components:
            print(f"Warning: No components found in {project_name}")
            return []
        
        # Identify circuit blocks
        identifier = CircuitBlockIdentifier(components)
        blocks = identifier.identify_all_blocks()
        
        # Create templates for each block
        templates = []
        
        # MCU template
        if blocks.get('mcu'):
            mcu_template = identifier.create_template(
                'mcu',
                f"{project_name}_mcu",
                project_name,
                "1.0"
            )
            if mcu_template:
                templates.append(mcu_template)
        
        # USB template
        if blocks.get('usb'):
            usb_template = identifier.create_template(
                'usb',
                f"{project_name}_usb",
                project_name,
                "1.0"
            )
            if usb_template:
                templates.append(usb_template)
        
        # Crystal template
        if blocks.get('crystal'):
            crystal_template = identifier.create_template(
                'crystal',
                f"{project_name}_crystal",
                project_name,
                "1.0"
            )
            if crystal_template:
                templates.append(crystal_template)
        
        # Reset template
        if blocks.get('reset'):
            reset_template = identifier.create_template(
                'reset',
                f"{project_name}_reset",
                project_name,
                "1.0"
            )
            if reset_template:
                templates.append(reset_template)
        
        # Power template
        if blocks.get('power'):
            power_template = identifier.create_template(
                'power',
                f"{project_name}_power",
                project_name,
                "1.0"
            )
            if power_template:
                templates.append(power_template)
        
        return templates
    
    def extract_mcu_circuit(self, project_name: str) -> Optional[CircuitTemplate]:
        """Extract MCU circuit template from a project.
        
        Args:
            project_name: Name of project
            
        Returns:
            MCU circuit template or None
        """
        # TODO: Implement MCU circuit extraction
        pass
    
    def extract_usb_circuit(self, project_name: str) -> Optional[CircuitTemplate]:
        """Extract USB circuit template from a project.
        
        Args:
            project_name: Name of project
            
        Returns:
            USB circuit template or None
        """
        # TODO: Implement USB circuit extraction
        pass
