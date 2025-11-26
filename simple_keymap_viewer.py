#!/usr/bin/env python3
"""
Simple keymap viewer that finds and watches a specific keymap.c file
"""

import os
import glob
import time
import json
import argparse
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SimpleKeymapHandler(FileSystemEventHandler):
    def __init__(self, target_file):
        self.target_file = Path(target_file).resolve()
        self.last_update = time.time()
        print(f"👀 Watching: {self.target_file}")
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        event_path = Path(event.src_path).resolve()
        
        if event_path == self.target_file:
            print(f"📝 File changed: {event.src_path}")
            self.last_update = time.time()
            
            # Write simple status
            with open('keymap_status.json', 'w') as f:
                json.dump({
                    'timestamp': self.last_update,
                    'file': str(self.target_file),
                    'content': self.read_keymap_content()
                }, f)
                
    def read_keymap_content(self):
        try:
            with open(self.target_file, 'r') as f:
                return f.read()
        except:
            return "Error reading file"

class SimpleHTTPHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
        
    def do_GET(self):
        if self.path == '/api/keymap':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            try:
                with open('keymap_status.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = {'timestamp': 0, 'file': None, 'content': ''}
                
            self.wfile.write(json.dumps(data).encode())
            return
            
        super().do_GET()

def find_keymap_files():
    """Find all keymap.c files in current directory"""
    keymaps = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == 'keymap.c':
                full_path = os.path.join(root, file)
                keymaps.append(full_path.replace('\\', '/'))
    return keymaps

def select_keymap():
    """Interactive keymap selection"""
    keymaps = find_keymap_files()
    
    if not keymaps:
        print("❌ No keymap.c files found!")
        return None
        
    print("🔍 Found keymap.c files:")
    print()
    
    for i, keymap in enumerate(keymaps, 1):
        print(f"  {i}. {keymap}")
    
    print()
    
    while True:
        try:
            choice = input(f"Enter number (1-{len(keymaps)}): ").strip()
            if choice == "":
                return None
            
            idx = int(choice) - 1
            if 0 <= idx < len(keymaps):
                return keymaps[idx]
            else:
                print(f"Please enter a number between 1 and {len(keymaps)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            return None

def start_watcher(target_file):
    """Start watching the target file"""
    handler = SimpleKeymapHandler(target_file)
    observer = Observer()
    
    watch_dir = os.path.dirname(os.path.abspath(target_file))
    observer.schedule(handler, watch_dir, recursive=False)
    observer.start()
    
    # Initial content load
    handler.on_modified(type('Event', (), {'src_path': target_file, 'is_directory': lambda: False})())
    
    return observer

def start_server(port=8000):
    """Start HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPHandler)
    
    print(f"🌐 Server starting on http://localhost:{port}")
    print(f"📁 Open http://localhost:{port}/simple_viewer.html")
    print("Press Ctrl+C to stop")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple QMK Keymap Viewer')
    parser.add_argument('--file', '-f', help='Specific keymap.c file to watch')
    parser.add_argument('--port', '-p', type=int, default=8000, help='Server port')
    
    args = parser.parse_args()
    
    if args.file:
        target_file = args.file
    else:
        target_file = select_keymap()
        
    if not target_file:
        print("No file selected. Exiting.")
        exit(1)
        
    if not os.path.exists(target_file):
        print(f"❌ File not found: {target_file}")
        exit(1)
    
    print(f"🎯 Selected: {target_file}")
    
    observer = start_watcher(target_file)
    
    try:
        start_server(args.port)
    finally:
        observer.stop()
        observer.join()