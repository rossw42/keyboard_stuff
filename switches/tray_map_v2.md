# Switch Tray Map v2

Full row/column map of the switch tester tray, built from all three tray
photos (`IMG_3218.JPG`, `IMG_3219.JPG`, `IMG_3220.JPG`) cross-referenced with
the labeled eBay listing photos (`fromebay1.PNG`, `fromebay2.webp`).

- Grid is 4 rows × 15 columns, top-left = `0,0`.
- **Rows do not all have the same columns filled** — empty wells are marked
  `(empty)`. Row 3 has wider spacing and only ~12 wells; column indices there
  are approximate.
- Second identification pass done: brand markings visible in IMG_3218/3219
  (GATERON, AKKO, YOK, Kailh, Outemu) raised several confidence scores.

## Grid

| Row\Col | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---------|---|---|---|---|---|---|---|---|---|---|----|----|----|----|----|
| **0** | Kailh Box Jade | Kailh Box White | Kailh Box Navy | Box Blue clone (Xinda?) | Cherry MX Blue | Outemu Blue | Kailh Speed Bronze | NK x Kailh Sherbet | Unknown blue clicky | (empty) | Akko Creamy Blues | BSUN Oceans | Unknown teal linear | Wingtree Yunies | HMX Firecrackers |
| **1** | Gateron Type-R | Holy Panda (Invyr) | Drop Holy Panda | JWK T1 | Durock T1 | Gateron Quinns | Akko Lavenders | Yok Trash Pandas | Unknown gray stem | Kailh Box Royal | Haimu Mints | Keebfront Dooms | Unknown cream/white | (empty?) | Durock Koalas |
| **2** | Zealios (62g or 68g) | Zealios (62g or 68g) | Neapolitan Ice Cream | CK x Haimu Thistles | WS Heavy Tactile | Akko Creamy Purple Pro | KTT Baby Blues | LTC Jerrzi | Drop Halos | Kailh Polias | Outemu Brown | Durock Amber T1 | Waverider V2 | Golden Apples V2 | (empty?) |
| **3** | Gateron Red | Box Yellow (verify) | Tecsee Carrot | Skyloong Crystal | Gateron Milky Yellow | Pink Crystal (unknown) | Smoky Black (Akko V3 Creamy Black Pro?) | Pale Mint (Silent Penguin / Tecsee Raw?) | (empty) | (empty) | (empty) | (empty) | — | — | — |

## Row detail (type / force / confidence)

### Row 0 — Clickies (left) + eBay linears (right)

| Pos  | Switch                    | Type    | Force (g)       | Confidence | Second-pass notes                                                           |
| ------| ---------------------------| ---------| -----------------| ------------| -----------------------------------------------------------------------------|
| 0,0  | Kailh Box Jade            | Clicky  | 50 op           | High       | Jade box stem, unmistakable                                                 |
| 0,1  | Kailh Box White           | Clicky  | 45 op           | High       | "Kailh" branding visible on gray top                                        |
| 0,2  | Kailh Box Navy            | Clicky  | 75 op           | High       | Navy box stem                                                               |
| 0,3  | Box Blue clone (Xinda?)   | Clicky  | ~55 (verify)    | Med        | Teal box-style stem, non-Kailh branding — verify                            |
| 0,4  | Cherry MX Blue            | Clicky  | 60 op / 50 act  | High       | CHERRY branding on black housing                                            |
| 0,5  | Outemu Blue               | Clicky  | ~50             | Med        | Blue stem, round click-pin visible                                          |
| 0,6  | Kailh Speed Bronze        | Clicky  | 50 op           | High       | "Kailh" branding, bronze stem                                               |
| 0,7  | NovelKeys x Kailh Sherbet | Clicky  | 45 op           | Med-High   | Orange stem, clear housing — matches old inventory                          |
| 0,8  | Unknown blue clicky       | Clicky? | TBD             | Low        | Bright blue stem, clear top — possibly Gateron Blue                         |
| 0,9  | *(empty)*                 | —       | —               | —          |                                                                             |
| 0,10 | Akko Creamy Blues         | Tactile | 45 op           | High ↑     | Transparent blue housing + blue stem matches Akko V3 Cream Blue Pro exactly |
| 0,11 | BSUN Oceans   not correct | Linear  | ~48 (verify)    | Med        | Housing looks lighter than eBay photo — could be swapped with 0,12          |
| 0,12 | Unknown teal linear       | Linear? | TBD             | Low        | Teal stem — possibly from the eBay "Linear Switches" pile                   |
| 0,13 | Wingtree Yunies           | Linear  | ~48 (verify)    | High       | Solid blue housing + orange stem, unique combo                              |
| 0,14 | HMX Firecrackers          | Linear  | ~50 op / 58 bot | High       | White top, blue accents, red stem, unique combo                             |

### Row 1 — Big tactiles

| Pos  | Switch              | Type                    | Force (g)      | Confidence | Second-pass notes                                                                 |
| ------| ---------------------| -------------------------| ----------------| ------------| -----------------------------------------------------------------------------------|
| 1,0  | Gateron Type-R      | Linear/Tactile (verify) | ~55 (verify)   | High       | GATERON branding confirmed on dark red housing                                    |
| 1,1  | Holy Panda (Invyr)  | Tactile                 | 67 bot         | Med        | Salmon/peach stem, milky top — per old tray notes                                 |
| 1,2  | Drop Holy Panda     | Tactile                 | 65 op          | Med        | Black housing, gold/tan stem — per old tray notes                                 |
| 1,3  | JWK T1              | Tactile                 | 67 bot         | Med        | Black housing, teal stem — T1 family look-alikes                                  |
| 1,4  | Durock T1           | Tactile                 | 67 bot         | Med        | Smokey housing, teal stem — T1 family look-alikes                                 |
| 1,5  | Gateron Quinns      | Tactile                 | 60 op          | High ↑     | GATERON branding confirmed on burgundy housing, cream stem                        |
| 1,6  | Akko Lavenders      | Tactile                 | 36 op          | High ↑     | AKKO branding confirmed on purple translucent housing                             |
| 1,7  | Yok Trash Pandas    | Tactile                 | 67 bot         | High ↑     | YOK branding confirmed, purple stem                                               |
| 1,8  | Unknown gray stem   | Linear?                 | TBD            | Low        | Clear housing, gray/silver stem — possibly Cherry Speed Silver from old inventory |
| 1,9  | Kailh Box Royal     | Tactile                 | 45 op / 75 tot | High ↑     | Kailh branding visible, dark purple box stem                                      |
| 1,10 | Haimu Mints         | Linear (poss. silent)   | ~50 (verify)   | High       | Solid mint-green housing                                                          |
| 1,11 | Keebfront Dooms     | Tactile (verify)        | ~63.5 (verify) | High       | Green housing, gray/white stem                                                    |
| 1,12 | Unknown cream/white | TBD                     | TBD            | Low        | Cream housing, white stem                                                         |
| 1,13 | *(empty?)*          | —                       | —              | —          | Verify — spacing ambiguous in photos                                              |
| 1,14 | Durock Koalas       | Tactile                 | 62 bot         | High       | Cream housing, dark brown stem                                                    |

### Row 2 — Medium tactiles + eBay linears (right)

| Pos  | Switch                        | Type           | Force (g)        | Confidence | Second-pass notes |
|------|-------------------------------|----------------|------------------|------------|-------------------|
| 2,0  | Zealios (62g or 68g)          | Tactile        | 62 or 68 bot     | Med        | Visually identical to 2,1 — press-test to tell apart |
| 2,1  | Zealios (62g or 68g)          | Tactile        | 62 or 68 bot     | Med        | Visually identical to 2,0 |
| 2,2  | Neapolitan Ice Cream (Tecsee) | Tactile        | 63 op            | High       | Pink housing, tan stem |
| 2,3  | CK x Haimu Thistles           | Silent Tactile | ~63.5 (verify)   | High       | Lilac housing + lilac stem |
| 2,4  | Wuque Studio Heavy Tactile    | Tactile        | ~68–70 bot       | High       | White/gray housing, black stem |
| 2,5  | Akko Creamy Purple Pro        | Tactile        | 36 op (verify)   | High ↑     | AKKO branding visible, tan/cream stem |
| 2,6  | KTT Baby Blues                | Linear         | ~45 (verify)     | High ↑     | Mint/aqua housing matches labeled eBay photo exactly |
| 2,7  | LTC Jerrzi                    | Clicky (verify)| ~45 (verify)     | High ↑     | Fully clear incl. stem — distinguishes it from Halos' opaque white stem |
| 2,8  | Drop Halos (True/Clear)       | Tactile        | 60/65 op         | High ↑     | Opaque white stem in clear housing — variant TBD |
| 2,9  | Kailh Polias                  | Tactile        | 50 (verify)      | High       | Periwinkle stem matches labeled eBay photo |
| 2,10 | Outemu Brown                  | Tactile        | 45 op            | High ↑     | Outemu branding visible, brown stem |
| 2,11 | Durock Amber T1               | Tactile        | 67 bot           | High       | Smokey amber translucent housing |
| 2,12 | Sillyworks x HMX Waverider V2 | Linear         | 45 op / 50 bot   | High       | Blue translucent housing, white stem |
| 2,13 | Wingtree Golden Apples V2     | Linear         | ~45 (verify)     | High       | Gold translucent housing, white stem |
| 2,14 | *(empty?)*                    | —              | —                | —          | Verify — spacing ambiguous in photos |

### Row 3 — Linears (wider spacing, ~12 wells, indices approximate)

| Pos  | Switch                          | Type    | Force (g)       | Confidence | Second-pass notes |
|------|---------------------------------|---------|-----------------|------------|-------------------|
| 3,0  | Gateron Red                     | Linear  | 45 op           | Med        | Clear top, red stem — old notes said Cherry Red, but housing style looks Gateron; verify branding |
| 3,1  | Box Yellow (Kailh?)             | Linear  | ~60 bot (verify)| Med        | Thick gold stem, clear housing |
| 3,2  | Tecsee Carrot                   | Linear  | ~55 (verify)    | High       | Orange housing + teal stem, unique combo |
| 3,3  | Skyloong Crystal                | Linear  | TBD             | Med-High   | Fully aqua translucent, white stem |
| 3,4  | Gateron Milky Yellow            | Linear  | 50 op           | High ↑     | GATERON branding confirmed in IMG_3219, milky housing + yellow stem |
| 3,5  | Pink Crystal (unknown)          | Linear  | TBD             | Low        | Pink translucent, white stem — matches a switch in the eBay linear pile |
| 3,6  | Akko V3 Creamy Black Pro (?)    | Linear  | TBD             | Med        | Smoky dark housing, black stem — per old inventory guess |
| 3,7  | Silent Penguin / Tecsee Raw (?) | Silent? | TBD             | Low        | Very pale mint/clear, dust-cover style stem |
| 3,8–3,11 | *(empty wells ×4)*          | —       | —               | —          | Four visibly empty square wells at right of row |

## Confidence changes from second pass (↑)

| Pos  | Switch                 | Was | Now  | Why                                                                       |
| ------| ------------------------| -----| ------| ---------------------------------------------------------------------------|
| 0,10 | Akko Creamy Blues      | Med | High | Transparent blue housing + blue stem is exact match for V3 Cream Blue Pro |
| 1,5  | Gateron Quinns         | —   | High | GATERON branding legible in IMG_3218                                      |
| 1,6  | Akko Lavenders         | —   | High | AKKO branding legible in IMG_3218/3219                                    |
| 1,7  | Yok Trash Pandas       | —   | High | YOK branding legible                                                      |
| 1,9  | Kailh Box Royal        | Med | High | Kailh branding legible                                                    |
| 2,5  | Akko Creamy Purple Pro | —   | High | AKKO branding legible in IMG_3219                                         |
| 2,6  | KTT Baby Blues         | Med | High | Mint/aqua housing matches labeled eBay photo                              |
| 2,7  | LTC Jerrzi             | Med | High | All-clear stem vs Halos' opaque white stem                                |
| 2,8  | Drop Halos             | Med | High | Opaque white stem confirms vs Jerrzi                                      |
| 2,10 | Outemu Brown           | Med | High | Outemu branding legible                                                   |
| 3,4  | Gateron Milky Yellow   | new | High | GATERON branding legible in IMG_3219 (was "Gateron Yellow" guess)         |

Speed Pink

## Still unresolved

- 0,8 unknown blue clicky (Gateron Blue?)
- 0,11 vs 0,12 — confirm which is BSUN Oceans (eBay photo shows a *darker* navy housing than 0,11 appears)
- 1,8 unknown gray stem (Cherry Speed Silver?)
- 1,12 unknown cream/white switch
- 2,0 vs 2,1 — Zealios 62g vs 68g (press-test)
- 3,5 pink crystal, 3,7 pale mint — likely from the eBay unlabeled piles
- Exact empty-well columns in rows 1 and 2 (1,13 / 2,14 assumed)