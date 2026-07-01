"""Environment-backed application settings."""

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables or a local file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "PIA API"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True
    database_url: str = "postgresql+psycopg://pia:pia@postgres:5432/pia"
    jwt_secret: SecretStr = SecretStr("change-me")
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance for the current process."""
    return Settings()
