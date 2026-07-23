import io

import pytest
from docx import Document

from app.core.config import Settings
from app.domain.exceptions import EmptyFileError, EmptyResumeError, FileTooLargeError, InvalidFileError
from app.infrastructure.parsing.resume_parser import extract_text
from app.utils.file_validation import validate_file_magic, validate_resume_upload
from app.utils.text import normalize_whitespace, sanitize_for_llm, sanitize_filename
from tests.conftest import make_pdf_bytes


def make_docx_bytes(text: str = "Jane Doe Python FastAPI") -> bytes:
    document = Document()
    document.add_paragraph(text)
    buffer = io.BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def test_normalize_whitespace() -> None:
    assert normalize_whitespace("  hello   world\n\n\n") == "hello world"


def test_sanitize_for_llm_strips_control_chars() -> None:
    assert sanitize_for_llm("hi\x00there") == "hithere"


def test_sanitize_filename() -> None:
    assert sanitize_filename("../evil.pdf") == "evil.pdf"


def test_validate_resume_rejects_txt(settings: Settings) -> None:
    with pytest.raises(InvalidFileError):
        validate_resume_upload("resume.txt", "text/plain", 100, settings)


def test_validate_resume_accepts_docx(settings: Settings) -> None:
    validate_resume_upload(
        "resume.docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        100,
        settings,
    )


def test_validate_resume_rejects_empty(settings: Settings) -> None:
    with pytest.raises(EmptyFileError):
        validate_resume_upload("resume.pdf", "application/pdf", 0, settings)


def test_validate_resume_rejects_large(settings: Settings) -> None:
    with pytest.raises(FileTooLargeError):
        validate_resume_upload(
            "resume.pdf",
            "application/pdf",
            settings.max_upload_bytes + 1,
            settings,
        )


def test_validate_file_magic_pdf() -> None:
    validate_file_magic(make_pdf_bytes(), "resume.pdf")


def test_validate_file_magic_rejects_spoofed_pdf() -> None:
    with pytest.raises(InvalidFileError):
        validate_file_magic(b"not-a-pdf", "resume.pdf")


def test_extract_text_from_pdf() -> None:
    pdf = make_pdf_bytes("Alice Example Python Engineer")
    text = extract_text(pdf, "resume.pdf")
    assert "Alice Example" in text


def test_extract_text_from_docx() -> None:
    docx = make_docx_bytes("Alice Example Python Engineer")
    text = extract_text(docx, "resume.docx")
    assert "Alice Example" in text


def test_extract_text_empty_pdf_raises() -> None:
    import fitz

    doc = fitz.open()
    doc.new_page()
    buffer = io.BytesIO()
    doc.save(buffer)
    doc.close()
    with pytest.raises(EmptyResumeError):
        extract_text(buffer.getvalue(), "resume.pdf")
