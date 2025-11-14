"""
Geometry generation modules for 2D profiles and features.
"""

from .profiles import (
    generate_rounded_rectangle,
    generate_external_profile,
    generate_pcb_opening,
    generate_usb_cutout,
    generate_circle,
    generate_brass_insert_holes,
    generate_top_frame_profile,
    generate_internal_cavity,
    generate_standoff_pillars,
    generate_standoff_holes,
    generate_assembly_screw_holes,
    generate_assembly_screw_counterbores,
    generate_rubber_feet_recesses,
    generate_bottom_tray_profile,
)

__all__ = [
    'generate_rounded_rectangle',
    'generate_external_profile',
    'generate_pcb_opening',
    'generate_usb_cutout',
    'generate_circle',
    'generate_brass_insert_holes',
    'generate_top_frame_profile',
    'generate_internal_cavity',
    'generate_standoff_pillars',
    'generate_standoff_holes',
    'generate_assembly_screw_holes',
    'generate_assembly_screw_counterbores',
    'generate_rubber_feet_recesses',
    'generate_bottom_tray_profile',
]
