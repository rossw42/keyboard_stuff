#!/bin/bash

echo "🐛 Creating Debug VSIX Package"
echo "=============================="

# Create a temporary directory for the extension
TEMP_DIR="ergogen-debug-temp"
rm -rf $TEMP_DIR
mkdir -p $TEMP_DIR/extension

# Copy debug files
echo "📁 Copying debug extension files..."
cp package-debug.json $TEMP_DIR/extension/package.json
cp debug-extension.js $TEMP_DIR/extension/
echo "# Ergogen DXF Viewer Debug Extension" > $TEMP_DIR/extension/README.md

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

# Create VSIX archive
echo "🗜️  Creating debug VSIX archive..."
cd $TEMP_DIR
zip -r ../ergogen-dxf-viewer-debug-0.1.2.vsix . -x "*.DS_Store"
cd ..

# Clean up
rm -rf $TEMP_DIR

if [ -f "ergogen-dxf-viewer-debug-0.1.2.vsix" ]; then
    echo "✅ Debug VSIX created: ergogen-dxf-viewer-debug-0.1.2.vsix"
    echo ""
    echo "🚀 To install and test:"
    echo "  1. Uninstall previous version if installed"
    echo "  2. Ctrl+Shift+P → 'Extensions: Install from VSIX'"
    echo "  3. Select: ergogen-dxf-viewer-debug-0.1.2.vsix"
    echo "  4. Restart VSCode"
    echo "  5. Try: Ctrl+Shift+P → 'Ergogen: Test Extension'"
    echo ""
    echo "🎯 This debug version will:"
    echo "  • Show activation message when loaded"
    echo "  • Provide 'Test Extension' command to verify it's working"
    echo "  • Have more verbose logging"
else
    echo "❌ Failed to create debug VSIX"
fi