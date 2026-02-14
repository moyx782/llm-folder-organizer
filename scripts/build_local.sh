#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
pip install .
pip install pyinstaller
pyinstaller build/pyinstaller.spec

echo "Built: dist/lfo-webui/"
