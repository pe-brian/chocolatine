from __future__ import annotations
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .expr.col import Col


def quote_expr(expr: int | float | str | Col | Self) -> str:
    """ Add apostrophes arround a string if it is one, otherwise do nothing """
    if type(expr) is str:
        return f"'{expr}'"
    return expr


def str_to_bool(string: str) -> bool:
    if string == "True":
        return True
    elif string == "False":
        return False
    raise ValueError(f"Unable to cast {string} to a boolean")
