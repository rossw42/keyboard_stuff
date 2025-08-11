#!/bin/bash

echo "📦 Creating VSIX Package Manually"
echo "================================="

# Create a temporary directory for the extension
TEMP_DIR="ergogen-dxf-viewer-temp"
rm -rf $TEMP_DIR
mkdir -p $TEMP_DIR/extension

# Copy necessary files to extension subdirectory
echo "📁 Copying extension files..."
cp package-simple.json $TEMP_DIR/extension/package.json
cp -r out $TEMP_DIR/extension/
cp README.md $TEMP_DIR/extension/ 2>/dev/null || echo "# Ergogen DXF Viewer Extension" > $TEMP_DIR/extension/README.md

# Create the proper VSIX manifest
echo "📝 Creating VSIX manifest..."
cat > $TEMP_DIR/\[Content_Types\].xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="json" ContentType="application/json" />
    <Default Extension="js" ContentType="application/javascript" />
    <Default Extension="md" ContentType="text/markdown" />
</Types>
EOF

# Create extension manifest
mkdir -p $TEMP_DIR/META-INF
cat > $TEMP_DIR/META-INF/MANIFEST.MF << 'EOF'
Manifest-Version: 1.0

EOF

# Create a simple VSIX structure (it's just a ZIP file)
echo "🗜️  Creating VSIX archive..."
cd $TEMP_DIR
zip -r ../ergogen-dxf-viewer-0.1.0.vsix . -x "*.DS_Store"
cd ..

# Clean up
rm -rf $TEMP_DIR

if [ -f "ergogen-dxf-viewer-0.1.0.vsix" ]; then
    echo "✅ VSIX created: ergogen-dxf-viewer-0.1.0.vsix"
    echo ""
    echo "🚀 To install:"
    echo "  1. Open VSCode"
    echo "  2. Ctrl+Shift+P → 'Extensions: Install from VSIX'"
    echo "  3. Select: ergogen-dxf-viewer-0.1.0.vsix"
    echo "  4. Restart VSCode"
    echo ""
    echo "🎯 Commands available after install:"
    echo "  • 'Ergogen: Run Ergogen' (Ctrl+Shift+E in YAML files)"
    echo "  • 'Ergogen: Open DXF Viewer'"
else
    echo "❌ Failed to create VSIX"
fi