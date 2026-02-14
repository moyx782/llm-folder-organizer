#!/usr/bin/env bash
set -euo pipefail
# Example:
#   DEEPSEEK_API_KEY=... bash scripts/dev_run.sh ~/Downloads
python -m llm_folder_organizer.cli scan "$1"
