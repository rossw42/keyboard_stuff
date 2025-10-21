#!/usr/bin/env python3
"""Create routing templates from best example PCBs.

This script creates reusable routing templates from the PCBs with the best
routing examples (lumberjack, dumbpad, etc.).
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from thkg.templates.routing_template import RoutingTemplateExtractor


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    routing_data_dir = script_dir / "routing_data"
    templates_dir = script_dir / "routing_templates"
    
    if not routing_data_dir.exists():
        print(f"Error: Routing data directory not found: {routing_data_dir}")
        print("Run extract_routing_patterns.py first")
        sys.exit(1)
    
    # Create extractor
    extractor = RoutingTemplateExtractor(routing_data_dir)
    
    # Define PCBs to extract templates from
    pcbs_to_extract = [
        ('lumberjack', 'lumberjack', 'Full-size keyboard with extensive routing'),
        ('dumbpad', 'dumbpad', '4x4 macropad with matrix routing'),
        ('litl', 'litl', 'Compact keyboard with efficient routing'),
    ]
    
    print("Creating routing templates...")
    print("="*80)
    
    templates_created = 0
    
    for project, pcb_name, description in pcbs_to_extract:
        print(f"\nExtracting: {project}/{pcb_name}")
        print(f"  Description: {description}")
        
        try:
            template = extractor.extract_template(project, pcb_name)
            
            if template:
                template.description = description
                
                # Print template info
                width, height = template.get_dimensions()
                print(f"  ✓ Template created:")
                print(f"    Matrix: {template.row_count} rows × {template.col_count} cols")
                print(f"    Dimensions: {width:.1f}mm × {height:.1f}mm")
                print(f"    Nets: {len(template.routing.nets)}")
                print(f"    Traces: {len(template.routing.traces)}")
                print(f"    Vias: {len(template.routing.vias)}")
                print(f"    Zones: {len(template.routing.zones)}")
                
                # Save template
                extractor.save_template(template, templates_dir)
                templates_created += 1
            else:
                print(f"  ✗ Failed to create template")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print(f"✓ Created {templates_created} routing templates")
    print(f"✓ Templates saved to: {templates_dir}")
    
    # List created templates
    if templates_dir.exists():
        template_files = list(templates_dir.glob("*_template.json"))
        print(f"\nAvailable templates:")
        for template_file in sorted(template_files):
            print(f"  - {template_file.name}")


if __name__ == "__main__":
    main()
