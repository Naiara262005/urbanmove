"""Tests unitarios para shared.events.event_factory."""

import pytest

from shared.events.event_factory import EventFactory
from shared.events.event_types import EventType
from shared.logging.correlation import correlation_context


def test_event_factory_rejects_blank_source() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        EventFactory(source="   ")


def test_event_factory_uses_active_correlation_context() -> None:
    factory = EventFactory(source="rides")
    with correlation_context("trace-abc-999"):
        event = factory.create(
            event_type=EventType.RIDE_FINISHED,
            payload={"ride_id": "R-1", "duration_minutes": 14},
        )

    assert event.source == "rides"
    assert event.event_type == EventType.RIDE_FINISHED
    assert event.correlation_id == "trace-abc-999"
    assert event.schema_version == "1.0"
    assert event.timestamp.tzinfo is not None
    assert event.payload == {"ride_id": "R-1", "duration_minutes": 14}


def test_event_factory_prefers_explicit_correlation_id() -> None:
    factory = EventFactory(source="inventory")
    with correlation_context("context-id"):
        event = factory.create(
            event_type=EventType.VEHICLE_PURCHASED,
            correlation_id="explicit-id",
        )

    assert event.correlation_id == "explicit-id"


def test_event_factory_generates_correlation_id_when_absent() -> None:
    factory = EventFactory(source="profiles")
    event = factory.create(event_type=EventType.USER_REGISTERED)
    assert event.correlation_id
    assert event.payload == {}
