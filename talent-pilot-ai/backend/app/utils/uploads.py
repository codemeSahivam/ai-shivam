"""Safe upload reading with size enforcement."""

from __future__ import annotations

from fastapi import UploadFile

from app.core.config import Settings
from app.domain.exceptions import FileTooLargeError


async def read_upload_limited(upload: UploadFile, settings: Settings) -> bytes:
    """Read upload in chunks and fail fast when size exceeds the configured limit."""
    chunks: list[bytes] = []
    total = 0
    chunk_size = 64 * 1024
    while True:
        chunk = await upload.read(chunk_size)
        if not chunk:
            break
        total += len(chunk)
        if total > settings.max_upload_bytes:
            raise FileTooLargeError()
        chunks.append(chunk)
    return b"".join(chunks)
