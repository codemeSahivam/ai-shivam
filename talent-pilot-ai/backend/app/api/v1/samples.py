"""Sample content API."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.domain.exceptions import NotFoundError
from app.samples import SAMPLE_JOB_DESCRIPTION
from app.schemas.samples import SampleJobDescriptionResponse

router = APIRouter(prefix="/api/v1/samples", tags=["samples"])

_REPO_ROOT = Path(__file__).resolve().parents[4]
_DEMO_CANDIDATES = [
    _REPO_ROOT / "frontend" / "assets" / "demo-resume.pdf",
    Path(__file__).resolve().parents[2] / "static" / "assets" / "demo-resume.pdf",
]


def _demo_resume_path() -> Path | None:
    for path in _DEMO_CANDIDATES:
        if path.exists():
            return path
    return None


@router.get(
    "/job-description",
    response_model=SampleJobDescriptionResponse,
    summary="Sample job description",
)
async def sample_job_description() -> SampleJobDescriptionResponse:
    return SampleJobDescriptionResponse(success=True, job_description=SAMPLE_JOB_DESCRIPTION)


@router.get(
    "/resume",
    summary="Sample resume PDF",
    response_class=FileResponse,
)
async def sample_resume() -> FileResponse:
    demo = _demo_resume_path()
    if demo is None:
        raise NotFoundError("Demo resume is not available.")
    return FileResponse(demo, media_type="application/pdf", filename="demo-resume.pdf")
