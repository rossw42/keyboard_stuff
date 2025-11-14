#!/usr/bin/env python3
"""
Unified Keyboard Case Workflow
Handles the complete workflow from KiCad PCB to 3D-printable case files.

Usage:
  # Single keyboard
  python keyboard_case_workflow.py single keyboard.step --kicad-pcb keyboard.kicad_pcb
  
  # Split keyboard (generate PCB halves + cases)
  python keyboard_case_workflow.py split keyboard.step --kicad-pcb keyboard.kicad_pcb
  
  # Just generate PCB STL from existing STEP
  python keyboard_case_workflow.py pcb-stl keyboard.step
"""

import argparse
import sys
from pathlib import Path
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def run_command(cmd, description):
    """Run a command and handle errors."""
    logger.info(f"\n{'='*60}")
    logger.info(f"{description}")
    logger.info(f"{'='*60}")
    logger.info(f"Running: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        logger.error(f"❌ Failed: {description}")
        return False
    logger.info(f"✅ Success: {description}")
    return True


def get_script_path(script_name):
    """Get the full path to a script in the scripts directory."""
    # Get the directory where this workflow script is located
    script_dir = Path(__file__).parent
    return str(script_dir / script_name)


def workflow_single(args):
    """Workflow for single (non-split) keyboard."""
    logger.info("\n🎹 SINGLE KEYBOARD WORKFLOW")
    logger.info("="*60)
    
    pcb_step = Path(args.pcb_step)
    output_dir = Path(args.output) if args.output else pcb_step.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Generate PCB STL (for reference/visualization)
    if args.generate_pcb_stl:
        logger.info("\n📦 Step 1: Generate PCB STL for visualization")
        pcb_stl = output_dir / f"{pcb_step.stem}.stl"
        cmd = ["python", get_script_path("convert_step_to_stl.py"), str(pcb_step), str(pcb_stl)]
        if not run_command(cmd, "Generate PCB STL"):
            return False
    
    # Step 2: Generate case
    logger.info("\n🏗️  Step 2: Generate keyboard case")
    cmd = ["python", get_script_path("generate_case_unified.py"), str(pcb_step)]
    
    if args.kicad_pcb:
        cmd.extend(["--kicad-pcb", args.kicad_pcb])
    
    cmd.extend(["--output", str(output_dir)])
    
    # Add optional flags
    if args.no_chamfers:
        cmd.append("--no-chamfers")
    if args.enable_fillets:
        cmd.append("--enable-fillets")
    if args.no_rubber_feet:
        cmd.append("--no-rubber-feet")
    if args.no_plate_lip:
        cmd.append("--no-plate-lip")
    
    if not run_command(cmd, "Generate case components"):
        return False
    
    logger.info("\n" + "="*60)
    logger.info("✅ WORKFLOW COMPLETE!")
    logger.info("="*60)
    logger.info(f"\nOutput files in: {output_dir}")
    logger.info("\nGenerated files:")
    logger.info("  - Bottom tray (STEP + STL)")
    logger.info("  - Switch plate (STEP + STL)")
    if args.generate_pcb_stl:
        logger.info("  - PCB visualization (STL)")
    
    return True


def workflow_split(args):
    """Workflow for split keyboard."""
    logger.info("\n✂️  SPLIT KEYBOARD WORKFLOW")
    logger.info("="*60)
    
    pcb_step = Path(args.pcb_step)
    output_dir = Path(args.output) if args.output else pcb_step.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Detect if PCB actually needs splitting
    if args.kicad_pcb:
        logger.info("\n🔍 Detecting PCB type...")
        from detect_pcb_type import detect_pcb_type
        pcb_type = detect_pcb_type(Path(args.kicad_pcb))
        
        if pcb_type == 'single_half':
            logger.info("\n⚠️  PCB appears to be a single unified keyboard, not split halves.")
            logger.info("    Using single keyboard workflow (no splitting needed)...")
            # Just generate case without splitting
            cmd = ["python", get_script_path("generate_case_unified.py"), str(pcb_step)]
            if args.kicad_pcb:
                cmd.extend(["--kicad-pcb", args.kicad_pcb])
            cmd.extend(["--output", str(output_dir)])
            
            # Add optional flags
            if args.no_chamfers:
                cmd.append("--no-chamfers")
            if args.enable_fillets:
                cmd.append("--enable-fillets")
            if args.no_rubber_feet:
                cmd.append("--no-rubber-feet")
            if args.no_plate_lip:
                cmd.append("--no-plate-lip")
            
            if not run_command(cmd, "Generate case for unified keyboard"):
                return False
            
            logger.info("\n" + "="*60)
            logger.info("✅ WORKFLOW COMPLETE!")
            logger.info("="*60)
            logger.info(f"\nOutput files in: {output_dir}")
            logger.info("\nGenerated files:")
            logger.info("  - Bottom tray (STEP + STL)")
            logger.info("  - Switch plate (STEP + STL)")
            return True
    
    # Step 1: Split PCB into left/right halves
    logger.info("\n📦 Step 1: Split PCB into left and right halves")
    cmd = ["python", get_script_path("split_keyboard.py"), str(pcb_step), str(output_dir)]
    if not run_command(cmd, "Split PCB"):
        return False
    
    # Determine the split PCB filenames
    # The split script removes _pcb suffix if present to avoid duplication
    base_name = pcb_step.stem
    if base_name.endswith('_pcb'):
        base_name = base_name[:-4]
    left_step = output_dir / f"{base_name}_pcb_left.step"
    right_step = output_dir / f"{base_name}_pcb_right.step"
    
    # Step 2: Generate cases for both halves
    logger.info("\n🏗️  Step 2: Generate cases for both halves")
    cmd = [
        "python", get_script_path("generate_case_unified.py"),
        "--left", str(left_step),
        "--right", str(right_step),
        "--output", str(output_dir)
    ]
    
    if args.kicad_pcb:
        cmd.extend(["--kicad-pcb", args.kicad_pcb])
    
    # Add optional flags
    if args.no_chamfers:
        cmd.append("--no-chamfers")
    if args.enable_fillets:
        cmd.append("--enable-fillets")
    if args.no_rubber_feet:
        cmd.append("--no-rubber-feet")
    if args.no_plate_lip:
        cmd.append("--no-plate-lip")
    
    if not run_command(cmd, "Generate cases for both halves"):
        return False
    
    logger.info("\n" + "="*60)
    logger.info("✅ WORKFLOW COMPLETE!")
    logger.info("="*60)
    logger.info(f"\nOutput files in: {output_dir}")
    logger.info("\nGenerated files:")
    logger.info("  LEFT HALF:")
    logger.info("    - PCB (STEP + STL)")
    logger.info("    - Bottom tray (STEP + STL)")
    logger.info("    - Switch plate (STEP + STL)")
    logger.info("  RIGHT HALF:")
    logger.info("    - PCB (STEP + STL)")
    logger.info("    - Bottom tray (STEP + STL)")
    logger.info("    - Switch plate (STEP + STL)")
    
    return True


def workflow_pcb_stl(args):
    """Just convert PCB STEP to STL."""
    logger.info("\n📦 PCB STEP → STL CONVERSION")
    logger.info("="*60)
    
    pcb_step = Path(args.pcb_step)
    output_dir = Path(args.output) if args.output else pcb_step.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pcb_stl = output_dir / f"{pcb_step.stem}.stl"
    
    cmd = ["python", get_script_path("convert_step_to_stl.py"), str(pcb_step), str(pcb_stl)]
    if not run_command(cmd, "Convert PCB STEP to STL"):
        return False
    
    logger.info(f"\n✅ PCB STL saved to: {pcb_stl}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Unified keyboard case generation workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single keyboard with switch detection
  python keyboard_case_workflow.py single keyboard.step --kicad-pcb keyboard.kicad_pcb
  
  # Split keyboard (auto-split + generate cases)
  python keyboard_case_workflow.py split keyboard.step --kicad-pcb keyboard.kicad_pcb
  
  # Just convert PCB to STL for visualization
  python keyboard_case_workflow.py pcb-stl keyboard.step
        """
    )
    
    subparsers = parser.add_subparsers(dest='workflow', help='Workflow type')
    
    # Single keyboard workflow
    single_parser = subparsers.add_parser('single', help='Single keyboard workflow')
    single_parser.add_argument('pcb_step', help='PCB STEP file')
    single_parser.add_argument('--kicad-pcb', help='KiCad PCB file for switch detection')
    single_parser.add_argument('-o', '--output', help='Output directory')
    single_parser.add_argument('--generate-pcb-stl', action='store_true', 
                              help='Also generate PCB STL for visualization')
    single_parser.add_argument('--no-chamfers', action='store_true', help='Disable chamfers')
    single_parser.add_argument('--enable-fillets', action='store_true', help='Enable fillets')
    single_parser.add_argument('--no-rubber-feet', action='store_true', help='Disable rubber feet')
    single_parser.add_argument('--no-plate-lip', action='store_true', help='Disable plate lip')
    
    # Split keyboard workflow
    split_parser = subparsers.add_parser('split', help='Split keyboard workflow')
    split_parser.add_argument('pcb_step', help='PCB STEP file (will be split)')
    split_parser.add_argument('--kicad-pcb', help='KiCad PCB file for switch detection')
    split_parser.add_argument('-o', '--output', help='Output directory')
    split_parser.add_argument('--no-chamfers', action='store_true', help='Disable chamfers')
    split_parser.add_argument('--enable-fillets', action='store_true', help='Enable fillets')
    split_parser.add_argument('--no-rubber-feet', action='store_true', help='Disable rubber feet')
    split_parser.add_argument('--no-plate-lip', action='store_true', help='Disable plate lip')
    
    # PCB STL conversion only
    pcb_parser = subparsers.add_parser('pcb-stl', help='Convert PCB STEP to STL only')
    pcb_parser.add_argument('pcb_step', help='PCB STEP file')
    pcb_parser.add_argument('-o', '--output', help='Output directory')
    
    args = parser.parse_args()
    
    if not args.workflow:
        parser.print_help()
        return 1
    
    # Run the appropriate workflow
    if args.workflow == 'single':
        success = workflow_single(args)
    elif args.workflow == 'split':
        success = workflow_split(args)
    elif args.workflow == 'pcb-stl':
        success = workflow_pcb_stl(args)
    else:
        parser.print_help()
        return 1
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
