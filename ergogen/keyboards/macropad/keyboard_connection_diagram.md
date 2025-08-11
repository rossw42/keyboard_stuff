# Keyboard_numpad Connection Diagram

Analysis of the keyboard_numpad ergogen configuration file showing physical layout and electrical connections.

## Physical Layout Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                KEYBOARD_NUMPAD                                      │
├──────────────┬────────────────────────────────────────────┬─────────────────────────┤
│   NAV        │             NUMPAD GRID                │    RIGHT SECTION        │
│  COLUMN      │                                            │                         │
│              │                                            │                         │
│              │                                            │                         │
│              │                                            │                         │
│              │                                            │                         │
│              │                                            │                         │
│              │                                            │                         │
│              │                                            │                         │
│              │                                            │                         │
│              │          ┌───────────────────┐             │                         │
│              │          │   PRO MICRO       │             │                         │
│              │          │      (MCU)        │             │                         │
│              │          │   18mm x 33mm     │             │                         │
│              │          └───────────────────┘             │                         │
└──────────────┴────────────────────────────────────────────┴─────────────────────────┘
```

## Electrical Connection Matrix

### Column Networks:
| Column | Pro Micro Pin | Connected Keys |
|--------|---------------|----------------|
| col0 | P0 | NumLock, 7, 4, 1, 0 |
| col1 | P1 | /, 8, 5, 2 |
| col_thumb | P4 | thumb bottom |
| col_left | P5 |  |
| col_enc_left | P7 | encoder left |
| col_enc_right | P8 | encoder right |
| col_enc_bottom | P9 | encoder bottom |

### Row Networks:
| Row | Pro Micro Pin | Connected Keys |
|-----|---------------|----------------|
| row_thumb | P6 | thumb bottom |
| row0 | P10 | NumLock, /, *, - |
| row1 | P14 | 7, 8, 9, + |
| row2 | P15 | 4, 5, 6 |
| row3 | P16 | 1, 2, 3, Enter |
| row4 | P21 | 0, . |
| row_enc_left | P18 | encoder left |
| row_enc_right | P19 | encoder right |
| row_enc_bottom | P20 | encoder bottom |

## Special Connections

### Encoders (Rotary + Switch functionality):
| Component | Column Pin | Row Pin | Rotary A Pin | Rotary B Pin | Common |
|-----------|------------|---------|--------------|--------------|--------|
| Encoder_left | N/A | N/A | encoder_left_a | encoder_left_b | GND |
| Encoder_right | N/A | N/A | encoder_right_a | encoder_right_b | GND |
| Encoder_bottom | N/A | N/A | encoder_bottom_a | encoder_bottom_b | GND |

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

### Matrix Section:
- **Total matrix coverage**: 7 columns × 9 rows
- Efficient use of pins for the bulk of the keys
- Standard matrix scanning: drive columns sequentially, read all rows

### Pin Usage Summary:
- **Total pins used**: 16 (7 columns + 9 rows)
- **Total components**: 23 keys + encoders + displays
- **Matrix efficiency**: Optimized for Pro Micro's limited pin count
- **N-key rollover**: Full NKRO capability with diode protection

## Key Layout Details

### Standard Keys (1U):
- NumLock, 7, 4, 1, /, 8, 5, 2, *, 9, 6, 3, ., -, encoder left, encoder right, encoder bottom

### Special Size Keys:
- **0: 2*capx + kx × capy**
- **+: capx × 2*capy + ky**
- **Enter: capx × 2*capy + ky**
- **oled screen: 32 × 16**
- **thumb bottom: 1.5*capx × capy**
- **mcu: 18 × 33**

### Additional Components:
- **3 Rotary Encoders**: Each with push-button switch functionality
- **OLED Screen**: Display for status and information
- **Pro Micro MCU**: Microcontroller for optimal trace routing

## Physical Dimensions

### Key Spacing:
- **kx**: 19.05mm (center-to-center horizontal)
- **ky**: 19.05mm (center-to-center vertical)
- **Key cap size**: 18×18mm

### Component Distances:
- **Main To Nav**: 1.25*kx
- **Main To Mcu**: 1.5*ky
- **Main To Screen**: 1.5*ky

This design provides a compact, efficient keyboard_numpad with 7 columns and 9 rows, while maintaining compatibility with standard MX switches and keycaps.

