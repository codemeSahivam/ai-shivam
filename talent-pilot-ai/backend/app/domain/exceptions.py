"""Domain exceptions for TalentPilot AI."""

from __future__ import annotations


class AppError(Exception):
    """Base application error with stable client-facing code and HTTP status."""

    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class InvalidFileError(AppError):
    def __init__(self, message: str = "Only PDF and DOCX files are supported.") -> None:
        super().__init__("INVALID_FILE", message, 400)


class EmptyFileError(AppError):
    def __init__(self, message: str = "Uploaded file is empty.") -> None:
        super().__init__("EMPTY_FILE", message, 400)


class FileTooLargeError(AppError):
    def __init__(self, message: str = "File exceeds the configured size limit.") -> None:
        super().__init__("FILE_TOO_LARGE", message, 400)


class EmptyResumeError(AppError):
    def __init__(self, message: str = "Could not extract text from the resume.") -> None:
        super().__init__("EMPTY_RESUME", message, 400)


class MissingJobDescriptionError(AppError):
    def __init__(self, message: str = "Job description is required.") -> None:
        super().__init__("MISSING_JOB_DESCRIPTION", message, 400)


class JobDescriptionTooLongError(AppError):
    def __init__(self, message: str = "Job description exceeds the character limit.") -> None:
        super().__init__("JOB_DESCRIPTION_TOO_LONG", message, 400)


class GeminiUnavailableError(AppError):
    def __init__(
        self,
        message: str = "AI service is temporarily unavailable. Please try again.",
    ) -> None:
        super().__init__("GEMINI_UNAVAILABLE", message, 503)


class InvalidAIResponseError(AppError):
    def __init__(self, message: str = "AI returned an invalid response.") -> None:
        super().__init__("INVALID_AI_RESPONSE", message, 500)


class AuthError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__("AUTH_ERROR", message, 400)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Authentication required.") -> None:
        super().__init__("UNAUTHORIZED", message, 401)


class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found.") -> None:
        super().__init__("NOT_FOUND", message, 404)


class RateLimitError(AppError):
    def __init__(self, message: str = "Too many requests. Please try again later.") -> None:
        super().__init__("RATE_LIMITED", message, 429)


class ConfigurationError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__("CONFIGURATION_ERROR", message, 500)
