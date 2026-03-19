from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class AppConfig:
    base_url: str
    model: str
    preview_chars: int = 3000
    max_bytes: int = 50000
    default_category: str = "Unsorted"
    category_map: Dict[str, list[str]] | None = None

    @staticmethod
    def load(path: str | Path) -> "AppConfig":
        p = Path(path)
        data: Dict[str, Any] = json.loads(p.read_text(encoding="utf-8"))
        return AppConfig(
            base_url=data.get("base_url", "https://api.deepseek.com"),
            model=data.get("model", "deepseek-chat"),
            preview_chars=int(data.get("preview_chars", 3000)),
            max_bytes=int(data.get("max_bytes", 50000)),
            default_category=data.get("default_category", "Unsorted"),
            category_map=data.get("category_map"),
        )
