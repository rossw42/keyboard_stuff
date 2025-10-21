#!/usr/bin/env python3
"""Test template extraction from all working projects."""

from pathlib import Path
from thkg.templates.extractor import TemplateExtractor


def main():
    """Extract templates from all working projects."""
    
    print("=" * 80)
    print("Template Extraction Test")
    print("=" * 80)
    print()
    
    # Projects that work with our parser (KiCad 6/7)
    working_projects = ['lumberjack', 'litl', 'dumbpad']
    
    # Initialize extractor
    extractor = TemplateExtractor()
    
    all_templates = []
    
    for project in working_projects:
        print(f"📦 Extracting from: {project}")
        print()
        
        try:
            templates = extractor.extract_from_project(project)
            
            if templates:
                print(f"   ✅ Extracted {len(templates)} templates:")
                for template in templates:
                    print(f"      - {template.name:30s} ({template.type:10s}) {len(template.components):3d} components")
                    all_templates.append(template)
                print()
            else:
                print(f"   ⚠️  No templates extracted")
                print()
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print()
    
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print()
    
    print(f"✅ Total templates extracted: {len(all_templates)}")
    print()
    
    # Group by type
    by_type = {}
    for template in all_templates:
        if template.type not in by_type:
            by_type[template.type] = []
        by_type[template.type].append(template)
    
    print("📊 Templates by Type:")
    for template_type, templates in sorted(by_type.items()):
        print(f"   {template_type:10s}: {len(templates)} templates")
        for template in templates:
            print(f"      - {template.name:30s} from {template.source_project}")
    print()
    
    # Show detailed info for key templates
    print("🔍 Key Templates:")
    print()
    
    # MCU templates
    mcu_templates = by_type.get('mcu', [])
    if mcu_templates:
        print("   MCU Templates:")
        for template in mcu_templates:
            mcu_comp = template.components[0] if template.components else None
            if mcu_comp:
                print(f"      {template.source_project:15s}: {mcu_comp.value:20s} ({mcu_comp.footprint})")
        print()
    
    # USB templates
    usb_templates = by_type.get('usb', [])
    if usb_templates:
        print("   USB Templates:")
        for template in usb_templates:
            usb_comp = [c for c in template.components if 'USB' in c.symbol.upper()]
            if usb_comp:
                print(f"      {template.source_project:15s}: {usb_comp[0].value:20s} ({len(template.components)} components)")
        print()
    
    # Crystal templates
    crystal_templates = by_type.get('crystal', [])
    if crystal_templates:
        print("   Crystal Templates:")
        for template in crystal_templates:
            crystal_comp = [c for c in template.components if c.reference.startswith('Y')]
            if crystal_comp:
                print(f"      {template.source_project:15s}: {crystal_comp[0].value:20s} ({len(template.components)} components)")
        print()
    
    print("=" * 80)
    print(f"✅ Template extraction complete!")
    print("=" * 80)
    
    return all_templates


if __name__ == "__main__":
    templates = main()
