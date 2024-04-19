import re
from typing import Any, List, Tuple

from .expr import Expr


class ChocExprAttr(Expr):

    def __init__(
            self,
            obj: Any,
            expr: str,
            list_join_sep: str = ", "
    ) -> None:
        self._expr = expr
        self._obj = obj
        self._list_join_sep = list_join_sep
        self._endline = False

    @property
    def list_join_sep(self) -> str:
        return self._list_join_sep

    @list_join_sep.setter
    def list_join_sep(self, value: str) -> None:
        self._list_join_sep = value

    def _get_nested_value(self, obj: Any, keys: List[str]) -> Any:
        for key in keys:
            obj = getattr(obj, key)
        return obj

    def _get_nested_value_from_expr(self, obj: Any, expr: str) -> Any:
        return self._get_nested_value(obj, expr.split("."))

    def _extract_list_expr(self, expr: str) -> Tuple[None | str, str]:
        if m := re.search(r"\$\(([\w.,~]+)\)", expr):
            if not expr.startswith("$("):
                raise ValueError("$ statement must be placed at the begining")
            return m[0][2:-1], expr[len(m[0]) + 1:]
        return None, expr

    def _check_endline(self) -> bool:
        if "~" in self._expr:
            if self._expr.endswith("~"):
                self._endline = True
                self._expr = self._expr[:-1]
            else:
                raise ValueError("The '~' must be placed at end")

    def _get_value(self) -> Any:
        lst_expr, sub_expr = self._extract_list_expr(self._expr)
        val = [str(self._get_nested_value_from_expr(x, sub_expr) if sub_expr else x) for x in self._get_nested_value_from_expr(self._obj, lst_expr)] if lst_expr else \
            str(self._get_nested_value_from_expr(self._obj, self._expr))
        return val

    def build(self) -> str:
        self._check_endline()
        val = self._get_value()
        expr = self.list_join_sep.join(x for x in val if x) if isinstance(val, List) else val
        if self._endline and expr != "":
            expr += "\n"
        return expr
