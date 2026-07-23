"""Shared API response schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ErrorBody(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorBody


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])
