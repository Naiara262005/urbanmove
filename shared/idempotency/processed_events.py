"""Control de idempotencia para consumidores de eventos (dedupe por event_id)."""

from threading import Lock
from typing import Protocol
from uuid import UUID


class ProcessedEventsStore(Protocol):
    """Puerto para registrar y consultar eventos ya procesados."""

    def has_been_processed(self, event_id: UUID) -> bool:
        """Indica si el evento ya fue procesado anteriormente."""
        ...

    def mark_as_processed(self, event_id: UUID) -> bool:
        """Marca el evento como procesado de forma atomica.

        Returns:
            True si el evento es nuevo y se registro correctamente;
            False si ya habia sido procesado antes (duplicado).
        """
        ...


class InMemoryProcessedEventsStore:
    """Adaptador en memoria thread-safe para tests unitarios."""

    def __init__(self) -> None:
        self._processed: set[UUID] = set()
        self._lock = Lock()

    def has_been_processed(self, event_id: UUID) -> bool:
        with self._lock:
            return event_id in self._processed

    def mark_as_processed(self, event_id: UUID) -> bool:
        with self._lock:
            if event_id in self._processed:
                return False
            self._processed.add(event_id)
            return True

    def clear(self) -> None:
        with self._lock:
            self._processed.clear()
