# Architecture Decision Records

## ADR-0001 — SQLite + session cookies for Stage 2 auth

**Status:** Accepted  
**Context:** Need persisted history without operating a Postgres cluster for learning/demo.  
**Decision:** SQLite file DB + signed session cookies; repository layer abstracts persistence.  
**Consequences:** Simple local ops; swap to Postgres via `DATABASE_URL` later; single-node write limits.

## ADR-0002 — Google Gemini as sole Stage-1/2 LLM

**Status:** Accepted  
**Context:** HLD locked Gemini.  
**Decision:** `GeminiService` behind `LLMClient` protocol for future providers.  
**Consequences:** Provider swap without rewriting use cases.

## ADR-0003 — Single FastAPI process serves UI + API

**Status:** Accepted  
**Context:** Prefer one microservice for Stage 1–2.  
**Decision:** FastAPI mounts `frontend/` static assets and exposes `/api/v1/*`.  
**Consequences:** Same-origin simplicity; scale UI separately later if needed.

## ADR-0004 — Layered architecture (API → Application → Infrastructure)

**Status:** Accepted  
**Context:** Enterprise maintainability and SOLID.  
**Decision:** Thin routes, use cases, repositories/adapters.  
**Consequences:** More files; clearer testing and DI.
