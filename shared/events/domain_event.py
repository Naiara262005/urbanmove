"""Modelo inmutable del contrato de eventos de dominio."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from shared.events.event_types import EventType


class DomainEvent(BaseModel):
    """Contrato inmutable de cualquier evento publicado en UrbanMove."""

    model_config = ConfigDict(frozen=True)

    event_id: UUID
    timestamp: datetime
    source: str = Field(min_length=1)
    event_type: EventType
    schema_version: str = Field(default="1.0", min_length=1)
    correlation_id: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("timestamp")
    @classmethod
    def _ensure_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            msg = "timestamp must be timezone-aware (UTC)"
            raise ValueError(msg)
        return value.astimezone(UTC)

    def to_json(self) -> str:
        """Serializa el evento a JSON canonico."""
        return self.model_dump_json()

    @classmethod
    def from_json(cls, raw_json: str) -> "DomainEvent":
        """Deserializa y valida un evento desde JSON."""
        return cls.model_validate_json(raw_json)
