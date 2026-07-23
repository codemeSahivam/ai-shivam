"""LLM client protocol."""

from __future__ import annotations

from typing import Protocol

from app.schemas.analysis import AnalysisResult


class LLMClient(Protocol):
    async def generate_analysis_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> AnalysisResult: ...
