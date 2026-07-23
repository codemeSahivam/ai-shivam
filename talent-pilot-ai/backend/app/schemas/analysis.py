"""Analysis DTOs."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.domain.enums import Recommendation


class AnalysisResult(BaseModel):
    match_score: int = Field(ge=0, le=100)
    ats_score: int = Field(ge=0, le=100)
    match_score_breakdown: list[str] = Field(default_factory=list)
    ats_score_breakdown: list[str] = Field(default_factory=list)
    summary: str = Field(min_length=1)
    matching_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[str]
    recommendation: Recommendation


class AnalyzeSuccessResponse(BaseModel):
    success: bool = True
    analysis: AnalysisResult
    saved_id: int | None = None
