# Through-Hole Keyboard Research: QMK Firmware Database

Method: `git grep -il "through.hole"` across `keyboards/*/readme.md` in the local QMK repo (D:\GitHub2\qmk_firmware), plus reading each readme for designer/hardware links. Cross-referenced with atmega32a/atmega328p usage (classic discrete-MCU TH recipe).

Excluded (already known): plaid, tartan (found elsewhere), discipline, discipad, mysterium, romeo, numdiscipline, punk75, torn, axon, basketweave, lumberjack, rosaline, lck75, lagom, litl, barleycorn, gingham, seigaiha, plaid_pad, herringbone, orthocode, redherring, framework, late9, etc. where already captured in other research files.

---

## Fully through-hole (discrete TH MCU: ATmega32A / ATmega328P)

| Keyboard | QMK Path | Designer | Hardware Link | Evidence |
|---|---|---|---|---|
| TH1800 | keyboards/mechlovin/th1800 | Team Mechlovin | https://github.com/mechlovin/PCB/tree/master/1800-Compact | "atmega32a, through hole component, 1800 compact, open source" |
| Resume1800 | keyboards/crimsonkeyboards/resume1800 | CrimsonKeyboards (github.com/DeeDesired) | not located | "1800 compact built with solely through-hole components", ATmega32A |
| HACKBOARD | keyboards/rot13labs/hackboard | c0ldbru (rot13labs) | https://rot13labs.com | "TKL for hackers based on the mysterium platform", ATmega32A |
| Mine | keyboards/adpenrose/mine | Arturo Avila (github.com/ADPenrose) | https://github.com/ADPenrose | "1800 alice, assembled only with THT components, solenoid + chunky encoder" |
| Argyle | keyboards/argyle | Yiancar | https://prototypist.net/ | "60 percent through hole keyboard with RGB", ATmega328p + V-USB |
| Stoutgat v1 | keyboards/tkw/stoutgat/v1 | Thys de Wet (vattern) | https://github.com/vattern/stoutgat | "ISO through hole component 65% with dual encoders, ATmega32A, inspired by cftkb Discipline" |
| Rartland | keyboards/rart/rartland | Alabahuy | private GB | "65% assembled with only through hole components", ATmega32A, OLED + encoder |
| SKErgo | keyboards/skergo | Keyz.io (C1intMason) | https://keyz.io | "ergonomic layout keyboard with a through-hole component design", ATmega32A |
| Chidori | keyboards/kagizaraya/chidori | ka2hiro (@kagizaraya) | Twitter @kagizaraya | "split keyboard made with only through-hole components", ATmega328P per half |
| Lattice60 | keyboards/keyhive/lattice60 | emdarcher | https://keyhive.xyz/ | "HHKB layout keyboard using only through-hole components" |
| Mini Ashen 40 | keyboards/mechanickeys/miniashen40 | MechanicKeys | ? | "40% ... full assembly with only through hole components" |
| Mercutio | keyboards/mechwild/mercutio | Kyle McCreery (MechWild) | https://mechwild.com/product/mercutio/ | "through-hole 40% keyboard kit featuring an encoder and oled display" |
| Jabberwocky | keyboards/nopunin10did/jabberwocky | nopunin10did | ? | full-size columnar-stagger Alice TH DIY kit |
| Red Herring | keyboards/dcpedit/redherring | dcpedit | https://github.com/dcpedit/redherring | unibody ergo, TH components, ATmega32A, OLED/encoder/solenoid |
| OrthoCode | keyboards/orthocode | Jrodna | https://github.com/Jrodna/OrthoCode | ortho w/ thumb clusters, all THT incl USB-C, ATmega32A |
| Framework | keyboards/7c8/framework | stevennguyen | https://github.com/stevennguyen/framework | 5x12 ortho TH kit w/ encoder |
| Daisy | keyboards/draytronics/daisy | Draytronics (ghostseven) | https://draytronics.co.uk | TH macropad w/ encoders, ATmega328P |
| Scarlet | keyboards/draytronics/scarlet | Draytronics (ghostseven) | https://github.com/ghostseven/Draytronics-Scarlet-PCB-V1 | 17-key TH numpad, ATmega32A |
| LATE-9 | keyboards/ivndbt/late9 | ivndbt | https://github.com/ivndbt/late-9 | multi-tap 9-key pad, TH only |
| Neopad | keyboards/ivndbt/neopad | ivndbt | https://github.com/ivndbt/neopad | 4-switch + 2-encoder macropad, TH only |
| naKey | keyboards/ckeys (naKey) | cKeys.org | https://ckeys.org | "naKey - Through hole numpad" (soldering workshop board) |
| Planck THK | keyboards/planck/thk | OLKB | https://github.com/olkb/planck_thk | official Planck Through Hole Kit |
| Unicomp Mini M / Model M Yacobo | keyboards/handwired/unicomp_mini_m, keyboards/ibm/model_m/yacobo | various | — | controller replacement projects using TH parts (not kits) |

## Through-hole with module controller (Pro Micro / Elite-C / Pico)

| Keyboard | QMK Path | Designer | Hardware Link | Evidence |
|---|---|---|---|---|
| 0-Sixty | keyboards/0_sixty | vinamarora8 | — | "60 key ortho inspired by Discipline and Preonic, DIY through-hole kit, ProMicro" |
| Labyrinth75 | keyboards/labyrinth75 | Livi (Liviturte) | GB on r/MechMarket | "through hole 75% FR4 sandwich keyboard, Pro Micro / Elite C" |
| Rhino | keyboards/keyprez/rhino | Christian Sandven (csandven) | TBA | 50%, "number row removed and replaced with through hole components", Pro Micro |
| Hackpad | keyboards/hackpad | Nico Stuhlmueller (ThePurox) | git.imaginaerraum.de | 4x4 pad, v0.2 all TH except reset/RGB, ProMicro |
| ortho5by12 | keyboards/ortho5by12 | (community) | — | "Plaid-style 5x12 design", Plaid-identical BOM |
| 3x3macropad | keyboards/rarepotato8de/3x3macropad | RarePotato8DE | https://github.com/rarepotato8de/3x3macropad | Discipline65-inspired stacked FR4 macropad |

## Mentioned "through hole" but NOT TH builds (filtered out)

- eek! (keyboards/eek) — supports SMD *or* TH diodes only; SMD RGB board
- Terrazzo (keyboards/terrazzo) — Pro Micro kit, TH mention incidental
- SP Mini (keyboards/viktus/sp_mini) — only "through hole LED indicators"; SMD ATmega32U4
- Atom47 rev2 — TH mention incidental
- Practice60/65 (cannonkeys) — solder practice line, Pro Micro/blue pill based

## Notes
- vial-qmk mirrors the same keyboard tree; no additional unique TH boards found there.
- kbd.news live site is Cloudflare-blocked; see research_community_vendors.md for wayback findings.