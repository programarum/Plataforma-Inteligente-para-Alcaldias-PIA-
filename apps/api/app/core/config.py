"""Environment-backed application configuration."""

from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "PIA API"
    app_version: str = "0.1.0"
    environment: Literal["development", "testing", "staging", "production"] = (
        "development"
    )
    debug: bool = True
    database_url: str = "postgresql+psycopg://pia:pia@postgres:5432/pia"
    jwt_secret: SecretStr = SecretStr("change-me")
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings instance."""
    return Settings()


settings = get_settings()

