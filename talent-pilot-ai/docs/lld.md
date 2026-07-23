# TalentPilot AI — Low-Level Design (LLD)

**Module:** Stage 1 — AI Resume Reviewer  
**Version:** 1.0  
**Status:** Approved for implementation

------------------------------------------------------------------------

## 1. Purpose

This LLD details module boundaries, function signatures, validation rules,
error codes, and request orchestration for Stage 1.

------------------------------------------------------------------------

## 2. Module Map

| Package | Responsibility |
|---------|----------------|
| `app.main` | FastAPI app factory, CORS, health route, exception handlers |
| `app.api.v1.analyze` | HTTP endpoint `POST /api/v1/analyze` |
| `app.core.config` | Environment-backed settings |
| `app.schemas.analysis` | Pydantic request/response and AI payload models |
| `app.prompts` | System and user prompt templates |
| `app.services.resume_parser` | PDF → normalized text via PyMuPDF |
| `app.services.gemini_service` | Gemini API client with retry/timeout |
| `app.services.analyzer` | Orchestrates parse → prompt → Gemini → validate |
| `app.utils.file_validation` | Upload size, MIME, extension checks |
| `app.utils.text` | Sanitize extracted / JD text |
| `app.exceptions` | Domain exceptions mapped to HTTP responses |

------------------------------------------------------------------------

## 3. Configuration

`Settings` (pydantic-settings):

| Field | Env | Default |
|-------|-----|---------|
| `gemini_api_key` | `GEMINI_API_KEY` | required |
| `gemini_model` | `GEMINI_MODEL` | `gemini-flash-latest` |
| `max_upload_bytes` | `MAX_UPLOAD_BYTES` | `10485760` (10 MB) |
| `max_job_description_chars` | `MAX_JOB_DESCRIPTION_CHARS` | `10000` |
| `gemini_timeout_seconds` | `GEMINI_TIMEOUT_SECONDS` | `60` |
| `gemini_max_retries` | `GEMINI_MAX_RETRIES` | `2` |
| `cors_origins` | `CORS_ORIGINS` | `http://localhost:3000,http://localhost:8080` |

------------------------------------------------------------------------

## 4. File Validation Rules

`validate_resume_upload(filename, content_type, size_bytes)`:

1. Reject if `size_bytes == 0` → `EMPTY_FILE`
2. Reject if `size_bytes > max_upload_bytes` → `FILE_TOO_LARGE`
3. Reject if extension not `.pdf` (case-insensitive) → `INVALID_FILE`
4. Reject if content-type present and not in `{application/pdf, application/octet-stream}` → `INVALID_FILE`

------------------------------------------------------------------------

## 5. Text Handling

- `normalize_whitespace(text)`: collapse runs of whitespace, strip ends.
- `sanitize_for_llm(text)`: strip null bytes / control chars except `\n` `\t`, then normalize.
- Empty resume text after parse → `EMPTY_RESUME`
- Empty / whitespace-only job description → `MISSING_JOB_DESCRIPTION`
- Job description length > max → `JOB_DESCRIPTION_TOO_LONG`

------------------------------------------------------------------------

## 6. Service Interfaces

### ResumeParser

```python
def extract_text(pdf_bytes: bytes) -> str
```

- Open with PyMuPDF from bytes.
- Concatenate page texts with newlines.
- Normalize whitespace.
- Raise `EmptyResumeError` if result is empty.

### PromptBuilder

```python
def build_messages(resume_text: str, job_description: str) -> tuple[str, str]
# returns (system_prompt, user_prompt)
```

### GeminiService

```python
async def generate_analysis_json(system_prompt: str, user_prompt: str) -> dict
```

- Call Gemini with JSON response mode.
- Retry transient failures up to `gemini_max_retries` with backoff.
- Raise `GeminiUnavailableError` on timeout / exhaustion.
- Raise `InvalidAIResponseError` if body is not parseable JSON.

### AnalyzerService

```python
async def analyze(pdf_bytes: bytes, filename: str, content_type: str | None, job_description: str) -> AnalysisResult
```

Pipeline: validate file → parse → sanitize JD → build prompts → Gemini → Pydantic validate → return.

------------------------------------------------------------------------

## 7. API Contract

### `POST /api/v1/analyze`

- Content-Type: `multipart/form-data`
- Fields: `resume` (file), `job_description` (string)

Success:

```json
{
  "success": true,
  "analysis": { ... }
}
```

Error:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_FILE",
    "message": "Only PDF files are supported."
  }
}
```

### `GET /health`

```json
{ "status": "ok" }
```

------------------------------------------------------------------------

## 8. Error Codes

| Code | HTTP | When |
|------|------|------|
| `INVALID_FILE` | 400 | Wrong type / extension |
| `EMPTY_FILE` | 400 | Zero-byte upload |
| `FILE_TOO_LARGE` | 400 | Over size limit |
| `EMPTY_RESUME` | 400 | No extractable text |
| `MISSING_JOB_DESCRIPTION` | 400 | Missing/blank JD |
| `JOB_DESCRIPTION_TOO_LONG` | 400 | JD over char limit |
| `GEMINI_UNAVAILABLE` | 503 | Timeout / API failure after retries |
| `INVALID_AI_RESPONSE` | 500 | JSON/schema validation failure |
| `INTERNAL_ERROR` | 500 | Unexpected errors |

Messages returned to clients are generic; never include API keys or stack traces.

------------------------------------------------------------------------

## 9. Analysis Schema Fields

| Field | Type | Constraints |
|-------|------|-------------|
| `match_score` | int | 0–100 |
| `ats_score` | int | 0–100 |
| `summary` | string | non-empty |
| `matching_skills` | string[] | |
| `missing_skills` | string[] | |
| `strengths` | string[] | |
| `weaknesses` | string[] | |
| `suggestions` | string[] | |
| `recommendation` | enum | `Strong Hire` \| `Hire` \| `Consider` \| `Reject` |

------------------------------------------------------------------------

## 10. Frontend Modules

| File | Role |
|------|------|
| `index.html` | Layout: upload, JD, analyze, results |
| `js/api.js` | `analyzeResume(file, jobDescription)` → fetch |
| `js/results.js` | Render analysis into DOM |
| `js/app.js` | Form submit, loading/error state |

API base URL from `window.TALENTPILOT_API_BASE` (default `http://localhost:8000`).

------------------------------------------------------------------------

## 11. Deployment Units

- **backend**: Uvicorn on port 8000
- **frontend**: nginx serving static files on port 80 (host 8080)
- Secrets via Compose env file only; `creds/` never mounted into images for production use

------------------------------------------------------------------------

**End of LLD**
