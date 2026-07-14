# Through-Hole Keyboard Research: Community and Vendor Sites

Sources searched: 42keebs.eu (with-discrete-mcu category + search), mechboards.co.uk, keyhive.xyz, p3dstore.com, kbd.news (via Wayback Machine; live site is Cloudflare-blocked), GitHub via gh search.

## New Through-Hole Keyboards Found (High Confidence)

| Keyboard | Source URL | GitHub Repo | Confidence |
|---|---|---|---|
| Sesame | https://42keebs.eu/shop/kits/with-discrete-mcu/sesame-ergo-60-kit/ | https://github.com/kb-elmo/sesame | High - vendor: only through-hole components; Alice-layout 60% |
| Donegal-C | https://42keebs.eu/shop/kits/with-discrete-mcu/donegal-c-60-keyboard-kit/ | https://github.com/piit79/donegal-c | High - vendor: only through-hole components; 60% USB-C |
| Herringbone / Herringbone Pro | https://42keebs.eu/shop/kits/with-discrete-mcu/herringbone-pro-75-ansi-iso-kit/ | https://github.com/ramonimbao/Herringbone-Pro (orig: https://github.com/ramonimbao/Herringbone) | High - TH 75% w/ rotary encoder + OLED |
| Gingham | https://github.com/yiancar/gingham_pcb | https://github.com/yiancar/gingham_pcb | High - 60% throughhole inspired by Plaid; USB-C variant gingham_usbc_pcb |
| Gingerham | https://github.com/itsnoteasy/gingerham | https://github.com/itsnoteasy/gingerham | High - Gingham fork, ISO 60%, drops I/O expander |
| Chevron | https://github.com/ramonimbao/Chevron | https://github.com/ramonimbao/Chevron | High - README: Through-hole 40%-ish, ATmega32A 40-pin DIP |
| AELITH | https://github.com/ramonimbao/AELITH | https://github.com/ramonimbao/AELITH | High - README: Through-hole Alice-layout, ATmega32A 40-pin DIP |
| SEGMENT | https://github.com/slonket/segment-keyboard | https://github.com/slonket/segment-keyboard | High - 60% only through-hole components, 1980s PCB aesthetic |
| 0xCB Jupiter | https://github.com/0xCB-dev/0xCB-Jupiter | https://github.com/0xCB-dev/0xCB-Jupiter | High - 1800-sized through-hole kit (same maker as 0xCB-Static) |
| luckyboard70 | https://github.com/luckybusted/luckyboard70 | https://github.com/luckybusted/luckyboard70 | High - entirely TH components incl USB-C (repo desc; sparse repo) |
| masochist | https://github.com/RSchneyer/masochist | https://github.com/RSchneyer/masochist | High - through-hole 27%, Pain27 x Romeo hybrid |
| plaid-lopro-keeb | https://github.com/FrancisUsher/plaid-lopro-keeb | https://github.com/FrancisUsher/plaid-lopro-keeb | High - 60% only TH components, Kailh low-profile switches |
| Swissterium | https://github.com/Davines123/Swissterium | https://github.com/Davines123/Swissterium | High - Mysterium variant, entirely TH incl USB-C |
| southpaw_discipline | https://github.com/JZolko/southpaw_discipline | https://github.com/JZolko/southpaw_discipline | High - Discipline variant w/ left-hand numpad |

## Medium / Lower Confidence Candidates

| Keyboard | Source URL | GitHub Repo | Confidence |
|---|---|---|---|
| casio59 | gh search | https://github.com/mrninhvn/casio59 (404 via API, may be renamed/private) | Medium - desc: TH components only, keyboard for Casio FX-880P |
| keyboard60-throughole | gh search | https://github.com/davidgraeff/keyboard60-throughole (404 via API, may be deleted) | Medium - 60% ANSI/ISO PCB, TH only |
| Wanda | gh search | https://github.com/ianfhunter/Wanda (README fetch 404) | Medium - TH numpad |
| Livewire | gh search | https://github.com/ElKinoflop/Livewire | Medium - exposed TH diodes/wiring aesthetic, but likely Pro Micro controller (not discrete TH MCU) |
| nullwing | gh search | https://github.com/CityRunner/nullwing-keyboard | Medium - TH per desc, Choc Mini; firmware incomplete |
| atmega328p-standalone-board | gh search | https://github.com/BenRoe/atmega328p-standalone-board | Low - dev board (not keyboard) but TH ATmega328P + USB-C, useful reference |
| Avlo44 | kbd.news tag/through-hole (wayback) | not found via gh search | Low - kbd.news TH-tagged post, no repo located |
| ErgoMorph55 | kbd.news tag/through-hole (wayback) | not found via gh search | Low - kbd.news TH-tagged post, no repo located |
| Pain27 | gh search | https://github.com/uuupah/pain27 | Low - TH LEDs but Pro Micro based, not discrete-MCU TH |

## Ruled Out / Notes
- Sagittarius (AcheronProject): ergo keyboard, no TH evidence in README - NOT through-hole.
- ThumbsUp (ak66666): split PCB, no TH-MCU evidence found in README.
- Nori, Jones, Ellora, Fave, Ginny: no TH repos found via gh search.
- BT65/BT75 (Mechboards): only through-hole LEDs; nRF52840 module controller - not a TH build.
- Keyhive, P3D Store: no through-hole kits found in search results.
- kbd.news live site is Cloudflare-protected; Wayback snapshot of /tag/through-hole listed: Avlo44, ErgoMorph55, Sesame (kb-elmo), LCK75 (excluded), Axon (excluded), Torn (excluded), plus a TH ortho w/ thumb cluster and Framework rev.1 prototype posts.
- 42keebs "With Discrete MCU" category = their through-hole section. Full list: Basketweave-S, Discipad, Discipline, Donegal-C, Herringbone Pro, Lumberjack-C, Mysteripad, Mysterium, Plaid, Romeo, Sesame (most already known/excluded).
