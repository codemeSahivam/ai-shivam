"""Analyze resume use case."""

from __future__ import annotations

import asyncio
import logging
import time

from app.core.config import Settings
from app.domain.exceptions import JobDescriptionTooLongError, MissingJobDescriptionError
from app.infrastructure.db.repositories.analysis_repository import AnalysisRepository
from app.infrastructure.gemini.protocol import LLMClient
from app.infrastructure.parsing.resume_parser import ResumeParser
from app.prompts import build_messages
from app.schemas.analysis import AnalysisResult
from app.utils.file_validation import validate_file_magic, validate_resume_upload
from app.utils.text import sanitize_filename, sanitize_for_llm

logger = logging.getLogger(__name__)


class AnalyzeResumeUseCase:
    def __init__(
        self,
        settings: Settings,
        llm_client: LLMClient,
        resume_parser: ResumeParser,
        analysis_repository: AnalysisRepository | None = None,
    ) -> None:
        self._settings = settings
        self._llm_client = llm_client
        self._resume_parser = resume_parser
        self._analysis_repository = analysis_repository

    async def execute(
        self,
        file_bytes: bytes,
        filename: str | None,
        content_type: str | None,
        job_description: str,
        user_id: int | None = None,
    ) -> tuple[AnalysisResult, int | None]:
        started = time.perf_counter()
        safe_name = sanitize_filename(filename)

        validate_resume_upload(
            filename=safe_name,
            content_type=content_type,
            size_bytes=len(file_bytes),
            settings=self._settings,
        )
        validate_file_magic(file_bytes, safe_name)

        jd = sanitize_for_llm(job_description or "")
        if not jd:
            raise MissingJobDescriptionError()
        if len(jd) > self._settings.max_job_description_chars:
            raise JobDescriptionTooLongError()

        resume_text = sanitize_for_llm(
            await asyncio.to_thread(self._resume_parser.extract_text, file_bytes, safe_name)
        )
        system_prompt, user_prompt = build_messages(resume_text, jd)
        analysis = await self._llm_client.generate_analysis_json(system_prompt, user_prompt)

        saved_id: int | None = None
        if user_id is not None and self._analysis_repository is not None:
            record = self._analysis_repository.create(
                user_id=user_id,
                filename=safe_name,
                job_description=jd,
                analysis=analysis,
            )
            saved_id = record.id

        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.info("analyze_resume completed in %.1fms saved_id=%s", elapsed_ms, saved_id)
        return analysis, saved_id
