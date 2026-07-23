"""Analysis persistence."""

from __future__ import annotations

import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.db.orm import AnalysisModel
from app.schemas.analysis import AnalysisResult
from app.schemas.history import HistoryItem

PREVIEW_MAX_CHARS = 120


class AnalysisRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(
        self,
        user_id: int,
        filename: str,
        job_description: str,
        analysis: AnalysisResult,
    ) -> AnalysisModel:
        record = AnalysisModel(
            user_id=user_id,
            filename=filename,
            job_description=job_description,
            analysis_json=analysis.model_dump_json(),
            match_score=analysis.match_score,
            ats_score=analysis.ats_score,
            recommendation=analysis.recommendation.value,
        )
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    def list_for_user(self, user_id: int, limit: int = 50) -> list[HistoryItem]:
        statement = (
            select(AnalysisModel)
            .where(AnalysisModel.user_id == user_id)
            .order_by(AnalysisModel.created_at.desc())
            .limit(limit)
        )
        rows = self._session.scalars(statement).all()
        return [self._to_history_item(row) for row in rows]

    def get_for_user(self, user_id: int, analysis_id: int) -> HistoryItem | None:
        statement = select(AnalysisModel).where(
            AnalysisModel.id == analysis_id,
            AnalysisModel.user_id == user_id,
        )
        row = self._session.scalars(statement).first()
        if row is None:
            return None
        return self._to_history_item(row)

    def _to_history_item(self, row: AnalysisModel) -> HistoryItem:
        analysis = AnalysisResult.model_validate(json.loads(row.analysis_json))
        preview = row.job_description.strip().replace("\n", " ")
        if len(preview) > PREVIEW_MAX_CHARS:
            preview = preview[: PREVIEW_MAX_CHARS - 3] + "..."
        return HistoryItem(
            id=row.id,
            filename=row.filename,
            job_description_preview=preview,
            match_score=row.match_score,
            ats_score=row.ats_score,
            recommendation=row.recommendation,
            created_at=row.created_at.isoformat() if row.created_at else "",
            analysis=analysis,
        )
