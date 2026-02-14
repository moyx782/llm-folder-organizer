from __future__ import annotations

import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional

from .extractor import read_preview
from .llm import DeepSeekLLM, LLMResult


@dataclass
class FileItem:
    path: Path
    name: str
    ext: str
    size: int
    mtime: str


def iter_files(root: Path) -> Iterable[FileItem]:
    for p in root.iterdir():
        if p.is_file():
            st = p.stat()
            yield FileItem(
                path=p,
                name=p.name,
                ext=p.suffix.lower().lstrip("."),
                size=st.st_size,
                mtime=datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
            )


def safe_folder_name(s: str) -> str:
    # Keep it simple and filesystem-friendly
    banned = '<>:"/\\|?*'
    for ch in banned:
        s = s.replace(ch, "_")
    s = s.strip().strip(".")
    return s or "Unsorted"


def render_prompt(template: str, **kwargs) -> str:
    return template.format(**kwargs)


def organize(
    root: Path,
    llm: DeepSeekLLM,
    system_prompt: str,
    user_prompt_tmpl: str,
    max_bytes: int,
    preview_chars: int,
    apply: bool = False,
    dry_run: bool = True,
) -> List[tuple[Path, Path, LLMResult]]:
    results: List[tuple[Path, Path, LLMResult]] = []

    for item in iter_files(root):
        preview = read_preview(item.path, max_bytes=max_bytes, preview_chars=preview_chars)
        user_prompt = render_prompt(
            user_prompt_tmpl,
            name=item.name,
            ext=item.ext or "(none)",
            size=item.size,
            mtime=item.mtime,
            preview=preview or "(empty)",
        )
        r = llm.classify(system_prompt=system_prompt, user_prompt=user_prompt)
        category = safe_folder_name(r.category)
        dest_dir = root / category
        dest_path = dest_dir / item.name
        results.append((item.path, dest_path, r))

        if apply and not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
            # avoid overwrite
            if dest_path.exists():
                stem = dest_path.stem
                suf = dest_path.suffix
                i = 1
                while True:
                    cand = dest_dir / f"{stem} ({i}){suf}"
                    if not cand.exists():
                        dest_path = cand
                        break
                    i += 1
            shutil.move(str(item.path), str(dest_path))

    return results
