"""History use cases."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.exceptions import NotFoundError
from app.infrastructure.db.repositories.analysis_repository import AnalysisRepository
from app.schemas.history import HistoryItem


class HistoryUseCase:
    def __init__(self, session: Session) -> None:
        self._analyses = AnalysisRepository(session)

    def list_items(self, user_id: int) -> list[HistoryItem]:
        return self._analyses.list_for_user(user_id)

    def get_item(self, user_id: int, analysis_id: int) -> HistoryItem:
        item = self._analyses.get_for_user(user_id, analysis_id)
        if item is None:
            raise NotFoundError("Analysis not found.")
        return item
