# QMK Utilities

A collection of utilities for working with QMK (Quantum Mechanical Keyboard) firmware, because apparently converting between keyboard formats is harder than rocket science. These are just cool ideas I have - do they always work out? No. But thinking you can conquer all the formats is fun... right?

> **Reality Check**: Half of these tools work most of the time, the other half work some of the time, and I'm still figuring out which is which. Welcome to the wonderful world of keyboard format conversion! 🎹

## What's Actually In This Folder (For Real This Time)

### [`ascii_keymap_gen/`](ascii_keymap_gen/) ✅ **Actually Works!**
Generates ASCII art of keyboard layouts because sometimes you need to see your keymap in glorious monospace font. Supports 18+ keyboards and has the rare distinction of actually doing what it says on the tin. No external dependencies, no drama, just pure ASCII art goodness. Working on supporting more keyboard layouts.

### [`qmk_format_converter/`](qmk_format_converter/) 🔧 **Mostly Works (With Caveats)**
Converts between keyboard formats with the enthusiasm of a tired seagull. Sometimes it works perfectly, sometimes it counts wrong, sometimes it forgets how parentheses work. But hey, when it works, it's magical! Features "automatic" format detection and a universal data model that's more like guidelines than actual rules... and forgets about the number of keys in a keyboard randomly.

## Contributing

Found a bug? Great, you're paying attention! PRs welcome, especially if you can fix the things I broke while trying to fix other things. Bonus points if you can explain why my regex patterns look like they were written by a caffeinated octopus.

## License

MIT License - because if you're brave enough to use this code, you deserve the freedom to modify it when it inevitably breaks. See [LICENSE](LICENSE) file for the legal stuff.
---

