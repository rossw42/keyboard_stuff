# 🎯 Quick Usage Guide

## Watch a Specific Keymap File

### Option 1: Interactive Menu (Recommended)
```bash
# Windows
.\start_keymap_viewer.bat

# PowerShell (any OS)
pwsh .\start_keymap_viewer.ps1
```

This will show you a menu like:
```
📁 Available keymaps:

  1. macropad\keymaps\default\keymap.c
  2. 4x2\keymaps\2rows-with-encoder\keymap.c
  3. lily58\keymaps\default\keymap.c
  4. lily58\keymaps\lily58l\keymap.c
  5. 4x2\keymaps\2rows-no-encoder\keymap.c
  6. lily58-hold\hold\keymaps\default\keymap.c

Enter number (1-6) or press Enter to watch all:
```

### Option 2: Direct File Specification
```bash
# Watch a specific file directly
python keymap_server.py --file "lily58/keymaps/default/keymap.c"

# Or with batch file
.\start_keymap_viewer.bat "lily58/keymaps/default/keymap.c"
```

### Option 3: Command Line Arguments
```bash
# Specify port and file
python keymap_server.py --file "macropad/keymaps/default/keymap.c" --port 8080
```

## What You'll See

1. **Server starts** and shows which file it's watching
2. **Browser opens** to `http://localhost:8000/keymap_visualization.html`
3. **Top-right indicator** shows "🎯 Watching: keymap.c"
4. **Edit your keymap.c file** and save
5. **Page automatically refreshes** with your changes!

## Live Workflow

1. Choose your keymap file (e.g., lily58 default)
2. Start the watcher: `.\start_keymap_viewer.bat`
3. Select option 3 for lily58 default
4. Open the webpage in your browser
5. Edit `lily58/keymaps/default/keymap.c` in your favorite editor
6. Save the file
7. Watch the visualization update automatically!

Perfect for iterating on keymap designs! 🎹✨