#!/usr/bin/env python3
"""
Unified Keyboard Case Generator

Generate 3D-printable keyboard case components from KiCad PCB exports.
"""

import argparse
import logging
import sys
import time
from pathlib import Path

from case_generator.config import CaseConfig, load_config_file
from case_generator.pcb_analyzer import analyze_pcb, PCBImportError
from case_generator.switch_detector import detect_switch_layout
from case_generator.bottom_tray import create_bottom_tray
from case_generator.switch_plate import create_switch_plate
from case_generator.features import (
    apply_chamfers,
    apply_fillets,
    add_rubber_feet_recesses,
    add_plate_mounting_lip
)
from case_generator.exporter import export_step, export_stl, generate_filename, ExportError
from case_generator.geometry_utils import calculate_bounding_box, offset_outline

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args() -> CaseConfig:
    """Parse command-line arguments and return configuration."""
    parser = argparse.ArgumentParser(
        description='Generate 3D-printable keyboard case from KiCad PCB export',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single keyboard
  %(prog)s keyboard.step --kicad-pcb keyboard.kicad_pcb
  
  # Split keyboard - both halves
  %(prog)s --left keyboard_left.step --right keyboard_right.step
  
  # Split keyboard - left half only
  %(prog)s --left keyboard_left.step --side left
        """
    )

    
    # Input files
    parser.add_argument('pcb_step', nargs='?', type=Path,
                       help='PCB STEP file (for single keyboard)')
    parser.add_argument('--left', type=Path,
                       help='Left PCB STEP file (for split keyboard)')
    parser.add_argument('--right', type=Path,
                       help='Right PCB STEP file (for split keyboard)')
    parser.add_argument('--kicad-pcb', type=Path,
                       help='KiCad PCB file for switch positions (optional)')
    parser.add_argument('--config', type=Path,
                       help='JSON configuration file')
    parser.add_argument('-o', '--output', type=Path, default=Path('./output'),
                       help='Output directory (default: ./output)')
    parser.add_argument('--side', choices=['left', 'right', 'both'], default='both',
                       help='Which side to generate for split keyboards (default: both)')
    
    # Case dimensions
    parser.add_argument('--wall-thickness', type=float, default=2.0,
                       help='Wall thickness in mm (default: 2.0)')
    parser.add_argument('--case-height', type=float, default=8.0,
                       help='Case height in mm (default: 8.0)')
    parser.add_argument('--case-offset', type=float, default=2.5,
                       help='Case offset from PCB edge in mm (default: 2.5)')
    
    # Features
    parser.add_argument('--no-chamfers', action='store_true',
                       help='Disable chamfered edges')
    parser.add_argument('--enable-fillets', action='store_true',
                       help='Use fillets instead of chamfers')
    parser.add_argument('--no-rubber-feet', action='store_true',
                       help='Disable rubber feet recesses')
    parser.add_argument('--no-plate-lip', action='store_true',
                       help='Disable plate mounting lip')
    
    args = parser.parse_args()
    
    # Determine input files and mode
    if args.pcb_step:
        # Single keyboard mode
        pcb_left = args.pcb_step
        pcb_right = None
        side = 'single'  # Special mode for single keyboard
    else:
        # Split keyboard mode
        pcb_left = args.left
        pcb_right = args.right
        side = args.side
    
    # Load config from file if provided
    if args.config:
        config_data = load_config_file(args.config)
        config = CaseConfig.from_dict(config_data)
    else:
        config = CaseConfig()
    
    # Override with command-line arguments
    config.pcb_step_left = pcb_left
    config.pcb_step_right = pcb_right
    config.kicad_pcb = args.kicad_pcb
    config.output_dir = args.output
    config.side = side
    config.wall_thickness = args.wall_thickness
    config.case_height = args.case_height
    config.case_offset = args.case_offset
    config.enable_chamfers = not args.no_chamfers
    config.enable_fillets = args.enable_fillets
    config.enable_rubber_feet = not args.no_rubber_feet
    config.enable_plate_lip = not args.no_plate_lip
    
    return config



def generate_case_for_side(
    pcb_file: Path,
    config: CaseConfig,
    side_name: str
) -> None:
    """Generate case for one side."""
    logger.info(f"\n{'='*60}")
    logger.info(f"Generating case for {side_name} side")
    logger.info(f"{'='*60}")
    
    start_time = time.time()
    
    # Step 1: Analyze PCB
    logger.info("\n[1/6] Analyzing PCB...")
    pcb_info = analyze_pcb(pcb_file)
    
    # Step 2: Detect switches
    logger.info("\n[2/6] Detecting switches...")
    switch_layout = detect_switch_layout(config.kicad_pcb, pcb_info, side_name)
    
    # Step 3: Generate bottom tray
    logger.info("\n[3/6] Generating bottom tray...")
    bottom_tray = create_bottom_tray(pcb_info, config, switch_layout)
    
    # Step 4: Apply features to bottom tray
    logger.info("\n[4/6] Applying features to bottom tray...")
    
    if config.enable_chamfers:
        bottom_tray = apply_chamfers(bottom_tray, config.outer_chamfer, config.inner_chamfer)
    elif config.enable_fillets:
        bottom_tray = apply_fillets(bottom_tray, config.fillet_radius)
    
    if config.enable_rubber_feet:
        bbox = calculate_bounding_box(offset_outline(pcb_info.outline, config.case_offset))
        bottom_tray = add_rubber_feet_recesses(
            bottom_tray,
            bbox,
            config.feet_diameter,
            config.feet_depth,
            config.feet_corner_offset
        )
    
    if config.enable_plate_lip:
        lip_z = config.bottom_thickness + config.pcb_clearance + pcb_info.thickness
        bottom_tray = add_plate_mounting_lip(
            bottom_tray,
            pcb_info.outline,
            config.wall_thickness,
            config.lip_width,
            config.lip_height,
            lip_z,
            config.case_offset,
            pcb_info.wire
        )
    
    # Step 5: Generate switch plate
    logger.info("\n[5/6] Generating switch plate...")
    switch_plate = create_switch_plate(pcb_info, switch_layout, config)
    
    # Step 6: Export files
    logger.info("\n[6/6] Exporting files...")
    
    base_name = pcb_file.stem.replace('_pcb', '').replace('_left', '').replace('_right', '')
    
    # Export bottom tray
    tray_step = config.output_dir / generate_filename(base_name, 'bottom_tray', side_name, 'step')
    tray_stl = config.output_dir / generate_filename(base_name, 'bottom_tray', side_name, 'stl')
    export_step(bottom_tray, tray_step)
    export_stl(bottom_tray, tray_stl, config.stl_tolerance)
    
    # Export switch plate
    plate_step = config.output_dir / generate_filename(base_name, 'switch_plate', side_name, 'step')
    plate_stl = config.output_dir / generate_filename(base_name, 'switch_plate', side_name, 'stl')
    export_step(switch_plate, plate_step)
    export_stl(switch_plate, plate_stl, config.stl_tolerance)
    
    elapsed = time.time() - start_time
    side_label = side_name.capitalize() if side_name else "Case"
    logger.info(f"\n✓ {side_label} complete in {elapsed:.1f} seconds")



def main():
    """Main entry point."""
    try:
        # Parse arguments
        config = parse_args()
        
        # Validate configuration
        errors = config.validate()
        if errors:
            logger.error("Configuration errors:")
            for error in errors:
                logger.error(f"  - {error}")
            sys.exit(1)
        
        # Display configuration
        logger.info("\n" + "="*60)
        logger.info("UNIFIED KEYBOARD CASE GENERATOR")
        logger.info("="*60)
        logger.info("\nConfiguration:")
        logger.info(f"  Side: {config.side}")
        logger.info(f"  Wall thickness: {config.wall_thickness}mm")
        logger.info(f"  Case height: {config.case_height}mm")
        logger.info(f"  Case offset: {config.case_offset}mm")
        logger.info(f"  Chamfers: {'enabled' if config.enable_chamfers else 'disabled'}")
        logger.info(f"  Fillets: {'enabled' if config.enable_fillets else 'disabled'}")
        logger.info(f"  Rubber feet: {'enabled' if config.enable_rubber_feet else 'disabled'}")
        logger.info(f"  Plate lip: {'enabled' if config.enable_plate_lip else 'disabled'}")
        logger.info(f"  Output: {config.output_dir}")
        
        total_start = time.time()
        
        # Generate for requested sides
        if config.side == 'single':
            # Single keyboard mode - no side suffix
            generate_case_for_side(config.pcb_step_left, config, None)
        else:
            # Split keyboard mode
            if config.side in ('left', 'both') and config.pcb_step_left:
                generate_case_for_side(config.pcb_step_left, config, 'left')
            
            if config.side in ('right', 'both') and config.pcb_step_right:
                generate_case_for_side(config.pcb_step_right, config, 'right')
        
        total_elapsed = time.time() - total_start
        
        logger.info("\n" + "="*60)
        logger.info(f"✓ ALL COMPLETE in {total_elapsed:.1f} seconds")
        logger.info("="*60)
        logger.info(f"\nOutput files in: {config.output_dir}")
        
    except PCBImportError as e:
        logger.error(f"\n{e}")
        sys.exit(1)
    except ExportError as e:
        logger.error(f"\n{e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\n\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
