"""Backward-compatible exception exports."""

from app.domain.exceptions import (
    AppError,
    AuthError,
    ConfigurationError,
    EmptyFileError,
    EmptyResumeError,
    FileTooLargeError,
    GeminiUnavailableError,
    InvalidAIResponseError,
    InvalidFileError,
    JobDescriptionTooLongError,
    MissingJobDescriptionError,
    NotFoundError,
    RateLimitError,
    UnauthorizedError,
)

__all__ = [
    "AppError",
    "AuthError",
    "ConfigurationError",
    "EmptyFileError",
    "EmptyResumeError",
    "FileTooLargeError",
    "GeminiUnavailableError",
    "InvalidAIResponseError",
    "InvalidFileError",
    "JobDescriptionTooLongError",
    "MissingJobDescriptionError",
    "NotFoundError",
    "RateLimitError",
    "UnauthorizedError",
]
