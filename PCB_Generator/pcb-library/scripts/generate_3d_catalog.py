#!/usr/bin/env python3
"""
3D Model Catalog Generator

Generates a comprehensive catalog of all 3D models and CAD drawings
with descriptions, dimensions, material recommendations, and source links.

Usage: python3 generate_3d_catalog.py
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json

# Configuration
SCRIPT_DIR = Path(__file__).parent
PCB_ROOT = SCRIPT_DIR.parent
MODELS_DIR = PCB_ROOT / "3d-models"
CAD_DIR = PCB_ROOT / "cad-drawings"
CATALOG_FILE = PCB_ROOT / "docs" / "3d_model_catalog.md"

# File size thresholds (bytes)
SIZE_SMALL = 1024 * 100  # 100KB
SIZE_MEDIUM = 1024 * 1024  # 1MB
SIZE_LARGE = 1024 * 1024 * 10  # 10MB


def get_file_size_str(size_bytes: int) -> str:
    """Convert file size to human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def estimate_print_time(size_bytes: int) -> str:
    """Estimate 3D print time based on file size (rough approximation)."""
    if size_bytes < SIZE_SMALL:
        return "< 1 hour"
    elif size_bytes < SIZE_MEDIUM:
        return "1-3 hours"
    elif size_bytes < SIZE_LARGE:
        return "3-8 hours"
    else:
        return "8+ hours"


def get_material_recommendations(filename: str) -> List[str]:
    """Get material recommendations based on component type."""
    filename_lower = filename.lower()
    
    if any(word in filename_lower for word in ['case', 'housing', 'enclosure', 'shell', 'body']):
        return ['PLA', 'PETG', 'ABS']
    elif any(word in filename_lower for word in ['plate', 'switch']):
        return ['PLA (rigid)', 'PETG', 'Polycarbonate']
    elif any(word in filename_lower for word in ['cover', 'lid', 'top', 'bottom']):
        return ['PLA', 'PETG', 'ABS']
    elif any(word in filename_lower for word in ['cradle', 'holder', 'support']):
        return ['PLA', 'PETG']
    else:
        return ['PLA', 'PETG']


def get_print_settings(filename: str, size_bytes: int) -> Dict[str, str]:
    """Get recommended print settings based on file type and size."""
    filename_lower = filename.lower()
    
    settings = {
        'layer_height': '0.2mm',
        'infill': '20%',
        'supports': 'Auto',
        'orientation': 'Check model'
    }
    
    # Adjust for specific types
    if 'plate' in filename_lower:
        settings['layer_height'] = '0.15mm'
        settings['infill'] = '30%'
        settings['orientation'] = 'Flat on bed'
    elif any(word in filename_lower for word in ['case', 'housing']):
        settings['infill'] = '25%'
        settings['supports'] = 'Likely required'
    elif any(word in filename_lower for word in ['cover', 'lid']):
        settings['infill'] = '15%'
        settings['supports'] = 'Minimal'
    
    # Adjust for size
    if size_bytes > SIZE_LARGE:
        settings['infill'] = '15%'  # Reduce infill for large prints
    
    return settings


def get_cutting_settings(filename: str) -> Dict[str, str]:
    """Get recommended cutting settings for DXF files."""
    filename_lower = filename.lower()
    
    settings = {
        'material': 'Acrylic, Wood, or Metal',
        'thickness': '1.5-3mm',
        'method': 'Laser cutting or CNC'
    }
    
    if 'plate' in filename_lower:
        settings['material'] = 'Acrylic, FR4, Aluminum, or Steel'
        settings['thickness'] = '1.5mm (standard switch plate)'
        settings['method'] = 'Laser cutting (acrylic/wood) or CNC (metal)'
    elif 'case' in filename_lower:
        settings['material'] = 'Acrylic or Wood'
        settings['thickness'] = '3-5mm'
        settings['method'] = 'Laser cutting or CNC routing'
    
    return settings


def scan_3d_models() -> Dict[str, List[Dict]]:
    """Scan all 3D model directories and collect file information."""
    models = {
        'cases': [],
        'plates': [],
        'accessories': []
    }
    
    # Scan cases
    cases_dir = MODELS_DIR / "cases"
    if cases_dir.exists():
        for project_dir in sorted(cases_dir.iterdir()):
            if project_dir.is_dir():
                project_name = project_dir.name
                
                # Scan STL files
                stl_dir = project_dir / "stl"
                if stl_dir.exists():
                    for stl_file in sorted(stl_dir.glob("*.stl")):
                        file_size = stl_file.stat().st_size
                        models['cases'].append({
                            'project': project_name,
                            'filename': stl_file.name,
                            'path': str(stl_file.relative_to(PCB_ROOT)),
                            'type': 'STL',
                            'category': 'Case',
                            'size': file_size,
                            'size_str': get_file_size_str(file_size)
                        })
                
                # Scan STEP files
                step_dir = project_dir / "step"
                if step_dir.exists():
                    for step_file in sorted(step_dir.glob("*.step")) + sorted(step_dir.glob("*.stp")):
                        file_size = step_file.stat().st_size
                        models['cases'].append({
                            'project': project_name,
                            'filename': step_file.name,
                            'path': str(step_file.relative_to(PCB_ROOT)),
                            'type': 'STEP',
                            'category': 'Case',
                            'size': file_size,
                            'size_str': get_file_size_str(file_size)
                        })
    
    # Scan plates
    plates_dir = MODELS_DIR / "plates"
    if plates_dir.exists():
        for project_dir in sorted(plates_dir.iterdir()):
            if project_dir.is_dir():
                project_name = project_dir.name
                
                for model_file in sorted(project_dir.glob("*.stl")) + sorted(project_dir.glob("*.step")) + sorted(project_dir.glob("*.stp")):
                    file_size = model_file.stat().st_size
                    file_type = 'STEP' if model_file.suffix.lower() in ['.step', '.stp'] else 'STL'
                    models['plates'].append({
                        'project': project_name,
                        'filename': model_file.name,
                        'path': str(model_file.relative_to(PCB_ROOT)),
                        'type': file_type,
                        'category': 'Plate',
                        'size': file_size,
                        'size_str': get_file_size_str(file_size)
                    })
    
    # Scan accessories
    accessories_dir = MODELS_DIR / "accessories"
    if accessories_dir.exists():
        for category_dir in sorted(accessories_dir.iterdir()):
            if category_dir.is_dir():
                category_name = category_dir.name.replace('-', ' ').title()
                
                for project_dir in sorted(category_dir.iterdir()):
                    if project_dir.is_dir():
                        project_name = project_dir.name
                        
                        for model_file in sorted(project_dir.glob("*.stl")) + sorted(project_dir.glob("*.step")) + sorted(project_dir.glob("*.stp")):
                            file_size = model_file.stat().st_size
                            file_type = 'STEP' if model_file.suffix.lower() in ['.step', '.stp'] else 'STL'
                            models['accessories'].append({
                                'project': project_name,
                                'filename': model_file.name,
                                'path': str(model_file.relative_to(PCB_ROOT)),
                                'type': file_type,
                                'category': category_name,
                                'size': file_size,
                                'size_str': get_file_size_str(file_size)
                            })
    
    return models


def scan_cad_drawings() -> Dict[str, List[Dict]]:
    """Scan all CAD drawing directories and collect file information."""
    drawings = {
        'plates': [],
        'cases': [],
        'covers': []
    }
    
    for category in ['plates', 'cases', 'covers']:
        category_dir = CAD_DIR / category
        if category_dir.exists():
            for project_dir in sorted(category_dir.iterdir()):
                if project_dir.is_dir():
                    project_name = project_dir.name
                    
                    for cad_file in sorted(project_dir.glob("*.dxf")) + sorted(project_dir.glob("*.svg")) + sorted(project_dir.glob("*.dwg")):
                        file_size = cad_file.stat().st_size
                        file_type = cad_file.suffix.upper()[1:]  # Remove dot
                        drawings[category].append({
                            'project': project_name,
                            'filename': cad_file.name,
                            'path': str(cad_file.relative_to(PCB_ROOT)),
                            'type': file_type,
                            'category': category.title(),
                            'size': file_size,
                            'size_str': get_file_size_str(file_size)
                        })
    
    return drawings


def generate_catalog(models: Dict, drawings: Dict) -> None:
    """Generate the master 3D model catalog markdown file."""
    
    # Count totals
    total_stl = sum(len([m for m in cat if m['type'] == 'STL']) for cat in models.values())
    total_step = sum(len([m for m in cat if m['type'] == 'STEP']) for cat in models.values())
    total_dxf = sum(len([d for d in cat if d['type'] == 'DXF']) for cat in drawings.values())
    total_svg = sum(len([d for d in cat if d['type'] == 'SVG']) for cat in drawings.values())
    total_projects = len(set(
        [m['project'] for cat in models.values() for m in cat] +
        [d['project'] for cat in drawings.values() for d in cat]
    ))
    
    with open(CATALOG_FILE, 'w') as f:
        # Header
        f.write("# 3D Model and CAD Drawing Catalog\n\n")
        f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
        # Overview
        f.write("## Overview\n\n")
        f.write("This catalog provides a comprehensive index of all 3D models and CAD drawings ")
        f.write("available in the Through-Hole Keyboard PCB Design Resource Library.\n\n")
        
        # Statistics
        f.write("### Statistics\n\n")
        f.write(f"- **Total Projects:** {total_projects}\n")
        f.write(f"- **STL Files:** {total_stl} (3D printing)\n")
        f.write(f"- **STEP Files:** {total_step} (CAD editing)\n")
        f.write(f"- **DXF Files:** {total_dxf} (laser cutting/CNC)\n")
        f.write(f"- **SVG Files:** {total_svg} (vector graphics)\n\n")
        
        # Table of Contents
        f.write("## Table of Contents\n\n")
        f.write("- [3D Models](#3d-models)\n")
        f.write("  - [Cases](#cases)\n")
        f.write("  - [Plates](#plates)\n")
        f.write("  - [Accessories](#accessories)\n")
        f.write("- [CAD Drawings](#cad-drawings)\n")
        f.write("  - [Plate Drawings](#plate-drawings)\n")
        f.write("  - [Case Drawings](#case-drawings)\n")
        f.write("  - [Cover Drawings](#cover-drawings)\n")
        f.write("- [Usage Guidelines](#usage-guidelines)\n\n")
        
        # 3D Models Section
        f.write("## 3D Models\n\n")
        
        # Cases
        if models['cases']:
            f.write("### Cases\n\n")
            f.write("Keyboard case models for 3D printing or CAD editing.\n\n")
            
            # Group by project
            projects = {}
            for model in models['cases']:
                if model['project'] not in projects:
                    projects[model['project']] = []
                projects[model['project']].append(model)
            
            for project_name in sorted(projects.keys()):
                f.write(f"#### {project_name.title()}\n\n")
                
                project_models = projects[project_name]
                stl_models = [m for m in project_models if m['type'] == 'STL']
                step_models = [m for m in project_models if m['type'] == 'STEP']
                
                if stl_models:
                    f.write("**STL Files (3D Printing):**\n\n")
                    f.write("| File | Size | Est. Print Time | Materials |\n")
                    f.write("|------|------|-----------------|----------|\n")
                    
                    for model in stl_models:
                        materials = ', '.join(get_material_recommendations(model['filename']))
                        print_time = estimate_print_time(model['size'])
                        f.write(f"| `{model['filename']}` | {model['size_str']} | {print_time} | {materials} |\n")
                    
                    f.write("\n")
                    
                    # Print settings
                    if stl_models:
                        sample_model = stl_models[0]
                        settings = get_print_settings(sample_model['filename'], sample_model['size'])
                        f.write("**Recommended Print Settings:**\n\n")
                        f.write(f"- Layer Height: {settings['layer_height']}\n")
                        f.write(f"- Infill: {settings['infill']}\n")
                        f.write(f"- Supports: {settings['supports']}\n")
                        f.write(f"- Orientation: {settings['orientation']}\n\n")
                
                if step_models:
                    f.write("**STEP Files (CAD Editing):**\n\n")
                    f.write("| File | Size | Purpose |\n")
                    f.write("|------|------|--------|\n")
                    
                    for model in step_models:
                        f.write(f"| `{model['filename']}` | {model['size_str']} | Editable CAD model |\n")
                    
                    f.write("\n")
                
                f.write(f"**Location:** `{project_models[0]['path'].rsplit('/', 1)[0]}/`\n\n")
        
        # Plates
        if models['plates']:
            f.write("### Plates\n\n")
            f.write("Switch plate models for 3D printing or CAD editing.\n\n")
            
            # Group by project
            projects = {}
            for model in models['plates']:
                if model['project'] not in projects:
                    projects[model['project']] = []
                projects[model['project']].append(model)
            
            for project_name in sorted(projects.keys()):
                f.write(f"#### {project_name.title()}\n\n")
                
                f.write("| File | Type | Size | Notes |\n")
                f.write("|------|------|------|-------|\n")
                
                for model in projects[project_name]:
                    notes = "3D printable" if model['type'] == 'STL' else "CAD editable"
                    f.write(f"| `{model['filename']}` | {model['type']} | {model['size_str']} | {notes} |\n")
                
                f.write("\n")
                f.write("**Material Recommendations:** PLA (rigid), PETG, Polycarbonate, or Aluminum (CNC)\n\n")
                f.write(f"**Location:** `{projects[project_name][0]['path'].rsplit('/', 1)[0]}/`\n\n")
        
        # Accessories
        if models['accessories']:
            f.write("### Accessories\n\n")
            f.write("Additional components and accessories.\n\n")
            
            # Group by project
            projects = {}
            for model in models['accessories']:
                if model['project'] not in projects:
                    projects[model['project']] = []
                projects[model['project']].append(model)
            
            for project_name in sorted(projects.keys()):
                f.write(f"#### {project_name.title()}\n\n")
                
                f.write("| File | Type | Category | Size |\n")
                f.write("|------|------|----------|------|\n")
                
                for model in projects[project_name]:
                    f.write(f"| `{model['filename']}` | {model['type']} | {model['category']} | {model['size_str']} |\n")
                
                f.write("\n")
                f.write(f"**Location:** `{projects[project_name][0]['path'].rsplit('/', 1)[0]}/`\n\n")
        
        # CAD Drawings Section
        f.write("## CAD Drawings\n\n")
        
        # Plate Drawings
        if drawings['plates']:
            f.write("### Plate Drawings\n\n")
            f.write("2D CAD drawings for laser cutting or CNC machining of switch plates.\n\n")
            
            # Group by project
            projects = {}
            for drawing in drawings['plates']:
                if drawing['project'] not in projects:
                    projects[drawing['project']] = []
                projects[drawing['project']].append(drawing)
            
            for project_name in sorted(projects.keys()):
                f.write(f"#### {project_name.title()}\n\n")
                
                f.write("| File | Type | Size |\n")
                f.write("|------|------|------|\n")
                
                for drawing in projects[project_name]:
                    f.write(f"| `{drawing['filename']}` | {drawing['type']} | {drawing['size_str']} |\n")
                
                f.write("\n")
                
                # Cutting settings
                settings = get_cutting_settings(projects[project_name][0]['filename'])
                f.write("**Recommended Settings:**\n\n")
                f.write(f"- Material: {settings['material']}\n")
                f.write(f"- Thickness: {settings['thickness']}\n")
                f.write(f"- Method: {settings['method']}\n\n")
                
                f.write(f"**Location:** `{projects[project_name][0]['path'].rsplit('/', 1)[0]}/`\n\n")
        
        # Case Drawings
        if drawings['cases']:
            f.write("### Case Drawings\n\n")
            f.write("2D CAD drawings for case components.\n\n")
            
            # Group by project
            projects = {}
            for drawing in drawings['cases']:
                if drawing['project'] not in projects:
                    projects[drawing['project']] = []
                projects[drawing['project']].append(drawing)
            
            for project_name in sorted(projects.keys()):
                f.write(f"#### {project_name.title()}\n\n")
                
                f.write("| File | Type | Size |\n")
                f.write("|------|------|------|\n")
                
                for drawing in projects[project_name]:
                    f.write(f"| `{drawing['filename']}` | {drawing['type']} | {drawing['size_str']} |\n")
                
                f.write("\n")
                f.write(f"**Location:** `{projects[project_name][0]['path'].rsplit('/', 1)[0]}/`\n\n")
        
        # Cover Drawings
        if drawings['covers']:
            f.write("### Cover Drawings\n\n")
            f.write("2D CAD drawings for covers and lids.\n\n")
            
            # Group by project
            projects = {}
            for drawing in drawings['covers']:
                if drawing['project'] not in projects:
                    projects[drawing['project']] = []
                projects[drawing['project']].append(drawing)
            
            for project_name in sorted(projects.keys()):
                f.write(f"#### {project_name.title()}\n\n")
                
                f.write("| File | Type | Size |\n")
                f.write("|------|------|------|\n")
                
                for drawing in projects[project_name]:
                    f.write(f"| `{drawing['filename']}` | {drawing['type']} | {drawing['size_str']} |\n")
                
                f.write("\n")
                f.write(f"**Location:** `{projects[project_name][0]['path'].rsplit('/', 1)[0]}/`\n\n")
        
        # Usage Guidelines
        f.write("## Usage Guidelines\n\n")
        
        f.write("### 3D Printing (STL Files)\n\n")
        f.write("**General Recommendations:**\n\n")
        f.write("- **Slicer Software:** Cura, PrusaSlicer, or Simplify3D\n")
        f.write("- **Layer Height:** 0.2mm standard, 0.1mm for fine details\n")
        f.write("- **Infill:** 20-30% for structural parts, 15% for large prints\n")
        f.write("- **Wall Thickness:** 3-4 perimeters recommended\n")
        f.write("- **Supports:** Enable for overhangs > 45°\n")
        f.write("- **Bed Adhesion:** Brim or raft for large prints\n\n")
        
        f.write("**Material Selection:**\n\n")
        f.write("- **PLA:** Easy to print, rigid, good for most cases\n")
        f.write("- **PETG:** More durable, slightly flexible, better layer adhesion\n")
        f.write("- **ABS:** Strong, heat resistant, requires heated enclosure\n")
        f.write("- **Polycarbonate:** Very strong, excellent for plates\n\n")
        
        f.write("### CAD Editing (STEP Files)\n\n")
        f.write("**Compatible Software:**\n\n")
        f.write("- FreeCAD (free, open-source)\n")
        f.write("- Fusion 360 (free for hobbyists)\n")
        f.write("- SolidWorks (professional)\n")
        f.write("- OnShape (browser-based)\n\n")
        
        f.write("**Editing Tips:**\n\n")
        f.write("- Always keep a backup of the original file\n")
        f.write("- Check dimensions before making modifications\n")
        f.write("- Maintain proper clearances for PCB and components\n")
        f.write("- Export to STL for 3D printing after modifications\n\n")
        
        f.write("### Laser Cutting / CNC (DXF Files)\n\n")
        f.write("**Service Providers:**\n\n")
        f.write("- Ponoko (laser cutting)\n")
        f.write("- SendCutSend (laser and CNC)\n")
        f.write("- Local makerspaces and fab labs\n\n")
        
        f.write("**Material Options:**\n\n")
        f.write("- **Acrylic:** 1.5-3mm for plates, 3-5mm for cases\n")
        f.write("- **FR4 (PCB material):** 1.5mm for plates\n")
        f.write("- **Aluminum:** 1.5mm for plates, requires CNC\n")
        f.write("- **Steel:** 1.5mm for plates, requires CNC\n")
        f.write("- **Wood:** 3-5mm for cases, laser or CNC\n\n")
        
        f.write("## Related Documentation\n\n")
        f.write("- [Repository Inventory](repository_inventory.md) - Project metadata\n")
        f.write("- [Manufacturing Guide](manufacturing_guide.md) - PCB ordering\n")
        f.write("- [Build Guides](build-guides/) - Assembly instructions\n\n")
        
        f.write("## Contributing\n\n")
        f.write("To add new 3D models or CAD drawings:\n\n")
        f.write("1. Organize files using `scripts/organize_3d_models.sh <project-name>`\n")
        f.write("2. Regenerate catalog using `scripts/generate_3d_catalog.py`\n")
        f.write("3. Verify files are properly categorized\n")
        f.write("4. Update project documentation as needed\n\n")
        
        f.write("---\n\n")
        f.write("*This catalog is automatically generated. Do not edit manually.*\n")


def main():
    """Main execution function."""
    print("Scanning 3D models...")
    models = scan_3d_models()
    
    print("Scanning CAD drawings...")
    drawings = scan_cad_drawings()
    
    print("Generating catalog...")
    generate_catalog(models, drawings)
    
    print(f"✓ Catalog generated: {CATALOG_FILE}")
    
    # Print summary
    total_files = (
        sum(len(cat) for cat in models.values()) +
        sum(len(cat) for cat in drawings.values())
    )
    print(f"\nSummary:")
    print(f"  Total files cataloged: {total_files}")
    print(f"  Cases: {len(models['cases'])}")
    print(f"  Plates: {len(models['plates'])}")
    print(f"  Accessories: {len(models['accessories'])}")
    print(f"  CAD drawings: {sum(len(cat) for cat in drawings.values())}")


if __name__ == "__main__":
    main()
