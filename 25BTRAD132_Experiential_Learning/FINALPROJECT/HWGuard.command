#!/usr/bin/env bash
# ==============================================================================
# HWGuard - 1-Click Launcher for macOS (Apple Silicon M1/M2/M3/M4 & Intel Mac)
# ==============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "========================================================"
echo "🛡️  HWGuard - Portable Tamper-Evident Hardware Guardian"
echo "========================================================"
echo "Checking macOS Python 3 environment..."

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$DIR/system/hwguard.py"
elif command -v python >/dev/null 2>&1; then
    exec python "$DIR/system/hwguard.py"
else
    echo ""
    echo "[!] Python 3 was not found on this Mac."
    echo "    To run HWGuard, open Terminal and install Python 3 or run:"
    echo "    xcode-select --install"
    echo ""
    read -p "Press Enter to exit..."
fi
