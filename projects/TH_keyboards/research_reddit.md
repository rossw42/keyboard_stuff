# Through-Hole Keyboard Research - Reddit

Method: Reddit official JSON API returned 403 for all user agents (curl + Invoke-RestMethod; www/old/api subdomains).
Fallback: PullPush.io API (Pushshift alternative, api.pullpush.io) for submissions and comments.
Searched r/MechanicalKeyboards, r/olkb, r/ErgoMechKeyboards, r/keyboards, r/diykeyboards, r/mechmarket.
Queries: through hole, through-hole, THT keyboard, atmega328, kit names. GitHub repos verified via HTTP status; QMK tree cross-referenced.

Excluded known list: 0xCB-Static, KBIC65, discipad, discipline, mysterium, romeo, cambkb, punk75, NumDiscipline, scientist, plaid, Plaid-Pad, LCK75, lagom, litl, sthlmkb-storre, basketweave, pinstripe, lumberjack, rosaline, voidPointer, torn, Claudia, axon, lesovoz, barleycorn, 00Key.

---

## New named through-hole keyboards

### Gingham (Yiancar Designs) - 60%
- Reddit: https://www.reddit.com/r/MechanicalKeyboards/comments/18vx9jw/gingham_project/
- Reddit: https://www.reddit.com/r/MechanicalKeyboards/comments/10pbn53/first_time_gingham_through_hole/
- GitHub: https://github.com/yiancar/gingham_pcb (verified 200)
- QMK: keyboards/yiancardesigns/gingham
- Notes: 60% all through-hole, ATmega328p + V-USB. Sold via NovelKeys/Mechboards. One of the most-recommended TH kits.

### Seigaiha (Yiancar Designs) - Alice
- Reddit: https://www.reddit.com/r/olkb/comments/10tzlwb/troubleshooting_seigaiha_though_hole_keyboard_kit/
- GitHub: https://github.com/yiancar/Seigaiha (verified 200)
- QMK: keyboards/yiancardesigns/seigaiha
- Notes: Alice-layout all through-hole kit, ATmega328p + V-USB.

### Argyle 60 (Yiancar) - 60%
- Reddit: https://www.reddit.com/r/MechanicalKeyboards/comments/srqhu4/gb_argyle_60_a_premium_throughhole_keyboard_live/
- GitHub: none found (QMK keyboards/argyle; hardware via prototypist.net)
- Notes: Premium 60% through-hole with RGB, ATmega328p + V-USB.

### Tartan (hsgw / dm9records) - 60%
- Reddit: sister board of Plaid (same designer); surfaced via QMK cross-reference
- GitHub: https://github.com/hsgw/tartan (verified 200)
- QMK: keyboards/dm9records/tartan
- Notes: 60% row-staggered all through-hole from the Plaid designer. ATmega328p + V-USB.

### Mercutio (MechWild) - 40%
- Reddit: https://www.reddit.com/r/MechanicalKeyboards/comments/1egpmcy/my_mercutio_doesnt_get_a_lot_of_time_out_of_the/
- Reddit: https://www.reddit.com/r/MechanicalKeyboards/comments/wfrgdj/just_finished_my_first_through_hole_diy_in_the/
- GitHub: hardware repo not found (QMK keyboards/mechwild/mercutio, maintainer kylemccreery). Product: mechwild.com/product/mercutio/
- Notes: Through-hole 40% with encoder + OLED. Very frequently recommended budget TH kit.

### Jabberwocky (nopunin10did) - full-size columnar Alice
- Reddit: https://www.reddit.com/r/olkb/comments/lqs5je/jabberwocky_fullsize_columnarstagger_alice/
- GitHub: hardware repo not found; community cases: dcpedit/jabberwocky-dexterous-case, lukeski14/jabberwocky-acrylic-case
- QMK: keyboards/nopunin10did/jabberwocky
- Notes: Full-size columnar-stagger Alice DIY through-hole kit, RH/southpaw numpad variants.

### Lattice60 (emdarcher / KeyHive) - HHKB 60%
- Reddit: https://www.reddit.com/r/olkb/comments/kdn72m/help_lattice60_pcb_not_working_in_testing_after/
- GitHub: user https://github.com/emdarcher (dedicated hardware repo not located)
- QMK: keyboards/keyhive/lattice60
- Notes: HHKB layout using only through-hole components, USBasploader bootloader. Sold via KeyHive.

### Framework (stevennguyen / 7c8) - 5x12 ortho
- Reddit: https://www.reddit.com/r/olkb/comments/pxmnm5/gb_framework_throughhole_5x12_ortholinear_kit/
- GitHub: https://github.com/stevennguyen/framework (verified 200)
- QMK: keyboards/7c8/framework
- Notes: All through-hole (except hotswap sockets), rotary encoder, USB-C, FR4/acrylic sandwich.

### Rosalina (rpiguy9907) - 40% + numpad
- Reddit: https://www.reddit.com/r/MechanicalKeyboards/comments/1fcv0tx/rosalina_with_via/
- GitHub: not located; derived from Rosaline by Peej (https://github.com/peej/rosaline-keyboard)
- Notes: Through-hole 40% with left-hand numpad. VIA firmware provided by Peej.

### Nibble (nullbits) - 65%
- Reddit: https://www.reddit.com/r/MechanicalKeyboards/comments/tzg24a/nibble_65_hit_up_an_electrical_engineering_friend/
- GitHub: https://github.com/nullbitsco/nibble (verified 200)
- Notes: 65% kit, all through-hole except optional LEDs. Sold via Amazon / nullbits.co.

### Tidbit (nullbits) - numpad
- Reddit: comments of https://www.reddit.com/r/MechanicalKeyboards/comments/sci0i8/affordable_and_readily_available_throughhole_kits/
- GitHub: https://github.com/nullbitsco/tidbit (verified 200)
- Notes: Beginner-friendly through-hole numpad/macropad.

### Red Herring (dcpedit) - unibody ergo
- GitHub: https://github.com/dcpedit/redherring (verified 200)
- QMK: keyboards/dcpedit/redherring
- Notes: Unibody ergo with through-hole components, ATmega32A, OLED, encoder, solenoid. Surfaced via QMK TH cross-reference.

### OrthoCode (Jrodna) - ortho with thumb clusters
- GitHub: https://github.com/Jrodna/OrthoCode (verified 200)
- QMK: keyboards/orthocode
- Notes: Ortholinear, all through-hole incl USB-C, ATmega32A, standard keysets.

### Resume1800 (CrimsonKeyboards) - 1800 compact
- GitHub: maintainer https://github.com/DeeDesired (hardware repo not located)
- QMK: keyboards/crimsonkeyboards/resume1800
- Notes: 1800-compact built solely with through-hole components, ATmega32A. Rare larger-format TH board.

### Chidori (kagizaraya / ka2hiro) - split
- GitHub: repo not located (kagizaraya org currently 404)
- QMK: keyboards/kagizaraya/chidori
- Notes: Split keyboard made with only through-hole components, ATmega328P per half.

### Rartland (Alabahuy / RART) - 65%
- GitHub: user https://github.com/Alabahuy
- QMK: keyboards/rart/rartland
- Notes: 65% assemblable with only through-hole components, ATmega32A, OLED + encoder, mini USB.

### LATE-9 (ivndbt) - multi-tap pad
- GitHub: https://github.com/ivndbt/late-9 (verified 200)
- QMK: keyboards/ivndbt/late9
- Notes: 90s-phone multi-tap input dev board, through-hole only, OLED.

### Daisy (Draytronics) - macropad
- GitHub: maintainer https://github.com/ghostseven; site draytronics.co.uk/daisy
- QMK: keyboards/draytronics/daisy
- Notes: Macropad with encoders/underglow, mostly through-hole, ATmega328P.

### Scarlet (Draytronics) - 17-key numpad
- GitHub: maintainer https://github.com/ghostseven; site draytronics.co.uk
- QMK: keyboards/draytronics/scarlet
- Notes: 17-key numpad, through-hole home build, ATmega32A.

### Rhino (Keyprez / csandven) - 50%
- GitHub: maintainer https://github.com/csandven (hardware repo not located)
- QMK: keyboards/keyprez/rhino
- Notes: Boardwalk-inspired 50%; number row replaced with exposed through-hole components.

### Practice60 / Practice65 (CannonKeys)
- Reddit: recommended in https://www.reddit.com/r/MechanicalKeyboards/comments/vpiiy7/through_hole_kits_out_there/
- GitHub: none dedicated; QMK keyboards/cannonkeys/practice60 and practice65
- Notes: CannonKeys Practice DIY solder-everything line (also the Stacked acrylic line). cannonkeys.com

### Orange Boy Ergo
- Reddit: comments of https://www.reddit.com/r/MechanicalKeyboards/comments/sci0i8/affordable_and_readily_available_throughhole_kits/
- GitHub: not verified in this pass
- Notes: TH ergo board recommended alongside Practice60/65 and Discipline.

### FinnGus (Clawsome Boards) - cat-shaped Alice
- Reddit: https://www.reddit.com/r/MechanicalKeyboards/comments/r0hd0e/gb_finngus_keyboard_kit_a_cat_shaped_3d_printed/
- GitHub: none found
- Notes: Cat-shaped 3D-printed/FR4 Alice through-hole kit GB (Nov 2021). Vendor also makes GameBuddy.

### KP24 - through-hole numpad/macropad
- Reddit: https://www.reddit.com/r/MechanicalKeyboards/comments/qyiriw/ic_kp24_throughhole_numpadmacropad/
- GitHub: not found
- Notes: IC for a 24-key through-hole numpad/macropad (Nov 2021).

### Berm - 60% ortho (one-off)
- Reddit: https://www.reddit.com/r/MechanicalKeyboards/comments/rllk7b/made_my_first_custom_keyboard_i_call_it_the_berm/
- GitHub: none posted
- Notes: Personal 60% ortholinear design, Elite-C, exposed-PCB minimal aesthetic.

### J73K (MakerJake01)
- Reddit: comment in https://www.reddit.com/r/ErgoMechKeyboards/comments/uwa1t4/are_there_any_throughhole_diy_ortho_kits/
- GitHub: https://github.com/MakerJake01/J73K_keyboard (verified 200)
- Notes: DIY keyboard suggested in through-hole ortho kit discussion.

### M65 (m-lego) - LEGO-cased 65%
- Reddit: comment in https://www.reddit.com/r/ErgoMechKeyboards/comments/uwa1t4/are_there_any_throughhole_diy_ortho_kits/
- GitLab: https://gitlab.com/m-lego/m65
- Notes: LEGO-case keyboard kit, DIY around 20 GBP, suggested in TH ortho thread.

### Lelelab Y2K 76 - commercial TH-aesthetic
- Reddit: https://www.reddit.com/r/MechanicalKeyboards/comments/1jlqocq/my_lelelab_y2k_76_finally_arrived/
- Reddit: https://www.reddit.com/r/MechanicalKeyboards/comments/1gqe7h9/opinions_on_lelelab_y2k_76/
- GitHub: none (commercial prebuilt)
- Notes: 76-key exposed-component through-hole-aesthetic board; aesthetic reference only.

### TU40 / Juliet40 - TaoBao 40%
- Reddit: comments of https://www.reddit.com/r/MechanicalKeyboards/comments/vpiiy7/through_hole_kits_out_there/
- GitHub: none; QMK has keyboards/handwired/juliet
- Notes: TaoBao 40% TH board commonly known as Juliet40.

---

## Key threads for further mining
- Through Hole Kits Out There? https://www.reddit.com/r/MechanicalKeyboards/comments/vpiiy7/ (Litl 40%, TU40/Juliet40, Barleycorne, Mercutio, Gingham, Mysterium, switchcouture.com, keyhive.xyz)
- affordable and readily available through-hole kits? https://www.reddit.com/r/MechanicalKeyboards/comments/sci0i8/ (Orange Boy Ergo, Practice65, Discipline 65, Practice60, Nibble, Tidbit)
- Are there any through-hole diy ortho kits? https://www.reddit.com/r/ErgoMechKeyboards/comments/uwa1t4/ (Plaid, Framework, J73K, m-lego M65)
- Through hole keyboards suggestions? https://www.reddit.com/r/MechanicalKeyboards/comments/1dztzj3/

## Access notes
- reddit.com/.json, old.reddit.com, api.reddit.com all returned 403 Blocked regardless of user agent.
- Working alternative: https://api.pullpush.io/reddit/search/submission/ and /comment/ (rate limited, roughly 1 request per 10s).
