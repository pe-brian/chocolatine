from typing import Any, Iterable, List

from typeguard import typechecked

from .expr import Expr
from .condition import Condition
from ..utils import quote_expr


@typechecked
class ConditionalCaseWhen(Expr):
    """ Conditional 'Case When' expression """
    def __init__(
            self,
            conditions: Iterable[Condition],
            returned_vals: Iterable[str | int | float],
            else_returned_val: str | int | float | None = None
    ):
        if len(conditions) != len(returned_vals):
            raise ValueError("'conditions' and 'returned_vals' must have the same length")

        if len(returned_vals) == 0:
            raise ValueError("CaseWhen must not be empty")

        self._items = [(condition, returned_val) for condition, returned_val in zip(conditions, returned_vals)]
        self._else_returned_val = else_returned_val

    def _build_when(self, condition: Condition, returned_val: Any) -> str:
        return f"WHEN {condition} THEN {quote_expr(returned_val)}"

    def _build_else(self) -> str:
        return f"ELSE {quote_expr(self._else_returned_val)}" if self._else_returned_val else ""

    def _build(self) -> List[str]:
        return list(x for x in ["CASE", *[self._build_when(c, v) for c, v in self._items], self._build_else(), "END"] if x)

    def build(self) -> str:
        return "\n".join(self._build())
