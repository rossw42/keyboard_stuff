#!/bin/bash

echo "🚀 Building Simple Ergogen Extension"
echo "===================================="

# Backup original files
if [ -f "package.json" ]; then
    cp package.json package.json.backup
fi

if [ -f "src/extension.ts" ]; then
    cp src/extension.ts src/extension.ts.backup
fi

# Use simple versions
cp package-simple.json package.json
cp src/extension-simple.ts src/extension.ts

# Create output directory
mkdir -p out

# Compile TypeScript
echo "📦 Compiling TypeScript..."
npx tsc src/extension.ts --outDir out --target es2020 --module commonjs --lib es2020 --declaration --strict

if [ $? -ne 0 ]; then
    echo "❌ TypeScript compilation failed"
    exit 1
fi

# Try to package with vsce (skip if not available)
if command -v vsce &> /dev/null; then
    echo "📦 Creating VSIX package..."
    vsce package --no-dependencies
    
    if [ $? -eq 0 ]; then
        VSIX_FILE=$(ls *.vsix | head -n 1)
        echo "✅ Extension built: $VSIX_FILE"
        echo ""
        echo "🚀 To install:"
        echo "  1. Open VSCode"
        echo "  2. Ctrl+Shift+P → 'Extensions: Install from VSIX'"
        echo "  3. Select: $VSIX_FILE"
    else
        echo "⚠️  VSIX packaging failed, but TypeScript compiled successfully"
        echo "📁 Compiled files are in the 'out' directory"
    fi
else
    echo "⚠️  vsce not available, but TypeScript compiled successfully"
    echo "📁 Compiled files are in the 'out' directory"
    echo ""
    echo "💡 To install vsce: npm install -g @vscode/vsce"
fi

# Restore original files
if [ -f "package.json.backup" ]; then
    mv package.json.backup package.json
fi

if [ -f "src/extension.ts.backup" ]; then
    mv src/extension.ts.backup src/extension.ts
fi

echo ""
echo "🎯 This simple extension provides:"
echo "  • Command: 'Ergogen: Run Ergogen' (Ctrl+Shift+E)"
echo "  • Command: 'Ergogen: Open DXF Viewer'"
echo "  • Auto-detection of Ergogen projects"
echo ""
echo "💡 Make sure to start the DXF viewer first:"
echo "  cd ../.. && ./start_dev.sh /path/to/your/keyboard/output"