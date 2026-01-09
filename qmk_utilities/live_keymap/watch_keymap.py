#!/usr/bin/env python3
"""
Ultra-simple keymap watcher
"""

import os
import sys
import time
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# Global variables
KEYMAP_FILE = None
LAST_MODIFIED = 0

class SimpleHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/keymap':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            global KEYMAP_FILE, LAST_MODIFIED
            
            try:
                # Check if file was modified
                if KEYMAP_FILE and os.path.exists(KEYMAP_FILE):
                    current_modified = os.path.getmtime(KEYMAP_FILE)
                    
                    if current_modified > LAST_MODIFIED:
                        LAST_MODIFIED = current_modified
                        print(f"📝 File updated: {KEYMAP_FILE}")
                    
                    # Read content
                    with open(KEYMAP_FILE, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    data = {
                        'file': KEYMAP_FILE,
                        'timestamp': current_modified,
                        'content': content
                    }
                else:
                    data = {
                        'file': KEYMAP_FILE,
                        'timestamp': 0,
                        'content': 'File not found'
                    }
                    
            except Exception as e:
                data = {
                    'file': KEYMAP_FILE,
                    'timestamp': 0,
                    'content': f'Error: {str(e)}'
                }
            
            self.wfile.write(json.dumps(data).encode())
            return
            
        # Serve files normally
        super().do_GET()

def find_keymaps():
    """Find keymap.c files"""
    keymaps = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == 'keymap.c':
                path = os.path.join(root, file).replace('\\', '/')
                keymaps.append(path)
    return keymaps

def main():
    global KEYMAP_FILE
    
    print("🎹 Ultra-Simple Keymap Watcher")
    print()
    
    # Find keymaps
    keymaps = find_keymaps()
    
    if not keymaps:
        print("❌ No keymap.c files found!")
        return
    
    print("📁 Found keymap.c files:")
    for i, keymap in enumerate(keymaps, 1):
        print(f"  {i}. {keymap}")
    
    print()
    
    # Get user choice
    while True:
        try:
            choice = input(f"Enter number (1-{len(keymaps)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(keymaps):
                KEYMAP_FILE = keymaps[idx]
                break
            else:
                print(f"Please enter 1-{len(keymaps)}")
        except (ValueError, KeyboardInterrupt):
            print("\nExiting...")
            return
    
    print(f"🎯 Watching: {KEYMAP_FILE}")
    
    # Start server
    port = 8000
    server = HTTPServer(('', port), SimpleHandler)
    
    print(f"🌐 Server: http://localhost:{port}/simple_viewer.html")
    print("Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopped")
        server.shutdown()

if __name__ == '__main__':
    main()