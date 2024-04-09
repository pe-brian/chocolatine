from typing import Any


def quote_expr(expr: Any) -> str:
    """ Add parenthesis arround a string if it is one, otherwise do nothing """
    if type(expr) is str:
        return f"'{expr}'"
    return expr
