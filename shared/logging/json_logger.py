"""Logger JSON estructurado con soporte nativo para correlation_id."""

import json
import logging
import sys
from datetime import UTC, datetime
from typing import Any

from shared.logging.correlation import get_correlation_id


class JSONFormatter(logging.Formatter):
    """Formatea cada registro de log en una linea JSON estructurada."""

    def __init__(self, service_name: str) -> None:
        super().__init__()
        self._service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "service": self._service_name,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": get_correlation_id(),
        }
        extra_data = getattr(record, "extra_data", None)
        if isinstance(extra_data, dict):
            log_entry["extra"] = extra_data
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry, ensure_ascii=False, default=str)


def get_logger(
    name: str,
    service_name: str = "urbanmove",
    level: str = "INFO",
) -> logging.Logger:
    """Devuelve un logger configurado con salida JSON hacia stdout."""
    logger = logging.getLogger(name)
    logger.setLevel(level.upper())
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter(service_name=service_name))
        logger.addHandler(handler)
    else:
        for handler in logger.handlers:
            handler.setFormatter(JSONFormatter(service_name=service_name))

    return logger
