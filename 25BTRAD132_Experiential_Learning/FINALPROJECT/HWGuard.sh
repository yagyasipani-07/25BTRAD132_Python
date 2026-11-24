#!/usr/bin/env bash
# ==============================================================================
# HWGuard - 1-Click Launcher for Linux (Ubuntu, Debian, Fedora, Arch, Mint)
# ==============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "========================================================"
echo "🛡️  HWGuard - Portable Tamper-Evident Hardware Guardian"
echo "========================================================"

SCRIPT="$DIR/FINALPROJECT.py"
if [ ! -f "$SCRIPT" ]; then
    SCRIPT="$DIR/system/hwguard.py"
fi

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$SCRIPT"
elif command -v python >/dev/null 2>&1; then
    exec python "$SCRIPT"
else
    echo ""
    echo "[!] Python 3 was not found on this Linux system."
    echo "    Please install python3 using your distribution package manager:"
    echo "    sudo apt install python3   (Ubuntu/Debian)"
    echo "    sudo dnf install python3   (Fedora/RHEL)"
    echo ""
    read -p "Press Enter to exit..."
fi
