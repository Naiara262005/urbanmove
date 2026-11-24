"""Patron Factory Method para construir eventos de dominio validados."""

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from shared.events.domain_event import DomainEvent
from shared.events.event_types import EventType
from shared.logging.correlation import get_correlation_id


class EventFactory:
    """Construye eventos inmutables garantizando metadatos y correlation_id."""

    def __init__(self, source: str, schema_version: str = "1.0") -> None:
        if not source.strip():
            msg = "source must be a non-empty service name"
            raise ValueError(msg)
        self._source = source.strip()
        self._schema_version = schema_version

    @property
    def source(self) -> str:
        return self._source

    def create(
        self,
        event_type: EventType,
        payload: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> DomainEvent:
        """Crea un DomainEvent con UUID, timestamp UTC y correlation_id activo."""
        resolved_correlation_id = correlation_id or get_correlation_id() or str(uuid4())
        return DomainEvent(
            event_id=uuid4(),
            timestamp=datetime.now(UTC),
            source=self._source,
            event_type=event_type,
            schema_version=self._schema_version,
            correlation_id=resolved_correlation_id,
            payload=dict(payload) if payload is not None else {},
        )
