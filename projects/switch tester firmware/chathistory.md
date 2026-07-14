# Keyboard Switch Tester with Vial Macros


## User
*6/29/2026, 2:08:31 PM*


another keyboard vial kinda of question.
i want to make a keyboard switch tester, i want it to be a keyboard, but I want a testing layer that will print out what switch you are pressing, for a 60% keyboard i dont think we have enough macros to be able to do that..   what do you think we can do to solve this /


---


## Assistant
*6/29/2026, 2:08:31 PM*


Great question! You're right that the default macro slot limit in Vial (typically 16) won't cover all ~61 keys on a 60%. But there are a few solid approaches:


## Options from simplest to most powerful:


### 1. Vial's Built-in Matrix Tester (already exists!)
Vial has a **"Matrix Tester"** tab — press any switch and it highlights the position on a visual layout. No firmware changes needed. If you just need to verify switches actuate, this already solves it.


### 2. QMK Console Output (no macros needed)
Enable `CONSOLE_ENABLE = yes` in `rules.mk`. QMK will output the row/col matrix position on every keypress to the debug console (viewable in QMK Toolbox or `hid_listen`). Zero macro slots used — it's firmware-level logging.


### 3. Custom Keycodes with `send_string()` (the real answer)
This bypasses the macro limit entirely. In your `keymap.c`, define custom keycodes for each position on a testing layer:


```c
// Each key gets a unique custom keycode
case TEST_KEY_Q:
   if (record->event.pressed) {
       send_string("Q position\n");
   }
   break;
```


Since these are compiled into firmware (not dynamic macros), you can have as many as flash allows — 61 is trivial. Each key on your testing layer prints its identity to whatever text field is focused.


### 4. Increase Macro Count (Vial-only fix)
In `config.h`:
```c
#define DYNAMIC_KEYMAP_MACRO_COUNT 64
#define DYNAMIC_KEYMAP_MACRO_BUFFER_SIZE 4096
```
Then you can assign all 61+ macros in Vial's GUI. Strings like `"Q\n"` are tiny so buffer isn't an issue. Downside: requires reflashing firmware with these defines.


---


**My recommendation:** If you want it configurable in Vial without recompiling every time → option **4** (bump macro count). If you want it clean and permanent → option **3** (custom keycodes). If you just need to verify switches work right now → option **1** already does it.


What's your use case — are you testing switches for customers/friends (so it needs to type the name visually), or is it more for your own QA?


---


## User
*6/29/2026, 2:10:16 PM*


well i want the output to be something like "Clicky - Kalih Box White"


---


## Assistant
*6/29/2026, 2:10:16 PM*


Got it — so you want full descriptive strings per key. Let's do the math:


**61 keys × ~25 chars average** (e.g. `"Clicky - Kailh Box White"`) = **~1,525 bytes** of macro buffer needed.


## Best approach: Bump Vial macro limits


In your `config.h`:
```c
#define DYNAMIC_KEYMAP_MACRO_COUNT 64
#define DYNAMIC_KEYMAP_MACRO_BUFFER_SIZE 4096  // plenty of headroom
```


Then in Vial you just:
1. Create a **testing layer**
2. Assign each key → Macro 0, Macro 1, Macro 2... up to Macro 60
3. Set each macro's text to `"Clicky - Kailh Box White{Enter}"`, `"Tactile - Boba U4T{Enter}"`, etc.


**This is the move** because:
- 4KB buffer easily fits 61 strings of that length
- You can **relabel in Vial's GUI** whenever you swap a switch — no reflashing
- You could even add a `\n` (Enter) or `\t` (Tab) at the end so it auto-advances in a spreadsheet


## The one catch


You need to **reflash once** with the bumped defines, but after that it's all GUI-configurable. Just make sure your MCU has enough EEPROM/flash for the larger buffer (any ATmega32U4 or RP2040 board handles 4KB no problem).


## Bonus idea


If you want it to auto-fill a spreadsheet as you go across a row of switches, end each macro with `\t` (Tab) instead of Enter — it'll jump to the next cell. Then you've got an instant comparison log.


Want help writing the full `config.h` changes for your specific board?


---


## User
*6/29/2026, 2:11:27 PM*


is macros the best solution here? it might be but lets <thinking>


---


## Assistant
*6/29/2026, 2:11:27 PM*


Good instinct to step back. Let's think through the options honestly:


## The contenders:


| Approach | Reconfigurable? | Complexity | String length limit? |
|----------|:-:|:-:|:-:|
| **Vial macros (bumped)** | ✅ GUI, no reflash | Low | ~4KB total buffer |
| **Compiled `send_string` array** | ❌ Reflash every swap | Medium | Basically unlimited (flash) |
| **Raw HID + companion app** | ✅ Edit a file on PC | High | None |
| **Position-only output + spreadsheet** | ✅ | Lowest | N/A |


## My actual take:


**Macros are the best fit here.** Here's why:


A switch tester's whole point is that **switches get swapped**. You want to relabel without reflashing. That kills the compiled `send_string` approach immediately.


A companion app (keyboard sends a position ID via Raw HID → Python script maps it to a name → types it out) is *technically* superior but way overkill for this — now you need software running on the host.


The macro buffer math is comfortable:
- 61 keys × `"Clicky - Kailh Box White\n"` (~27 bytes) = **~1,650 bytes**
- 4KB buffer = room for strings up to ~65 chars each


**The one real alternative worth considering:** each key just types a number/position code (`01`, `02`... `61`), and you maintain a reference card or spreadsheet mapping positions to switches. Zero firmware changes ever. But that's less *cool* — you lose the instant "oh that's a Box White" moment.


So yeah — bumped macros is the move. Want to proceed with the firmware config?


---


## User
*6/29/2026, 2:12:40 PM*


yes.


---


## Assistant
*6/29/2026, 2:12:41 PM*


Here's what you need to add/change in your `config.h`:


```c
// Switch tester macro config
#define DYNAMIC_KEYMAP_MACRO_COUNT 64
#define DYNAMIC_KEYMAP_MACRO_BUFFER_SIZE 4096
```


That's it for firmware. Reflash once, then in Vial:


1. **Add a testing layer** (e.g. Layer 1)
2. **Set a layer toggle** on Layer 0 — maybe `Fn` or a key you won't use as a switch position — to `MO(1)` or `TG(1)`
3. **Assign every key on Layer 1** to Macro 0 through Macro 60
4. **Fill each macro** with the switch description:
  - Macro 0: `Clicky - Kailh Box White` + Enter
  - Macro 1: `Tactile - Boba U4T` + Enter
  - ...etc


From there, every time you swap a switch, just update that one macro in Vial. No reflash needed.


Want me to put together a starter layout mapping (position → macro number) or a template spreadsheet you could use to track which switch is in which position?


---


## User
*6/29/2026, 2:19:00 PM*


can we create the vial saved layout that has the macros in it?
lets go with a standard 60% keyboard.


---


## Assistant
*6/29/2026, 2:19:00 PM*


Here's your layout file — [switch_tester_60pct.vil.json](qw-file://workspace/artifacts/switch_tester_60pct.vil.json)


## What's in it:


- **Layer 0** — Normal ANSI 60% layout
- **Layer 1** — Testing layer: every key fires a macro that types the switch name + Enter
- **Fn key** (bottom row, 2nd from right) — `TG(1)` toggles between normal and testing layer
- **60 macros** pre-filled with example switch names (Linear/Tactile/Clicky varieties)
- Only using **36% of the 4KB buffer** — plenty of room for longer descriptions


## Important note:


Vial's `.vil` save files are UID-locked to a specific keyboard. Since I don't know your board's UID, you won't be able to directly "Load Saved Layout" from this file. Instead, use it as a **reference map** — it shows:


- Which macro number → which key position
- The layer structure
- Example switch text for each position


You'll set it up in Vial manually (takes ~10 min), or if you share your board's `.vil` export I can patch the UID in.


## Quick setup steps:


1. Reflash with the `config.h` additions (macro count + buffer size)
2. Open Vial → set Layer 1 keys to M(0) through M(59), skipping Fn
3. Fill macros with your actual switch names
4. Toggle Fn to enter/exit test mode


Want me to reformat this as a simpler CSV/spreadsheet mapping instead, or adjust any of the example switch names?


> **Tool call:** `run_python`
> ```
> Total keys: 61
> Macros used: 60
> Total macro buffer usage: ~1484 bytes / 4096 bytes (36% used)
>
> Saved to: /Users/ross/.quickwork/profiles/federate-prod/sessions/f21c02a7-4a0b-4538-8c4e-ad92889134c5/workspace/artifacts/switch_tester_60pct.vil.json
> ```


> **Tool call:** `open_in_session_tab`
> ```
> <artifact type="canvas" doc_type="json" file_path="workspace/artifacts/switch_tester_60pct.vil.json" title="Switch Tester Layout" />
> ```


---


## User
*6/29/2026, 2:21:17 PM*


here is the KLE json.  [["~\n`","!\n1","@\n2","#\n3","$\n4","%\n5","^\n6","&\n7","*\n8","(\n9",")\n0","_\n-","+\n=",{"w":2},"Backspace"],
[{"w":1.5},"Tab","Q","W","E","R","T","Y","U","I","O","P","{\n[","}\n]",{"w":1.5},"|\n\\"],
[{"w":1.75},"Caps Lock","A","S","D","F","G","H","J","K","L",":\n;","\"\n'",{"w":2.25},"Enter"],
[{"w":2.25},"Shift","Z","X","C","V","B","N","M","<\n,",">\n.","?\n/",{"w":2.75},"Shift"],
[{"w":1.25},"Ctrl",{"w":1.25},"Win",{"w":1.25},"Alt",{"a":0,"w":6.25},"",{"a":4,"w":1.25},"Alt",{"w":1.25},"Win",{"w":1.25},"Menu",{"w":1.25},"Ctrl"]]


---


## Assistant
*6/29/2026, 2:21:17 PM*


Here's the updated layout based on your KLE — [switch_tester_60pct.vil.json](qw-file://workspace/artifacts/switch_tester_60pct.vil.json)


## What's in it:


- **Your exact KLE** embedded for reference
- **Layer 0** — Standard ANSI 60%
- **Layer 1** — Testing layer with M(0)–M(59) mapped to each key
- **Menu key** (bottom row, 2nd from right) → `TG(1)` to toggle in/out of test mode
- **60 macros** pre-filled with example switches, mapped by row
- **33% buffer used** — tons of headroom


## The macro map is organized by row so you can quickly see:


```
Row 0: M(0)=Esc/~ ... M(13)=Backspace
Row 1: M(14)=Tab  ... M(27)=Backslash
Row 2: M(28)=Caps ... M(40)=Enter
Row 3: M(41)=LShift ... M(52)=RShift
Row 4: M(53)=LCtrl ... M(59)=TG(1) ... M(59)=RCtrl
```


Since Vial `.vil` files are UID-locked to a specific board, you'll use this as your programming reference. If you export your board's `.vil` and send it to me, I can inject the macros directly into that file format.


Want me to swap any of the example switch names, or change the layer toggle to a different key?


> **Tool call:** `run_python`
> ```
> Total keys: 61
>    0: ~            (1.0u) - Row 0
>    1: !            (1.0u) - Row 0
>    2: @            (1.0u) - Row 0
>    3: #            (1.0u) - Row 0
>    4: $            (1.0u) - Row 0
>    5: %            (1.0u) - Row 0
>    6: ^            (1.0u) - Row 0
>    7: &            (1.0u) - Row 0
>    8: *            (1.0u) - Row 0
>    9: (            (1.0u) - Row 0
>   10: )            (1.0u) - Row 0
>   11: _            (1.0u) - Row 0
>   12: +            (1.0u) - Row 0
>   13: Backspace    (2u) - Row 0
>   14: Tab  ...
> ```


> **Tool call:** `run_python`
> ```
> Macros: 60
> Buffer usage: 1362 / 4096 bytes (33%)
> Layer toggle key: Menu (position 59) -> TG(1)
>
> Saved: /Users/ross/.quickwork/profiles/federate-prod/sessions/f21c02a7-4a0b-4538-8c4e-ad92889134c5/workspace/artifacts/switch_tester_60pct.vil.json
> ```


> **Tool call:** `open_in_session_tab`
> ```
> <artifact type="canvas" doc_type="json" file_path="workspace/artifacts/switch_tester_60pct.vil.json" title="Switch Tester 60% Layout" />
> ```


---


## User
*6/29/2026, 2:24:11 PM*


i would like to seperate clicky, tactile, linear per row - as much as possible and then descending activation force


---


## Assistant
*6/29/2026, 2:24:11 PM*


Done! Here's the reorganized layout — [switch_tester_60pct.vil.json](qw-file://workspace/artifacts/switch_tester_60pct.vil.json)


## Organization:


| Row | Type | Keys | Force Range |
|-----|------|------|-------------|
| **Row 0** (Number) | 🔵 Clicky | 14 | 80g → 45g |
| **Row 1** (QWERTY) | 🟣 Tactile | 14 | 78g → 62g |
| **Row 2** (Home) | 🟣 Tactile | 13 | 62g → 37g |
| **Row 3** (Bottom) | 🔴 Linear | 12 | 67g → 55g |
| **Row 4** (Mods) | 🔴 Linear | 7 | 50g → 40g |


Heaviest on the left, lightest on the right within each row. Tactile gets two rows (27 switches) since that's usually the largest category people want to compare.


**43% buffer used** — still plenty of room if you want to add more detail to the strings (like "lubed" or spring weight variants).


The macro output includes the force in the string too, e.g. pressing the `Q` key outputs:
> `Tactile - Tungsten (68g)`


Want me to swap any of the specific switches, adjust the type distribution across rows, or change the output format?


> **Tool call:** `run_python`
> ```
> Clicky: 14 (Row 0)
> Tactile: 27 (Row 1 + Row 2)
> Linear: 19 (Row 3 + Row 4)
> Total: 60
>
> ======================================================================
> ROW 0 - CLICKY (Number Row) - Heaviest → Lightest
> ======================================================================
>   M( 0) | Esc/~      → Clicky - Cherry MX Green (80g)
>   M( 1) | 1          → Clicky - Kailh Box Navy (75g)
>   M( 2) | 2          → Clicky - Kailh Box Jade (70g)
>   M( 3) | 3          → Clicky - Kailh Box Noble Yellow (65g)
>   ...
> ```


> **Tool call:** `run_python`
> ```
> Saved: /Users/ross/.quickwork/profiles/federate-prod/sessions/f21c02a7-4a0b-4538-8c4e-ad92889134c5/workspace/artifacts/switch_tester_60pct.vil.json
> ```


> **Tool call:** `open_in_session_tab`
> ```
> <artifact type="canvas" doc_type="json" file_path="workspace/artifacts/switch_tester_60pct.vil.json" title="Switch Tester 60% Layout" />
> ```


---


## User
*6/29/2026, 2:28:29 PM*


THis is good work.  thanks - will try buiding the board firmware later


---


## Assistant
*6/29/2026, 2:28:30 PM*


Sounds good! Have fun with the build. When you're ready to flash, the two `config.h` lines are all you need — then it's just macro entry in Vial.


Let me know if you hit any snags with the firmware or want to tweak the switch list once you've decided what's going in each position. 🤙


---


## User
*6/29/2026, 2:30:06 PM*


oh i still wan the enter at the end of each line


---


## Assistant
*6/29/2026, 2:30:07 PM*


Done! Every macro now ends with Enter so each keypress outputs on its own line. Still only 44% buffer — plenty of room. The file's updated: [switch_tester_60pct.vil.json](qw-file://workspace/artifacts/switch_tester_60pct.vil.json)


> **Tool call:** `run_python`
> ```
> Done - all macros now end with Enter (\n)
> Buffer: 1842 / 4096 bytes (44%)
>
> Example output: Clicky - Cherry MX Green (80g)\n
> ```


---


Filter keys or values...




{
_readme: "Switch Tester 60% - Organized by Type & Force"
_organization: {
row_0_number_row: "CLICKY - 80g down to 45g (left to right)"
row_1_qwerty_row: "TACTILE - 78g down to 62g"
row_2_home_row: "TACTILE (cont.) - 62g down to 37g"
row_3_bottom_row: "LINEAR - 67g down to 55g"
row_4_mod_row: "LINEAR (cont.) - 50g down to 40g"
layer_toggle: "Menu key (pos 59) = TG(1) — toggle test layer"
}
config_h: [
0: "#define DYNAMIC_KEYMAP_MACRO_COUNT 64"
1: "#define DYNAMIC_KEYMAP_MACRO_BUFFER_SIZE 4096"
]
kle: [
0: [...]
1: [...]
2: [...]
3: [...]
4: [...]
]
layers: {
layer_0_normal: [...]
layer_1_testing: [...]
}
macros: {
M(0): "Clicky - Cherry MX Green (80g)\n"
M(1): "Clicky - Kailh Box Navy (75g)\n"
M(2): "Clicky - Kailh Box Jade (70g)\n"
M(3): "Clicky - Kailh Box Noble Yellow (65g)\n"
M(4): "Clicky - NovelKeys Sherbet (65g)\n"
M(5): "Clicky - Cherry MX White (55g)\n"
M(6): "Clicky - Kailh Box Pink (55g)\n"
M(7): "Clicky - Gateron Blue (55g)\n"
M(8): "Clicky - Cherry MX Blue (50g)\n"
M(9): "Clicky - Kailh Speed Gold (50g)\n"
M(10): "Clicky - Kailh Speed Bronze (50g)\n"
M(11): "Clicky - Outemu Blue (50g)\n"
M(12): "Clicky - Kailh Pro Light Green (50g)\n"
M(13): "Clicky - Kailh Box White (45g)\n"
M(14): "Tactile - Zealio V2 78g (78g)\n"
M(15): "Tactile - Tungsten (68g)\n"
M(16): "Tactile - Holy Panda (67g)\n"
M(17): "Tactile - Durock T1 (67g)\n"
M(18): "Tactile - Glorious Panda (67g)\n"
M(19): "Tactile - Zealio V2 67g (67g)\n"
M(20): "Tactile - SP Star Meteor White (67g)\n"
M(21): "Tactile - Cherry MX Clear (65g)\n"
M(22): "Tactile - Anubis (65g)\n"
M(23): "Tactile - Azure Dragon (63g)\n"
M(24): "Tactile - Moyu Black (63g)\n"
M(25): "Tactile - Wuque Studio Aurora (63g)\n"
M(26): "Tactile - Virtue (63g)\n"
M(27): "Tactile - Boba U4T (62g)\n"
M(28): "Tactile - Durock Sunflower (62g)\n"
M(29): "Tactile - Ergo Clear (62g)\n"
M(30): "Tactile - Pewter (60g)\n"
M(31): "Tactile - Coffee Chip (55g)\n"
M(32): "Tactile - KTT Mallo (55g)\n"
M(33): "Tactile - Akko CS Lavender Purple (50g)\n"
M(34): "Tactile - Akko CS Sponge (48g)\n"
M(35): "Tactile - Cherry MX Brown (45g)\n"
M(36): "Tactile - Gateron Brown (45g)\n"
M(37): "Tactile - Outemu Brown (45g)\n"
M(38): "Tactile - Gateron Low Profile Brown (45g)\n"
M(39): "Tactile - TTC Bluish White (42g)\n"
M(40): "Tactile - TTC Gold Pink (37g)\n"
M(41): "Linear - Tangerine 67g (67g)\n"
M(42): "Linear - Tealio V2 (67g)\n"
M(43): "Linear - Lavender (65g)\n"
M(44): "Linear - Durock L7 62g (62g)\n"
M(45): "Linear - Alpaca V2 (62g)\n"
M(46): "Linear - Banana Split (62g)\n"
M(47): "Linear - Cherry MX Black (60g)\n"
M(48): "Linear - H1 (60g)\n"
M(49): "Linear - Black Ink V2 (60g)\n"
M(50): "Linear - NK Cream (55g)\n"
M(51): "Linear - Gateron Oil King (55g)\n"
M(52): "Linear - Aqua King (55g)\n"
M(53): "Linear - Gateron Milky Yellow (50g)\n"
M(54): "Linear - WS Morandi (50g)\n"
M(55): "Linear - Cherry MX Red (45g)\n"
M(56): "Linear - Gateron CJ (45g)\n"
M(57): "Linear - KTT Strawberry (45g)\n"
M(58): "Linear - Cherry MX Silent Red (45g)\n"
M(59): "Linear - Kailh Speed Silver (40g)\n"
}
macro_map: {
row_0_CLICKY: [...]
row_1_TACTILE: [...]
row_2_TACTILE: [...]
row_3_LINEAR: [...]
row_4_LINEAR: [...]
}
buffer_usage: "1842 / 4096 bytes (44%)"
}

