from __future__ import annotations

import os
import sys
from pathlib import Path

# When bundled by PyInstaller, resources live under sys._MEIPASS
def _resource_path(rel: str) -> Path:
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return Path(base) / rel
    # dev mode
    return Path(__file__).resolve().parents[2] / rel

def main() -> int:
    # Ensure Streamlit can find config/prompts in standalone mode:
    # We'll set CWD to the folder that contains the bundled assets.
    bundle_root = getattr(sys, "_MEIPASS", None)
    if bundle_root:
        os.chdir(bundle_root)

    # Import after chdir so relative paths work
    from llm_folder_organizer.webui import run_webui

    host = os.getenv("LFO_HOST", "127.0.0.1")
    port = int(os.getenv("LFO_PORT", "8501"))
    return run_webui(host=host, port=port)

if __name__ == "__main__":
    raise SystemExit(main())
