"""Tests unitarios para shared.events.domain_event y event_types."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from shared.events.domain_event import DomainEvent
from shared.events.event_types import EventType

MANDATORY_EVENTS = {
    "UserRegistered",
    "VehiclePurchased",
    "VehicleReserved",
    "ReservationCancelled",
    "ReservationExpired",
    "RideStarted",
    "RideFinished",
    "VehicleBatteryLow",
    "VehicleWithdrawnForMaintenance",
    "VehicleReturnedToService",
    "DemandHotspotDetected",
    "RelocationOrderCreated",
    "RelocationOrderCompleted",
}


def test_all_mandatory_event_types_exist() -> None:
    defined_values = {event.value for event in EventType}
    assert MANDATORY_EVENTS.issubset(defined_values)


def test_domain_event_is_immutable_and_roundtrips_json() -> None:
    event = DomainEvent(
        event_id=uuid4(),
        timestamp=datetime.now(UTC),
        source="reservations",
        event_type=EventType.VEHICLE_RESERVED,
        schema_version="1.0",
        correlation_id="corr-123",
        payload={"vehicle_id": "V-001", "user_id": "U-42"},
    )

    with pytest.raises(ValidationError):
        event.source = "rides"  # type: ignore[misc]

    serialized = event.to_json()
    restored = DomainEvent.from_json(serialized)
    assert restored == event


def test_domain_event_rejects_naive_timestamp() -> None:
    naive_dt = datetime(2026, 11, 24, 12, 0, 0)  # noqa: DTZ001
    with pytest.raises(ValidationError, match="timezone-aware"):
        DomainEvent(
            event_id=uuid4(),
            timestamp=naive_dt,
            source="rides",
            event_type=EventType.RIDE_STARTED,
            correlation_id="corr-456",
        )
