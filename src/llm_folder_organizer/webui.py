from __future__ import annotations

import sys
from pathlib import Path


def run_webui(host: str = "127.0.0.1", port: int = 8501) -> int:
    """Launch Streamlit WebUI.

    This runs:
      python -m streamlit run <module_file> --server.address host --server.port port
    """
    module_file = Path(__file__).with_name("webui_app.py")
  argv = [
    "streamlit",
    "run",
    str(module_file),
    "--server.address",
    host,
    "--server.port",
    str(port),
  ]

  try:
    from streamlit.web import cli as stcli
  except Exception as exc:
    raise SystemExit(f"Streamlit not available: {exc}")

  prev_argv = sys.argv[:]
  try:
    sys.argv = argv
    stcli.main()
  except SystemExit as exc:
    code = exc.code if isinstance(exc.code, int) else 0
    return code
  finally:
    sys.argv = prev_argv

  return 0
