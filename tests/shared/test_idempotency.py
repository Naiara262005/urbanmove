"""Tests unitarios para InMemoryProcessedEventsStore."""

from uuid import uuid4

from shared.idempotency.processed_events import InMemoryProcessedEventsStore


def test_mark_as_processed_detects_duplicates() -> None:
    store = InMemoryProcessedEventsStore()
    event_id = uuid4()

    assert store.has_been_processed(event_id) is False
    assert store.mark_as_processed(event_id) is True
    assert store.has_been_processed(event_id) is True
    assert store.mark_as_processed(event_id) is False


def test_clear_resets_processed_events() -> None:
    store = InMemoryProcessedEventsStore()
    event_id = uuid4()

    store.mark_as_processed(event_id)
    store.clear()

    assert store.has_been_processed(event_id) is False
    assert store.mark_as_processed(event_id) is True
