# 5x3 Matrix Layout

## Expected Matrix Positions

| Row/Col | Col 2 | Col 1 | Col 0 |
| ------- | ----- | ----- | ----- |
| Row 4   | [4,2] | [4,1] | [4,0] |
| Row 3   | [3,2] | [3,1] | [3,0] |
| Row 2   | [2,2] | [2,1] | [2,0] |
| Row 1   | [1,2] | [1,1] | [1,0] |
| Row 0   | [0,2] | [0,1] | [0,0] |

## Actual reported Matrix Positions

| Col/Row | Row 2 | Row 1 | Row 0 |
| ------- | ----- | ----- | ----- |
| Col 4   | [?,?] | [?,?] | [?,?] |
| Col 3   | [?,?] | [?,?] | [?,?] |
| Col 2   | [2,2] | [2,1] | [2,0] |
| Col 1   | [1,2] | [1,1] | [1,0] |
| Col 0   | [0,2] | [0,1] | [0,0] |


## Pin Connections

| Row/Col     | Col 2 (B2) | Col 1 (B1) | Col 0 (B0) |
| ----------- | ---------- | ---------- | ---------- |
| Row 4 (A0)  | KC_F2      | KC_C       | KC_I       |
| Row 3 (A1)  | KC_C       | KC_2       | KC_F1      |
| Row 2 (B14) | KC_9       | KC_P       | KC_B       |
| Row 1 (B15) | KC_1       | KC_V       | KC_8       |
| Row 0 (B9)  | KC_M       | KC_A       | KC_0       |
