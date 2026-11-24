"""Puerto EventPublisher y adaptadores InMemory y AWS SNS."""

from typing import Any, Protocol

from shared.events.domain_event import DomainEvent
from shared.events.event_types import EventType


class EventPublisher(Protocol):
    """Puerto de salida para publicar eventos de dominio."""

    def publish(self, event: DomainEvent) -> None:
        """Publica un evento de dominio."""
        ...


class InMemoryEventPublisher:
    """Adaptador en memoria para tests unitarios sin AWS ni LocalStack."""

    def __init__(self) -> None:
        self._events: list[DomainEvent] = []

    @property
    def events(self) -> list[DomainEvent]:
        return list(self._events)

    def publish(self, event: DomainEvent) -> None:
        self._events.append(event)

    def by_type(self, event_type: EventType) -> list[DomainEvent]:
        return [event for event in self._events if event.event_type == event_type]

    def clear(self) -> None:
        self._events.clear()


class SNSEventPublisher:
    """Adaptador real que publica eventos en un topico AWS SNS."""

    def __init__(self, sns_client: Any, topic_arn: str) -> None:
        if not topic_arn.strip():
            msg = "topic_arn must be configured for SNSEventPublisher"
            raise ValueError(msg)
        self._sns_client = sns_client
        self._topic_arn = topic_arn

    def publish(self, event: DomainEvent) -> None:
        """Publica el JSON del evento con atributos para filtrado en SQS."""
        self._sns_client.publish(
            TopicArn=self._topic_arn,
            Message=event.to_json(),
            MessageAttributes={
                "event_type": {
                    "DataType": "String",
                    "StringValue": event.event_type.value,
                },
                "source": {
                    "DataType": "String",
                    "StringValue": event.source,
                },
                "correlation_id": {
                    "DataType": "String",
                    "StringValue": event.correlation_id,
                },
                "schema_version": {
                    "DataType": "String",
                    "StringValue": event.schema_version,
                },
            },
        )
