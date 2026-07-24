# Switch Tester Inventory — Custom RP2040 Lumberjack-style (5×12)

<!-- vil-tool: terminator=enter  include-force=true  auto-sort=true -->

Placeholder inventory (example switches trimmed to 60-key layout). Replace
with the real collection as it gets catalogued. Rules:

- `Pos` is the **full matrix position** `row,col` (top-left = `0,0`,
  bottom-right = `4,11`). Macro index = `row × 12 + col`.
- `Type` is **explicit for every switch** (Clicky / Tactile / Linear).
  One-type-per-row is only the starting guideline, not a requirement.
- `RESERVED` in the Switch column = position skipped (layer-exit key etc.).
- With `auto-sort=true`, switches within each section are re-seated across
  that section's positions heaviest → lightest (reserved positions stay put).
  Set `auto-sort=false` to make the `Pos` column authoritative instead.

## Row 0 — Clicky

| Pos  | Switch                  | Type   | Force (g) | Notes |
|------|-------------------------|--------|----------:|-------|
| 0,0  | Cherry MX Green         | Clicky |        80 |       |
| 0,1  | Kailh Box Navy          | Clicky |        75 |       |
| 0,2  | Kailh Box Jade          | Clicky |        70 |       |
| 0,3  | Kailh Box Noble Yellow  | Clicky |        65 |       |
| 0,4  | NovelKeys Sherbet       | Clicky |        65 |       |
| 0,5  | Cherry MX White         | Clicky |        55 |       |
| 0,6  | Kailh Box Pink          | Clicky |        55 |       |
| 0,7  | Gateron Blue            | Clicky |        55 |       |
| 0,8  | Cherry MX Blue          | Clicky |        50 |       |
| 0,9  | Kailh Speed Gold        | Clicky |        50 |       |
| 0,10 | Kailh Speed Bronze      | Clicky |        50 |       |
| 0,11 | Kailh Box White         | Clicky |        45 |       |

## Row 1 — Tactile

| Pos  | Switch                  | Type    | Force (g) | Notes |
|------|-------------------------|---------|----------:|-------|
| 1,0  | Zealio V2 78g           | Tactile |        78 |       |
| 1,1  | Tungsten                | Tactile |        68 |       |
| 1,2  | Holy Panda              | Tactile |        67 |       |
| 1,3  | Durock T1               | Tactile |        67 |       |
| 1,4  | Glorious Panda          | Tactile |        67 |       |
| 1,5  | Zealio V2 67g           | Tactile |        67 |       |
| 1,6  | SP Star Meteor White    | Tactile |        67 |       |
| 1,7  | Cherry MX Clear         | Tactile |        65 |       |
| 1,8  | Anubis                  | Tactile |        65 |       |
| 1,9  | Azure Dragon            | Tactile |        63 |       |
| 1,10 | Moyu Black              | Tactile |        63 |       |
| 1,11 | Wuque Studio Aurora     | Tactile |        63 |       |

## Row 2 — Tactile

| Pos  | Switch                     | Type    | Force (g) | Notes |
|------|----------------------------|---------|----------:|-------|
| 2,0  | Virtue                     | Tactile |        63 |       |
| 2,1  | Boba U4T                   | Tactile |        62 |       |
| 2,2  | Durock Sunflower           | Tactile |        62 |       |
| 2,3  | Boba U4 Silent             | Tactile |        62 |       |
| 2,4  | Gazzew U4Tx                | Tactile |        62 |       |
| 2,5  | Ergo Clear                 | Tactile |        62 |       |
| 2,6  | Pewter                     | Tactile |        60 |       |
| 2,7  | Feker Holy Panda           | Tactile |        60 |       |
| 2,8  | Coffee Chip                | Tactile |        55 |       |
| 2,9  | KTT Mallo                  | Tactile |        55 |       |
| 2,10 | Akko CS Lavender Purple    | Tactile |        50 |       |
| 2,11 | Cherry MX Brown            | Tactile |        45 |       |

## Row 3 — Linear

| Pos  | Switch               | Type   | Force (g) | Notes |
|------|----------------------|--------|----------:|-------|
| 3,0  | Tangerine 67g        | Linear |        67 |       |
| 3,1  | Tealio V2            | Linear |        67 |       |
| 3,2  | Lavender             | Linear |        65 |       |
| 3,3  | JWK Black            | Linear |        63 |       |
| 3,4  | Durock L7 62g        | Linear |        62 |       |
| 3,5  | Alpaca V2            | Linear |        62 |       |
| 3,6  | Banana Split         | Linear |        62 |       |
| 3,7  | Cherry MX Black      | Linear |        60 |       |
| 3,8  | H1                   | Linear |        60 |       |
| 3,9  | Black Ink V2         | Linear |        60 |       |
| 3,10 | NK Cream             | Linear |        55 |       |
| 3,11 | Gateron Oil King     | Linear |        55 |       |

## Row 4 — Linear

| Pos  | Switch                 | Type   | Force (g) | Notes |
|------|------------------------|--------|----------:|-------|
| 4,0  | Aqua King              | Linear |        55 |       |
| 4,1  | Gateron Milky Yellow   | Linear |        50 |       |
| 4,2  | WS Morandi             | Linear |        50 |       |
| 4,3  | Gateron Yellow         | Linear |        50 |       |
| 4,4  | Haimu Whisper          | Linear |        48 |       |
| 4,5  | Outemu Red             | Linear |        46 |       |
| 4,6  | Cherry MX Red          | Linear |        45 |       |
| 4,7  | Gateron CJ             | Linear |        45 |       |
| 4,8  | KTT Strawberry         | Linear |        45 |       |
| 4,9  | Cherry MX Silent Red   | Linear |        45 |       |
| 4,10 | Kailh Speed Silver     | Linear |        40 |       |
| 4,11 | RESERVED               |        |           | TG(3) exit key — bottom-right |
