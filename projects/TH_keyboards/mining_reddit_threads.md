# Thread Mining: Key Reddit Threads (Round 2)

Method: PullPush API comment dumps (Reddit JSON API 403s), followed by `gh` repo searches, README verification, and local QMK readme cross-checks.

---

## Thread vpiiy7 — "Through Hole Kits Out There?" (r/MechanicalKeyboards)

17 comments mined. OP selftext removed.

Every keyboard/vendor mentioned:
- **Litl 40%** — sthlmkb.com (already known)
- **TU40 / Juliet40** — TaoBao board; QMK `keyboards/handwired/juliet` is a handwire of it. No GitHub hardware repo exists. NOT resolvable further.
- **"Barleycorne 75%"** — RESOLVED: misspelling of **Barleycorn** (NovelKeys URL slug `barleycorn-keyboard-kit`), Yiancar's compact-1800. Already known — not a distinct board.
- **Discipline65, Mysterium V2, Romeo40** — cftkb.com (already known)
- **Treadstone48** — via KeebD (keebd.com, AU vendor). QMK `keyboards/marksard/treadstone48`, repo https://github.com/marksard/Keyboards. Verified readme: "47/48-key Symmetric Staggered" — **no TH claim; Pro Micro based. NOT confirmed TH.**
- **GameBuddy / "Clawboards"** — Clawsome Boards (u/ChalkButter). Gamepad-style TH board; no GitHub found. See FinnGus (same vendor).
- **MurphPad** (MechWild), **Maypad** (KeyHive) — macropads:
  - MurphPad = Pro Micro/Blackpill macropad, not discrete-TH.
  - **May Pad** = "through hole kit using a pro micro footprint and through hole diodes", 20-key numpad by u/reggatronics; QMK `keyboards/keyhive/maypad`, maintainer Cody Bender → hardware lives in **cfbender/keyboards** (ALREADY STARRED).
- **Mercutio, Gingham** — already known
- **CannonKeys Practice / Stacked lines** — see sci0i8 verdict below
- **switchcouture.com, keyhive.xyz** — vendor deep-dive in mining_vendors_deep.md

## Thread sci0i8 — "affordable and readily available through-hole kits?" (r/MechanicalKeyboards)

Only 3 comments (confirmed num_comments=3):
1. Mercutio (known)
2. Nibble 65 + Tidbit, nullbits, Amazon US (known)
3. "Orange boy ergo, pratice 65, Discipline 65, Practice60"

### Orange Boy Ergo — RESOLVED
- = **MechWild OBE**, budget Alice-like ~70-key kit by Kyle McCreery.
- QMK `keyboards/mechwild/obe`: "powered by the **STM32 Blackpill**" (module controller).
- Verdict: **TH-adjacent** — TH diodes/parts + socketed Blackpill module, NOT discrete-TH MCU.
- Product: https://mechwild.com/product/orange-boy-ergo/

### Practice60 / Practice65 (CannonKeys) — VERDICT
- Solder-practice boards using **STM32 Blue Pill / module controllers**, not discrete TH MCU.
- Verdict: **NOT true TH** (soldering-practice line). Confirmed ruled out.

## Thread uwa1t4 — "Are there any through-hole diy ortho kits?" (r/ErgoMechKeyboards)

5 comments:
- **m-lego M65** (designer alinelena) — https://gitlab.com/m-lego/m65 — VERDICT: **NOT strict TH**. Revs 9–11 use Seeed XIAO RP2040/nRF52840 SMD module + socketed DIP shift registers (74HC595/589). TH-adjacent at best.
- **J73K** — https://github.com/MakerJake01/J73K_keyboard (see leads file)
- **ortho5by12** (u/squeezeonein, aka itsnoteasy) — PCB+QMK zip: https://github.com/itsnoteasy/misc/blob/master/ortho5by12.zip — Plaid-BOM TH design (already catalogued)
- **Aardvark** — https://www.40percent.club/2020/08/the-aardvark.html — **CONFIRMED TH**: 3x12 ortho, ATmega328P in DIP-28 socket, V-USB (zeners + resistors), 1n4148 THT diodes, ceramic resonator, USBasp bootloader, APA106 TH RGB LEDs. Designer: di0ib (40% club). No dedicated GitHub hardware repo; files via 40percent.club blog. **NEW confirmed TH board.**
- Plaid, Framework, Lumberjack, punk75, Planck THK (all known)

## Thread 1dztzj3 — "Through hole keyboards suggestions?"

DEAD END: post was removed by AutoModerator (help-request rule). 1 comment (bot). Zero content.

---

## Net-new confirmed TH from this round
| Keyboard | Link | Status |
|---|---|---|
| **Aardvark** (di0ib, 40% club) | https://www.40percent.club/2020/08/the-aardvark.html | CONFIRMED TH (ATmega328P DIP + V-USB) |

## Resolved / closed leads
- Barleycorne = Barleycorn (known) — closed
- Orange Boy Ergo = MechWild OBE — TH-adjacent (Blackpill)
- Practice60/65 — NOT TH (Blue Pill practice boards)
- M65 — NOT strict TH (XIAO module)
- TU40/Juliet40 — no repo exists, TaoBao-only
- Nightmare + May Pad (KeyHive) — designed by Cody Bender; hardware in **cfbender/keyboards** which is already starred
- Treadstone48 — not TH (Pro Micro, no TH claim)
- MurphPad — not TH (module controller)