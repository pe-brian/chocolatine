import re
from typing import Any


# def quote_and_check_expr(expr: str):
#     if expr:
#         if type(expr) is str:
#             if not re.search(r"^[A-Za-z\.\s_]*$", expr):
#                 raise Exception("Invalid expression")
#             return f"'{expr}'"
#         return expr


def quote_expr(expr: Any) -> str:
    if type(expr) is str:
        return f"'{expr}'"
    return expr
