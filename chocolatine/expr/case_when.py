from typing import Any, Iterable

from typeguard import typechecked

from .expr import Expr
from .col import Col
from ..utils import quote_expr


@typechecked
class CaseWhen(Expr):
    """ 'Case When' expression  """
    def __init__(
            self,
            col: Col | str,
            expected_vals: Iterable[str | int | float],
            returned_vals: Iterable[str | int | float],
            else_returned_val: str | int | float | None = None
    ):
        if len(expected_vals) != len(returned_vals):
            raise ValueError("'conditions' and 'returned_vals' must have the same length")

        if len(returned_vals) == 0:
            raise ValueError("CaseWhen must not be empty")

        self._col = (Col(col) if type(col) is str else col).remove_alias()
        self._items = [(expected_val, returned_val) for expected_val, returned_val in zip(expected_vals, returned_vals)]
        self._else_returned_val = else_returned_val

    def _build_when(self, expected_val, returned_val: Any) -> str:
        return f"WHEN {quote_expr(expected_val)} THEN {quote_expr(returned_val)}"

    def _build_else(self) -> str:
        return f"ELSE {quote_expr(self._else_returned_val)}" if self._else_returned_val else ""

    def build(self) -> str:
        return "\n".join([x for x in [f"CASE {self._col}", *[self._build_when(c, v) for c, v in self._items], self._build_else(), "END"] if x])
