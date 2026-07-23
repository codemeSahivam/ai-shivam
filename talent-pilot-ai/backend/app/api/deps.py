"""FastAPI dependency providers."""

from __future__ import annotations

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.application.analyze_resume import AnalyzeResumeUseCase
from app.application.auth import AuthUseCase
from app.application.history import HistoryUseCase
from app.core.config import Settings, get_settings
from app.domain.exceptions import UnauthorizedError
from app.infrastructure.db.repositories.analysis_repository import AnalysisRepository
from app.infrastructure.db.session import get_db_session
from app.infrastructure.gemini.client import GeminiService
from app.infrastructure.parsing.resume_parser import ResumeParser


def provide_settings() -> Settings:
    return get_settings()


def provide_db() -> Generator[Session, None, None]:
    yield from get_db_session()


def provide_gemini(settings: Annotated[Settings, Depends(provide_settings)]) -> GeminiService:
    return GeminiService(settings)


def provide_resume_parser() -> ResumeParser:
    return ResumeParser()


def provide_analyze_use_case(
    settings: Annotated[Settings, Depends(provide_settings)],
    gemini: Annotated[GeminiService, Depends(provide_gemini)],
    parser: Annotated[ResumeParser, Depends(provide_resume_parser)],
    session: Annotated[Session, Depends(provide_db)],
) -> AnalyzeResumeUseCase:
    return AnalyzeResumeUseCase(
        settings=settings,
        llm_client=gemini,
        resume_parser=parser,
        analysis_repository=AnalysisRepository(session),
    )


def provide_auth_use_case(
    session: Annotated[Session, Depends(provide_db)],
) -> AuthUseCase:
    return AuthUseCase(session)


def provide_history_use_case(
    session: Annotated[Session, Depends(provide_db)],
) -> HistoryUseCase:
    return HistoryUseCase(session)


def get_optional_user_id(request: Request) -> int | None:
    user_id = request.session.get("user_id")
    return int(user_id) if user_id is not None else None


def require_user_id(request: Request) -> int:
    user_id = get_optional_user_id(request)
    if user_id is None:
        raise UnauthorizedError()
    return user_id


SettingsDep = Annotated[Settings, Depends(provide_settings)]
AnalyzeUseCaseDep = Annotated[AnalyzeResumeUseCase, Depends(provide_analyze_use_case)]
AuthUseCaseDep = Annotated[AuthUseCase, Depends(provide_auth_use_case)]
HistoryUseCaseDep = Annotated[HistoryUseCase, Depends(provide_history_use_case)]
OptionalUserIdDep = Annotated[int | None, Depends(get_optional_user_id)]
UserIdDep = Annotated[int, Depends(require_user_id)]
