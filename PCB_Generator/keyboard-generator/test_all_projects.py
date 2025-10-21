#!/usr/bin/env python3
"""Test parser and identifier on all PCB library projects."""

from pathlib import Path
from thkg.templates.kicad_parser import parse_kicad_schematic
from thkg.templates.identifier import CircuitBlockIdentifier


# All projects in the library
PROJECTS = [
    'lumberjack',
    'discipline', 
    'mysterium',
    'tartan',
    'plaid',
    'litl',
    'kbic65',
    'rosaline',
    'dumbpad',
    'plaid-pad',
    'gh60',
]


def test_project(project_name: str) -> dict:
    """Test parsing and identification for a single project.
    
    Args:
        project_name: Name of project to test
        
    Returns:
        Dictionary with results
    """
    result = {
        'name': project_name,
        'success': False,
        'components': 0,
        'blocks': {},
        'error': None,
        'schematic_found': False,
    }
    
    # Find schematic file
    project_path = Path(f"../pcb-library/design-files/{project_name}/kicad")
    
    if not project_path.exists():
        result['error'] = "Project directory not found"
        return result
    
    # Find schematic file (.kicad_sch for KiCad 6/7, .sch for KiCad 5)
    schematic_files = list(project_path.glob("*.kicad_sch"))
    if not schematic_files:
        schematic_files = list(project_path.glob("*.sch"))
    
    if not schematic_files:
        result['error'] = "No schematic file found"
        return result
    
    result['schematic_found'] = True
    schematic_path = schematic_files[0]
    
    try:
        # Parse schematic
        components, connections = parse_kicad_schematic(schematic_path)
        result['components'] = len(components)
        
        # Identify blocks
        identifier = CircuitBlockIdentifier(components)
        blocks = identifier.identify_all_blocks()
        
        # Get summary
        result['blocks'] = {
            block_type: len(comps) 
            for block_type, comps in blocks.items() 
            if len(comps) > 0
        }
        
        result['success'] = True
        
    except Exception as e:
        result['error'] = str(e)
    
    return result


def main():
    """Test all projects."""
    print("=" * 80)
    print("Testing Parser on All PCB Library Projects")
    print("=" * 80)
    print()
    
    results = []
    
    for project in PROJECTS:
        print(f"📄 Testing: {project:15s} ... ", end='', flush=True)
        result = test_project(project)
        results.append(result)
        
        if result['success']:
            print(f"✅ {result['components']:3d} components")
        elif not result['schematic_found']:
            print(f"⚠️  No schematic")
        else:
            print(f"❌ {result['error']}")
    
    print()
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print()
    
    # Success rate
    successful = [r for r in results if r['success']]
    print(f"✅ Successful: {len(successful)}/{len(PROJECTS)} projects")
    print()
    
    # Detailed results
    if successful:
        print("📊 Component Counts:")
        for result in successful:
            print(f"   {result['name']:15s}: {result['components']:3d} components")
        print()
        
        print("🔍 Circuit Blocks Found:")
        print()
        
        # Collect all block types
        all_block_types = set()
        for result in successful:
            all_block_types.update(result['blocks'].keys())
        
        # Show blocks for each project
        for result in successful:
            print(f"   {result['name']:15s}:")
            blocks = result['blocks']
            
            if blocks.get('mcu', 0) > 0:
                print(f"      MCU:     {blocks['mcu']} components")
            if blocks.get('usb', 0) > 0:
                print(f"      USB:     {blocks['usb']} components")
            if blocks.get('crystal', 0) > 0:
                print(f"      Crystal: {blocks['crystal']} components")
            if blocks.get('reset', 0) > 0:
                print(f"      Reset:   {blocks['reset']} components")
            if blocks.get('matrix', 0) > 0:
                switches = blocks['matrix'] // 2  # Approximate (switches + diodes)
                print(f"      Matrix:  {blocks['matrix']} components (~{switches} keys)")
            print()
    
    # Failed projects
    failed = [r for r in results if not r['success']]
    if failed:
        print("❌ Failed Projects:")
        for result in failed:
            print(f"   {result['name']:15s}: {result['error']}")
        print()
    
    # Template extraction opportunities
    print("🎨 Template Extraction Opportunities:")
    print()
    
    mcu_projects = {}
    usb_projects = {}
    
    for result in successful:
        # Identify MCU type (would need to parse actual component values)
        if result['blocks'].get('mcu', 0) > 0:
            # For now, just list projects with MCU
            mcu_projects[result['name']] = result['blocks']['mcu']
        
        if result['blocks'].get('usb', 0) > 0:
            usb_projects[result['name']] = result['blocks']['usb']
    
    if mcu_projects:
        print("   MCU Templates available from:")
        for project, count in mcu_projects.items():
            print(f"      - {project}")
    
    if usb_projects:
        print()
        print("   USB Templates available from:")
        for project, count in usb_projects.items():
            print(f"      - {project}")
    
    print()
    print("=" * 80)
    
    return len(successful) == len(PROJECTS)


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
