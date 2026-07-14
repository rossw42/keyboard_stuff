#!/usr/bin/env python3
"""
Live QMK Keymap Viewer
======================

A single, self-contained server for viewing QMK keymap.c files live in the
browser.

- Scans a directory (recursively) for keymap.c files
- Serves a web UI (viewer.html) with a dropdown to pick ONE keyboard
- The page shows only the selected board and auto-refreshes when the
  keymap.c file changes on disk (polling, no extra dependencies)

Usage:
    python keymap_viewer.py                     # scan current directory
    python keymap_viewer.py --dir path/to/qmk   # scan a specific directory
    python keymap_viewer.py --port 9000         # use a different port

Endpoints:
    GET /                       -> viewer.html
    GET /api/keymaps            -> JSON list of keymap.c files found
    GET /api/keymap?file=<rel>  -> JSON {file, timestamp, content}

No third-party packages required (pure standard library).
"""

import argparse
import json
import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

SCRIPT_DIR = Path(__file__).parent.resolve()

# Set at startup from --dir
SCAN_ROOT = Path.cwd()

# Directories that are never worth scanning
SKIP_DIRS = {'.git', '.build', 'node_modules', '__pycache__', '.vscode'}


def find_keymap_files(root: Path):
    """Recursively find all keymap.c files under root. Returns sorted
    forward-slash relative paths."""
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if 'keymap.c' in filenames:
            rel = Path(dirpath).relative_to(root) / 'keymap.c'
            results.append(rel.as_posix())
    return sorted(results)


def safe_resolve(rel_file: str):
    """Resolve a client-supplied relative path safely.

    Returns the absolute Path only if it stays inside SCAN_ROOT and is
    actually a keymap.c file; otherwise returns None.
    """
    try:
        target = (SCAN_ROOT / rel_file).resolve()
    except (ValueError, OSError):
        return None
    if target.name != 'keymap.c':
        return None
    try:
        target.relative_to(SCAN_ROOT)
    except ValueError:
        return None
    return target if target.is_file() else None


class ViewerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve static files (viewer.html) from the script's own directory,
        # regardless of where the server was launched from.
        super().__init__(*args, directory=str(SCRIPT_DIR), **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def send_json(self, obj, status=200):
        body = json.dumps(obj).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == '/api/keymaps':
            self.send_json({'root': str(SCAN_ROOT),
                            'keymaps': find_keymap_files(SCAN_ROOT)})
            return

        if parsed.path == '/api/keymap':
            params = parse_qs(parsed.query)
            rel_file = params.get('file', [None])[0]
            if not rel_file:
                self.send_json({'error': 'missing ?file= parameter'}, 400)
                return
            target = safe_resolve(rel_file)
            if target is None:
                self.send_json({'error': f'not found: {rel_file}'}, 404)
                return
            try:
                content = target.read_text(encoding='utf-8', errors='replace')
                self.send_json({
                    'file': rel_file,
                    'timestamp': target.stat().st_mtime,
                    'content': content,
                })
            except OSError as e:
                self.send_json({'error': str(e)}, 500)
            return

        if parsed.path == '/':
            self.path = '/viewer.html'

        super().do_GET()

    def log_message(self, fmt, *args):
        # Silence routine polling requests; keep errors visible.
        first = str(args[0]) if args else ''
        if '/api/keymap' not in first:
            super().log_message(fmt, *args)


def main():
    global SCAN_ROOT

    parser = argparse.ArgumentParser(description='Live QMK Keymap Viewer')
    parser.add_argument('--dir', '-d', default='.',
                        help='Directory to scan for keymap.c files '
                             '(default: current directory)')
    parser.add_argument('--port', '-p', type=int, default=8000,
                        help='Server port (default: 8000)')
    parser.add_argument('--no-browser', action='store_true',
                        help='Do not open the browser automatically')
    args = parser.parse_args()

    SCAN_ROOT = Path(args.dir).resolve()
    if not SCAN_ROOT.is_dir():
        print(f'ERROR: not a directory: {SCAN_ROOT}')
        sys.exit(1)

    keymaps = find_keymap_files(SCAN_ROOT)
    print(f'Scanning: {SCAN_ROOT}')
    print(f'Found {len(keymaps)} keymap.c file(s)')
    for k in keymaps:
        print(f'  - {k}')
    if not keymaps:
        print('  (none found -- check the --dir argument)')

    url = f'http://localhost:{args.port}/'
    print(f'\nServing on {url}')
    print('Press Ctrl+C to stop')

    httpd = HTTPServer(('', args.port), ViewerHandler)

    if not args.no_browser:
        webbrowser.open(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped')


if __name__ == '__main__':
    main()