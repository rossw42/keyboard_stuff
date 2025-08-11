# Ergogen Toolkit

A comprehensive VSCode extension that provides a complete toolkit for Ergogen keyboard design workflows, including build automation, DXF viewing, and planned JSCAD support.

## Features

- **Run Ergogen**: Execute Ergogen directly from VSCode with keyboard shortcuts
- **DXF Viewer**: Interactive viewer for generated DXF files with zoom, pan, and layer controls
- **Auto-refresh**: Automatically refresh the viewer when DXF files change
- **Layer Management**: Toggle visibility of different DXF layers
- **Grid & Dimensions**: Optional grid display and dimension annotations
- **File Management**: Browse and switch between multiple DXF files
- **Future JSCAD Support**: Planned support for viewing 3D JSCAD models

## Usage

1. Open a workspace containing Ergogen YAML files
2. Use `Ctrl+Shift+E` (or `Cmd+Shift+E` on Mac) to run Ergogen
3. Use `Ctrl+Shift+D` (or `Cmd+Shift+D` on Mac) to open the DXF viewer
4. Browse generated DXF files in the sidebar and click to view them

## Commands

- `Ergogen: Run Ergogen` - Execute Ergogen on the current YAML file
- `Ergogen: Open DXF Viewer` - Open the integrated DXF viewer
- `Ergogen: Refresh DXF Viewer` - Refresh the file list and viewer
- `Ergogen: Fit DXF to Window` - Fit the current DXF to the viewer window

## Configuration

- `ergogen-toolkit.autoRefresh` - Auto-refresh viewer when files change
- `ergogen-toolkit.autoRunErgogen` - Auto-run Ergogen when YAML files are saved
- `ergogen-toolkit.ergogenCommand` - Command to run Ergogen (default: "ergogen")
- `ergogen-toolkit.outputDirectory` - Output directory name (default: "output")
- `ergogen-toolkit.theme` - Viewer color theme (dark/light/auto)
- `ergogen-toolkit.lineWidth` - Line width for DXF rendering
- `ergogen-toolkit.gridEnabled` - Show grid in viewer

## Requirements

- Ergogen must be installed and available in your PATH
- VSCode 1.74.0 or higher

## Installation

1. Package the extension: `npm run package`
2. Install the generated `.vsix` file in VSCode

## Development

```bash
npm install
npm run compile
```

## License

MIT
