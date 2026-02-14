python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel
pip install .
pip install pyinstaller
pyinstaller build\pyinstaller.spec
Write-Host "Built: dist\lfo-webui\"
