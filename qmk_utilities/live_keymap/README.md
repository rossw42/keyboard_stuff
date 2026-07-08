# Live Keymap Viewer

View your QMK `keymap.c` files in the browser, live. Pick **one keyboard**
from a dropdown and the page shows only that board — with layer tabs, key
coloring, and combo listings. When you edit and save the `keymap.c` file,
the page updates automatically within ~2 seconds.

## Quick Start

Double-click **`start_viewer.bat`** — it scans the repo's `keyboards\`
folder, starts the server, and opens your browser at
`http://localhost:8000/`.

Then just pick your board from the **Keyboard** dropdown. Your choice is
remembered (in browser localStorage), so next time the page opens straight
to your board.

## Usage

```
python keymap_viewer.py [--dir DIR] [--port PORT] [--no-browser]
```

| Option | Default | Description |
|---|---|---|
| `--dir`, `-d` | `.` (current dir) | Directory to scan recursively for `keymap.c` files |
| `--port`, `-p` | `8000` | HTTP server port |
| `--no-browser` | off | Don't auto-open the browser |

Examples:

```powershell
# Scan this repo's keyboards folder (what the .bat file does)
python keymap_viewer.py --dir ..\..\keyboards

# Scan a full qmk_firmware checkout on another port
python keymap_viewer.py --dir D:\qmk_firmware\keyboards\lily58 --port 9000
```

You can also pass a directory to the launcher:

```
start_viewer.bat D:\some\other\keyboards
```

## Files

| File | Purpose |
|---|---|
| `keymap_viewer.py` | The whole server: scans for keymaps, serves the UI and the JSON API |
| `viewer.html` | The web UI (dropdown, layer tabs, visual keymap, raw view) |
| `start_viewer.bat` | Windows launcher, defaults to scanning `..\..\keyboards` |

## API

| Endpoint | Returns |
|---|---|
| `GET /api/keymaps` | `{ root, keymaps: ["lily58/keymaps/default/keymap.c", ...] }` |
| `GET /api/keymap?file=<rel>` | `{ file, timestamp, content }` for one keymap |

## Requirements

- Python 3 (standard library only — no pip installs needed)

## How live updates work

The page polls `GET /api/keymap?file=...` every 2 seconds and compares the
file's modification timestamp. When it changes, the keymap is re-parsed and
re-rendered. Use the **Pause** button to stop polling, and **Rescan** to
refresh the dropdown after adding new keymap files.

## Notes

- The parser handles `[NAME] = LAYOUT_xxx( ... )` blocks with numeric or
  named layers, keeps `LT(1, KC_SPC)`-style keys intact, and uses the
  source line breaks in `keymap.c` as visual rows.
- Keys are color-coded: modifiers (orange), layer keys (purple),
  F-keys (blue), media (teal), RGB (pink), transparent/no-op (dimmed).

## History

This folder previously contained three overlapping server scripts
(`keymap_server.py`, `simple_keymap_viewer.py`, `watch_keymap.py`), three
HTML pages (one with a hardcoded static gallery of six boards), an unused
`keymap_watcher.js`, three start scripts, and three README files. All of
that was consolidated into the single server + single page above
(2026-07-08).