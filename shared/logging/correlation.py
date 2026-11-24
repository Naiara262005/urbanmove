"""Gestion del identificador de correlacion usando ContextVar."""

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar, Token
from uuid import uuid4

_correlation_id_var: ContextVar[str | None] = ContextVar("correlation_id", default=None)


def get_correlation_id() -> str | None:
    """Devuelve el correlation_id activo en el contexto actual, si existe."""
    return _correlation_id_var.get()


def set_correlation_id(correlation_id: str) -> Token[str | None]:
    """Establece el correlation_id en el contexto actual."""
    return _correlation_id_var.set(correlation_id)


def reset_correlation_id(token: Token[str | None]) -> None:
    """Restaura el valor anterior del correlation_id."""
    _correlation_id_var.reset(token)


def ensure_correlation_id() -> str:
    """Devuelve el correlation_id activo o genera uno nuevo si no existe."""
    current = _correlation_id_var.get()
    if current is not None:
        return current
    generated = str(uuid4())
    _correlation_id_var.set(generated)
    return generated


@contextmanager
def correlation_context(correlation_id: str | None = None) -> Iterator[str]:
    """Context manager que propaga un correlation_id y lo restaura al salir."""
    resolved = correlation_id or str(uuid4())
    token = set_correlation_id(resolved)
    try:
        yield resolved
    finally:
        reset_correlation_id(token)
