#!/usr/bin/env python3
"""
Simple HTTP server with file watching for QMK keymap visualization
Run this to serve the HTML file and watch for a specific keymap.c file
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class KeymapFileHandler(FileSystemEventHandler):
    def __init__(self, target_file=None):
        self.target_file = Path(target_file).resolve() if target_file else None
        self.last_update = time.time()
        print(f"👀 Watching: {self.target_file}")
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        event_path = Path(event.src_path).resolve()
        
        # Check if it's our target file or any keymap.c if no target specified
        if self.target_file:
            if event_path == self.target_file:
                print(f"📝 Detected change in target file: {event.src_path}")
                self.last_update = time.time()
                self._write_update_status(event.src_path)
        else:
            # Fallback: watch any keymap.c file
            if event.src_path.endswith('keymap.c'):
                print(f"📝 Detected change in {event.src_path}")
                self.last_update = time.time()
                self._write_update_status(event.src_path)
                
    def _write_update_status(self, file_path):
        # Write update timestamp for the web interface
        with open('last_update.json', 'w') as f:
            json.dump({
                'timestamp': self.last_update,
                'file': file_path,
                'target': str(self.target_file) if self.target_file else None
            }, f)

class KeymapHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
        
    def do_GET(self):
        # Handle special endpoints
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            try:
                with open('last_update.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = {'timestamp': 0, 'file': None}
                
            self.wfile.write(json.dumps(data).encode())
            return
            
        # Serve files normally
        super().do_GET()

def start_file_watcher(target_file=None):
    """Start watching a specific keymap file for changes"""
    event_handler = KeymapFileHandler(target_file)
    observer = Observer()
    
    if target_file and os.path.exists(target_file):
        # Watch the specific file's directory
        watch_dir = os.path.dirname(os.path.abspath(target_file))
        observer.schedule(event_handler, watch_dir, recursive=False)
        print(f"👀 Watching directory: {watch_dir}")
    else:
        # Fallback: watch current directory
        observer.schedule(event_handler, '.', recursive=True)
        print("👀 Watching current directory (no specific file provided)")
    
    observer.start()
    return observer

def start_server(port=8000):
    """Start HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, KeymapHTTPRequestHandler)
    
    print(f"🌐 Server starting on http://localhost:{port}")
    print(f"📁 Open http://localhost:{port}/keymap_visualization.html")
    print("Press Ctrl+C to stop")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='QMK Keymap Live Viewer')
    parser.add_argument('--file', '-f', help='Specific keymap.c file to watch')
    parser.add_argument('--port', '-p', type=int, default=8000, help='Server port (default: 8000)')
    
    args = parser.parse_args()
    
    # Start file watcher in background
    observer = start_file_watcher(args.file)
    
    try:
        # Start web server
        start_server(args.port)
    finally:
        observer.stop()
        observer.join()