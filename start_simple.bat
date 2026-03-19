@echo off
cd /d "%~dp0"
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found
    pause
    exit /b 1
)
if not exist ".venv" (
    echo Creating venv...
    python -m venv .venv
)
call .venv\Scripts\activate.bat
pip show llm-folder-organizer >nul 2>&1
if errorlevel 1 (
    echo Installing...
    pip install -e . --quiet
)
echo Starting WebUI...
start http://localhost:8501
lfo web --host 127.0.0.1 --port 8501
pause
