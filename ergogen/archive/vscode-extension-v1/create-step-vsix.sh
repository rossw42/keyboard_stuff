#!/bin/bash

echo "🔍 Creating Step-by-Step Debug VSIX"
echo "==================================="

# Create a temporary directory for the extension
TEMP_DIR="ergogen-step-temp"
rm -rf $TEMP_DIR
mkdir -p $TEMP_DIR/extension

# Copy step files
echo "📁 Copying step extension files..."
cp package-step.json $TEMP_DIR/extension/package.json
cp step-by-step-debug.js $TEMP_DIR/extension/
echo "# Step-by-Step Debug Extension" > $TEMP_DIR/extension/README.md

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
echo "🗜️  Creating step VSIX archive..."
cd $TEMP_DIR
zip -r ../ergogen-dxf-viewer-step-0.2.0.vsix . -x "*.DS_Store"
cd ..

# Clean up
rm -rf $TEMP_DIR

if [ -f "ergogen-dxf-viewer-step-0.2.0.vsix" ]; then
    echo "✅ Step VSIX created: ergogen-dxf-viewer-step-0.2.0.vsix"
    echo ""
    echo "🚀 To install and test:"
    echo "  1. Uninstall previous version"
    echo "  2. Install: ergogen-dxf-viewer-step-0.2.0.vsix"
    echo "  3. Restart VSCode"
    echo "  4. Test: Ergogen: Open DXF Viewer"
    echo "  5. Test: Ergogen: Run Ergogen"
    echo ""
    echo "🎯 This version tests:"
    echo "  • Basic webview panel creation"
    echo "  • Simple ergogen execution"
    echo "  • No backend startup complexity"
else
    echo "❌ Failed to create step VSIX"
fi