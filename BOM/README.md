# Multi-Keyboard BOM Sourcing — Overview

**Created:** 2026-07-26
**Boards covered:** Discipline 65% (×2 builds), Lattice60, Absinthe (rev4), DumbPad ("combo" variant)

> **2026-08-25 update:** Rosalina and Mercutio parts have been **purchased** — their line items were removed from both consolidated CSVs (quantities of shared parts adjusted down accordingly). Their individual BOM files (`rosalina_bom.csv`, `mercutio_bom.csv`) are kept for reference.

This folder contains an individual BOM CSV + sourcing notes for each keyboard being built, plus a single **consolidated CSV** meant to be uploaded to [octopart.com](https://octopart.com)'s BOM tool for pricing/availability across all builds at once.

**Two consolidated CSVs exist:**
- `consolidated_bom_octopart.csv` — the original, unmerged consolidation (kept as-is/unedited for reference).
- `consolidated_bom_octopart_deduped.csv` — **use this one for Octopart / inventory tracking.** Rows for the identical physical part that appeared multiple times (e.g. the 6x6mm tactile pushbutton) have been merged into a single row. Also separates truly-different parts that share a similar description (e.g. 1.5K resistors at different wattages/tolerances) into distinct rows so they aren't accidentally merged.

### Inventory workflow (parts you already have on hand)

This file has three quantity columns to support doing an inventory pass before ordering:
- **`Total Qty Needed`** — the full quantity required across all 5 keyboard builds (do not edit this column casually — it reflects the sourced/estimated BOM data).
- **`On Hand Qty`** — currently defaulted to `0`. Edit this column with how many of each part you already have in your parts bins.
- **`Qty to Order`** — currently mirrors `Total Qty Needed` (since `On Hand Qty` starts at 0). **After you fill in `On Hand Qty`, manually update `Qty to Order` to `Total Qty Needed − On Hand Qty`** (this is a plain CSV, not a spreadsheet with live formulas — if you open it in Excel/Google Sheets, you can convert this column to a real formula like `=E2-F2` for auto-calculation).

Only upload the **`Qty to Order`** column's values to Octopart once you've done your inventory pass, so you don't over-order parts you already have.

## Files

| Keyboard | CSV | Notes doc | Confidence |
|---|---|---|---|
| Discipline 65% (×2 units) | `discipline65_bom.csv` | `discipline65_bom_notes.md` | **High** — official cftkb build guide + Octopart-verified MPNs |
| Lattice60 | `lattice60_bom.csv` | `lattice60_bom_notes.md` | **High** — official QMK repo + prior Octopart-corrected CSV in this repo, most MPNs confirmed |
| Mercutio | `mercutio_bom.csv` | `mercutio_bom_notes.md` | **Medium** — official MechWild build guide gives exact qty/refdes, but MechWild doesn't publish component MPNs (proprietary kit; bought pre-sourced, not part-by-part) |
| Absinthe (rev4) | `absinthe_bom.csv` | N/A | **Medium** — ⚠️ **No "rev4" of Absinthe could be found anywhere** (GitHub, KeyHive archives, reddit, geekhack, or the official KeyHive imgur build guide "So you bought yourself an Absinthe..."). Only one Absinthe PCB revision is documented. The official build guide confirmed the PCB uses socketed 2.54mm headers for a Pro Micro/Elite-C daughterboard (not soldered directly), SMD-or-THT diode footprints, and a 5-pin rotary encoder — verify rev4 claim with the seller before ordering. |
| Rosalina | `rosalina_bom.csv` | N/A | **High** — Rosalina's firmware readme states it uses the same BOM as `peej/lumberjack-keyboard`. This CSV contains the official, verbatim BOM.md from that repo (confirmed via direct GitHub fetch), including the designer's own published Octopart BOM tool link. |
| DumbPad ("combo" variant) | `dumbpad_bom.csv` | N/A | **High** — official imchipwood/dumbpad GitHub repo, `combo/README.md` Bill of Materials section fetched directly. Includes all optional parts (2nd encoder, reset button, 3 status LEDs + resistors) explicitly marked. Note: repo has 6 hardware variants total (combo, combo_teensy, combo_oled, combo_low_profile_oled, reversible, hotswap_rgb) — this BOM is specifically for the "combo" variant per your confirmation. |

## Key uncertainties to resolve before ordering

1. **Absinthe "rev4"** — could not be confirmed to exist, even after reviewing the official KeyHive build guide (imgur album "So you bought yourself an Absinthe..."). That guide confirmed: socketed Pro Micro/Elite-C headers (not soldered), diode footprints supporting both SMD and through-hole, and a 5-pin rotary encoder — but no revision/version markings. Double check with the designer (cfbender) / KeyHive whether you actually have a rev4 PCB and if its BOM differs.
2. **Rosalina** — this is a personal commission board built on the `peej/lumberjack-keyboard` PCB design (per the Rosalina firmware readme, "uses the same BOM as Lumberjack"). The BOM here is the official, confirmed Lumberjack BOM.md — ATmega328P-PU, 60x 1N4148 diodes, 16MHz crystal, USB-C, etc. The designer even published an [Octopart BOM tool link](https://octopart.com/bom-tool/0k8Ap0AF) for it directly.
3. **Mercutio** — MechWild sells this as a complete kit with parts already included; the BOM here is for reference/replacement-parts purposes. If you're ordering a fresh kit, you likely don't need to source these individually — buy the kit from mechwild.com. MPNs for the kit-specific kitted parts (resistors, caps, diodes, fuse) are not published by MechWild, so exact MPNs are marked "verify" in the CSV — generic equivalents are suggested instead.
4. **Discipline 65% quantities are already doubled (×2)** in `discipline65_bom.csv` to cover both builds you're planning.
5. **Switches, keycaps, and stabilizers are NOT priced via Octopart** (Octopart is for electronic components) — they're listed for your own tracking but you'll want to source those from a keyboard vendor (KBDfans, NovelKeys, etc.), not Octopart.
6. **DumbPad optional parts** — the "combo" variant's 2nd EC11 encoder, reset button, and 3x status-LED+resistor set are all optional per the official BOM. Rows for these are included in the consolidated CSV but flagged — remove/zero them out if you don't plan to populate those features.

## Next steps

1. Review each individual CSV/notes doc, fill in your chosen switch count/layout/stabilizer choices where marked TBD.
2. Upload `consolidated_bom_octopart_deduped.csv` to https://octopart.com/bom-tool for pricing & distributor matching.
3. Cross-check Octopart's suggested matches against the "Manufacturer/MPN" columns here — some rows are marked `VERIFY` and will need manual matching in Octopart's UI.
