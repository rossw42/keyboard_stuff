#!/usr/bin/env python3
"""
Generate comprehensive project catalog with metadata, tags, and categories.

This script creates a searchable project catalog from the repository inventory
and other metadata sources, including firmware support, licenses, and features.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional


class ProjectCatalog:
    """Generate comprehensive project catalog with metadata."""
    
    def __init__(self, base_dir: str = "PCB"):
        self.base_dir = Path(base_dir)
        self.projects = []
        self.categories = {
            "form_factor": set(),
            "mcu": set(),
            "usb": set(),
            "features": set(),
            "firmware": set(),
            "license": set()
        }
        
    def parse_repository_inventory(self) -> List[Dict]:
        """Parse repository_inventory.md to extract project metadata."""
        inventory_path = self.base_dir / "docs" / "repository_inventory.md"
        
        if not inventory_path.exists():
            print(f"Warning: {inventory_path} not found")
            return []
        
        with open(inventory_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        projects = []
        # Split by project sections (## Project Name)
        sections = re.split(r'\n## ([^\n]+)\n', content)
        
        for i in range(1, len(sections), 2):
            if i + 1 >= len(sections):
                break
                
            project_name = sections[i].strip()
            project_content = sections[i + 1]
            
            project = self._parse_project_section(project_name, project_content)
            if project:
                projects.append(project)
        
        return projects
    
    def _parse_project_section(self, name: str, content: str) -> Optional[Dict]:
        """Parse individual project section."""
        project = {
            "name": name,
            "repository": "",
            "layout": "",
            "form_factor": "",
            "key_count": 0,
            "mcu": "",
            "usb": "",
            "files": {
                "gerber": False,
                "design": False,
                "bom": False,
                "build_guide": False,
                "3d_models": False,
                "cad_drawings": False
            },
            "firmware": {
                "qmk": False,
                "via": False,
                "vial": False,
                "zmk": False
            },
            "license": "",
            "features": [],
            "tags": [],
            "revision": "",
            "description": ""
        }
        
        # Extract repository URL
        repo_match = re.search(r'\*\*Repository:\*\*\s*(.+)', content)
        if repo_match:
            project["repository"] = repo_match.group(1).strip()
        
        # Extract layout
        layout_match = re.search(r'\*\*Layout:\*\*\s*(.+)', content)
        if layout_match:
            layout = layout_match.group(1).strip()
            project["layout"] = layout
            project["form_factor"] = self._extract_form_factor(layout)
            project["key_count"] = self._extract_key_count(layout)
        
        # Extract MCU
        mcu_match = re.search(r'\*\*MCU:\*\*\s*(.+)', content)
        if mcu_match:
            project["mcu"] = mcu_match.group(1).strip()
        
        # Extract USB
        usb_match = re.search(r'\*\*USB:\*\*\s*(.+)', content)
        if usb_match:
            project["usb"] = usb_match.group(1).strip()
        
        # Extract available files
        if '✅ Gerber files' in content:
            project["files"]["gerber"] = True
        if '✅ KiCad/Eagle files' in content or '✅ KiCad files' in content or '✅ Eagle files' in content:
            project["files"]["design"] = True
        if '✅ BOM' in content:
            project["files"]["bom"] = True
        if '✅ Build guide' in content:
            project["files"]["build_guide"] = True
        if '✅ 3D models' in content:
            project["files"]["3d_models"] = True
        if '✅ DXF drawings' in content or '✅ DXF files' in content:
            project["files"]["cad_drawings"] = True
        
        # Extract firmware support
        qmk_match = re.search(r'\*\*QMK Support:\*\*\s*(.+)', content)
        if qmk_match and 'Yes' in qmk_match.group(1):
            project["firmware"]["qmk"] = True
        
        via_match = re.search(r'\*\*VIA.*Support:\*\*\s*(.+)', content)
        if via_match and 'Yes' in via_match.group(1):
            project["firmware"]["via"] = True
        
        vial_match = re.search(r'\*\*VIAL.*Support:\*\*\s*(.+)', content)
        if vial_match and 'Yes' in vial_match.group(1):
            project["firmware"]["vial"] = Trueoject["firmware"]["vial"] = True
        
        # Check for ZMK in content
        if 'ZMK' in content:
            project["firmware"]["zmk"] = True
        
        # Extract license
        license_match = re.search(r'\*\*License:\*\*\s*(.+)', content)
        if license_match:
            project["license"] = license_match.group(1).strip()
        
        # Extract special features
        features_match = re.search(r'\*\*Special Features:\*\*\s*(.+)', content)
        if features_match:
            features_text = features_match.group(1).strip()
            if features_text and features_text != "None documented":
                project["features"] = [f.strip() for f in features_text.split(',')]
        
        # Extract revision
        revision_match = re.search(r'\*\*Revision.*:\*\*\s*(.+)', content)
        if revision_match:
            project["revision"] = revision_match.group(1).strip()
        
        # Generate tags
        project["tags"] = self._generate_tags(project)
        
        # Generate description
        project["description"] = self._generate_description(project)
        
        return project
    
    def _extract_form_factor(self, layout: str) -> str:
        """Extract form factor from layout string."""
        layout_lower = layout.lower()
        
        if 'macropad' in layout_lower or 'numpad' in layout_lower:
            return "Macropad"
        elif '40%' in layout or '40 ' in layout:
            return "40%"
        elif '60%' in layout or '60 ' in layout:
            return "60%"
        elif '65%' in layout or '65 ' in layout:
            return "65%"
        elif '75%' in layout or '75 ' in layout:
            return "75%"
        elif 'tkl' in layout_lower or 'tenkeyless' in layout_lower:
            return "TKL"
        elif 'ortholinear' in layout_lower or 'ortho' in layout_lower:
            return "Ortholinear"
        else:
            return "Other"
    
    def _extract_key_count(self, layout: str) -> int:
        """Extract key count from layout string."""
        # Look for patterns like "68 keys", "(61 keys)", "4x4"
        key_match = re.search(r'(\d+)\s*keys?', layout, re.IGNORECASE)
        if key_match:
            return int(key_match.group(1))
        
        # Look for grid patterns like "4x4", "5x12"
        grid_match = re.search(r'(\d+)\s*[x×]\s*(\d+)', layout)
        if grid_match:
            return int(grid_match.group(1)) * int(grid_match.group(2))
        
        return 0
    
    def _generate_tags(self, project: Dict) -> List[str]:
        """Generate searchable tags for project."""
        tags = []
        
        # Form factor tags
        if project["form_factor"]:
            tags.append(project["form_factor"].lower())
        
        # Layout tags
        if 'ortholinear' in project["layout"].lower():
            tags.append("ortholinear")
        if 'split' in project["layout"].lower():
            tags.append("split")
        if 'staggered' in project["layout"].lower():
            tags.append("staggered")
        
        # MCU tags
        if project["mcu"]:
            mcu_lower = project["mcu"].lower()
            if 'atmega328' in mcu_lower:
                tags.append("atmega328p")
                tags.append("dip-mcu")
            elif 'atmega32' in mcu_lower:
                tags.append("atmega32a")
                tags.append("dip-mcu")
            elif 'pro micro' in mcu_lower:
                tags.append("pro-micro")
            elif 'atmega32u4' in mcu_lower:
                tags.append("atmega32u4")
        
        # USB tags
        if project["usb"]:
            usb_lower = project["usb"].lower()
            if 'usb-c' in usb_lower or 'usbc' in usb_lower:
                tags.append("usb-c")
            if 'mini' in usb_lower:
                tags.append("usb-mini")
            if 'micro' in usb_lower:
                tags.append("usb-micro")
        
        # Feature tags
        for feature in project["features"]:
            feature_lower = feature.lower()
            if 'rotary' in feature_lower or 'encoder' in feature_lower:
                tags.append("rotary-encoder")
            if 'oled' in feature_lower:
                tags.append("oled")
            if 'rgb' in feature_lower or 'led' in feature_lower:
                tags.append("rgb-led")
            if 'wireless' in feature_lower:
                tags.append("wireless")
            if 'hot' in feature_lower and 'swap' in feature_lower:
                tags.append("hotswap")
        
        # Firmware tags
        if project["firmware"]["qmk"]:
            tags.append("qmk")
        if project["firmware"]["via"]:
            tags.append("via")
        if project["firmware"]["vial"]:
            tags.append("vial")
        if project["firmware"]["zmk"]:
            tags.append("zmk")
        
        # Through-hole tag (all projects)
        tags.append("through-hole")
        tags.append("tht")
        
        # Open source tag
        tags.append("open-source")
        
        return sorted(list(set(tags)))
    
    def _generate_description(self, project: Dict) -> str:
        """Generate human-readable description."""
        parts = []
        
        if project["form_factor"] and project["key_count"]:
            parts.append(f"{project['form_factor']} keyboard with {project['key_count']} keys")
        elif project["form_factor"]:
            parts.append(f"{project['form_factor']} keyboard")
        elif project["layout"]:
            parts.append(project["layout"])
        
        if project["mcu"]:
            parts.append(f"using {project['mcu']} MCU")
        
        if project["features"]:
            feature_str = ", ".join(project["features"][:3])
            parts.append(f"featuring {feature_str}")
        
        return ". ".join(parts) + "." if parts else "Through-hole keyboard PCB design."
    
    def collect_categories(self):
        """Collect all unique categories from projects."""
        for project in self.projects:
            if project["form_factor"]:
                self.categories["form_factor"].add(project["form_factor"])
            if project["mcu"]:
                self.categories["mcu"].add(project["mcu"])
            if project["usb"]:
                self.categories["usb"].add(project["usb"])
            if project["license"]:
                self.categories["license"].add(project["license"])
            
            for feature in project["features"]:
                self.categories["features"].add(feature)
            
            for fw_type, supported in project["firmware"].items():
                if supported:
                    self.categories["firmware"].add(fw_type.upper())
    
    def generate_catalog_markdown(self) -> str:
        """Generate markdown catalog document."""
        lines = []
        lines.append("# Through-Hole Keyboard Project Catalog")
        lines.append("")
        lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        lines.append("")
        
        # Overview
        lines.append("## Overview")
        lines.append("")
        lines.append("Comprehensive catalog of through-hole keyboard PCB designs with searchable metadata, ")
        lines.append("firmware support information, and file availability.")
        lines.append("")
        
        # Statistics
        lines.append("### Statistics")
        lines.append("")
        lines.append(f"- **Total Projects:** {len(self.projects)}")
        lines.append(f"- **Form Factors:** {len(self.categories['form_factor'])}")
        lines.append(f"- **MCU Types:** {len(self.categories['mcu'])}")
        lines.append(f"- **Firmware Options:** {len(self.categories['firmware'])}")
        lines.append("")
        
        # Table of Contents
        lines.append("## Table of Contents")
        lines.append("")
        lines.append("- [Quick Reference](#quick-reference)")
        lines.append("- [Projects by Category](#projects-by-category)")
        lines.append("- [All Projects (Alphabetical)](#all-projects-alphabetical)")
        lines.append("- [Search by Tags](#search-by-tags)")
        lines.append("- [Firmware Support Matrix](#firmware-support-matrix)")
        lines.append("- [License Information](#license-information)")
        lines.append("")
        
        # Quick Reference Table
        lines.append("## Quick Reference")
        lines.append("")
        lines.append("| Project | Form Factor | Keys | MCU | USB | QMK | VIA | Files |")
        lines.append("|---------|-------------|------|-----|-----|-----|-----|-------|")
        
        for project in sorted(self.projects, key=lambda p: p["name"]):
            files_available = sum(1 for v in project["files"].values() if v)
            qmk = "✅" if project["firmware"]["qmk"] else "❌"
            via = "✅" if project["firmware"]["via"] else "❌"
            
            lines.append(f"| [{project['name']}](#{project['name'].lower().replace(' ', '-')}) | "
                        f"{project['form_factor']} | {project['key_count'] or 'N/A'} | "
                        f"{project['mcu'] or 'N/A'} | {project['usb'] or 'N/A'} | "
                        f"{qmk} | {via} | {files_available}/6 |")
        
        lines.append("")
        
        # Projects by Category
        lines.append("## Projects by Category")
        lines.append("")
        
        # Group by form factor
        by_form_factor = {}
        for project in self.projects:
            ff = project["form_factor"] or "Other"
            if ff not in by_form_factor:
                by_form_factor[ff] = []
            by_form_factor[ff].append(project)
        
        for form_factor in sorted(by_form_factor.keys()):
            lines.append(f"### {form_factor}")
            lines.append("")
            
            for project in sorted(by_form_factor[form_factor], key=lambda p: p["name"]):
                lines.append(f"- **[{project['name']}](#{project['name'].lower().replace(' ', '-')})** - "
                           f"{project['description']}")
            
            lines.append("")
        
        # All Projects (Detailed)
        lines.append("## All Projects (Alphabetical)")
        lines.append("")
        
        for project in sorted(self.projects, key=lambda p: p["name"]):
            lines.extend(self._format_project_detail(project))
        
        # Search by Tags
        lines.append("## Search by Tags")
        lines.append("")
        lines.append("Find projects by common tags:")
        lines.append("")
        
        # Collect all tags
        all_tags = set()
        for project in self.projects:
            all_tags.update(project["tags"])
        
        for tag in sorted(all_tags):
            matching_projects = [p for p in self.projects if tag in p["tags"]]
            project_names = ", ".join(sorted([p["name"] for p in matching_projects]))
            lines.append(f"- **{tag}** ({len(matching_projects)}): {project_names}")
        
        lines.append("")
        
        # Firmware Support Matrix
        lines.append("## Firmware Support Matrix")
        lines.append("")
        lines.append("| Project | QMK | VIA | VIAL | ZMK |")
        lines.append("|---------|-----|-----|------|-----|")
        
        for project in sorted(self.projects, key=lambda p: p["name"]):
            qmk = "✅" if project["firmware"]["qmk"] else "❌"
            via = "✅" if project["firmware"]["via"] else "❌"
            vial = "✅" if project["firmware"]["vial"] else "❌"
            zmk = "✅" if project["firmware"]["zmk"] else "❌"
            
            lines.append(f"| {project['name']} | {qmk} | {via} | {vial} | {zmk} |")
        
        lines.append("")
        
        # License Information
        lines.append("## License Information")
        lines.append("")
        lines.append("All projects are open-source. Please respect the original licenses:")
        lines.append("")
        
        by_license = {}
        for project in self.projects:
            lic = project["license"] or "Unknown"
            if lic not in by_license:
                by_license[lic] = []
            by_license[lic].append(project["name"])
        
        for license_type in sorted(by_license.keys()):
            projects_list = ", ".join(sorted(by_license[license_type]))
            lines.append(f"- **{license_type}**: {projects_list}")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("*For detailed project information, see [Repository Inventory](repository_inventory.md)*")
        lines.append("")
        
        return "\n".join(lines)
    
    def _format_project_detail(self, project: Dict) -> List[str]:
        """Format detailed project information."""
        lines = []
        
        lines.append(f"### {project['name']}")
        lines.append("")
        
        if project["description"]:
            lines.append(f"**Description:** {project['description']}")
            lines.append("")
        
        # Basic Info
        lines.append("**Specifications:**")
        lines.append("")
        lines.append(f"- **Repository:** {project['repository']}")
        lines.append(f"- **Layout:** {project['layout']}")
        lines.append(f"- **Form Factor:** {project['form_factor']}")
        if project["key_count"]:
            lines.append(f"- **Key Count:** {project['key_count']}")
        lines.append(f"- **MCU:** {project['mcu']}")
        lines.append(f"- **USB Connector:** {project['usb']}")
        if project["license"]:
            lines.append(f"- **License:** {project['license']}")
        if project["revision"]:
            lines.append(f"- **Latest Revision:** {project['revision']}")
        lines.append("")
        
        # Available Files
        lines.append("**Available Files:**")
        lines.append("")
        for file_type, available in project["files"].items():
            status = "✅" if available else "❌"
            lines.append(f"- {status} {file_type.replace('_', ' ').title()}")
        lines.append("")
        
        # Firmware Support
        lines.append("**Firmware Support:**")
        lines.append("")
        for fw_type, supported in project["firmware"].items():
            status = "✅" if supported else "❌"
            lines.append(f"- {status} {fw_type.upper()}")
        lines.append("")
        
        # Features
        if project["features"]:
            lines.append("**Special Features:**")
            lines.append("")
            for feature in project["features"]:
                lines.append(f"- {feature}")
            lines.append("")
        
        # Tags
        if project["tags"]:
            tags_str = ", ".join([f"`{tag}`" for tag in project["tags"]])
            lines.append(f"**Tags:** {tags_str}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        
        return lines
    
    def generate_json_catalog(self) -> str:
        """Generate JSON catalog for programmatic access."""
        catalog = {
            "generated": datetime.now().isoformat(),
            "version": "1.0.0",
            "statistics": {
                "total_projects": len(self.projects),
                "form_factors": len(self.categories["form_factor"]),
                "mcu_types": len(self.categories["mcu"]),
                "firmware_options": len(self.categories["firmware"])
            },
            "categories": {
                "form_factor": sorted(list(self.categories["form_factor"])),
                "mcu": sorted(list(self.categories["mcu"])),
                "usb": sorted(list(self.categories["usb"])),
                "features": sorted(list(self.categories["features"])),
                "firmware": sorted(list(self.categories["firmware"])),
                "license": sorted(list(self.categories["license"]))
            },
            "projects": self.projects
        }
        
        return json.dumps(catalog, indent=2, ensure_ascii=False)
    
    def run(self):
        """Main execution."""
        print("Generating project catalog...")
        
        # Parse repository inventory
        self.projects = self.parse_repository_inventory()
        print(f"Found {len(self.projects)} projects")
        
        # Collect categories
        self.collect_categories()
        
        # Generate markdown catalog
        catalog_md = self.generate_catalog_markdown()
        output_path = self.base_dir / "docs" / "project_catalog.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(catalog_md)
        print(f"Generated: {output_path}")
        
        # Generate JSON catalog
        catalog_json = self.generate_json_catalog()
        json_path = self.base_dir / "docs" / "project_catalog.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(catalog_json)
        print(f"Generated: {json_path}")
        
        print("\nCatalog generation complete!")
        print(f"  - {len(self.projects)} projects cataloged")
        print(f"  - {len(self.categories['form_factor'])} form factors")
        print(f"  - {len(self.categories['mcu'])} MCU types")
        print(f"  - {len(self.categories['firmware'])} firmware options")


if __name__ == "__main__":
    catalog = ProjectCatalog()
    catalog.run()
