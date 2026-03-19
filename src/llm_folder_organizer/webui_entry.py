from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    from .webui import run_webui
except Exception:
    src_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(src_root))
    from llm_folder_organizer.webui import run_webui


def _get_port() -> int:
    raw = os.getenv("LFO_PORT", "8501")
    try:
        return int(raw)
    except ValueError:
        return 8501


def main() -> None:
    host = os.getenv("LFO_HOST", "127.0.0.1")
    port = _get_port()
    raise SystemExit(run_webui(host=host, port=port))


if __name__ == "__main__":
    main()
