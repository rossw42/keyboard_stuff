#!/bin/bash

# Package VSCode Extension with DXF Viewer Backend and Frontend

echo "📦 Packaging Ergogen DXF Viewer Extension"
echo "========================================"

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the vscode-extension directory"
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf out/
rm -rf backend/
rm -rf frontend-dist/

# Compile TypeScript
echo "🔨 Compiling TypeScript..."
npm run compile

# Copy backend files
echo "📁 Copying backend files..."
mkdir -p backend
cp -r ../backend/* backend/
# Remove unnecessary files
rm -rf backend/__pycache__/
rm -rf backend/venv/
rm -f backend/*.log
rm -f backend/test_*.py
rm -f backend/create_test_dxf.py

# Build frontend
echo "⚛️  Building React frontend..."
cd ../frontend
npm run build
cd ../vscode-extension
mkdir -p frontend-dist
cp -r ../frontend/dist/* frontend-dist/

# Update backend to serve built frontend
echo "🔧 Configuring backend for production..."
cat > backend/static_server.py << 'EOF'
"""
Static file server for VSCode extension
Serves the built React frontend
"""
from flask import Flask, send_from_directory
import os

def setup_static_routes(app):
    """Setup routes to serve the built React frontend"""
    
    @app.route('/')
    def serve_frontend():
        return send_from_directory('../frontend-dist', 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        # Serve static files from frontend-dist
        if os.path.exists(f'../frontend-dist/{path}'):
            return send_from_directory('../frontend-dist', path)
        # Fallback to index.html for SPA routing
        return send_from_directory('../frontend-dist', 'index.html')
EOF

# Update app.py to include static routes
echo "🔧 Updating app.py for extension use..."
cat >> backend/app.py << 'EOF'

# Import static server for VSCode extension
try:
    from static_server import setup_static_routes
    setup_static_routes(app)
except ImportError:
    pass  # Skip if not in extension environment
EOF

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Create .vscodeignore
echo "📝 Creating .vscodeignore..."
cat > .vscodeignore << 'EOF'
.vscode/**
.vscode-test/**
src/**
.gitignore
.yarnrc
vsc-extension-quickstart.md
**/tsconfig.json
**/.eslintrc.json
**/node_modules/**
scripts/**
backend/venv/**
backend/__pycache__/**
backend/*.log
backend/test_*.py
EOF

echo ""
echo "✅ Extension packaged successfully!"
echo ""
echo "🚀 To install and test:"
echo "  1. Open VSCode"
echo "  2. Press F5 to launch Extension Development Host"
echo "  3. Open an Ergogen project"
echo "  4. Run command: 'Ergogen: Open DXF Viewer'"
echo ""
echo "📦 To create VSIX package:"
echo "  npm install -g vsce"
echo "  vsce package"