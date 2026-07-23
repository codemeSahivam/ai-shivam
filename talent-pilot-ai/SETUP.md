# Setup Guide — TalentPilot AI

Step-by-step setup for local development and Docker. For product overview and docs index, see [README.md](README.md).

---

## Prerequisites

| Tool | Notes |
|------|--------|
| **Python 3.11 or 3.12** | Prefer 3.12. `python3.14` may lack wheels for some deps. |
| **Make** | Used for `make run`, `make test`, etc. |
| **Gemini API key** | From [Google AI Studio](https://aistudio.google.com/) / AI Developer console |
| **Docker** (optional) | Only needed for `make docker-up` |

Verify Python:

```bash
python3.12 --version   # or python3.11 --version
```

---

## 1. Clone and enter the project

```bash
cd talent-pilot-ai
```

---

## 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set at least:

```env
GEMINI_API_KEY=your_real_key_here
SECRET_KEY=replace-with-a-long-random-string-at-least-32-chars
```

### Optional: seed key from local creds

If you keep a key in `creds/gemini/geminikey.txt` (gitignored), `make setup` / `make run` will copy `.env.example` → `.env` and seed `GEMINI_API_KEY` automatically when `.env` does not exist yet.

### Important variables

| Variable | Purpose | Typical local value |
|----------|---------|---------------------|
| `GEMINI_API_KEY` | Google Gemini auth | *(required)* |
| `GEMINI_MODEL` | Model id | `gemini-flash-latest` |
| `ENVIRONMENT` | `development` / `staging` / `production` | `development` |
| `SECRET_KEY` | Session cookie signing | long random string |
| `DATABASE_URL` | SQLAlchemy URL | `sqlite:///./data/talentpilot.db` |
| `HTTPS_ONLY` | Secure session cookies | `false` locally |
| `CORS_ORIGINS` | Allowed origins | `http://localhost:8000,http://127.0.0.1:8000` |
| `TRUSTED_HOSTS` | Host header allowlist | `localhost,127.0.0.1` |
| `MAX_UPLOAD_BYTES` | Upload size cap | `10485760` (10 MB) |
| `RATE_LIMIT_*` | Per-IP per-minute limits | see `.env.example` |

**Production** (`ENVIRONMENT=production`) refuses to boot unless:

- `GEMINI_API_KEY` is set
- `SECRET_KEY` is strong and not the default
- `HTTPS_ONLY=true`

Full template: [.env.example](.env.example)

---

## 3. Local run (recommended)

One command creates the venv, installs `backend/requirements.txt`, ensures `.env`, and starts Uvicorn:

```bash
make run
```

Then open:

- UI: http://localhost:8000  
- API docs: http://localhost:8000/docs  
- Health: http://localhost:8000/health  

Stop with `Ctrl+C`.

### Setup only (no server)

```bash
make setup
```

### Manual run (without Make)

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
set -a && source ../.env && set +a
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 4. Verify the UI

1. Open http://localhost:8000  
2. Toggle **Light / Dark** in the header  
3. Click **Load sample resume + JD**  
4. Click **Analyze Resume**  
5. Optionally **Sign in** / register to save history  

---

## 5. Tests

```bash
make test
make cov
```

Tests use an isolated SQLite DB and a fake Gemini client. They do not call the real Gemini API.

---

## 6. Docker Compose

Requires Docker Desktop (or equivalent) running and a valid `.env`.

```bash
make docker-up
```

- App: http://localhost:8000  
- SQLite data: Docker volume `app-data`  

Stop:

```bash
make docker-down
```

Compose uses `ENVIRONMENT=development` by default for local containers. For real production images, set production env vars as in [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md).

---

## 7. Project layout (after setup)

```text
talent-pilot-ai/
├── .env                 # local secrets (gitignored)
├── backend/
│   ├── .venv/           # created by make setup
│   ├── data/            # SQLite DB (gitignored)
│   ├── app/             # FastAPI application
│   ├── tests/
│   └── requirements.txt
├── frontend/            # Vanilla JS UI + themes
├── docs/
├── AGENTS.md
├── SETUP.md             # this file
└── Makefile
```

---

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| `GEMINI_API_KEY` / analyze returns 503 | Set a valid key in `.env`; restart `make run` |
| Pip / pydantic build fails on Python 3.14 | Use **3.11 or 3.12**: `PYTHON=$(which python3.12) make run` |
| Port 8000 in use | `PORT=8001 make run` or stop the other process |
| Theme flash / wrong theme | Clear `localStorage` key `talentpilot_theme_v1` or toggle in the header |
| Docker “cannot connect to daemon” | Start Docker Desktop, then `make docker-up` |
| `TrustedHost` / 400 errors | Ensure `TRUSTED_HOSTS` includes the host you use (`localhost`, `127.0.0.1`) |
| Session / login not sticking | Same origin (use `:8000` UI, not a separate static server); cookies enabled |

Clean rebuild of the Python env:

```bash
make clean
make run
```

---

## Related docs

- [README.md](README.md) — overview  
- [AGENTS.md](AGENTS.md) — AI agent / Cursor conventions  
- [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) — production checklist  
- [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md) — test conventions  
