# Numpad Keyboard Connection Diagram

Analysis of the config_4x5.yaml ergogen configuration file showing physical layout and electrical connections.

## Physical Layout Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                NUMPAD KEYBOARD                                      │
├──────────────┬────────────────────────────────────────────┬─────────────────────────┤
│   NAV        │             NUMPAD GRID (4x5)              │    RIGHT SECTION        │
│  COLUMN      │                                            │                         │
│              │                                            │  ┌─────────────────┐    │
│  ┌───────┐   │  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐   │  │      OLED       │    │
│  │       │   │  │  NUM  │ │   /   │ │   *   │ │   -   │   │  │     SCREEN      │    │
│  │       │   │  │ LOCK  │ │       │ │       │ │       │   │  │   (32x16mm)     │    │
│  └───────┘   │  └───────┘ └───────┘ └───────┘ └───────┘   │  └─────────────────┘    │
│              │                                            │                         │
│  ┌───────┐   │  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐   │   ┌───────┐ ┌───────┐   │
│  │       │   │  │   7   │ │   8   │ │   9   │ │       │   │   │  ENC  │ │  ENC  │   │
│  │       │   │  │       │ │       │ │       │ │   +   │   │   │ LEFT  │ │ RIGHT │   │
│  └───────┘   │  └───────┘ └───────┘ └───────┘ │  (2U) │   │   └───────┘ └───────┘   │
│              │                                │       │   │                         │
│  ┌───────┐   │  ┌───────┐ ┌───────┐ ┌───────┐ │       │   │      ┌───────┐          │
│  │       │   │  │   4   │ │   5   │ │   6   │ └───────┘   │      │  ENC  │          │
│  │       │   │  │       │ │       │ │       │             │      │ BOTTOM│          │
│  └───────┘   │  └───────┘ └───────┘ └───────┘             │      └───────┘          │
│              │                                            │                         │
│  ┌───────┐   │  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐   │   ┌─────────────────┐   │
│  │       │   │  │   1   │ │   2   │ │   3   │ │       │   │   │     THUMB       │   │
│  │       │   │  │       │ │       │ │       │ │ ENTER │   │   │     (1.5U)      │   │
│  └───────┘   │  └───────┘ └───────┘ └───────┘ │  (2U) │   │   └─────────────────┘   │
│              │                                │       │   │                         │
│  ┌───────┐   │  ┌─────────────────┐ ┌───────┐ │       │   │                         │
│  │       │   │  │        0        │ │   .   │ └───────┘   │                         │
│  │       │   │  │      (2U)       │ │       │             │                         │
│  └───────┘   │  └─────────────────┘ └───────┘             │                         │
│              │                                            │                         │
│              │          ┌───────────────────┐             │                         │
│              │          │   PRO MICRO       │             │                         │
│              │          │      (MCU)        │             │                         │
│              │          │   18mm x 33mm     │             │                         │
│              │          └───────────────────┘             │                         │
└──────────────┴────────────────────────────────────────────┴─────────────────────────┘
```

## Electrical Connection Matrix

### Column Networks (8 total):
| Column | Pro Micro Pin | Connected Keys |
|--------|---------------|----------------|
| col0 | P0 | NumLock, 7, 4, 1, 0 |
| col1 | P1 | /, 8, 5, 2 |
| col2 | P3 | *, 9, 6, 3, . |
| col3 | P4 | -, +, Enter |
| col_left | P5 | Nav column (5 keys) |
| col_thumb | P4 | Thumb key |
| col_enc_left | P7 | Left encoder |
| col_enc_right | P8 | Right encoder |
| col_enc_bottom | P9 | Bottom encoder |

### Row Networks (9 total):
| Row | Pro Micro Pin | Connected Keys |
|-----|---------------|----------------|
| row0 | P10 | Top row (NumLock, /, *, -, nav_top) |
| row1 | P14 | 7, 8, 9, +, nav |
| row2 | P15 | 4, 5, 6, +, nav |
| row3 | P16 | 1, 2, 3, Enter, nav |
| row4 | P21 | 0, ., Enter, nav |
| row_thumb | P6 | Thumb key |
| row_enc_left | P18 | Left encoder |
| row_enc_right | P19 | Right encoder |
| row_enc_bottom | P20 | Bottom encoder |

## Special Connections

### Encoders (Rotary + Switch functionality):
| Component | Column Pin | Row Pin | Rotary A Pin | Rotary B Pin | Common |
|-----------|------------|---------|--------------|--------------|--------|
| Left Encoder | P7 | P18 | encoder_left_a | encoder_left_b | GND |
| Right Encoder | P8 | P19 | encoder_right_a | encoder_right_b | GND |
| Bottom Encoder | P9 | P20 | encoder_bottom_a | encoder_bottom_b | GND |

### OLED Display (I2C):
| Signal | Pro Micro Pin | Description |
|--------|---------------|-------------|
| SDA | P3 | I2C Data Line |
| SCL | P2 | I2C Clock Line |
| VCC | VCC | Power (3.3V/5V) |
| GND | GND | Ground |

### Diode Configuration:
- Every key switch has an anti-ghosting diode
- Diode direction: `{{colrow}}` → `{{row_net}}`
- Prevents current backflow during matrix scanning

## Matrix Scanning Logic

The keyboard uses a **hybrid matrix approach**:

### Shared Matrix Section:
- **Main numpad (4 columns × 5 rows)** + **Nav column (1 column × 5 rows)**
- Share the same 5 row lines (row0-row4)
- Efficient use of pins for the bulk of the keys
- Standard matrix scanning: drive columns sequentially, read all rows

### Individual Component Section:
- **3 Encoders**: Each has dedicated column/row pair
- **1 Thumb key**: Has dedicated column/row pair
- Allows independent control without matrix conflicts

### Pin Usage Summary:
- **Total pins used**: 17 (8 columns + 9 rows)
- **Total components**: 26 keys + 3 encoders + 1 OLED
- **Matrix efficiency**: Optimized for Pro Micro's limited pin count
- **N-key rollover**: Full NKRO capability with diode protection

## Key Layout Details

### Standard Numpad Keys (1U):
- NumLock, /, *, -, 7, 8, 9, 4, 5, 6, 1, 2, 3, .

### Special Size Keys:
- **0 key**: 2U wide (spans 2 standard key widths)
- **+ key**: 2U tall (spans 2 standard key heights, row1-row2)
- **Enter key**: 2U tall (spans 2 standard key heights, row3-row4)
- **Thumb key**: 1.5U wide

### Navigation Column:
- 5 keys in vertical column to the left of main numpad
- Shares row networks with main numpad for efficiency

### Additional Components:
- **3 Rotary Encoders**: Positioned to the right, each with push-button switch
- **OLED Screen**: 32×16mm display above encoders
- **Pro Micro MCU**: Positioned below center of numpad for optimal trace routing

## Physical Dimensions

### Key Spacing:
- **kx**: 19.05mm (center-to-center horizontal)
- **ky**: 19.05mm (center-to-center vertical)
- **Key cap size**: 18×18mm

### Component Distances:
- **Nav to Numpad**: 1.25 × kx (23.81mm)
- **Numpad to MCU**: 1.5 × ky (28.58mm)
- **Numpad to Screen**: 1.5 × ky (28.58mm)

This design provides a compact, efficient numpad keyboard with additional functionality through encoders and display, while maintaining compatibility with standard MX switches and keycaps.
