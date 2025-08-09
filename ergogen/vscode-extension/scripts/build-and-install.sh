#!/bin/bash

# Simple script to build and install the VSCode extension

echo "🚀 Building and Installing Ergogen DXF Viewer Extension"
echo "====================================================="

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the vscode-extension directory"
    exit 1
fi

# Check if @vscode/vsce is installed
if ! command -v vsce &> /dev/null; then
    echo "📦 Installing @vscode/vsce (VSCode Extension Manager)..."
    npm install -g @vscode/vsce
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Package the extension
echo "📦 Packaging extension..."
./scripts/package-extension.sh

# Build VSIX
echo "🔨 Building VSIX package..."
vsce package

# Get the VSIX file name
VSIX_FILE=$(ls *.vsix | head -n 1)

if [ -z "$VSIX_FILE" ]; then
    echo "❌ Error: No VSIX file found"
    exit 1
fi

echo "✅ Extension built: $VSIX_FILE"
echo ""
echo "🚀 To install in VSCode:"
echo "  1. Open VSCode"
echo "  2. Press Ctrl+Shift+P (or Cmd+Shift+P on Mac)"
echo "  3. Type 'Extensions: Install from VSIX'"
echo "  4. Select the file: $VSIX_FILE"
echo "  5. Restart VSCode"
echo ""
echo "🎯 To use:"
echo "  1. Open an Ergogen project in VSCode"
echo "  2. Press Ctrl+Shift+P"
echo "  3. Type 'Ergogen: Open DXF Viewer'"
echo ""
echo "💡 Alternative: Use the standalone viewer with:"
echo "  cd ../.. && ./start_dev.sh /path/to/keyboard/output"