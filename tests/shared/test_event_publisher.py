"""Tests unitarios para InMemoryEventPublisher y SNSEventPublisher."""

import json
from unittest.mock import MagicMock

import pytest

from shared.events.event_factory import EventFactory
from shared.events.event_types import EventType
from shared.events.publisher import InMemoryEventPublisher, SNSEventPublisher


def test_in_memory_publisher_stores_and_filters_events() -> None:
    publisher = InMemoryEventPublisher()
    factory = EventFactory(source="reservations")

    e1 = factory.create(EventType.VEHICLE_RESERVED, {"vehicle_id": "B-1"})
    e2 = factory.create(EventType.RESERVATION_CANCELLED, {"vehicle_id": "B-1"})
    publisher.publish(e1)
    publisher.publish(e2)

    assert len(publisher.events) == 2
    assert publisher.by_type(EventType.VEHICLE_RESERVED) == [e1]

    publisher.clear()
    assert publisher.events == []


def test_sns_publisher_rejects_empty_topic_arn() -> None:
    with pytest.raises(ValueError, match="topic_arn"):
        SNSEventPublisher(sns_client=MagicMock(), topic_arn="  ")


def test_sns_publisher_sends_json_and_filter_attributes() -> None:
    mock_sns = MagicMock()
    topic_arn = "arn:aws:sns:us-east-1:000000000000:urbanmove-events"
    publisher = SNSEventPublisher(sns_client=mock_sns, topic_arn=topic_arn)
    event = EventFactory(source="maintenance").create(
        event_type=EventType.VEHICLE_WITHDRAWN_FOR_MAINTENANCE,
        payload={"vehicle_id": "S-10"},
        correlation_id="corr-mnt-1",
    )

    publisher.publish(event)

    mock_sns.publish.assert_called_once()
    call_kwargs = mock_sns.publish.call_args.kwargs
    assert call_kwargs["TopicArn"] == topic_arn
    assert json.loads(call_kwargs["Message"])["event_type"] == "VehicleWithdrawnForMaintenance"
    attrs = call_kwargs["MessageAttributes"]
    assert attrs["event_type"]["StringValue"] == "VehicleWithdrawnForMaintenance"
    assert attrs["source"]["StringValue"] == "maintenance"
    assert attrs["correlation_id"]["StringValue"] == "corr-mnt-1"
