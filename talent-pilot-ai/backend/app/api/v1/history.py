"""Saved analysis history API."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import HistoryUseCaseDep, UserIdDep
from app.schemas.history import HistoryItem, HistoryListResponse

router = APIRouter(prefix="/api/v1", tags=["history"])


@router.get(
    "/history",
    response_model=HistoryListResponse,
    summary="List saved analyses for the current user",
)
async def list_history(user_id: UserIdDep, use_case: HistoryUseCaseDep) -> HistoryListResponse:
    items = use_case.list_items(user_id)
    return HistoryListResponse(success=True, items=items)


@router.get(
    "/history/{analysis_id}",
    response_model=HistoryItem,
    summary="Get a saved analysis by id",
)
async def get_history_item(
    analysis_id: int,
    user_id: UserIdDep,
    use_case: HistoryUseCaseDep,
) -> HistoryItem:
    return use_case.get_item(user_id, analysis_id)
