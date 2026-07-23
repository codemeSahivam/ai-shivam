"""History DTOs."""

from __future__ import annotations

from pydantic import BaseModel

from app.schemas.analysis import AnalysisResult


class HistoryItem(BaseModel):
    id: int
    filename: str
    job_description_preview: str
    match_score: int
    ats_score: int
    recommendation: str
    created_at: str
    analysis: AnalysisResult


class HistoryListResponse(BaseModel):
    success: bool = True
    items: list[HistoryItem]
