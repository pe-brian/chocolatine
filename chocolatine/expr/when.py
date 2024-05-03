from typing import Iterable

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from .condition import Condition
from ..utils import quote_expr


@typechecked
class When(ChocExpr):
    """ Conditional 'Case When' expression """
    def __init__(
            self,
            conditions: Iterable[Condition],
            returned_vals: Iterable[str | int | float],
            else_returned_val: str | int | float | None = None,
            compact: bool = False
    ):
        if len(conditions) != len(returned_vals):
            raise ValueError("'conditions' and 'returned_vals' must have the same length")

        if len(returned_vals) == 0:
            raise ValueError("CaseWhen must not be empty")

        self._items = [(condition, returned_val) for condition, returned_val in zip(conditions, returned_vals)]
        self._when_then_items = [
            f"WHEN {condition} THEN {quote_expr(returned_val)}" for condition, returned_val in zip(conditions, returned_vals)
        ]
        self._else = f"ELSE {quote_expr(else_returned_val)}" if else_returned_val else ""
        super().__init__("CASE\n{$(_when_then_items)~}{_else~}END", compact=compact, list_join_sep="\n")
