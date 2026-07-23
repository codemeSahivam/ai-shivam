# Deployment Guide

## Local (`make run`)

See **[SETUP.md](../SETUP.md)** for the full walkthrough.

1. `cp .env.example .env` and set `GEMINI_API_KEY`
2. `make run`
3. Visit http://localhost:8000

## Docker Compose

1. Ensure `.env` exists with a valid Gemini key and a long `SECRET_KEY`
2. `make docker-up`
3. Visit http://localhost:8000
4. `make docker-down` to stop

## Production checklist

- `ENVIRONMENT=production`
- `HTTPS_ONLY=true`
- Strong unique `SECRET_KEY` (≥32 chars, not the example)
- Restrict `CORS_ORIGINS` and `TRUSTED_HOSTS`
- Persist `backend/data` (or move to Postgres later)
- Terminate TLS at a reverse proxy
- Disable or protect `/docs` if exposed publicly
