#!/bin/bash
# LLM Folder Organizer - Cross-platform starter
# Usage: ./start.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  LLM Folder Organizer${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}Error: Python not found${NC}"
        echo "Please install Python 3.9+ from https://www.python.org/downloads/"
        exit 1
    fi
    PYTHON=python
else
    PYTHON=python3
fi

echo -e "${YELLOW}Using Python: $PYTHON${NC}"

# Create virtual environment
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    $PYTHON -m venv "$VENV_DIR"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
elif [ -f "$VENV_DIR/Scripts/activate" ]; then
    source "$VENV_DIR/Scripts/activate"
else
    echo -e "${RED}Error: Cannot find virtual environment activation script${NC}"
    exit 1
fi

# Check if package is installed
if ! $PYTHON -c "import llm_folder_organizer" 2>/dev/null; then
    echo -e "${YELLOW}Installing LLM Folder Organizer...${NC}"
    pip install -e . -q
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Starting WebUI...${NC}"
echo -e "${GREEN}Open: http://localhost:8501${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Tip: Enter your API Key in the left sidebar"
echo ""

# Open browser (platform specific)
if command -v xdg-open &> /dev/null; then
    xdg-open "http://localhost:8501" &
elif command -v open &> /dev/null; then
    open "http://localhost:8501" &
fi

# Start WebUI
lfo web --host 127.0.0.1 --port 8501
