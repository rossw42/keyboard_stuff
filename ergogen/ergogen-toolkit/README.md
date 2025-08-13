# 🎹 Ergogen Toolkit

*Because life's too short for bad keyboard layouts and even shorter for squinting at DXF files in text editors.*

A delightfully simple VS Code extension that makes working with [Ergogen](https://ergogen.xyz) keyboard configurations actually enjoyable. No more switching between seventeen different applications just to see if your keyboard looks like a keyboard or abstract art.

## ✨ Features That Actually Work

### 🚀 One-Click Ergogen Execution
- Hit `Ctrl+Shift+E` (or `Cmd+Shift+E` on Mac) and watch the magic happen
- Or click the shiny ▶ button that appears when you're editing YAML files
- No more terminal gymnastics or remembering cryptic command flags

### 🎨 Professional DXF Viewer
- **Sidebar layout** with file list on the left (like a civilized human interface)
- **Actual graphics rendering** - see your keyboard layouts as beautiful SVG graphics, not hieroglyphics
- **Entity information** - know exactly how many lines, arcs, and circles make up your masterpiece
- **Click to switch** between different DXF files faster than you can say "split keyboard"

### 🔄 Smart Workflow Integration
- **Run Ergogen** button right in the DXF viewer (because context switching is for quitters)
- **Refresh** button to instantly see your latest changes
- **Automatic file detection** - finds your DXF files wherever Ergogen decides to put them

## 🎯 What This Extension Actually Does

1. **Runs Ergogen** on your YAML files without you having to remember command line syntax
2. **Shows you the results** in a viewer that doesn't make your eyes bleed
3. **Gets out of your way** so you can focus on designing the keyboard of your dreams

*It's like having a very polite assistant who only does exactly what you need and never suggests you upgrade to the premium version.*

## 📦 Installation

### From VS Code Marketplace (Coming Soon™)
1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for "Ergogen Toolkit"
4. Click Install
5. Start designing keyboards like a pro

### From VSIX (For the Adventurous)
1. Download the `.vsix` file
2. Open VS Code
3. `Ctrl+Shift+P` → "Extensions: Install from VSIX"
4. Select the file
5. Profit! 💰

## 🚀 Quick Start

1. **Open your Ergogen YAML file** (you know, the one with all the keyboard magic)
2. **Press `Ctrl+Shift+E`** to run Ergogen
3. **Press `Ctrl+Shift+D`** to open the DXF viewer
4. **Marvel at your creation** in glorious vector graphics
5. **Iterate** until your keyboard is perfect (or until you run out of coffee)

## ⚙️ Configuration

The extension is designed to work out of the box, but if you're the tweaking type:

```json
{
  "ergogen-toolkit.ergogenCommand": "ergogen",
  "ergogen-toolkit.outputDirectory": "output"
}
```

- `ergogenCommand`: How to invoke Ergogen (default: `"ergogen"`)
- `outputDirectory`: Where to look for output files (default: `"output"`)

*Pro tip: If you installed Ergogen via npm, you might need `"npx ergogen"` instead.*

## 🎮 Keyboard Shortcuts

| Shortcut | Action | When |
|----------|--------|------|
| `Ctrl+Shift+E` | Run Ergogen | YAML file is open |
| `Ctrl+Shift+D` | Open DXF Viewer | Anytime |

*Mac users: Replace `Ctrl` with `Cmd` because Apple likes to be different.*

## 🐛 Troubleshooting

### "Ergogen command not found"
- Make sure Ergogen is installed: `npm install -g ergogen`
- Or use the full path in settings: `"ergogen-toolkit.ergogenCommand": "/path/to/ergogen"`

### "No DXF files found"
- Run Ergogen first (the extension will remind you)
- Check that your YAML file actually generates DXF output
- Make sure you're not in a parallel universe where DXF files don't exist

### "The viewer shows weird text instead of graphics"
- You're probably looking at the raw DXF file in VS Code's text editor
- Use `Ctrl+Shift+D` to open the proper DXF viewer instead
- Trust us, it's much prettier

## 🎨 What Makes This Special

Unlike other solutions that shall remain nameless, this extension:

- ✅ **Actually renders DXF files** as graphics (revolutionary!)
- ✅ **Has a proper sidebar layout** (not a popup from 1995)
- ✅ **Integrates with your workflow** (no app switching required)
- ✅ **Doesn't crash** when you look at it funny
- ✅ **Follows VS Code design patterns** (it actually looks like it belongs)

## 🏗️ For Developers

Built with:
- **JavaScript** (because TypeScript is for people who have time)
- **VS Code Extension API** (surprisingly well-documented)
- **SVG rendering** (because vector graphics are beautiful)
- **Love and caffeine** (the two essential ingredients)

## 📝 Changelog

### 4.0.0 - "The Great Awakening"
- 🎉 **Complete rewrite** of the DXF viewer
- ✨ **Professional sidebar layout** (goodbye, annoying popups!)
- 🎨 **Actual SVG rendering** of DXF files
- 🔄 **Integrated Run Ergogen button** in the viewer
- 🔄 **Refresh functionality** for instant updates
- 🎯 **Smart directory detection** (finds your files wherever they hide)
- 🐛 **Fixed approximately 47 bugs** (we stopped counting)

### 3.x and below
- *We don't talk about the dark times*

## 🤝 Contributing

Found a bug? Have a feature request? Want to make keyboards even more awesome?

1. **Open an issue** on GitHub (be nice, we're sensitive)
2. **Submit a PR** (we love good code)
3. **Share your keyboard designs** (we love seeing what you create)

## 📄 License

MIT License - because sharing is caring and lawyers are expensive.

## 🙏 Acknowledgments

- **Ergogen** - for making keyboard design accessible to mere mortals
- **The VS Code team** - for creating an actually extensible editor
- **Coffee** - for making this extension possible
- **You** - for reading this far (seriously, thanks!)

---

*Made with ❤️ and an unhealthy obsession with keyboard layouts.*

**Happy typing!** 🎹✨