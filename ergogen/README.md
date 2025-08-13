# Ergogen Toolkit

A simple VS Code extension for Ergogen keyboard design workflow. Run Ergogen on YAML files and view DXF output files.

## 🎯 Core Functions

This extension has **two simple functions**:

1. **Run Ergogen** - Execute ergogen command on YAML files
2. **View DXF Files** - Open DXF files using your system's default viewer

That's it. No complexity, no heavy dependencies, just the essentials.

## 🚀 Quick Start

1. **Install the extension**
2. **Open a YAML file** (keyboard config)
3. **Run Ergogen**: `Ctrl+Shift+E` or Command Palette → "Run Ergogen"
4. **View DXF files**: `Ctrl+Shift+D` or Command Palette → "Open DXF Viewer"

## 📋 Commands

| Command | Shortcut | Description |
|---------|----------|-------------|
| Run Ergogen | `Ctrl+Shift+E` | Execute ergogen on current YAML file |
| Open DXF Viewer | `Ctrl+Shift+D` | View generated DXF files |

## ⚙️ Configuration

Simple configuration options in VS Code settings:

```json
{
  "ergogen-toolkit.ergogenCommand": "ergogen",  // Command to run (default: "ergogen")
  "ergogen-toolkit.outputDirectory": "output"   // Output directory name (default: "output")
}
```

## 🔧 Requirements

- **Ergogen CLI** installed and available in PATH
- **DXF Viewer** application for viewing files (optional)

### Installing Ergogen

```bash
npm install -g ergogen
```

### DXF Viewers

The extension opens DXF files using your system's default application. Popular options:

- **Windows**: DraftSight, AutoCAD, FreeCAD
- **macOS**: LibreCAD, FreeCAD, AutoCAD
- **Linux**: LibreCAD, FreeCAD, QCAD

## 🎯 How It Works

1. **YAML Detection**: Extension automatically detects YAML files in your workspace
2. **Ergogen Execution**: Runs `ergogen -o <output-dir> <yaml-file>` 
3. **Output Scanning**: Finds generated DXF files in output directory
4. **System Integration**: Opens DXF files with your system's default viewer

## 📁 File Structure

```
Your Project/
├── config.yaml           # Your ergogen config
├── config/               # Generated outputs (named after YAML file)
│   ├── pcbs/
│   │   └── keyboard.dxf  # Generated DXF files
│   └── outlines/
│       └── board.dxf
```

## 🛠️ Troubleshooting

### Ergogen Command Not Found
- Install Ergogen CLI: `npm install -g ergogen`
- Or specify full path in settings: `"ergogen-toolkit.ergogenCommand": "/path/to/ergogen"`

### No DXF Viewer Available
- Install a DXF viewer application
- The extension will show a helpful message with installation guidance

### No YAML Files Found
- Ensure your files have `.yaml` or `.yml` extension
- Open the YAML file in VS Code before running Ergogen

## 🎹 Context Menus

- **YAML files**: Right-click → "Run Ergogen"
- **DXF files**: Right-click → "Open DXF Viewer"

## 📊 Extension Size

This extension is lightweight:
- **Package size**: Under 100KB
- **Dependencies**: None (uses system DXF viewer)
- **Memory usage**: Minimal

## 🔄 Version 4.0.0 - Simplified

This version focuses on the core functionality:

- ✅ Run Ergogen command
- ✅ View DXF files with system viewer
- ❌ Removed complex DXF viewer (use system apps instead)
- ❌ Removed connection diagram generation
- ❌ Removed heavy dependencies

## 📄 License

MIT License - Simple and permissive.

## 🙏 Acknowledgments

- [Ergogen](https://github.com/ergogen/ergogen) - The amazing keyboard design tool
- VS Code team for the excellent extension API

---

**Keep it simple.** This extension does two things well: run Ergogen and open DXF files. Nothing more, nothing less.