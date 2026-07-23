"""Domain package."""

from app.domain.enums import Environment, Recommendation
from app.domain.exceptions import AppError

__all__ = ["AppError", "Environment", "Recommendation"]
