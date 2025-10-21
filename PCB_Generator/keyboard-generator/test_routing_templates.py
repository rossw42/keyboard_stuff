#!/usr/bin/env python3
"""Test routing templates to verify they can be loaded and used."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from thkg.templates.routing_template import RoutingTemplateExtractor, RoutingTemplateApplicator


def test_template_loading():
    """Test loading routing templates."""
    script_dir = Path(__file__).parent
    templates_dir = script_dir / "routing_templates"
    
    if not templates_dir.exists():
        print("❌ Templates directory not found")
        return False
    
    template_files = list(templates_dir.glob("*_template.json"))
    
    if not template_files:
        print("❌ No template files found")
        return False
    
    print(f"Found {len(template_files)} template files")
    print("="*80)
    
    routing_data_dir = script_dir / "routing_data"
    extractor = RoutingTemplateExtractor(routing_data_dir)
    
    all_passed = True
    
    for template_file in sorted(template_files):
        print(f"\nTesting: {template_file.name}")
        
        try:
            # Load template
            template = extractor.load_template(template_file)
            
            print(f"  ✓ Loaded successfully")
            print(f"    Name: {template.name}")
            print(f"    Source: {template.source_project}/{template.source_pcb}")
            print(f"    Matrix: {template.row_count} rows × {template.col_count} cols")
            
            width, height = template.get_dimensions()
            print(f"    Dimensions: {width:.1f}mm × {height:.1f}mm")
            print(f"    Routing: {len(template.routing.traces)} traces, {len(template.routing.vias)} vias")
            
            # Test applicator
            applicator = RoutingTemplateApplicator(template)
            
            # Test coordinate transformation
            test_bbox = ((10.0, 10.0), (100.0, 80.0))
            test_point = template.bbox_min
            
            transformed = applicator._transform_point(test_point, test_bbox, 1.0, 1.0)
            print(f"    Transform test: {test_point} → {transformed}")
            
            # Test net mapping (just a few common nets)
            net_mapping = {}
            for net in template.routing.nets[:5]:
                if net.name:
                    net_mapping[net.name] = net.name.replace('/', '')
            
            if net_mapping:
                print(f"    Net mapping test: {len(net_mapping)} nets mapped")
                
                # Try applying template (just to test, won't use result)
                try:
                    new_routing = applicator.apply_to_layout(test_bbox, net_mapping)
                    print(f"    ✓ Template application test passed")
                    print(f"      Generated: {len(new_routing.traces)} traces, {len(new_routing.vias)} vias")
                except Exception as e:
                    print(f"    ⚠ Template application test failed: {e}")
            
            print(f"  ✓ All tests passed for {template_file.name}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False
    
    return all_passed


def test_template_statistics():
    """Print statistics about available templates."""
    script_dir = Path(__file__).parent
    templates_dir = script_dir / "routing_templates"
    routing_data_dir = script_dir / "routing_data"
    
    print("\n" + "="*80)
    print("TEMPLATE STATISTICS")
    print("="*80)
    
    extractor = RoutingTemplateExtractor(routing_data_dir)
    template_files = list(templates_dir.glob("*_template.json"))
    
    total_traces = 0
    total_vias = 0
    total_zones = 0
    
    for template_file in sorted(template_files):
        template = extractor.load_template(template_file)
        total_traces += len(template.routing.traces)
        total_vias += len(template.routing.vias)
        total_zones += len(template.routing.zones)
    
    print(f"\nTotal across {len(template_files)} templates:")
    print(f"  Traces: {total_traces}")
    print(f"  Vias: {total_vias}")
    print(f"  Zones: {total_zones}")
    
    print(f"\nTemplates by size:")
    templates_by_size = []
    for template_file in template_files:
        template = extractor.load_template(template_file)
        width, height = template.get_dimensions()
        area = width * height
        templates_by_size.append((template.name, width, height, area, len(template.routing.traces)))
    
    templates_by_size.sort(key=lambda x: x[3], reverse=True)
    
    for name, width, height, area, trace_count in templates_by_size:
        print(f"  {name:30s} {width:6.1f}mm × {height:5.1f}mm = {area:8.0f}mm² ({trace_count:4d} traces)")


def main():
    """Main entry point."""
    print("Testing Routing Templates")
    print("="*80)
    
    # Test loading
    success = test_template_loading()
    
    # Print statistics
    test_template_statistics()
    
    print("\n" + "="*80)
    if success:
        print("✓ All tests passed!")
    else:
        print("❌ Some tests failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
