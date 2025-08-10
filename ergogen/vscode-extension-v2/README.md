# Ergogen DXF Viewer

A VSCode extension that provides integrated DXF viewing capabilities for Ergogen keyboard design workflows.

## Features

- **Run Ergogen**: Execute Ergogen directly from VSCode with keyboard shortcuts
- **DXF Viewer**: Interactive viewer for generated DXF files with zoom, pan, and layer controls
- **Auto-refresh**: Automatically refresh the viewer when DXF files change
- **Layer Management**: Toggle visibility of different DXF layers
- **Grid & Dimensions**: Optional grid display and dimension annotations
- **File Management**: Browse and switch between multiple DXF files

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

- `ergogen-dxf-viewer.autoRefresh` - Auto-refresh viewer when files change
- `ergogen-dxf-viewer.autoRunErgogen` - Auto-run Ergogen when YAML files are saved
- `ergogen-dxf-viewer.ergogenCommand` - Command to run Ergogen (default: "ergogen")
- `ergogen-dxf-viewer.outputDirectory` - Output directory name (default: "output")
- `ergogen-dxf-viewer.theme` - Viewer color theme (dark/light/auto)
- `ergogen-dxf-viewer.lineWidth` - Line width for DXF rendering
- `ergogen-dxf-viewer.gridEnabled` - Show grid in viewer
- `ergogen-dxf-viewer.showDimensions` - Show dimensions and text

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