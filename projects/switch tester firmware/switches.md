# Switch Tester Inventory — YMDK ID75

<!-- vil-tool: terminator=enter  include-force=true  auto-sort=true -->

Placeholder inventory (example switches from the planning session). Replace
with the real collection as it gets catalogued. Rules:

- `Pos` is the **full matrix position** `row,col` (top-left = `0,0`,
  bottom-right = `4,14`). Every position is fully self-describing, so switch
  types can be mixed anywhere — the `## Row N` sections are just organization.
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
| 0,11 | Outemu Blue             | Clicky |        50 |       |
| 0,12 | Kailh Pro Light Green   | Clicky |        50 |       |
| 0,13 | Kailh Box White         | Clicky |        45 |       |
| 0,14 | Kailh Box White Clone   | Clicky |        45 |       |

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
| 1,12 | Virtue                  | Tactile |        63 |       |
| 1,13 | Boba U4T                | Tactile |        62 |       |
| 1,14 | Durock Sunflower        | Tactile |        62 |       |

## Row 2 — Tactile

| Pos  | Switch                     | Type    | Force (g) | Notes |
|------|----------------------------|---------|----------:|-------|
| 2,0  | Boba U4 Silent             | Tactile |        62 |       |
| 2,1  | Gazzew U4Tx                | Tactile |        62 |       |
| 2,2  | Ergo Clear                 | Tactile |        62 |       |
| 2,3  | Pewter                     | Tactile |        60 |       |
| 2,4  | Feker Holy Panda           | Tactile |        60 |       |
| 2,5  | Coffee Chip                | Tactile |        55 |       |
| 2,6  | KTT Mallo                  | Tactile |        55 |       |
| 2,7  | Akko CS Lavender Purple    | Tactile |        50 |       |
| 2,8  | Akko CS Sponge             | Tactile |        48 |       |
| 2,9  | Cherry MX Brown            | Tactile |        45 |       |
| 2,10 | Gateron Brown              | Tactile |        45 |       |
| 2,11 | Outemu Brown               | Tactile |        45 |       |
| 2,12 | Gateron Low Profile Brown  | Tactile |        45 |       |
| 2,13 | TTC Bluish White           | Tactile |        42 |       |
| 2,14 | TTC Gold Pink              | Tactile |        37 |       |

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
| 3,12 | Aqua King            | Linear |        55 |       |
| 3,13 | Gateron Milky Yellow | Linear |        50 |       |
| 3,14 | WS Morandi           | Linear |        50 |       |

## Row 4 — Linear

| Pos  | Switch                 | Type   | Force (g) | Notes |
|------|------------------------|--------|----------:|-------|
| 4,0  | Gateron Yellow         | Linear |        50 |       |
| 4,1  | Haimu Whisper          | Linear |        48 |       |
| 4,2  | Outemu Red             | Linear |        46 |       |
| 4,3  | Cherry MX Red          | Linear |        45 |       |
| 4,4  | Gateron CJ             | Linear |        45 |       |
| 4,5  | KTT Strawberry         | Linear |        45 |       |
| 4,6  | Cherry MX Silent Red   | Linear |        45 |       |
| 4,7  | Gateron Red            | Linear |        45 |       |
| 4,8  | TTC Ace                | Linear |        45 |       |
| 4,9  | Gateron Pro Red        | Linear |        45 |       |
| 4,10 | Cherry MX Speed Silver | Linear |        45 |       |
| 4,11 | Akko CS Jelly Pink     | Linear |        45 |       |
| 4,12 | Akko CS Rose Red       | Linear |        43 |       |
| 4,13 | Kailh Speed Silver     | Linear |        40 |       |
| 4,14 | RESERVED               |        |           | TG(3) exit key — bottom-right |