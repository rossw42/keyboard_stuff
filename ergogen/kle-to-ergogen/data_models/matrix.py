"""
Matrix (row/col) Assignment

Ported from kle-to-scad (formerly KLE_SCAD_Ergogen):
  - src/kleToIntermediate.js  assignMatrixPositions()

Assigns electrical-matrix-style row/col indices to keys based on their
*physical* positions rather than their KLE JSON row index. This handles
layouts where keys are placed with explicit y offsets (row skips, split
halves, thumb clusters) that would confuse a naive per-KLE-row counter.

Algorithm (faithful port of the JS original):
  1. Sort keys by Y position, then X position.
  2. Group keys into rows: a key starts a new row when its Y differs from
     the previous row's Y by more than ROW_TOLERANCE_U (0.1u).
  3. Within each row, keys are ordered by X; each key gets
     (row_index, column_index_within_row).

This intermediate row/col data also feeds the future QMK conversion stage
(see docs/qmk/ARCHITECTURE.md).
"""

from typing import List, Sequence, Any

# Keys whose Y positions differ by more than this (in key units) are
# considered to be on different physical rows. Matches kle-to-scad's 0.1.
ROW_TOLERANCE_U = 0.1


def assign_matrix_positions(keys: Sequence[Any], tolerance: float = ROW_TOLERANCE_U) -> List[List[Any]]:
    """
    Assign position-based matrix row/col indices to keys in place.

    Each key object must expose numeric `x` and `y` attributes (in KLE key
    units) and writable `matrix_row` / `matrix_col` attributes
    (e.g. parsers.simple_kle_parser.KeyDefinition).

    Args:
        keys: Sequence of key objects to annotate (mutated in place).
        tolerance: Max Y difference (in units) for keys to share a row.

    Returns:
        The grouped rows (list of lists of keys), ordered top-to-bottom
        and left-to-right, for callers that want the grouping itself.
    """
    if not keys:
        return []

    # 1. Sort by Y, then X (mirrors the JS comparator; exact-tie X ordering
    #    is finalized by the per-row X sort below).
    sorted_keys = sorted(keys, key=lambda k: (k.y, k.x))

    # 2. Group into rows using the running-Y tolerance check.
    rows: List[List[Any]] = []
    current_row: List[Any] = [sorted_keys[0]]
    last_y = sorted_keys[0].y

    for key in sorted_keys[1:]:
        if abs(key.y - last_y) > tolerance:
            rows.append(current_row)
            current_row = [key]
            last_y = key.y
        else:
            current_row.append(key)

    rows.append(current_row)

    # 3. Assign indices (rows top-to-bottom, columns left-to-right).
    for row_index, row in enumerate(rows):
        row.sort(key=lambda k: k.x)
        for col_index, key in enumerate(row):
            key.matrix_row = row_index
            key.matrix_col = col_index

    return rows