#!/usr/bin/env bash
# Installs launcher.py to ~/bin and makes it executable.

set -e

INSTALL_DIR="$HOME/bin"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$INSTALL_DIR"
cp "$SCRIPT_DIR/launcher.py" "$INSTALL_DIR/claude-launch"
chmod +x "$INSTALL_DIR/claude-launch"

echo "Installed: $INSTALL_DIR/claude-launch"

if ! echo ":$PATH:" | grep -q ":$INSTALL_DIR:"; then
    echo "NOTE: $INSTALL_DIR not in PATH. Add to ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"\$HOME/bin:\$PATH\""
fi
