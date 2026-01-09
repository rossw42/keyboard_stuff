# 🎹 Interactive QMK Keymap Visualizer

A live-updating visualization tool for your QMK keymap.c files that automatically refreshes when you make changes.

## 🚀 Quick Start

### Option 1: Simple (File-based)
Just open `keymap_visualization.html` in your browser. It will work as a static visualization.

### Option 2: Live Updates (Recommended)
1. **Windows**: Double-click `start_keymap_viewer.bat`
2. **Manual**: Run `python keymap_server.py`
3. Open http://localhost:8000/keymap_visualization.html

## ✨ Features

### 🔄 Auto-Refresh
- Automatically detects changes to keymap.c files
- Refreshes the visualization when files are modified
- Works with any QMK keymap in your directory structure

### 🎮 Interactive Controls
- **🔄 Refresh Now**: Manual refresh button
- **⏸️ Pause/Resume**: Toggle auto-updates
- **📁 Load File**: Import keymap.c files directly
- **Keyboard Shortcuts**:
  - `Ctrl/Cmd + R`: Refresh
  - `Ctrl/Cmd + Space`: Pause/Resume

### 📊 Visual Features
- Color-coded keys (modifiers, layers, special functions)
- Split keyboard layouts properly displayed
- Encoder functions shown for each layer
- OLED and RGB feature indicators
- Live update status indicator

## 🛠️ How It Works

1. **File Watching**: Python script monitors keymap.c files for changes
2. **Live Updates**: Web interface polls for changes every 3 seconds
3. **Auto-Refresh**: Page automatically reloads when changes detected
4. **Fallback Mode**: Works offline with manual refresh

## 📁 Supported Files

The visualizer automatically detects these keymap files:
- `macropad/keymaps/default/keymap.c`
- `4x2/keymaps/2rows-with-encoder/keymap.c`
- `lily58/keymaps/default/keymap.c`
- `lily58/keymaps/lily58l/keymap.c`
- `4x2/keymaps/2rows-no-encoder/keymap.c`
- `lily58-hold/hold/keymaps/default/keymap.c`

## 🔧 Requirements

- **Python 3.x** (for live updates)
- **watchdog** package (auto-installed)
- **Modern web browser**

## 💡 Usage Tips

1. **Edit your keymap.c files** in your favorite editor
2. **Save the file** - the visualizer will detect the change
3. **Watch the live indicator** turn orange, then green
4. **See your changes** reflected automatically

## 🎯 Perfect For

- **Keymap Development**: See changes as you code
- **Layout Planning**: Visual feedback while designing
- **Documentation**: Share live layouts with others
- **Learning QMK**: Understand layer structures visually

## 🚨 Troubleshooting

**Server won't start?**
- Make sure Python is installed
- Run `pip install watchdog`

**Changes not detected?**
- Check the file paths match your structure
- Ensure you're saving the .c files
- Try manual refresh (Ctrl+R)

**Page won't load?**
- Try opening the HTML file directly
- Check if port 8000 is available
- Use a different port: `python keymap_server.py 8080`

---

*Happy keymap coding! 🎹✨*