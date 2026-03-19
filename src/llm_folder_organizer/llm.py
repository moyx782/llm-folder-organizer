from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass
class LLMResult:
    category: str
    confidence: float
    reason: str


class DeepSeekLLM:
    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def classify(self, system_prompt: str, user_prompt: str) -> LLMResult:
        # Ask model to output JSON reliably by using response_format if available.
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )
        raw = resp.choices[0].message.content or "{}"
        data: Dict[str, Any] = json.loads(raw)
        return LLMResult(
            category=str(data.get("category", "Unsorted")),
            confidence=float(data.get("confidence", 0.0)),
            reason=str(data.get("reason", "")),
        )
