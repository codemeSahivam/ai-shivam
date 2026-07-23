"""Application settings loaded from environment variables."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.domain.enums import Environment
from app.domain.exceptions import ConfigurationError

DEFAULT_DEV_SECRET = "dev-change-me-talentpilot-secret"
MAX_UPLOAD_BYTES_DEFAULT = 10 * 1024 * 1024
MAX_JOB_DESCRIPTION_CHARS_DEFAULT = 10_000


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: Environment = Environment.DEVELOPMENT
    log_level: str = "INFO"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-flash-latest"
    gemini_timeout_seconds: float = 60.0
    gemini_max_retries: int = 2
    max_upload_bytes: int = MAX_UPLOAD_BYTES_DEFAULT
    max_job_description_chars: int = MAX_JOB_DESCRIPTION_CHARS_DEFAULT
    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000"
    secret_key: str = DEFAULT_DEV_SECRET
    database_url: str = "sqlite:///./data/talentpilot.db"
    session_max_age_seconds: int = 60 * 60 * 24 * 14
    https_only: bool = False
    trusted_hosts: str = "localhost,127.0.0.1"
    rate_limit_analyze_per_minute: int = 10
    rate_limit_auth_per_minute: int = 20
    frontend_dir: str = ""

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        return value.upper()

    @property
    def is_production(self) -> bool:
        return self.environment == Environment.PRODUCTION

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def trusted_host_list(self) -> list[str]:
        return [host.strip() for host in self.trusted_hosts.split(",") if host.strip()]

    @property
    def sqlite_path(self) -> Path | None:
        if not self.database_url.startswith("sqlite:///"):
            return None
        raw = self.database_url.removeprefix("sqlite:///")
        return Path(raw)

    def validate_for_boot(self) -> None:
        if self.is_production:
            if not self.gemini_api_key:
                raise ConfigurationError("GEMINI_API_KEY is required in production.")
            if self.secret_key == DEFAULT_DEV_SECRET or len(self.secret_key) < 32:
                raise ConfigurationError(
                    "SECRET_KEY must be a strong non-default value in production."
                )
            if not self.https_only:
                raise ConfigurationError("HTTPS_ONLY must be true in production.")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.validate_for_boot()
    return settings
