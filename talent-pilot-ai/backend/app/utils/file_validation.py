"""Upload validation helpers."""

from __future__ import annotations

from pathlib import Path

from app.core.config import Settings
from app.domain.exceptions import EmptyFileError, FileTooLargeError, InvalidFileError

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/octet-stream",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
PDF_MAGIC = b"%PDF"
ZIP_MAGIC = b"PK"


def validate_resume_upload(
    filename: str | None,
    content_type: str | None,
    size_bytes: int,
    settings: Settings,
) -> None:
    if size_bytes <= 0:
        raise EmptyFileError()

    if size_bytes > settings.max_upload_bytes:
        raise FileTooLargeError()

    if not filename:
        raise InvalidFileError()

    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise InvalidFileError()

    if content_type:
        normalized = content_type.split(";")[0].strip().lower()
        if normalized and normalized not in ALLOWED_CONTENT_TYPES:
            raise InvalidFileError()


def validate_file_magic(file_bytes: bytes, filename: str) -> None:
    extension = Path(filename).suffix.lower()
    if extension == ".pdf":
        if not file_bytes.startswith(PDF_MAGIC):
            raise InvalidFileError("File content is not a valid PDF.")
    elif extension == ".docx":
        if not file_bytes.startswith(ZIP_MAGIC):
            raise InvalidFileError("File content is not a valid DOCX.")
