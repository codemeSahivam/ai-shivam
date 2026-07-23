import io
from pathlib import Path

import fitz
import pytest
from fastapi.testclient import TestClient

from app.api.deps import provide_gemini
from app.core.config import Settings, get_settings
from app.db import reset_db_state
from app.domain.enums import Recommendation
from app.infrastructure.gemini.client import GeminiService
from app.main import create_app
from app.schemas.analysis import AnalysisResult


def make_pdf_bytes(text: str = "Jane Doe\nBackend Engineer\nPython FastAPI Docker") -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    buffer = io.BytesIO()
    doc.save(buffer)
    doc.close()
    return buffer.getvalue()


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    db_path = tmp_path / "test.db"
    return Settings(
        environment="development",
        gemini_api_key="test-key",
        gemini_model="gemini-flash-latest",
        max_upload_bytes=10 * 1024 * 1024,
        max_job_description_chars=10_000,
        gemini_timeout_seconds=5,
        gemini_max_retries=0,
        cors_origins="http://testserver",
        secret_key="test-secret-key-with-enough-length",
        database_url=f"sqlite:///{db_path}",
        https_only=False,
        trusted_hosts="testserver,localhost,127.0.0.1",
        rate_limit_analyze_per_minute=1000,
        rate_limit_auth_per_minute=1000,
    )


@pytest.fixture
def sample_analysis() -> AnalysisResult:
    return AnalysisResult(
        match_score=82,
        ats_score=76,
        match_score_breakdown=["Strong Python overlap", "API experience aligns"],
        ats_score_breakdown=["Clear skill keywords", "Some metrics present"],
        summary="Strong backend engineer with Python and Docker experience.",
        matching_skills=["Python", "FastAPI", "Docker"],
        missing_skills=["Terraform", "Redis"],
        strengths=["Strong backend experience", "Cloud-friendly skills"],
        weaknesses=["No certifications", "Missing testing depth"],
        suggestions=["Add measurable metrics", "Include cloud projects"],
        recommendation=Recommendation.HIRE,
    )


class FakeGeminiService(GeminiService):
    def __init__(self, settings: Settings, result: AnalysisResult) -> None:
        self._settings = settings
        self._result = result

    async def generate_analysis_json(self, system_prompt: str, user_prompt: str) -> AnalysisResult:
        assert system_prompt
        assert "JOB DESCRIPTION" in user_prompt
        assert "RESUME" in user_prompt
        return self._result


@pytest.fixture
def client(settings: Settings, sample_analysis: AnalysisResult, monkeypatch: pytest.MonkeyPatch):
    get_settings.cache_clear()
    reset_db_state()

    def _settings() -> Settings:
        return settings

    monkeypatch.setattr("app.core.config.get_settings", _settings)
    monkeypatch.setattr("app.main.get_settings", _settings)

    app = create_app()
    app.dependency_overrides[provide_gemini] = lambda: FakeGeminiService(
        settings,
        sample_analysis,
    )

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    reset_db_state()
    get_settings.cache_clear()
