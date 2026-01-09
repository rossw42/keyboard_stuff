/* Copyright 2022 Jose Pablo Ramirez <jp.ramangulo@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#pragma once

/* OLED SPI Defines */
#define OLED_DISPLAY_128X64
#define OLED_IC OLED_IC_SSD1306

/* OLED SPI Pins */
#define OLED_DC_PIN A9
#define OLED_CS_PIN A10

#define MATRIX_ROWS 4
#define MATRIX_COLS 3

/* Shift OLED columns by 2 pixels */
#define OLED_COLUMN_OFFSET 2

/* Divisor for OLED 
#define OLED_SPI_DIVISOR 4 */

#define ENCODER_A_PINS { A2, B7 }
#define ENCODER_B_PINS { A1, B6 }
#define ENCODER_RESOLUTIONS { 10, 100 }
