from typing import Any


def quote_expr(expr: Any) -> str:
    if type(expr) is str:
        return f"'{expr}'"
    return expr
