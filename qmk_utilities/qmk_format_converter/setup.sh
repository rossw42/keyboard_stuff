#!/bin/bash
# QMK Format Converter Setup Script

set -e

echo "🔧 Setting up QMK Format Converter..."

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Make the main script executable
chmod +x "$SCRIPT_DIR/qmk-convert"

# Create symlink in user's local bin if it exists
if [ -d "$HOME/.local/bin" ]; then
    echo "📦 Creating symlink in ~/.local/bin..."
    ln -sf "$SCRIPT_DIR/qmk-convert" "$HOME/.local/bin/qmk-convert"
    echo "✅ You can now run 'qmk-convert' from anywhere!"
elif [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
    echo "📦 Creating symlink in /usr/local/bin..."
    ln -sf "$SCRIPT_DIR/qmk-convert" "/usr/local/bin/qmk-convert"
    echo "✅ You can now run 'qmk-convert' from anywhere!"
else
    echo "ℹ️  No writable bin directory found. You can run the converter with:"
    echo "   $SCRIPT_DIR/qmk-convert"
fi

echo ""
echo "🎉 Setup complete! Try these commands to get started:"
echo ""
echo "# List supported formats"
echo "qmk-convert --list-formats"
echo ""
echo "# Convert KLE to VIA"
echo "qmk-convert input.json --to via -o output.json"
echo ""
echo "# Convert with explicit input format"
echo "qmk-convert keymap.c --from keymap --to kle -o layout.json"
echo ""
echo "# Validate a file"
echo "qmk-convert layout.json --validate"
echo ""
