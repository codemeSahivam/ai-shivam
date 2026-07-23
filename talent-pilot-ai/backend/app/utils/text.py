"""Text sanitization utilities."""

from __future__ import annotations

import re

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_WHITESPACE = re.compile(r"[ \t]+")
_MULTI_NEWLINE = re.compile(r"\n{3,}")


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _WHITESPACE.sub(" ", text)
    text = _MULTI_NEWLINE.sub("\n\n", text)
    return text.strip()


def sanitize_for_llm(text: str) -> str:
    cleaned = _CONTROL_CHARS.sub("", text)
    return normalize_whitespace(cleaned)


def sanitize_filename(filename: str | None) -> str:
    if not filename:
        return "resume.pdf"
    name = filename.replace("\\", "/").split("/")[-1]
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    return name[:255] or "resume.pdf"
