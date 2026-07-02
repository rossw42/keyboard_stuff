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

import cadquery as cq

from case_generator.config import CaseConfig, load_config_file
from case_generator.pcb_analyzer import analyze_pcb, PCBImportError
from case_generator.switch_detector import detect_switch_layout
from case_generator.bottom_tray import create_bottom_tray
from case_generator.sandwich_mount import create_sandwich_case
from case_generator.switch_plate import create_switch_plate
from case_generator.features import (
    apply_chamfers,
    apply_fillets,
    add_rubber_feet_recesses,
    add_plate_mounting_lip
)
from case_generator.exporter import export_step, export_stl, generate_filename, ExportError
from case_generator.geometry_utils import calculate_bounding_box, offset_outline
from case_generator.split_to_unified import detect_split_keyboard, create_unified_outline

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
  
  # Split keyboard - unified case (auto-detect split and mirror)
  %(prog)s keyboard_split.step --kicad-pcb keyboard.kicad_pcb --unified
        """
    )

    
    # Input files
    parser.add_argument('pcb_step', nargs='?', type=Path,
                       help='PCB STEP file (for single or split keyboard)')
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
                       help='Wall thickness in mm (default: 2.0, recommended: 2-3mm)')
    parser.add_argument('--case-height', type=float, default=8.0,
                       help='Case height in mm (default: 8.0 for MX hotswap, 6.5 for MX soldered, 4.5 for Choc hotswap, 3.0 for Choc soldered)')
    parser.add_argument('--case-offset', type=float, default=1.0,
                       help='Case offset from PCB edge in mm (default: 1.0, recommended for PCB manufacturing tolerance)')
    
    # Features
    parser.add_argument('--no-chamfers', action='store_true',
                       help='Disable chamfered edges')
    parser.add_argument('--enable-fillets', action='store_true',
                       help='Use fillets instead of chamfers')
    parser.add_argument('--no-rubber-feet', action='store_true',
                       help='Disable rubber feet recesses')
    parser.add_argument('--no-plate-lip', action='store_true',
                       help='Disable plate mounting lip')
    parser.add_argument('--unified', action='store_true',
                       help='Unified keyboard (mirror switches for both halves)')
    
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
    config.is_unified = args.unified
    
    return config



def generate_unified_case(
    pcb_file: Path,
    config: CaseConfig
) -> None:
    """Generate unified case from split keyboard PCB."""
    logger.info(f"\n{'='*60}")
    logger.info(f"Generating unified case from split keyboard")
    logger.info(f"{'='*60}")
    
    start_time = time.time()
    
    # Step 1: Analyze PCB
    logger.info("\n[1/7] Analyzing PCB...")
    pcb_info = analyze_pcb(pcb_file)
    
    # Step 2: Detect split keyboard
    logger.info("\n[2/7] Detecting split keyboard...")
    split_detection = detect_split_keyboard(pcb_info.outline, pcb_info.wire)
    
    if not split_detection.is_split:
        logger.warning("No split detected - treating as single keyboard")
        generate_case_for_side(pcb_file, config, None)
        return
    
    logger.info(f"  Split axis: {split_detection.split_axis}")
    logger.info(f"  Split position: {split_detection.split_position:.2f}")
    
    # Step 3: Create unified outline
    logger.info("\n[3/7] Creating unified outline...")
    unified_outline = create_unified_outline(
        split_detection.left_outline,
        split_detection.right_outline,
        split_detection.split_axis,
        split_detection.split_position
    )
    
    # Create a modified PCBInfo with unified outline
    from case_generator.pcb_analyzer import PCBInfo
    
    # Create a wire from the unified outline for smooth geometry
    try:
        import cadquery as cq
        unified_wire = cq.Wire.makePolygon([cq.Vector(p[0], p[1], 0) for p in unified_outline])
    except Exception as e:
        logger.warning(f"Failed to create wire from unified outline: {e}")
        unified_wire = None
    
    unified_pcb_info = PCBInfo(
        outline=unified_outline,
        bounding_box=calculate_bounding_box(unified_outline),
        mounting_holes=pcb_info.mounting_holes,  # Keep original mounting holes
        thickness=pcb_info.thickness,
        wire=unified_wire  # Use the created wire for smooth offsetting
    )
    
    # Step 4: Detect switches (with unified flag)
    logger.info("\n[4/7] Detecting switches...")
    switch_layout = detect_switch_layout(config.kicad_pcb, unified_pcb_info, None, is_unified=True)
    
    # Step 5: Generate bottom tray
    logger.info("\n[5/7] Generating bottom tray...")
    bottom_tray = create_bottom_tray(unified_pcb_info, config, switch_layout)
    
    # Step 6: Apply features to bottom tray
    logger.info("\n[6/7] Applying features to bottom tray...")
    
    if config.enable_chamfers:
        bottom_tray = apply_chamfers(bottom_tray, config.outer_chamfer, config.inner_chamfer)
    elif config.enable_fillets:
        bottom_tray = apply_fillets(bottom_tray, config.fillet_radius)
    
    if config.enable_rubber_feet:
        bbox = calculate_bounding_box(offset_outline(unified_outline, config.case_offset))
        bottom_tray = add_rubber_feet_recesses(
            bottom_tray,
            bbox,
            config.feet_diameter,
            config.feet_depth,
            config.feet_corner_offset
        )
    
    if config.enable_plate_lip:
        lip_z = config.bottom_thickness + config.pcb_clearance + unified_pcb_info.thickness
        bottom_tray = add_plate_mounting_lip(
            bottom_tray,
            unified_outline,
            config.wall_thickness,
            config.lip_width,
            config.lip_height,
            lip_z,
            config.case_offset,
            None  # No wire for unified outline
        )
    
    # Step 7: Generate switch plate
    logger.info("\n[7/7] Generating switch plate...")
    switch_plate = create_switch_plate(unified_pcb_info, switch_layout, config)
    
    # Export files
    logger.info("\nExporting files...")
    
    base_name = pcb_file.stem.replace('_pcb', '').replace('_split', '')
    
    # Export bottom tray
    tray_step = config.output_dir / generate_filename(base_name, 'bottom_tray', 'unified', 'step')
    tray_stl = config.output_dir / generate_filename(base_name, 'bottom_tray', 'unified', 'stl')
    export_step(bottom_tray, tray_step)
    export_stl(bottom_tray, tray_stl, config.stl_tolerance)
    
    # Export switch plate
    plate_step = config.output_dir / generate_filename(base_name, 'switch_plate', 'unified', 'step')
    plate_stl = config.output_dir / generate_filename(base_name, 'switch_plate', 'unified', 'stl')
    export_step(switch_plate, plate_step)
    export_stl(switch_plate, plate_stl, config.stl_tolerance)
    
    elapsed = time.time() - start_time
    logger.info(f"\n✓ Unified case complete in {elapsed:.1f} seconds")


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
    
    # Step 1.5: Clean outline for aesthetics
    if config.clean_outline:
        logger.info("\n[1.5/6] Cleaning outline for aesthetics...")
        from case_generator.outline_cleanup import clean_outline_for_case
        from case_generator.pcb_analyzer import PCBInfo
        from case_generator.geometry_utils import calculate_bounding_box
        
        cleaned_outline = clean_outline_for_case(
            pcb_info.outline,
            fill_notches=True,
            smooth=True,
            notch_depth=config.notch_fill_depth
        )
        
        # Create wire from cleaned outline
        try:
            cleaned_wire = cq.Wire.makePolygon([cq.Vector(p[0], p[1], 0) for p in cleaned_outline])
        except:
            cleaned_wire = None
        
        pcb_info = PCBInfo(
            outline=cleaned_outline,
            bounding_box=calculate_bounding_box(cleaned_outline),
            mounting_holes=pcb_info.mounting_holes,
            thickness=pcb_info.thickness,
            wire=cleaned_wire
        )
    
    # Step 2: Detect switches
    logger.info("\n[2/6] Detecting switches...")
    switch_layout = detect_switch_layout(config.kicad_pcb, pcb_info, side_name, config.is_unified)
    
    # Step 3: Generate flat bottom plate (just a plate with mounting holes)
    logger.info("\n[3/6] Generating flat bottom plate...")
    # Create simple flat plate
    if pcb_info.wire:
        outer_wires = pcb_info.wire.offset2D(config.case_offset + config.wall_thickness)
        bottom_tray = (cq.Workplane("XY")
                      .add(outer_wires[0])
                      .toPending()
                      .extrude(config.bottom_thickness))
    else:
        from case_generator.geometry_utils import simplify_outline, offset_outline
        simplified = simplify_outline(pcb_info.outline, tolerance=0.2)
        plate_outline = offset_outline(simplified, config.case_offset + config.wall_thickness)
        bottom_tray = cq.Workplane("XY").polyline(plate_outline).close().extrude(config.bottom_thickness)
    
    # Add mounting holes to bottom plate
    if pcb_info.mounting_holes:
        for x, y in pcb_info.mounting_holes:
            hole = (cq.Workplane("XY")
                   .center(x, y)
                   .circle(config.boss_hole_diameter / 2)
                   .extrude(config.bottom_thickness + 1))
            bottom_tray = bottom_tray.cut(hole)
    
    # Step 4: Generate top frame (switch plate with walls extending downward)
    logger.info("\n[4/6] Generating top frame with walls...")
    switch_plate = create_sandwich_case(pcb_info, config, switch_layout)
    
    # Step 5: Add switch cutouts to top frame
    logger.info("\n[5/6] Adding switch cutouts to top frame...")
    if switch_layout and switch_layout.switches:
        from case_generator.switch_plate import create_switch_cutouts
        switch_plate = create_switch_cutouts(
            switch_plate,
            switch_layout.switches,
            config.switch_cutout_size,
            config.plate_thickness
        )
    
    # Step 5.5: Apply chamfers/fillets to top edges
    if config.enable_chamfers or config.enable_fillets:
        logger.info("  Applying edge finishing to top edges...")
        try:
            # Apply fillet (rounded edge) which is more reliable than chamfer
            fillet_size = 0.5  # Small fillet for clean edges
            
            # Fillet all edges on the top surface
            switch_plate = switch_plate.faces(">Z").edges().fillet(fillet_size)
            logger.info(f"  ✓ Applied {fillet_size}mm fillet to top edges")
        except Exception as e:
            logger.warning(f"  Failed to apply edge finishing: {e}, continuing without")
    
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
        if config.is_unified and config.pcb_step_left:
            # Unified mode - take single split PCB and create unified case
            generate_unified_case(config.pcb_step_left, config)
        elif config.side == 'single':
            # Single keyboard mode - no side suffix
            generate_case_for_side(config.pcb_step_left, config, None)
        else:
            # Split keyboard mode (separate left/right cases)
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
