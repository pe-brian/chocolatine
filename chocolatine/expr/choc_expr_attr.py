import re
from typing import Any, List, Tuple

from .expr import Expr


class ChocExprAttr(Expr):

    def __init__(
            self,
            obj: Any,
            expr: str
    ) -> None:
        self._expr = expr
        self._obj = obj

    def _get_nested_value(self, obj: Any, keys: List[str]) -> Any:
        for key in keys:
            obj = getattr(obj, key)
        return obj

    def _get_nested_value_from_expr(self, obj: Any, expr: str) -> Any:
        return self._get_nested_value(obj, expr.split("."))

    def _extract_list_expr(self, expr: str) -> Tuple[None | str, str]:
        if m := re.search(r"\$\(([\w.]+)\)", expr):
            if not expr.startswith("$("):
                raise ValueError("$ statement must be placed at the begining")
            return m[0][2:-1], expr[len(m[0]) + 1:]
        return None, expr

    def _get_value(self) -> Any:
        lst_expr, sub_expr = self._extract_list_expr(self._expr)
        val = [str(self._get_nested_value_from_expr(x, sub_expr) if sub_expr else x) for x in self._get_nested_value_from_expr(self._obj, lst_expr)] if lst_expr else \
            str(self._get_nested_value_from_expr(self._obj, self._expr))
        return val

    def build(self) -> str:
        val = self._get_value()
        return ", ".join(x for x in val if x) if isinstance(val, List) else val
