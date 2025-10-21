#!/usr/bin/env python3
"""
Validation script for Through-Hole Keyboard PCB Library
Checks file organization, completeness, and consistency
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Expected projects
PROJECTS = [
    'discipline', 'mysterium', 'lumberjack', 'rosaline', 'litl',
    'kbic65', 'plaid', 'tartan', 'gh60', 'plaid-pad', 'dumbpad'
]

# Expected directory structure
EXPECTED_DIRS = [
    'design-files',
    'gerbers',
    'boms',
    '3d-models',
    'cad-drawings',
    'firmware',
    'docs',
    'scripts'
]

class LibraryValidator:
    def __init__(self, library_root: Path):
        self.root = library_root
        self.errors = []
        self.warnings = []
        self.info = []
        
    def log_error(self, msg: str):
        self.errors.append(msg)
        print(f"{RED}✗ ERROR:{RESET} {msg}")
    
    def log_warning(self, msg: str):
        self.warnings.append(msg)
        print(f"{YELLOW}⚠ WARNING:{RESET} {msg}")
    
    def log_info(self, msg: str):
        self.info.append(msg)
        print(f"{BLUE}ℹ INFO:{RESET} {msg}")
    
    def log_success(self, msg: str):
        print(f"{GREEN}✓{RESET} {msg}")
    
    def validate_directory_structure(self) -> bool:
        """Check if main directories exist"""
        print(f"\n{BLUE}=== Validating Directory Structure ==={RESET}")
        
        all_exist = True
        for dir_name in EXPECTED_DIRS:
            dir_path = self.root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                self.log_success(f"Directory exists: {dir_name}/")
            else:
                self.log_error(f"Missing directory: {dir_name}/")
                all_exist = False
        
        return all_exist
    
    def validate_project_files(self) -> Dict[str, Dict[str, bool]]:
        """Check if each project has expected files"""
        print(f"\n{BLUE}=== Validating Project Files ==={RESET}")
        
        results = {}
        
        for project in PROJECTS:
            print(f"\n{BLUE}Checking project: {project}{RESET}")
            results[project] = {
                'design_files': False,
                'gerbers': False,
                'bom': False,
                'build_guide': False,
                '3d_models': False,
                'cad_drawings': False
            }
            
            # Check design files
            design_path = self.root / 'design-files' / project
            if design_path.exists():
                results[project]['design_files'] = True
                self.log_success(f"  Design files found")
            else:
                self.log_warning(f"  No design files")
            
            # Check gerbers
            gerber_path = self.root / 'gerbers' / project
            if gerber_path.exists():
                results[project]['gerbers'] = True
                self.log_success(f"  Gerber files found")
            else:
                self.log_warning(f"  No gerber files")
            
            # Check BOM
            bom_path = self.root / 'boms' / project
            if bom_path.exists() and any(bom_path.iterdir()):
                results[project]['bom'] = True
                self.log_success(f"  BOM found")
            else:
                self.log_warning(f"  No BOM")
            
            # Check build guide
            guide_path = self.root / 'docs' / 'build-guides' / project
            if guide_path.exists():
                results[project]['build_guide'] = True
                self.log_success(f"  Build guide found")
            else:
                self.log_warning(f"  No build guide")
            
            # Check 3D models
            model_paths = [
                self.root / '3d-models' / 'cases' / project,
                self.root / '3d-models' / 'plates' / project,
                self.root / '3d-models' / 'accessories' / project
            ]
            if any(p.exists() for p in model_paths):
                results[project]['3d_models'] = True
                self.log_success(f"  3D models found")
            else:
                self.log_info(f"  No 3D models (optional)")
            
            # Check CAD drawings
            cad_path = self.root / 'cad-drawings' / project
            if cad_path.exists():
                results[project]['cad_drawings'] = True
                self.log_success(f"  CAD drawings found")
            else:
                self.log_info(f"  No CAD drawings (optional)")
        
        return results
    
    def validate_documentation(self) -> bool:
        """Check if key documentation files exist"""
        print(f"\n{BLUE}=== Validating Documentation ==={RESET}")
        
        required_docs = [
            'README.md',
            'PROJECT_CATALOG.md',
            'FILE_INDEX.md',
            'CONTRIBUTING.md',
            'docs/repository_inventory.md',
            'docs/gh60_pcb_specifications.md',
            'boms/master-bom.csv',
            'boms/master-bom-summary.md'
        ]
        
        all_exist = True
        for doc in required_docs:
            doc_path = self.root / doc
            if doc_path.exists():
                self.log_success(f"Documentation exists: {doc}")
            else:
                self.log_error(f"Missing documentation: {doc}")
                all_exist = False
        
        return all_exist
    
    def validate_master_bom(self) -> bool:
        """Check master BOM file"""
        print(f"\n{BLUE}=== Validating Master BOM ==={RESET}")
        
        bom_path = self.root / 'boms' / 'master-bom.csv'
        if not bom_path.exists():
            self.log_error("Master BOM file not found")
            return False
        
        try:
            with open(bom_path, 'r') as f:
                lines = f.readlines()
            
            if len(lines) < 10:
                self.log_warning(f"Master BOM has only {len(lines)} lines (seems incomplete)")
            else:
                self.log_success(f"Master BOM has {len(lines)} lines")
            
            # Check for header
            if lines and 'Component' in lines[0]:
                self.log_success("Master BOM has proper header")
            else:
                self.log_warning("Master BOM header may be incorrect")
            
            return True
            
        except Exception as e:
            self.log_error(f"Error reading master BOM: {e}")
            return False
    
    def generate_report(self) -> Tuple[int, int, int]:
        """Generate summary report"""
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}=== Validation Summary ==={RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")
        
        print(f"{GREEN}Successes:{RESET} {len([m for m in self.info if 'found' in m.lower()])}")
        print(f"{YELLOW}Warnings:{RESET} {len(self.warnings)}")
        print(f"{RED}Errors:{RESET} {len(self.errors)}")
        
        if self.errors:
            print(f"\n{RED}Critical Issues:{RESET}")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n{YELLOW}Warnings:{RESET}")
            for warning in self.warnings[:10]:  # Show first 10
                print(f"  • {warning}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more")
        
        return len(self.errors), len(self.warnings), len(self.info)

def main():
    # Find library root
    script_dir = Path(__file__).parent
    library_root = script_dir.parent
    
    print(f"{BLUE}Through-Hole Keyboard Library Validator{RESET}")
    print(f"Library root: {library_root}\n")
    
    validator = LibraryValidator(library_root)
    
    # Run validations
    validator.validate_directory_structure()
    project_results = validator.validate_project_files()
    validator.validate_documentation()
    validator.validate_master_bom()
    
    # Generate report
    errors, warnings, info = validator.generate_report()
    
    # Exit code
    if errors > 0:
        print(f"\n{RED}Validation FAILED with {errors} errors{RESET}")
        sys.exit(1)
    elif warnings > 0:
        print(f"\n{YELLOW}Validation PASSED with {warnings} warnings{RESET}")
        sys.exit(0)
    else:
        print(f"\n{GREEN}Validation PASSED - Library is in excellent condition!{RESET}")
        sys.exit(0)

if __name__ == '__main__':
    main()
