# Changelog

## 2.0.0 — Enterprise refactor

- Layered backend: `domain`, `application`, `infrastructure`, `middleware`, `api/deps`
- FastAPI dependency injection; repositories; Alembic scaffold
- Security: streaming upload limits, magic-byte checks, security headers, request IDs, rate-limit middleware, production settings fail-fast
- Frontend moved to `frontend/` with modular ES modules; removed Tailwind CDN
- Docker + Compose restored; docs expanded

## 1.1.0 — Stage 1.5 / 2 features

- DOCX, score breakdowns, export, samples, session history
- SQLite auth + saved analyses

## 1.0.0 — Stage 1

- PDF resume analysis via Gemini; single-process UI + API
