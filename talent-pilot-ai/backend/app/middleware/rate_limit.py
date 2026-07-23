"""Simple in-memory rate limiting (single-process readiness)."""

from __future__ import annotations

import time
from collections import defaultdict, deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp

from app.core.config import Settings
from app.domain.exceptions import RateLimitError


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, settings: Settings) -> None:
        super().__init__(app)
        self._settings = settings
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        limit: int | None = None
        if path.endswith("/api/v1/analyze") and request.method == "POST":
            limit = self._settings.rate_limit_analyze_per_minute
        elif path.startswith("/api/v1/auth/") and request.method == "POST":
            limit = self._settings.rate_limit_auth_per_minute

        if limit is not None:
            client = request.client.host if request.client else "unknown"
            key = f"{client}:{path}"
            now = time.time()
            window = self._hits[key]
            while window and now - window[0] > 60:
                window.popleft()
            if len(window) >= limit:
                error = RateLimitError()
                return JSONResponse(
                    status_code=error.status_code,
                    content={
                        "success": False,
                        "error": {"code": error.code, "message": error.message},
                    },
                )
            window.append(now)

        return await call_next(request)
