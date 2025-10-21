#!/usr/bin/env python3
"""
BOM Consolidation and Deduplication Engine
Generates master BOM from multiple project BOMs
"""

import csv
import sys
from pathlib import Path
from typing import List, Dict, Set
from collections import defaultdict
from dataclasses import dataclass, field

# Import our parser and normalizer
from parse_bom import BOMParser, BOMComponent
from normalize_components import ComponentNormalizer


@dataclass
class MasterComponent:
    """Represents a deduplicated component in the master BOM"""
    category: str
    component: str
    value: str
    footprint: str
    package: str
    vendor_part: str = ""
    min_qty: int = 0
    max_qty: int = 0
    projects: Set[str] = field(default_factory=set)
    notes: str = ""
    
    def add_project(self, project: str, quantity: int):
        """Add a project that uses this component"""
        self.projects.add(project)
        if self.min_qty == 0 or quantity < self.min_qty:
            self.min_qty = quantity
        if quantity > self.max_qty:
            self.max_qty = quantity
    
    def get_key(self) -> str:
        """Get unique key for component matching"""
        return f"{self.category}|{self.component}|{self.value}|{self.footprint}"
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for CSV export"""
        return {
            'Component': self.component,
            'Value': self.value,
            'Footprint': self.footprint,
            'Package': self.package,
            'Vendor_Part_No': self.vendor_part,
            'Category': self.category,
            'Min_Qty': str(self.min_qty),
            'Max_Qty': str(self.max_qty),
            'Projects_Using': '; '.join(sorted(self.projects)),
            'Notes': self.notes
        }


class BOMConsolidator:
    """Consolidates multiple project BOMs into a master BOM"""
    
    def __init__(self, bom_dir: Path, config_path: Path = None):
        self.bom_dir = Path(bom_dir)
        self.normalizer = ComponentNormalizer(config_path)
        self.master_components: Dict[str, MasterComponent] = {}
        self.category_indexes: Dict[str, List[MasterComponent]] = defaultdict(list)
    
    def process_all_projects(self):
        """Process all project BOMs in the directory"""
        if not self.bom_dir.exists():
            print(f"Error: BOM directory not found: {self.bom_dir}", file=sys.stderr)
            return
        
        # Find all project directories
        project_dirs = [d for d in self.bom_dir.iterdir() if d.is_dir()]
        
        if not project_dirs:
            print(f"Warning: No project directories found in {self.bom_dir}", file=sys.stderr)
            return
        
        print(f"Processing {len(project_dirs)} projects...")
        
        for project_dir in project_dirs:
            project_name = project_dir.name
            self._process_project(project_name, project_dir)
        
        print(f"\nProcessed {len(project_dirs)} projects")
        print(f"Found {len(self.master_components)} unique components")
    
    def _process_project(self, project_name: str, project_dir: Path):
        """Process a single project's BOM"""
        # Look for BOM files in the project directory
        bom_files = list(project_dir.glob('*.csv'))
        bom_files.extend(project_dir.glob('*.md'))
        bom_files.extend(project_dir.glob('*.txt'))
        bom_files.extend(project_dir.glob('bom.*'))
        
        if not bom_files:
            print(f"  Warning: No BOM file found for {project_name}", file=sys.stderr)
            return
        
        # Use the first BOM file found
        bom_file = bom_files[0]
        print(f"  Processing {project_name}: {bom_file.name}")
        
        try:
            parser = BOMParser(bom_file)
            components = parser.parse()
            
            for comp in components:
                self._add_component(project_name, comp)
            
            print(f"    Added {len(components)} components")
        
        except Exception as e:
            print(f"  Error processing {project_name}: {e}", file=sys.stderr)
    
    def _add_component(self, project_name: str, component: BOMComponent):
        """Add a component to the master BOM with deduplication"""
        # Normalize the component
        normalized = self.normalizer.normalize(
            component.component,
            component.value,
            component.footprint
        )
        
        # Create or update master component
        key = f"{normalized.category}|{normalized.component}|{normalized.value}|{normalized.footprint}"
        
        if key in self.master_components:
            # Update existing component
            master = self.master_components[key]
            master.add_project(project_name, component.quantity)
            
            # Update vendor part if not set
            if not master.vendor_part and component.vendor_part:
                master.vendor_part = component.vendor_part
            
            # Append notes if different
            if component.notes and component.notes not in master.notes:
                if master.notes:
                    master.notes += f"; {component.notes}"
                else:
                    master.notes = component.notes
        else:
            # Create new master component
            master = MasterComponent(
                category=normalized.category,
                component=normalized.component,
                value=normalized.value,
                footprint=normalized.footprint,
                package=normalized.package,
                vendor_part=component.vendor_part,
                notes=component.notes
            )
            master.add_project(project_name, component.quantity)
            
            self.master_components[key] = master
            self.category_indexes[normalized.category].append(master)
    
    def generate_master_bom(self, output_path: Path):
        """Generate master BOM CSV file"""
        if not self.master_components:
            print("Error: No components to export", file=sys.stderr)
            return
        
        # Sort components by category, then by component name
        sorted_components = sorted(
            self.master_components.values(),
            key=lambda c: (c.category, c.component, c.value)
        )
        
        # Write CSV
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'Component', 'Value', 'Footprint', 'Package',
                'Vendor_Part_No', 'Category', 'Min_Qty', 'Max_Qty',
                'Projects_Using', 'Notes'
            ]
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for comp in sorted_components:
                writer.writerow(comp.to_dict())
        
        print(f"\nGenerated master BOM: {output_path}")
        print(f"  Total components: {len(sorted_components)}")
    
    def generate_category_indexes(self, output_dir: Path):
        """Generate category-specific BOM indexes"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for category, components in self.category_indexes.items():
            if not components:
                continue
            
            # Sort by component name and value
            sorted_comps = sorted(components, key=lambda c: (c.component, c.value))
            
            # Generate category file
            category_file = output_dir / f"{category.lower().replace(' ', '_')}.csv"
            
            with open(category_file, 'w', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'Component', 'Value', 'Footprint', 'Package',
                    'Vendor_Part_No', 'Min_Qty', 'Max_Qty',
                    'Projects_Using', 'Notes'
                ]
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for comp in sorted_comps:
                    row = comp.to_dict()
                    del row['Category']  # Remove category from individual files
                    writer.writerow(row)
            
            print(f"  Generated {category} index: {category_file.name} ({len(sorted_comps)} components)")
    
    def generate_summary_report(self, output_path: Path):
        """Generate a summary report in Markdown"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Master BOM Summary\n\n")
            
            # Overall statistics
            f.write("## Statistics\n\n")
            f.write(f"- **Total Unique Components:** {len(self.master_components)}\n")
            
            # Count projects
            all_projects = set()
            for comp in self.master_components.values():
                all_projects.update(comp.projects)
            f.write(f"- **Total Projects:** {len(all_projects)}\n")
            
            # Category breakdown
            f.write(f"- **Categories:** {len(self.category_indexes)}\n\n")
            
            # Category details
            f.write("## Components by Category\n\n")
            
            for category in sorted(self.category_indexes.keys()):
                components = self.category_indexes[category]
                f.write(f"### {category} ({len(components)} components)\n\n")
                
                # Top 5 most common components in this category
                sorted_by_projects = sorted(
                    components,
                    key=lambda c: len(c.projects),
                    reverse=True
                )[:5]
                
                if sorted_by_projects:
                    f.write("**Most Common:**\n\n")
                    for comp in sorted_by_projects:
                        f.write(f"- {comp.component} {comp.value} ")
                        f.write(f"({len(comp.projects)} projects: {', '.join(sorted(comp.projects))})\n")
                    f.write("\n")
            
            # Project list
            f.write("## Projects Processed\n\n")
            for project in sorted(all_projects):
                f.write(f"- {project}\n")
        
        print(f"\nGenerated summary report: {output_path}")


def main():
    """Command-line interface for BOM consolidator"""
    if len(sys.argv) < 2:
        print("Usage: consolidate_bom.py <bom-directory> [config-file]")
        print("\nConsolidates all project BOMs in the directory into a master BOM")
        print("\nExample:")
        print("  consolidate_bom.py PCB/boms")
        print("  consolidate_bom.py PCB/boms PCB/scripts/normalization_config.json")
        sys.exit(1)
    
    bom_dir = Path(sys.argv[1])
    config_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    
    if not bom_dir.exists():
        print(f"Error: Directory not found: {bom_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Create consolidator
    consolidator = BOMConsolidator(bom_dir, config_path)
    
    # Process all projects
    consolidator.process_all_projects()
    
    if not consolidator.master_components:
        print("\nNo components found to consolidate", file=sys.stderr)
        sys.exit(1)
    
    # Generate outputs
    master_bom_path = bom_dir / "master-bom.csv"
    consolidator.generate_master_bom(master_bom_path)
    
    # Generate category indexes
    category_dir = bom_dir / "by-category"
    print(f"\nGenerating category indexes...")
    consolidator.generate_category_indexes(category_dir)
    
    # Generate summary report
    summary_path = bom_dir / "master-bom-summary.md"
    consolidator.generate_summary_report(summary_path)
    
    print("\n✓ BOM consolidation complete!")


if __name__ == '__main__':
    main()
