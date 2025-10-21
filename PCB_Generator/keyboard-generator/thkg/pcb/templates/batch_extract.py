"""Batch extract templates from all library schematics."""

import json
import logging
from pathlib import Path
from typing import Dict, List

# Handle imports for both module and standalone execution
try:
    from .extractor import extract_templates, CircuitBlock
except ImportError:
    from extractor import extract_templates, CircuitBlock

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def find_schematics(library_path: Path) -> List[Path]:
    """Find all main schematic files in library.
    
    Args:
        library_path: Path to pcb-library/design-files
    
    Returns:
        List of schematic file paths
    """
    schematics = []
    
    # Key designs to extract from
    designs = {
        'lumberjack': 'lumberjack/kicad/lumberjack.kicad_sch',  # ATmega328P + USB-C
        'dumbpad': 'dumbpad/kicad/dumbpad.kicad_sch',           # ATmega32U4 + USB-C
        'litl': 'litl/kicad/litl.kicad_sch',                    # Pro Micro
    }
    
    for name, path in designs.items():
        full_path = library_path / path
        if full_path.exists():
            schematics.append((name, full_path))
        else:
            logger.warning(f"Schematic not found: {path}")
    
    return schematics


def extract_all_templates(library_path: Path) -> Dict[str, List[CircuitBlock]]:
    """Extract templates from all library schematics.
    
    Args:
        library_path: Path to pcb-library/design-files
    
    Returns:
        Dictionary mapping design name to list of circuit blocks
    """
    schematics = find_schematics(library_path)
    all_templates = {}
    
    logger.info(f"Found {len(schematics)} schematics to process\n")
    logger.info("=" * 80)
    
    for design_name, schematic_path in schematics:
        logger.info(f"\n📋 Processing: {design_name}")
        logger.info(f"   File: {schematic_path.name}")
        logger.info("-" * 80)
        
        try:
            blocks = extract_templates(schematic_path)
            all_templates[design_name] = blocks
            
            logger.info(f"\n✓ Extracted {len(blocks)} circuit blocks:")
            for block in blocks:
                logger.info(f"  • {block.name} ({block.block_type})")
                logger.info(f"    Components: {len(block.components)}")
                
                # Show key components
                for comp in block.components[:5]:  # First 5
                    logger.info(f"      - {comp['reference']:8s} {comp['value']:15s} ({comp['lib_id'].split(':')[-1]})")
                
                if len(block.components) > 5:
                    logger.info(f"      ... and {len(block.components) - 5} more")
        
        except Exception as e:
            logger.error(f"✗ Failed to extract from {design_name}: {e}")
            all_templates[design_name] = []
    
    logger.info("\n" + "=" * 80)
    logger.info(f"\n✓ Batch extraction complete!")
    logger.info(f"  Processed: {len(schematics)} designs")
    logger.info(f"  Total blocks: {sum(len(blocks) for blocks in all_templates.values())}")
    
    return all_templates


def save_templates(templates: Dict[str, List[CircuitBlock]], output_path: Path):
    """Save extracted templates to JSON file.
    
    Args:
        templates: Dictionary of templates by design
        output_path: Path to save JSON file
    """
    # Convert to serializable format
    data = {}
    for design_name, blocks in templates.items():
        data[design_name] = [block.to_dict() for block in blocks]
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    logger.info(f"\n💾 Saved templates to: {output_path}")
    logger.info(f"   File size: {output_path.stat().st_size / 1024:.1f} KB")


def print_summary(templates: Dict[str, List[CircuitBlock]]):
    """Print summary of extracted templates.
    
    Args:
        templates: Dictionary of templates by design
    """
    logger.info("\n" + "=" * 80)
    logger.info("📊 TEMPLATE LIBRARY SUMMARY")
    logger.info("=" * 80)
    
    # Group by MCU type
    mcu_blocks = {}
    usb_blocks = {}
    crystal_blocks = {}
    reset_blocks = {}
    
    for design_name, blocks in templates.items():
        for block in blocks:
            if block.block_type == 'mcu':
                mcu_blocks[design_name] = block
            elif block.block_type == 'usb':
                usb_blocks[design_name] = block
            elif block.block_type == 'crystal':
                crystal_blocks[design_name] = block
            elif block.block_type == 'reset':
                reset_blocks[design_name] = block
    
    logger.info(f"\n🔧 MCU Templates ({len(mcu_blocks)}):")
    for design, block in mcu_blocks.items():
        logger.info(f"  • {design:15s} → {block.name}")
    
    logger.info(f"\n🔌 USB Templates ({len(usb_blocks)}):")
    for design, block in usb_blocks.items():
        logger.info(f"  • {design:15s} → {block.name}")
    
    logger.info(f"\n⏰ Crystal Templates ({len(crystal_blocks)}):")
    for design, block in crystal_blocks.items():
        logger.info(f"  • {design:15s} → {block.name}")
    
    if reset_blocks:
        logger.info(f"\n🔄 Reset Templates ({len(reset_blocks)}):")
        for design, block in reset_blocks.items():
            logger.info(f"  • {design:15s} → {block.name}")
    
    logger.info("\n" + "=" * 80)


if __name__ == "__main__":
    # Extract from library
    library_path = Path("../pcb-library/design-files")
    
    if not library_path.exists():
        logger.error(f"Library path not found: {library_path}")
        logger.error("Run from keyboard-generator directory")
        exit(1)
    
    logger.info("🚀 Starting batch template extraction")
    logger.info(f"   Library: {library_path.absolute()}\n")
    
    # Extract all templates
    templates = extract_all_templates(library_path)
    
    # Print summary
    print_summary(templates)
    
    # Save to cache
    cache_path = Path("thkg/pcb/templates/cache/library_templates.json")
    save_templates(templates, cache_path)
    
    logger.info("\n✅ Done! Templates ready for use in PCB generation.")
