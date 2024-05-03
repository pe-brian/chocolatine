from __future__ import annotations
from typing import Any, Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .expr.col import Col


def quote_expr(expr: int | float | str | Col | Self) -> str:
    """ Add apostrophes arround a string if it is one, otherwise do nothing """
    if type(expr) is str:
        return f"'{expr}'"
    return expr


def to_bool(val: Any) -> bool:
    """ Cast any value into boolean """
    if not val or val in ("False", "None"):
        return False
    return True
