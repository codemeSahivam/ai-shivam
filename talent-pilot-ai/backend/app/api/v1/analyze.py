"""Analyze resume API."""

from __future__ import annotations

from fastapi import APIRouter, File, Form, UploadFile

from app.api.deps import AnalyzeUseCaseDep, OptionalUserIdDep, SettingsDep
from app.schemas.analysis import AnalyzeSuccessResponse
from app.utils.uploads import read_upload_limited

router = APIRouter(prefix="/api/v1", tags=["analyze"])


@router.post(
    "/analyze",
    response_model=AnalyzeSuccessResponse,
    summary="Analyze resume against a job description",
    description="Upload a PDF or DOCX resume and a job description to receive structured hiring insights.",
    responses={
        400: {"description": "Validation error"},
        429: {"description": "Rate limited"},
        500: {"description": "Invalid AI response"},
        503: {"description": "AI unavailable"},
    },
)
async def analyze_resume(
    settings: SettingsDep,
    use_case: AnalyzeUseCaseDep,
    user_id: OptionalUserIdDep,
    resume: UploadFile = File(..., description="PDF or DOCX resume"),
    job_description: str = Form(..., description="Job description text"),
) -> AnalyzeSuccessResponse:
    file_bytes = await read_upload_limited(resume, settings)
    analysis, saved_id = await use_case.execute(
        file_bytes=file_bytes,
        filename=resume.filename,
        content_type=resume.content_type,
        job_description=job_description,
        user_id=user_id,
    )
    return AnalyzeSuccessResponse(success=True, analysis=analysis, saved_id=saved_id)
