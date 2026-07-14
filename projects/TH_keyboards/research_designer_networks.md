# Through-Hole Keyboard Research: Designer Networks

Method: crawled GitHub accounts of known TH keyboard designers (hsgw, coseyfannitutti, peej, null-ll, mohoyt, rtitmuss, yiancar, lyso1, subottimale, thatfellarobin, dsanchezseco, RafaelCasamaximo, b-karl, godders, ericrlau, 0xCB-dev, ZeroZeroOne-dev, Tsquash, cosimini) via `gh repo list`, checked forks/derivatives of famous TH boards (Plaid, Discipline, Mysterium), and mined the jcmkk3/keyboard-inspiration curated list.

Excluded (already known): 0xCB-Static, KBIC65, cfbender/keyboards, discipad, discipline, mysterium, romeo, cambkb, punk75, NumDiscipline, scientist, plaid, keyboard-inspiration, Plaid-Pad, LCK75, LCK75v3, lagom, litl, sthlmkb-storre, basketweave, pinstripe, lumberjack-keyboard, rosaline-keyboard, voidPointer, torn, Claudia, axon, lesovoz-files, barleycorn_pcb, 00Key.

---

## Confirmed TH (description/README explicitly through-hole/THT)

| Repo | Description | Confidence |
|---|---|---|
| https://github.com/hsgw/tartan | 60% keyboard, through-hole parts only (Plaid designer) | confirmed TH |
| https://github.com/hsgw/Madras | TH-components-only keyboard, QAZ layout, w/ relay (Plaid designer) | confirmed TH |
| https://github.com/peej/tripel-keyboard | Modular ortho 60%, all through-hole components | confirmed TH |
| https://github.com/peej/crosshatch-keyboard | 13x5 ortho TH PCB for 60% tray cases | confirmed TH |
| https://github.com/peej/orthgyle-keyboard | 5x15 ortho THT PCB for the Argyle, ATmega328p, duplex matrix | confirmed TH |
| https://github.com/yiancar/gingham_pcb | 60% through-hole, Plaid-inspired | confirmed TH |
| https://github.com/yiancar/gingham_usbc_pcb | Gingham with USB-C | confirmed TH |
| https://github.com/yiancar/Seigaiha | Alice through-hole w/ USB-C, Plaid/TGR Alice inspired | confirmed TH |
| https://github.com/ramonimbao/Herringbone | Original TH 75%, ATmega32A | confirmed TH |
| https://github.com/ramonimbao/Herringbone-Pro | TH 75% w/ encoder + OLED | confirmed TH |
| https://github.com/ramonimbao/AELITH | Alice-layout TH keyboard, ATmega32A DIP | confirmed TH |
| https://github.com/ramonimbao/Chevron | 40%-ish TH keyboard, ATmega32A DIP | confirmed TH |
| https://github.com/slonket/segment-keyboard | 60% TH kit themed after 1980s PCBs | confirmed TH |
| https://github.com/0xCB-dev/0xCB-Jupiter | 1800-size THT keyboard kit (0xCB-Static maker) | confirmed TH |
| https://github.com/olkb/planck_thk | Official Planck Through Hole Kit | confirmed TH |
| https://github.com/kb-elmo/sesame (mirror: str-dst/sesame) | Alice ergo, only THT parts | confirmed TH |
| https://github.com/itsnoteasy/gingerham | Gingham fork: ISO-UK/ANSI/ABNT2 60%, drops I/O expander | confirmed TH |
| https://github.com/piit79/donegal-c | 60% TH with USB-C (Gingham/Donegal lineage) | confirmed TH |
| https://github.com/piit79/mysteripad | TH numpad matching the Mysterium form factor | confirmed TH |
| https://github.com/piit79/kilt-keyboard | Ortho 5-column DIY kit inspired by the Plaid | confirmed TH |

## Derivatives / forks of known TH boards (likely TH)

| Repo | Description | Confidence |
|---|---|---|
| https://github.com/JZolko/southpaw_discipline | Discipline 65% mod w/ left-hand numpad | likely TH |
| https://github.com/Davines123/Swissterium | Heavily edited Mysterium variant, entirely TH incl USB-C | confirmed TH |
| https://github.com/LordRabel/Rabelius | Compact 1800 based on CFTKB Mysterium | confirmed TH |
| https://github.com/covah901/CN62B---Ergo-Keyboard | ATmega32A ergo based on CFTKB Mysterium | confirmed TH |
| https://github.com/RSchneyer/masochist | TH 27% (Pain27 x Romeo hybrid) | confirmed TH |
| https://github.com/FrancisUsher/plaid-lopro-keeb | Plaid variant w/ Kailh low-profile switches, TH only | confirmed TH |
| https://github.com/tjeffree/lumberelite | Lumberjack variant w/ Elite-C + OLED | likely TH (module controller) |
| https://github.com/Ardakilic/woodpecker-keyboard | Lumberjack/Lumberelite fork for nice!nano wireless | likely TH (module controller) |
| https://github.com/ianelsbree/wik75 | Ortho 75% inspired by Discipline | likely TH |
| https://github.com/jamerhar/poppy | 70% Alice using THT components, expands on kb-elmo Sesame | confirmed TH |

## From jcmkk3/keyboard-inspiration + misc network finds

| Repo | Description | Confidence |
|---|---|---|
| https://github.com/mothdotmonster/OK96 | 96-key ortho, TH components (untested per README) | confirmed TH (untested) |
| https://github.com/ndeporceri/NMB-75 | TH 75% keyboard PCB | confirmed TH |
| https://github.com/htpkbs/pin-check | Small all-TH PCB for hand-wired keyboards | confirmed TH |
| https://github.com/htpkbs/splotch | Ortho split w/ thumb clusters, TH (abandoned, matrix bug) | likely TH |

## Notes
- Designer accounts lyso1, subottimale, thatfellarobin, dsanchezseco, RafaelCasamaximo, b-karl, godders, ericrlau, ZeroZeroOne-dev, Tsquash, cosimini had no additional TH keyboard repos beyond the known list.
- Forks of hsgw/plaid and coseyfannitutti/discipline are almost entirely unmodified mirrors; only meaningful derivatives are listed above.
- Overlap intentional with research_github_search.md — this file records network-crawl provenance.