from __future__ import annotations
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .expr.col import Col

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


def flatten(lst):
    """ Flatten a list of list """
    return [x for row in lst for x in row]


def proc_chocolang(expr: str | None) -> str:
    """ Process an expression in chocolanguage into string """
    if not expr:
        return ""
    parts = expr.split("@")
    parts = flatten(list(part.split(";") for part in parts if part))
    parts = list(part.split(":") for part in parts if part)
    res = []
    for part in parts:
        if part[0] == 'False':
            if part[2]:
                res.append(part[2])
        elif part[0] == 'True':
            if part[1]:
                res.append(part[1])
        else:
            if part[0]:
                res.append(part[0])
    return "".join(res)
