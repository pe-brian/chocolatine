import random
import string
from typing import Any


def quote_expr(expr: Any) -> str:
    """ Add parenthesis arround a string if it is one, otherwise do nothing """
    if type(expr) is str:
        return f"'{expr}'"
    return expr


def gen_random_string(length: int) -> str:
    """ Generate a random lowercase alphabetic string """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
