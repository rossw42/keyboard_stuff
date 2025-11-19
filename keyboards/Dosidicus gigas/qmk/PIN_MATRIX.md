# Dosidicus Gigas Pin Matrix

## Matrix Configuration

Based on the Ergogen YAML configuration, here's the pin mapping:

### Left Half (Primary)
**Columns (8 total):**
- Col 0: F4 (Pinky column - P1, P3, P4)
- Col 1: F5 (Ring column - P5, P6, P7)
- Col 2: F6 (Middle column - P8, P9, P16)
- Col 3: F7 (Index column - P14, P15, P18)
- Col 4: B1 (Inner column - P19, P20, P21)
- Col 5: B3 (Thumb - P10)
- Col 6: B2 (Reserved)
- Col 7: B6 (Reserved)

**Rows (4 total):**
- Row 0: D4 (Top row)
- Row 1: C6 (Home row)
- Row 2: D7 (Bottom row)
- Row 3: E6 (Thumb row)

### Right Half (Secondary - Mirrored)
Uses the same pin configuration but mirrored through TRRS connection.

### Split Communication
- **Serial Pin:** D2 (TRRS pin C - P2 in Ergogen)
- **Handedness Detection:** B5 (SPLIT_HAND_PIN)
- **TRRS Pinout:**
  - Tip (A): GND
  - Ring 1 (B): GND
  - Ring 2 (C): D2 (Serial Data)
  - Sleeve (D): VCC

## Physical Layout

```
Left Hand:                    Right Hand:
┌───┬───┬───┬───┬───┐        ┌───┬───┬───┬───┬───┐
│ Q │ W │ E │ R │ T │        │ Y │ U │ I │ O │ P │
├───┼───┼───┼───┼───┤        ├───┼───┼───┼───┼───┤
│ A │ S │ D │ F │ G │        │ H │ J │ K │ L │ ; │
├───┼───┼───┼───┼───┤        ├───┼───┼───┼───┼───┤
│ Z │ X │ C │ V │ B │        │ N │ M │ , │ . │ / │
└───┴───┴───┴───┴───┘        └───┴───┴───┴───┴───┘
            ┌───┐                    ┌───┐
            │SPC│                    │ENT│
            └───┘                    └───┘
```

## Matrix Mapping

### Left Half Matrix
```
     Col0  Col1  Col2  Col3  Col4  Col5
Row0  Q     W     E     R     T     -
Row1  A     S     D     F     G     -
Row2  Z     X     C     V     B     -
Row3  -     -     -     -     -    SPC
```

### Right Half Matrix (Mirrored)
```
     Col0  Col1  Col2  Col3  Col4  Col5
Row0  P     O     I     U     Y     -
Row1  ;     L     K     J     H     -
Row2  /     .     ,     M     N     -
Row3  -     -     -     -     -    ENT
```

## Ergogen Column Net Mapping

From the YAML file, the column_net assignments map to Pro Micro pins:

| Ergogen Net | Pro Micro Pin | QMK Pin | Usage |
|-------------|---------------|---------|-------|
| P1          | 2             | F4      | Pinky bottom |
| P3          | 3             | F5      | Pinky home |
| P4          | 4             | F6      | Pinky top |
| P5          | 5             | F7      | Ring bottom |
| P6          | 6             | B1      | Ring home |
| P7          | 7             | B3      | Ring top |
| P8          | 8             | B2      | Middle bottom |
| P9          | 9             | B6      | Middle home |
| P10         | 10            | D4      | Thumb |
| P14-P21     | (mirrored)    | -       | Right half |

## Notes

1. The keyboard uses COL2ROW diode direction
2. Each switch connects column_net to GND
3. TRRS cable carries serial data on pin D2
4. Handedness is detected via SPLIT_HAND_PIN (B5) or EEPROM
5. The matrix is 8 rows × 5 cols total (4 rows per half)
