# 🎹 Live QMK Keymap Visualizer

A simple tool to visualize and monitor your QMK keymap.c files in real-time.

## 🚀 Quick Start

1. **Run the watcher:**
   ```bash
   python watch_keymap.py
   ```

2. **Select your keymap** from the list (e.g., 3x4, lily58, macropad)

3. **Open browser** to: `http://localhost:8000`

4. **Edit your keymap.c file** and save - watch it update live!

## ✨ Features

- **🔍 Auto-discovery** - Finds all keymap.c files in your project
- **🎯 Focused viewing** - Watch one specific keymap at a time
- **🎨 Visual layout** - See your keys in a grid with color coding
- **📱 Layer switching** - Click tabs to view different layers
- **🔗 Combo display** - Shows key combinations
- **⚡ Live updates** - Automatically refreshes when you save changes
- **📝 Raw view** - See the actual C code alongside the visualization

## 🎨 Color Coding

- **🟠 Orange**: Modifiers (Backspace, Enter, Shift, etc.)
- **🔵 Blue**: Function keys (F1-F12)
- **🟣 Purple**: Media keys (Volume, Play, Stop, etc.)
- **🔴 Pink**: RGB lighting controls
- **⚪ Gray**: Regular keys (letters, numbers)

## 🎮 Keyboard Shortcuts

- **Ctrl+R**: Refresh content
- **Ctrl+Space**: Pause/Resume auto-updates

## 📁 Supported Layouts

Works with any QMK keymap.c file! Automatically detects:
- Grid layouts (3x4, 4x2, etc.)
- Split keyboards (Lily58, etc.)
- Macropads
- Custom layouts

## 🛠️ Requirements

- **Python 3.x**
- **Modern web browser**

## 💡 Usage Tips

1. **Keep the Python script running** while you edit
2. **Save your keymap.c file** to see changes
3. **Use layer tabs** to switch between different layers
4. **Check combos section** to see key combinations
5. **Copy content** button to grab the raw keymap code

## 🎯 Perfect For

- **Keymap development** - See changes as you code
- **Layout planning** - Visual feedback while designing
- **Learning QMK** - Understand layer structures
- **Debugging** - Quickly spot issues in your layout

---

**Happy keymap coding!** 🎹✨