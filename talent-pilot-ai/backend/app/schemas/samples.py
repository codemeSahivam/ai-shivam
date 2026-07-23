"""Sample content DTOs."""

from __future__ import annotations

from pydantic import BaseModel


class SampleJobDescriptionResponse(BaseModel):
    success: bool = True
    job_description: str
