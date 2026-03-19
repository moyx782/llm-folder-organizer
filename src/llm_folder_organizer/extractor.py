from __future__ import annotations

from pathlib import Path


def read_preview(path: Path, max_bytes: int, preview_chars: int) -> str:
    """Read a safe preview from a file.

    Strategy: read up to max_bytes then decode as utf-8 with errors ignored.
    For binary files, preview may be empty or gibberish; filename/ext still helps.
    """
    try:
        with path.open("rb") as f:
            blob = f.read(max_bytes)
        text = blob.decode("utf-8", errors="ignore")
        return text[:preview_chars].strip()
    except Exception:
        return ""
