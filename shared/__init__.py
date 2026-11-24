"""Paquete compartido de UrbanMove: configuracion, eventos, AWS, logging e idempotencia."""

from shared.aws.client_factory import AWSClientFactory
from shared.config import Settings, get_settings
from shared.events.domain_event import DomainEvent
from shared.events.event_factory import EventFactory
from shared.events.event_types import EventType
from shared.events.publisher import (
    EventPublisher,
    InMemoryEventPublisher,
    SNSEventPublisher,
)
from shared.idempotency.processed_events import (
    InMemoryProcessedEventsStore,
    ProcessedEventsStore,
)
from shared.logging.correlation import (
    correlation_context,
    ensure_correlation_id,
    get_correlation_id,
    set_correlation_id,
)
from shared.logging.json_logger import get_logger

__all__ = [
    "AWSClientFactory",
    "DomainEvent",
    "EventFactory",
    "EventPublisher",
    "EventType",
    "InMemoryEventPublisher",
    "InMemoryProcessedEventsStore",
    "ProcessedEventsStore",
    "SNSEventPublisher",
    "Settings",
    "correlation_context",
    "ensure_correlation_id",
    "get_correlation_id",
    "get_logger",
    "get_settings",
    "set_correlation_id",
]
