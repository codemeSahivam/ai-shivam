# TalentPilot AI

**AI Resume Reviewer** — upload a PDF/DOCX resume and a job description, get structured hiring insights from Google Gemini.

One FastAPI process serves both the **Vanilla JS UI** (light/dark theme) and the **REST API**. Optional sign-in saves analysis history in SQLite.

---

## Features

- PDF and DOCX resume upload
- Gemini analysis: match score, ATS score, score breakdowns, skills, strengths/weaknesses, suggestions, hiring recommendation
- Sample resume + job description
- Export analysis as Markdown or printable PDF
- Session history (last 5 in the browser)
- Register / sign in with saved history (SQLite)
- Light and dark UI themes (purple/orange brand accents)

---

## Quick start

**Prerequisites:** Python **3.11 or 3.12**, Make, and a [Google Gemini API key](https://ai.google.dev/).

```bash
cp .env.example .env
# Edit .env and set GEMINI_API_KEY=...

make run
```

Open **http://localhost:8000**

Full setup details: **[SETUP.md](SETUP.md)**

---

## Commands

| Command | Purpose |
|---------|---------|
| `make run` | Create venv, install deps, ensure `.env`, start app |
| `make setup` | Venv + deps + `.env` only |
| `make test` | Run pytest |
| `make cov` | Pytest with coverage |
| `make docker-up` | Build and run with Docker Compose |
| `make docker-down` | Stop Compose stack |
| `make clean` | Remove venv and caches |
| `make help` | List targets |

---

## Architecture

```text
Browser (frontend/)
    │
    ▼
FastAPI ── api → application → infrastructure ──► Google Gemini
                              └─ repositories ──► SQLite
```

| Area | Path |
|------|------|
| Backend app | `backend/app/` |
| UI | `frontend/` |
| Docs | `docs/` |
| Agent rules | `AGENTS.md`, `.cursorrules` |

---

## API (summary)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/analyze` | Analyze resume (multipart: `resume`, `job_description`) |
| `POST` | `/api/v1/auth/register` · `/login` · `/logout` | Auth |
| `GET` | `/api/v1/auth/me` | Current user |
| `GET` | `/api/v1/history` | Saved analyses |
| `GET` | `/api/v1/samples/*` | Sample JD / demo PDF |

Interactive docs: **http://localhost:8000/docs**

---

## Documentation

| Doc | Description |
|-----|-------------|
| [SETUP.md](SETUP.md) | Install, env, local & Docker setup |
| [AGENTS.md](AGENTS.md) | Guidance for Cursor / AI coding agents |
| [docs/PRD.md](docs/PRD.md) / [requirement.md](docs/requirement.md) | Requirements |
| [docs/HLD.md](docs/HLD.md) / [hld.md](docs/hld.md) | High-level design |
| [docs/LLD.md](docs/LLD.md) / [lld.md](docs/lld.md) | Low-level design |
| [docs/API_SPECIFICATION.md](docs/API_SPECIFICATION.md) | API overview |
| [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) | Deploy checklist |
| [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md) | Testing conventions |
| [docs/CODING_STANDARDS.md](docs/CODING_STANDARDS.md) | Code standards |
| [docs/ARCHITECTURE_DECISIONS.md](docs/ARCHITECTURE_DECISIONS.md) | ADRs |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | Version history |

---

## Security

- Never commit `.env`, `creds/`, or database files
- Keep `GEMINI_API_KEY` and `SECRET_KEY` server-side only
- Production: `ENVIRONMENT=production`, strong `SECRET_KEY`, `HTTPS_ONLY=true`

See [SETUP.md](SETUP.md) and [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md).
