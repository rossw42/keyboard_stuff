# Ergogen DXF Viewer - VSCode Extension

Integrate DXF file viewing directly into VSCode for seamless Ergogen keyboard development.

## ✨ Features

- **🎯 Integrated DXF Viewer** - View DXF files directly in VSCode panels
- **🔄 Auto-Detection** - Automatically detects Ergogen projects
- **⚡ Real-time Updates** - Auto-refresh when DXF files change
- **🚀 Ergogen Integration** - Run Ergogen commands from VSCode
- **📱 Split View** - YAML config on one side, DXF preview on the other

## 🚀 Quick Start

1. **Install Extension** (when published to marketplace)
2. **Open Ergogen Project** - Open a workspace with `.yaml` config files
3. **Open DXF Viewer** - Command Palette → "Ergogen: Open DXF Viewer"
4. **Edit & Preview** - Edit YAML, run Ergogen, see results instantly

## 📋 Commands

- `Ergogen: Open DXF Viewer` - Open the DXF viewer panel
- `Ergogen: Run Ergogen` - Execute Ergogen on current YAML file
- `Ergogen: Refresh DXF Viewer` - Manually refresh the viewer

## ⚙️ Settings

- `ergogen-dxf-viewer.autoRefresh` - Auto-refresh viewer when files change
- `ergogen-dxf-viewer.autoRunErgogen` - Auto-run Ergogen when YAML saved
- `ergogen-dxf-viewer.backendPort` - Port for the DXF viewer backend
- `ergogen-dxf-viewer.ergogenCommand` - Command to run Ergogen

## 🎯 Workflow

```
┌─────────────────┬─────────────────┐
│ keyboard.yaml   │ DXF Viewer      │
│                 │                 │
│ points:         │ [Switch Plate]  │
│   key:          │                 │
│     spread: 19  │ ○ ○ ○ ○ ○      │
│     stagger: 5  │ ○ ○ ○ ○ ○      │
│                 │ ○ ○ ○ ○ ○      │
│ [Save] → Auto   │ [Auto-refresh]  │
│ runs Ergogen    │                 │
└─────────────────┴─────────────────┘
```

## 🔧 Development

This extension bundles the DXF viewer backend and frontend:

- **Backend**: Python Flask server (from `../backend/`)
- **Frontend**: React application (from `../frontend/`)
- **Extension**: TypeScript VSCode extension

## 📦 Installation

### From Source
```bash
cd vscode-extension
npm install
npm run compile
# Install in VSCode: Extensions → Install from VSIX
```

### From Marketplace
Search for "Ergogen DXF Viewer" in VSCode Extensions

## 🤝 Contributing

This extension is part of the larger DXF Viewer project. See the main README for contribution guidelines.

## 📄 License

MIT License - See LICENSE file for details.