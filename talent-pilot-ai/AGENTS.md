# AGENTS.md — TalentPilot AI

Guidance for AI coding agents working in this repository. Keep this file updated when architecture, commands, or conventions change.

---

## Product

**TalentPilot AI** — Stage 1+ AI Resume Reviewer.

Users upload a PDF/DOCX resume and a job description; the app analyzes fit via **Google Gemini** and returns structured scores, skills, breakdowns, and hiring recommendations. Optional auth persists history in **SQLite**.

---

## Quick commands

| Command | Purpose |
|---------|---------|
| `make run` | Create venv, install deps, ensure `.env`, start app on `:8000` |
| `make setup` | Venv + deps + `.env` only |
| `make test` | Run pytest |
| `make cov` | Pytest + coverage |
| `make docker-up` / `make docker-down` | Docker Compose |
| `make clean` | Remove venv/caches |

App UI + API: http://localhost:8000 · OpenAPI: http://localhost:8000/docs

First-time install: see **[SETUP.md](SETUP.md)**.

---

## Repository layout

```text
talent-pilot-ai/
├── backend/app/
│   ├── api/                 # Thin FastAPI routes + deps.py
│   ├── application/         # Use cases (analyze, auth, history)
│   ├── domain/              # Exceptions, enums
│   ├── infrastructure/      # DB/ORM/repos, Gemini, resume parser
│   ├── middleware/          # Request ID, security headers, rate limit
│   ├── schemas/             # Pydantic DTOs (split by domain)
│   ├── prompts/             # LLM system/user prompts
│   ├── core/                # Settings, logging
│   ├── utils/               # Validation, text, uploads
│   └── main.py              # App factory; mounts frontend/
├── frontend/
│   ├── index.html
│   ├── css/styles.css       # Light/dark theme via CSS variables
│   ├── assets/              # demo-resume.pdf, hero-illustration.png
│   └── js/
│       ├── theme-boot.js    # Early theme apply (no FOUC)
│       ├── config.js
│       ├── app.js
│       ├── pages/main.js
│       ├── components/
│       ├── services/
│       └── utils/           # theme.js, dom.js
├── docs/                    # PRD, HLD, LLD, ADRs, guides, diagrams
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── .cursorrules
└── AGENTS.md                # This file
```

---

## Architecture rules (mandatory)

```text
API (thin) → Application (use cases) → Infrastructure (adapters)
                ↘ Domain (exceptions / enums)
```

1. **No business logic in routes** — routes validate HTTP and call use cases.
2. **Dependency injection** via FastAPI `Depends` (`app/api/deps.py`) or constructors.
3. **Repositories** for persistence — do not query ORM from routes.
4. **LLM** behind `LLMClient` protocol; Gemini lives in `infrastructure/gemini/`.
5. **Domain errors** from `app.domain.exceptions` with stable `code` + HTTP status.
6. Unified error envelope: `{ "success": false, "error": { "code", "message" } }`.

---

## Stack locks

| Layer | Allowed | Forbidden |
|-------|---------|-----------|
| Backend | Python 3.11+/3.12, FastAPI, Pydantic v2, SQLAlchemy, Gemini, PyMuPDF, python-docx | Django, Flask as primary app |
| Frontend | Vanilla JS ES modules, CSS variables, light/dark theme | React, Next.js, Vue, Angular |
| Data | SQLite (+ Alembic scaffold); Postgres-ready via `DATABASE_URL` | Ad-hoc SQL in routes |
| Run | `make run` or Docker Compose | Committing secrets |

---

## Frontend / theme conventions

- Theme tokens live in `frontend/css/styles.css` as CSS variables under `[data-theme="light"]` and `[data-theme="dark"]`.
- Brand accents: **purple** (primary) + **orange** (accent); soft blue surfaces in light mode; navy surfaces in dark mode.
- Persist theme with `talentpilot_theme_v1` in `localStorage` (`frontend/js/utils/theme.js` + `theme-boot.js`).
- Prefer `textContent` / DOM helpers in `utils/dom.js` — avoid unsafe `innerHTML`.
- No inline `<script>` blocks for app logic; keep modules under `js/{pages,components,services,utils}`.
- When changing visuals, update both light and dark tokens.

---

## Security & config

- Secrets only in `.env` (never commit). `.env.example` is the template; `creds/` is gitignored.
- Production (`ENVIRONMENT=production`) must fail fast on weak `SECRET_KEY`, missing `GEMINI_API_KEY`, or `HTTPS_ONLY=false`.
- Uploads: stream with size cap, extension allowlist (PDF/DOCX), magic-byte checks.
- Do not log API keys or raw resume PII unnecessarily.

---

## Testing expectations

- Add/adjust tests under `backend/tests/` for every public behavior change.
- Fake Gemini with `app.dependency_overrides[provide_gemini]`.
- Use isolated SQLite (`tmp_path`) per test.
- Assert stable error codes (`INVALID_FILE`, `NOT_FOUND`, `UNAUTHORIZED`, …).
- Target ≥85% line coverage (`make cov`). Current suite should stay green.

---

## Documentation sync

When you change APIs, architecture, or UX meaningfully, update the relevant docs:

- `docs/API_SPECIFICATION.md` / live `/docs`
- `docs/CHANGELOG.md`
- `docs/ARCHITECTURE_DECISIONS.md` (new ADRs when decisions stick)
- `docs/PROMPT_DESIGN.md` / `backend/app/prompts/` if LLM contract changes
- This `AGENTS.md` and `.cursorrules` if agent conventions change

---

## Agent workflow checklist

Before coding:

1. Read this file and `.cursorrules`.
2. Locate the correct layer (do not dump logic into `api/`).

While coding:

3. Match existing naming (PEP-8 / project conventions).
4. Keep routes thin; inject deps.
5. Update light **and** dark theme if touching CSS.

After coding:

6. Run `make test` (or targeted pytest).
7. Update CHANGELOG / AGENTS / rules if conventions shifted.
8. Never commit `.env`, `creds/`, or DB files.

---

## Key entry points

| Concern | Path |
|---------|------|
| App factory | `backend/app/main.py` |
| DI providers | `backend/app/api/deps.py` |
| Analyze use case | `backend/app/application/analyze_resume.py` |
| Gemini adapter | `backend/app/infrastructure/gemini/client.py` |
| Theme JS | `frontend/js/utils/theme.js` |
| Theme CSS | `frontend/css/styles.css` |
| UI boot | `frontend/js/pages/main.js` |
