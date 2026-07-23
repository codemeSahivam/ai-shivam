.PHONY: run setup install test cov lint clean docker-up docker-down help

PYTHON ?= $(shell command -v python3.12 2>/dev/null || command -v python3.11 2>/dev/null || command -v python3)
VENV := backend/.venv
PIP := $(VENV)/bin/pip
DEPS_STAMP := $(VENV)/.deps-installed
HOST ?= 0.0.0.0
PORT ?= 8000

help:
	@echo "TalentPilot AI"
	@echo "  make run         Setup + start app"
	@echo "  make setup       Venv + deps + .env"
	@echo "  make test        Run pytest"
	@echo "  make cov         Run pytest with coverage"
	@echo "  make lint        Run ruff check if installed"
	@echo "  make docker-up   Build and run via Docker Compose"
	@echo "  make docker-down Stop Docker Compose"
	@echo "  make clean       Remove venv/caches"

run: setup
	@echo "Starting TalentPilot AI at http://localhost:$(PORT)"
	cd backend && .venv/bin/uvicorn app.main:app --reload --host $(HOST) --port $(PORT)

setup: $(DEPS_STAMP) .env

$(VENV)/bin/python:
	@if [ -z "$(PYTHON)" ]; then echo "Python 3.11+ required"; exit 1; fi
	$(PYTHON) -m venv $(VENV)

$(DEPS_STAMP): backend/requirements.txt | $(VENV)/bin/python
	$(PIP) install --upgrade pip
	$(PIP) install -r backend/requirements.txt
	@touch $(DEPS_STAMP)

install: $(DEPS_STAMP)

.env:
	cp .env.example .env
	@if [ -f creds/gemini/geminikey.txt ]; then \
		$(PYTHON) -c "from pathlib import Path; \
key=Path('creds/gemini/geminikey.txt').read_text().strip(); \
p=Path('.env'); p.write_text(p.read_text().replace('your_gemini_api_key_here', key))"; \
	fi

test: setup
	cd backend && .venv/bin/pytest -q

cov: setup
	cd backend && .venv/bin/pytest --cov=app --cov-report=term-missing -q

lint: setup
	@if [ -x backend/.venv/bin/ruff ]; then backend/.venv/bin/ruff check app; else echo "ruff not installed (optional)"; fi

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

clean:
	rm -rf backend/.venv backend/.pytest_cache backend/.coverage
	find backend -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
