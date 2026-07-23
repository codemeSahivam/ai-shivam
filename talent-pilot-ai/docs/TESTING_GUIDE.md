# Testing Guide

## Run tests

```bash
make test
make cov
```

## Layout

- `backend/tests/test_validation_and_parser.py` — unit validation/parser
- `backend/tests/test_analyze_api.py` — analyze API + samples + UI
- `backend/tests/test_auth_history.py` — auth + saved history

## Conventions

- Fake Gemini via `app.dependency_overrides[provide_gemini]`
- Isolated SQLite per test (`tmp_path`)
- Assert stable error codes (`INVALID_FILE`, `NOT_FOUND`, …)
