from __future__ import annotations
from contextvars import ContextVar
from typing import Any, Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .expr.col import Col

_params: ContextVar[list | None] = ContextVar('_params', default=None)


def quote_expr(expr: int | float | str | Col | Self) -> str:
    """ Add apostrophes around a string if it is one, otherwise do nothing.
        In parameterized mode, collects values and returns %s placeholders. """
    params = _params.get()
    if params is not None and type(expr) in (str, int, float, bool):
        params.append(expr)
        return "%s"
    if type(expr) is str:
        return f"'{expr}'"
    return expr


def to_bool(val: Any) -> bool:
    """ Cast any value into boolean """
    if not val or val in ("False", "None"):
        return False
    return True
