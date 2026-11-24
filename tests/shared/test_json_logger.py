"""Tests unitarios para JSONFormatter, get_logger y correlation_context."""

import json
import logging

from shared.logging.correlation import (
    correlation_context,
    ensure_correlation_id,
    get_correlation_id,
)
from shared.logging.json_logger import JSONFormatter, get_logger


def test_json_formatter_includes_correlation_id_and_extra() -> None:
    formatter = JSONFormatter(service_name="reservations")
    record = logging.LogRecord(
        name="reservations.use_case",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Reservation created",
        args=(),
        exc_info=None,
    )
    record.extra_data = {"vehicle_id": "V-7"}

    with correlation_context("corr-log-77"):
        formatted = formatter.format(record)

    parsed = json.loads(formatted)
    assert parsed["level"] == "INFO"
    assert parsed["service"] == "reservations"
    assert parsed["message"] == "Reservation created"
    assert parsed["correlation_id"] == "corr-log-77"
    assert parsed["extra"] == {"vehicle_id": "V-7"}
    assert "timestamp" in parsed


def test_correlation_context_restores_previous_value() -> None:
    assert get_correlation_id() is None
    with correlation_context("outer"):
        assert get_correlation_id() == "outer"
        with correlation_context("inner"):
            assert get_correlation_id() == "inner"
        assert get_correlation_id() == "outer"
    assert get_correlation_id() is None


def test_ensure_correlation_id_generates_and_reuses_value() -> None:
    with correlation_context("existing-id"):
        assert ensure_correlation_id() == "existing-id"


def test_get_logger_does_not_duplicate_handlers() -> None:
    logger1 = get_logger("urbanmove.test.singleton", service_name="rides", level="DEBUG")
    logger2 = get_logger("urbanmove.test.singleton", service_name="rides", level="INFO")
    assert logger1 is logger2
    assert len(logger2.handlers) == 1
    assert logger2.level == logging.INFO
