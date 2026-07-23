# Coding Standards — TalentPilot AI

## Python

- PEP-8; PascalCase classes/exceptions; snake_case functions/modules; UPPER_SNAKE constants
- Type hints on all public functions
- No bare `except`; domain exceptions in `app.domain.exceptions`
- No `print()` — use structured logging
- Business logic in `application/`; routes stay thin; DI via FastAPI `Depends`

## JavaScript

- ES modules only; no inline scripts
- Prefer DOM APIs / `textContent` over `innerHTML`
- Config in `frontend/js/config.js`

## Security

- Validate uploads (extension, size while streaming, magic bytes)
- Secrets only via environment variables
- Fail fast in production when secrets are weak/missing

## Testing

- Every public use case and validator has tests
- Use `dependency_overrides` for Gemini fakes
- Target ≥85% line coverage (`make cov`)
