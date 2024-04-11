from __future__ import annotations
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .col import Col

import random
import string


def quote_expr(expr: int | float | str | Col | Self) -> str:
    """ Add parenthesis arround a string if it is one, otherwise do nothing """
    if type(expr) is str:
        return f"'{expr}'"
    return expr


def gen_random_string(length: int) -> str:
    """ Generate a random lowercase alphabetic string """
    if length < 3:
        raise ValueError("You must have a min length of 3")
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
