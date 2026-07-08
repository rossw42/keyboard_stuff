"""
Stabilizer Detection & Spacing

Ported from kle-to-scad (formerly KLE_SCAD_Ergogen):
  - src/kleToIntermediate.js  (detection: keys >= 2u wide or tall need stabilizers)
  - scad/stabilizer_spacing.scad  (Cherry stabilizer spacing constants,
    measured center-to-center; source: Cherry MX stabilizer spec /
    hotswap_pcb_generator)

Offsets are in millimeters from the key center, based on a 19.05mm key unit.
Format mirrors the SCAD data: (key_size_u, left_offset_mm, right_offset_mm, switch_offset_mm)
"""

from typing import Dict, List, Optional, Any

UNIT = 19.05  # 1u in mm

# Cherry stabilizer spacing per key size (center-to-center offsets in mm).
# Key: canonical stabilizer type name. Values ported from stabilizer_spacing.scad.
STABILIZER_SPACING: Dict[str, Dict[str, float]] = {
    'stab_2u':            {'size': 2.0,  'left': 5 / 8 * UNIT,   'right': 5 / 8 * UNIT,   'switch_offset': 0.0},
    'stab_2_25u':         {'size': 2.25, 'left': 5 / 8 * UNIT,   'right': 5 / 8 * UNIT,   'switch_offset': 0.0},
    'stab_2_5u':          {'size': 2.5,  'left': 5 / 8 * UNIT,   'right': 5 / 8 * UNIT,   'switch_offset': 0.0},
    'stab_2_75u':         {'size': 2.75, 'left': 5 / 8 * UNIT,   'right': 5 / 8 * UNIT,   'switch_offset': 0.0},
    'stab_3u':            {'size': 3.0,  'left': 1.0 * UNIT,     'right': 1.0 * UNIT,     'switch_offset': 0.0},
    'stab_6u':            {'size': 6.0,  'left': 2.5 * UNIT,     'right': 2.5 * UNIT,     'switch_offset': 0.0},
    'stab_6_25u':         {'size': 6.25, 'left': 2.625 * UNIT,   'right': 2.625 * UNIT,   'switch_offset': 0.0},
    'stab_7u':            {'size': 7.0,  'left': 3.0 * UNIT,     'right': 3.0 * UNIT,     'switch_offset': 0.0},
}

# Ordered sizes for nearest-match lookup
_SIZES: List[float] = sorted(v['size'] for v in STABILIZER_SPACING.values())

STABILIZER_THRESHOLD_U = 2.0  # keys >= 2u (wide or tall) need a stabilizer


def needs_stabilizer(width_u: float, height_u: float = 1.0) -> bool:
    """A key needs a stabilizer if it is >= 2u wide or tall (Cherry spec)."""
    return width_u >= STABILIZER_THRESHOLD_U or height_u >= STABILIZER_THRESHOLD_U


def stabilizer_size(width_u: float, height_u: float = 1.0) -> float:
    """The dimension (in units) the stabilizer spans. 0 if none needed."""
    if width_u >= STABILIZER_THRESHOLD_U:
        return width_u
    if height_u >= STABILIZER_THRESHOLD_U:
        return height_u
    return 0.0


def get_stabilizer_type(width_u: float, height_u: float = 1.0) -> Optional[str]:
    """
    Return the canonical stabilizer type name (e.g. 'stab_6_25u') for a key,
    or None if the key doesn't need a stabilizer.

    Sizes without an exact entry map to the nearest defined size at or below
    (e.g. a 4u key uses stab_3u spacing, matching kle-to-scad behavior of
    falling back to the closest known constant).
    """
    size = stabilizer_size(width_u, height_u)
    if size <= 0:
        return None

    # Exact match first
    for name, data in STABILIZER_SPACING.items():
        if abs(data['size'] - size) < 0.001:
            return name

    # Nearest defined size at or below; else smallest
    candidates = [s for s in _SIZES if s <= size]
    nearest = candidates[-1] if candidates else _SIZES[0]
    for name, data in STABILIZER_SPACING.items():
        if abs(data['size'] - nearest) < 0.001:
            return name
    return None


def get_stabilizer_spacing(width_u: float, height_u: float = 1.0) -> Optional[Dict[str, float]]:
    """
    Return spacing info {'size', 'left', 'right', 'switch_offset'} in mm
    for a key, or None if no stabilizer is needed.
    """
    stab_type = get_stabilizer_type(width_u, height_u)
    if stab_type is None:
        return None
    return dict(STABILIZER_SPACING[stab_type])


def get_stabilizer_info(width_u: float, height_u: float = 1.0) -> Optional[Dict[str, Any]]:
    """
    Full stabilizer record for a key, or None.

    Returns:
        {'type': 'stab_6_25u', 'size': 6.25, 'vertical': bool,
         'left': mm, 'right': mm, 'switch_offset': mm}
    """
    stab_type = get_stabilizer_type(width_u, height_u)
    if stab_type is None:
        return None
    spacing = STABILIZER_SPACING[stab_type]
    return {
        'type': stab_type,
        'size': stabilizer_size(width_u, height_u),
        'vertical': height_u >= STABILIZER_THRESHOLD_U and width_u < STABILIZER_THRESHOLD_U,
        'left': spacing['left'],
        'right': spacing['right'],
        'switch_offset': spacing['switch_offset'],
    }