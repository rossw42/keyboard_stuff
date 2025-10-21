#!/usr/bin/env python3
"""Build the complete template library from PCB projects."""

from pathlib import Path
from thkg.templates.extractor import TemplateExtractor
from thkg.templates.manager import TemplateManager


def main():
    """Build template library."""
    
    print("=" * 80)
    print("Building Template Library")
    print("=" * 80)
    print()
    
    # Projects that work with our parser (KiCad 6/7)
    working_projects = ['lumberjack', 'litl', 'dumbpad']
    
    # Initialize
    extractor = TemplateExtractor()
    manager = TemplateManager()
    
    # Clear existing cache
    print("🗑️  Clearing existing cache...")
    manager.clear_cache()
    print()
    
    # Extract templates from each project
    all_templates = []
    
    for project in working_projects:
        print(f"📦 Extracting from: {project}")
        
        try:
            templates = extractor.extract_from_project(project)
            
            if templates:
                print(f"   ✅ Extracted {len(templates)} templates")
                all_templates.extend(templates)
            else:
                print(f"   ⚠️  No templates extracted")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    # Cache all templates
    print("💾 Caching templates...")
    manager.cache_templates(all_templates)
    print(f"   ✅ Cached {len(all_templates)} templates")
    print()
    
    # Verify cache
    print("🔍 Verifying cache...")
    cached_templates = manager.list_templates()
    print(f"   ✅ {len(cached_templates)} templates in cache")
    print()
    
    # Show statistics
    stats = manager.get_cache_stats()
    
    print("=" * 80)
    print("Template Library Statistics")
    print("=" * 80)
    print()
    
    print(f"📊 Total Templates: {stats['total']}")
    print()
    
    print("By Type:")
    for template_type, count in sorted(stats['by_type'].items()):
        print(f"   {template_type:10s}: {count}")
    print()
    
    print("By Project:")
    for project, count in sorted(stats['by_project'].items()):
        print(f"   {project:15s}: {count}")
    print()
    
    # Show template details
    print("=" * 80)
    print("Template Details")
    print("=" * 80)
    print()
    
    for template_type in ['mcu', 'usb', 'crystal', 'reset', 'power']:
        templates = manager.get_templates_by_type(template_type)
        if templates:
            print(f"🔧 {template_type.upper()} Templates:")
            for template in templates:
                print(f"   {template.name:30s} - {len(template.components)} components from {template.source_project}")
            print()
    
    print("=" * 80)
    print("✅ Template library built successfully!")
    print(f"📁 Cache location: {manager.cache_dir}")
    print("=" * 80)
    
    return manager


if __name__ == "__main__":
    manager = main()
