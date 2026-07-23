"""Database engine and session management."""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.infrastructure.db.orm import Base

_engine = None
_session_factory: sessionmaker[Session] | None = None
_initialized_url: str | None = None


def _resolve_url(settings: Settings) -> str:
    sqlite_path = settings.sqlite_path
    if sqlite_path is not None:
        if not sqlite_path.is_absolute():
            sqlite_path = sqlite_path.resolve()
        sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{sqlite_path}"
    return settings.database_url


def init_db(settings: Settings) -> None:
    global _engine, _session_factory, _initialized_url

    url = _resolve_url(settings)
    if _engine is not None and _initialized_url == url:
        return

    connect_args = {"check_same_thread": False} if url.startswith("sqlite:") else {}
    _engine = create_engine(url, connect_args=connect_args, pool_pre_ping=True)
    _session_factory = sessionmaker(bind=_engine, autoflush=False, autocommit=False)
    _initialized_url = url
    try:
        Base.metadata.create_all(bind=_engine, checkfirst=True)
    except OperationalError as exc:
        if "already exists" not in str(exc).lower():
            raise


def get_session_factory() -> sessionmaker[Session]:
    if _session_factory is None:
        raise RuntimeError("Database not initialized")
    return _session_factory


def get_db_session() -> Generator[Session, None, None]:
    factory = get_session_factory()
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def reset_db_state() -> None:
    global _engine, _session_factory, _initialized_url
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _session_factory = None
    _initialized_url = None
