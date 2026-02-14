#!/usr/bin/env bash
set -euo pipefail

# Build a standalone WebUI executable with PyInstaller.
python -m PyInstaller packaging/pyinstaller_webui.spec --noconfirm --clean
