"""Configuracion centralizada por variables de entorno (sin secretos)."""

from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Ajustes globales cargados desde variables de entorno o fichero .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    urbanmove_environment: Literal["dev", "test", "prod"] = "dev"
    urbanmove_service_name: str = "urbanmove"
    urbanmove_log_level: str = "INFO"
    aws_region: str = "us-east-1"
    aws_endpoint_url: str | None = None
    urbanmove_events_topic_arn: str = ""

    @field_validator("aws_endpoint_url", mode="before")
    @classmethod
    def _empty_string_to_none(cls, value: str | None) -> str | None:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @field_validator("urbanmove_log_level", mode="before")
    @classmethod
    def _normalize_log_level(cls, value: str) -> str:
        return value.strip().upper()

    @property
    def environment(self) -> Literal["dev", "test", "prod"]:
        return self.urbanmove_environment

    @property
    def service_name(self) -> str:
        return self.urbanmove_service_name

    @property
    def log_level(self) -> str:
        return self.urbanmove_log_level

    @property
    def events_topic_arn(self) -> str:
        return self.urbanmove_events_topic_arn

    @property
    def is_localstack(self) -> bool:
        """Indica si el entorno apunta a LocalStack en lugar de AWS real."""
        return self.aws_endpoint_url is not None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Devuelve una instancia cacheada de Settings."""
    return Settings()
