#!/bin/bash

echo "🔍 Creating Minimal Debug VSIX"
echo "=============================="

# Create a temporary directory for the extension
TEMP_DIR="ergogen-minimal-temp"
rm -rf $TEMP_DIR
mkdir -p $TEMP_DIR/extension

# Copy minimal files
echo "📁 Copying minimal extension files..."
cp package-minimal.json $TEMP_DIR/extension/package.json
cp minimal-debug.js $TEMP_DIR/extension/
echo "# Minimal Debug Extension" > $TEMP_DIR/extension/README.md

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
echo "🗜️  Creating minimal VSIX archive..."
cd $TEMP_DIR
zip -r ../ergogen-dxf-viewer-minimal-0.1.3.vsix . -x "*.DS_Store"
cd ..

# Clean up
rm -rf $TEMP_DIR

if [ -f "ergogen-dxf-viewer-minimal-0.1.3.vsix" ]; then
    echo "✅ Minimal VSIX created: ergogen-dxf-viewer-minimal-0.1.3.vsix"
    echo ""
    echo "🚀 To install and test:"
    echo "  1. Uninstall previous version if installed"
    echo "  2. Ctrl+Shift+P → 'Extensions: Install from VSIX'"
    echo "  3. Select: ergogen-dxf-viewer-minimal-0.1.3.vsix"
    echo "  4. Restart VSCode"
    echo "  5. Look for activation messages"
    echo ""
    echo "🎯 This minimal version will:"
    echo "  • Show multiple activation messages"
    echo "  • Register commands with simple message responses"
    echo "  • Help identify if the issue is with activation or command logic"
else
    echo "❌ Failed to create minimal VSIX"
fi