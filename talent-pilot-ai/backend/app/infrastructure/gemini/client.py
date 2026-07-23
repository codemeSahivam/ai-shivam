"""Gemini LLM adapter."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from google import genai
from google.genai import types
from pydantic import ValidationError

from app.core.config import Settings
from app.domain.exceptions import GeminiUnavailableError, InvalidAIResponseError
from app.schemas.analysis import AnalysisResult

logger = logging.getLogger(__name__)

ANALYSIS_RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "match_score": {"type": "integer"},
        "ats_score": {"type": "integer"},
        "match_score_breakdown": {"type": "array", "items": {"type": "string"}},
        "ats_score_breakdown": {"type": "array", "items": {"type": "string"}},
        "summary": {"type": "string"},
        "matching_skills": {"type": "array", "items": {"type": "string"}},
        "missing_skills": {"type": "array", "items": {"type": "string"}},
        "strengths": {"type": "array", "items": {"type": "string"}},
        "weaknesses": {"type": "array", "items": {"type": "string"}},
        "suggestions": {"type": "array", "items": {"type": "string"}},
        "recommendation": {
            "type": "string",
            "enum": ["Strong Hire", "Hire", "Consider", "Reject"],
        },
    },
    "required": [
        "match_score",
        "ats_score",
        "match_score_breakdown",
        "ats_score_breakdown",
        "summary",
        "matching_skills",
        "missing_skills",
        "strengths",
        "weaknesses",
        "suggestions",
        "recommendation",
    ],
}


class GeminiService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        if not settings.gemini_api_key:
            logger.warning("GEMINI_API_KEY is not set")
        self._client = genai.Client(api_key=settings.gemini_api_key)

    async def generate_analysis_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> AnalysisResult:
        last_error: Exception | None = None
        attempts = self._settings.gemini_max_retries + 1

        for attempt in range(attempts):
            try:
                raw = await asyncio.wait_for(
                    asyncio.to_thread(self._call_gemini, system_prompt, user_prompt),
                    timeout=self._settings.gemini_timeout_seconds,
                )
                return self._parse_analysis(raw)
            except InvalidAIResponseError:
                raise
            except TimeoutError as exc:
                last_error = exc
                logger.warning("Gemini timeout on attempt %s/%s", attempt + 1, attempts)
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                logger.warning(
                    "Gemini failure on attempt %s/%s: %s: %s",
                    attempt + 1,
                    attempts,
                    type(exc).__name__,
                    str(exc)[:300],
                )

            if attempt < attempts - 1:
                await asyncio.sleep(0.5 * (2**attempt))

        raise GeminiUnavailableError() from last_error

    def _call_gemini(self, system_prompt: str, user_prompt: str) -> str:
        response = self._client.models.generate_content(
            model=self._settings.gemini_model,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=ANALYSIS_RESPONSE_SCHEMA,
                temperature=0.2,
            ),
        )
        text = (response.text or "").strip()
        if not text:
            raise InvalidAIResponseError()
        return text

    def _parse_analysis(self, raw: str) -> AnalysisResult:
        try:
            payload = json.loads(raw)
            return AnalysisResult.model_validate(payload)
        except (json.JSONDecodeError, ValidationError) as exc:
            raise InvalidAIResponseError() from exc
