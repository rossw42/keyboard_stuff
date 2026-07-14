# Mining Round 2: Vendor Deep-Dive + Unverified Lead Resolution

---

## Vendor catalog deep-dive

### switchcouture.com — DEFUNCT
Domain redirects to parked/spam site. Wayback catalog check: they sold acrylic **cases** for known TH PCBs (Discipline, Mysterium) plus their own "ElectroType60/16" acrylic boards (standard PCBs, no TH evidence, no GitHub). **No new TH kits.**

### keyhive.xyz (Squarespace catalog scraped)
- **Nightmare** — "pseudo-TMO50 ... with through hole components", Pro Micro. QMK `keyboards/nightmare`, maintainer cfbender. Hardware: https://github.com/cfbender/keyboards/tree/master/nightmare → **already starred via cfbender/keyboards**. TH-adjacent (Pro Micro).
- **May Pad** — "through hole kit using a pro micro footprint and through hole diodes", 20-key numpad by u/reggatronics. QMK `keyboards/keyhive/maypad` (Cody Bender = cfbender) → **already starred via cfbender/keyboards**. TH-adjacent.
- Lattice60 (known). No other TH kits.

### mechwild.com
- **Mercutio** (known, TH w/ ATmega328P... actually kit uses discrete design) — flagship TH board
- **OBE (Orange Boy Ergo)** — TH-adjacent (Blackpill module)
- MurphPad, Mokulua, BDE, PuckBuddy — module-controller boards, **not TH**

### cannonkeys.com
- Practice60 / Practice65 / Stacked line — Blue Pill-based solder practice. **NOT discrete-TH.**

### Clawsome Boards (Etsy)
- **FinnGus** (cat-shaped Alice) and **GameBuddy** (gamepad) — TH kits per GB posts; **no GitHub presence found**.

### nullbits.co (gh repo list nullbitsco)
- **Nibble** (65%) and **Tidbit** (numpad) — TH kits (known, repos catalogued)
- SNAP (split 75%) — Bit-C module + mostly SMD → TH-adjacent at best
- Scramble — 40% w/ RP2040 SMD → not TH

### p3dstore.com
- Carried Jabberwocky (known, TH). No other new TH kits identified.

---

## Unverified lead verdicts (README/schematic inspection)

| Lead | Verdict | Evidence |
|---|---|---|
| ianelsbree/wik75 | **NOT TH** | Schematic: ATmega32U4-AU TQFP-44 (SMD) + SMD USB-C; only diodes are THT |
| atcheng2/65-Percent-Keyboard | **NOT TH** | README claims ATmega32A+V-USB but schematic uses ATmega32A-A TQFP-44 (SMD) |
| CityRunner/nullwing-keyboard | TH-adjacent | THT diodes + nice!nano v2 module, no discrete MCU |
| jsmercier/panama-keyboard | **CONFIRMED TH** ✅ | ATmega32A-PU DIP-40 socket, THT DO-35 diodes, USB-C (GCT USB4085), USBaspLoader + QMK |
| zzsmoky/EygptBar-70 | **CONFIRMED TH (mostly)** ✅ | ATmega328P-PU DIP-28, THT diodes/resistors, HC-49 crystals; USB-hub subsection is SMD (CH334R etc.) |
| ScatteredDrifter/Quasar-67 | Unbuilt concept | Lumberjack-inspired PCB for KBD67-lite; prototypes never ordered; likely TH design (Lumberjack lineage) but unverified/incomplete |
| casio59 (mrninhvn) | UNRESOLVABLE | Repo deleted/renamed; not found in user's repo list |
| keyboard60-throughole (davidgraeff) | UNRESOLVABLE | Repo deleted; no keyboard repos on account |
| Wanda (ianfhunter) | UNRESOLVABLE | Not in user's public repos |
| Avlo44 | UNRESOLVABLE | No repo found via gh or Wayback |
| ErgoMorph55 | UNRESOLVABLE | No repo found |
| KP24 | UNRESOLVABLE | IC-only Reddit post, never released |
| Berm | UNRESOLVABLE | Personal one-off, no repo posted |
| J73K (MakerJake01/J73K_keyboard) | TH-adjacent | DIY board; controller is a module per README |
| m-lego M65 (gitlab) | **NOT strict TH** | Revs 9–11: Seeed XIAO RP2040/nRF52840 SMD module + DIP shift registers |
| Aardvark (40% club, di0ib) | **CONFIRMED TH** ✅ | ATmega328P DIP-28 socket, V-USB, 1n4148 THT, ceramic resonator, USBasp bootloader, APA106 TH RGB. No GitHub repo; files on 40percent.club blog |
| Treadstone48 (marksard) | NOT TH | Pro Micro, no TH claim in readme |
| Orange Boy Ergo (MechWild OBE) | TH-adjacent | STM32 Blackpill module |

---

## Net-new confirmed TH from Round 2

| Keyboard | Link | Notes |
|---|---|---|
| **Panama** | https://github.com/jsmercier/panama-keyboard | ATmega32A-PU DIP-40, USB-C, USBaspLoader — upgrade from "unverified" to confirmed |
| **EgyptBar-70** | https://github.com/zzsmoky/EygptBar-70 | ATmega328P-PU DIP, 5x14 ortho w/ built-in USB hub (hub section SMD) |
| **Aardvark** | https://www.40percent.club/2020/08/the-aardvark.html | 3x12 ortho, ATmega328P DIP + V-USB (no GitHub repo) |

## Downgraded / removed from candidate list
- wik75 → NOT TH (SMD ATmega32U4)
- 65-Percent-Keyboard → NOT TH (SMD ATmega32A)
- M65, J73K, nullwing, OBE → TH-adjacent
- Practice60/65, Treadstone48, MurphPad, SNAP, Scramble → not TH