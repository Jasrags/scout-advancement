#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== Scout Advancement Labels — Build ==="
echo "Root: $ROOT"

# Activate venv
if [ -d "$ROOT/.venv" ]; then
    source "$ROOT/.venv/bin/activate"
else
    echo "Error: .venv not found. Run: python3 -m venv .venv && pip install -e '.[dev]'"
    exit 1
fi

# Ensure dependencies
pip install --quiet pyinstaller reportlab PySide6

# Clean previous builds
rm -rf "$ROOT/build" "$ROOT/dist"

# Build
echo ""
echo "Building with PyInstaller..."
pyinstaller "$ROOT/packaging/scout_labels.spec" \
    --distpath "$ROOT/dist" \
    --workpath "$ROOT/build" \
    --clean \
    --noconfirm

echo ""
echo "=== Build complete ==="
echo "App: $ROOT/dist/Scout Advancement Labels.app"
echo ""
echo "To test: open '$ROOT/dist/Scout Advancement Labels.app'"
