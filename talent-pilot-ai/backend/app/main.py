"""FastAPI application factory."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.api.v1 import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.domain.exceptions import AppError
from app.infrastructure.db.session import init_db
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.security import RequestContextMiddleware, SecurityHeadersMiddleware
from app.schemas.common import ErrorBody, ErrorResponse, HealthResponse

logger = get_logger(__name__)


def _resolve_frontend_dir() -> Path | None:
    settings = get_settings()
    candidates: list[Path] = []
    if settings.frontend_dir:
        candidates.append(Path(settings.frontend_dir))
    # Preferred: repo frontend/
    candidates.append(Path(__file__).resolve().parents[2] / "frontend")
    # Legacy: backend/app/static
    candidates.append(Path(__file__).resolve().parent / "static")
    for path in candidates:
        if path.exists() and (path / "index.html").exists():
            return path
    return None


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings)
    init_db(settings)

    app = FastAPI(
        title="TalentPilot AI",
        version="2.0.0",
        description="Enterprise AI Resume Reviewer microservice (UI + API).",
    )

    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(RateLimitMiddleware, settings=settings)
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.secret_key,
        max_age=settings.session_max_age_seconds,
        same_site="lax",
        https_only=settings.https_only,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "X-Request-ID"],
    )
    if settings.trusted_host_list:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=[*settings.trusted_host_list, "testserver"],
        )

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        body = ErrorResponse(success=False, error=ErrorBody(code=exc.code, message=exc.message))
        return JSONResponse(status_code=exc.status_code, content=body.model_dump())

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        message = "; ".join(
            f"{'.'.join(str(part) for part in err.get('loc', []))}: {err.get('msg')}"
            for err in exc.errors()
        )
        body = ErrorResponse(
            success=False,
            error=ErrorBody(code="VALIDATION_ERROR", message=message or "Invalid request."),
        )
        return JSONResponse(status_code=422, content=body.model_dump())

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "-")
        logger.exception("Unhandled error request_id=%s type=%s", request_id, type(exc).__name__)
        body = ErrorResponse(
            success=False,
            error=ErrorBody(code="INTERNAL_ERROR", message="An unexpected error occurred."),
        )
        return JSONResponse(status_code=500, content=body.model_dump())

    @app.get("/health", response_model=HealthResponse, tags=["health"])
    async def health() -> HealthResponse:
        return HealthResponse(status="ok")

    app.include_router(api_router)

    frontend_dir = _resolve_frontend_dir()
    if frontend_dir is not None:
        css_dir = frontend_dir / "css"
        js_dir = frontend_dir / "js"
        assets_dir = frontend_dir / "assets"
        if css_dir.exists():
            app.mount("/css", StaticFiles(directory=css_dir), name="css")
        if js_dir.exists():
            app.mount("/js", StaticFiles(directory=js_dir), name="js")
        if assets_dir.exists():
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

        favicon_png = assets_dir / "favicon.png"
        favicon_svg = assets_dir / "logo.svg"

        @app.get("/favicon.ico", include_in_schema=False)
        async def serve_favicon() -> FileResponse:
            if favicon_png.exists():
                return FileResponse(favicon_png, media_type="image/png")
            return FileResponse(favicon_svg, media_type="image/svg+xml")

        @app.get("/")
        async def serve_index() -> FileResponse:
            return FileResponse(frontend_dir / "index.html")

    return app


app = create_app()
