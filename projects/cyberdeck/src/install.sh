#!/usr/bin/env bash
#
# install.sh — Cyberdeck keyboard overlay for micro-journal-linux
#
# Installs the matrix keyboard driver + keyd remapping layer on a stock
# micro-journal-linux image (Raspberry Pi OS based). Purely additive:
# does not touch unkyulee's scripts or launcher. Safe to re-run after
# any image update.
#
# Run on the Pi (via SSH or a temporary USB keyboard):
#   sudo bash install.sh
#
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
    echo "run as root: sudo bash install.sh" >&2
    exit 1
fi

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPT_DIR=/opt/cyberdeck
ETC_DIR=/etc/cyberdeck

echo "==> Installing dependencies (python3-lgpio, python3-evdev)"
apt-get update -qq
apt-get install -y python3-lgpio python3-evdev

echo "==> Installing keyd"
if command -v keyd >/dev/null 2>&1; then
    echo "    keyd already installed: $(keyd --version 2>/dev/null || echo present)"
elif apt-get install -y keyd 2>/dev/null; then
    echo "    keyd installed from apt"
else
    echo "    keyd not in apt (Debian < trixie) — building from source"
    apt-get install -y git make gcc
    BUILD_DIR="$(mktemp -d)"
    git clone --depth 1 https://github.com/rvaiya/keyd "$BUILD_DIR/keyd"
    make -C "$BUILD_DIR/keyd"
    make -C "$BUILD_DIR/keyd" install
    rm -rf "$BUILD_DIR"
fi

echo "==> Installing cyberdeck files"
install -d "$OPT_DIR" "$ETC_DIR" /etc/keyd
install -m 0755 "$SRC_DIR/cyberdeck_kbd.py" "$OPT_DIR/cyberdeck_kbd.py"
install -m 0755 "$SRC_DIR/matrix_test.py"   "$OPT_DIR/matrix_test.py"

# Never clobber user-edited configs on re-install.
if [[ -f "$ETC_DIR/matrix_layout.json" ]]; then
    echo "    keeping existing $ETC_DIR/matrix_layout.json (new copy -> .new)"
    install -m 0644 "$SRC_DIR/matrix_layout.json" "$ETC_DIR/matrix_layout.json.new"
else
    install -m 0644 "$SRC_DIR/matrix_layout.json" "$ETC_DIR/matrix_layout.json"
fi

if [[ -f /etc/keyd/default.conf ]]; then
    echo "    keeping existing /etc/keyd/default.conf (new copy -> .new)"
    install -m 0644 "$SRC_DIR/keyd/default.conf" /etc/keyd/default.conf.new
else
    install -m 0644 "$SRC_DIR/keyd/default.conf" /etc/keyd/default.conf
fi

echo "==> Installing systemd services"
install -m 0644 "$SRC_DIR/cyberdeck-kbd.service" /etc/systemd/system/cyberdeck-kbd.service
systemctl daemon-reload
systemctl enable keyd
systemctl restart keyd
systemctl enable cyberdeck-kbd
systemctl restart cyberdeck-kbd

echo
echo "==> Done. Checks:"
systemctl --no-pager --lines 0 status cyberdeck-kbd || true
systemctl --no-pager --lines 0 status keyd || true
echo
echo "Next steps:"
echo "  * verify wiring first:      sudo systemctl stop cyberdeck-kbd && sudo python3 $OPT_DIR/matrix_test.py"
echo "  * remap keys:               sudo nano /etc/keyd/default.conf && sudo keyd reload"
echo "  * reload physical layout:   sudo systemctl reload cyberdeck-kbd"
echo "  * logs:                     journalctl -u cyberdeck-kbd -e"