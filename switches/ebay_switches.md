# Switch Collection Inventory

<!-- vil-tool: terminator=enter  include-force=true  auto-sort=true -->

Switch collection inventory. Same rules as the switch tester inventory:

- `Pos` is the **full matrix position** `row,col` (top-left = `0,0`,
  bottom-right = `4,14`). Every position is fully self-describing, so switch
  types can be mixed anywhere — the `## Row N` sections are just organization.
- `Type` is **explicit for every switch** (Clicky / Tactile / Linear).
  One-type-per-row is only the starting guideline, not a requirement.
- `RESERVED` in the Switch column = position skipped (layer-exit key etc.).
- With `auto-sort=true`, switches within each section are re-seated across
  that section's positions heaviest → lightest (reserved positions stay put).
  Set `auto-sort=false` to make the `Pos` column authoritative instead.
- Force values are **estimates from published specs** — verify against the
  actual switches. Blank force = unknown, marked `TBD` in Notes.

## Row 0 — Clicky & Tactile

| Pos  | Switch                      | Type    | Force (g) | Notes |
|------|-----------------------------|---------|----------:|-------|
| 0,0  | Outemu Blues                | Clicky  |        50 |       |
| 0,1  | Kailh Royals                | Tactile |        75 | Box Royal |
| 0,2  | Zealios 68g                 | Tactile |        68 |       |
| 0,3  | JWK T1                      | Tactile |        67 |       |
| 0,4  | Durock T1                   | Tactile |        67 |       |
| 0,5  | Durock Amber T1             | Tactile |        67 |       |
| 0,6  | Yok Trash Pandas            | Tactile |        67 |       |
| 0,7  | Wuque Studio Heavy Tactiles | Tactile |        65 | verify weight |
| 0,8  | Neapolitan Ice Cream        | Tactile |        63 |       |
| 0,9  | Zealios 62g                 | Tactile |        62 |       |
| 0,10 | Durock Koalas               | Tactile |        62 | T1 variant |
| 0,11 | Drop Halos                  | Tactile |        60 | Halo True/Clear |
| 0,12 | Gateron Quinns              | Tactile |           | TBD — verify type/weight |
| 0,13 | CK x Haimu Thistles         | Tactile |           | silent tactile — TBD weight |
| 0,14 | Akko Lavenders              | Tactile |        50 | CS Lavender Purple |

## Row 1 — Tactile & Linear

| Pos  | Switch                        | Type    | Force (g) | Notes |
|------|-------------------------------|---------|----------:|-------|
| 1,0  | Kailh Polias                  | Tactile |        50 | verify weight |
| 1,1  | Akko Creamy Blues             | Tactile |        45 | V3 Cream Blue Pro |
| 1,2  | Akko Creamy Purple Pro        | Tactile |        45 | V3 Cream Purple Pro |
| 1,3  | Outemu Brown                  | Tactile |        45 |       |
| 1,4  | HMX Firecrackers              | Linear  |        58 |       |
| 1,5  | Sillyworks x HMX Waverider V2 | Linear  |        50 |       |
| 1,6  | Wingtree Golden Apples V2     | Linear  |           | TBD weight |
| 1,7  | Wingtree Yunies               | Linear  |           | TBD weight |
| 1,8  | BSUN Oceans                   | Linear  |           | TBD weight |
| 1,9  | KTT Baby Blues                | Linear  |           | TBD weight |
| 1,10 | Haimu Mints                   | Linear  |           | possibly silent — TBD |
| 1,11 | Keebfront Dooms               |         |           | TBD — verify type/weight |
| 1,12 | Gateron Type-R                |         |           | TBD — verify type/weight |
| 1,13 | LTC Jerrzi                    |         |           | TBD — verify type/weight |
| 1,14 | RESERVED                      |         |           |       |
